"""Pure content-input lock checks shared by rendering and promotion."""


def exact_set_problems(lock, declared_inputs):
    """Return exact-set defects between a lock and its declaration."""
    if not isinstance(lock, dict) or not isinstance(lock.get("reads"), list):
        return ["content lock has no reads array"]
    if not isinstance(declared_inputs, (list, tuple)) or not all(
            isinstance(path, str) and path for path in declared_inputs):
        return ["declared transitive inputs are malformed"]
    read = {
        entry.get("path") for entry in lock["reads"]
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }
    declared = set(declared_inputs)
    problems = []
    extra = sorted(read - declared)
    missing = sorted(declared - read)
    if extra:
        problems.append("undeclared content reads: %s" % extra)
    if missing:
        problems.append("declared content inputs not read: %s" % missing)
    if len(read) != len(lock["reads"]):
        problems.append("content lock reads are malformed or duplicated")
    if len(declared) != len(declared_inputs):
        problems.append("declared content inputs contain duplicates")
    return problems
