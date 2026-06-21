# Skill: Text2SQL — Natural Language to Parameterised SQL

## Description
Converts natural language questions into safe, parameterised PostgreSQL queries
against the Mergington activities and signups tables.
Eval-gated: SQL correctness must be ≥ 90% (4/5 test cases) before use in production.

## Interface
Module:  src/text2sql/queries.py
Schema:  src/text2sql/schema.sql
Usage:   Import SQL_QUERIES dict; select query by key (q1–q5); execute with params tuple.

## Trigger
Use this skill when the query requires:
- Counting signups or participants
- Finding available spots (aggregation: max_participants − signup count)
- Filtering activities by attribute (schedule, capacity)
- Adding or removing a signup (INSERT / DELETE)
- Any query that needs JOIN across activities and signups tables

Do NOT use this skill when:
- The query is about activity descriptions or metadata → use rag-kb-search skill
- The query is a free-text "tell me about" question → use rag-kb-search skill

## Constraints

### NEVER_MODIFY — UAT-locked
- src/app.py — production routes, must not be touched
- src/tests/test_app.py — UAT-passing tests, must not be modified
- src/text2sql/schema.sql — schema is source of truth; change via migration only

### Forbidden operations
- String formatting or f-strings in SQL — automatic security rejection
- Raw string concatenation with user input — SQL injection risk
- DROP, TRUNCATE, or ALTER statements — destructive, forbidden without DBA approval
- Adding new tables without a reviewed migration script

### Eval threshold (mandatory)
- SQL correctness ≥ 90% required before any PR using this skill merges
- Run: cd src/text2sql && python eval_sql.py — must exit 0

## DRI
[Your name] — [your team]

## Version
v1.0 — 2026-06-21

## Deprecation policy
Review when schema changes. Re-run eval after any schema migration.
Retire and replace when query set expands beyond 10 NL patterns.