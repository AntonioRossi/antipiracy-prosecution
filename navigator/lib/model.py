"""Edition model — everything the validator, projections, and renderer
consume, built once per command through the gateways.

Loads the edition config, registry, profiles, corpora, claims, dependency
map, gate inventory, strings, schemas, and relation set; computes aggregate
claim hashes, dependency-chain hashes, anchor indexes (including table-row
anchors ``S###.rK`` and whole-claim anchors ``PC<n>``), digest ambiguity
sets, and the per-owner review projections whose composite digest is
``review.contentHash`` (TDD §8.2, §8.4, §13).
"""

import json
import re

from . import canon, claims as claims_mod, depgraph, registry as registry_mod
from . import segmenter

PHRASE_ID_RE = re.compile(r"^c(\d+)u(\d+)p(\d+)$")
FRAG_ID_RE = re.compile(r"^c(\d+)u(\d+)$")


class ModelError(RuntimeError):
    pass


def gate_entry_projection(entry):
    """Review projection of a gate-inventory entry: the source block locator
    is excluded (declared locator exception — mechanical re-anchoring never
    invalidates review), its identity covered by source.textHash; appliesTo
    hashes stay included, so applicability changes deliberately cascade to
    the gate's dispositions."""
    return {
        "gateId": entry["gateId"],
        "code": entry["code"],
        "requiredScope": entry["requiredScope"],
        "requirement": entry["requirement"],
        "source": {"textHash": entry["source"]["textHash"]},
        "appliesTo": entry["appliesTo"],
    }


class Anchor:
    __slots__ = ("id", "digest", "kind", "cls", "label", "parent", "block")

    def __init__(self, id_, digest, kind, cls, label, parent=None, block=None):
        self.id = id_
        self.digest = digest
        self.kind = kind
        self.cls = cls
        self.label = label
        self.parent = parent      # parent-container anchor id (rows -> table)
        self.block = block        # owning Block


def _anchor_index(blocks):
    """Anchor id -> Anchor, including row anchors, in document order."""
    anchors = {}
    order = []
    heading = None
    for b in blocks:
        if b.kind == "heading":
            heading = b
        a = Anchor(b.id, b.digest, b.kind, b.cls, b.label,
                   parent=heading.id if heading and heading.id != b.id else None,
                   block=b)
        anchors[b.id] = a
        order.append(a)
        for r in b.rows:
            rid = "%s.%s" % (b.id, r["id"])
            ra = Anchor(rid, r["digest"], "table-row", b.cls,
                        "%s · %s" % (b.label, r["label"]), parent=b.id, block=b)
            anchors[rid] = ra
            order.append(ra)
    return anchors, order


