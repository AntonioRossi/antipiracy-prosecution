"""Projections — derived from the schema ship axis, never hand-maintained
(TDD §13). Also derives the reverse index and provenance data at build time
(derived content is never stored).
"""

from . import canon, schema_validate

ROLE_RANK = {"specific": 0, "combination": 1, "context": 2}

# Closed production implementation inventory.  This is deliberately an
# explicit code-side commitment rather than a suffix or directory scan: an
# allowlist entry cannot appoint itself as trusted executable input merely by
# ending in ``.py``.  AC-07 compares this tuple bidirectionally with both the
# filesystem family and every edition declaration.
BUILDER_SOURCE_PATHS = (
    "navigator/build.py",
    "navigator/lib/__init__.py",
    "navigator/lib/authority.py",
    "navigator/lib/qaevidence.py",
    "navigator/lib/recordprovenance.py",
    "navigator/lib/bundleplan.py",
    "navigator/lib/bundlezip.py",
    "navigator/lib/canon.py",
    "navigator/lib/claims.py",
    "navigator/lib/depgraph.py",
    "navigator/lib/gateway.py",
    "navigator/lib/migrate.py",
    "navigator/lib/model.py",
    "navigator/lib/projections.py",
    "navigator/lib/registry.py",
    "navigator/lib/release.py",
    "navigator/lib/render.py",
    "navigator/lib/schema_validate.py",
    "navigator/lib/segmenter.py",
    "navigator/lib/unicode15_1.py",
    "navigator/lib/validate.py",
    "navigator/schema/invariants.py",
)


def artifact_strings(m):
    """Return the exact strings projection capable of affecting an edition.

    Other-edition vocabulary and bundle-only manifest wording are excluded,
    so their changes cannot alter this artifact's provenance.
    """
    strings = m.strings
    return {
        "stringsVersion": strings["stringsVersion"],
        "counselLegend": strings["counselLegend"],
        "standingDisclaimer": strings["standingDisclaimer"],
        "status": strings["status"],
        "role": strings["role"],
        "cautionType": strings["cautionType"],
        "cautionScope": strings["cautionScope"],
        "dispositions": strings["dispositions"],
        "generalizationCodes": strings["generalizationCodes"],
        "ui": strings["ui"],
        "editionNamespace": strings["editionNamespaces"][
            m.edition["stringsNamespace"]],
    }


def ship_relation(m, mode="artifact"):
    """Ship-axis projection of the relation set, with dispositions regrouped
    under their subjects and presentation ordering applied (most specific
    candidate first). mode 'schedule' additionally keeps rationale."""
    proj = schema_validate.ship_axis(m.schemas["relation"], m.relation, mode)
    for frag in proj.get("fragments", {}).values():
        if "targets" in frag:
            frag["targets"] = sorted(
                frag["targets"], key=lambda t: ROLE_RANK.get(t.get("role"), 3))
        for ph in frag.get("phrases", []):
            if "targets" in ph:
                ph["targets"] = sorted(
                    ph["targets"], key=lambda t: ROLE_RANK.get(t.get("role"), 3))
    # dispositions attach under their subjects as (gateId, disposition)
    frag_disp, claim_disp = {}, {}
    for d in m.relation.get("dispositions", []):
        entry = {"gateId": d["gateId"], "disposition": d["disposition"]}
        if d["subject"]["kind"] == "fragment":
            frag_disp.setdefault(d["subject"]["id"], []).append(entry)
        else:
            claim_disp.setdefault(d["subject"]["id"], []).append(entry)
    for fid, entries in frag_disp.items():
        if fid in proj.get("fragments", {}):
            proj["fragments"][fid]["dispositions"] = entries
    proj["claimDispositions"] = claim_disp
    proj.pop("dispositions", None)
    return proj


def reverse_index(ship):
    """Invert the forward relation: block id -> ordered fragment refs
    (claims ascending, units before phrases within a claim). Derived at
    build time; never separately authored (TDD §6.2)."""

    def claim_num(fid):
        return int(fid.split("u")[0][1:])

    def unit_num(fid):
        rest = fid.split("u")[1]
        return int(rest.split("p")[0])

    def phrase_num(fid):
        return int(fid.rsplit("p", 1)[1]) if "p" in fid else -1

    entries = []
    for fid, frag in ship.get("fragments", {}).items():
        for t in frag.get("targets", []):
            entries.append((t["block"], fid, "unit"))
        for ph in frag.get("phrases", []):
            for t in ph.get("targets", []):
                entries.append((t["block"], ph["id"], "phrase"))
    index = {}
    for block, fid, kind in entries:
        index.setdefault(block, [])
        if not any(e["fragment"] == fid for e in index[block]):
            index[block].append({"fragment": fid, "kind": kind})
    for block in index:
        index[block].sort(key=lambda e: (
            claim_num(e["fragment"]),
            0 if e["kind"] == "unit" else 1,
            unit_num(e["fragment"]), phrase_num(e["fragment"])))
    return index


