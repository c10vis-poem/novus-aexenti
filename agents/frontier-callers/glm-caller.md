# glm-caller

**Vendor:** GLM (Z-AI via OpenRouter) · **Model:** `glm-5.2` · **Permission tier:** medium

## Used for

Bulk file admin, 1M context sweeps, cheap auditing

## Not used for

Anything an on-device model can answer. Escalation is on-device -> GLM -> frontier.

## Logged on every call

`{caller_agent, model, prompt_tokens, completion_tokens, cost_estimate_usd, timestamp}`
-> `05_episodic_logs/` and the cost-checking ledger.

## Write access

**None.** Returns text only. An on-device agent decides what gets persisted.
