"""Projections — derived from the schema ship axis, never hand-maintained
(TDD §13). Also derives the reverse index and provenance data at build time
(derived content is never stored).
"""

from . import schema_validate

ROLE_RANK = {"specific": 0, "combination": 1, "context": 2}


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
            claim_num(e["fragment"]), unit_num(e["fragment"]),
            0 if e["kind"] == "unit" else 1, e["fragment"]))
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
            collect(g.get("source"))
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
    authority = None
    for cid, entry in m.registry.corpora.items():
        if entry["role"] == "authoritative":
            authority = {
                "id": cid, "version": entry["version"],
                "digest": next(iter(entry["files"].values())),
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
        "stringsDigest": log.get("navigator/strings.json"),
        "declaredReleaseTimestamp": m.edition["declaredReleaseTimestamp"],
        "counts": {
            "claims": m.edition["census"]["claims"],
            "units": m.edition["census"]["units"],
            "disclosureBlocks": len(m.target_blocks),
        },
    }


def builder_tree_hash(gw, inputs):
    """Digest over the builder source files (part of embedded provenance).
    Reads through the gateway so the lock covers the builder tree."""
    from . import canon
    digests = []
    for path in sorted(p for p in inputs
                       if p.endswith(".py")):
        digests.append(canon.bytes_digest(gw.read_bytes(path)))
    return canon.composite_digest("aa11393:lock:c1", {"builderTree": digests})
