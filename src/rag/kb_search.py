"""
Knowledge Base Search Module

This module provides functions for searching the activities knowledge base
stored in JSON format. It uses keyword overlap scoring to find relevant
activity entries matching user queries.
"""

import json
from pathlib import Path
from typing import List, Dict, Any


def search_kb(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Search the activities knowledge base and return top matching entries.

    This function loads activities from src/rag/activities_kb.json and performs
    keyword overlap scoring against the title and description fields. Keywords
    from the query are matched case-insensitively.

    Args:
        query: The search query string (e.g., "chess" or "basketball")
        top_k: Number of top results to return (default: 3)

    Returns:
        A list of up to top_k activity dictionaries (with id, title, description,
        max_participants, schedule), sorted by relevance score (highest first).
        Returns an empty list if the knowledge base is empty or no matches found.

    Example:
        >>> results = search_kb("chess")
        >>> len(results) <= 3
        True
        >>> results[0]["title"] if results else None
        'Chess Club'
    """
    # Load knowledge base from JSON
    kb_path = Path(__file__).parent / "activities_kb.json"
    
    try:
        with open(kb_path, "r") as f:
            activities = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
    # Normalize query for matching
    query_words = query.lower().split()
    if not query_words or not query_words[0]:
        return []
    
    # Score each activity
    scored_activities = []
    for activity in activities:
        # Combine searchable fields
        searchable_text = (activity.get("title", "") + " " + 
                          activity.get("description", "")).lower()
        
        # Calculate keyword overlap score
        score = sum(1 for word in query_words if word in searchable_text)
        
        if score > 0:
            scored_activities.append((score, activity))
    
    # Sort by score (descending) and return top_k
    scored_activities.sort(key=lambda x: x[0], reverse=True)
    return [activity for _, activity in scored_activities[:top_k]]


if __name__ == "__main__":
    # Sample queries for testing
    print("=" * 60)
    print("Knowledge Base Search - Sample Queries")
    print("=" * 60)
    
    queries = ["chess", "basketball", "creative"]
    
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = search_kb(q, top_k=3)
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['title']} - {result['description'][:50]}...")
        else:
            print("  No results found.")
