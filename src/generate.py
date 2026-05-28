#!/usr/bin/env python3

import os
import re
import shutil
import xml.etree.ElementTree as ET

THEME_NAME = "monocons"

BASE_DIR = "base/scalable/apps"
THEME_DIR = os.path.expanduser(f"~/.local/share/icons/{THEME_NAME}")
OUTPUT_DIR = os.path.join(THEME_DIR, "scalable/apps")

SQUIRCLE_PATH = "M176 102c0 22.358 0 33.538-3.511 42.406a50 50 0 0 1-28.083 28.083C135.538 176 124.358 176 102 176H90c-22.358 0-33.538 0-42.406-3.511a50 50 0 0 1-28.083-28.083C16 135.538 16 124.358 16 102V90c0-22.358 0-33.538 3.511-42.406a50 50 0 0 1 28.083-28.083C56.462 16 67.642 16 90 16h12c22.358 0 33.538 0 42.406 3.511a50 50 0 0 1 28.083 28.083C176 56.462 176 67.642 176 90z"

CANVAS_SIZE = 192
INNER_SIZE = 118
INNER_OFFSET = (CANVAS_SIZE - INNER_SIZE) / 2

GTK_CSS = os.path.expanduser("~/.config/gtk-4.0/gtk.css")


def get_gtk_color(name):
    if not os.path.exists(GTK_CSS):
        return None

    with open(GTK_CSS) as f:
        match = re.search(rf"@define-color {name} (#[0-9a-fA-F]+);", f.read())

    return match.group(1) if match else None


def get_accent():
    return get_gtk_color("accent_color") or "#7f5af0"


def get_background():
    return get_gtk_color("window_bg_color") or "#2e2e2e"


def strip_namespace(root):
    for elem in root.iter():
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]


def extract_svg_data(svg_path):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    strip_namespace(root)

    viewbox = root.attrib.get("viewBox", "0 0 192 192")
    _, _, width, height = map(float, viewbox.replace(",", " ").split())

    for elem in root.iter():
        elem.attrib.pop("fill", None)
        elem.attrib.pop("stroke", None)

    elements = []
    for child in root:
        if child.tag in {"path", "rect", "circle", "polygon", "g", "defs"}:
            elements.append(ET.tostring(child, encoding="unicode"))

    return "\n".join(elements), width, height


def build_icon(path_data, fg, bg, orig_w, orig_h):
    scale = INNER_SIZE / max(orig_w, orig_h)

    return f"""<svg viewBox="0 0 {CANVAS_SIZE} {CANVAS_SIZE}" xmlns="http://www.w3.org/2000/svg">
  <path fill="{bg}" d="{SQUIRCLE_PATH}"/>
  <g fill="{fg}" transform="translate({INNER_OFFSET},{INNER_OFFSET}) scale({scale})">
    {path_data}
  </g>
</svg>
"""


def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def copy_index():
    shutil.copy("index.theme", THEME_DIR)


def generate_icons():
    fg = get_accent()
    bg = get_background()

    for file in os.listdir(BASE_DIR):
        if file.endswith(".svg"):
            src = os.path.join(BASE_DIR, file)
            dst = os.path.join(OUTPUT_DIR, file)

            paths, w, h = extract_svg_data(src)
            with open(dst, "w") as f:
                f.write(build_icon(paths, fg, bg, w, h))

            print(f"generated {file}")


def main():
    ensure_dirs()
    copy_index()
    generate_icons()
    print("\nmonocons generated successfully")


if __name__ == "__main__":
    main()
