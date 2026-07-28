"""Snapshot-bracketed current navigator derivation and validation."""

from __future__ import annotations

import io
import os
import posixpath
import re
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from html.parser import HTMLParser
from types import MappingProxyType
from urllib.parse import unquote, urlsplit

from . import acceptance, browserqa, bundlezip, canon, gateway, model, priorart
from . import projections, registry as registry_mod, release, render, snapshot, validate
from . import schema_validate


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROFILE_WORDING_ID = "artifact-label-technical-preview"
TECHNICAL_PREVIEW_LABEL = (
    "TECHNICAL PREVIEW — Pinned Chromium navigator interaction vectors pass; "
    "cross-platform and assistive-technology compatibility is not validated."
)
VALIDATION_PURPOSE = (
    "Technical coherence and deterministic reproducibility of the current "
    "package for independent inventor and counsel review."
)
TECHNICAL_SCOPE = (
    "closed package, artifact, internal-link, reference, and dependency inventories",
    "strict parser, schema, profile, identity, provenance, and digest bindings",
    "deterministic generated representations and delivery products",
    "declared consumer reads and retained handoffs",
    "registered tests executed in an isolated materialization",
    "one unchanged retained worktree capture",
)
NON_PROOF_BOUNDARY = (
    "source authenticity",
    "transcription fidelity",
    "factual or legal correctness",
    "completeness of prior-art or support analysis",
    "inventor confirmation",
    "counsel approval",
    "filing readiness or authorization",
    "entitlement to rely on the package without reviewing its evidence",
)
HUMAN_REVIEW_BOUNDARY = (
    "Human review of source evidence and substantive analysis remains "
    "authoritative; uncertainty, disputed conclusions, draft status, and "
    "not-for-filing labels remain operative."
)
STRUCTURED_TEST_MODULES = (
    "structured_source.tests.test_acceptance",
    "structured_source.tests.test_atomic",
    "structured_source.tests.test_conversion",
    "structured_source.tests.test_pdf_transcription",
    "structured_source.tests.test_registry",
    "structured_source.tests.test_xml_contract",
)
PREFLIGHT_TEST_MODULES = (
    "structured_source.tests.test_acceptance",
)
NAVIGATOR_INPUT_ROOTS = (
    "navigator/bundles/",
    "navigator/editions/",
    "navigator/policy/",
    "navigator/relations/",
    "navigator/schema/",
    "navigator/wording/",
)
NAVIGATOR_FIXED_INPUT_PATHS = frozenset({
    bundlezip.BUNDLE_CONFIG_PATH,
    browserqa.BROWSER_CONTROL_PATH,
    "navigator/schema/acceptance.json",
    "navigator/schema/prior-art-map-acceptance.json",
    "navigator/schema/prior-art-acceptance.json",
    "navigator/schema/edition.schema.json",
    "navigator/schema/navigator-relations.xsd",
    "navigator/schema/wording.xsd",
    "navigator/wording/shared.wording.xml",
})


class CurrentStateError(RuntimeError):
    """The live checkout does not express one exact current navigator state."""

    def __init__(self, message, *, phase=None, check_id=None, subject=None,
                 expected=None, actual=None, remediation=None):
        super().__init__(message)
        self.phase = phase
        self.check_id = check_id
        self.subject = subject
        self.expected = expected
        self.actual = actual
        self.remediation = remediation

    def __str__(self):
        message = super().__str__()
        if self.phase is None:
            return message
        return ("phase=%s check=%s subject=%s expected=%s actual=%s action=%s: %s" %
                (self.phase, self.check_id, self.subject, self.expected,
                 self.actual, self.remediation, message))


def failure_diagnostic(error):
    """Return one stable actionable projection for a validation failure."""
    if not isinstance(error, CurrentStateError):
        raise TypeError("failure diagnostic requires CurrentStateError")
    return {
        "actual": error.actual or str(error),
        "checkId": error.check_id or "unclassifiedFailure",
        "error": str(error.args[0]) if error.args else str(error),
        "expected": error.expected or "the current validation contract passes",
        "phase": error.phase or "validation",
        "remediation": error.remediation or "correct the reported current-state defect",
        "subject": error.subject or "current governed worktree",
    }


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    check_id: str
    subject: str
    expected: str
    actual: str
    remediation: str

    def render(self):
        return ("check=%s subject=%s expected=%s actual=%s action=%s" %
                (self.check_id, self.subject, self.expected, self.actual,
                 self.remediation))


@dataclass(frozen=True, slots=True)
class ValidatedNavigatorSources:
    """One snapshot-bound structured corpus and its frozen navigator inputs."""

    snapshot_digest: str
    capture_token: object
    corpus: object
    consumer_inputs: MappingProxyType

    def __post_init__(self):
        if not isinstance(self.snapshot_digest, str) or \
                not self.snapshot_digest or self.capture_token is None or \
                not isinstance(self.consumer_inputs, MappingProxyType) or \
                not self.consumer_inputs or any(
                    not isinstance(value, registry_mod.ConsumerInput) or
                    key != value.consumer_id or
                    value.snapshot_digest != self.snapshot_digest or
                    value.capture_token is not self.capture_token
                    for key, value in self.consumer_inputs.items()):
            raise CurrentStateError(
                "validated navigator sources are not one frozen capture")

    def input_for(self, consumer_id):
        try:
            value = self.consumer_inputs[consumer_id]
        except KeyError as exc:
            raise CurrentStateError(
                "configured navigator consumer has no validated handoff") from exc
        if value.snapshot_digest != self.snapshot_digest:
            raise CurrentStateError(
                "navigator consumer handoff belongs to another snapshot")
        if value.capture_token is not self.capture_token:
            raise CurrentStateError(
                "navigator consumer handoff belongs to another capture")
        return value


@dataclass(frozen=True, slots=True)
class ProductSpec:
    capture_token: object
    plan_token: object
    product_id: str
    product_kind: str
    edition_id: str
    path: str
    consumer_id: str
    claim_package_id: str
    relation_path: str
    wording_path: str
    artifact_name: str
    declared_timestamp: str
    comparison_package_id: str | None
    passage_map_package_id: str | None

    def __post_init__(self):
        values = (
            self.product_id, self.product_kind, self.edition_id, self.path,
            self.consumer_id, self.claim_package_id, self.wording_path,
            self.artifact_name, self.declared_timestamp,
        )
        if self.capture_token is None or self.plan_token is None or any(
                not isinstance(value, str) or not value for value in values):
            raise CurrentStateError("edition specification is incomplete")


@dataclass(frozen=True, slots=True)
class ProductPlan:
    """Closed product inventory resolved from current bundle and edition data."""

    snapshot_digest: str
    capture_token: object
    plan_token: object
    bundle_config: MappingProxyType
    products: tuple
    by_id: MappingProxyType
    input_paths: frozenset

    def __post_init__(self):
        malformed_products = not isinstance(self.products, tuple) or \
            not self.products or any(
                not isinstance(item, ProductSpec) for item in self.products)
        product_ids = () if malformed_products else tuple(
            item.product_id for item in self.products)
        if not isinstance(self.snapshot_digest, str) or \
                not self.snapshot_digest or self.capture_token is None or \
                self.plan_token is None or \
                not isinstance(self.bundle_config, MappingProxyType) or \
                malformed_products or \
                len(product_ids) != len(set(product_ids)) or \
                not isinstance(self.by_id, MappingProxyType) or \
                not isinstance(self.input_paths, frozenset) or \
                set(self.by_id) != set(product_ids) or \
                any(item.capture_token is not self.capture_token or
                    item.plan_token is not self.plan_token or
                    self.by_id.get(item.product_id) is not item
                    for item in self.products):
            raise CurrentStateError("product plan is not one closed capture")

    def product(self, product_id):
        try:
            return self.by_id[product_id]
        except KeyError as exc:
            raise CurrentStateError("product is absent from the current product plan") from exc

    @property
    def product_ids(self):
        return tuple(item.product_id for item in self.products)

    @property
    def consumer_ids(self):
        return tuple(item.consumer_id for item in self.products)


