"""Execute the sole current navigator command boundary."""

from __future__ import annotations

import sys

from .build import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
