"""Shared ephemeral fixture for tests in one isolated materialization."""

from types import MappingProxyType


_validation_session = None


def install_validation_session(session):
    """Install the already-proved immutable product session exactly once."""
    global _validation_session
    if not isinstance(session, MappingProxyType) or set(session) != {
            "models", "plan", "snapshot", "sources"}:
        raise ValueError("navigator test validation session is malformed")
    if _validation_session is not None and _validation_session is not session:
        raise ValueError("navigator test validation session is already bound")
    _validation_session = session


def validation_session():
    """Return the installed session or construct one for standalone tests."""
    global _validation_session
    if _validation_session is None:
        from navigator.lib import currentstate
        from navigator.lib.snapshot import RepositorySnapshot

        frozen = RepositorySnapshot.capture(
            currentstate.ROOT, retain_bytes=True)
        plan = currentstate.load_product_plan(frozen)
        sources = currentstate.validate_structured_corpus(frozen)
        currentstate.bind_sources_to_plan(plan, sources)
        states = currentstate.derive_editions(frozen, plan.editions, sources)
        _validation_session = MappingProxyType({
            "models": MappingProxyType({
                edition_id: states[edition_id]["model"]
                for edition_id in plan.edition_ids
            }),
            "plan": plan,
            "snapshot": frozen,
            "sources": sources,
        })
    return _validation_session
