# novus_aexenti_cognitive_engine.md — Cognitive Reasoning Engine Specification


**Subsystem**: `novus-aexenti` (NovusÆxenti)  
**Corpus Source**: `___Lex-Novi-Æxentis-Copiæ/--• 🦁 NovusÆxenti🌲NovÆcopia🕷️• ~`  
**Target Category**: Clean High-Density Markdown (`clean_md/`)  
**Standard**: Universal 5+1 Cognitive Memory & Subsystem Co-Location Standard  


---


## 1. Subsystem Mission & Invariants


`novus-aexenti` functions as the cognitive Multi-Agent Mixture-of-Experts (MoE) brain for the ecosystem. It decouples low-latency user intent triage from heavy code and reasoning execution to maintain an active on-device RAM footprint below 5.0 GB on Android (Snapdragon 8 Elite / Motorola Razr Ultra 2025).


### Core Invariants
1. **RAM Ceiling Enforcement**: Active edge weights and working memory must never exceed 4,800 MB to prevent Android Low Memory Killer (LMK) eviction.
2. **Zero Raw Chat Flooding**: Raw multi-turn chat context is never fed directly to the 9B model. All prompts are pre-processed by token-compression routines and enriched with condensed episodic habit keys.
3. **Deterministic Triage Gating**: Queries under the 120-token complexity threshold without code markers route exclusively to the on-device 0.8B triage model.
4. **Crash-Resilient State Continuity**: Multi-step agent trajectories must register progress steps in the Reasoning Bank (`active_execution_paths.json`) to guarantee zero-loss recovery across process restarts.


---


## 2. Model Weight Hierarchy & Hardware Allocations


| Model Tier | Model Name | Parameter Scale | Quantization / Format | Memory Footprint | Runtime / Engine | Target Hardware | Context Window / Max Output |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Triage / Intent** | Qwen3.5-0.8B-Instruct | 0.8 Billion | Q4_0 (GGUF) | 507 MB | GenieX / llama.cpp | Snapdragon 8 Elite Hexagon v79 NPU | 4,096 ctx / 512 out |
| **Intermediate Edge** | Qwen3.5-2B-Instruct | 2.0 Billion | Q4_0 (GGUF) | 1.21 GB (on-disk) | GenieX / QAIRT | Snapdragon Hexagon NPU | 8,192 ctx / 1,024 out |
| **Primary Executor** | Qwen3.5-9B-Instruct | 9.0 Billion | Q4_0 (GGUF) | 5.4 GB | llama.cpp / CUDA or HTP Split | Jetson Orin Nano (Node Beta) or NPU | 16,384 ctx / 4,096 out |
| **Specialist Analytical** | Gemma-4-12B-IT-QAT | 12.0 Billion | QAT-Q4_0 (.bin / GGUF) | ~6.8 GB | llama.cpp (`-ctk q8_0 -ctv q8_0`) | Jetson Orin Nano Super (8GB) | 8,192 ctx / 2,048 out |


### Qualcomm AI Hub Performance Metrics (Qwen3.5-0.8B)
- **Prefilling Speed**: 1,156 tokens/s
- **Decoding Speed**: 39.6 tokens/s
- **Supported SoC**: Qualcomm Snapdragon 8 Elite (Gen 4/5), Dragonwing IQ-9075 EVK


---


## 3. Dual-Agent Router Architecture


The Dual-Agent Router (`dual_agent_router/`) evaluates incoming prompt strings, balances token load, and bridges context between triage and execution models.


```
Incoming User Input (Voice / Text)
               │
               ▼
┌──────────────────────────────────────────────┐
│ query_analyzer.py                            │
│ - Calculates estimated tokens (len // 4)     │
│ - Scans for CODE_BLOCK_REGEX                 │
│ - Matches against COMPLEX_KEYWORDS           │
└──────────────────────┬───────────────────────┘
                       │
       ┌───────────────┴───────────────┐
       ▼ [Tokens ≤ 120 & No Code]      ▼ [Tokens > 120 OR Complex Keyword OR Code]
┌──────────────────────────────┐┌──────────────────────────────┐
│ 0.8B Triage Model (GenieX)   ││ 9B Executor Model (llama.cpp)│
│ - Fast response (<512 tokens)││ - Multi-step code synthesis  │
│ - Simple conversational facts││ - Full repository audit      │
└──────────────────────────────┘└──────────────┬───────────────┘
                                               ▲
                                               │ Context Injection
                                ┌──────────────┴───────────────┐
                                │ executor_bridge.py           │
                                │ - Strips conversational fat  │
                                │ - Injects rolling_habits.json│
                                │ - Formats structured payload │
                                └──────────────────────────────┘
```


