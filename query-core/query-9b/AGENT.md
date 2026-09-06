# Query-9B

**Slug:** `query-9b` · **Role:** meta-prompt compiler · **Tier:** query

## What problem this solves

Compiles meta-prompts, decides escalation, calls cloud tools. The thinking half of the executor/query tandem.

## Binding

| Field | Value |
|---|---|
| Model | Qwen 3.5 9B Q4_0 GGUF (GenieX) |
| Node | Alpha |
| Memory scope | Recall + Declarative |
| Tool allowance | vault read, cloud tool calls |
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
