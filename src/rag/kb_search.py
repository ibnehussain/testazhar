"""Search helpers for the activities knowledge base.

This module loads the local JSON knowledge base and provides a simple keyword
overlap scorer for ranking activity entries.
"""

from __future__ import annotations

import json
from pathlib import Path


_KB_PATH = Path(__file__).with_name("activities_kb.json")


def _load_kb() -> list[dict]:
    """Load the activities knowledge base from the adjacent JSON file."""
    with _KB_PATH.open("r", encoding="utf-8") as kb_file:
        return json.load(kb_file)


def _tokenize(text: str) -> set[str]:
    """Convert text into a set of lowercase keyword tokens."""
    cleaned = "".join(character if character.isalnum() else " " for character in text.lower())
    return {token for token in cleaned.split() if token}


def search_kb(query: str, top_k: int = 3) -> list[dict]:
    """Return the top_k knowledge base entries that best match a query.

    The ranking uses simple keyword overlap between the query and each entry's
    title and description. Results are ordered by overlap score, then title.
    """
    query_tokens = _tokenize(query)
    if not query_tokens or top_k <= 0:
        return []

    ranked_entries: list[tuple[int, dict]] = []
    for entry in _load_kb():
        searchable_text = f"{entry.get('title', '')} {entry.get('description', '')}"
        entry_tokens = _tokenize(searchable_text)
        score = len(query_tokens & entry_tokens)

        if score > 0:
            ranked_entries.append((score, entry))

    ranked_entries.sort(key=lambda item: (-item[0], str(item[1].get("title", ""))))
    return [entry for _, entry in ranked_entries[:top_k]]


if __name__ == "__main__":
    SAMPLE_QUERIES = ["chess tournament", "creative art", "daily run"]

    for sample_query in SAMPLE_QUERIES:
        print(f"Query: {sample_query}")
        print(json.dumps(search_kb(sample_query), indent=2, ensure_ascii=False))
        print()