@dataclass(frozen=True, slots=True)
class ProductState:
    """One immutable edition derivation owned by one capture and plan."""

    capture_token: object
    plan_token: object
    derivation_token: object
    model: object
    html: bytes
    content_lock: gateway.ContentLock
    candidate_name: str

    def __post_init__(self):
        if self.capture_token is None or self.plan_token is None or \
                self.derivation_token is None or \
                not isinstance(self.model, (model.EditionModel,
                                            priorart.PriorArtModel)) or \
                self.model._capture_token is not self.capture_token or \
                self.model._plan_token is not self.plan_token or \
                self.model._derivation_token is not self.derivation_token or \
                not isinstance(self.html, bytes) or \
                not isinstance(self.content_lock, gateway.ContentLock) or \
                self.model.content_lock is not self.content_lock or \
                not isinstance(self.candidate_name, str) or \
                self.candidate_name != release.candidate_name(
                    self.model.artifact_name):
            raise CurrentStateError("product state is not one immutable derivation")


@dataclass(frozen=True, slots=True)
class BundleState:
    """One immutable delivery-bundle derivation over one product state set."""

    capture_token: object
    plan_token: object
    derivation_token: object
    bundle_token: object
    config: MappingProxyType
    config_digest: str
    manifest: bytes
    members: tuple
    origin_inventory: tuple
    states: MappingProxyType
    zip_bytes: bytes

    def __post_init__(self):
        if self.capture_token is None or self.plan_token is None or \
                self.derivation_token is None or self.bundle_token is None or \
                not isinstance(self.config, MappingProxyType) or \
                not isinstance(self.config_digest, str) or \
                not isinstance(self.manifest, bytes) or \
                not isinstance(self.members, tuple) or \
                any(not isinstance(item, tuple) or len(item) != 2 or
                    not isinstance(item[0], str) or not isinstance(item[1], bytes)
                    for item in self.members) or \
                not isinstance(self.origin_inventory, tuple) or \
                not isinstance(self.states, MappingProxyType) or \
                not self.states or \
                not isinstance(self.zip_bytes, bytes) or \
                any(not isinstance(state, ProductState) or
                    state.capture_token is not self.capture_token or
                    state.plan_token is not self.plan_token or
                    state.derivation_token is not self.derivation_token
                    for state in self.states.values()):
            raise CurrentStateError("bundle state is not one immutable derivation")


@dataclass(frozen=True, slots=True)
class CandidateProof:
    """Ephemeral authorization bound to one exact edition derivation."""

    capture_token: object
    plan_token: object
    derivation_token: object
    digest: str

    def __post_init__(self):
        if self.capture_token is None or self.plan_token is None or \
                self.derivation_token is None or \
                re.fullmatch(r"sha256/c1:[0-9a-f]{64}", self.digest or "") \
                is None:
            raise CurrentStateError("candidate proof is malformed")


@dataclass(frozen=True, slots=True)
class ReproductionRequest:
    product_ids: tuple
    include_bundle: bool

    def __post_init__(self):
        if not isinstance(self.product_ids, tuple) or not self.product_ids or \
                any(not isinstance(item, str) or not item
                    for item in self.product_ids) or \
                len(self.product_ids) != len(set(self.product_ids)) or \
                type(self.include_bundle) is not bool:
            raise CurrentStateError("reproduction request is malformed")


def _read_path(relpath, byte_source):
    if not isinstance(relpath, str) or not relpath or \
            posixpath.normpath(relpath) != relpath or \
            relpath.startswith("/") or "\\" in relpath or \
            any(part in {"", ".", ".."} for part in relpath.split("/")):
        raise CurrentStateError("current-state path is not canonical")
    absolute = os.path.join(ROOT, *relpath.split("/"))
    try:
        return byte_source(absolute)
    except (OSError, KeyError, TypeError) as exc:
        raise CurrentStateError("current-state path is unreadable: %s" % relpath) from exc


def _load_json(relpath, byte_source):
    data = _read_path(relpath, byte_source)
    try:
        value = canon.parse_json(data)
    except (ValueError, canon.CanonError) as exc:
        raise CurrentStateError("control is not strict JSON: %s" % relpath) from exc
    if data != canon.canonical_json(value) + b"\n":
        raise CurrentStateError("control JSON is not canonical: %s" % relpath)
    return value


def load_bundle_config(byte_source):
    value = _load_json(bundlezip.BUNDLE_CONFIG_PATH, byte_source)
    try:
        return bundlezip.validate_bundle_config(value)
    except bundlezip.BundleError as exc:
        raise CurrentStateError("bundle configuration is invalid: %s" % exc) from exc


def _parsed_json(relpath, byte_source):
    try:
        return canon.parse_json(_read_path(relpath, byte_source))
    except (ValueError, canon.CanonError) as exc:
        raise CurrentStateError("control is not strict JSON: %s" % relpath) from exc


def _freeze_json(value):
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze_json(item)
                                 for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_json(item) for item in value)
    return value


def load_product_plan(repository_snapshot):
    """Resolve the exact current edition and product inventory from retained data."""
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot):
        raise CurrentStateError("product plan requires a repository snapshot")
    byte_source = repository_snapshot.byte_source()
    config = load_bundle_config(byte_source)
    schema_path = "navigator/schema/edition.schema.json"
    schema = _parsed_json(schema_path, byte_source)
    try:
        schema_validate.check_schema(schema)
    except schema_validate.SchemaError as exc:
        raise CurrentStateError("edition schema is invalid") from exc
    sealed = {
        entry["product"]: entry["name"] for entry in config["members"]
        if entry["kind"] == "sealed"
    }
    plan_token = object()
    products = []
    for product_id in config["products"]:
        path = "navigator/editions/%s.json" % product_id
        value = _parsed_json(path, byte_source)
        problems = schema_validate.validate(value, schema)
        if problems:
            raise CurrentStateError(
                "edition configuration is invalid: %s: %s" %
                (path, "; ".join(problems[:20])))
        edition_id = value["editionId"]
        expected_consumer = ("navigator-" + edition_id
                             if value["productKind"] == "specification"
                             else "navigator-" + product_id)
        common_stale = (
                value["productId"] != product_id or
                value["consumerId"] != expected_consumer or
                value["strategyPrefix"].casefold() != edition_id or
                value["claimPackageId"] != \
                "aa11393us-%s-us-claim-set" % edition_id or
                not value["claimSetVersion"].startswith(
                    value["strategyPrefix"] + "-") or
                value["artifactName"] != sealed.get(product_id) or
                value["declaredReleaseTimestamp"] != config["declaredTimestamp"])
        if value["productKind"] == "specification":
            kind_stale = (
                product_id != edition_id + "-specification" or
                value.get("relationPath") !=
                    "navigator/relations/%s__pct.relations.xml" % edition_id or
                value.get("editionWordingPath") !=
                    "navigator/wording/%s.wording.xml" % edition_id or
                any(field in value for field in (
                    "comparisonPackageId", "passageMapPackageId",
                    "priorArtWordingPath", "documentCensus")))
            relation_path = value["relationPath"]
            wording_path = value["editionWordingPath"]
            comparison_package_id = passage_map_package_id = None
        else:
            kind_stale = (
                product_id != edition_id + "-prior-art" or
                value.get("priorArtWordingPath") !=
                    "navigator/wording/prior-art.wording.xml" or
                value.get("comparisonPackageId") !=
                    "aa11393us-%s-prior-art-comparison-matrix" % edition_id or
                value.get("passageMapPackageId") !=
                    "aa11393us-%s-claim-prior-art-passage-map" % edition_id or
                value.get("documentCensus") != 33 or
                any(field in value for field in (
                    "relationPath", "editionWordingPath")))
            relation_path = ""
            wording_path = value["priorArtWordingPath"]
            comparison_package_id = value["comparisonPackageId"]
            passage_map_package_id = value["passageMapPackageId"]
        if common_stale or kind_stale:
            raise CurrentStateError(
                "product, consumer, source, artifact, or bundle identity differs: %s" %
                product_id)
        products.append(ProductSpec(
            capture_token=repository_snapshot.capture_token,
            plan_token=plan_token,
            product_id=product_id, product_kind=value["productKind"],
            edition_id=edition_id, path=path,
            consumer_id=value["consumerId"],
            claim_package_id=value["claimPackageId"],
            relation_path=relation_path,
            wording_path=wording_path,
            artifact_name=value["artifactName"],
            declared_timestamp=value["declaredReleaseTimestamp"],
            comparison_package_id=comparison_package_id,
            passage_map_package_id=passage_map_package_id,
        ))
    consumer_ids = [item.consumer_id for item in products]
    artifact_names = [item.artifact_name for item in products]
    if len(consumer_ids) != len(set(consumer_ids)) or \
            len(artifact_names) != len(set(name.casefold()
                                           for name in artifact_names)):
        raise CurrentStateError(
            "product plan contains duplicate consumers or artifact identities")
    input_paths = set(NAVIGATOR_FIXED_INPUT_PATHS)
    for item in products:
        input_paths.update((item.path, item.wording_path))
        if item.relation_path:
            input_paths.add(item.relation_path)
    by_id = MappingProxyType({item.product_id: item for item in products})
    return ProductPlan(
        snapshot_digest=repository_snapshot.digest,
        capture_token=repository_snapshot.capture_token,
        plan_token=plan_token,
        bundle_config=_freeze_json(config), products=tuple(products),
        by_id=by_id, input_paths=frozenset(input_paths))


