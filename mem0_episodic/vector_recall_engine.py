#!/usr/bin/env python3
"""
vector_recall_engine.py - Semantic lookup script for in-session conversational facts and habit keys.
Pulls episodic memory facts, user preferences, and working session constraints.
Part of the NovusÆxenti cognitive engine.
"""

import json
import math
import os
import sys
from typing import List, Dict, Any, Tuple

DEFAULT_HABITS_PATH = os.path.join(os.path.dirname(__file__), "rolling_habits.json")

def token_vector(text: str) -> Dict[str, int]:
    """Generates simple term-frequency vector for lightweight local cosine matching."""
    vec = {}
    for word in text.lower().split():
        w = "".join(c for c in word if c.isalnum())
        if w:
            vec[w] = vec.get(w, 0) + 1
    return vec

def cosine_similarity(v1: Dict[str, int], v2: Dict[str, int]) -> float:
    """Calculates cosine similarity between two term frequency dictionaries."""
    dot = sum(v1[k] * v2.get(k, 0) for k in v1)
    mag1 = math.sqrt(sum(val ** 2 for val in v1.values()))
    mag2 = math.sqrt(sum(val ** 2 for val in v2.values()))
    if not mag1 or not mag2:
        return 0.0
    return dot / (mag1 * mag2)

def recall_habits(query: str, habits_path: str = DEFAULT_HABITS_PATH, top_k: int = 5) -> List[Tuple[str, float]]:
    """Recalls active user habits and constraints matching the current query."""
    if not os.path.exists(habits_path):
        return [("No habits file found at target path.", 0.0)]

    with open(habits_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    habits = data.get("active_habits", [])
    query_vec = token_vector(query)

    scored = []
    for item in habits:
        content = f"{item.get('category', '')} {item.get('rule', '')} {item.get('context', '')}"
        sim = cosine_similarity(query_vec, token_vector(content))
        scored.append((item.get("rule", ""), round(sim, 3)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]

if __name__ == "__main__":
    test_q = sys.argv[1] if len(sys.argv) > 1 else "naming conventions and file structure"
    results = recall_habits(test_q)
    print(f"Recall results for query: '{test_q}'")
    for rule, score in results:
        print(f"  [{score}] {rule}")
