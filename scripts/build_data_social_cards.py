#!/usr/bin/env python3
"""Create restrained, raster social cards for non-India Data studies."""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "social"
SITE = "https://www.pickleballcosmos.com"


def line_wrap(text: str, width: int = 24, max_lines: int = 3) -> list[str]:
    words = text.split()
    lines, current = [], ""
    for word in words:
        next_line = f"{current} {word}".strip()
        if len(next_line) <= width or not current:
            current = next_line
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".,;:") + "…"
    return lines


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for path in sorted((ROOT / "data").glob("*/index.html")):
        if path.parent.name == "dataset-terms":
            continue
        text = path.read_text(encoding="utf-8")
        title_match = re.search(r'<meta property="og:title" content="([^"]+)">', text)
        description_match = re.search(r'<meta property="og:description" content="([^"]+)">', text)
        if not title_match:
            continue
        title = html.unescape(title_match.group(1)).replace(" — Pickleball Cosmos", "")
        description = html.unescape(description_match.group(1)) if description_match else "Original data and reporting from Pickleball Cosmos."
        slug = path.parent.name
        output = ASSETS / f"{slug}.png"
        lines = line_wrap(title)
        title_svg = "".join(f'<text x="104" y="{306 + i * 64}" fill="#f5f7f2" font-family="Georgia,Times New Roman,serif" font-size="55" font-weight="700">{html.escape(line)}</text>' for i, line in enumerate(lines))
        description_line = html.escape(description[:88].rstrip(".,;:") + ("…" if len(description) > 88 else ""))
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
<rect width="1200" height="630" fill="#07111b"/><rect x="66" y="66" width="1068" height="498" rx="28" fill="#0c1824" stroke="#21303d" stroke-width="2"/>
<circle cx="142" cy="142" r="34" fill="#cfff36"/><circle cx="129" cy="130" r="4" fill="#07111b"/><circle cx="146" cy="121" r="4" fill="#07111b"/><circle cx="159" cy="137" r="4" fill="#07111b"/><circle cx="132" cy="151" r="4" fill="#07111b"/><circle cx="151" cy="158" r="4" fill="#07111b"/>
<text x="196" y="155" fill="#f5f7f2" font-family="Arial,Helvetica,sans-serif" font-size="32" font-weight="700" letter-spacing="1">PICKLEBALL COSMOS</text><text x="104" y="226" fill="#cfff36" font-family="Arial,Helvetica,sans-serif" font-size="22" font-weight="700" letter-spacing="3">DATA DESK</text>
{title_svg}
<text x="108" y="518" fill="#98a6b3" font-family="Arial,Helvetica,sans-serif" font-size="23">{description_line}</text><rect x="108" y="548" width="168" height="6" rx="3" fill="#cfff36"/>
</svg>'''
        svg_path = ASSETS / f"{slug}.svg"
        svg_path.write_text(svg, encoding="utf-8")
        subprocess.run(["rsvg-convert", "--width", "1200", "--height", "630", "--output", str(output), str(svg_path)], check=True)
        svg_path.unlink()
        social = f"{SITE}/assets/social/{slug}.png"
        text = re.sub(r'(property="og:image" content=")[^"]+("\s*>)', rf'\g<1>{social}\2', text)
        text = re.sub(r'(name="twitter:image" content=")[^"]+("\s*>)', rf'\g<1>{social}\2', text)
        text = text.replace(f'"image":"{SITE}/assets/social-card.png"', f'"image":"{social}"')
        path.write_text(text, encoding="utf-8")
        print(f"{path.relative_to(ROOT)} -> {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
