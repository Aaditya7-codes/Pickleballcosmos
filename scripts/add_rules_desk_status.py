#!/usr/bin/env python3
"""Add a scoped, consistent Rules Desk review status to priority rule guides."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "learn/pickleball-serving-rules/index.html": "Section 7 · Serving",
    "learn/pickleball-two-bounce-rule/index.html": "Section 10.A · Two-Bounce Rule",
    "learn/pickleball-kitchen-rules/index.html": "Section 11 · Non-Volley Zone",
    "learn/pickleball-scoring/index.html": "Sections 4–5 · Scoring & service sequence",
    "learn/what-does-0-0-2-mean-pickleball/index.html": "Section 5 · Traditional doubles scoring",
    "learn/can-paddle-cross-net-pickleball/index.html": "Section 13 · Plane of the net",
    "learn/can-pickleball-serve-hit-net/index.html": "Rule 7.E · Serve placement",
    "learn/pickleball-faults/index.html": "Sections 7–13 · Faults by action",
    "learn/pickleball-line-rules/index.html": "Section 8 · Line calls",
    "learn/pickleball-kitchen-momentum-rule/index.html": "Rule 11.A · Volley momentum",
}
STATUS = '<div class="rules-desk-status"><span>Rules Desk</span><strong>Reviewed against the 2026 USA Pickleball Official Rulebook</strong><span>{focus}</span></div>'

for relative, focus in PAGES.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    status = STATUS.format(focus=focus)
    if 'class="rules-desk-status"' not in text:
        text, count = re.subn(r'(<div class="byline">.*?</div>)', r'\1' + status, text, count=1, flags=re.S)
        if count != 1:
            raise SystemExit(f"Could not place review status in {relative}")
    text, count = re.subn(
        r'(<div class="byline">.*?</span><span>).*?(</span></div>)',
        r'\1Reviewed August 16, 2026\2',
        text,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f"Could not update review date in {relative}")
    text = re.sub(r'("dateModified":")\d{4}-\d{2}-\d{2}', r'\g<1>2026-08-16', text)
    path.write_text(text, encoding="utf-8")