### Routing Parameters & Thresholds
- **`TRIAGE_MAX_ESTIMATED_TOKENS`**: 120 tokens.
- **Complex Keywords List**: `refactor`, `implement`, `architect`, `synthesize`, `audit`, `reverse-engineer`, `quantize`, `decompilation`, `benchmark`, `regression`, `orchestration`, `arbitration`, `heuristic`.
- **Code Block Regex**: `r"```[\s\S]*?```"`.


### Model Profiles Configuration (`model_profile_registry.json`)
- **`qwen_0_8b_triage`**:
  - `temperature`: 0.2
  - `top_p`: 0.8
  - `repeat_penalty`: 1.1
  - `system_prompt_path`: `dual_agent_router/prompts/triage_system.md`
- **`qwen_9b_executor`**:
  - `temperature`: 0.3
  - `top_p`: 0.9
  - `repeat_penalty`: 1.05
  - `system_prompt_path`: `dual_agent_router/prompts/executor_system.md`


### Token Compression Rules (`executor_bridge.py`)
`executor_bridge.py` strips conversational fluff, greetings, and boilerplate framing before sending requests to the 9B model:
- Strips matches for: `r"^sure,?\s*(here is|i can help with)?"`, `r"^i understand\b"`, `r"^as an ai model\b"`, `r"^certainly\b"`.
- Wraps payload in a strict JSON contract containing `task_id`, `contract.invariants`, `style_preferences`, and `retrieved_context`.


---


## 4. Qualcomm Hexagon NPU 3.5GB Process Domain (PD) Model Splitting


On Qualcomm Snapdragon platforms, the Hexagon Tensor Processor (HTP) enforces a strict memory ceiling of **3.5GB per Process Domain (PD)**. Monolithic allocation of the 5.4GB Qwen 3.5 9B model causes `QNN_COMMON_ERROR_MEM_ALLOC_FAILED` / `HEXAGON_ERROR_OUT_OF_MEMORY`.


### Multi-Device Virtual Layer Splitting (`D=HTP0,HTP1`)
To bypass this limitation, `novus-aexenti` uses GGML multi-device layer-splitting, partitioning the single physical Hexagon processor into two virtual devices:


```
                  Qwen 3.5 9B Q4_0 GGUF (~5.4 GB)
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                               ▼
┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│ Virtual Device 1: HTP0          │ │ Virtual Device 2: HTP1          │
│ (Process Domain 1: Max 3.5GB)   │ │ (Process Domain 2: Max 3.5GB)   │
├─────────────────────────────────┤ ├─────────────────────────────────┤
│ Model Layers: 0 to 24           │ │ Model Layers: 25 to 48          │
│ - Token Embeddings              │ │ - Attention & FFN (25 to 48)    │
│ - Attention & FFN (0 to 24)     │ │ - Final RMSNorm & LM Head       │
│ Context Allocation: ~2.8 GB     │ │ Context Allocation: ~2.7 GB     │
└────────────────┬────────────────┘ └────────────────▲────────────────┘
                 │                                   │
                 └────── FastRPC On-Chip Bus ────────┘
                         (Activation Handoff)
```


### Execution Invariants
1. **FastRPC Activation Handoff**: Layer 24 output activations transfer directly over the on-chip FastRPC silicon bus (`libadsprpc`) with sub-millisecond latency, avoiding CPU RAM roundtrips.
2. **CLI Invocation**:
   ```bash
   M=qwen3.5-9b-q4_0.gguf D=HTP0,HTP1 ./llama-server --host 127.0.0.1 --port 8081 -c 4096
   ```
