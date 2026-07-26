"""Snapshot-bracketed current navigator derivation and validation."""

from __future__ import annotations

import os
import posixpath
import re
import subprocess
import sys
import tempfile

from . import acceptance, bundlezip, canon, gateway, model
from . import projections, release, render, snapshot, validate


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DIST = os.path.join(ROOT, "navigator", "dist")
EDITION_IDS = ("na", "af")
PROFILE_WORDING_ID = "artifact-label-technical-preview"
TECHNICAL_PREVIEW_LABEL = (
    "TECHNICAL PREVIEW — Manual cross-platform and assistive-technology QA "
    "is deferred; browser and assistive-technology compatibility is not "
    "validated."
)
STRUCTURED_TEST_MODULES = (
    "structured_source.tests.test_acceptance",
    "structured_source.tests.test_atomic",
    "structured_source.tests.test_conversion",
    "structured_source.tests.test_pdf_transcription",
    "structured_source.tests.test_registry",
    "structured_source.tests.test_xml_contract",
)
NAVIGATOR_INPUT_ROOTS = (
    "navigator/bundles/",
    "navigator/editions/",
    "navigator/relations/",
    "navigator/schema/",
    "navigator/wording/",
)
NAVIGATOR_INPUT_PATHS = frozenset({
    "navigator/bundles/na-af-2026.json",
    "navigator/editions/af.json",
    "navigator/editions/na.json",
    "navigator/relations/af__pct.relations.xml",
    "navigator/relations/na__pct.relations.xml",
    "navigator/schema/acceptance.json",
    "navigator/schema/edition.schema.json",
    "navigator/schema/navigator-relations.xsd",
    "navigator/schema/wording.xsd",
    "navigator/wording/af.wording.xml",
    "navigator/wording/na.wording.xml",
    "navigator/wording/shared.wording.xml",
})


class CurrentStateError(RuntimeError):
    """The live checkout does not express one exact current navigator state."""


def edition_path(edition_id):
    if edition_id not in EDITION_IDS:
        raise CurrentStateError("edition must be exactly 'na' or 'af'")
    return "navigator/editions/%s.json" % edition_id


def _read_path(relpath, byte_source=None):
    if not isinstance(relpath, str) or not relpath or \
            posixpath.normpath(relpath) != relpath or \
            relpath.startswith("/") or "\\" in relpath or \
            any(part in {"", ".", ".."} for part in relpath.split("/")):
        raise CurrentStateError("current-state path is not canonical")
    absolute = os.path.join(ROOT, *relpath.split("/"))
    try:
        if byte_source is None:
            with open(absolute, "rb") as handle:
                return handle.read()
        return byte_source(absolute)
    except (OSError, KeyError) as exc:
        raise CurrentStateError("current-state path is unreadable: %s" % relpath) from exc


def _load_json(relpath, byte_source=None):
    data = _read_path(relpath, byte_source)
    try:
        value = canon.parse_json(data)
    except (ValueError, canon.CanonError) as exc:
        raise CurrentStateError("control is not strict JSON: %s" % relpath) from exc
    if data != canon.canonical_json(value) + b"\n":
        raise CurrentStateError("control JSON is not canonical: %s" % relpath)
    return value


def load_bundle_config(byte_source=None):
    value = _load_json(bundlezip.BUNDLE_CONFIG_PATH, byte_source)
    try:
        return bundlezip.validate_bundle_config(value)
    except bundlezip.BundleError as exc:
        raise CurrentStateError("bundle configuration is invalid: %s" % exc) from exc


def build_model(edition_id, byte_source=None):
    """Construct the sole immutable edition model through one XML gateway."""
    path = edition_path(edition_id)
    content_gateway = gateway.ContentGateway(
        ROOT, byte_source=byte_source, allowlist=None)
    try:
        edition_model = model.EditionModel(content_gateway, path)
    except (gateway.GatewayError, model.ModelError) as exc:
        raise CurrentStateError(
            "%s typed model could not be constructed: %s" %
            (edition_id, exc)) from exc
    if getattr(edition_model, "edition_id", None) != edition_id:
        raise CurrentStateError("typed model edition identity does not match request")
    return edition_model


