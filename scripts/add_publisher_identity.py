#!/usr/bin/env python3
"""Apply the approved accountable-publisher details without creating a legal entity claim."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAIL = "pickleball.hero7@gmail.com"

for path in ROOT.rglob("*.html"):
    if "india" in path.parts or path == ROOT / "contact" / "index.html":
        continue
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        '<a href="/editorial/">Editorial</a><a href="/methodology/">Methodology</a>',
        '<a href="/editorial/">Editorial</a><a href="/methodology/">Methodology</a><a href="/contact/">Contact</a>',
    )
    text = re.sub(
        r'(<a href="/methodology/">Methodology</a>)(?:<a href="/contact/">Contact</a>)*',
        r'\1<a href="/contact/">Contact</a>',
        text,
    )
    text = text.replace(
        '<span>Independently published by Aaditya Sharma.</span>',
        '<span>Independent pickleball media.</span>',
    )
    if path == ROOT / "corrections" / "index.html":
        marker = '<h2>Factual errors</h2>'
        addition = '<h2>How to submit a correction</h2><p>Email <a class="source-link" href="mailto:pickleball.hero7@gmail.com?subject=Correction%20request">pickleball.hero7@gmail.com</a> with the page URL, the specific claim at issue and the best available supporting source. We review substantiated requests and date material corrections or updates.</p>'
        if addition not in text:
            text = text.replace(marker, addition + marker, 1)
    if path == ROOT / "about" / "index.html":
        marker = '<h2>How accountability works</h2>'
        addition = '<p><strong>Publisher:</strong> Pickleball Cosmos is independently published by Aaditya Sharma. For editorial, corrections, data and press enquiries, use the <a class="source-link" href="/contact/">publication contact route</a>.</p>'
        if addition not in text:
            text = text.replace(marker, addition + marker, 1)
    if path in {ROOT / "index.html", ROOT / "about" / "index.html"}:
        text = text.replace(
            '"correctionsPolicy":"https://www.pickleballcosmos.com/corrections/"}',
            '"correctionsPolicy":"https://www.pickleballcosmos.com/corrections/","email":"pickleball.hero7@gmail.com","founder":{"@type":"Person","name":"Aaditya Sharma"}}',
        )
    if text != original:
        path.write_text(text, encoding="utf-8")

site_js = ROOT / "assets" / "site.js"
text = site_js.read_text(encoding="utf-8")
text = re.sub(
    r'(<a href="/methodology/">Methodology</a>)(?:<a href="/contact/">Contact</a>)*',
    r'\1<a href="/contact/">Contact</a>',
    text,
)
text = text.replace('Independently published by Aaditya Sharma.</span></div>', 'Independent pickleball media.</span></div>')
site_js.write_text(text, encoding="utf-8")

sitemap = ROOT / "sitemap.xml"
text = sitemap.read_text(encoding="utf-8")
entry = '<url><loc>https://www.pickleballcosmos.com/contact/</loc><lastmod>2026-08-16</lastmod></url>'
if entry not in text:
    text = text.replace('<url><loc>https://www.pickleballcosmos.com/corrections/</loc><lastmod>2026-08-12</lastmod></url>', '<url><loc>https://www.pickleballcosmos.com/corrections/</loc><lastmod>2026-08-12</lastmod></url>\n' + entry)
sitemap.write_text(text, encoding="utf-8")
