# Web-Ingestion-Monitor

**Slug:** `web-ingestion-monitor` · **Role:** upstream change tracker · **Tier:** monitor

## What problem this solves

Tracks upstream model/tool/repo changes. Fires when a pinned dependency moves.

## Binding

| Field | Value |
|---|---|
| Model | executor-0.8b |
| Node | Alpha |
| Memory scope | Declarative |
| Tool allowance | web fetch, diff, write alerts |
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
