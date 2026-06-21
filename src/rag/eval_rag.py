"""Simple RAGAS-style faithfulness evaluation harness for the KB search module.

This script uses the existing search_kb function to retrieve context from the
activity knowledge base, asks an LLM to answer the question using only that
context, and then evaluates how faithful the answer is to the retrieved
context. The implementation is intentionally lightweight and uses only the
Python standard library plus optional ragas support when available.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib import request, error

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rag.kb_search import search_kb


TEST_CASES: List[Dict[str, Any]] = [
    {
        "query": "how many people can join chess club",
        "expected_contains": ["12"],
    },
    {
        "query": "when does basketball practice run",
        "expected_contains": ["Monday"],
    },
    {
        "query": "which activity allows most participants",
        "expected_contains": ["30"],
    },
    {
        "query": "is there a daily activity",
        "expected_contains": ["Daily"],
    },
]


def _get_api_key() -> Optional[str]:
    """Read the API key from the preferred environment variable."""
    return os.getenv("GITHUB_TOKEN") or os.getenv("OPENAI_API_KEY")


def _build_context(chunks: List[Dict[str, Any]]) -> str:
    """Convert retrieved KB chunks into a concise text context."""
    pieces: List[str] = []
    for chunk in chunks:
        title = chunk.get("title", "")
        description = chunk.get("description", "")
        schedule = chunk.get("schedule", "")
        max_participants = chunk.get("max_participants", "")
        pieces.append(
            f"Title: {title}\nDescription: {description}\nSchedule: {schedule}\nMax participants: {max_participants}"
        )
    return "\n\n".join(pieces)


def _call_llm(query: str, context: str) -> str:
    """Call an OpenAI-compatible chat completion endpoint using stdlib urllib."""
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "No API key found. Set GITHUB_TOKEN (preferred) or OPENAI_API_KEY."
        )

    model = os.getenv("RAG_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_API_BASE", "https://models.inference.ai.azure.com")
    api_url = f"{base_url.rstrip('/')}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You answer using only the provided context. If the context does not contain the answer, say so clearly.",
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            },
        ],
        "temperature": 0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = json.dumps(payload).encode("utf-8")

    req = request.Request(api_url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"LLM request failed: {exc.code} {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected response format: {body}") from exc


def _faithfulness_score(answer: str, context: str) -> float:
    """Compute a lightweight faithfulness score from supported evidence words."""
    if not answer.strip():
        return 0.0

    # Normalize text and extract a simple set of content words.
    context_words = set(re.findall(r"[a-z0-9]+", context.lower()))
    answer_words = set(re.findall(r"[a-z0-9]+", answer.lower()))

    if not context_words:
        return 0.0

    overlap = len(answer_words & context_words)
    denom = max(1, len(answer_words))
    score = overlap / denom
    return max(0.0, min(1.0, score))


def run_ragas_eval() -> Tuple[List[Dict[str, Any]], float]:
    """Run the faithfulness evaluation across the provided test cases."""
    results: List[Dict[str, Any]] = []
    scores: List[float] = []

    for case in TEST_CASES:
        query = case["query"]
        chunks = search_kb(query, top_k=3)
        context = _build_context(chunks)
        answer = _call_llm(query, context)
        score = _faithfulness_score(answer, context)
        scores.append(score)

        expected_contains = case.get("expected_contains", [])
        expected_found = all(token.lower() in context.lower() for token in expected_contains)

        results.append(
            {
                "query": query,
                "context": context,
                "answer": answer,
                "faithfulness": score,
                "expected_context_found": expected_found,
            }
        )

        print(f"Query: {query}")
        print(f"  Context matched expected tokens: {expected_found}")
        print(f"  Faithfulness: {score:.2f}")
        print(f"  Answer: {answer}")
        print("-" * 60)

    overall_score = sum(scores) / len(scores) if scores else 0.0
    print(f"Overall faithfulness score: {overall_score:.2f}")
    return results, overall_score


if __name__ == "__main__":
    try:
        _, overall_score = run_ragas_eval()
    except Exception as exc:  # pragma: no cover - simple CLI entrypoint
        print(f"Evaluation failed: {exc}")
        raise SystemExit(1) from exc

    raise SystemExit(1 if overall_score < 0.85 else 0)
