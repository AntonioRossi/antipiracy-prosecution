"""Typed failures for the structured-source command boundary."""


class StructuredSourceError(ValueError):
    """A closed structured-source contract was not satisfied."""


class EnvironmentError(StructuredSourceError):
    """The project-local locked execution environment is not exact."""


class ParseError(StructuredSourceError):
    """XML bytes violate secure parsing or resource limits."""


class SchemaError(StructuredSourceError):
    """XML bytes do not validate against the selected XSD 1.1 profile."""
