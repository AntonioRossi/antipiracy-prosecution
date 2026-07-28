"""Small computed projections over the immutable navigator model."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class RelationRef:
    kind: str
    relation_id: str
    subject_fragment_id: str


@dataclass(frozen=True, slots=True)
class OriginRecord:
    value_id: str
    kind: str
    owner_path: str
    owner_ref: str
    owner_digest: str


def reverse_index(relation_set, units_by_fragment):
    """Compute target-fragment → ordered relation references."""
    values = {}
    for mapping in relation_set.mappings:
        for target in mapping.targets:
            for endpoint in target.endpoints:
                values.setdefault(
                    (endpoint.document_id, endpoint.fragment_id), []).append(RelationRef(
                    kind="mapping",
                    relation_id=mapping.relation_id,
                    subject_fragment_id=mapping.subject.fragment_id,
                ))
    for phrase in relation_set.phrase_mappings:
        for target in phrase.targets:
            for endpoint in target.endpoints:
                values.setdefault(
                    (endpoint.document_id, endpoint.fragment_id), []).append(RelationRef(
                    kind="phrase",
                    relation_id=phrase.relation_id,
                    subject_fragment_id=phrase.parent.fragment_id,
                ))

    def key(reference):
        unit = units_by_fragment[reference.subject_fragment_id]
        return (unit.claim_number,
                0 if reference.kind == "mapping" else 1,
                unit.unit_index,
                reference.relation_id)

    return MappingProxyType({
        endpoint: tuple(sorted(references, key=key))
        for endpoint, references in sorted(values.items())
    })


def origin_inventory(model):
    """Compute substantive/security-relevant value origins from typed state."""
    if getattr(model, "product_kind", None) == "prior-art":
        return _prior_art_origin_inventory(model)
    reads = dict(model.read_inventory)
    values = []

    def add(value_id, kind, path, owner_ref, digest=None):
        values.append(OriginRecord(
            value_id=value_id,
            kind=kind,
            owner_path=path,
            owner_ref=owner_ref,
            owner_digest=reads[path] if digest is None else digest,
        ))

    claim_document, pct_document = model.source_documents
    for document in model.source_documents:
        add("document:" + document.document_id, "source-document",
            document.registered_path, document.document_id,
            document.xml_raw_digest)
    for fragment_id, item in sorted(model._source_items.items()):
        add("source-item:%s#%s" % (claim_document.document_id, fragment_id),
            "source-item", claim_document.registered_path, fragment_id,
            item.content_digest)
    for fragment_id, item in sorted(model.disclosure_index.items()):
        add("source-item:%s#%s" % (pct_document.document_id, fragment_id),
            "source-item", pct_document.registered_path, fragment_id,
            item.content_digest)
    for asset_id, asset in sorted(model.assets.items()):
        add("asset:" + asset_id, "asset", asset.path, asset_id,
            asset.raw_digest)

    relation_path = model._relation_path
    add("relation-set:" + model.relation_set_id, "relation-set",
        relation_path, model.relation_set_id)
    for gate in model.relations.gate_definitions:
        add("gate:" + gate.gate_id, "relation-gate", relation_path,
            gate.gate_id)
    relation_items = (*model.relations.mappings,
                      *model.relations.phrase_mappings)
    for relation in relation_items:
        add("relation:" + relation.relation_id, "relation", relation_path,
            relation.relation_id)
        for index, target in enumerate(relation.targets, 1):
            add("relation:%s:target:%d" % (relation.relation_id, index),
                "relation-target", relation_path,
                "%s/target/%d" % (relation.relation_id, index))
    for disposition in model.relations.dispositions:
        add("disposition:" + disposition.disposition_id,
            "relation-disposition", relation_path,
            disposition.disposition_id)

    for wording_id, entry in sorted(model._wording.items()):
        path = model._wording_owner_paths[wording_id]
        add("wording:" + wording_id, "controlled-wording", path, wording_id)
        for slot in entry.slots:
            if slot.origin_ref.startswith("bundle."):
                # The bundle resolver proves this multi-edition origin once
                # all independently sealed configured models are available.
                continue
            if slot.origin_ref in {
                    "edition.claimSetVersion",
                    "edition.declaredReleaseTimestamp"}:
                owner_path = model._edition_path
            elif slot.origin_ref in {
                    "edition.claimCount", "edition.unitCount"}:
                owner_path = claim_document.registered_path
            elif slot.origin_ref == "target.blockCount":
                owner_path = pct_document.registered_path
            else:
                raise ValueError("controlled wording slot origin is unowned")
            add("wording:%s:slot:%s" % (wording_id, slot.name),
                "wording-slot-" + slot.origin_kind, owner_path,
                slot.origin_ref)

    for field in (
            "artifactName", "census", "claimPackageId", "claimSetVersion",
            "consumerId", "declaredReleaseTimestamp", "displayName",
            "editionId", "editionVersion", "editionWordingPath", "groups",
            "independentClaims",
            "productId", "productKind", "productVersion", "relationPath",
            "strategyName", "strategyPrefix"):
        add("edition:" + field, "edition-control", model._edition_path,
            "edition." + field)

    value_ids = [item.value_id for item in values]
    if len(value_ids) != len(set(value_ids)):
        raise ValueError("computed substantive origin identities collide")
    return tuple(sorted(values, key=lambda item: item.value_id))


def _prior_art_origin_inventory(model):
    reads = dict(model.read_inventory)
    values = []

    def add(value_id, kind, path, owner_ref, digest=None):
        values.append(OriginRecord(
            value_id=value_id, kind=kind, owner_path=path,
            owner_ref=owner_ref,
            owner_digest=reads[path] if digest is None else digest))

    claim_document = model.source_documents[0]
    comparison_document = model.source_documents[1]
    map_document = model.source_documents[2]
    for document in model.source_documents:
        add("document:" + document.document_id, "source-document",
            document.registered_path, document.document_id,
            document.xml_raw_digest)
    for fragment_id, item in sorted(model._source_items.items()):
        add("source-item:%s#%s" % (claim_document.document_id, fragment_id),
            "source-item", claim_document.registered_path, fragment_id,
            item.content_digest)
    for document_id, surface in sorted(model._target_surfaces.items()):
        document = model.get_document(document_id)
        for item in surface.items:
            add("source-item:%s#%s" % (
                document_id, item.item_id), "source-item",
                document.registered_path, item.item_id,
                item.content_digest)
    add("relation-set:" + model.relation_set_id, "relation-set",
        map_document.registered_path, model.relation_set_id)
    for relation in (*model.prior_art_obligations,
                     *model.review_allocations,
                     *model.candidate_relations):
        add("relation:" + relation.relation_id, "relation",
            map_document.registered_path, relation.relation_id)
        for index, unused_target in enumerate(
                getattr(relation, "targets", ()), 1):
            add("relation:%s:target:%d" % (relation.relation_id, index),
                "relation-target", map_document.registered_path,
                "%s/target/%d" % (relation.relation_id, index))
    for mapping in model.relations.mappings:
        add("computed-unit-state:" + mapping.subject.fragment_id,
            "closed-derivation", map_document.registered_path,
            mapping.subject.fragment_id)
    for wording_id, entry in sorted(model._wording.items()):
        path = model._wording_owner_paths[wording_id]
        add("wording:" + wording_id, "controlled-wording", path, wording_id)
        for slot in entry.slots:
            if slot.origin_ref.startswith("bundle."):
                continue
            if slot.origin_ref in {
                    "edition.claimSetVersion",
                    "edition.declaredReleaseTimestamp"}:
                owner_path = model._edition_path
            elif slot.origin_ref in {
                    "edition.claimCount", "edition.unitCount"}:
                owner_path = claim_document.registered_path
            elif slot.origin_ref == "target.blockCount":
                owner_path = comparison_document.registered_path
            else:
                raise ValueError("controlled wording slot origin is unowned")
            add("wording:%s:slot:%s" % (wording_id, slot.name),
                "wording-slot-" + slot.origin_kind, owner_path,
                slot.origin_ref)
    for field in (
            "artifactName", "census", "claimPackageId", "claimSetVersion",
            "comparisonPackageId", "consumerId", "declaredReleaseTimestamp",
            "displayName", "documentCensus", "editionId", "editionVersion",
            "groups", "independentClaims", "passageMapPackageId",
            "priorArtWordingPath", "productId", "productKind",
            "productVersion", "strategyName", "strategyPrefix"):
        add("edition:" + field, "edition-control", model._edition_path,
            "edition." + field)
    ids = [item.value_id for item in values]
    if len(ids) != len(set(ids)):
        raise ValueError("computed prior-art origin identities collide")
    return tuple(sorted(values, key=lambda item: item.value_id))


def bundle_origin_inventory(models, config, config_digest, config_path):
    """Compute configured-edition wording and bundle-control origins."""
    models = tuple(models)
    if not models or len({item.product_id for item in models}) != len(models):
        raise ValueError("bundle origin models are not one exact edition set")
    values = []
    for item in models:
        reads = dict(item.read_inventory)
        values.append(OriginRecord(
            value_id=("wording:bundle-manifest-neutral:slot:"
                      "editionSchedule:product:%s" % item.product_id),
            kind="wording-slot-closed-derivation",
            owner_path=item._edition_path,
            owner_ref="product.%s.claimSetVersion" % item.product_id,
            owner_digest=reads[item._edition_path],
        ))
    controls = (
        ("bundle:bundleVersion", "bundleVersion"),
        ("bundle:name", "name"),
        ("bundle:declaredTimestamp", "declaredTimestamp"),
        ("bundle:products", "products"),
        ("bundle:manifestWordingId", "manifestWordingId"),
    )
    values.extend(OriginRecord(
        value_id=value_id, kind="bundle-control", owner_path=config_path,
        owner_ref="bundle." + field, owner_digest=config_digest)
        for value_id, field in controls if field in config)
    values.extend(OriginRecord(
        value_id="bundle:member:%d" % index, kind="bundle-control",
        owner_path=config_path, owner_ref="bundle.members.%d" % index,
        owner_digest=config_digest)
        for index, unused_member in enumerate(config["members"]))
    return tuple(sorted(values, key=lambda item: item.value_id))
