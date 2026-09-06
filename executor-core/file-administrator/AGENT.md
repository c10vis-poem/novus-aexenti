# NovusÆxenti-Housekeeper

**Slug:** `file-administrator` · **Role:** vault file administration · **Tier:** admin

## What problem this solves

Keeps the vault tidy: naming canon enforcement, MAP.md regeneration, manifest.jsonl compaction, dead-link sweeps.

## Binding

| Field | Value |
|---|---|
| Model | GLM-5.2 (cloud, OpenRouter) |
| Node | Delta |
| Memory scope | Declarative + Strategic |
| Tool allowance | full vault write, git |
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