def build_model(edition, repository_snapshot, consumer_input,
                derivation_token):
    """Construct one model from a retained structured-source handoff."""
    if not isinstance(edition, ProductSpec) or \
            not isinstance(repository_snapshot, snapshot.RepositorySnapshot) or \
            derivation_token is None:
        raise CurrentStateError(
            "model construction requires an edition specification and snapshot")
    if not isinstance(consumer_input, registry_mod.ConsumerInput) or \
            consumer_input.snapshot_digest != repository_snapshot.digest or \
            consumer_input.consumer_id != edition.consumer_id or \
            edition.capture_token is not repository_snapshot.capture_token or \
            consumer_input.capture_token is not repository_snapshot.capture_token or \
            edition.plan_token is None:
        raise CurrentStateError(
            "model inputs do not match one repository capture and product plan")
    content_gateway = gateway.ContentGateway(
        ROOT, byte_source=repository_snapshot.byte_source(), allowlist=None)
    try:
        model_type = (model.EditionModel
                      if edition.product_kind == "specification"
                      else priorart.PriorArtModel)
        edition_model = model_type(
            content_gateway, edition.path, consumer_input,
            capture_token=repository_snapshot.capture_token,
            plan_token=edition.plan_token,
            derivation_token=derivation_token)
    except (gateway.GatewayError, model.ModelError,
            registry_mod.RegistryError) as exc:
            raise CurrentStateError(
                "%s typed model could not be constructed: %s" %
                (edition.edition_id, exc)) from exc
    if getattr(edition_model, "product_id", None) != edition.product_id or \
            getattr(edition_model, "edition_id", None) != edition.edition_id or \
            edition_model.artifact_name != edition.artifact_name or \
            edition_model._edition_path != edition.path or \
            edition_model._consumer_id != edition.consumer_id or \
            edition_model._claim_package_id != edition.claim_package_id or \
            (edition.product_kind == "specification" and
             edition_model._relation_path != edition.relation_path) or \
            edition_model._edition_wording_path != edition.wording_path or \
            edition_model.declared_release_timestamp != \
            edition.declared_timestamp:
        raise CurrentStateError(
            "typed model does not match the exact edition specification")
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


def derive(edition, mode, repository_snapshot, consumer_input,
           derivation_token):
    """Return one capture-bound immutable state for a current edition.

    ``release`` intentionally renders the candidate projection: release seals
    those exact bytes rather than creating a second semantic output mode.
    """
    if mode not in {"preview", "candidate", "release"}:
        raise CurrentStateError("derivation mode is not current")
    if not isinstance(edition, ProductSpec) or derivation_token is None:
        raise CurrentStateError("derivation requires a current edition specification")
    edition_model = build_model(
        edition, repository_snapshot, consumer_input, derivation_token)
    problems = validate.validate_product(edition_model)
    if not isinstance(problems, tuple) or any(
            not isinstance(problem, tuple) or len(problem) != 2 or
            not all(isinstance(value, str) and value for value in problem)
            for problem in problems):
        raise CurrentStateError("edition validator returned a malformed result")
    if problems:
        detail = "; ".join("[%s] %s" % problem for problem in problems)
        raise CurrentStateError(
            "%s edition validation failed: %s" %
            (edition.edition_id, detail))
    _validate_model_metadata(edition_model)
    render_mode = "preview" if mode == "preview" else "candidate"
    try:
        html_bytes = render.render(edition_model, mode=render_mode)
    except (KeyError, model.ModelError, RuntimeError, ValueError) as exc:
        raise CurrentStateError(
            "%s renderer failed: %s" % (edition.edition_id, exc)) from exc
    if not isinstance(html_bytes, bytes) or not html_bytes.startswith(b"<!DOCTYPE html>"):
        raise CurrentStateError("renderer did not return a complete HTML5 byte product")
    content_lock = edition_model.content_lock
    if not isinstance(content_lock, gateway.ContentLock) or \
            not isinstance(content_lock.lock_digest, str) or \
            not isinstance(content_lock.reads, tuple):
        raise CurrentStateError("gateway content lock is malformed")
    return ProductState(
        capture_token=repository_snapshot.capture_token,
        plan_token=edition.plan_token,
        derivation_token=derivation_token,
        model=edition_model,
        html=html_bytes,
        content_lock=content_lock,
        candidate_name=release.candidate_name(edition_model.artifact_name),
    )


def _artifact_bytes(name, byte_source):
    release.validate_output_name(name)
    relpath = "navigator/dist/" + name
    return _read_path(relpath, byte_source)


def derive_products(repository_snapshot, products, sources):
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot) or \
            not isinstance(products, tuple) or not products or \
            any(not isinstance(item, ProductSpec) for item in products) or \
            len(products) != len(set(item.product_id for item in products)) or \
            not isinstance(sources, ValidatedNavigatorSources) or \
            sources.snapshot_digest != repository_snapshot.digest or \
            sources.capture_token is not repository_snapshot.capture_token or \
            any(item.capture_token is not repository_snapshot.capture_token
                for item in products) or \
            len({id(item.plan_token) for item in products}) != 1:
        raise CurrentStateError("product derivation inputs are incomplete")
    derivation_token = object()
    states = {}
    for edition in products:
        state = derive(
            edition, "candidate", repository_snapshot,
            sources.input_for(edition.consumer_id), derivation_token)
        states[edition.product_id] = state
    return MappingProxyType(states)


def _manifest_bytes(product_plan, states, artifact_members):
    config = product_plan.bundle_config
    models = [states[product_id].model
              for product_id in product_plan.product_ids]
    if any(item.profile_label != TECHNICAL_PREVIEW_LABEL for item in models):
        raise CurrentStateError("products do not share the current product profile")
    if config["manifestWordingId"] != "bundle-manifest-neutral":
        raise CurrentStateError("bundle manifest wording identity is not current")
    try:
        manifest_text = model.bundle_manifest_text(models)
    except model.ModelError as exc:
        raise CurrentStateError(
            "neutral bundle wording could not be resolved") from exc
    if not manifest_text.strip() or manifest_text != manifest_text.strip():
        raise CurrentStateError("neutral bundle wording is malformed")

    lines = [models[0].profile_label, "", manifest_text, "", "Member checksums:"]
    for name, data in artifact_members:
        lines.append("%s  %s" % (canon.bytes_digest(data), name))
    return ("\n".join(lines) + "\n").encode("utf-8")


