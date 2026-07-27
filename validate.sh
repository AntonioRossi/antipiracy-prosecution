#!/usr/bin/env bash

set -euo pipefail

if (( $# != 0 )); then
    printf 'Usage: %s\n' "${0##*/}" >&2
    exit 64
fi

readonly repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
cd -- "$repository_root"

exec uv --no-cache --offline run --locked --no-sync \
    python -m navigator validate-current
