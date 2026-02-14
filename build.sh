#!/usr/bin/env bash

set -e

python3 generate.py

gtk-update-icon-cache ~/.local/share/icons/monocons || true