3. **Ahead-Of-Time (AOT) HTP Compilation**:
   ```bash
   python3 $QNN_SDK_ROOT/bin/gguf_builder \
     --input_model ./models/qwen3.5-9b-q4_0.gguf \
     --target_backend htp \
     --output_path ./app/src/main/assets/qwen_htp.bin \
     --config_file ./config/htp_backend_profile.json
   ```
4. **Zero-Copy Shared Memory**: Buffer transfer between the Kotlin APK layer and NPU uses `AHardwareBuffer` / `ASharedMemory` mapped via `QnnMem_register()`.


---


## 5. Mem0 Episodic Memory & Habit Retention


The episodic memory tier (`mem0_episodic/`) extracts and persists active working constraints, user syntax rules, and operational habits without flooding the context window.


### Semantic TF-Cosine Recall Engine (`vector_recall_engine.py`)
- Computes lightweight local term-frequency vectors and cosine similarity against `rolling_habits.json`.
- Evaluates similarity score:
  $$\text{Cosine Similarity} = \frac{\mathbf{v_1} \cdot \mathbf{v_2}}{\|\mathbf{v_1}\| \|\mathbf{v_2}\|}$$
- Returns top-$k$ relevant rules (default: $k=3$) to prepend into executor prompts.


### Active Habit Categories (`rolling_habits.json`)
```json
{
  "version": "1.0.0",
  "active_habits": [
    {
      "category": "naming_syntax",
      "rule": "Never use 'Omni Claw' or 'Omni-Claw'. Novaexopia (novaecopia) is the harness runtime.",
      "priority": "critical"
    },
    {
      "category": "file_integrity",
      "rule": "Strict non-destructive file operations. Never modify or delete canonical originals.",
      "priority": "critical"
    },
    {
      "category": "consolidation_philosophy",
      "rule": "Reject dogmatic 1:1 file parity. Trim fluff, but retain 100% technical build instructions.",
      "priority": "high"
    },
    {
      "category": "retrieval_architecture",
      "rule": "Strict separation between raw sources, clean_md, chunk.jsonl, and wiki_md.",
      "priority": "high"
    },
    {
      "category": "tone_and_style",
      "rule": "Professional, humble, no superlatives, direct and concise.",
      "priority": "high"
    }
  ]
}
```


### Persistent Ledger Schema (`_dumbass_universal_memory/sqlite/mem0.db`)
- Embedded SQLite tables: `episodic_facts`, `user_habits`, `active_task_state`.
- Mode: WAL mode enabled (`PRAGMA journal_mode = WAL;`) to prevent concurrent read/write locking across background daemons.


---


## 6. Reasoning Bank & Crash Recovery Ledger


Located in `novus-aexenti/reasoning_bank/`:


### Active Execution Ledger (`active_execution_paths.json`)
Maintains real-time checkpoint state for multi-step tasks:
```json
{
  "ledger_version": "1.0.0",
  "active_sessions": [
    {
      "session_id": "SESSION-CANON-001",
      "target_repository": "novus-aexenti",
      "current_stage": "populating_subsystems",
      "total_steps": 4,
      "completed_steps": [
        "dual_agent_router_populated",
        "mem0_episodic_populated"
      ],
      "in_progress_step": "reasoning_bank_population",
      "checkpoint": {
        "status": "HEALTHY",
        "last_verified_file": "rolling_habits.json",
        "rollback_target": "novus-aexenti/mem0_episodic"
      }
    }
  ],
  "crash_recovery_protocol": {
    "enabled": true,
    "strategy": "idempotent_file_reverification"
  }
}
```


### Capability Regression Test Battery (`baseline_tests.json`)
- **`TEST-01-JSON-SCHEMA`**: Verifies exact JSON syntax output with keys: `status`, `exit_code`, `message`.
- **`TEST-02-INVARIANT-SAFETY`**: Negative assertion test verifying that attempts to overwrite raw original files are rejected.
- **`TEST-03-TRIAGE-ROUTING`**: Validates that short prompts route to `0.8B_triage` and complex prompts route to `9B_executor`.
- **`TEST-04-CAR-WASH-TASK`**: End-to-end integration test chaining simulated voice ingress ➔ triage ➔ executor ➔ tool dispatch.