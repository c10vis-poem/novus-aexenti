# Early-Trend-Scraper

**Slug:** `early-trend-scraper` · **Role:** daily upstream scraper · **Tier:** scraper

## What problem this solves

Daily pass over dev news + GitHub trending. Writes candidates into references/, never into canon.

## Binding

| Field | Value |
|---|---|
| Model | executor-0.8b |
| Node | Alpha |
| Memory scope | Working-Ephemeral |
| Tool allowance | web fetch, write to references/ |
| Harness | see `harnesses/` |

## Data flow

1. Trigger arrives (operator, schedule, or upstream agent).
2. Agent reads `MAP.md` first — non-negotiable, every session, every agent.
3. Retrieval: `manifest.jsonl` query -> targeted leaf notes. Never load a whole tier.
4. Work happens under the harness's control loop.
5. Trajectory written to `05_episodic_logs/` with speaker attribution intact.

## Failure mode

_To be filled from first real run. Do not guess it here._

## Open questions

_Track in `novae-xorpus/unresolved.md`, not inline._
