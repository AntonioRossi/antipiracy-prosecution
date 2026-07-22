"""Closed-schema validation engine + axis extraction (TDD §10.1, §13).

Implements the JSON-Schema subset used by the navigator's schemas: type,
enum, required, properties, patternProperties, additionalProperties:false,
items, $ref (local definitions). Closed by construction: an object with
neither a matching property nor patternProperty is invalid.

Axis discipline (relation schema): every leaf field must carry both
``x-ship`` and ``x-review``; inter-axis invariants are validated here —
every ship:artifact/schedule-only field is review:include except declared
locator exceptions, which must be ship:artifact + review:exclude, name a
review-included sibling covering digest, and be block locators only.
"""

import re

SHIP = ("artifact", "schedule-only", "never")
REVIEW = ("include", "exclude")


class SchemaError(ValueError):
    """The schema itself violates the meta-rules."""


class ValidationError(ValueError):
    pass


def _resolve(schema, root):
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise SchemaError("only local $refs supported: %r" % ref)
        node = root
        for part in ref[2:].split("/"):
            node = node[part]
        return node
    return schema


def _type_ok(value, tp):
    return {
        "object": lambda v: isinstance(v, dict),
        "array": lambda v: isinstance(v, (list, tuple)),
        "string": lambda v: isinstance(v, str),
        "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
        "null": lambda v: v is None,
        "boolean": lambda v: isinstance(v, bool),
    }[tp](value)


def validate(instance, schema, root=None, path="$"):
    """Validate; returns a list of error strings (empty = valid)."""
    root = root if root is not None else schema
    schema = _resolve(schema, root)
    errors = []

    tp = schema.get("type")
    if tp is not None:
        types = tp if isinstance(tp, list) else [tp]
        if not any(_type_ok(instance, t) for t in types):
            return ["%s: expected %s, got %r" % (path, "/".join(types), type(instance).__name__)]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append("%s: %r not in enum %r" % (path, instance, schema["enum"]))

    if isinstance(instance, dict):
        props = schema.get("properties", {})
        patterns = schema.get("patternProperties", {})
        for req in schema.get("required", []):
            if req not in instance:
                errors.append("%s: missing required field %r" % (path, req))
        for key, val in instance.items():
            sub = None
            if key in props:
                sub = props[key]
            else:
                for pat, ps in patterns.items():
                    if re.match(pat, key):
                        sub = ps
                        break
            if sub is None:
                if schema.get("additionalProperties", True) is False:
                    errors.append("%s: unexpected field %r (closed schema)" % (path, key))
                continue
            errors.extend(validate(val, sub, root, "%s.%s" % (path, key)))
    elif isinstance(instance, (list, tuple)):
        items = schema.get("items")
        if items is not None:
            for i, val in enumerate(instance):
                errors.extend(validate(val, items, root, "%s[%d]" % (path, i)))
    return errors


def _walk_leaves(schema, root, path, seen):
    schema = _resolve(schema, root)
    sid = id(schema)
    key = (sid, path.split(".")[-1])
    if key in seen:
        return
    seen.add(key)
    if schema.get("x-ship") is not None or schema.get("x-review") is not None:
        # a tagged container is an opaque leaf (e.g. previousTargets)
        yield path, schema
        return
    tp = schema.get("type")
    types = tp if isinstance(tp, list) else [tp]
    if "object" in types:
        for name, sub in schema.get("properties", {}).items():
            yield from _walk_leaves(sub, root, path + "." + name, seen)
        for pat, sub in schema.get("patternProperties", {}).items():
            yield from _walk_leaves(sub, root, path + ".<%s>" % pat, seen)
    elif "array" in types:
        if "items" in schema:
            yield from _walk_leaves(schema["items"], root, path + "[]", seen)
    else:
        yield path, schema


