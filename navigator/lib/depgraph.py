"""Dependency graphs — dual-sourced, validated, never inferred-only.

The authored dependency map (``profiles/deps_<corpusId>.json``) is
cross-validated against the parsed ``of claim N`` references in the claim
text; any mismatch fails the build. Where the claim-set document publishes
its own dependency table (a document-table source in the map), validation
is three-way. The graph must be total (every claim present exactly once),
acyclic, and rooted at the declared independent claims (TDD §8.1).

Dependency-chain hashes (§8.2) are computed only from a validated map.
"""

from . import canon


class DepGraphError(ValueError):
    pass


def validate(dep_map, claims, independents):
    """Validate the authored map against parsed claims. Returns parents dict
    {claim_number: parent_number_or_None}."""
    authored = {int(k): v for k, v in dep_map["claims"].items()}
    numbers = [c.number for c in claims]

    missing = set(numbers) - set(authored)
    extra = set(authored) - set(numbers)
    if missing or extra:
        raise DepGraphError(
            "dependency map not total: missing %r, extra %r"
            % (sorted(missing), sorted(extra)))

    for c in claims:
        parent = authored[c.number]
        refs = [r for r in c.parsed_refs]
        if parent is None:
            if refs:
                raise DepGraphError(
                    "claim %d authored independent but text references %r"
                    % (c.number, refs))
        else:
            if refs != [parent]:
                raise DepGraphError(
                    "claim %d authored parent %r but text references %r"
                    % (c.number, parent, refs))
            if parent not in authored:
                raise DepGraphError(
                    "claim %d depends on unknown claim %r" % (c.number, parent))
            if parent >= c.number:
                raise DepGraphError(
                    "claim %d depends forward on claim %d" % (c.number, parent))

    doc_table = dep_map.get("documentTable")
    if doc_table is not None:
        table = {int(k): v for k, v in doc_table.items()}
        if table != authored:
            diff = {k for k in set(table) | set(authored)
                    if table.get(k, "∅") != authored.get(k, "∅")}
            raise DepGraphError(
                "three-way check failed: document table disagrees on claims %r"
                % sorted(diff))

    roots = sorted(n for n, p in authored.items() if p is None)
    if roots != sorted(independents):
        raise DepGraphError(
            "graph roots %r do not match declared independent claims %r"
            % (roots, sorted(independents)))

    # acyclicity: parents strictly decrease, so chains terminate; walk anyway
    for n in authored:
        seen = set()
        cur = n
        while cur is not None:
            if cur in seen:
                raise DepGraphError("dependency cycle at claim %d" % n)
            seen.add(cur)
            cur = authored[cur]
    return authored


def ancestor_chain(parents, number):
    """Ancestor chain, independent claim first, the claim itself last."""
    chain = []
    cur = number
    while cur is not None:
        chain.append(cur)
        cur = parents[cur]
    return list(reversed(chain))


def chain_hash(parents, agg_hashes, number):
    """Dependency-chain hash: digest-list composite over the ordered
    aggregate claim hashes of the ancestor chain (§8.2)."""
    return canon.composite_digest(
        "aa11393:dep-chain:c1",
        [agg_hashes[n] for n in ancestor_chain(parents, number)])
