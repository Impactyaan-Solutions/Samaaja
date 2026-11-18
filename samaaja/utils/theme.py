import re

import frappe

# Shade -> (percent of the brand colour, colour it is mixed with).
# 600 is the brand colour itself; lighter shades mix towards white,
# darker ones towards black.
SHADES = {
    50: (8, "white"),
    100: (18, "white"),
    200: (35, "white"),
    300: (55, "white"),
    400: (75, "white"),
    500: (90, "white"),
    600: (100, None),
    700: (85, "black"),
    800: (70, "black"),
    900: (55, "black"),
}

HEX_COLOUR = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def _scale(name, colour):
    lines = []
    for shade, (percent, base) in SHADES.items():
        value = colour if base is None else f"color-mix(in oklch, {colour} {percent}%, {base})"
        lines.append(f"--color-{name}-{shade}: {value};")
    return "".join(lines)


def get_theme_css():
    """CSS injected into www/index.html on every page load.

    Overrides the default primary-* tokens from frontend/src/style.css with
    the colour chosen in Samaaja Settings, then appends the custom CSS.
    Empty settings return "", so the defaults in style.css apply.
    """
    settings = frappe.get_cached_doc("Samaaja Settings")

    css = ""
    colour = (settings.get("colour") or "").strip()
    if HEX_COLOUR.match(colour):
        css = ":root{" + _scale("primary", colour) + "}"

    css += settings.get("custom_css") or ""

    # The result sits inside a <style> tag: never let it close that tag.
    return re.sub(r"</style", "", css, flags=re.IGNORECASE)
