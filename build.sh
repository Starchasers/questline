#!/usr/bin/env sh
# Dependency-light monorepo build and deterministic packaging entry point.
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$ROOT/tools/packaging/package.py" "$@"
