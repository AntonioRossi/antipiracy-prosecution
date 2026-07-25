"""Dependency graph computed only from exact authored claim text."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from . import canon


class DepGraphError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class DependencyGraph:
    parents: object
    children: object
    roots: tuple[int, ...]
    aggregate_hashes: object
    chain_hashes: object

    def ancestor_chain(self, number: int) -> tuple[int, ...]:
        if number not in self.parents:
            raise DepGraphError("unknown claim %r" % number)
        chain = []
        current = number
        while current is not None:
            chain.append(current)
            current = self.parents[current]
        return tuple(reversed(chain))


def build(claims, independent_claims) -> DependencyGraph:
    sequence = tuple(claims)
    numbers = tuple(claim.number for claim in sequence)
    if numbers != tuple(range(1, len(sequence) + 1)):
        raise DepGraphError("claim sequence is not exact and contiguous")
    roots = tuple(sorted(independent_claims))
    if not roots or len(roots) != len(set(roots)) or \
            any(not isinstance(number, int) or isinstance(number, bool) or
                number not in numbers for number in roots):
        raise DepGraphError("independent claim inventory is invalid")

    parents = {}
    for claim in sequence:
        references = claim.dependencies
        if claim.number in roots:
            if references:
                raise DepGraphError(
                    "independent claim %d references claim ancestors %r" %
                    (claim.number, references))
            parents[claim.number] = None
        else:
            if len(references) != 1:
                raise DepGraphError(
                    "dependent claim %d must name exactly one parent" % claim.number)
            parent = references[0]
            if parent not in numbers or parent >= claim.number:
                raise DepGraphError(
                    "claim %d has an invalid parent %d" % (claim.number, parent))
            parents[claim.number] = parent
    actual_roots = tuple(number for number in numbers if parents[number] is None)
    if actual_roots != roots:
        raise DepGraphError(
            "computed roots %r differ from declared roots %r" %
            (actual_roots, roots))

    children = {number: [] for number in numbers}
    for number, parent in parents.items():
        if parent is not None:
            children[parent].append(number)
    aggregate = {
        claim.number: canon.composite_digest(
            "aa11393:claim-agg:c1",
            [unit.text_digest for unit in claim.units])
        for claim in sequence
    }

    def ancestors(number):
        found = []
        current = number
        while current is not None:
            if current in found:
                raise DepGraphError("dependency graph contains a cycle")
            found.append(current)
            current = parents[current]
        return tuple(reversed(found))

    chain_hashes = {
        number: canon.composite_digest(
            "aa11393:dep-chain:c1",
            [aggregate[item] for item in ancestors(number)])
        for number in numbers
    }
    return DependencyGraph(
        parents=MappingProxyType(parents),
        children=MappingProxyType({
            number: tuple(children[number]) for number in numbers}),
        roots=roots,
        aggregate_hashes=MappingProxyType(aggregate),
        chain_hashes=MappingProxyType(chain_hashes),
    )


def ancestor_chain(parents, number):
    chain = []
    current = number
    while current is not None:
        if current not in parents or current in chain:
            raise DepGraphError("invalid dependency chain for claim %r" % number)
        chain.append(current)
        current = parents[current]
    return tuple(reversed(chain))


def chain_hash(parents, aggregate_hashes, number):
    return canon.composite_digest(
        "aa11393:dep-chain:c1",
        [aggregate_hashes[item] for item in ancestor_chain(parents, number)])
