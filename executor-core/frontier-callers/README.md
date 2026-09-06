# Frontier callers

Personas permitted to call frontier APIs. **Permission gated** — a frontier call
is a cost event and a data-egress event, both of which get logged.

| Caller | Vendor | Model | Used for | Permission |
|---|---|---|---|---|
| `claude-caller` | Claude (Anthropic) | `claude-opus-5 / claude-sonnet-5` | Code, review, long-context synthesis | high |
| `glm-caller` | GLM (Z-AI via OpenRouter) | `glm-5.2` | Bulk file admin, 1M context sweeps, cheap auditing | medium |
| `gemini-caller` | Gemini (Google) | `gemini via AI Studio / Spark` | Multimodal, NotebookLM-adjacent analysis | medium |
| `fable-caller` | Fable (Anthropic) | `claude-fable-5-1` | Narrative/long-form generation | low |
| `opus-caller` | Opus (Anthropic) | `claude-opus-5` | Hardest reasoning, architecture calls | high |

## Rules

1. Every frontier call is logged: model, token count, cost estimate, calling agent.
2. Escalation order is on-device -> cheap cloud (GLM) -> frontier. Never skip straight to frontier for something the 9B can answer.
3. Cost checking runs against these logs — see `protocols/cost-checking`.
4. No frontier caller gets vault *write* access. They return text; an on-device agent decides what to persist.