def _validate_model_metadata(edition_model):
    for name in (
            "artifact_name", "claim_set_version", "declared_release_timestamp",
            "edition_id", "profile_label", "shared_wording_digest"):
        value = getattr(edition_model, name, None)
        if not isinstance(value, str) or not value:
            raise CurrentStateError("typed model metadata %s is unavailable" % name)
    release.validate_output_name(edition_model.artifact_name)
    if not edition_model.artifact_name.endswith(".html"):
        raise CurrentStateError("typed model artifact name is not HTML")
    try:
        bundlezip.parse_utc_second(edition_model.declared_release_timestamp)
        label = edition_model.controlled_text(PROFILE_WORDING_ID)
    except (bundlezip.BundleError, KeyError, model.ModelError,
            TypeError, ValueError) as exc:
        raise CurrentStateError("typed model product metadata is invalid: %s" % exc) from exc
    if label != TECHNICAL_PREVIEW_LABEL or edition_model.profile_label != label:
        raise CurrentStateError("typed model product label is not the exact current label")


def derive(edition_id, mode, byte_source=None):
    """Return ``(model, html_bytes, content_lock)`` for one current edition.

    ``release`` intentionally renders the candidate projection: release seals
    those exact bytes rather than creating a second semantic output mode.
    """
    if mode not in {"preview", "candidate", "release"}:
        raise CurrentStateError("derivation mode is not current")
    edition_model = build_model(edition_id, byte_source)
    problems = validate.validate_edition(edition_model)
    if not isinstance(problems, tuple) or any(
            not isinstance(problem, tuple) or len(problem) != 2 or
            not all(isinstance(value, str) and value for value in problem)
            for problem in problems):
        raise CurrentStateError("edition validator returned a malformed result")
    if problems:
        detail = "; ".join("[%s] %s" % problem for problem in problems)
        raise CurrentStateError(
            "%s edition validation failed: %s" % (edition_id, detail))
    _validate_model_metadata(edition_model)
    render_mode = "preview" if mode == "preview" else "candidate"
    try:
        html_bytes = render.render(edition_model, mode=render_mode)
    except (KeyError, model.ModelError, RuntimeError, ValueError) as exc:
        raise CurrentStateError(
            "%s renderer failed: %s" % (edition_id, exc)) from exc
    if not isinstance(html_bytes, bytes) or not html_bytes.startswith(b"<!DOCTYPE html>"):
        raise CurrentStateError("renderer did not return a complete HTML5 byte product")
    content_lock = edition_model.content_lock
    if not isinstance(content_lock, dict) or \
            not isinstance(content_lock.get("lockDigest"), str) or \
            not isinstance(content_lock.get("reads"), list):
        raise CurrentStateError("gateway content lock is malformed")
    return edition_model, html_bytes, content_lock


def _artifact_bytes(name, byte_source=None):
    release.validate_output_name(name)
    relpath = "navigator/dist/" + name
    return _read_path(relpath, byte_source)


def _derive_editions(byte_source=None):
    states = {}
    for edition_id in EDITION_IDS:
        edition_model, html_bytes, content_lock = derive(
            edition_id, "candidate", byte_source)
        states[edition_id] = {
            "model": edition_model,
            "html": html_bytes,
            "lock": content_lock,
            "candidateName": release.candidate_name(
                edition_model.artifact_name),
        }
    return states


def _manifest_bytes(config, states, artifact_members):
    models = [states[edition_id]["model"] for edition_id in EDITION_IDS]
    if any(item.profile_label != TECHNICAL_PREVIEW_LABEL for item in models):
        raise CurrentStateError("editions do not share the current product profile")
    if models[0].shared_wording_digest != models[1].shared_wording_digest:
        raise CurrentStateError("editions resolved different shared wording bytes")
    if config["manifestWordingId"] != "bundle-manifest-neutral":
        raise CurrentStateError("bundle manifest wording identity is not current")
    try:
        manifest_text = model.bundle_manifest_text(
            states["na"]["model"], states["af"]["model"])
    except model.ModelError as exc:
        raise CurrentStateError(
            "neutral bundle wording could not be resolved") from exc
    if not manifest_text.strip() or manifest_text != manifest_text.strip():
        raise CurrentStateError("neutral bundle wording is malformed")

    lines = [models[0].profile_label, "", manifest_text, "", "Member checksums:"]
    for name, data in artifact_members:
        lines.append("%s  %s" % (canon.bytes_digest(data), name))
    return ("\n".join(lines) + "\n").encode("utf-8")


