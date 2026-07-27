"""Shared validated-corpus fixture for isolated structured-source tests."""


_validated_corpus = None


def install_validated_corpus(corpus):
    """Bind the aggregate's immutable corpus result exactly once."""
    global _validated_corpus
    from structured_source.verify import ValidatedCorpus

    if not isinstance(corpus, ValidatedCorpus):
        raise ValueError("structured-source test corpus is malformed")
    if _validated_corpus is not None and _validated_corpus is not corpus:
        raise ValueError("structured-source test corpus is already bound")
    _validated_corpus = corpus


def validated_corpus():
    """Return the bound corpus or construct it once for standalone tests."""
    global _validated_corpus
    if _validated_corpus is None:
        from navigator.lib import currentstate
        from navigator.lib.snapshot import RepositorySnapshot
        from structured_source.verify import validate_corpus

        frozen = RepositorySnapshot.capture(
            currentstate.ROOT, retain_bytes=True)
        _validated_corpus = validate_corpus(
            currentstate.ROOT, byte_source=frozen.byte_source(),
            repository_snapshot=frozen)
    return _validated_corpus
