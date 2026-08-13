# Pickleball Cosmos Paddle Approval Watch — monitoring protocol

This directory is the evidence layer behind the public Paddle Approval Watch.

## Source of record

USA Pickleball remains the source of record for USA Pickleball-sanctioned paddle eligibility. The monitor observes:

- `https://equipment.usapickleball.org/paddle-list/` — the newest visible page of approved paddles and the total approved-list count.
- `https://equipment.usapickleball.org/compliance/` — the complete public Paddle Compliance Report.

The monitor does **not** mirror the full approved-equipment database.

## What is automated

A scheduled GitHub Action fetches the two public source pages, validates their visible structure, normalizes the records, compares them with the previous observation, and writes a new observation only when a material source change is detected.

Each automated observation records:

- UTC observation time;
- source URLs;
- HTTP status;
- SHA-256 hash of each fetched HTML response;
- total approved-list count;
- the complete newest visible approval page;
- the complete public compliance board.

The parser deliberately fails if the approval page stops being newest-first, if the expected number of visible rows cannot be parsed, or if duplicate records appear. A source-layout change should produce a failed monitor, not a misleading news item.

## What is not automated

The monitor does **not** automatically update the public article or publish editorial conclusions. Detection and publication are separate layers.

In particular:

- A paddle leaving the recent first-page approval window is **not** treated as removed or decertified.
- A decrease in the total approved-list count does not identify which model changed status.
- A compliance record disappearing from the compliance board is **not** automatically treated as resolved.
- `Under Investigation` remains `Under Investigation`; it is not rewritten as `banned`, `illegal`, or `removed`.
- Approval status is not a performance review, endorsement, durability finding, or Pickleball Cosmos test result.

Material changes should be checked against USA Pickleball before the public Paddle Approval Watch is updated.

## Files

- `latest-observation.json` — most recent preserved normalized observation.
- `observations/` — immutable dated observations created only when the monitored source state changes.
- `latest-change.json` / `latest-change.md` — most recent machine-generated comparison.
- `changes/` — dated machine-generated comparisons.

The original launch baseline remains at `research/usap-paddle-watch-baseline-2026-08-13.json` for provenance.

## Cadence

The monitor runs daily and can also be run manually through GitHub Actions. Daily monitoring is sufficient for editorial detection while avoiding needless requests to the governing-body site.

## Editorial principle

The system is built to preserve **status, date, provenance, and uncertainty**. It is intentionally conservative: a missed headline is preferable to a false claim that a paddle was banned or decertified.
