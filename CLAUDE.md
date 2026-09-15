# NovÆxenti — agent logic layer

Canon name: **NovÆxenti**. Repo name: `novus-aexenti`. See `novae-xorpus/NAMING-CANON.md`.

## What this is

The agent intelligence layer of the Æsop-Xi stack. Houses executor-core (task
execution agents, mode definitions) and query-core (meta-prompt compilation,
intent classification). This is the "brain" — Æsop-Xi is the infrastructure it
runs on, NovÆxopia is the action surface it drives.

## Stack position

```
Æsop-Xi          infrastructure (MCPs, hooks, memory, routing, protocols)
  └─ NovÆxenti   agent logic (this repo) — executor + query cores
       └─ NovÆxopia   tools, harness, engine — what the agent can do
            ├─ Æsc         terminal daemon
            └─ Æyre        voice / vision daemon
```

NovÆxorpus (novae-xorpus) is the data bank — orthogonal to this stack, feeds
all layers.

## Conventions

- `executor-core/` — small-model task execution agents (0.8B executor,
  file-administrator, NPU inference manager, frontier callers).
- `query-core/` — large-model query/reasoning agents (9B query, oeracle,
  IT helpdesk).
- `node-beta-swarm/` — Node Beta home-node agents (cross-auditor,
  home-assistant, red-auditor, trend-scraper, web-ingestion).
- Harness configs in `harnesses/` define how an agent runtime is invoked.
- Mode definitions in `modes/` describe behavioral presets.
- `manifest.jsonl` is the machine-readable index — regenerate, don't hand-edit.

## Operator Rule 1 — no action without an explicit prompt

A skipped or unanswered question is NOT consent. No action — reading,
searching, or anything else — without an explicit prompt or permitted
request. State-changing or not, it doesn't matter.

## Operator Rule 2 — read this file and RESUME.md first

Before doing anything else in this repo, read this CLAUDE.md and RESUME.md.
Standing convention across the operator's repos for months — step one,
every session, no exceptions.

## Git workflow — push directly to main

Push directly to `main`. No feature branches, no PRs — operator directive
2026-09-15, superseding the previous branch/PR-required convention (that
workflow left work stranded on unmerged branches across sessions and
devices instead of ever reaching a shared, cloneable state). Before every
push, scan the diff for secrets/keys and refuse to push if any are found.
