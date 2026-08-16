#!/usr/bin/env python3
"""Normalize discoverability metadata across the static site.

This is intentionally conservative: it updates existing Article JSON-LD records,
adds breadcrumb records to content articles, and replaces the legacy SVG social
card references with the raster card that social platforms can consistently fetch.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.pickleballcosmos.com"
SOCIAL = f"{SITE}/assets/social-card.png"
AUTHOR = {"@type": "Organization", "name": "Pickleball Cosmos Editorial", "url": f"{SITE}/editorial/"}
PUBLISHER = {
    "@type": "NewsMediaOrganization",
    "name": "Pickleball Cosmos",
    "url": f"{SITE}/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/logo.svg"},
    "publishingPrinciples": f"{SITE}/methodology/",
    "correctionsPolicy": f"{SITE}/corrections/",
}
SCRIPT_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.DOTALL)


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{SITE}/"
    if rel.endswith("/index.html"):
        return f"{SITE}/{rel[:-10]}"
    return f"{SITE}/{rel}"


def section_for(path: Path) -> str | None:
    parts = path.relative_to(ROOT).parts
    return parts[0].title() if parts and parts[0] in {"learn", "gear", "data", "stories"} else None


def json_script(obj: dict) -> str:
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"


def breadcrumb(url: str, section: str, headline: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": section, "item": f"{SITE}/{section.lower()}/"},
            {"@type": "ListItem", "position": 3, "name": headline, "item": url},
        ],
    }


def dataset_schema(url: str, headline: str, csv_href: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": headline,
        "url": url,
        "publisher": PUBLISHER,
        "distribution": {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": csv_href},
    }


def main() -> None:
    counts = Counter()
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts or "india" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        text = original.replace("https://www.pickleballcosmos.com/assets/social-card.svg", SOCIAL)
        if text != original:
            counts["raster_social_references"] += 1

        url = page_url(path)
        section = section_for(path)
        extra = []
        has_breadcrumb = False
        article_headline = None
        dataset_download = None

        def update_jsonld(match: re.Match[str]) -> str:
            nonlocal has_breadcrumb, article_headline
            raw = match.group(1).strip()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return match.group(0)
            if data.get("@type") == "BreadcrumbList":
                has_breadcrumb = True
            if data.get("@type") in {"Article", "NewsArticle"}:
                article_headline = data.get("headline") or article_headline
                data.setdefault("author", AUTHOR)
                data.setdefault("image", SOCIAL)
                data.setdefault("articleSection", section or "Pickleball")
                data["publisher"] = {**PUBLISHER, **data.get("publisher", {})}
                counts["article_markup_updated"] += 1
                return json_script(data)
            return match.group(0)

        text = SCRIPT_RE.sub(update_jsonld, text)
        if article_headline and section and not has_breadcrumb:
            extra.append(json_script(breadcrumb(url, section, article_headline)))
            counts["breadcrumbs_added"] += 1

        csv_match = re.search(r'(?:href|contentUrl)=["\']([^"\']+\.csv)["\']', text)
        if section == "Data" and article_headline and csv_match and '"@type":"Dataset"' not in text:
            csv_href = csv_match.group(1)
            if csv_href.startswith("/"):
                csv_href = SITE + csv_href
            elif not csv_href.startswith("http"):
                csv_href = f"{SITE}/{csv_href.lstrip('./')}"
            extra.append(json_script(dataset_schema(url, article_headline, csv_href)))
            counts["dataset_markup_added"] += 1

        if extra:
            text = text.replace("</head>", "".join(extra) + "</head>", 1)
        if text != original:
            path.write_text(text, encoding="utf-8")

    inventory = ROOT / "research" / "schema-inventory-2026-08-16.md"
    inventory.write_text(
        "# Schema inventory - August 16, 2026\n\n"
        "## Before normalization\n\n"
        "The site used a mixture of Article and NewsMediaOrganization records. Several older article templates omitted one or more of: organizational author, image, article section, publisher logo, or breadcrumb markup. Social metadata referenced an SVG card, which is not reliably rendered by major sharing surfaces.\n\n"
        "## Normalization applied\n\n"
        f"- Replaced legacy SVG social-card references on {counts['raster_social_references']} non-India HTML pages with `/assets/social-card.png`.\n"
        f"- Standardized Article / NewsArticle fields on {counts['article_markup_updated']} records: organizational author, raster image, article section, publisher identity and publisher logo.\n"
        f"- Added BreadcrumbList records to {counts['breadcrumbs_added']} content articles.\n"
        f"- Added Dataset records to {counts['dataset_markup_added']} data pages that expose a CSV download.\n\n"
        "## Deliberate exclusions\n\n"
        "India pages were not altered. Organization contactPoint and legal identity were not added because no verified public contact address or operating entity exists in the source repository.\n",
        encoding="utf-8",
    )
    print(json.dumps(counts, sort_keys=True))


if __name__ == "__main__":
    main()
