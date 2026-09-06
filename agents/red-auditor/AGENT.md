# Red Auditor

**Slug:** `red-auditor` · **Role:** INCOGNITO adversarial auditor · **Tier:** auditor

## What problem this solves

LINK ONLY. Spec, code and NopeDataBank live OUTSIDE the visible tree. The vault sees only `red_verdict: pass|fail|n/a` on trajectory records. See protocols/incognito-red-audit.

## Binding

| Field | Value |
|---|---|
| Model | undisclosed |
| Node | undisclosed |
| Memory scope | isolated — no vault memory |
| Tool allowance | none in visible tree |
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
