"""Closed source inventory for verification and promotion control code.

These paths are bound by acceptance receipts rather than artifact provenance.
Renderer inputs are independently bound by each receipt's content-lock
subject, so a source belongs to one inventory instead of two.
"""

CONTROL_SOURCE_PATHS = (
    "navigator/lib/acceptance.py",
    "navigator/build.py",
    "navigator/lib/bundleplan.py",
    "navigator/lib/bundlezip.py",
    "navigator/lib/control_inventory.py",
    "navigator/lib/currentstate.py",
    "navigator/lib/migrate.py",
    "navigator/lib/pinplan.py",
    "navigator/lib/qaevidence.py",
    "navigator/lib/qaregistry.py",
    "navigator/lib/recordprovenance.py",
    "navigator/lib/recordresolver.py",
    "navigator/lib/release.py",
    "navigator/lib/snapshot.py",
)
