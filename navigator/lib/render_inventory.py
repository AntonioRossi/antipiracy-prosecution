"""Closed source inventory for code capable of changing artifact bytes.

The renderer trust boundary is intentionally narrower than the command and
verification implementation.  Every path in this tuple is a content input and
is hashed into artifact provenance.  Control-plane modules must not be added
merely because they share the Python package.
"""

RENDER_SOURCE_PATHS = (
    "navigator/lib/__init__.py",
    "navigator/lib/authority.py",
    "navigator/lib/canon.py",
    "navigator/lib/claims.py",
    "navigator/lib/depgraph.py",
    "navigator/lib/gateway.py",
    "navigator/lib/inputlock.py",
    "navigator/lib/model.py",
    "navigator/lib/profilepolicy.py",
    "navigator/lib/projections.py",
    "navigator/lib/registry.py",
    "navigator/lib/render.py",
    "navigator/lib/render_inventory.py",
    "navigator/lib/schema_validate.py",
    "navigator/lib/segmenter.py",
    "navigator/lib/timepolicy.py",
    "navigator/lib/unicode15_1.py",
    "navigator/lib/validate.py",
    "navigator/schema/invariants.py",
)