def build_bundle_state(byte_source=None, states=None):
    """Resolve and reproduce the exact current five-member delivery bundle."""
    config = load_bundle_config(byte_source)
    states = _derive_editions(byte_source) if states is None else states
    if set(states) != set(EDITION_IDS):
        raise CurrentStateError("bundle edition state is incomplete")
    for edition_id in EDITION_IDS:
        item = states[edition_id]
        if item["model"].declared_release_timestamp != config["declaredTimestamp"]:
            raise CurrentStateError(
                "%s release timestamp differs from bundle timestamp" % edition_id)

    artifacts = {}
    ordered_artifact_members = []
    for entry in config["members"][:-1]:
        name = entry["name"]
        stored = _artifact_bytes(name, byte_source)
        if entry["kind"] == "sealed":
            edition_id = entry["edition"]
            edition_model = states[edition_id]["model"]
            if name != edition_model.artifact_name or \
                    stored != states[edition_id]["html"]:
                raise CurrentStateError(
                    "%s sealed artifact is not the current candidate" % edition_id)
            artifacts[name] = stored
        else:
            artifact = entry["artifact"]
            if artifact not in artifacts:
                raise CurrentStateError(
                    "artifact checksum precedes or mismatches its artifact")
            try:
                release.verify_checksum(stored, artifact, artifacts[artifact])
            except release.ReleaseError as exc:
                raise CurrentStateError(str(exc)) from exc
        ordered_artifact_members.append((name, stored))

    manifest = _manifest_bytes(config, states, ordered_artifact_members)
    members = ordered_artifact_members + [("MANIFEST.txt", manifest)]
    try:
        zip_bytes = bundlezip.build_zip(members, config["declaredTimestamp"])
    except bundlezip.BundleError as exc:
        raise CurrentStateError("deterministic bundle build failed: %s" % exc) from exc
    config_digest = canon.bytes_digest(
        _read_path(bundlezip.BUNDLE_CONFIG_PATH, byte_source))
    bundle_origins = projections.bundle_origin_inventory(
        states["na"]["model"], states["af"]["model"], config,
        config_digest, bundlezip.BUNDLE_CONFIG_PATH)
    return {
        "config": config,
        "configDigest": config_digest,
        "manifest": manifest,
        "members": members,
        "originInventory": bundle_origins,
        "states": states,
        "zip": zip_bytes,
    }


def _bundle_reproduction_projection(bundle_state):
    origins = {}
    for edition_id in EDITION_IDS:
        inventory = bundle_state["states"][edition_id]["model"].origin_inventory
        encoded = [[
            item.value_id, item.kind, item.owner_path,
            item.owner_ref, item.owner_digest,
        ] for item in inventory]
        origins[edition_id] = canon.bytes_digest(canon.canonical_json(encoded))
    return {
        "bundleOriginInventoryDigest": canon.bytes_digest(canon.canonical_json([
            [item.value_id, item.kind, item.owner_path,
             item.owner_ref, item.owner_digest]
            for item in bundle_state["originInventory"]
        ])),
        "manifestDigest": canon.bytes_digest(bundle_state["manifest"]),
        "memberDigests": [
            {"digest": canon.bytes_digest(data), "name": name}
            for name, data in bundle_state["members"]
        ],
        "originInventoryDigests": origins,
        "zipDigest": canon.bytes_digest(bundle_state["zip"]),
    }