def check_axes(schema):
    """Validate the axis discipline over a tagged schema. Returns the list
    of (path, ship, review, locator_exception) leaves; raises SchemaError on
    any violation (untagged leaf, bad tag, inter-axis breach, non-block
    locator exception, exception without covering proof)."""
    leaves = []
    for path, leaf in _walk_leaves(schema, schema, "$", set()):
        # container-typed fields tagged as opaque (previousTargets etc.)
        ship = leaf.get("x-ship")
        review = leaf.get("x-review")
        if ship is None or review is None:
            raise SchemaError("untagged leaf field %s (both axes required)" % path)
        if ship not in SHIP or review not in REVIEW:
            raise SchemaError("bad axis tag on %s: %r/%r" % (path, ship, review))
        exc = leaf.get("x-locatorException")
        if ship in ("artifact", "schedule-only") and review == "exclude":
            if not exc:
                raise SchemaError(
                    "%s: ship-visible but review-excluded without a declared "
                    "locator exception" % path)
            if ship != "artifact":
                raise SchemaError("%s: locator exceptions are ship:artifact only" % path)
            if not path.rsplit(".", 1)[-1].startswith("block"):
                raise SchemaError(
                    "%s: locator exceptions apply to block locators only" % path)
            covered_by = exc.get("coveredBy")
            if not covered_by:
                raise SchemaError("%s: locator exception without covering digest" % path)
        elif exc:
            raise SchemaError(
                "%s: locator exception declared on a non-excepted field" % path)
        leaves.append((path, ship, review, exc))
    return leaves


def _walk_tagged(schema, root):
    """Yield (parent_schema, name, leaf) for all named leaf properties, to
    verify covering digests exist as review-included siblings."""
    schema = _resolve(schema, root)
    if schema.get("type") == "object" or (isinstance(schema.get("type"), list) and "object" in schema["type"]):
        props = schema.get("properties", {})
        for name, sub in props.items():
            rsub = _resolve(sub, root)
            exc = rsub.get("x-locatorException")
            if exc:
                cover = exc["coveredBy"]
                rcover = _resolve(props.get(cover, {}), root) if cover in props else None
                if rcover is None:
                    raise SchemaError(
                        "locator %r names covering digest %r that is not a sibling"
                        % (name, cover))
                if rcover.get("x-review") != "include":
                    raise SchemaError(
                        "locator %r covering digest %r is not review-included"
                        % (name, cover))
            yield from _walk_tagged(sub, root)
    elif "items" in schema:
        yield from _walk_tagged(schema["items"], root)
    for sub in schema.get("patternProperties", {}).values():
        yield from _walk_tagged(sub, root)


def check_locator_coverage(schema):
    """Every declared locator exception names an existing review-included
    sibling covering digest (an exception without proof is schema-invalid)."""
    for _ in _walk_tagged(schema, schema):
        pass


def ship_axis(schema, instance, mode):
    """Project an instance through the ship axis. mode: 'artifact' keeps
    artifact fields; 'schedule' keeps artifact + schedule-only."""
    keep = {"artifact"} if mode == "artifact" else {"artifact", "schedule-only"}
    return _project(instance, schema, schema, keep)


def _project(instance, schema, root, keep):
    schema = _resolve(schema, root)
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        patterns = schema.get("patternProperties", {})
        out = {}
        for key, val in instance.items():
            sub = props.get(key)
            if sub is None:
                for pat, ps in patterns.items():
                    if re.match(pat, key):
                        sub = ps
                        break
            if sub is None:
                continue
            rsub = _resolve(sub, root)
            if rsub.get("x-ship") is not None:
                if rsub["x-ship"] in keep:
                    out[key] = val
                continue
            child = _project(val, sub, root, keep)
            if child not in ({}, []):
                out[key] = child
        return out
    if isinstance(instance, (list, tuple)):
        items = schema.get("items", {})
        out = []
        for val in instance:
            child = _project(val, items, root, keep)
            if child not in ({}, []):
                out.append(child)
        return out
    return instance
