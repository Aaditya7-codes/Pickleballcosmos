#!/usr/bin/env python3
"""Render three citation-ready State of the Game PNG cards."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "media"
OUT.mkdir(parents=True, exist_ok=True)
CARDS = [
    ("state-of-pickleball-24-3m", "24.3M", "U.S. PICKLEBALL PARTICIPANTS", "SFIA reported annual participants in 2025. Participation is not a membership count."),
    ("state-of-pickleball-7-5m", "7.5M", "CORE PARTICIPANTS", "Players who participated at least eight times during 2025, according to SFIA."),
    ("state-of-pickleball-82-613", "82,613", "KNOWN COURTS", "A Pickleheads database count cited by USA Pickleball - not a complete national census."),
]
for slug, stat, label, note in CARDS:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><rect width="1200" height="630" fill="#07111b"/><rect x="66" y="66" width="1068" height="498" rx="28" fill="#0c1824" stroke="#21303d" stroke-width="2"/><circle cx="142" cy="142" r="34" fill="#cfff36"/><circle cx="129" cy="130" r="4" fill="#07111b"/><circle cx="146" cy="121" r="4" fill="#07111b"/><circle cx="159" cy="137" r="4" fill="#07111b"/><circle cx="132" cy="151" r="4" fill="#07111b"/><circle cx="151" cy="158" r="4" fill="#07111b"/><text x="196" y="155" fill="#f5f7f2" font-family="Arial,Helvetica,sans-serif" font-size="32" font-weight="700" letter-spacing="1">PICKLEBALL COSMOS</text><text x="104" y="226" fill="#cfff36" font-family="Arial,Helvetica,sans-serif" font-size="22" font-weight="700" letter-spacing="3">STATE OF THE GAME · 2026</text><text x="104" y="408" fill="#f5f7f2" font-family="Georgia,Times New Roman,serif" font-size="156" font-weight="700">{stat}</text><text x="108" y="466" fill="#f5f7f2" font-family="Arial,Helvetica,sans-serif" font-size="29" font-weight="700" letter-spacing="1">{label}</text><text x="108" y="518" fill="#98a6b3" font-family="Arial,Helvetica,sans-serif" font-size="22">{note}</text><rect x="108" y="548" width="168" height="6" rx="3" fill="#cfff36"/></svg>'''
    source = OUT / f"{slug}.svg"
    source.write_text(svg, encoding="utf-8")
    subprocess.run(["rsvg-convert", "--width", "1200", "--height", "630", "--output", str(OUT / f"{slug}.png"), str(source)], check=True)
    source.unlink()
