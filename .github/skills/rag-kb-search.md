# Skill: RAG Knowledge Base Search

## Description
Searches the Mergington activities knowledge base using keyword overlap scoring.
Returns top-k activity entries as context chunks for grounded answer generation.
Eval-gated: RAGAS faithfulness must be ≥ 0.85 before this skill is used in production.

## Interface
Function: search_kb(query: str, top_k: int = 3) → list[dict]
Module:   src/rag/kb_search.py
Input:    Natural language query string
Output:   List of KB entry dicts with keys: id, title, description, max_participants, schedule

## Trigger
Use this skill when the query is about:
- Activity details (schedule, capacity, description)
- "What activities are available?"
- "Tell me about [activity name]"
- Any question answerable from activity metadata

Do NOT use this skill when:
- The query requires database aggregation or JOIN logic → use text2sql skill
- The query requires real-time signup counts → use text2sql skill

## Constraints

### NEVER_MODIFY — UAT-locked
- src/app.py — production API routes, must not be touched
- src/tests/test_app.py — all existing tests, must not be modified
- src/rag/activities_kb.json — KB data, update via separate data pipeline only

### Forbidden operations
- Do not add vector DB dependencies without lead approval
- Do not change the search_kb function signature (breaks router agent interface)
- Do not hardcode OPENAI_API_KEY or any secret in any file

### Eval threshold (mandatory)
- RAGAS faithfulness ≥ 0.85 required before any PR using this skill merges
- Run: python src/rag/eval_rag.py — must exit 0

## DRI
[Your name] — [your team]

## Version
v1.0 — 2026-06-21

## Deprecation policy
Review when KB grows beyond 100 entries. Replace keyword scoring with
vector search when faithfulness drops below 0.85 on ≥ 3 consecutive eval runs.