def build_bundle_state(repository_snapshot, product_plan, states):
    """Resolve and reproduce the exact configured delivery bundle."""
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot) or \
            not isinstance(product_plan, ProductPlan) or \
            product_plan.snapshot_digest != repository_snapshot.digest or \
            product_plan.capture_token is not repository_snapshot.capture_token:
        raise CurrentStateError(
            "bundle construction requires one snapshot-bound product plan")
    byte_source = repository_snapshot.byte_source()
    config = product_plan.bundle_config
    if not isinstance(states, MappingProxyType):
        raise CurrentStateError("bundle construction requires frozen product states")
    if set(states) != set(product_plan.product_ids):
        raise CurrentStateError("bundle product state is incomplete")
    derivation_tokens = {id(item.derivation_token) for item in states.values()
                         if isinstance(item, ProductState)}
    if len(derivation_tokens) != 1 or any(
            not isinstance(item, ProductState) or
            item.capture_token is not repository_snapshot.capture_token or
            item.plan_token is not product_plan.plan_token
            for item in states.values()):
        raise CurrentStateError(
            "bundle product states cross a capture, plan, or derivation boundary")
    for edition_id in product_plan.product_ids:
        item = states[edition_id]
        if item.model.declared_release_timestamp != config["declaredTimestamp"]:
            raise CurrentStateError(
                "%s release timestamp differs from bundle timestamp" % edition_id)

    artifacts = {}
    ordered_artifact_members = []
    for entry in config["members"][:-1]:
        name = entry["name"]
        if entry["kind"] == "sealed":
            product_id = entry["product"]
            edition_model = states[product_id].model
            if name != edition_model.artifact_name:
                raise CurrentStateError(
                    "%s sealed artifact name differs from its product" % product_id)
            stored = states[product_id].html
            artifacts[name] = stored
        else:
            artifact = entry["artifact"]
            if artifact not in artifacts:
                raise CurrentStateError(
                    "artifact checksum precedes or mismatches its artifact")
            expected_checksum = release.checksum_text(
                artifact, artifacts[artifact])
            stored = expected_checksum
        ordered_artifact_members.append((name, stored))

    manifest = _manifest_bytes(product_plan, states, ordered_artifact_members)
    members = tuple(ordered_artifact_members + [("MANIFEST.txt", manifest)])
    try:
        zip_bytes = bundlezip.build_zip(members, config["declaredTimestamp"])
    except bundlezip.BundleError as exc:
        raise CurrentStateError("deterministic bundle build failed: %s" % exc) from exc
    config_digest = canon.bytes_digest(
        _read_path(bundlezip.BUNDLE_CONFIG_PATH, byte_source))
    bundle_origins = projections.bundle_origin_inventory(
        (states[edition_id].model for edition_id in product_plan.product_ids),
        config, config_digest, bundlezip.BUNDLE_CONFIG_PATH)
    return BundleState(
        capture_token=repository_snapshot.capture_token,
        plan_token=product_plan.plan_token,
        derivation_token=states[product_plan.product_ids[0]].derivation_token,
        bundle_token=object(),
        config=config,
        config_digest=config_digest,
        manifest=manifest,
        members=members,
        origin_inventory=bundle_origins,
        states=states,
        zip_bytes=zip_bytes,
    )


def verify_stored_artifact_members(repository_snapshot, bundle_state):
    """Require stored sealed/checksum bytes to equal one derived bundle state."""
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot) or \
            not isinstance(bundle_state, BundleState) or \
            bundle_state.capture_token is not repository_snapshot.capture_token:
        raise CurrentStateError(
            "stored bundle-member verification inputs are malformed")
    byte_source = repository_snapshot.byte_source()
    for name, expected in bundle_state.members[:-1]:
        actual = _artifact_bytes(name, byte_source)
        if actual != expected:
            raise CurrentStateError(
                "stored bundle member differs from derived bytes: %s" % name)
    return bundle_state


def product_reproduction_projection(states, bundle_state=None):
    """Return the canonical digest projection for one explicit product set."""
    if not isinstance(states, MappingProxyType) or not states:
        raise CurrentStateError("product projection requires frozen product states")
    if any(not isinstance(state, ProductState) or
           product_id != state.model.product_id
           for product_id, state in states.items()) or \
            len({id(state.capture_token) for state in states.values()}) != 1 or \
            len({id(state.plan_token) for state in states.values()}) != 1 or \
            len({id(state.derivation_token) for state in states.values()}) != 1:
        raise CurrentStateError("product projection state is malformed")
    if bundle_state is not None and (
            not isinstance(bundle_state, BundleState) or
            bundle_state.states is not states):
        raise CurrentStateError("product projection bundle state is detached")
    products = {}
    origins = {}
    for edition_id, state in states.items():
        inventory = state.model.origin_inventory
        encoded = [[
            item.value_id, item.kind, item.owner_path,
            item.owner_ref, item.owner_digest,
        ] for item in inventory]
        origin_digest = canon.bytes_digest(canon.canonical_json(encoded))
        origins[edition_id] = origin_digest
        products[edition_id] = {
            "artifactName": state.model.artifact_name,
            "contentLockDigest": state.content_lock.lock_digest,
            "htmlDigest": canon.bytes_digest(state.html),
            "originInventoryDigest": origin_digest,
        }
    bundle = None if bundle_state is None else {
        "bundleOriginInventoryDigest": canon.bytes_digest(canon.canonical_json([
            [item.value_id, item.kind, item.owner_path,
             item.owner_ref, item.owner_digest]
            for item in bundle_state.origin_inventory
        ])),
        "manifestDigest": canon.bytes_digest(bundle_state.manifest),
        "memberDigests": [
            {"digest": canon.bytes_digest(data), "name": name}
            for name, data in bundle_state.members
        ],
        "originInventoryDigests": origins,
        "zipDigest": canon.bytes_digest(bundle_state.zip_bytes),
    }
    return {"bundle": bundle, "products": products}


def prove_candidate(state, stored_candidate, fresh_projection):
    """Bind candidate authorization to one complete fresh projection."""
    if not isinstance(state, ProductState) or \
            not isinstance(stored_candidate, bytes) or \
            not isinstance(fresh_projection, dict):
        raise CurrentStateError("candidate proof inputs are malformed")
    expected_projection = product_reproduction_projection(
        MappingProxyType({state.model.product_id: state}))
    if fresh_projection != expected_projection:
        raise CurrentStateError(
            "fresh candidate projection differs from the retained derivation")
    if stored_candidate != state.html:
        raise CurrentStateError("stored candidate is stale")
    return CandidateProof(
        capture_token=state.capture_token,
        plan_token=state.plan_token,
        derivation_token=state.derivation_token,
        digest=canon.bytes_digest(state.html),
    )


def derive_reproduction_projection(repository_snapshot, product_plan, sources,
                                   request):
    """Derive one requested product projection without implicit work."""
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot) or \
            not isinstance(product_plan, ProductPlan) or \
            product_plan.snapshot_digest != repository_snapshot.digest or \
            product_plan.capture_token is not repository_snapshot.capture_token or \
            not isinstance(sources, ValidatedNavigatorSources) or \
            sources.snapshot_digest != repository_snapshot.digest or \
            sources.capture_token is not repository_snapshot.capture_token or \
            not isinstance(request, ReproductionRequest) or \
            not set(request.product_ids).issubset(product_plan.by_id) or \
            (request.include_bundle and
             request.product_ids != product_plan.product_ids):
        raise CurrentStateError(
            "reproduction request does not match the current product plan")
    bind_sources_to_plan(product_plan, sources)
    products = tuple(product_plan.product(item)
                     for item in request.product_ids)
    states = derive_products(repository_snapshot, products, sources)
    bundle_state = (build_bundle_state(
        repository_snapshot, product_plan, states)
        if request.include_bundle else None)
    return product_reproduction_projection(states, bundle_state)


def reproduce_materialized(request):
    """Execute one complete reproduction session in the current interpreter."""
    if not isinstance(request, ReproductionRequest):
        raise CurrentStateError("materialized reproduction request is malformed")
    repository_snapshot = snapshot.RepositorySnapshot.capture(
        ROOT, retain_bytes=True)
    product_plan = load_product_plan(repository_snapshot)
    sources = validate_structured_corpus(repository_snapshot)
    return derive_reproduction_projection(
        repository_snapshot, product_plan, sources, request)


def fresh_product_projection(root, request, timeout=900):
    """Derive one explicit product set in exactly one fresh interpreter."""
    if not isinstance(request, ReproductionRequest):
        raise CurrentStateError("fresh reproduction request is malformed")
    script = (
        "import sys\n"
        "from navigator.lib import canon,currentstate\n"
        "request=currentstate.ReproductionRequest("
        "tuple(sys.argv[1].split(',')),sys.argv[2]=='bundle')\n"
        "p=currentstate.reproduce_materialized(request)\n"
        "sys.stdout.buffer.write(canon.canonical_json(p)+b'\\n')\n"
    )
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-c", script,
             ",".join(request.product_ids),
             "bundle" if request.include_bundle else "products"], cwd=root,
            capture_output=True, timeout=timeout, env=environment)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CurrentStateError(
            "fresh-process product derivation could not complete") from exc
    if result.returncode:
        raise CurrentStateError(
            "fresh-process product derivation failed: %s" %
            (result.stderr.decode("utf-8", "replace")[-4000:] or
             "no diagnostic"))
    try:
        value = canon.parse_json(result.stdout)
    except (ValueError, canon.CanonError) as exc:
        raise CurrentStateError(
            "fresh-process product projection is malformed") from exc
    if result.stdout != canon.canonical_json(value) + b"\n":
        raise CurrentStateError(
            "fresh-process product projection is not canonical")
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


