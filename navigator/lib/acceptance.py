"""Current navigator acceptance registry and ephemeral result projection."""

from __future__ import annotations

import importlib
import os

from . import canon


ACCEPTANCE_PATH = "navigator/schema/acceptance.json"
CONTRACT_PATH = (
    "contracts/30-product-generation/claims-navigator/"
    "acceptance-criteria_DRAFT.md"
)
PRIOR_ACCEPTANCE_PATH = "navigator/schema/prior-art-acceptance.json"
PRIOR_CONTRACT_PATH = (
    "contracts/30-product-generation/claims-prior-art-navigator/"
    "acceptance-criteria_DRAFT.md"
)
MAP_ACCEPTANCE_PATH = "navigator/schema/prior-art-map-acceptance.json"
MAP_CONTRACT_PATH = (
    "contracts/20-semantic-relations/claim-prior-art-passage-map/"
    "acceptance-criteria_DRAFT.md"
)
SPEC_CRITERIA = tuple("AC-%02d" % number for number in range(1, 21))
MAP_CRITERIA = tuple("PAM-AC-%02d" % number for number in range(1, 11))
PRIOR_CRITERIA = tuple("PA-AC-%02d" % number for number in range(1, 18))
CRITERIA = SPEC_CRITERIA + MAP_CRITERIA + PRIOR_CRITERIA
TEST_COVERAGE = {
    ("navigator.tests.test_canon.TestVectors."
     "test_json_parser_rejects_information_losing_inputs"):
        frozenset({"AC-15"}),
    ("navigator.tests.test_current_pipeline.CurrentPipelineTests."
     "test_one_source_pass_returns_same_context_frozen_handoffs"):
        frozenset({"AC-01"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_live_editions_have_exact_claim_and_mapping_census"):
        frozenset({"AC-02"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_stale_relation_digest_fails_during_construction"):
        frozenset({"AC-03", "AC-18"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_navigator_relations_reject_upstream_relation_references"):
        frozenset({"AC-03", "AC-18"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_relation_endpoint_and_semantic_ownership_fail_closed"):
        frozenset({"AC-03", "AC-18"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_validator_rejects_overlapping_phrases_and_cross_target_repeats"):
        frozenset({"AC-03", "AC-18"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_wording_origins_and_editorial_targeting_fail_closed"):
        frozenset({"AC-03", "AC-18"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_controlled_wording_has_exact_slots"):
        frozenset({"AC-04"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_authored_handoff_uses_handed_xml_and_retained_controls_only"):
        frozenset({"AC-05"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_model_lookups_require_explicit_nonempty_identities"):
        frozenset({"AC-06"}),
    ("navigator.tests.test_current_pipeline.CurrentPipelineTests."
     "test_product_plan_is_derived_from_an_arbitrary_edition_inventory"):
        frozenset({"AC-07"}),
    ("navigator.tests.test_render_current.CurrentRenderTests."
     "test_composites_are_one_candidate_and_reverse_index_every_endpoint"):
        frozenset({"AC-08"}),
    ("navigator.tests.test_render_current.CurrentRenderTests."
     "test_hostile_typed_values_are_inert_and_composite_data_is_exact"):
        frozenset({"AC-09", "AC-15"}),
    ("navigator.tests.test_render_current.CurrentRenderTests."
     "test_live_products_are_complete_self_contained_and_accessible"):
        frozenset({"AC-12", "AC-14", "AC-17"}),
    ("navigator.tests.test_render_current.CurrentRenderTests."
     "test_current_profile_specification_vectors_reach_renderer"):
        frozenset({"AC-18"}),
    ("navigator.tests.test_render_current.CurrentRenderTests."
     "test_pinned_browser_matrix_proves_specification_runtime"):
        frozenset({"AC-10", "AC-11", "AC-13", "AC-18"}),
    ("navigator.tests.test_xml_model.XMLModelTests."
     "test_candidate_proof_binds_the_complete_fresh_projection"):
        frozenset({"AC-16"}),
    ("navigator.tests.test_current_pipeline.CurrentPipelineTests."
     "test_materialized_reproduction_constructs_each_boundary_once"):
        frozenset({"AC-18"}),
    ("navigator.tests.test_current_pipeline.CurrentPipelineTests."
     "test_live_navigator_input_inventory_is_exact"):
        frozenset({"AC-19", "PA-AC-17"}),
    ("navigator.tests.test_current_pipeline.CurrentPipelineTests."
     "test_configured_member_bundle_and_checksums_are_deterministic"):
        frozenset({"AC-20", "PA-AC-15"}),
    ("navigator.tests.test_current_pipeline.CurrentPipelineTests."
     "test_generated_writes_are_atomic_generated_only_and_safe"):
        frozenset({"PA-AC-14"}),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_exact_product_and_handoff_inventory"):
        frozenset({"PAM-AC-08", "PA-AC-01", "PA-AC-05", "PA-AC-13"}),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_matrix_scope_obligations_and_candidates_are_exact"):
        frozenset({
            "PAM-AC-01", "PAM-AC-02", "PAM-AC-03", "PAM-AC-04",
            "PA-AC-02", "PA-AC-03", "PA-AC-04",
        }),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_static_html_has_exact_forward_and_reverse_passage_navigation"):
        frozenset({"PA-AC-06", "PA-AC-11"}),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_positive_and_adverse_multiplicity_vectors_use_model_enforcers"):
        frozenset({
            "PAM-AC-05", "PAM-AC-06", "PAM-AC-07",
        }),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_current_profile_adverse_vectors_fail_before_render"):
        frozenset({"PA-AC-12"}),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_current_profile_xml_vector_reaches_the_immutable_renderer"):
        frozenset({"PAM-AC-10", "PA-AC-16"}),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_pinned_browser_matrix_proves_runtime_layout_and_navigation"):
        frozenset({
            "PA-AC-07", "PA-AC-08", "PA-AC-09", "PA-AC-10",
        }),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_pinned_browser_vector_proves_independent_candidate_movement"):
        frozenset({"PA-AC-16"}),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_noncurrent_passage_map_profile_fails_closed"):
        frozenset({"PAM-AC-09"}),
    ("navigator.tests.test_prior_art.PriorArtNavigatorTests."
     "test_closed_profile_and_bundle_controls_are_current"):
        frozenset({"PA-AC-17"}),
}


def test_modules():
    """Return the exact modules owning registered criterion verifier methods."""
    return tuple(sorted({".".join(identifier.split(".")[:-2])
                         for identifier in TEST_COVERAGE}))

_SCOPES = {
    **{"AC-%02d" % number: "edition" for number in range(1, 19)},
    "AC-19": "shared",
    "AC-20": "bundle",
    **{"PAM-AC-%02d" % number: "semantic"
       for number in range(1, 11)},
    **{"PA-AC-%02d" % number: "product"
       for number in range(1, 13)},
    "PA-AC-13": "shared",
    "PA-AC-14": "product",
    "PA-AC-15": "bundle",
    "PA-AC-16": "product",
    "PA-AC-17": "shared",
}


class AcceptanceError(ValueError):
    """The current executable acceptance contract is malformed or failed."""


def _resolve_enforcer(path):
    """Resolve one exact dotted implementation symbol without aliases."""
    if not isinstance(path, str) or not path or any(
            not part or not part.replace("_", "a").isalnum()
            for part in path.split(".")):
        raise AcceptanceError("acceptance enforcer path is malformed")
    parts = path.split(".")
    for boundary in range(len(parts), 0, -1):
        try:
            value = importlib.import_module(".".join(parts[:boundary]))
        except ImportError:
            continue
        try:
            for part in parts[boundary:]:
                value = getattr(value, part)
        except AttributeError as exc:
            raise AcceptanceError(
                "acceptance enforcer symbol is absent: %s" % path) from exc
        if not callable(value):
            raise AcceptanceError(
                "acceptance enforcer is not executable: %s" % path)
        return value
    raise AcceptanceError("acceptance enforcer module is absent: %s" % path)


def validate_registry(value):
    identifiers = ([entry.get("id") for entry in value.get("criteria", [])]
                   if isinstance(value, dict) and
                   isinstance(value.get("criteria"), list) else [])
    if identifiers[:1] == ["AC-01"]:
        expected_criteria = SPEC_CRITERIA
        expected_version = "9"
    elif identifiers[:1] == ["PAM-AC-01"]:
        expected_criteria = MAP_CRITERIA
        expected_version = "2"
    else:
        expected_criteria = PRIOR_CRITERIA
        expected_version = "4"
    if not isinstance(value, dict) or set(value) != {
            "acceptanceVersion", "criteria"} or \
            value.get("acceptanceVersion") != expected_version:
        raise AcceptanceError(
            "acceptance registry shape/version is not current")
    criteria = value.get("criteria")
    if not isinstance(criteria, list) or len(criteria) != len(expected_criteria) or \
            [entry.get("id") for entry in criteria
             if isinstance(entry, dict)] != list(expected_criteria):
        raise AcceptanceError("acceptance criterion census/order is not exact")
    for criterion in criteria:
        if not isinstance(criterion, dict) or set(criterion) != {
                "enforcer", "id", "outcome", "scope"}:
            raise AcceptanceError("acceptance criterion shape is malformed")
        identifier = criterion["id"]
        outcome = criterion["outcome"]
        enforcer = criterion["enforcer"]
        covering_tests = {
            test_id for test_id, identifiers in TEST_COVERAGE.items()
            if identifier in identifiers
        }
        enforcer_parts = enforcer.split("; ") if isinstance(enforcer, str) else []
        if criterion["scope"] != _SCOPES[identifier] or \
                not isinstance(outcome, str) or not outcome.strip() or \
                outcome != outcome.strip() or \
                not isinstance(enforcer, str) or not enforcer.strip() or \
                enforcer != enforcer.strip() or len(enforcer_parts) != 2 or \
                enforcer_parts[1] not in covering_tests:
            raise AcceptanceError(
                "acceptance criterion %s is malformed" % identifier)
        _resolve_enforcer(enforcer_parts[0])
        _resolve_enforcer(enforcer_parts[1])
    return value


def _load_one(root, registry_path, contract_path, table_start,
              table_end, byte_source=None):
    absolute = os.path.join(root, *registry_path.split("/"))
    try:
        if byte_source is None:
            with open(absolute, "rb") as handle:
                data = handle.read()
        else:
            data = byte_source(absolute)
    except (OSError, KeyError) as exc:
        raise AcceptanceError("acceptance registry is unreadable") from exc
    try:
        value = canon.parse_json(data)
    except (ValueError, canon.CanonError) as exc:
        raise AcceptanceError("acceptance registry is not strict JSON") from exc
    if data != canon.canonical_json(value) + b"\n":
        raise AcceptanceError("acceptance registry bytes are not canonical")
    registry = validate_registry(value)
    contract_absolute = os.path.join(root, *contract_path.split("/"))
    try:
        if byte_source is None:
            with open(contract_absolute, "rb") as handle:
                contract_data = handle.read()
        else:
            contract_data = byte_source(contract_absolute)
        contract = contract_data.decode("utf-8")
    except (OSError, KeyError, UnicodeDecodeError) as exc:
        raise AcceptanceError("acceptance contract is unreadable") from exc
    start = table_start + "\n"
    end = table_end
    if contract.count(start) != 1 or contract.count(end) != 1 or \
            contract.split(start, 1)[1].split(end, 1)[0] != \
            render_table(registry):
        raise AcceptanceError(
            "acceptance contract and registry text differ")
    return registry


def load_registry(root, byte_source=None):
    return _load_one(
        root, ACCEPTANCE_PATH, CONTRACT_PATH,
        "<!-- NAV-AC-TABLE:START -->",
        "<!-- NAV-AC-TABLE:END -->", byte_source)


def load_registries(root, byte_source=None):
    return (
        load_registry(root, byte_source),
        _load_one(
            root, MAP_ACCEPTANCE_PATH, MAP_CONTRACT_PATH,
            "<!-- PA-MAP-AC-TABLE:START -->",
            "<!-- PA-MAP-AC-TABLE:END -->", byte_source),
        _load_one(
            root, PRIOR_ACCEPTANCE_PATH, PRIOR_CONTRACT_PATH,
            "<!-- PA-NAV-AC-TABLE:START -->",
            "<!-- PA-NAV-AC-TABLE:END -->", byte_source),
    )


def render_table(registry):
    validate_registry(registry)
    lines = [
        "| ID | Scope | Executable technical outcome | Independent enforcer |",
        "|---|---|---|---|",
    ]
    for criterion in registry["criteria"]:
        outcome = criterion["outcome"].replace("|", "\\|").replace("\n", " ")
        enforcer = criterion["enforcer"].replace("|", "\\|").replace("\n", " ")
        lines.append("| **%s** | %s | %s | %s |" % (
            criterion["id"], criterion["scope"], outcome, enforcer))
    return "\n".join(lines) + "\n"


def passed_result(registries, passed_test_ids):
    """Create ephemeral technical status after the named current checks pass.

    The result deliberately carries no identity, timestamp, signature, source
    digest, or authorization semantics.  Its only lifetime is the invoking
    validation process.
    """
    registries = tuple(registries)
    if len(registries) != 3:
        raise AcceptanceError(
            "ephemeral acceptance requires all current registries")
    for registry in registries:
        validate_registry(registry)
    test_ids = tuple(passed_test_ids)
    if len(test_ids) != len(set(test_ids)) or \
            not set(TEST_COVERAGE).issubset(test_ids):
        raise AcceptanceError(
            "ephemeral acceptance result lacks an exact verifier census")
    passed = set().union(*TEST_COVERAGE.values())
    if passed != set(CRITERIA) or \
            any(not coverage for coverage in TEST_COVERAGE.values()):
        raise AcceptanceError(
            "registered test coverage does not cover the exact criterion set")
    return {
        "acceptanceResultVersion": "1",
        "status": "passed",
        "results": [
            {"id": identifier, "status": "passed"}
            for identifier in CRITERIA
        ],
    }
