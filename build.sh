#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 generate.py

gtk-update-icon-cache "$HOME/.local/share/icons/monocons" || true
