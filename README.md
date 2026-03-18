# monocons

**Dynamic Material You monochrome icons for GNOME.**

monocons is a dynamic icon theme that automatically adapts to your system's current GTK accent and background colors. It works by taking flat, monochrome SVGs and compiling them into perfectly scaled, squircle-shaped icons on the fly.

Whenever you change your system accent color, a lightweight background service instantly detects the change and rebuilds the theme to match.

## Features

- **True Dynamic Theming:** Automatically reads from `~/.config/gtk-4.0/gtk.css` to match your system.
- **Instant Rebuilds:** Uses lightweight systemd paths to watch for color changes without polling.
- **Smart Aliasing:** Uses a clean `icon_map.json` file to map dozens of app variants (like Flatpaks or specific release versions) to a single base SVG using efficient symlinks.
- **Broad Fallbacks:** Inherits from Papirus and Adwaita to ensure total system coverage.

## Installation

To install monocons, clone the repository and run the install script.

```bash
# Clone the repository
git clone https://github.com/k4ustu3h/monocons-gnome.git

# Navigate into the directory
cd monocons-gnome

# Run the installer and automatically activate the theme
./install.sh --activate
```

_Note: If you just want to install the theme in the background without switching to it immediately, run `./install.sh` without the `--activate` flag._

## Uninstallation

The install script comes with a clean uninstall routine that removes all files, disables the systemd services, and safely reverts your icon theme back to Adwaita.

```bash
cd monocons-gnome
./install.sh --uninstall
```

## Recommendations

To get the true "Material You" experience on GNOME, it is recommended to use this icon theme alongside the **Material You Colors** GNOME extension. This extension automatically extracts accent colors from your wallpaper and applies them to the system, which will in turn automatically trigger monocons to rebuild.

- [Material You Colors Extension](https://github.com/FrancescoCaracciolo/material-you-colors)

## Credits

- **[Material Symbols](https://fonts.google.com/icons)**
- **[Simple Icons](https://simpleicons.org/)**
- **[Papirus Icon Theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme)**
