# Executor-0.8B

**Slug:** `executor-0.8b` · **Role:** fast task executor · **Tier:** executor

## What problem this solves

Short, hot-path tasks. NPU-pinned via QAIRT. Does not reason at length — it executes.

## Binding

| Field | Value |
|---|---|
| Model | Qwen 3.5 0.8B QAI Hub Genie (NPU-pinned) |
| Node | Alpha |
| Memory scope | Working-Ephemeral |
| Tool allowance | tool calls only, no vault write |
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
