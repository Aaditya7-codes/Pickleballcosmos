#!/usr/bin/env python3
"""Wire the media guide and reported Story into discovery surfaces."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

state = ROOT / "data" / "state-of-pickleball-us-2026" / "index.html"
text = state.read_text(encoding="utf-8")
link = '<p><a class="source-link" href="/data/state-of-pickleball-us-2026/media/">Media &amp; citation guide: key findings, downloads and source notes →</a></p>'
marker = '<h2>The numbers that define the market</h2>'
if link not in text:
    text = text.replace(marker, link + marker, 1)
state.write_text(text, encoding="utf-8")

data = ROOT / "data" / "index.html"
text = data.read_text(encoding="utf-8")
media_card = '<a class="editorial-card" href="/data/state-of-pickleball-us-2026/media/"><div class="eyebrow">For Journalists &amp; Researchers</div><h3>State of the Game: Media &amp; Citation Guide</h3><p>Key findings, definitions, source notes and downloadable data from the 2026 flagship report.</p><div class="foot">Open media guide →</div></a>'
if media_card not in text:
    text = text.replace('<section class="section" style="padding-top:20px">', '<div class="list-grid">' + media_card + '</div><section class="section" style="padding-top:20px">', 1)
data.write_text(text, encoding="utf-8")

stories = ROOT / "stories" / "index.html"
text = stories.read_text(encoding="utf-8")
card = '<a class="editorial-card" href="/stories/pickleball-noise-court-planning/"><div class="eyebrow">Courts &amp; Communities · August 2026</div><h3>Pickleball Noise Is a Court-Planning Problem, Not a Culture War</h3><p>Why court location, hours, monitoring and alternatives matter more than the usual players-versus-neighbors framing.</p><div class="foot">Read analysis →</div></a>'
if card not in text:
    text = text.replace('</main>', card + '</main>', 1)
stories.write_text(text, encoding="utf-8")

courts = ROOT / "data" / "pickleball-courts-by-state-2026" / "index.html"
text = courts.read_text(encoding="utf-8")
story_link = '<p><a class="source-link" href="/stories/pickleball-noise-court-planning/">Why more courts also creates a siting problem: the pickleball-noise planning analysis →</a></p>'
if story_link not in text:
    text = text.replace('</article>', story_link + '</article>', 1)
courts.write_text(text, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
new = [
    '<url><loc>https://www.pickleballcosmos.com/data/state-of-pickleball-us-2026/media/</loc><lastmod>2026-08-16</lastmod></url>',
    '<url><loc>https://www.pickleballcosmos.com/stories/pickleball-noise-court-planning/</loc><lastmod>2026-08-16</lastmod></url>',
]
for entry in new:
    if entry not in text:
        text = text.replace('</urlset>', entry + '\n</urlset>')
sitemap.write_text(text, encoding="utf-8")
