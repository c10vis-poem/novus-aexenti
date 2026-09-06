# Cross-Auditor

**Slug:** `cross-auditor` · **Role:** home-node public auditor · **Tier:** auditor

## What problem this solves

Script collector + log aggregator. Runs OVER combined traces from both harnesses. Public counterpart to the red auditor.

## Binding

| Field | Value |
|---|---|
| Model | GLM-5.2 or on-device 9B |
| Node | Beta |
| Memory scope | Strategic |
| Tool allowance | read all trajectories, write audit verdicts |
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
