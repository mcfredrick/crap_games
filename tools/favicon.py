"""Draws the crap.games favicon from a 16x16 pixel grid.

Run from the repo root: uv run --with pillow python -I tools/favicon.py
Writes favicon.ico (16, 32, 48) and apple-touch-icon.png (180) next to index.html.
"""

from pathlib import Path

from PIL import Image

GRID = [
    "................",
    "................",
    "...........M....",
    "......KK..MMM...",
    ".....KLBK..M....",
    "......KBBK......",
    "....KKKBBBKK....",
    "...KLBBBBBBBK...",
    "...KBWKBBWKBK...",
    "..KKBWKBBWKBKK..",
    ".KLBBBBBBBBBBBK.",
    ".KBBKBBBBBBKBBK.",
    "KLBBBKKKKKKBBBBK",
    "KBBBBBBBBBBBBBBK",
    ".KKKKKKKKKKKKKK.",
    "................",
]

COLORS = {
    ".": (255, 255, 0),
    "K": (59, 31, 14),
    "B": (139, 69, 19),
    "L": (196, 120, 60),
    "W": (255, 255, 255),
    "M": (255, 0, 255),
}

ROOT = Path(__file__).resolve().parent.parent


def draw() -> Image.Image:
    assert len(GRID) == 16 and all(len(row) == 16 for row in GRID)
    img = Image.new("RGB", (16, 16))
    img.putdata([COLORS[c] for row in GRID for c in row])
    return img


def main() -> None:
    base = draw()
    sizes = [16, 32, 48]
    frames = [base.resize((s, s), Image.NEAREST) for s in sizes]
    # Pillow drops any ICO size larger than the image it saves from, so save from the largest.
    frames[-1].save(ROOT / "favicon.ico", sizes=[(s, s) for s in sizes], append_images=frames[:-1])
    # 176 is a whole multiple of 16, so every pixel stays square; the yellow border fills to 180.
    touch = Image.new("RGB", (180, 180), COLORS["."])
    touch.paste(base.resize((176, 176), Image.NEAREST), (2, 2))
    touch.save(ROOT / "apple-touch-icon.png")


if __name__ == "__main__":
    main()
