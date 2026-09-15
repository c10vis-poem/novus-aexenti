# NovÆxenti — agent logic layer

Canon name: **NovÆxenti**. Repo name: `novus-aexenti`. See `NovAExorpus/NAMING-CANON.md`.

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

NovÆxorpus (NovAExorpus) is the data bank — orthogonal to this stack, feeds
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

## Git workflow

PR required. No direct pushes to main. CI runs gitleaks + structure check.
Before every push, scan the diff for secrets/keys and refuse to push if any
are found. On green CI, auto-merge into `main` immediately — do not wait for
a manual merge step. Leave the branch in place after merge; do not delete it.

The point of this workflow is that everything reaches `main` — a branch
that never gets a PR opened, or a PR that never gets merged, is a failure
of this rule, not a valid alternative to it. Don't let work sit stranded.
