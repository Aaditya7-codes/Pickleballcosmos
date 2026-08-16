#!/usr/bin/env python3
"""Reduce formulaic micro-headings in the site’s highest-traffic explainers.

This is intentionally a curated map, not a blanket heading conversion: each
umbrella heading represents a real editorial section and the demoted headings
remain useful wayfinding within it.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGES = {
    "gear/how-to-choose-first-pickleball-paddle/index.html": [
        ("<h2>Step 1: make sure the exact paddle is legal for the play you care about</h2>", "<h2>Start with legality and fit</h2><h3>Make sure the exact paddle is legal for the play you care about</h3>"),
        ("<h2>Step 2: do not start with “power vs control”</h2>", "<h3>Do not start with “power vs control”</h3>"),
        ("<h2>Step 3: choose shape before chasing materials</h2>", "<h3>Choose shape before chasing materials</h3>"),
        ("<h2>Step 4: understand static weight, swing weight and twist weight</h2>", "<h3>Understand static weight, swing weight and twist weight</h3>"),
        ("<h2>What weight should a beginner buy?</h2>", "<h3>What weight should a beginner buy?</h3>"),
        ("<h2>Step 5: treat 14mm vs 16mm as a secondary choice</h2>", "<h2>Use construction labels as context, not verdicts</h2><h3>Treat 14mm vs 16mm as a secondary choice</h3>"),
        ("<h2>Step 6: do not buy a material word</h2>", "<h3>Do not buy a material word</h3>"),
        ("<h2>Step 7: check the grip and handle</h2>", "<h3>Check the grip and handle</h3>"),
        ("<h2>Step 8: pay for evidence, not adjectives</h2>", "<h2>Finish with evidence, price and terms</h2><h3>Pay for evidence, not adjectives</h3>"),
        ("<h2>Step 9: read the warranty before you need it</h2>", "<h3>Read the warranty before you need it</h3>"),
        ("<h2>What should a beginner avoid?</h2>", "<h3>What should a beginner avoid?</h3>"),
        ("<h2>How much should you spend?</h2>", "<h3>How much should you spend?</h3>"),
    ],
    "gear/pickleball-paddle-warranties/index.html": [
        ("<h2>Selkirk: strong headline, but check which Selkirk line you are buying</h2>", "<h2>Where the policies materially differ</h2><h3>Selkirk: strong headline, but check which Selkirk line you are buying</h3>"),
        ("<h2>JOOLA: six months is the default; 12 months requires the extension conditions</h2>", "<h3>JOOLA: six months is the default; 12 months requires the extension conditions</h3>"),
        ("<h2>CRBN: one year, with retailer-registration and ownership requirements</h2>", "<h3>CRBN: one year, with retailer-registration and ownership requirements</h3>"),
        ("<h2>Six Zero: one of the clearest structural policies</h2>", "<h3>Six Zero: one of the clearest structural policies</h3>"),
        ("<h2>Vatic Pro: straightforward one-year manufacturing-defect warranty</h2>", "<h3>Vatic Pro: straightforward one-year manufacturing-defect warranty</h3>"),
        ("<h2>Paddletek: lifetime performance guarantee, but registration matters</h2>", "<h3>Paddletek: lifetime performance guarantee, but registration matters</h3>"),
        ("<h2>Engage: lifetime defect coverage with a 30-day registration rule</h2>", "<h3>Engage: lifetime defect coverage with a 30-day registration rule</h3>"),
        ("<h2>Gearbox: one year generally, with named six-month exceptions</h2>", "<h3>Gearbox: one year generally, with named six-month exceptions</h3>"),
        ("<h2>Franklin: the exact model matters more than the brand name</h2>", "<h3>Franklin: the exact model matters more than the brand name</h3>"),
    ],
    "learn/pickleball-serving-rules/index.html": [
        ("<h2>1. Start in the correct serving area</h2>", "<h2>How to make a legal serve</h2><h3>Start in the correct serving area</h3>"),
        ("<h2>2. The release cannot be used to pre-spin the ball</h2>", "<h3>The release cannot be used to pre-spin the ball</h3>"),
        ("<h2>3. A volley serve has three contact requirements</h2>", "<h3>A volley serve has three contact requirements</h3>"),
        ("<h2>4. The drop serve follows a different motion rule</h2>", "<h3>The drop serve follows a different motion rule</h3>"),
        ("<h2>5. The serve must go diagonally into the correct service court</h2>", "<h3>The serve must go diagonally into the correct service court</h3>"),
        ("<h2>6. A serve may touch the net and still be legal</h2>", "<h3>A serve may touch the net and still be legal</h3>"),
        ("<h2>7. There is no tennis-style second serve</h2>", "<h3>There is no tennis-style second serve</h3>"),
        ("<h2>Where do you serve from?</h2>", "<h3>Where do you serve from?</h3>"),
    ],
    "learn/pickleball-kitchen-rules/index.html": [
        ("<h2>1. Yes, you can step into the kitchen</h2>", "<h2>What you may do in and around the kitchen</h2><h3>Yes, you can step into the kitchen</h3>"),
        ("<h2>2. The kitchen line counts as part of the kitchen</h2>", "<h3>The kitchen line counts as part of the kitchen</h3>"),
        ("<h2>3. Momentum is part of the volley</h2>", "<h3>Momentum is part of the volley</h3>"),
        ("<h2>4. Your partner can become part of a kitchen fault</h2>", "<h3>Your partner can become part of a kitchen fault</h3>"),
        ("<h2>5. You must re-establish completely outside before volleying again</h2>", "<h3>You must re-establish completely outside before volleying again</h3>"),
        ("<h2>6. You can reach over the kitchen line</h2>", "<h3>You can reach over the kitchen line</h3>"),
        ("<h2>7. What if something you are wearing or carrying touches the kitchen?</h2>", "<h3>What if something you are wearing or carrying touches the kitchen?</h3>"),
        ("<h2>8. The serve has a separate kitchen-line rule</h2>", "<h3>The serve has a separate kitchen-line rule</h3>"),
    ],
    "learn/pickleball-scoring/index.html": [
        ("<h2>Doubles scores have three numbers</h2>", "<h2>How traditional doubles scoring works</h2><h3>Doubles scores have three numbers</h3>"),
        ("<h2>Why does doubles start at 0–0–2?</h2>", "<h3>Why does doubles start at 0–0–2?</h3>"),
        ("<h2>Server 1 and server 2 are not permanent identities</h2>", "<h3>Server 1 and server 2 are not permanent identities</h3>"),
        ("<h2>How a normal doubles service turn works</h2>", "<h3>How a normal doubles service turn works</h3>"),
        ("<h2>The serving team switches sides only when it scores</h2>", "<h3>The serving team switches sides only when it scores</h3>"),
        ("<h2>A full doubles example</h2>", "<h3>A full doubles example</h3>"),
        ("<h2>How many points do you play to?</h2>", "<h3>How many points do you play to?</h3>"),
    ],
    "learn/pickleball-two-bounce-rule/index.html": [
        ("<h2>Does the return of serve have to bounce in a particular area?</h2>", "<h2>Edge cases that change the call</h2><h3>Does the return of serve have to bounce in a particular area?</h3>"),
        ("<h2>Can the third shot bounce too?</h2>", "<h3>Can the third shot bounce too?</h3>"),
        ("<h2>What if the first or second required ball is going out?</h2>", "<h3>What if the first or second required ball is going out?</h3>"),
        ("<h2>Is it the two-bounce rule or double-bounce rule?</h2>", "<h3>Is it the two-bounce rule or double-bounce rule?</h3>"),
    ],
    "stories/history-of-pickleball/index.html": [
        ("<h2>1965: the game begins on Bainbridge Island</h2>", "<h2>Before the boom: a game becomes a national sport</h2><h3>1965: the game begins on Bainbridge Island</h3>"),
        ("<h2>Where did the name “pickleball” come from?</h2>", "<h3>Where did the name “pickleball” come from?</h3>"),
        ("<h2>1967: the first permanent pickleball court</h2>", "<h3>1967: the first permanent pickleball court</h3>"),
        ("<h2>1976: the first known tournament</h2>", "<h3>1976: the first known tournament</h3>"),
        ("<h2>1984: national organization and the first rulebook</h2>", "<h3>1984: national organization and the first rulebook</h3>"),
        ("<h2>1990: played in all 50 states</h2>", "<h3>1990: played in all 50 states</h3>"),
        ("<h2>1990s–2000s: infrastructure before the explosion</h2>", "<h3>1990s–2000s: infrastructure before the explosion</h3>"),
        ("<h2>2015: pickleball passes two million U.S. participants</h2>", "<h3>2015: pickleball passes two million U.S. participants</h3>"),
        ("<h2>2020: 4.2 million players — and the curve changes</h2>", "<h2>The boom inherited an older system</h2><h3>2020: 4.2 million players — and the curve changes</h3>"),
        ("<h2>The professional game becomes a real ecosystem</h2>", "<h3>The professional game becomes a real ecosystem</h3>"),
        ("<h2>2025: 82,613 known courts and more than 100,000 USA Pickleball members</h2>", "<h3>2025: 82,613 known courts and more than 100,000 USA Pickleball members</h3>"),
        ("<h2>2026: the sport is dealing with mature-sport problems</h2>", "<h3>2026: the sport is dealing with mature-sport problems</h3>"),
    ],
}

for relative, changes in CHANGES.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for old, new in changes:
        if old in text:
            text = text.replace(old, new, 1)
        elif new not in text:
            raise SystemExit(f"Missing expected heading in {relative}: {old}")
    path.write_text(text, encoding="utf-8")

history = ROOT / "stories/history-of-pickleball/index.html"
text = history.read_text(encoding="utf-8")
old = "The interesting story is everything that happened between those two points."
new = "What made that change possible was not a sudden invention, but decades of rules, local organizers, dedicated courts and institutions."
if old in text:
    history.write_text(text.replace(old, new, 1), encoding="utf-8")
elif new not in text:
    raise SystemExit("Missing history dek sentence")

EXTRA_GROUPS = {
    "gear/pickleball-paddle-break-in/index.html": [
        ("What does “break-in” mean?", "What break-in is—and what it is not", ["There is no universal break-in time", "What can actually change?", "The important distinction: break-in is not core crushing"]),
        ("Why governing bodies suddenly care so much about break-in", "When change becomes a compliance question", ["UPA-A's accelerated break-in test is not “months of normal play in a machine”", "When does break-in become a problem?", "Can break-in make a legal paddle illegal?"]),
        ("Do full-foam and honeycomb paddles break in differently?", "What a player can do with limited evidence", ["Should you try to accelerate the break-in yourself?", "How to evaluate your own paddle without pretending to run a lab"]),
    ],
    "gear/pickleball-paddle-twist-weight/index.html": [
        ("Why off-center hits twist the paddle", "What twist weight measures", ["Why mass distribution matters more than total weight alone", "Wider paddles often have a structural advantage — but width is not destiny", "What the sports-engineering evidence actually supports"]),
        ("Does higher twist weight mean a bigger sweet spot?", "What the number can—and cannot—tell you", ["Does higher twist weight mean more power?", "Twist weight vs swing weight", "What happens when you add weight at 3 and 9 o'clock?"]),
        ("Can you compare twist-weight numbers from different websites?", "How to use it in a buying decision", ["What should buyers do with twist weight?", "There is no universal “good twist weight”"]),
    ],
    "learn/how-to-play-pickleball/index.html": [
        ("1. Know the court", "Set up the first rally", ["2. Decide who serves first", "3. Serve diagonally", "4. Let the first two shots bounce", "5. After that, the rally is open", "6. Understand the kitchen before you rush the net", "7. Learn the scoring system"]),
        ("8. Singles and doubles use the same court", "Play your first points", ["9. Where should a beginner stand?", "10. What shots do you actually need?"]),
    ],
    "learn/pickleball-line-rules/index.html": [
        ("1. A ball touching a line is normally in", "How line calls work", ["2. The kitchen line is different on the serve", "3. The kitchen line is part of the kitchen"]),
        ("4. Who makes the line call?", "Who decides a close call", ["5. An out call requires certainty", "6. What happens when doubles partners disagree?", "7. Can you overrule your partner?", "8. Can spectators help with a line call?", "9. What changes in an officiated tournament?"]),
    ],
}

for relative, groups in EXTRA_GROUPS.items():
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for anchor, section, children in groups:
        old_anchor = f"<h2>{anchor}</h2>"
        new_anchor = f"<h2>{section}</h2><h3>{anchor}</h3>"
        if old_anchor in text:
            text = text.replace(old_anchor, new_anchor, 1)
        elif new_anchor not in text:
            raise SystemExit(f"Missing expected heading in {relative}: {anchor}")
        for child in children:
            old_child = f"<h2>{child}</h2>"
            new_child = f"<h3>{child}</h3>"
            if old_child in text:
                text = text.replace(old_child, new_child, 1)
            elif new_child not in text:
                raise SystemExit(f"Missing expected heading in {relative}: {child}")
    path.write_text(text, encoding="utf-8")

swing = ROOT / "gear/pickleball-paddle-swing-weight/index.html"
text = swing.read_text(encoding="utf-8")
text = text.replace("present them as one seamless dataset", "present them as though they were directly comparable")
swing.write_text(text, encoding="utf-8")