def _fresh_bundle_projection(timeout=900):
    script = (
        "import sys\n"
        "from navigator.lib import canon,currentstate\n"
        "s=currentstate.build_bundle_state()\n"
        "p=currentstate._bundle_reproduction_projection(s)\n"
        "sys.stdout.buffer.write(canon.canonical_json(p)+b'\\n')\n"
    )
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-c", script], cwd=ROOT,
            capture_output=True, timeout=timeout, env=environment)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CurrentStateError(
            "fresh-process bundle derivation could not complete") from exc
    if result.returncode:
        raise CurrentStateError(
            "fresh-process bundle derivation failed: %s" %
            (result.stderr.decode("utf-8", "replace")[-4000:] or
             "no diagnostic"))
    try:
        value = canon.parse_json(result.stdout)
    except (ValueError, canon.CanonError) as exc:
        raise CurrentStateError(
            "fresh-process bundle projection is malformed") from exc
    if result.stdout != canon.canonical_json(value) + b"\n":
        raise CurrentStateError(
            "fresh-process bundle projection is not canonical")
    return value


def _dist_inventory(repository_snapshot):
    prefix = "navigator/dist/"
    names = []
    for entry in repository_snapshot.entries:
        if entry.path.startswith(prefix):
            suffix = entry.path[len(prefix):]
            if not suffix or "/" in suffix:
                raise CurrentStateError("navigator/dist is not a flat product directory")
            names.append(suffix)
    if len(names) != len(set(name.casefold() for name in names)):
        raise CurrentStateError("navigator/dist has duplicate path identities")
    return set(names)


def _verify_navigator_input_inventory(repository_snapshot):
    """Refuse any missing or unowned live navigator semantic/control file."""
    actual = {
        entry.path for entry in repository_snapshot.entries
        if entry.path.startswith(NAVIGATOR_INPUT_ROOTS)
    }
    if actual != NAVIGATOR_INPUT_PATHS:
        raise CurrentStateError(
            "navigator live-input inventory differs: missing=%s extra=%s" %
            (sorted(NAVIGATOR_INPUT_PATHS - actual),
             sorted(actual - NAVIGATOR_INPUT_PATHS)))


def _structured_source_result(repository_snapshot):
    try:
        from structured_source.errors import StructuredSourceError
        from structured_source.verify import run_acceptance
        return run_acceptance(
            ROOT, byte_source=repository_snapshot.byte_source(),
            repository_snapshot=repository_snapshot)
    except (ImportError, OSError, StructuredSourceError) as exc:
        raise CurrentStateError(
            "structured-source current gate failed: %s" % exc) from exc


def verify_structured_source(repository_snapshot, consumer_ids):
    """Prove only the requested consumers' authority/conversion closure."""
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot):
        raise CurrentStateError("structured-source proof requires a repository snapshot")
    consumers = tuple(consumer_ids)
    if not consumers or len(consumers) != len(set(consumers)) or \
            not set(consumers).issubset({"navigator-na", "navigator-af"}):
        raise CurrentStateError("structured-source consumer proof request is invalid")
    try:
        from structured_source.errors import StructuredSourceError
        from structured_source.verify import VerificationContext
        context = VerificationContext(
            ROOT, byte_source=repository_snapshot.byte_source(),
            repository_snapshot=repository_snapshot)
        by_id = {item["consumerId"]: item
                 for item in context.registry["consumers"]}
        results = []
        for consumer_id in consumers:
            consumer = by_id.get(consumer_id)
            if consumer is None or len(consumer["edges"]) != 2:
                raise StructuredSourceError(
                    "navigator consumer edge inventory is not exact")
            for edge in consumer["edges"]:
                if edge["inputRepresentation"] != "xml" or \
                        edge["dependencies"] != []:
                    raise StructuredSourceError(
                        "navigator consumer does not use direct current XML")
                checked = context.check(edge["packageId"])
                context.read_for_consumer(consumer_id, edge["packageId"])
                results.append({
                    "consumerId": consumer_id,
                    "packageId": edge["packageId"],
                    "status": checked["status"],
                })
        return {"results": results, "status": "conformant"}
    except (ImportError, OSError, StructuredSourceError) as exc:
        raise CurrentStateError(
            "structured-source consumer closure failed: %s" % exc) from exc