def _verify_navigator_input_inventory(repository_snapshot, product_plan):
    """Refuse any missing or unowned live navigator semantic/control file."""
    if not isinstance(product_plan, ProductPlan):
        raise CurrentStateError("navigator input inventory requires a product plan")
    actual = {
        entry.path for entry in repository_snapshot.entries
        if entry.path.startswith(NAVIGATOR_INPUT_ROOTS)
    }
    if actual != product_plan.input_paths:
        raise CurrentStateError(
            "navigator live-input inventory differs: missing=%s extra=%s" %
            (sorted(product_plan.input_paths - actual),
             sorted(actual - product_plan.input_paths)))


def validate_structured_corpus(repository_snapshot):
    """Validate all source domains once and freeze every declared handoff."""
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot):
        raise CurrentStateError(
            "structured-source validation requires a repository snapshot")
    try:
        from structured_source.errors import StructuredSourceError
        from structured_source.verify import validate_corpus
        corpus = validate_corpus(
            ROOT, byte_source=repository_snapshot.byte_source(),
            repository_snapshot=repository_snapshot)
        result = corpus.public_result()
        domains = result.get("domains") if isinstance(result, dict) else None
        expected = (
            ("pdf-transcription", "pdf-evidence-transcription-v1"),
            ("authored-markdown", "authored-markdown-v1"),
            ("authored-relations", "authored-relations-v1"),
        )
        if not isinstance(result, dict) or \
                result.get("status") != "passed" or \
                result.get("snapshotDigest") != repository_snapshot.digest or \
                not isinstance(domains, list) or \
                any(not isinstance(item, dict) for item in domains) or tuple(
                    (item.get("domain"), item.get("authorityScheme"))
                    for item in domains) != expected or \
                any(item.get("status") != "passed" for item in domains):
            raise StructuredSourceError(
                "structured-source domain acceptance inventory is not exact")
        inputs = {}
        for consumer_id, handoffs in corpus.consumer_handoffs.items():
            expected_minimum = 3 if consumer_id.endswith("-prior-art") else 2
            if len(handoffs) < expected_minimum or \
                    (not consumer_id.endswith("-prior-art") and
                     len(handoffs) != expected_minimum):
                raise StructuredSourceError(
                    "navigator consumer edge inventory is not exact")
            for handoff in handoffs.values():
                if handoff["inputRepresentation"] != "xml" or \
                        handoff["dependencies"]:
                    raise StructuredSourceError(
                        "navigator consumer does not use direct current XML")
            inputs[consumer_id] = registry_input = registry_mod.ConsumerInput(
                consumer_id=consumer_id,
                snapshot_digest=repository_snapshot.digest,
                capture_token=repository_snapshot.capture_token,
                handoffs=handoffs,
                parser_controls=corpus.parser_controls)
            if registry_input.consumer_id != consumer_id:
                raise StructuredSourceError(
                    "navigator consumer handoff set is malformed")
        return ValidatedNavigatorSources(
            snapshot_digest=repository_snapshot.digest,
            capture_token=repository_snapshot.capture_token,
            corpus=corpus,
            consumer_inputs=MappingProxyType(inputs),
        )
    except (ImportError, OSError, StructuredSourceError) as exc:
        raise CurrentStateError(
            "structured-source current gate failed: %s" % exc) from exc


def bind_sources_to_plan(product_plan, sources):
    """Require exact same-snapshot agreement between products and handoffs."""
    if not isinstance(product_plan, ProductPlan) or \
            not isinstance(sources, ValidatedNavigatorSources) or \
            product_plan.snapshot_digest != sources.snapshot_digest or \
            product_plan.capture_token is not sources.capture_token or \
            set(sources.consumer_inputs) != set(product_plan.consumer_ids):
        raise CurrentStateError(
            "configured product consumers and validated handoffs differ")
    return sources


def verify_current_closure(repository_snapshot, reproduction_root):
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot) or \
            not isinstance(reproduction_root, str) or not reproduction_root:
        raise CurrentStateError(
            "current closure requires a snapshot and isolated reproduction root")
    byte_source = repository_snapshot.byte_source()
    product_plan = load_product_plan(repository_snapshot)
    _verify_navigator_input_inventory(repository_snapshot, product_plan)
    registries = acceptance.load_registries(ROOT, byte_source)
    request = ReproductionRequest(product_plan.product_ids, True)
    with ThreadPoolExecutor(max_workers=1) as fresh_pool:
        fresh_future = fresh_pool.submit(
            fresh_product_projection, reproduction_root, request)
        sources = validate_structured_corpus(repository_snapshot)
        bind_sources_to_plan(product_plan, sources)
        states = derive_products(
            repository_snapshot, product_plan.products, sources)
        bundle_state = build_bundle_state(
            repository_snapshot, product_plan, states)
        verify_stored_artifact_members(repository_snapshot, bundle_state)
        current_projection = product_reproduction_projection(
            states, bundle_state)
        fresh_projection = fresh_future.result()
    if fresh_projection != current_projection:
        raise CurrentStateError(
            "fresh-process products, manifest, origins, or ZIP differ")
    expected_dist = set()
    products = {}
    for edition_id in product_plan.product_ids:
        item = states[edition_id]
        candidate_name = item.candidate_name
        candidate = _artifact_bytes(candidate_name, byte_source)
        if candidate != item.html:
            raise CurrentStateError(
                "%s stored candidate is stale" % edition_id)
        expected_dist.add(candidate_name)
        products[edition_id] = {
            "artifact": item.model.artifact_name,
            "candidateDigest": canon.bytes_digest(item.html),
            "claimSetVersion": item.model.claim_set_version,
            "contentLockDigest": item.content_lock.lock_digest,
        }

    config = bundle_state.config
    expected_dist.update(name for name, unused_data in bundle_state.members[:-1])
    expected_dist.add(config["name"])
    expected_dist.add(config["name"] + ".sha256")
    stored_zip = _artifact_bytes(config["name"], byte_source)
    if stored_zip != bundle_state.zip_bytes:
        raise CurrentStateError("stored delivery bundle is stale")
    try:
        if tuple(bundlezip.read_zip_members(stored_zip)) != bundle_state.members:
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
        "acceptanceRegistries": registries,
        "bundle": {
            "digest": canon.bytes_digest(stored_zip),
            "members": [name for name, unused_data in bundle_state.members],
            "name": config["name"],
        },
        "products": products,
        "structuredSource": sources.corpus.public_result(),
        "testSession": MappingProxyType({
            "models": MappingProxyType({
                edition_id: states[edition_id].model
                for edition_id in product_plan.product_ids
            }),
            "plan": product_plan,
            "snapshot": repository_snapshot,
            "sources": sources,
        }),
    }


def _registered_test_modules():
    return STRUCTURED_TEST_MODULES + acceptance.test_modules()


def _verify_test_module_census(root):
    modules = _registered_test_modules()
    expected_files = {module.replace(".", "/") + ".py" for module in modules}
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


def _run_discovered_tests(root, modules=None, verify_census=True,
                          validation_session=None):
    reports = []
    total = 0
    registered = _registered_test_modules()
    modules = registered if modules is None else tuple(modules)
    if not modules or len(modules) != len(set(modules)) or \
            not set(modules).issubset(registered):
        raise CurrentStateError("requested test-module set is not registered")
    if verify_census:
        _verify_test_module_census(root)
    if os.path.realpath(root) != os.path.realpath(ROOT):
        raise CurrentStateError(
            "registered tests must execute in the active isolated materialization")
    if validation_session is not None:
        from navigator import tests as navigator_tests
        from structured_source import tests as structured_source_tests
        navigator_tests.install_validation_session(validation_session)
        structured_source_tests.install_validated_corpus(
            validation_session["sources"].corpus)
    for module in modules:
        output = io.StringIO()
        suite = unittest.defaultTestLoader.loadTestsFromName(module)
        count = suite.countTestCases()
        if count < 1:
            raise CurrentStateError(
                "registered test census is unavailable for %s" % module)
        def test_ids(value):
            if isinstance(value, unittest.TestSuite):
                return tuple(identifier for item in value
                             for identifier in test_ids(item))
            return (value.id(),)

        exact_tests = test_ids(suite)
        if len(exact_tests) != count or len(set(exact_tests)) != count or \
                any(not identifier.startswith(module + ".")
                    for identifier in exact_tests):
            raise CurrentStateError(
                "registered exact test census is malformed for %s" % module)
        try:
            result = unittest.TextTestRunner(
                stream=output, verbosity=1, failfast=False).run(suite)
        except BaseException as exc:
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
            raise CurrentStateError(
                "registered tests could not complete for %s" % module) from exc
        detail = output.getvalue()
        if not result.wasSuccessful():
            raise CurrentStateError(
                "registered tests failed for %s: %s" %
                (module, detail[-8000:] or "no diagnostic"))
        if result.skipped or result.expectedFailures or \
                result.unexpectedSuccesses:
            raise CurrentStateError(
                "registered tests may not skip or xfail: %s" % module)
        if result.testsRun != count:
            raise CurrentStateError(
                "registered test execution count differs for %s" % module)
        total += count
        reports.append({
            "count": count, "module": module, "tests": list(exact_tests)})
    return {
        "count": total, "modules": reports,
        "tests": [identifier for report in reports
                  for identifier in report["tests"]],
        "status": "passed",
    }


