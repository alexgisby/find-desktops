# find-desktops.py

Quick Python script to recursively find images in a directory that are above a certain
size (ie for your desktop background!).

You can specify a minimum width and/or height for the image to be, or will default to
detecting your screen resolution and using that.

Files are copied to a separate directory to avoid munging your beautifully arranged files!

## Requirements

Requires [PIL](http://www.pythonware.com/products/pil/)

Everything else is standard lib.

## Docs

Usage:
    python find_desktops.py [OPTS]

Requires:
    PIL

Options:
    --path          Path to search on. Defaults to ./
    --min-width     Minimum width for images to be. Defaults to screen resolution
    --min-height    Minimum height for images to be. Defaults to screen resolution
    --copy-dir      Directory to copy desktops to. Default: ./DesktopsFound
    --orientation   Orientation to limit to (horizontal or vertical)