class EditionModel:
    def __init__(self, gw, edition_path):
        self.gw = gw
        self.edition = json.loads(gw.read_text(edition_path))
        allowed = {
            self.edition["claimCorpus"], self.edition["targetCorpus"],
        }
        self.registry = registry_mod.Registry(gw, allowed_corpora=allowed)
        self.strings = json.loads(gw.read_text("navigator/strings.json"))
        self.schemas = {
            "relation": json.loads(gw.read_text("navigator/schema/relation.schema.json")),
            "gates": json.loads(gw.read_text("navigator/schema/gates.schema.json")),
            "deps": json.loads(gw.read_text("navigator/schema/deps.schema.json")),
            "edition": json.loads(gw.read_text("navigator/schema/edition.schema.json")),
        }
        self.planes = json.loads(gw.read_text("navigator/schema/planes.json"))
        self.api_policy = json.loads(gw.read_text("navigator/schema/api-policy.json"))
        self.support_matrix_bytes = gw.read_bytes("navigator/schema/support-matrix.json")
        self.acceptance = json.loads(gw.read_text("navigator/schema/acceptance.json"))

        # target corpus segmentation
        tc = self.edition["targetCorpus"]
        self.target_profile = self.registry.profile(tc)
        self.target_profile_digest = self.gw.read_log[
            self.registry.entry(tc)["profile"]]
        self.target_blocks = segmenter.segment(
            self.registry.primary_text(tc), self.target_profile,
            self.registry.sibling_reader(tc))
        self.target_anchors, self.target_order = _anchor_index(self.target_blocks)

        # claim corpus: guidance segmentation + claims parsing
        cc = self.edition["claimCorpus"]
        self.claim_profile = self.registry.profile(cc)
        self.claim_profile_digest = self.gw.read_log[
            self.registry.entry(cc)["profile"]]
        claim_text = self.registry.primary_text(cc)
        self.guidance_blocks = segmenter.segment(
            claim_text, self.claim_profile, self.registry.sibling_reader(cc))
        self.guidance_anchors, self.guidance_order = _anchor_index(self.guidance_blocks)
        self.claims = claims_mod.parse_claims(
            claim_text, self.claim_profile.get("claimsHeading", "Candidate claims"))
        self.claims_by_number = {c.number: c for c in self.claims}
        self.units = {}
        for c in self.claims:
            for u in c.units:
                self.units[u.id] = u

        # dependency map (dual-sourced) + chain hashes
        self.deps = json.loads(gw.read_text(self.edition["dependencyMap"]))
        self.parents = depgraph.validate(
            self.deps, self.claims, self.edition["independentClaims"])
        self.agg_hashes = {c.number: c.aggregate_hash for c in self.claims}
        self.chain_hashes = {
            n: depgraph.chain_hash(self.parents, self.agg_hashes, n)
            for n in self.agg_hashes
        }

        # gate inventory + relation set
        self.gates = json.loads(gw.read_text(self.edition["gateInventory"]))
        self.gates_by_id = {g["gateId"]: g for g in self.gates["gates"]}
        self.relation = json.loads(gw.read_text(self.edition["relationSet"]))
        self.binding = self.relation.get("binding", {})

        # digest ambiguity over the eligible (targetable) anchor set
        self.digest_positions = {}
        for a in self.target_order:
            if a.cls == "targetable":
                self.digest_positions.setdefault(a.digest, []).append(a.id)

    # -- lookups ----------------------------------------------------------

    def claim_of(self, fragment_id):
        m = FRAG_ID_RE.match(fragment_id) or PHRASE_ID_RE.match(fragment_id)
        if not m:
            raise ModelError("bad fragment id %r" % fragment_id)
        return int(m.group(1))

    def unit_of(self, fragment_id):
        m = PHRASE_ID_RE.match(fragment_id)
        if m:
            return "c%su%s" % (m.group(1), m.group(2))
        return fragment_id

    def target_anchor(self, block_id):
        return self.target_anchors.get(block_id)

    def quotable_anchor(self, block_id):
        a = self.guidance_anchors.get(block_id)
        return a if a is not None and a.cls == "quotable" else None

    def contextual_identity(self, block_id, digest):
        """Contextual identity for an ambiguous covering digest (TDD §13):
        parent-container canonical hash + occurrence index among same-digest
        eligible anchors in document order. None when the digest is unique."""
        positions = self.digest_positions.get(digest, [])
        if len(positions) <= 1:
            return None
        anchor = self.target_anchors.get(block_id)
        if anchor is None or block_id not in positions:
            return None
        parent_id = anchor.parent
        parent = self.target_anchors.get(parent_id) if parent_id else None
        return {
            "parentHash": parent.digest if parent else self.binding.get("targetCorpus", ""),
            "occurrence": positions.index(block_id) + 1,
        }

    def gate_entry_hash(self, gate_id):
        entry = self.gates_by_id.get(gate_id)
        if entry is None:
            raise ModelError("unknown gateId %r" % gate_id)
        return canon.composite_digest("aa11393:inventory:c1",
                                      gate_entry_projection(entry))

    def inventory_digest(self):
        return canon.composite_digest("aa11393:inventory:c1", self.gates)

    # -- review projections (§13) -----------------------------------------

    def _caution_projection(self, caution):
        out = {"type": caution["type"], "code": caution["code"]}
        if "gateId" in caution:
            out["gateId"] = caution["gateId"]
        if "source" in caution:
            out["source"] = {
                "corpus": caution["source"]["corpus"],
                "textHash": caution["source"]["textHash"],
            }
        return out

    def _target_projection(self, target):
        out = {"textHash": target["textHash"], "note": target["note"]}
        if "role" in target:
            out["role"] = target["role"]
        if "rationale" in target:
            out["rationale"] = target["rationale"]
        if "caution" in target:
            out["caution"] = self._caution_projection(target["caution"])
        ctx = self.contextual_identity(target["block"], target["textHash"])
        if ctx is not None:
            out["contextualIdentity"] = ctx
        return out

    def unit_projection(self, fragment_id, frag):
        proj = {
            "identity": {
                "binding": self.binding, "owner": "unit",
                "fragment": fragment_id,
            },
            "dependencyChainHash": self.chain_hashes[self.claim_of(fragment_id)],
            "fragmentTextHash": frag["fragmentTextHash"],
            "status": frag["status"],
        }
        if "targets" in frag:
            proj["targets"] = [self._target_projection(t) for t in frag["targets"]]
        if "caution" in frag:
            proj["caution"] = self._caution_projection(frag["caution"])
        return proj

    def phrase_projection(self, fragment_id, frag, phrase):
        proj = {
            "identity": {
                "binding": self.binding, "owner": "phrase",
                "fragment": fragment_id, "phrase": phrase["id"],
            },
            "dependencyChainHash": self.chain_hashes[self.claim_of(fragment_id)],
            "parentFragmentHash": frag["fragmentTextHash"],
            "text": phrase["text"],
            "occurrence": phrase["occurrence"],
            "status": phrase["status"],
        }
        if "targets" in phrase:
            proj["targets"] = [self._target_projection(t) for t in phrase["targets"]]
        if "caution" in phrase:
            proj["caution"] = self._caution_projection(phrase["caution"])
        return proj

    def claim_gate_projection(self, claim_key, gate):
        return {
            "identity": {
                "binding": self.binding, "owner": "claim-gate",
                "claim": claim_key, "gateId": gate["gateId"],
            },
            "dependencyChainHash": self.chain_hashes[int(claim_key[1:])],
            "claimHash": gate["claimHash"],
            "type": gate["type"],
            "code": gate["code"],
            "source": {
                "corpus": gate["source"]["corpus"],
                "textHash": gate["source"]["textHash"],
            },
        }

    def disposition_projection(self, disp):
        subject = disp["subject"]
        if subject["kind"] == "fragment":
            claim = self.claim_of(subject["id"])
        else:
            claim = int(subject["id"][1:])
        return {
            "identity": {
                "binding": self.binding, "owner": "disposition",
                "gateId": disp["gateId"], "subject": dict(subject),
            },
            "dependencyChainHash": self.chain_hashes[claim],
            "gateEntryHash": disp["gateEntryHash"],
            "subjectHash": disp["subjectHash"],
            "disposition": disp["disposition"],
        }

    def content_hash(self, projection):
        return canon.composite_digest("aa11393:review:c1", projection)

    def iter_owners(self):
        """Yield (owner_type, key, stored_fields, projection) for every
        owner in the relation set."""
        for fid in sorted(self.relation.get("fragments", {})):
            frag = self.relation["fragments"][fid]
            yield "unit", fid, frag, self.unit_projection(fid, frag)
            for ph in frag.get("phrases", []):
                yield ("phrase", ph.get("id", "%s?" % fid), ph,
                       self.phrase_projection(fid, frag, ph))
        for ckey in sorted(self.relation.get("claimGates", {})):
            for gate in self.relation["claimGates"][ckey]:
                yield ("claim-gate", "%s/%s" % (ckey, gate.get("gateId")),
                       gate, self.claim_gate_projection(ckey, gate))
        for disp in self.relation.get("dispositions", []):
            key = "%s@%s" % (disp.get("gateId"), disp.get("subject", {}).get("id"))
            yield "disposition", key, disp, self.disposition_projection(disp)