def _combine_test_results(*results):
    modules = [item for result in results for item in result["modules"]]
    if len({item["module"] for item in modules}) != len(modules):
        raise CurrentStateError("registered test module executed more than once")
    return {
        "count": sum(result["count"] for result in results),
        "modules": modules,
        "tests": [identifier for result in results
                  for identifier in result["tests"]],
        "status": "passed",
    }


_TEXT_SUFFIXES = frozenset({
    ".css", ".html", ".json", ".lock", ".md", ".py", ".sh",
    ".toml", ".txt", ".xml", ".xsd", ".yaml", ".yml",
})
_TEXT_FILENAMES = frozenset({".gitignore", ".gitattributes"})
_TRAILING_WHITESPACE_EXEMPT_SUFFIXES = frozenset({".md"})
_TRAILING_WHITESPACE_EXEMPT_ROOTS = ("PCT/office action pct/",)
_LOWER_CONTRACT_DOCUMENTS = (
    "contracts/10-source-surfaces/pdf-transcription/acceptance-criteria.md",
    "contracts/10-source-surfaces/pdf-transcription/technical-description.md",
    "contracts/10-source-surfaces/authored-markdown/acceptance-criteria.md",
    "contracts/10-source-surfaces/authored-markdown/technical-description.md",
    "contracts/20-semantic-relations/authored-relations/acceptance-criteria.md",
    "contracts/20-semantic-relations/authored-relations/technical-description.md",
    "contracts/20-semantic-relations/claim-prior-art-passage-map/acceptance-criteria_DRAFT.md",
    "contracts/20-semantic-relations/claim-prior-art-passage-map/technical-description_DRAFT.md",
)
_SHARED_AGGREGATE_LINK = "](../../README.md#aggregate-validation-boundary)"
_PRODUCT_CONTRACT_DOCUMENTS = (
    "contracts/30-product-generation/claims-navigator/technical-description_DRAFT.md",
    "contracts/30-product-generation/claims-navigator/acceptance-criteria_DRAFT.md",
    "contracts/30-product-generation/claims-prior-art-navigator/technical-description_DRAFT.md",
    "contracts/30-product-generation/claims-prior-art-navigator/acceptance-criteria_DRAFT.md",
)


def _contract_preflight_problems(repository_snapshot):
    """Return all cheap structural contract-boundary defects."""
    issues = []
    for path in _LOWER_CONTRACT_DOCUMENTS:
        try:
            text = repository_snapshot.read_bytes(path).decode("utf-8")
        except (KeyError, UnicodeDecodeError, snapshot.SnapshotError) as exc:
            issues.append(ValidationIssue(
                "contract-aggregate-reference", path,
                "one readable shared aggregate-boundary link", str(exc),
                "restore the current contract document and shared link"))
            continue
        count = text.count(_SHARED_AGGREGATE_LINK)
        if count != 1:
            issues.append(ValidationIssue(
                "contract-aggregate-reference", path,
                "exactly one %s link" % _SHARED_AGGREGATE_LINK,
                "%d links" % count,
                "link this domain contract once to contracts/README.md"))
        command_count = text.casefold().count(
            "python -m navigator validate-current")
        if command_count:
            issues.append(ValidationIssue(
                "contract-command-ownership", path,
                "no duplicated aggregate command", "%d command copies" % command_count,
                "retain only the shared contract-router reference"))
    router_path = "contracts/README.md"
    try:
        router = repository_snapshot.read_bytes(router_path).decode("utf-8")
    except (KeyError, UnicodeDecodeError, snapshot.SnapshotError) as exc:
        issues.append(ValidationIssue(
            "contract-router-boundary", router_path,
            "one readable aggregate boundary", str(exc),
            "restore the current contract router"))
    else:
        heading = "## Aggregate validation boundary"
        target = "](../README.md#validation)"
        required_router_rules = (
            "exactly four authored-relation XML handoffs",
            "exactly two structured-source XML handoffs per specification product",
            "No pair or implementation component is accepted independently.",
        )
        missing_router_rules = tuple(
            rule for rule in required_router_rules if router.count(rule) != 1)
        if router.count(heading) != 1 or router.count(target) != 1 or \
                missing_router_rules:
            issues.append(ValidationIssue(
                "contract-router-boundary", router_path,
                "one aggregate heading, root Validation link, and exact dependency law",
                "headings=%d links=%d missing=%s" %
                (router.count(heading), router.count(target),
                 missing_router_rules),
                "restore the single current aggregate boundary"))
    start = "<!-- CURRENT-VALIDATION-BOUNDARY:START -->"
    end = "<!-- CURRENT-VALIDATION-BOUNDARY:END -->"
    regions = []
    for path in _PRODUCT_CONTRACT_DOCUMENTS:
        try:
            text = repository_snapshot.read_bytes(path).decode("utf-8")
        except (KeyError, UnicodeDecodeError, snapshot.SnapshotError) as exc:
            issues.append(ValidationIssue(
                "product-validation-boundary", path,
                "one readable current validation region", str(exc),
                "restore the current product contract pair"))
            continue
        if text.count(start) != 1 or text.count(end) != 1:
            issues.append(ValidationIssue(
                "product-validation-boundary", path,
                "one start marker and one end marker",
                "starts=%d ends=%d" % (text.count(start), text.count(end)),
                "restore the one current marked validation region"))
            continue
        region = text.split(start, 1)[1].split(end, 1)[0]
        regions.append((path, region))
        if path.endswith("technical-description_DRAFT.md") and text.count(
                "form one indivisible current implementation") != 1:
            issues.append(ValidationIssue(
                "product-implementation-closure", path,
                "one operative indivisible-current-implementation rule",
                "%d rules" % text.count(
                    "form one indivisible current implementation"),
                "restore the product contract implementation-closure rule"))
        command = ("uv --no-cache --offline run --locked --no-sync "
                   "python -m navigator validate-current")
        normalized = " ".join(region.split())
        missing = [phrase for phrase in NON_PROOF_BOUNDARY
                   if phrase not in normalized]
        if region.count(command) != 1 or missing:
            issues.append(ValidationIssue(
                "product-validation-boundary", path,
                "one aggregate command and the complete non-proof boundary",
                "commands=%d missing=%s" % (region.count(command), missing),
                "restore the exact current validation boundary wording"))
    if len(regions) == len(_PRODUCT_CONTRACT_DOCUMENTS) and \
            any(region != regions[0][1] for unused_path, region in regions[1:]):
        issues.append(ValidationIssue(
            "product-validation-boundary", "phase-30 contract pair",
            "byte-identical marked regions", "regions differ",
            "project one exact current boundary into both documents"))
    return issues


def validate_product_contract(repository_snapshot):
    """Bind the operative product pair and registry before any product work."""
    if not isinstance(repository_snapshot, snapshot.RepositorySnapshot):
        raise CurrentStateError(
            "product contract validation requires retained repository bytes")
    issues = _contract_preflight_problems(repository_snapshot)
    if issues:
        issue = issues[0]
        raise CurrentStateError(
            "product contract preflight failed: %s" % issue.render(),
            phase="preflight", check_id=issue.check_id,
            subject=issue.subject, expected=issue.expected,
            actual=issue.actual, remediation=issue.remediation)
    try:
        return acceptance.load_registries(
            ROOT, repository_snapshot.byte_source())
    except acceptance.AcceptanceError as exc:
        raise CurrentStateError(
            "product acceptance pair and registry differ: %s" % exc,
            phase="preflight", check_id="product-acceptance-closure",
            subject="phase-30 contract pair and acceptance registry",
            expected="one exact current acceptance projection",
            actual=str(exc),
            remediation="align the registry and generated acceptance table") \
            from exc


