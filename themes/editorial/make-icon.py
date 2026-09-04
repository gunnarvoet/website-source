# /// script
# requires-python = ">=3.11"
# dependencies = ["fonttools", "brotli"]
# ///
"""Draw the site icon: a GV monogram knocked out of a dark tile.

The letters are cut from the theme's own Archivo file at the same variable
setting the display headlines use (wdth 70, wght 900), so the icon is set in
the site's face rather than an approximation of it. The glyphs are converted
to outlines, so nothing has to load a font to render the icon.

Writes into static/icons/: icon.svg is the one browsers should take; the PNGs
are the fallbacks that cannot be SVG (Safari's older favicon path, the iOS
home screen, the web app manifest).

    uv run themes/editorial/make-icon.py

Needs rsvg-convert (brew install librsvg) for the PNGs. Run it after changing
the palette or the display cut; the output is committed, and nothing in the
build regenerates it.
"""

import subprocess
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = Path(__file__).parent
FONT = HERE / "static/fonts/archivo-latin.woff2"
OUT = HERE / "static/icons"

TEXT = "GV"
PAPER = "#f2f0ea"  # --paper
ABYSS = "#0f2b33"  # --abyss
WGHT, WDTH = 900, 70  # the display cut, as used by the headlines
TRACKING = 0.02  # em, matching .brand
MARGIN = 4  # of a 64-unit tile
SIZE = 64

PNGS = {  # filename -> pixel size
    "icon-32.png": 32,  # favicon fallback
    "apple-touch-icon.png": 180,  # iOS home screen
    "icon-192.png": 192,  # manifest
    "icon-512.png": 512,  # manifest
}


def monogram_svg():
    font = instancer.instantiateVariableFont(TTFont(FONT), {"wght": WGHT, "wdth": WDTH})
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    track = TRACKING * font["head"].unitsPerEm

    # lay the glyphs out along a baseline at y=0, in font units
    names = [cmap[ord(c)] for c in TEXT]
    offsets, pen_x = [], 0.0
    for i, name in enumerate(names):
        offsets.append(pen_x)
        pen_x += hmtx[name][0] + (track if i < len(names) - 1 else 0)

    # Center on the inked bounds, not on the advance widths: the side bearings
    # and the G's overshoot would otherwise push the pair off center in a tile
    # this small.
    x0 = y0 = float("inf")
    x1 = y1 = float("-inf")
    for name, dx in zip(names, offsets):
        bounds = BoundsPen(glyphs)
        glyphs[name].draw(bounds)
        a, b, c, d = bounds.bounds
        x0, y0 = min(x0, a + dx), min(y0, b)
        x1, y1 = max(x1, c + dx), max(y1, d)

    scale = (SIZE - 2 * MARGIN) / (x1 - x0)
    ox = MARGIN - x0 * scale
    oy = (SIZE + (y1 - y0) * scale) / 2 + y0 * scale  # SVG y grows downward

    paths = []
    for name, dx in zip(names, offsets):
        pen = SVGPathPen(glyphs)
        place = Transform(scale, 0, 0, -scale, ox + dx * scale, oy)
        glyphs[name].draw(TransformPen(pen, place))
        paths.append(pen.getCommands())

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}">\n'
        f'  <rect width="{SIZE}" height="{SIZE}" fill="{ABYSS}"/>\n'
        f'  <path fill="{PAPER}" d="{" ".join(paths)}"/>\n'
        f"</svg>\n"
    )


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    svg = OUT / "icon.svg"
    svg.write_text(monogram_svg())
    print(f"wrote {svg.relative_to(HERE)}")
    for name, px in PNGS.items():
        subprocess.run(
            ["rsvg-convert", "-w", str(px), "-h", str(px), "-o", str(OUT / name), str(svg)],
            check=True,
        )
        print(f"wrote {(OUT / name).relative_to(HERE)} ({px}px)")


if __name__ == "__main__":
    main()
