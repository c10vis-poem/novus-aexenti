# NovÆxenti

**Agent logic.** Personas, harness bindings, agent manifests.

Repo: `novus-aexenti` (hyphenated, `novus-` prefix — see `NAMING-CANON.md` in
`novae-xorpus`, operator correction 2026-09-06).

## What lives here vs elsewhere

| This repo | Elsewhere |
|---|---|
| **Who** an agent is — persona, scope, memory access, tool allowance | **What** it runs on → `novaexopia` (runtimes, engines, weights) |
| Harness *bindings* — which agent runs under which harness | Harness *specs* → `novae-xorpus/data_vault/02_wiki_md/harnesses/` |
| Agent manifests (machine-readable) | Protocols → `aesop-xi` |

An **agent** is a specific persona running *under* a harness. It is not a model
and not a harness. See the terminology glossary in
`novae-xorpus/canon/DECISIONS-LOCKED.md` — one meaning per term, no exceptions.

## Layout

```
agents/                 one folder per persona
  <name>/
    AGENT.md            the persona spec (human-readable)
    manifest.json       machine-readable binding
harnesses/              which agents run under which harness
modes/                  the 4 operating modes
manifest.jsonl          all agents, one line each — queried, never loaded whole
```

## The 4 operating modes

Not 2. Modes are about **who holds the control loop**, not which model answers.

| Mode | Control loop | Models | When |
|---|---|---|---|
| **Dev-Terminal** | ECC only | Frontier (Claude) | Operator at a terminal, building. |
| **Sovereign-Edge** | Prime Agent only | On-device weights only | No network. Full autonomy on Alpha. |
| **Prime-with-Claude-as-Query** | Prime Agent | On-device + Claude as a *subprocess* | Prime holds the loop; escalates hard sub-questions to Claude and keeps going. |
| **Hybrid-Auditor** | Cross-auditor over both | Combined traces | Post-hoc. Audits trajectories from both harnesses together. |

## Beginner-Proof Standard

Every agent spec states: the problem it solves, its data flow, and its failure
mode. If a beginner dev or a third-rate model can't pick it up and resume the
work, the spec is broken and gets rewritten — not annotated.
