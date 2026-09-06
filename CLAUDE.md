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

- Agent manifests live in `agents/` as individual markdown files with YAML
  frontmatter (name, mode, capabilities, model preferences).
- Harness configs in `harnesses/` define how an agent runtime is invoked.
- Mode definitions in `modes/` describe behavioral presets (executor, query,
  auditor, etc.).
- `manifest.jsonl` is the machine-readable index — regenerate, don't hand-edit.

## Git workflow

PR required. No direct pushes to main. CI runs gitleaks + structure check.
