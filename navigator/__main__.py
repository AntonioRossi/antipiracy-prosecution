"""Module execution entry: ``python3 -m navigator <command>``.

Delegates to :func:`build.main` after the same ``sys.path`` bootstrap that
``python3 navigator/build.py`` performs, so both entries share exactly one
dispatch.  ``validate-current`` is the canonical command for this entry.
"""

import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build  # noqa: E402

if __name__ == "__main__":
    build.main(sys.argv[1:])
