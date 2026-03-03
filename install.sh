#!/usr/bin/env bash

set -e

THEME_NAME="monocons"
INSTALL_DIR="$HOME/.local/share/monocons"
ICON_DIR="$HOME/.local/share/icons/$THEME_NAME"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

ACTIVATE=false
UNINSTALL=false

# Parse flags
for arg in "$@"; do
	case "$arg" in
	--activate | -a)
		ACTIVATE=true
		;;
	--uninstall | -u)
		UNINSTALL=true
		;;
	*)
		echo "Unknown option: $arg"
		echo "Usage: $0 [--activate|-a] [--uninstall|-u]"
		exit 1
		;;
	esac
done

# UNINSTALL MODE

if [ "$UNINSTALL" = true ]; then
	echo "Uninstalling $THEME_NAME..."

	# Stop and disable systemd units
	systemctl --user disable --now monocons.path 2>/dev/null || true
	systemctl --user disable --now monocons.service 2>/dev/null || true

	# Remove systemd files
	rm -f "$SYSTEMD_USER_DIR/monocons.path"
	rm -f "$SYSTEMD_USER_DIR/monocons.service"

	systemctl --user daemon-reload

	# Remove installed files
	rm -rf "$INSTALL_DIR"
	rm -rf "$ICON_DIR"

	# If currently active, revert to Adwaita
	CURRENT=$(gsettings get org.gnome.desktop.interface icon-theme | tr -d "'")
	if [[ "$CURRENT" == "$THEME_NAME" ]]; then
		echo "Reverting icon theme to Adwaita..."
		gsettings set org.gnome.desktop.interface icon-theme "Adwaita"
	fi

	echo "monocons successfully removed."
	exit 0
fi

# INSTALL MODE

echo "Installing $THEME_NAME..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$ICON_DIR"
mkdir -p "$SYSTEMD_USER_DIR"

# Copy theme files
cp -r base "$INSTALL_DIR/"
cp generate.py index.theme build.sh "$INSTALL_DIR/"

# Make build executable
chmod +x "$INSTALL_DIR/build.sh"

# Install systemd service
cp systemd/monocons.service "$SYSTEMD_USER_DIR/"
cp systemd/monocons.path "$SYSTEMD_USER_DIR/"

# Reload systemd
systemctl --user daemon-reload

# Enable service
systemctl --user enable --now monocons.path

# Initial build
"$INSTALL_DIR/build.sh"

if [ "$ACTIVATE" = true ]; then
	echo "Activating monocons..."
	gsettings set org.gnome.desktop.interface icon-theme "$THEME_NAME"
fi

CURRENT=$(gsettings get org.gnome.desktop.interface icon-theme | tr -d "'")

if [[ "$CURRENT" != "$THEME_NAME" ]]; then
	echo "Monocons installed."
	echo "Run with --activate or -a to switch to it."
fi
