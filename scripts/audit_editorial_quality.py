#!/usr/bin/env python3
"""Flag cliches and mechanically over-sectioned public pages for editorial review."""
from pathlib import Path
import re
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED = {"india", "node_modules", ".git"}
CLICHES = [r"\bwhether you(?:'re| are)\b", r"\beverything you need to know\b", r"\bultimate guide\b", r"\blet'?s dive\b", r"\bin this (?:guide|article|post)\b", r"\bgame[ -]?changer\b", r"\bit'?s worth noting\b", r"\bmore than just\b", r"\bseamless\b"]

class ArticleText(HTMLParser):
    def __init__(self):
        super().__init__(); self.in_article = False; self.text = []; self.h2 = 0; self.h3 = 0
    def handle_starttag(self, tag, attrs):
        if tag == "article": self.in_article = True
        elif self.in_article and tag in {"h2", "h3"}: setattr(self, tag, getattr(self, tag) + 1)
    def handle_endtag(self, tag):
        if tag == "article": self.in_article = False
    def handle_data(self, data):
        if self.in_article: self.text.append(data)

issues = []
for path in sorted(ROOT.rglob("*.html")):
    if EXCLUDED.intersection(path.relative_to(ROOT).parts): continue
    parser = ArticleText(); parser.feed(path.read_text(encoding="utf-8"))
    if not parser.text: continue
    text = " ".join(" ".join(parser.text).split())
    words = len(re.findall(r"\b[\w’'-]+\b", text))
    cliches = [pattern for pattern in CLICHES if re.search(pattern, text, re.I)]
    density = parser.h2 / max(words, 1) * 1000
    if cliches or (parser.h2 >= 12 and density > 8): issues.append((path.relative_to(ROOT).as_posix(), words, parser.h2, parser.h3, density, cliches))

print("Editorial quality audit")
print("Flags are prompts for an editor, not automatic rewrite instructions.")
print(f"pages_flagged={len(issues)}")
for path, words, h2, h3, density, cliches in issues:
    reasons = (["cliche=" + ",".join(cliches)] if cliches else []) + ([f"h2_density={density:.1f}/1k words"] if h2 >= 12 and density > 8 else [])
    print(f"{path}\twords={words}\th2={h2}\th3={h3}\t" + "; ".join(reasons))