def _verify_current_closure(repository_snapshot, *, reproduce=False):
    byte_source = repository_snapshot.byte_source()
    _verify_navigator_input_inventory(repository_snapshot)
    structured_result = _structured_source_result(repository_snapshot)
    registry = acceptance.load_registry(ROOT, byte_source)
    states = _derive_editions(byte_source)
    expected_dist = set()
    editions = {}
    for edition_id in EDITION_IDS:
        item = states[edition_id]
        candidate_name = item["candidateName"]
        candidate = _artifact_bytes(candidate_name, byte_source)
        if candidate != item["html"]:
            raise CurrentStateError(
                "%s committed candidate is stale" % edition_id)
        if reproduce:
            try:
                fresh = release.fresh_candidate(ROOT, edition_id)
                release.prove_candidate(item["html"], candidate, fresh)
            except release.ReleaseError as exc:
                raise CurrentStateError(
                    "%s fresh-process candidate differs: %s" %
                    (edition_id, exc)) from exc
        expected_dist.add(candidate_name)
        editions[edition_id] = {
            "artifact": item["model"].artifact_name,
            "candidateDigest": canon.bytes_digest(item["html"]),
            "claimSetVersion": item["model"].claim_set_version,
            "contentLockDigest": item["lock"]["lockDigest"],
        }

    bundle_state = build_bundle_state(byte_source, states)
    if reproduce and _fresh_bundle_projection() != \
            _bundle_reproduction_projection(bundle_state):
        raise CurrentStateError(
            "fresh-process manifest, ZIP, or origin inventory differs")
    config = bundle_state["config"]
    expected_dist.update(name for name, unused_data in bundle_state["members"][:-1])
    expected_dist.add(config["name"])
    expected_dist.add(config["name"] + ".sha256")
    stored_zip = _artifact_bytes(config["name"], byte_source)
    if stored_zip != bundle_state["zip"]:
        raise CurrentStateError("committed delivery bundle is stale")
    try:
        if bundlezip.read_zip_members(stored_zip) != bundle_state["members"]:
            raise CurrentStateError("delivery bundle member bytes are stale")
        release.verify_checksum(
            _artifact_bytes(config["name"] + ".sha256", byte_source),
            config["name"], stored_zip)
    except (bundlezip.BundleError, release.ReleaseError) as exc:
        raise CurrentStateError("delivery bundle integrity failed: %s" % exc) from exc
    actual_dist = _dist_inventory(repository_snapshot)
    if actual_dist != expected_dist:
        raise CurrentStateError(
            "navigator/dist inventory differs: missing=%s extra=%s" %
            (sorted(expected_dist - actual_dist),
             sorted(actual_dist - expected_dist)))
    return {
        "acceptanceRegistry": registry,
        "bundle": {
            "digest": canon.bytes_digest(stored_zip),
            "members": [name for name, unused_data in bundle_state["members"]],
            "name": config["name"],
        },
        "editions": editions,
        "structuredSource": structured_result,
    }


def _subprocess_detail(result):
    return "\n".join(
        part.strip() for part in (result.stdout, result.stderr) if part.strip())


