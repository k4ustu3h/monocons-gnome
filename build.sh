#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python3 generate.py
python3 map_icons.py

gtk-update-icon-cache -f "$HOME/.local/share/icons/monocons" || true
