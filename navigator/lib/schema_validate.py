"""Closed-schema validation engine + axis extraction (TDD §10.1, §13).

Implements the JSON-Schema subset used by the navigator's schemas: type,
enum, required, properties, patternProperties, additionalProperties:false,
items, minLength/maxLength, minimum, minItems/maxItems, uniqueItems, pattern,
and $ref (local definitions). Closed by construction: an object with neither a
matching property nor patternProperty is invalid.

Axis discipline (relation schema): every leaf field must carry both
``x-ship`` and ``x-review``; inter-axis invariants are validated here —
every ship:artifact/schedule-only field is review:include except declared
locator exceptions, which must be ship:artifact + review:exclude, name a
review-included sibling covering digest, and be block locators only.
"""

import re

from . import canon

SHIP = ("artifact", "schedule-only", "never")
REVIEW = ("include", "exclude")

SCHEMA_KEYWORDS = frozenset((
    "$ref", "type", "enum", "required", "properties",
    "patternProperties", "additionalProperties", "items", "minLength",
    "maxLength", "minimum", "minItems", "maxItems", "uniqueItems",
    "pattern", "definitions", "schemaVersion", "comment", "x-ship",
    "x-review", "x-locatorException", "x-reviewOwnerBoundary",
))
INSTANCE_TYPES = frozenset((
    "object", "array", "string", "integer", "null", "boolean",
))


class SchemaError(ValueError):
    """The schema itself violates the meta-rules."""


class ValidationError(ValueError):
    pass


def check_schema(schema):
    """Reject unsupported or malformed schema declarations.

    The validator intentionally implements a small JSON-Schema subset.  A
    misspelled or unsupported keyword must be fatal; silently ignoring it
    could make an authored constraint look enforced when it is not.
    """
    root = schema

    def walk(node, path):
        if not isinstance(node, dict):
            raise SchemaError("%s is not a schema object" % path)
        unknown = set(node) - SCHEMA_KEYWORDS
        if unknown:
            raise SchemaError("%s has unsupported schema keyword(s) %r" %
                              (path, sorted(unknown)))
        if "$ref" in node:
            if set(node) != {"$ref"} or not isinstance(node["$ref"], str):
                raise SchemaError("%s has a malformed $ref" % path)
            try:
                _resolve(node, root)
            except (KeyError, TypeError):
                raise SchemaError("%s has an unresolved $ref %r" %
                                  (path, node.get("$ref")))
            return
        if "schemaVersion" in node:
            version_problems = canon.require_version(
                node, "schemaVersion", "1")
            if version_problems:
                raise SchemaError("%s: %s" % (path, version_problems[0]))
        if "comment" in node and (not isinstance(node["comment"], str) or
                                  not node["comment"].strip()):
            raise SchemaError("%s has an empty schema comment" % path)

        declared_type = node.get("type")
        types = declared_type if isinstance(declared_type, list) \
            else [declared_type]
        if declared_type is not None and (
                not types or
                not all(isinstance(item, str) for item in types) or
                len(types) != len(set(types)) or
                any(item not in INSTANCE_TYPES for item in types)):
            raise SchemaError("%s has an invalid type declaration" % path)

        for field in ("properties", "patternProperties", "definitions"):
            value = node.get(field, {})
            if not isinstance(value, dict):
                raise SchemaError("%s.%s is not an object" % (path, field))
            for name, child in value.items():
                if not isinstance(name, str) or not name:
                    raise SchemaError("%s.%s has an empty key" %
                                      (path, field))
                if field == "patternProperties":
                    try:
                        re.compile(name)
                    except re.error as exc:
                        raise SchemaError("%s has invalid pattern %r: %s" %
                                          (path, name, exc))
                walk(child, "%s.%s[%r]" % (path, field, name))

        if "object" in types:
            if node.get("additionalProperties") is not False:
                raise SchemaError(
                    "%s object schema is not closed with "
                    "additionalProperties:false" % path)
            required = node.get("required", [])
            if not isinstance(required, list) or \
                    not all(isinstance(name, str) and name
                            for name in required) or \
                    len(required) != len(set(required)):
                raise SchemaError("%s has malformed required fields" % path)
            declared = set(node.get("properties", {}))
            if not set(required).issubset(declared):
                raise SchemaError("%s requires undeclared properties %r" %
                                  (path, sorted(set(required) - declared)))
        elif any(field in node for field in (
                "properties", "patternProperties", "required",
                "additionalProperties")):
            raise SchemaError("%s uses object keywords without object type" %
                              path)

        if "array" in types:
            if "items" not in node or not isinstance(node["items"], dict):
                raise SchemaError("%s array schema has no item schema" % path)
            walk(node["items"], path + ".items")
        elif "items" in node:
            raise SchemaError("%s uses items without array type" % path)

        for field in ("minLength", "maxLength", "minItems", "maxItems"):
            if field in node and (isinstance(node[field], bool) or
                                  not isinstance(node[field], int) or
                                  node[field] < 0):
                raise SchemaError("%s.%s must be a nonnegative integer" %
                                  (path, field))
        if "minimum" in node and (isinstance(node["minimum"], bool) or
                                  not isinstance(node["minimum"], int)):
            raise SchemaError("%s.minimum must be an integer" % path)
        for low, high in (("minLength", "maxLength"),
                          ("minItems", "maxItems")):
            if low in node and high in node and node[low] > node[high]:
                raise SchemaError("%s has %s greater than %s" %
                                  (path, low, high))
        if "uniqueItems" in node and node["uniqueItems"] is not True:
            raise SchemaError("%s uniqueItems must be true" % path)
        if "pattern" in node:
            if not isinstance(node["pattern"], str):
                raise SchemaError("%s pattern is not a string" % path)
            try:
                re.compile(node["pattern"])
            except re.error as exc:
                raise SchemaError("%s has invalid pattern: %s" % (path, exc))
        if "enum" in node:
            values = node["enum"]
            if not isinstance(values, list) or not values or any(
                    value == prior
                    for index, value in enumerate(values)
                    for prior in values[:index]):
                raise SchemaError("%s has an empty or duplicate enum" % path)
        if "x-reviewOwnerBoundary" in node and \
                node["x-reviewOwnerBoundary"] is not True:
            raise SchemaError("%s review owner boundary must be true" % path)
        if "x-locatorException" in node:
            exception = node["x-locatorException"]
            if not isinstance(exception, dict) or \
                    set(exception) != {"coveredBy"} or \
                    not isinstance(exception.get("coveredBy"), str) or \
                    not exception["coveredBy"]:
                raise SchemaError("%s has a malformed locator exception" %
                                  path)

    walk(schema, "$")


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

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            errors.append("%s: string is shorter than minLength %d" %
                          (path, schema["minLength"]))
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append("%s: string is longer than maxLength %d" %
                          (path, schema["maxLength"]))
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append("%s: %r does not match pattern %r" %
                          (path, instance, schema["pattern"]))

    if isinstance(instance, int) and not isinstance(instance, bool) and \
            "minimum" in schema and instance < schema["minimum"]:
        errors.append("%s: %d is less than minimum %d" %
                      (path, instance, schema["minimum"]))

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
        if len(instance) < schema.get("minItems", 0):
            errors.append("%s: array has fewer than minItems %d" %
                          (path, schema["minItems"]))
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append("%s: array has more than maxItems %d" %
                          (path, schema["maxItems"]))
        if schema.get("uniqueItems"):
            for i, value in enumerate(instance):
                if any(value == prior for prior in instance[:i]):
                    errors.append("%s[%d]: duplicate item (uniqueItems)" %
                                  (path, i))
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
    return _axis_project(instance, schema, schema, "x-ship", keep)


