#!/usr/bin/env python3
"""
executor_bridge.py - Formats clean, compressed meta-prompts for execution models.
Applies RTK/Caveman token compression, strips redundant framing, and wraps context.
Part of the NovusÆxenti cognitive engine.
"""

import json
import re
from typing import Dict, Any, List, Optional

SYSTEM_INVARIANTS = [
    "Strict non-destructive file operations.",
    "Deterministic exit codes (0 for success, non-zero for failure).",
    "Preserve verbatim speaker attribution and error traces."
]

def compress_context(text: str) -> str:
    """Strips conversational boilerplate, redundant whitespace, and filler phrases."""
    cleaned = re.sub(r"[ \t]+", " ", text)
    lines = [line.strip() for line in cleaned.split("\n") if line.strip()]

    # Remove common conversational filler
    filler_patterns = [
        r"^sure,?\s*(here is|i can help with)?",
        r"^i understand\b",
        r"^as an ai model\b",
        r"^certainly\b"
    ]
    filtered_lines = []
    for line in lines:
        filtered = line
        for pat in filler_patterns:
            filtered = re.sub(pat, "", filtered, flags=re.IGNORECASE).strip()
        if filtered:
            filtered_lines.append(filtered)

    return "\n".join(filtered_lines)

def build_executor_payload(
    task_id: str,
    raw_prompt: str,
    relevant_chunks: Optional[List[Dict[str, Any]]] = None,
    habits: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Constructs a structured, token-optimized meta-prompt payload for the 9B executor.
    """
    compressed_task = compress_context(raw_prompt)

    payload = {
        "task_id": task_id,
        "contract": {
            "invariants": SYSTEM_INVARIANTS,
            "formatting": "markdown",
            "style_preferences": habits or {}
        },
        "retrieved_context": relevant_chunks or [],
        "instruction": compressed_task
    }
    return payload

if __name__ == "__main__":
    sample_prompt = "Can you please refactor the socket listener in aesc daemon? Thanks so much!"
    sample_payload = build_executor_payload("TASK-001", sample_prompt)
    print(json.dumps(sample_payload, indent=2))
