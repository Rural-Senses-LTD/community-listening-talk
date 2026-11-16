"""Build the self-contained talk deck.

Reads src/slides.template.html, pastes in src/viewport-base.css (from the
skills-slides skill) verbatim, inlines every {{IMG:<file>}} from images/ as a
base64 data URI, and writes index.html next to this script, which is also the
page GitHub Pages serves. Run:

    python build.py
"""

from __future__ import annotations

import base64
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "src" / "slides.template.html"
VIEWPORT_BASE = ROOT / "src" / "viewport-base.css"
IMAGES = ROOT / "images"
OUTPUT = ROOT / "index.html"


def data_uri(name: str) -> str:
    """Return the image as a data URI so the deck works offline as a single file."""
    path = IMAGES / name
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def main() -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("{{VIEWPORT_BASE}}", VIEWPORT_BASE.read_text(encoding="utf-8"))
    html = re.sub(r"\{\{IMG:([^}]+)\}\}", lambda m: data_uri(m.group(1)), html)
    leftover = re.findall(r"\{\{[^}]+\}\}", html)
    if leftover:
        raise SystemExit(f"Unfilled placeholders: {leftover}")
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUTPUT} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