def quotable_texts(m, ship):
    """Pinned quotable source texts referenced by carried gates — derived at
    render from the pinned blocks, never stored (TDD §8.5)."""
    blocks = set()

    def collect(caution):
        if caution and "source" in caution:
            blocks.add(caution["source"]["block"])
    for frag in ship.get("fragments", {}).values():
        collect(frag.get("caution"))
        for t in frag.get("targets", []):
            collect(t.get("caution"))
        for ph in frag.get("phrases", []):
            collect(ph.get("caution"))
            for t in ph.get("targets", []):
                collect(t.get("caution"))
    for gates in ship.get("claimGates", {}).values():
        for g in gates:
            collect(g)
    out = {}
    for b in sorted(blocks):  # deterministic: set iteration is seed-dependent
        anchor = m.quotable_anchor(b)
        if anchor is not None:
            out[b] = anchor.block.canonical
    return out


def provenance(m):
    """Embedded provenance projection (§13): rendered/quotable corpora with
    versions and per-file SHA-256, public authority metadata for the
    authoritative corpus, artifact-input digests, and counts. Internal
    QA-source identifiers, paths, and hashes never appear."""
    corpora = []
    for cid in sorted((m.edition["claimCorpus"], m.edition["targetCorpus"])):
        entry = m.registry.corpora[cid]
        corpora.append({
            "id": cid, "role": entry["role"], "version": entry["version"],
            "files": entry["files"],
        })
    authority_id = m.edition["authorityCorpus"]
    authority_entry = m.registry.entry(authority_id)
    authority = {
        "id": authority_id,
        "version": authority_entry["version"],
        "digest": m.authority_digest,
    }
    log = m.gw.read_log
    return {
        "corpora": corpora,
        "authority": authority,
        "canonVersion": m.binding.get("canonVersion", "c1"),
        "schemaVersion": m.binding.get("schemaVersion", "1"),
        "relationSetDigest": log.get(m.edition["relationSet"]),
        "gateInventoryDigest": log.get(m.edition["gateInventory"]),
        "dependencyMapDigest": log.get(m.edition["dependencyMap"]),
        "editionConfigDigest": log.get(
            "navigator/editions/%s.json" % m.edition["editionId"]),
        "schemaDigest": log.get("navigator/schema/relation.schema.json"),
        "stringsProjectionDigest": canon.bytes_digest(
            canon.canonical_json(artifact_strings(m))),
        "declaredReleaseTimestamp": m.edition["declaredReleaseTimestamp"],
        "counts": {
            "claims": m.edition["census"]["claims"],
            "units": m.edition["census"]["units"],
            "disclosureBlocks": len(m.target_blocks),
        },
    }


def builder_source_paths(inputs):
    """Validate and return the exact production builder-source inventory.

    Python is also used for tests and maintenance tools, so ``*.py`` is not
    itself an implementation boundary.  Missing implementation sources and
    out-of-family Python declarations both fail before any source is read or
    hash-bound.
    """
    declared = {
        path for path in inputs
        if isinstance(path, str) and path.endswith(".py")
    }
    expected = set(BUILDER_SOURCE_PATHS)
    if declared != expected:
        raise ValueError(
            "declared Python source inventory is not exact "
            "(missing=%r, extra=%r)" %
            (sorted(expected - declared), sorted(declared - expected)))
    return BUILDER_SOURCE_PATHS


def builder_tree_hash(gw, inputs):
    """Digest over the exact builder family (embedded provenance).

    Reads cross the content gateway so the private lock covers every selected
    source byte.  Out-of-family declarations are rejected, never absorbed
    into this hash.
    """
    digests = []
    for path in builder_source_paths(inputs):
        digests.append(canon.bytes_digest(gw.read_bytes(path)))
    return canon.composite_digest("aa11393:lock:c1", {"builderTree": digests})
