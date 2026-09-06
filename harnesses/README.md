# Harness bindings

Which agent runs under which control loop. The harness **specs** live in
`novae-xorpus/data_vault/02_wiki_md/harnesses/` — this file is only the binding.

| Harness | Agents bound |
|---|---|
| **ECC** (Everything Claude Code) | operator's Claude Code sessions; not a persona binding |
| **Prime Agent** (RLM) | `executor-0.8b`, `query-9b`, `oeracle`, `npu-inference-manager` |
| **DeepSeek** (coming) | TBD — see `novae-xorpus/.../harnesses/deepseek/` |
| **Cross-auditor** (out-of-band) | `cross-auditor`, `home-assistant-auditor` |
| *(isolated)* | `red-auditor` — runs outside every harness in this table |

## Modular hot-swap

A harness is swappable because it touches exactly **4 interfaces**:

1. **Model** — via OmniRoute (`localhost:20128`). Harness never binds a model directly.
2. **Memory** — via MCP servers. Harness never touches the vault filesystem directly.
3. **Tools** — via MCP servers. Same rule.
4. **Output** — trajectories to `05_episodic_logs/`, one schema for all harnesses.

Swap a harness by reimplementing those 4. Nothing else in the stack should notice.
If swapping a harness requires changing anything outside these 4, that's a bug in
the boundary, not a reason to widen it.
