#!/usr/bin/env python3
"""
query_analyzer.py - Dual Agent Router: Query Analysis & Triage Engine
Directs incoming prompt strings to 0.8B triage or 9B executor based on token complexity and intent.
Part of the NovusÆxenti cognitive engine.
"""

import re
import sys
import json
from typing import Dict, Any, Tuple

# Token complexity thresholds
TRIAGE_MAX_ESTIMATED_TOKENS = 120
COMPLEX_KEYWORDS = {
    "refactor", "implement", "architect", "synthesize", "audit",
    "reverse-engineer", "quantize", "decompilation", "benchmark",
    "regression", "orchestration", "arbitration", "heuristic"
}
CODE_BLOCK_REGEX = re.compile(r"```[\s\S]*?```")

def estimate_token_count(text: str) -> int:
    """Rough estimation: ~4 chars per token for English / code."""
    return max(1, len(text) // 4)

def analyze_intent(text: str) -> Dict[str, Any]:
    """Analyzes intent markers, structural complexity, and domain tags."""
    lowered = text.lower()
    has_code = bool(CODE_BLOCK_REGEX.search(text))
    keyword_matches = [kw for kw in COMPLEX_KEYWORDS if kw in lowered]
    token_est = estimate_token_count(text)

    # Calculate complexity score (0.0 to 1.0)
    score = 0.0
    if token_est > TRIAGE_MAX_ESTIMATED_TOKENS:
        score += 0.4
    if has_code:
        score += 0.3
    if keyword_matches:
        score += min(0.3, len(keyword_matches) * 0.1)

    return {
        "estimated_tokens": token_est,
        "has_code": has_code,
        "matched_keywords": keyword_matches,
        "complexity_score": round(score, 2)
    }

def route_query(prompt: str) -> Tuple[str, Dict[str, Any]]:
    """
    Determines routing target:
    - '0.8B_triage': Fast, lightweight classification, short queries, intent parsing.
    - '9B_executor': Multi-turn execution, code generation, architectural synthesis.
    """
    analysis = analyze_intent(prompt)
    if analysis["complexity_score"] >= 0.5:
        target_model = "9B_executor"
        reasoning = "High complexity, code structures, or extensive context required."
    else:
        target_model = "0.8B_triage"
        reasoning = "Short query suitable for rapid local triage."

    decision = {
        "target_model": target_model,
        "reasoning": reasoning,
        "analysis": analysis
    }
    return target_model, decision

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_prompt = " ".join(sys.argv[1:])
    else:
        test_prompt = "Status check on active daemons"

    model, details = route_query(test_prompt)
    print(json.dumps(details, indent=2))
