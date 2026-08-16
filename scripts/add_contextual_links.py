#!/usr/bin/env python3
"""Add reviewed contextual cross-links to pages with weak source-level discovery."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINKS = {
    "gear/how-to-choose-first-pickleball-paddle/index.html": '<p><a class="source-link" href="/gear/elongated-vs-standard-pickleball-paddles/">Elongated vs standard: compare the shape trade-off in detail →</a></p><p>Shopping to a firm budget? <a class="source-link" href="/gear/best-pickleball-paddles-under-100/">See the under-$100 buying guide and its research ledger →</a></p>',
    "gear/14mm-vs-16mm-pickleball-paddles/index.html": '<p><a class="source-link" href="/gear/elongated-vs-standard-pickleball-paddles/">Shape is often the next useful comparison: elongated vs standard paddles →</a></p>',
    "learn/pickleball-scoring/index.html": '<p><a class="source-link" href="/learn/what-does-0-0-2-mean-pickleball/">Need the opening score only? See why doubles starts at 0-0-2 →</a></p>',
    "data/state-of-pickleball-us-2026/index.html": '<p><a class="source-link" href="/data/pickleball-facility-scale-by-state-2026/">Related analysis: which states concentrate courts into larger listed locations? →</a></p>',
    "data/pickleball-courts-by-state-2026/index.html": '<p><a class="source-link" href="/data/dataset-terms/">Dataset use terms: citation, sharing and source-rights guidance →</a></p>',
}

for relative, link in LINKS.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if link in text:
        continue
    path.write_text(text.replace("</article>", link + "</article>", 1), encoding="utf-8")

path = ROOT / "data/index.html"
text = path.read_text(encoding="utf-8")
terms = '<div class="list-section-head list-section-spaced"><div class="eyebrow">Data use</div><h2>Methods, terms and source limits</h2><p>Each data page distinguishes reported figures from Cosmos calculations and preserves the scope of the underlying source material.</p></div><div class="list-grid"><a class="editorial-card" href="/data/dataset-terms/"><div class="eyebrow">Terms</div><h3>Dataset Use Terms</h3><p>How to cite, share and work with Pickleball Cosmos datasets while preserving third-party source rights.</p><div class="foot">Read terms →</div></a></div>'
if terms not in text:
    text = text.replace('<section class="section" style="padding-top:20px">', terms + '<section class="section" style="padding-top:20px">', 1)
path.write_text(text, encoding="utf-8")
