#!/usr/bin/env python3

import os
import json

THEME_NAME = "monocons"
THEME_DIR = os.path.expanduser(f"~/.local/share/icons/{THEME_NAME}")
OUTPUT_DIR = os.path.join(THEME_DIR, "scalable/apps")
MAP_FILE = "icon_map.json"


def map_icons():
    if not os.path.exists(MAP_FILE):
        print(f"Map file '{MAP_FILE}' not found. Skipping mapping.")
        return

    with open(MAP_FILE, "r") as f:
        try:
            icon_map = json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading '{MAP_FILE}'. Ensure it is formatted correctly.")
            return

    for master_icon, aliases in icon_map.items():
        master_file = f"{master_icon}.svg"
        master_path = os.path.join(OUTPUT_DIR, master_file)

        if os.path.exists(master_path):
            for alias in aliases:
                alias_file = f"{alias}.svg"
                alias_path = os.path.join(OUTPUT_DIR, alias_file)

                if os.path.lexists(alias_path):
                    os.remove(alias_path)

                os.symlink(master_file, alias_path)
                print(f"mapped {alias_file} -> {master_file}")
        else:
            print(
                f"Warning: Master icon '{master_file}' not found. Skipping its mappings."
            )


if __name__ == "__main__":
    print("Creating icon mappings...")
    map_icons()
    print("Mapping complete.")
