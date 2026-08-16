#!/usr/bin/env python3
"""Lightweight static integrity checks for the published site."""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.pickleballcosmos.com"
SCRIPT_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def normalize(path: str) -> str:
    path = path.split("#", 1)[0].split("?", 1)[0]
    return path if path.endswith(("/", ".html")) else path + "/"


def main() -> int:
    urls = re.findall(rf"<loc>{re.escape(SITE)}([^<]*)</loc>", (ROOT / "sitemap.xml").read_text())
    sitemap = {normalize(url) for url in urls}
    inbound = {url: [] for url in sitemap}
    issues = []
    article_records = 0
    for page in ROOT.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for href in re.findall(r'(?:href|src)=["\']([^"\']+)["\']', text):
            if href.startswith("/"):
                target = normalize(href)
                if target in inbound:
                    inbound[target].append(page.relative_to(ROOT).as_posix())
        for match in SCRIPT_RE.finditer(text):
            try:
                data = json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                issues.append(f"invalid JSON-LD: {page.relative_to(ROOT)} ({exc})")
                continue
            if data.get("@type") in {"Article", "NewsArticle"} and "india" not in page.parts:
                article_records += 1
                for key in ("author", "image", "articleSection", "publisher"):
                    if key not in data:
                        issues.append(f"Article missing {key}: {page.relative_to(ROOT)}")
    coverage = ROOT / "research" / "internal-link-coverage-2026-08-16.csv"
    with coverage.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["sitemap_url", "source_level_inbound_links", "sample_source_pages"])
        for url in sorted(sitemap):
            refs = sorted(set(inbound[url]))
            writer.writerow([url, len(refs), " | ".join(refs[:8])])
            if len(refs) < 2:
                issues.append(f"fewer than two inbound links: {url}")
    non_india = [p for p in ROOT.rglob("*.html") if "india" not in p.parts]
    svg_references = [p.relative_to(ROOT).as_posix() for p in non_india if "assets/social-card.svg" in p.read_text(encoding="utf-8")]
    if svg_references:
        issues.append("legacy SVG social-card references remain: " + ", ".join(svg_references))
    print(f"sitemap_urls={len(sitemap)}")
    print(f"article_records_checked={article_records}")
    print(f"urls_with_at_least_two_source_links={sum(len(set(v)) >= 2 for v in inbound.values())}")
    print(f"coverage_report={coverage.relative_to(ROOT)}")
    if issues:
        print("\n".join(issues), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
