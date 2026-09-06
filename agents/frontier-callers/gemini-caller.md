# gemini-caller

**Vendor:** Gemini (Google) · **Model:** `gemini via AI Studio / Spark` · **Permission tier:** medium

## Used for

Multimodal, NotebookLM-adjacent analysis

## Not used for

Anything an on-device model can answer. Escalation is on-device -> GLM -> frontier.

## Logged on every call

`{caller_agent, model, prompt_tokens, completion_tokens, cost_estimate_usd, timestamp}`
-> `05_episodic_logs/` and the cost-checking ledger.

## Write access

**None.** Returns text only. An on-device agent decides what gets persisted.
