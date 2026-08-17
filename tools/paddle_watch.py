#!/usr/bin/env python3
"""Pickleball Cosmos Paddle Approval Watch.

Collects a compact observation from USA Pickleball's public Approved Paddle
List and Paddle Compliance Report, validates it, compares it with the prior
observation, and preserves only material changes.

Editorial rule: detection is automated; publication and interpretation are not.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

APPROVED_URL = "https://equipment.usapickleball.org/paddle-list/"
COMPLIANCE_URL = "https://equipment.usapickleball.org/compliance/"
FAQ_URL = "https://equipment.usapickleball.org/equipment-submission-faq/"
USER_AGENT = "PickleballCosmos-PaddleWatch/1.0 (+https://www.pickleballcosmos.com/gear/paddle-approval-watch/)"
SCHEMA_VERSION = "1.0"


class PaddleWatchError(RuntimeError):
    pass


class TextCollector(HTMLParser):
    """Minimal standard-library HTML-to-text collector for public source pages."""

    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_data(self, data: str) -> None:
        value = norm(data)
        if value:
            self.values.append(value)


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def key_text(value: str) -> str:
    return unicodedata.normalize("NFKC", norm(value)).casefold()


def parse_us_date(value: str) -> str:
    try:
        return datetime.strptime(norm(value), "%m/%d/%Y").date().isoformat()
    except ValueError as exc:
        raise PaddleWatchError(f"Unparseable USA Pickleball date: {value!r}") from exc


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso_z(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stamp(dt: datetime) -> str:
    return dt.strftime("%Y%m%d-%H%M%SZ")


def fetch_html(url: str, attempts: int = 3, timeout: int = 35) -> dict[str, Any]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=timeout) as response:  # nosec B310: public URLs are constants above
                body = response.read()
                status = response.status
                charset = response.headers.get_content_charset() or "utf-8"
            html = body.decode(charset, errors="replace")
            if len(html) < 1000:
                raise PaddleWatchError(f"Suspiciously short response from {url}")
            return {
                "url": url,
                "html": html,
                "http_status": status,
                "sha256_html": hashlib.sha256(body).hexdigest(),
            }
        except Exception as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    raise PaddleWatchError(f"Failed to fetch {url}: {last_error}")


def text_lines(html: str) -> list[str]:
    parser = TextCollector()
    parser.feed(html)
    return parser.values


def display_counts(html: str) -> tuple[int, int, int]:
    text = " ".join(text_lines(html))
    match = re.search(r"Displaying\s+([\d,]+)\s*-\s*([\d,]+)\s+of\s+([\d,]+)", text, flags=re.I)
    if not match:
        raise PaddleWatchError("Could not find 'Displaying X - Y of Z' on source page")
    return tuple(int(v.replace(",", "")) for v in match.groups())


def next_index(lines: list[str], start: int, predicate, max_ahead: int = 12) -> int:
    for i in range(start, min(len(lines), start + max_ahead)):
        if predicate(lines[i]):
            return i
    return -1


def first_data_index(lines: list[str]) -> int:
    for i, line in enumerate(lines):
        if re.search(r"Displaying\s+\d+\s*-\s*\d+\s+of", line, re.I):
            return i
    return next((i for i, line in enumerate(lines) if line == "Brand"), 0)


def parse_approved_list(html: str) -> dict[str, Any]:
    start_num, end_num, total = display_counts(html)
    expected = end_num - start_num + 1
    lines = text_lines(html)
    rows: list[dict[str, str]] = []
    i = first_data_index(lines)

    while i < len(lines) and len(rows) < expected:
        if lines[i] != "Brand" or i + 1 >= len(lines):
            i += 1
            continue
        brand = lines[i + 1]
        model_i = next_index(lines, i + 2, lambda x: x.startswith("Model"))
        if model_i < 0 or model_i + 1 >= len(lines):
            i += 1
            continue
        added_i = next_index(lines, model_i + 2, lambda x: x == "Added")
        if added_i < 0 or added_i + 1 >= len(lines):
            i += 1
            continue
        try:
            added_date = parse_us_date(lines[added_i + 1])
        except PaddleWatchError:
            i += 1
            continue
        rows.append({
            "manufacturer": norm(brand),
            "model": norm(lines[model_i + 1]),
            "added_date": added_date,
        })
        i = added_i + 2

    if len(rows) != expected:
        raise PaddleWatchError(
            f"Approved-list parser expected {expected} rows but parsed {len(rows)}; source layout may have changed"
        )

    dates = [row["added_date"] for row in rows]
    if dates != sorted(dates, reverse=True):
        raise PaddleWatchError("Approved list is no longer newest-first; refusing to create a false change report")

    keys = {(key_text(r["manufacturer"]), key_text(r["model"]), r["added_date"]) for r in rows}
    if len(keys) != len(rows):
        raise PaddleWatchError("Duplicate approval rows detected")

    return {
        "display_start": start_num,
        "display_end": end_num,
        "approved_list_total": total,
        "recent_approvals": rows,
    }


def parse_compliance_report(html: str) -> dict[str, Any]:
    start_num, end_num, total = display_counts(html)
    expected = end_num - start_num + 1
    lines = text_lines(html)
    rows: list[dict[str, str]] = []
    i = first_data_index(lines)

    while i < len(lines) and len(rows) < expected:
        if lines[i] != "Brand" or i + 1 >= len(lines):
            i += 1
            continue
        report_i = next_index(lines, i + 2, lambda x: x == "Report Date")
        models_i = next_index(lines, report_i + 2 if report_i >= 0 else i + 2, lambda x: x == "Model(s)")
        status_i = next_index(lines, models_i + 2 if models_i >= 0 else i + 2, lambda x: x == "Compliance Issue or Status")
        if min(report_i, models_i, status_i) < 0:
            i += 1
            continue
        if max(report_i + 1, models_i + 1, status_i + 1) >= len(lines):
            break
        rows.append({
            "brand": norm(lines[i + 1]),
            "models": norm(lines[models_i + 1]),
            "report_date": parse_us_date(lines[report_i + 1]),
            "status": norm(lines[status_i + 1]),
        })
        i = status_i + 2

    if len(rows) != expected:
        raise PaddleWatchError(
            f"Compliance parser expected {expected} rows but parsed {len(rows)}; source layout may have changed"
        )

    keys = {(key_text(r["brand"]), key_text(r["models"])) for r in rows}
    if len(keys) != len(rows):
        raise PaddleWatchError("Duplicate compliance records detected")

    return {
        "display_start": start_num,
        "display_end": end_num,
        "compliance_total": total,
        "compliance_board": rows,
    }


def collect() -> dict[str, Any]:
    observed = now_utc()
    approved_doc = fetch_html(APPROVED_URL)
    compliance_doc = fetch_html(COMPLIANCE_URL)
    approved = parse_approved_list(approved_doc["html"])
    compliance = parse_compliance_report(compliance_doc["html"])

    return {
        "schema_version": SCHEMA_VERSION,
        "observation_id": f"PC-PADDLE-WATCH-{stamp(observed)}",
        "observed_at_utc": iso_z(observed),
        "publisher": "Pickleball Cosmos Editorial",
        "scope": "Newest visible USA Pickleball approval page plus the complete public Paddle Compliance Report; not a full database mirror.",
        "source_of_record": {
            "approved_paddle_list": APPROVED_URL,
            "compliance_report": COMPLIANCE_URL,
            "equipment_faq": FAQ_URL,
        },
        "source_evidence": {
            "approved_paddle_list": {
                "url": APPROVED_URL,
                "http_status": approved_doc["http_status"],
                "sha256_html": approved_doc["sha256_html"],
            },
            "compliance_report": {
                "url": COMPLIANCE_URL,
                "http_status": compliance_doc["http_status"],
                "sha256_html": compliance_doc["sha256_html"],
            },
        },
        "approved_list": approved,
        "compliance_report": compliance,
        "editorial_guardrails": [
            "USA Pickleball's live database remains the source of record for sanctioned-play eligibility.",
            "Rows leaving the recent-approval window are not removals or decertifications.",
            "A compliance record disappearing from the board is not automatically resolved.",
            "Under Investigation is not equivalent to Removed from USAP Approved List.",
            "Approval is a compliance status, not a Pickleball Cosmos performance test or endorsement.",
            "The monitor detects changes; editorial conclusions require verification before publication.",
        ],
    }


def approval_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (key_text(row.get("manufacturer", "")), key_text(row.get("model", "")), row.get("added_date", ""))


def compliance_key(row: dict[str, Any]) -> tuple[str, str]:
    return (key_text(row.get("brand", "")), key_text(row.get("models", "")))


def diff_observations(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    prev_a = {approval_key(r): r for r in previous.get("approved_list", {}).get("recent_approvals", [])}
    curr_a = {approval_key(r): r for r in current.get("approved_list", {}).get("recent_approvals", [])}
    new_rows = [curr_a[k] for k in curr_a.keys() - prev_a.keys()]
    rolled_off = [prev_a[k] for k in prev_a.keys() - curr_a.keys()]
    new_rows.sort(key=lambda r: (r["added_date"], key_text(r["manufacturer"]), key_text(r["model"])), reverse=True)
    rolled_off.sort(key=lambda r: (r["added_date"], key_text(r["manufacturer"]), key_text(r["model"])), reverse=True)

    prev_c = {compliance_key(r): r for r in previous.get("compliance_report", {}).get("compliance_board", [])}
    curr_c = {compliance_key(r): r for r in current.get("compliance_report", {}).get("compliance_board", [])}
    compliance_added = [curr_c[k] for k in curr_c.keys() - prev_c.keys()]
    compliance_no_longer_listed = [prev_c[k] for k in prev_c.keys() - curr_c.keys()]
    status_changes = []
    for key in curr_c.keys() & prev_c.keys():
        before, after = prev_c[key], curr_c[key]
        if before.get("status") != after.get("status") or before.get("report_date") != after.get("report_date"):
            status_changes.append({"before": before, "after": after})

    before_total = previous.get("approved_list", {}).get("approved_list_total")
    after_total = current.get("approved_list", {}).get("approved_list_total")
    total_delta = after_total - before_total if isinstance(before_total, int) and isinstance(after_total, int) else None

    changed = any([
        new_rows,
        rolled_off,
        compliance_added,
        compliance_no_longer_listed,
        status_changes,
        total_delta not in (None, 0),
    ])

    return {
        "schema_version": SCHEMA_VERSION,
        "previous_observation_id": previous.get("observation_id"),
        "current_observation_id": current.get("observation_id"),
        "detected_at_utc": current.get("observed_at_utc"),
        "has_substantive_change": bool(changed),
        "new_rows_in_recent_approval_window": new_rows,
        "rows_rolled_off_recent_approval_window": rolled_off,
        "approved_list_total_before": before_total,
        "approved_list_total_after": after_total,
        "approved_list_total_delta": total_delta,
        "compliance_records_added": compliance_added,
        "compliance_records_no_longer_listed": compliance_no_longer_listed,
        "compliance_record_status_or_date_changes": status_changes,
        "interpretation_guardrails": [
            "A recent approval row rolling off the first page is not evidence of decertification.",
            "A decrease in the total approved-list count does not identify which model changed status.",
            "A compliance record no longer appearing is not automatically classified as resolved.",
            "Only USA Pickleball's published status wording is carried into editorial review.",
        ],
    }


def render_change(change: dict[str, Any]) -> str:
    delta = change.get("approved_list_total_delta")
    total_line = f"- Approved-list total: `{change.get('approved_list_total_before')}` → `{change.get('approved_list_total_after')}`"
    if isinstance(delta, int):
        total_line += f" ({delta:+d})"
    lines = [
        "# Paddle Approval Watch — detected source change",
        "",
        f"- Previous observation: `{change.get('previous_observation_id')}`",
        f"- Current observation: `{change.get('current_observation_id')}`",
        f"- Detected: `{change.get('detected_at_utc')}`",
        total_line,
        "",
        "## New rows in monitored recent-approval window",
    ]
    rows = change.get("new_rows_in_recent_approval_window", [])
    lines += [f"- {r['added_date']} — **{r['manufacturer']}** — {r['model']}" for r in rows] or ["- None"]
    lines += ["", "## Compliance records added"]
    rows = change.get("compliance_records_added", [])
    lines += [f"- {r['report_date']} — **{r['brand']}** — {r['models']} — `{r['status']}`" for r in rows] or ["- None"]
    lines += ["", "## Compliance status/date changes"]
    rows = change.get("compliance_record_status_or_date_changes", [])
    if rows:
        for item in rows:
            before, after = item["before"], item["after"]
            lines.append(f"- **{after['brand']} — {after['models']}**: `{before['status']}` ({before['report_date']}) → `{after['status']}` ({after['report_date']})")
    else:
        lines.append("- None")
    lines += ["", "## Compliance records no longer listed on the public board"]
    rows = change.get("compliance_records_no_longer_listed", [])
    lines += [f"- **{r['brand']}** — {r['models']} — previously `{r['status']}`" for r in rows] or ["- None"]
    lines += [
        "",
        "## Editorial warning",
        "",
        "This is a machine-generated detection report, not a published conclusion. A recent-approval row leaving the monitored first page is not a decertification. A compliance record disappearing is not automatically a resolution. Verify material changes against USA Pickleball before updating the public tracker.",
        "",
    ]
    return "\n".join(lines)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def set_output(name: str, value: str) -> None:
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with open(output, "a", encoding="utf-8") as handle:
            handle.write(f"{name}={value}\n")


def monitor(repo_root: Path) -> int:
    base = repo_root / "research" / "paddle-watch"
    latest = base / "latest-observation.json"
    current = collect()
    previous = load_json(latest) if latest.exists() else None

    if previous is None:
        changed = True
        change = None
    else:
        change = diff_observations(previous, current)
        changed = change["has_substantive_change"]

    set_output("changed", "true" if changed else "false")
    print(f"PADDLE_WATCH_CHANGED={'true' if changed else 'false'}")
    if not changed:
        print("No substantive source change. No research files written.")
        return 0

    current_stamp = current["observation_id"].replace("PC-PADDLE-WATCH-", "")
    write_json(base / "observations" / f"{current_stamp}.json", current)
    write_json(latest, current)

    if change is not None:
        write_json(base / "changes" / f"{current_stamp}.json", change)
        (base / "changes" / f"{current_stamp}.md").write_text(render_change(change), encoding="utf-8")
        write_json(base / "latest-change.json", change)
        (base / "latest-change.md").write_text(render_change(change), encoding="utf-8")
        print(f"New approval-window rows: {len(change['new_rows_in_recent_approval_window'])}")
        print(f"Compliance records added: {len(change['compliance_records_added'])}")
        print(f"Compliance status/date changes: {len(change['compliance_record_status_or_date_changes'])}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Pickleball Cosmos Paddle Approval Watch")
    parser.add_argument("command", choices=["monitor"])
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    try:
        return monitor(Path(args.repo_root).resolve())
    except PaddleWatchError as exc:
        print(f"PADDLE WATCH ERROR: {exc}", file=sys.stderr)
        set_output("changed", "false")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
