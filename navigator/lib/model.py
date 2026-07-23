"""Edition model — everything the validator, projections, and renderer
consume, built once per command through the gateways.

Loads the edition config, registry, profiles, corpora, claims, dependency
map, gate inventory, strings, schemas, and relation set; computes aggregate
claim hashes, dependency-chain hashes, anchor indexes (including table-row
anchors ``S###.rK`` and whole-claim anchors ``PC<n>``), digest ambiguity
sets, and the per-owner review projections whose composite digest is
``review.contentHash`` (TDD §8.2, §8.4, §13).
"""

import re

from . import canon, claims as claims_mod, depgraph, gateway
from . import registry as registry_mod, schema_validate, segmenter

PHRASE_ID_RE = re.compile(r"^c(\d+)u(\d+)p(\d+)$")
FRAG_ID_RE = re.compile(r"^c(\d+)u(\d+)$")


class ModelError(RuntimeError):
    pass


def gate_entry_projection(entry, source_context=None):
    """Review projection of a gate-inventory entry: the source block locator
    is excluded (declared locator exception — mechanical re-anchoring never
    invalidates review), its identity covered by source.textHash and, when
    that digest repeats in the quotable set, computed contextual identity;
    appliesTo hashes stay included, so applicability changes deliberately
    cascade to the gate's dispositions.

    ``source_context`` is computed from the pinned corpus by
    :class:`EditionModel`; it is never authored into the inventory.  Keeping
    this small pure helper public is useful for synthetic fixture generation,
    where a source is known to be unique and no context is required.
    """
    source = {"textHash": entry["source"]["textHash"]}
    if source_context is not None:
        source["contextualIdentity"] = source_context
    return {
        "gateId": entry["gateId"],
        "code": entry["code"],
        "requiredScope": entry["requiredScope"],
        "requirement": entry["requirement"],
        "source": source,
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
    claim_headings = {}
    for b in blocks:
        if b.kind == "heading":
            heading = b
        if b.kind in ("claim-head", "claim-element") and b.meta.get("pctClaim"):
            claim_number = b.meta["pctClaim"]
            if heading is not None:
                claim_headings.setdefault(claim_number, heading.id)
            parent = "PC%d" % claim_number
        elif b.kind == "claim-whole":
            # Whole-claim anchors contain their members.  Parenting a whole
            # claim back to its first member creates a two-node cycle, so use
            # the real Claims section captured while parsing those members.
            parent = claim_headings.get(b.meta.get("pctClaim"))
        else:
            parent = heading.id if heading and heading.id != b.id else None
        a = Anchor(b.id, b.digest, b.kind, b.cls, b.label,
                   parent=parent, block=b)
        if b.id in anchors:
            raise ModelError("duplicate anchor id %r" % b.id)
        anchors[b.id] = a
        order.append(a)
        for r in b.rows:
            rid = "%s.%s" % (b.id, r["id"])
            ra = Anchor(rid, r["digest"], "table-row", b.cls,
                        "%s · %s" % (b.label, r["label"]), parent=b.id, block=b)
            if rid in anchors:
                raise ModelError("duplicate anchor id %r" % rid)
            anchors[rid] = ra
            order.append(ra)
    return anchors, order


class EditionModel:
    def __init__(self, gw, edition_path):
        self.gw = gw
        self.edition = canon.parse_json(gw.read_text(edition_path))
        # The edition object selects every subsequent path.  Validate its
        # closed shape before dereferencing any selector so malformed source
        # data fails as a schema defect rather than escaping into a KeyError
        # (and so authoring commands such as migrate cannot consume an
        # unvalidated parameter set).
        edition_schema = canon.parse_json(gw.read_text(
            "navigator/schema/edition.schema.json"))
        try:
            schema_validate.check_schema(edition_schema)
        except schema_validate.SchemaError as exc:
            raise ModelError("invalid edition schema: %s" % exc)
        edition_errors = schema_validate.validate(
            self.edition, edition_schema)
        if edition_errors:
            raise ModelError("invalid edition config: %s" %
                             "; ".join(edition_errors))
        allowed = {
            self.edition["claimCorpus"], self.edition["targetCorpus"],
            self.edition["authorityCorpus"],
        }
        self.registry = registry_mod.Registry(
            gw, registry_paths=self.edition["corpusRegistries"],
            allowed_corpora=allowed, require_exact=True)
        self._qa_registry = None
        for field, expected_role in (
                ("claimCorpus", "fragment-source"),
                ("targetCorpus", "derivative")):
            corpus_id = self.edition[field]
            corpus_entry = self.registry.entry(corpus_id)
            if corpus_entry["role"] != expected_role or \
                    corpus_entry["visibility"] != "rendered":
                raise ModelError(
                    "%s %r must be role %r with rendered visibility"
                    % (field, corpus_id, expected_role))
        authority_id = self.edition["authorityCorpus"]
        authority_entry = self.registry.entry(authority_id)
        if authority_entry["role"] != "authoritative":
            raise ModelError("authorityCorpus %r is not authoritative"
                             % authority_id)
        authority_bytes = self.registry.read_file(
            authority_id, authority_entry["primary"])
        self.authority_digest = canon.bytes_digest(authority_bytes)
        shared_strings = canon.parse_json(
            gw.read_text("navigator/strings.json"))
        edition_strings = canon.parse_json(
            gw.read_text(self.edition["stringsResource"]))
        expected_shared_string_fields = {
            "stringsVersion", "comment", "counselLegend",
            "standingDisclaimer", "status", "role", "cautionType",
            "cautionScope", "dispositions", "migrationReasons",
            "generalizationCodes", "ui",
        }
        if set(shared_strings) != expected_shared_string_fields or \
                canon.require_version(shared_strings, "stringsVersion", "1"):
            raise ModelError(
                "shared strings fields/version do not match the closed "
                "artifact-microcopy resource")
        expected_string_fields = {
            "stringsVersion", "namespace", "sourceGateCodes",
        }
        if set(edition_strings) != expected_string_fields:
            raise ModelError(
                "edition strings fields must be exactly %r"
                % sorted(expected_string_fields))
        namespace = self.edition["stringsNamespace"]
        if edition_strings["namespace"] != namespace:
            raise ModelError(
                "edition strings namespace %r does not match %r"
                % (edition_strings["namespace"], namespace))
        if edition_strings["stringsVersion"] != \
                shared_strings.get("stringsVersion"):
            raise ModelError("shared and edition strings versions differ")
        source_codes = edition_strings["sourceGateCodes"]
        if not isinstance(source_codes, dict) or not all(
                isinstance(code, str) and code.strip() and
                isinstance(label, str) and label.strip()
                for code, label in source_codes.items()):
            raise ModelError(
                "edition sourceGateCodes must map non-empty strings")
        self.strings = dict(shared_strings)
        # Preserve the renderer-facing shape while exposing only the selected
        # namespace.  No other edition's authored strings enter this model.
        self.strings["editionNamespaces"] = {
            namespace: {"sourceGateCodes": source_codes},
        }
        self.schemas = {
            "relation": canon.parse_json(gw.read_text(
                "navigator/schema/relation.schema.json")),
            "gates": canon.parse_json(gw.read_text(
                "navigator/schema/gates.schema.json")),
            "deps": canon.parse_json(gw.read_text(
                "navigator/schema/deps.schema.json")),
            "edition": edition_schema,
            "support-matrix": canon.parse_json(gw.read_text(
                "navigator/schema/support-matrix.schema.json")),
            "segmentation-profile": canon.parse_json(gw.read_text(
                "navigator/schema/segmentation-profile.schema.json")),
        }
        try:
            for schema_name, schema in self.schemas.items():
                schema_validate.check_schema(schema)
        except schema_validate.SchemaError as exc:
            raise ModelError("invalid %s schema: %s" %
                             (schema_name, exc))
        relation_schema = self.schemas["relation"]
        self.review_schemas = {
            "binding": relation_schema["properties"]["binding"],
            "unit": next(iter(relation_schema["properties"]["fragments"]
                              ["patternProperties"].values())),
            "phrase": relation_schema["definitions"]["phrase"],
            "target": relation_schema["definitions"]["target"],
            "claim-gate": next(iter(
                relation_schema["properties"]["claimGates"]
                ["patternProperties"].values()))["items"],
            "disposition": relation_schema["properties"]["dispositions"]
            ["items"],
        }
        self.planes = canon.parse_json(gw.read_text(
            "navigator/schema/planes.json"))
        planes_errors = canon.require_version(
            self.planes, "planesVersion", "1")
        if planes_errors:
            raise ModelError("invalid planes: %s" % "; ".join(planes_errors))
        self.api_policy = canon.parse_json(gw.read_text(
            "navigator/schema/api-policy.json"))
        self.support_matrix_bytes = gw.read_bytes(
            "navigator/schema/support-matrix.json")
        self.support_matrix = canon.parse_json(self.support_matrix_bytes)
        support_errors = schema_validate.validate(
            self.support_matrix, self.schemas["support-matrix"])
        if support_errors:
            raise ModelError("invalid support matrix: %s" %
                             "; ".join(support_errors))
        self.release_policy = canon.parse_json(gw.read_text(
            "navigator/schema/release-policy.json"))

        # target corpus segmentation
        tc = self.edition["targetCorpus"]
        self.target_profile = self.registry.profile(tc)
        profile_errors = schema_validate.validate(
            self.target_profile, self.schemas["segmentation-profile"])
        profile_errors.extend(segmenter.profile_problems(
            self.target_profile, tc))
        if profile_errors:
            raise ModelError("invalid target segmentation profile: %s" %
                             "; ".join(profile_errors))
        self.target_profile_digest = self.gw.read_log[
            self.registry.entry(tc)["profile"]]
        target_text = self.registry.primary_text(tc)
        self.target_root_hash = canon.text_digest(canon.canon_prose(target_text))
        self.target_blocks = segmenter.segment(
            target_text, self.target_profile,
            self.registry.sibling_reader(tc))
        self.target_anchors, self.target_order = _anchor_index(self.target_blocks)

        # claim corpus: guidance segmentation + claims parsing
        cc = self.edition["claimCorpus"]
        self.claim_profile = self.registry.profile(cc)
        profile_errors = schema_validate.validate(
            self.claim_profile, self.schemas["segmentation-profile"])
        profile_errors.extend(segmenter.profile_problems(
            self.claim_profile, cc))
        if profile_errors:
            raise ModelError("invalid claim segmentation profile: %s" %
                             "; ".join(profile_errors))
        self.claim_profile_digest = self.gw.read_log[
            self.registry.entry(cc)["profile"]]
        claim_text = self.registry.primary_text(cc)
        self.guidance_root_hash = canon.text_digest(
            canon.canon_prose(claim_text))
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
        self.deps = canon.parse_json(gw.read_text(
            self.edition["dependencyMap"]))
        dependency_errors = schema_validate.validate(
            self.deps, self.schemas["deps"])
        if dependency_errors:
            raise ModelError("invalid dependency map: %s" %
                             "; ".join(dependency_errors))
        document_table = claims_mod.parse_dependency_table(claim_text)
        self.parents = depgraph.validate(
            self.deps, self.claims, self.edition["independentClaims"],
            document_table=document_table)
        self.agg_hashes = {c.number: c.aggregate_hash for c in self.claims}
        self.chain_hashes = {
            n: depgraph.chain_hash(self.parents, self.agg_hashes, n)
            for n in self.agg_hashes
        }

        # gate inventory + relation set
        self.gates = canon.parse_json(gw.read_text(
            self.edition["gateInventory"]))
        gate_errors = schema_validate.validate(
            self.gates, self.schemas["gates"])
        if gate_errors:
            raise ModelError("invalid gate inventory: %s" %
                             "; ".join(gate_errors))
        self.gates_by_id = {g["gateId"]: g for g in self.gates["gates"]}
        self.relation = canon.parse_json(gw.read_text(
            self.edition["relationSet"]))
        relation_errors = schema_validate.validate(
            self.relation, self.schemas["relation"])
        if relation_errors:
            raise ModelError("invalid relation set: %s" %
                             "; ".join(relation_errors))
        self.binding = self.relation.get("binding", {})

        # digest ambiguity over the eligible (targetable) anchor set
        self.digest_positions = {}
        for a in self.target_order:
            if a.cls == "targetable":
                self.digest_positions.setdefault(a.digest, []).append(a.id)
        self.quotable_digest_positions = {}
        for a in self.guidance_order:
            if a.cls == "quotable":
                self.quotable_digest_positions.setdefault(
                    a.digest, []).append(a.id)

    # -- lookups ----------------------------------------------------------

    def qa_registry(self):
        """Load this edition's QA-only registry outside the content lock.

        Verification commands call this lazily.  Candidate derivation never
        reads QA pins, and another edition's QA registry is not reachable.
        """
        if self._qa_registry is None:
            from . import qaregistry

            allowed = {
                corpus_id
                for corpus_id in self.edition.get("qaSources", {}).values()
                if corpus_id is not None
            }
            selected = qaregistry.QaRegistry(
                gateway.ContentGateway(
                    self.gw.root, byte_source=self.gw.byte_source),
                self.edition["qaRegistry"], allowed)
            overlap = set(selected.corpora) & set(self.registry.corpora)
            if overlap:
                raise ModelError(
                    "QA and artifact registries duplicate corpus id(s): %r"
                    % sorted(overlap))
            self._qa_registry = selected
        return self._qa_registry

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

    @staticmethod
    def _contextual_identity(block_id, digest, positions_by_digest,
                             anchors, root_hash):
        """Return the non-positional proof for one ambiguous block locator."""
        positions = positions_by_digest.get(digest, [])
        if len(positions) <= 1:
            return None
        anchor = anchors.get(block_id)
        if anchor is None or block_id not in positions:
            return None
        parent_id = anchor.parent
        parent = anchors.get(parent_id) if parent_id else None
        return {
            "parentHash": parent.digest if parent else root_hash,
            "occurrence": positions.index(block_id) + 1,
        }

    def contextual_identity(self, block_id, digest):
        """Contextual identity for an ambiguous target covering digest.

        The parent-container canonical hash and occurrence index are review
        inputs; the positional block id remains a review-excluded locator.
        """
        return self._contextual_identity(
            block_id, digest, self.digest_positions,
            self.target_anchors, self.target_root_hash)

    def quotable_contextual_identity(self, block_id, digest):
        """Contextual identity for an ambiguous quotable-source digest.

        This is the caution-source and gate-inventory counterpart of
        :meth:`contextual_identity`.  A root-level guidance block is covered
        by the canonical claim-corpus root hash, never by an empty or
        positional surrogate.
        """
        return self._contextual_identity(
            block_id, digest, self.quotable_digest_positions,
            self.guidance_anchors, self.guidance_root_hash)

    def gate_entry_projection(self, entry):
        """Return an inventory entry's corpus-aware review projection."""
        source = entry["source"]
        context = self.quotable_contextual_identity(
            source["block"], source["textHash"])
        return gate_entry_projection(entry, context)

    def gate_entry_hash(self, gate_id):
        entry = self.gates_by_id.get(gate_id)
        if entry is None:
            raise ModelError("unknown gateId %r" % gate_id)
        return canon.composite_digest("aa11393:inventory:c1",
                                      self.gate_entry_projection(entry))

    def inventory_digest(self):
        return canon.composite_digest("aa11393:inventory:c1", self.gates)

    # -- review projections (§13) -----------------------------------------

    def _stored_review(self, schema_name, instance,
                       stop_owner_boundaries=False):
        """Project stored fields from the relation schema's review axis."""
        return schema_validate.review_axis(
            self.review_schemas[schema_name], instance,
            root=self.schemas["relation"],
            stop_owner_boundaries=stop_owner_boundaries)

    def _target_projection(self, target):
        out = self._stored_review("target", target)
        ctx = self.contextual_identity(target["block"], target["textHash"])
        if ctx is not None:
            out["contextualIdentity"] = ctx
        if "caution" in out and "caution" in target:
            out["caution"] = self._caution_projection(
                target["caution"], out["caution"])
        return out

    def _source_projection(self, source, projected):
        """Add computed identity to a schema-projected source reference."""
        out = dict(projected)
        ctx = self.quotable_contextual_identity(
            source["block"], source["textHash"])
        if ctx is not None:
            out["contextualIdentity"] = ctx
        return out

    def _caution_projection(self, caution, projected):
        """Add computed identity to a projected source-gate caution."""
        out = dict(projected)
        if "source" in out and "source" in caution:
            out["source"] = self._source_projection(
                caution["source"], out["source"])
        return out

    def _owner_stored_review(self, schema_name, owner):
        """Schema-derived owner fields with computed locator context added.

        Phrases are independent reviewed owners, so the unit-owner projection
        stops at the ownership boundary declared on the relation schema.
        Computed contextual identity is added only to target and quotable
        source references that survived that same schema projection.
        """
        out = self._stored_review(
            schema_name, owner,
            stop_owner_boundaries=(schema_name == "unit"))
        if "targets" in out:
            out["targets"] = [self._target_projection(t)
                              for t in owner["targets"]]
        if "caution" in out and "caution" in owner:
            out["caution"] = self._caution_projection(
                owner["caution"], out["caution"])
        if "source" in out and "source" in owner:
            out["source"] = self._source_projection(
                owner["source"], out["source"])
        return out

    def unit_projection(self, fragment_id, frag):
        proj = self._owner_stored_review("unit", frag)
        proj.update({
            "identity": {
                "binding": self._stored_review("binding", self.binding),
                "owner": "unit",
                "fragment": fragment_id,
            },
            "dependencyChainHash": self.chain_hashes[self.claim_of(fragment_id)],
        })
        return proj

    def phrase_projection(self, fragment_id, frag, phrase):
        proj = self._owner_stored_review("phrase", phrase)
        proj.update({
            "identity": {
                "binding": self._stored_review("binding", self.binding),
                "owner": "phrase",
                "fragment": fragment_id, "phrase": phrase["id"],
            },
            "dependencyChainHash": self.chain_hashes[self.claim_of(fragment_id)],
            "parentFragmentHash": frag["fragmentTextHash"],
        })
        return proj

    def claim_gate_projection(self, claim_key, gate):
        proj = self._owner_stored_review("claim-gate", gate)
        proj.update({
            "identity": {
                "binding": self._stored_review("binding", self.binding),
                "owner": "claim-gate",
                "claim": claim_key, "gateId": gate["gateId"],
            },
            "dependencyChainHash": self.chain_hashes[int(claim_key[1:])],
        })
        return proj

    def disposition_projection(self, disp):
        subject = disp["subject"]
        if subject["kind"] == "fragment":
            claim = self.claim_of(subject["id"])
        else:
            claim = int(subject["id"][1:])
        proj = self._owner_stored_review("disposition", disp)
        proj.update({
            "identity": {
                "binding": self._stored_review("binding", self.binding),
                "owner": "disposition",
                "gateId": disp["gateId"], "subject": dict(subject),
            },
            "dependencyChainHash": self.chain_hashes[claim],
        })
        return proj

    def content_hash(self, projection):
        return canon.composite_digest("aa11393:review:c1", projection)

    def iter_owners(self, with_projection=True, skip_stale=False):
        """Yield ``(owner_type, key, stored_fields, projection)``.

        Migration must be able to enumerate owners whose projection inputs
        have disappeared (for example, every owner of a removed claim).
        Callers doing that bookkeeping use ``with_projection=False``; normal
        validation and review callers retain the eager-projection default.
        ``skip_stale`` avoids constructing projections that a migration pass
        has already classified as unresolved.
        """
        def item(owner_type, key, fields, projection_factory):
            if skip_stale and fields.get("migrationState") == "stale":
                return None
            projection = projection_factory() if with_projection else None
            return owner_type, key, fields, projection

        for fid in sorted(self.relation.get("fragments", {})):
            frag = self.relation["fragments"][fid]
            result = item("unit", fid, frag,
                          lambda fid=fid, frag=frag:
                          self.unit_projection(fid, frag))
            if result is not None:
                yield result
            for ph in frag.get("phrases", []):
                key = ph.get("id", "%s?" % fid)
                result = item("phrase", key, ph,
                              lambda fid=fid, frag=frag, ph=ph:
                              self.phrase_projection(fid, frag, ph))
                if result is not None:
                    yield result
        for ckey in sorted(self.relation.get("claimGates", {})):
            for gate in self.relation["claimGates"][ckey]:
                key = "%s/%s" % (ckey, gate.get("gateId"))
                result = item("claim-gate", key, gate,
                              lambda ckey=ckey, gate=gate:
                              self.claim_gate_projection(ckey, gate))
                if result is not None:
                    yield result
        for disp in self.relation.get("dispositions", []):
            key = "%s@%s" % (disp.get("gateId"), disp.get("subject", {}).get("id"))
            result = item("disposition", key, disp,
                          lambda disp=disp: self.disposition_projection(disp))
            if result is not None:
                yield result