def review_axis(schema, instance, root=None, stop_owner_boundaries=False):
    """Project *instance* through the schema's review axis.

    This is the generic mechanism used by owner-specific review projection
    builders: ``review:include`` fields survive, ``review:exclude`` fields
    do not.  ``root`` is required only when *schema* is a subschema whose
    local ``$ref`` values resolve against a larger schema document.
    Computed context (owner identity, dependency-chain hash, and ambiguous
    locator identity) is deliberately added by the model after this stored-
    field projection.
    """
    root = schema if root is None else root
    return _axis_project(instance, schema, root, "x-review", {"include"},
                         stop_owner_boundaries=stop_owner_boundaries)


def _axis_project(instance, schema, root, axis, keep,
                  stop_owner_boundaries=False):
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
            if axis == "x-review" and stop_owner_boundaries and \
                    rsub.get("x-reviewOwnerBoundary") is True:
                continue
            if rsub.get(axis) is not None:
                if rsub[axis] in keep:
                    out[key] = val
                continue
            child = _axis_project(
                val, sub, root, axis, keep,
                stop_owner_boundaries=stop_owner_boundaries)
            if child not in ({}, []):
                out[key] = child
        return out
    if isinstance(instance, (list, tuple)):
        items = schema.get("items", {})
        out = []
        for val in instance:
            child = _axis_project(
                val, items, root, axis, keep,
                stop_owner_boundaries=stop_owner_boundaries)
            if child not in ({}, []):
                out.append(child)
        return out
    return instance
