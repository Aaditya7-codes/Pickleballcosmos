#!/usr/bin/env python3
"""Wire the first public briefing and citation resources into existing pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

briefing = ROOT / "briefing" / "index.html"
text = briefing.read_text(encoding="utf-8")
archive = '<section class="newsletter" style="margin-top:18px;align-items:start"><div><div class="eyebrow">Archive</div><h2>Read the published editions.</h2><p>Each public archive edition preserves the links, definitions and source context available when it was prepared.</p></div><div><a class="editorial-card" href="/briefing/archive/issue-001/"><div class="eyebrow">Issue 001 · August 16, 2026</div><h3>The Numbers Need Context</h3><p>Rules, participation, rankings, approval status and one strong read - the first public Cosmos Briefing.</p><div class="foot">Read issue →</div></a></div></section>'
if archive not in text:
    text = text.replace('<div class="newsletter-benefits">', archive + '<div class="newsletter-benefits">', 1)
briefing.write_text(text, encoding="utf-8")

home = ROOT / "index.html"
text = home.read_text(encoding="utf-8")
launch = 'Want more context first? <a href="/briefing/">See what the briefing covers →</a>'
replacement = 'Read the first public edition: <a href="/briefing/archive/issue-001/">The Numbers Need Context →</a>'
if replacement not in text:
    text = text.replace(launch, replacement, 1)
home.write_text(text, encoding="utf-8")

flagship = ROOT / "data" / "state-of-pickleball-us-2026" / "index.html"
text = flagship.read_text(encoding="utf-8")
text = text.replace('"dateModified":"2026-08-12"', '"dateModified":"2026-08-16"')
text = text.replace('Published August 12, 2026</span></div>', 'Updated August 16, 2026</span></div>')
citation = '<div class="source-box"><h3>Cite and use this report</h3><p><strong>Suggested citation:</strong> Pickleball Cosmos Editorial. <em>The State of Pickleball in the U.S. 2026.</em> Pickleball Cosmos, updated August 16, 2026. https://www.pickleballcosmos.com/data/state-of-pickleball-us-2026/</p><p><a class="source-link" href="/data/state-of-pickleball-us-2026.csv" download>Download the report data (CSV) →</a> &nbsp; <a class="source-link" href="/data/dataset-terms/">Dataset use terms →</a></p><p style="font-size:.83rem;color:#92a0aa">The CSV preserves the reported figures shown in this report. It is not a new survey or a replacement for the underlying sources.</p></div>'
marker = '<h2>The numbers that define the market</h2>'
if citation not in text:
    text = text.replace(marker, citation + marker, 1)
flagship.write_text(text, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
text = text.replace('<url><loc>https://www.pickleballcosmos.com/briefing/</loc><lastmod>2026-08-14</lastmod></url>', '<url><loc>https://www.pickleballcosmos.com/briefing/</loc><lastmod>2026-08-16</lastmod></url>')
text = text.replace('<url><loc>https://www.pickleballcosmos.com/data/state-of-pickleball-us-2026/</loc><lastmod>2026-08-12</lastmod></url>', '<url><loc>https://www.pickleballcosmos.com/data/state-of-pickleball-us-2026/</loc><lastmod>2026-08-16</lastmod></url>')
entry = '<url><loc>https://www.pickleballcosmos.com/briefing/archive/issue-001/</loc><lastmod>2026-08-16</lastmod></url>'
if entry not in text:
    text = text.replace('<url><loc>https://www.pickleballcosmos.com/briefing/</loc><lastmod>2026-08-16</lastmod></url>', '<url><loc>https://www.pickleballcosmos.com/briefing/</loc><lastmod>2026-08-16</lastmod></url>\n' + entry)
sitemap.write_text(text, encoding="utf-8")