class _RenderedMarkdownInventory(HTMLParser):
    """Collect link targets and anchors from Pandoc's rendered bytes."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors = set()
        self.links = []

    def handle_starttag(self, unused_tag, attrs):
        values = dict(attrs)
        identifier = values.get("id")
        if isinstance(identifier, str) and identifier:
            self.anchors.add(identifier)
        target = values.get("href")
        if isinstance(target, str) and target:
            self.links.append(target)


def _snapshot_whitespace_problems(repository_snapshot):
    """Check textual retained bytes without consulting repository metadata."""
    problems = []
    for entry in repository_snapshot.entries:
        name = posixpath.basename(entry.path)
        suffix = posixpath.splitext(name)[1]
        if suffix not in _TEXT_SUFFIXES and name not in _TEXT_FILENAMES:
            continue
        data = repository_snapshot.read_bytes(entry.path)
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            problems.append("declared text file is not UTF-8: %s" % entry.path)
            continue
        trailing_exempt = suffix in _TRAILING_WHITESPACE_EXEMPT_SUFFIXES or \
            entry.path.startswith(_TRAILING_WHITESPACE_EXEMPT_ROOTS)
        for number, line in enumerate(text.splitlines(), 1):
            if not trailing_exempt and line.endswith((" ", "\t")):
                problems.append("trailing whitespace: %s:%d" %
                                (entry.path, number))
            indentation = line[:len(line) - len(line.lstrip(" \t"))]
            if " \t" in indentation:
                problems.append("space before tab in indentation: %s:%d" %
                                (entry.path, number))
    return problems


def _snapshot_markdown_problems(repository_snapshot, worker_count=1):
    """Render retained Markdown bytes and resolve every local path/fragment.

    The governed corpus contains several multi-megabyte generated tables.
    Serial rendering keeps each bounded Pandoc process within its independent
    timeout while the product-closure phase runs concurrently.
    """
    if type(worker_count) is not int or worker_count < 1 or worker_count > 4:
        raise CurrentStateError("Markdown worker count must be between one and four")
    problems = []
    rendered = {}
    entries = tuple(entry for entry in repository_snapshot.entries
                    if entry.path.endswith(".md"))

    def render_markdown(entry):
        try:
            result = subprocess.run(
                ["pandoc", "--from=gfm", "--to=html"],
                cwd=ROOT, input=repository_snapshot.read_bytes(entry.path),
                capture_output=True, timeout=120)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return None, "pandoc could not render %s: %s" % (entry.path, exc)
        if result.returncode:
            detail = (result.stdout + result.stderr).decode("utf-8", "replace")
            return None, (
                "pandoc failed for %s: %s" %
                (entry.path, detail[-4000:].strip() or "no diagnostic"))
        try:
            parser = _RenderedMarkdownInventory()
            parser.feed(result.stdout.decode("utf-8"))
            parser.close()
        except (UnicodeDecodeError, ValueError) as exc:
            return None, (
                "pandoc output could not be indexed for %s: %s" %
                (entry.path, exc))
        return parser, None

    with ThreadPoolExecutor(max_workers=worker_count,
                            thread_name_prefix="markdown-link") as executor:
        futures = tuple(executor.submit(render_markdown, entry)
                        for entry in entries)
        for entry, future in zip(entries, futures):
            parser, problem = future.result()
            if problem is not None:
                problems.append(problem)
            else:
                rendered[entry.path] = parser

    paths = {entry.path for entry in repository_snapshot.entries}
    directories = {
        prefix
        for path in paths
        for prefix in (
            "/".join(path.split("/")[:count]) + "/"
            for count in range(1, len(path.split("/"))))
    }
    for source_path, parser in sorted(rendered.items()):
        for raw_target in parser.links:
            try:
                target = urlsplit(raw_target)
            except ValueError:
                problems.append(
                    "Markdown link target is malformed: %s -> %s" %
                    (source_path, raw_target))
                continue
            if target.scheme or target.netloc:
                continue
            decoded_path = unquote(target.path)
            fragment = unquote(target.fragment)
            if "\\" in decoded_path or decoded_path.startswith("/"):
                problems.append(
                    "Markdown local link is not canonical: %s -> %s" %
                    (source_path, raw_target))
                continue
            resolved = posixpath.normpath(posixpath.join(
                posixpath.dirname(source_path), decoded_path)) \
                if decoded_path else source_path
            if resolved == "." or resolved == ".." or \
                    resolved.startswith("../"):
                problems.append(
                    "Markdown local link escapes the worktree: %s -> %s" %
                    (source_path, raw_target))
                continue
            is_directory = decoded_path.endswith("/") and \
                resolved.rstrip("/") + "/" in directories
            if resolved not in paths and not is_directory:
                problems.append(
                    "Markdown local link target is absent: %s -> %s" %
                    (source_path, raw_target))
                continue
            if fragment and resolved.endswith(".md"):
                target_inventory = rendered.get(resolved)
                if target_inventory is None or \
                        fragment not in target_inventory.anchors:
                    problems.append(
                        "Markdown local link fragment is absent: %s -> %s" %
                        (source_path, raw_target))
    return problems


def _public_structured_source_result(result):
    """Remove the internal capture binding from the ephemeral public result."""
    return {
        "domains": result["domains"],
        "results": result["results"],
        "status": result["status"],
        "technicalValidationResultVersion": result[
            "technicalValidationResultVersion"],
    }


def _run_phase(phase, check_id, subject, expected, remediation, callback):
    try:
        return callback()
    except CurrentStateError as exc:
        if exc.phase is not None:
            raise
        raise CurrentStateError(
            str(exc), phase=phase, check_id=check_id, subject=subject,
            expected=expected, actual=str(exc), remediation=remediation) from exc
    except Exception as exc:
        raise CurrentStateError(
            str(exc), phase=phase, check_id=check_id, subject=subject,
            expected=expected, actual=type(exc).__name__,
            remediation=remediation) from exc


def _validate_captured_worktree(initial, reproduction_root):
    """Validate one capture using only it and its isolated materialization."""
    if not isinstance(initial, snapshot.RepositorySnapshot) or \
            not isinstance(reproduction_root, str) or not reproduction_root:
        raise CurrentStateError(
            "captured-worktree validation inputs are malformed",
            phase="capture", check_id="capturedWorktreeInputs",
            subject="retained worktree", expected="one retained snapshot and root",
            actual="malformed validation inputs",
            remediation="invoke validation through the aggregate command")
    try:
        initial.validate_retained()
    except snapshot.SnapshotError as exc:
        raise CurrentStateError(
            "retained worktree identity is invalid", phase="capture",
            check_id="retainedWorktreeIdentity", subject="retained worktree",
            expected="every retained path, mode, size, and digest agrees",
            actual=str(exc), remediation="recapture the current worktree") from exc
    for label, check, remediation in (
            ("capturedWhitespace", _snapshot_whitespace_problems,
             "correct the named retained text bytes"),
            ("contractPreflight", _contract_preflight_problems,
             "restore the exact shared contract boundary")):
        problems = _run_phase(
            "preflight", label, "retained worktree", "no structural defects",
            remediation, lambda check=check: check(initial))
        if problems:
            detail = problems[:50]
            if len(problems) > len(detail):
                detail.append("%d additional problems" %
                              (len(problems) - len(detail)))
            rendered = [item.render() if isinstance(item, ValidationIssue)
                        else str(item) for item in detail]
            raise CurrentStateError(
                "; ".join(rendered), phase="preflight", check_id=label,
                subject="retained worktree", expected="no structural defects",
                actual="%d defects" % len(problems),
                remediation=remediation)

    preflight_tests = _run_phase(
        "preflight", "acceptanceContractTests", "acceptance contract tests",
        "the focused contract suite passes and the test census is exact",
        "correct the named acceptance contract or test census defect",
        lambda: _run_discovered_tests(
            reproduction_root, PREFLIGHT_TEST_MODULES, verify_census=True))

    with ThreadPoolExecutor(max_workers=2) as phase_pool:
        markdown_future = phase_pool.submit(
            _run_phase,
            "markdown", "capturedMarkdownLinks", "all retained Markdown",
            "all documents render and every local reference resolves",
            "correct the named Markdown render or reference defect",
            lambda: _snapshot_markdown_problems(initial))
        closure_future = phase_pool.submit(
            _run_phase,
            "product-closure", "currentProductClosure",
            "configured product set",
            "one validated source boundary and byte-identical fresh reproduction",
            "correct the named source, product, or reproduction defect",
            lambda: verify_current_closure(initial, reproduction_root))
        markdown_problems = markdown_future.result()
        final_closure = closure_future.result()
    if markdown_problems:
        detail = markdown_problems[:50]
        if len(markdown_problems) > len(detail):
            detail.append("%d additional problems" %
                          (len(markdown_problems) - len(detail)))
        raise CurrentStateError(
            "; ".join(detail), phase="markdown",
            check_id="capturedMarkdownLinks", subject="all retained Markdown",
            expected="all documents and references pass",
            actual="%d defects" % len(markdown_problems),
            remediation="correct every named Markdown defect")

    remaining_tests = _run_phase(
        "software-tests", "registeredSoftwareTests", "registered test census",
        "every registered test passes without skips",
        "correct the failing registered test",
        lambda: _run_discovered_tests(
            reproduction_root,
            tuple(module for module in _registered_test_modules()
                  if module not in PREFLIGHT_TEST_MODULES),
            verify_census=False,
            validation_session=final_closure["testSession"]))
    test_result = _combine_test_results(preflight_tests, remaining_tests)

    try:
        final = snapshot.RepositorySnapshot.capture(ROOT)
    except snapshot.SnapshotError as exc:
        raise CurrentStateError(
            "final worktree recapture failed", phase="recapture",
            check_id="finalWorktreeCapture", subject="live governed worktree",
            expected="a complete final recapture", actual=str(exc),
            remediation="remove the concurrent filesystem failure and rerun") from exc
    live_changes = initial.differences(final)
    if live_changes:
        raise CurrentStateError(
            "governed worktree changed during validation: %s" %
            "; ".join(live_changes), phase="recapture",
            check_id="worktreeUnchanged", subject="live governed worktree",
            expected="identical initial and final paths, modes, and bytes",
            actual="; ".join(live_changes),
            remediation="stop concurrent writes and validate the resulting current state")

    navigator_tests = tuple(
        identifier for identifier in test_result["tests"]
        if identifier.startswith("navigator.tests."))
    return {
        "acceptance": acceptance.passed_result(
            final_closure["acceptanceRegistries"], navigator_tests),
        "bundle": final_closure["bundle"],
        "checks": {
            "capturedMarkdownLinks": "passed",
            "capturedWhitespace": "passed",
            "contractPreflight": "passed",
            "acceptanceContractTests": "passed",
            "sourceManifests": "passed",
            "softwareTests": test_result,
            "worktreeInventory": "passed",
            "worktreeUnchanged": "passed",
        },
        "products": final_closure["products"],
        "humanReviewBoundary": HUMAN_REVIEW_BOUNDARY,
        "nonProofBoundary": list(NON_PROOF_BOUNDARY),
        "purpose": VALIDATION_PURPOSE,
        "status": "passed",
        "structuredSource": _public_structured_source_result(
            final_closure["structuredSource"]),
        "technicalScope": list(TECHNICAL_SCOPE),
        "validationResultVersion": "4",
    }


def _validate_materialized_worktree():
    """Run inside the retained materialization, never the live worktree."""
    try:
        initial = snapshot.RepositorySnapshot.capture(ROOT, retain_bytes=True)
    except snapshot.SnapshotError as exc:
        raise CurrentStateError(
            "materialized worktree capture failed", phase="capture",
            check_id="materializedWorktreeCapture",
            subject="isolated retained materialization",
            expected="one complete retained-byte capture", actual=str(exc),
            remediation="correct the retained materialization and rerun") from exc
    return _validate_captured_worktree(initial, ROOT)


def validate_current_state():
    """Bracket validation of one live capture by a final live recapture."""
    try:
        initial = snapshot.RepositorySnapshot.capture(ROOT, retain_bytes=True)
        initial.validate_retained()
    except snapshot.SnapshotError as exc:
        raise CurrentStateError(
            "initial worktree capture failed", phase="capture",
            check_id="initialWorktreeCapture", subject="live governed worktree",
            expected="one complete retained-byte capture", actual=str(exc),
            remediation="correct the unreadable path and rerun") from exc

    script = (
        "import sys\n"
        "from navigator.lib import canon,currentstate\n"
        "try:\n"
        " r=currentstate._validate_materialized_worktree()\n"
        "except currentstate.CurrentStateError as exc:\n"
        " sys.stdout.buffer.write(canon.canonical_json("
        "currentstate.failure_diagnostic(exc))+b'\\n')\n"
        " raise SystemExit(1)\n"
        "sys.stdout.buffer.write(canon.canonical_json(r)+b'\\n')\n"
    )
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    validation_error = None
    result = None
    try:
        with tempfile.TemporaryDirectory(
                prefix="aa11393-current-snapshot-") as sandbox_root:
            initial.materialize(sandbox_root)
            completed = subprocess.run(
                [sys.executable, "-B", "-c", script], cwd=sandbox_root,
                capture_output=True, timeout=7200, env=environment)
            if completed.returncode:
                try:
                    diagnostic = canon.parse_json(completed.stdout)
                    if completed.stdout != canon.canonical_json(diagnostic) + b"\n" or \
                            not isinstance(diagnostic, dict) or set(diagnostic) != {
                                "actual", "checkId", "error", "expected", "phase",
                                "remediation", "subject"}:
                        raise ValueError("diagnostic shape is malformed")
                    validation_error = CurrentStateError(
                        diagnostic["error"], phase=diagnostic["phase"],
                        check_id=diagnostic["checkId"],
                        subject=diagnostic["subject"],
                        expected=diagnostic["expected"],
                        actual=diagnostic["actual"],
                        remediation=diagnostic["remediation"])
                except (ValueError, canon.CanonError):
                    detail = (completed.stderr + completed.stdout).decode(
                        "utf-8", "replace").strip()
                    validation_error = CurrentStateError(
                        "isolated retained-worktree validation failed",
                        phase="isolated-validation",
                        check_id="isolatedWorktreeValidation",
                        subject="isolated retained materialization",
                        expected="one canonical actionable result",
                        actual=detail[-12000:] or "no diagnostic",
                        remediation="correct the reported isolated failure and rerun")
            else:
                try:
                    result = canon.parse_json(completed.stdout)
                except (ValueError, canon.CanonError) as exc:
                    validation_error = CurrentStateError(
                        "isolated validation result is malformed",
                        phase="isolated-validation",
                        check_id="isolatedResultShape",
                        subject="isolated validation result",
                        expected="canonical current passed-result JSON",
                        actual=type(exc).__name__,
                        remediation="correct the isolated result projection")
                    validation_error.__cause__ = exc
                if result is not None and completed.stdout != \
                        canon.canonical_json(result) + b"\n":
                    validation_error = CurrentStateError(
                        "isolated validation result is not canonical",
                        phase="isolated-validation",
                        check_id="isolatedResultCanonicalBytes",
                        subject="isolated validation result",
                        expected="one canonical JSON encoding",
                        actual="non-canonical result bytes",
                        remediation="emit the result through the canonical serializer")
    except (OSError, subprocess.TimeoutExpired, snapshot.SnapshotError) as exc:
        validation_error = CurrentStateError(
            "isolated retained-worktree validation could not complete",
            phase="isolated-validation",
            check_id="isolatedWorktreeProcess",
            subject="isolated retained materialization",
            expected="the isolated validation process completes",
            actual=str(exc), remediation="correct the process failure and rerun")
        validation_error.__cause__ = exc

    try:
        final = snapshot.RepositorySnapshot.capture(ROOT)
    except snapshot.SnapshotError as exc:
        raise CurrentStateError(
            "final worktree recapture failed", phase="recapture",
            check_id="finalWorktreeCapture", subject="live governed worktree",
            expected="a complete final recapture", actual=str(exc),
            remediation="remove the concurrent filesystem failure and rerun") from exc
    live_changes = initial.differences(final)
    if live_changes:
        raise CurrentStateError(
            "governed worktree changed during validation: %s" %
            "; ".join(live_changes), phase="recapture",
            check_id="worktreeUnchanged", subject="live governed worktree",
            expected="identical initial and final paths, modes, and bytes",
            actual="; ".join(live_changes),
            remediation="stop concurrent writes and validate the resulting current state") \
            from validation_error
    if validation_error is not None:
        raise validation_error
    if not isinstance(result, dict) or result.get("status") != "passed":
        raise CurrentStateError(
            "isolated validation did not return technical passed status",
            phase="isolated-validation", check_id="isolatedPassedStatus",
            subject="isolated validation result",
            expected="ephemeral technical passed status",
            actual=repr(result), remediation="correct the failed isolated phase")
    return result