def _run_discovered_tests(root):
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    reports = []
    total = 0
    modules = STRUCTURED_TEST_MODULES + tuple(sorted(acceptance.TEST_COVERAGE))
    expected_files = {
        module.replace(".", "/") + ".py" for module in modules
    }
    actual_files = set()
    for test_root in ("structured_source/tests", "navigator/tests"):
        absolute = os.path.join(root, *test_root.split("/"))
        if not os.path.isdir(absolute):
            raise CurrentStateError("test root is absent: %s" % test_root)
        actual_files.update(
            test_root + "/" + name for name in os.listdir(absolute)
            if name.startswith("test_") and name.endswith(".py") and
            os.path.isfile(os.path.join(absolute, name)))
    if actual_files != expected_files:
        raise CurrentStateError(
            "current test-module census differs: missing=%s extra=%s" %
            (sorted(expected_files - actual_files),
             sorted(actual_files - expected_files)))
    for module in modules:
        try:
            with tempfile.TemporaryDirectory(
                    prefix="aa11393-test-pycache-") as pycache:
                result = subprocess.run(
                    [sys.executable, "-B", "-X", "pycache_prefix=" + pycache,
                     "-m", "unittest", module],
                    cwd=root, capture_output=True, text=True, timeout=1800,
                    env=environment)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise CurrentStateError(
                "registered tests could not complete for %s" % module) from exc
        detail = _subprocess_detail(result)
        if result.returncode:
            raise CurrentStateError(
                "registered tests failed for %s: %s" %
                (module, detail[-8000:] or "no diagnostic"))
        if any(marker in detail for marker in (
                "skipped=", "expected failures=", "unexpected successes=")):
            raise CurrentStateError(
                "registered tests may not skip or xfail: %s" % module)
        match = re.search(r"Ran ([0-9]+) tests? in [^\n]+", detail)
        if match is None or int(match.group(1)) < 1:
            raise CurrentStateError(
                "registered test census is unavailable for %s" % module)
        count = int(match.group(1))
        total += count
        reports.append({"count": count, "module": module})
    return {"count": total, "modules": reports, "status": "passed"}


def _git_audit_unit(repository_snapshot):
    """Return the exact clean commit or refuse a non-HEAD live tree."""
    commands = {
        "commit": ["git", "rev-parse", "--verify", "HEAD^{commit}"],
        "status": ["git", "status", "--porcelain=v1", "-z",
                   "--untracked-files=all"],
        "tracked": ["git", "ls-files", "-z", "--cached"],
        "diff": ["git", "diff", "--quiet", "HEAD", "--"],
    }
    results = {}
    for name, command in commands.items():
        try:
            results[name] = subprocess.run(
                command, cwd=ROOT, capture_output=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise CurrentStateError(
                "Git audit command %s could not complete: %s" %
                (name, exc)) from exc
    if results["commit"].returncode or results["diff"].returncode or \
            results["status"].returncode or results["status"].stdout:
        detail = (results["status"].stdout + results["status"].stderr +
                  results["diff"].stderr).decode("utf-8", "replace")
        raise CurrentStateError(
            "audit unit is not one exact clean HEAD commit: %s" %
            (detail.replace("\x00", "; ").strip() or "tracked bytes differ"))
    if results["tracked"].returncode:
        raise CurrentStateError("Git tracked-path census failed")
    try:
        tracked = {
            item.decode("utf-8")
            for item in results["tracked"].stdout.split(b"\x00") if item
        }
        commit = results["commit"].stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise CurrentStateError("Git audit identities are not canonical text") from exc
    snapshot_paths = {entry.path for entry in repository_snapshot.entries}
    if tracked != snapshot_paths:
        raise CurrentStateError(
            "snapshot differs from tracked HEAD paths: missing=%s extra=%s" %
            (sorted(tracked - snapshot_paths)[:20],
             sorted(snapshot_paths - tracked)[:20]))
    if re.fullmatch(r"[0-9a-f]{40,64}", commit) is None:
        raise CurrentStateError("Git commit identity is malformed")
    return commit


def _git_whitespace_problems():
    try:
        empty = subprocess.run(
            ["git", "hash-object", "-t", "tree", "--stdin"], cwd=ROOT,
            input=b"", capture_output=True, timeout=60)
        if empty.returncode:
            return ["Git empty-tree identity is unavailable"]
        empty_tree = empty.stdout.decode("ascii").strip()
        result = subprocess.run(
            ["git", "diff", "--check", empty_tree, "HEAD", "--"], cwd=ROOT,
            capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ["git whitespace check could not complete: %s" % exc]
    if result.returncode:
        return ["git whitespace check failed: %s" %
                (_subprocess_detail(result)[-4000:] or "no diagnostic")]
    return []


def _tracked_markdown_paths():
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "*.md"], cwd=ROOT,
        capture_output=True, timeout=60)
    if result.returncode:
        raise CurrentStateError(
            "tracked-Markdown listing failed: %s" %
            ((result.stdout + result.stderr)[-4000:] or b"no diagnostic"))
    try:
        return sorted(
            item.decode("utf-8") for item in result.stdout.split(b"\0") if item)
    except UnicodeDecodeError as exc:
        raise CurrentStateError("tracked Markdown path is not UTF-8") from exc


def _tracked_markdown_problems():
    try:
        paths = _tracked_markdown_paths()
    except (OSError, subprocess.TimeoutExpired, CurrentStateError) as exc:
        return [str(exc)]
    problems = []
    for relpath in paths:
        absolute = os.path.join(ROOT, *relpath.split("/"))
        if not os.path.exists(absolute):
            continue
        if os.path.islink(absolute) or not os.path.isfile(absolute):
            problems.append("changed Markdown is not a regular file: %s" % relpath)
            continue
        try:
            result = subprocess.run(
                ["pandoc", "--from=gfm", "--to=html", "--output", os.devnull,
                 relpath], cwd=ROOT, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            problems.append(
                "pandoc could not render %s: %s" % (relpath, exc))
            continue
        if result.returncode:
            problems.append(
                "pandoc failed for %s: %s" %
                (relpath, _subprocess_detail(result)[-4000:] or "no diagnostic"))
    return problems


def validate_current_state(run_tests=True):
    """Certify only one final unchanged live snapshot; write nothing."""
    try:
        initial = snapshot.RepositorySnapshot.capture(ROOT, retain_bytes=True)
    except snapshot.SnapshotError as exc:
        raise CurrentStateError("initial repository snapshot failed") from exc
    commit = _git_audit_unit(initial)
    _verify_current_closure(initial)

    for label, check in (
            ("gitWhitespace", _git_whitespace_problems),
            ("trackedMarkdown", _tracked_markdown_problems)):
        problems = check()
        if problems:
            raise CurrentStateError("%s: %s" % (label, "; ".join(problems)))

    test_result = None
    if run_tests:
        try:
            with tempfile.TemporaryDirectory(
                    prefix="aa11393-current-snapshot-") as sandbox_root:
                initial.materialize(sandbox_root)
                sandbox_before = snapshot.RepositorySnapshot.capture(sandbox_root)
                test_result = _run_discovered_tests(sandbox_root)
                sandbox_after = snapshot.RepositorySnapshot.capture(sandbox_root)
                changes = sandbox_before.differences(sandbox_after)
                if changes:
                    raise CurrentStateError(
                        "discovered tests mutated their snapshot: %s" %
                        "; ".join(changes))
        except snapshot.SnapshotError as exc:
            raise CurrentStateError("isolated test snapshot failed") from exc

    before_final = snapshot.RepositorySnapshot.capture(ROOT, retain_bytes=True)
    changes = initial.differences(before_final)
    if changes:
        raise CurrentStateError(
            "live repository changed during validation: %s" % "; ".join(changes))
    final_commit = _git_audit_unit(before_final)
    if final_commit != commit:
        raise CurrentStateError("Git commit changed during validation")
    final_closure = _verify_current_closure(before_final, reproduce=True)
    final = snapshot.RepositorySnapshot.capture(ROOT)
    changes = initial.differences(final)
    if changes:
        raise CurrentStateError(
            "live repository changed before certification: %s" %
            "; ".join(changes))

    result = {
        "bundle": final_closure["bundle"],
        "checks": {
            "trackedMarkdown": "passed",
            "gitCommit": commit,
            "gitWhitespace": "passed",
            "repositorySnapshot": final.digest,
            "sourceManifests": "passed",
        },
        "editions": final_closure["editions"],
        "status": "current" if run_tests else "closure-conformant",
        "structuredSource": final_closure["structuredSource"],
        "validationResultVersion": "2",
    }
    if run_tests:
        navigator_modules = tuple(
            item["module"] for item in test_result["modules"]
            if item["module"].startswith("navigator.tests."))
        result["acceptance"] = acceptance.passed_result(
            final_closure["acceptanceRegistry"], navigator_modules)
        result["checks"]["softwareTests"] = test_result
    return result
