# LAB M8 — RAG · Text2SQL · CI/CD Integration
## Module M8 · Model Development
**Type:** Lecture / Demo → Individual lab

---

> **Prerequisites**
> - M6 SKILL.md pattern completed — you know how to author a skill file
> - M7 eval gate in place — `promptfooconfig.yaml` and `eval.yml` committed
> - RAGAS and promptfoo installed (from M7)
> - PostgreSQL available locally or via Docker (Part C)
>
> **What you build in this lab:**
> - A context-aware Copilot workflow using repo context
> - A RAG extension backed by a custom knowledge base, eval-gated with RAGAS
> - A Text2SQL module generating parameterised SQL, eval-gated for correctness
> - SKILL.md wrappers for both — ready for the M9 Router Agent to consume

---

## M8 Quality Gate

```
RAG faithfulness  ≥ 0.85   (measured by RAGAS)   → below threshold = PR blocked
Text2SQL correctness ≥ 90%  (5 NL → SQL tests)    → below threshold = iterate before merge
```

These are **hard gates**, not targets. The GitHub Actions pipeline enforces them automatically.

---

---

# PART A — Context-Aware Copilot Generation
## Lab 1 · Compare Contextual vs Non-Contextual Output
**Time:** 10 min

---

### Background

Copilot's output quality depends directly on what context it can see. When you open a bare chat window with no file context, Copilot generates plausible but generic code. When you attach the actual schema, KB index, or relevant source files, the output is grounded in your real system.

**Rule:** Never generate integration code without anchoring Copilot to your repo context first.

---

### Step 1 — Non-contextual baseline (observe only)

Open Copilot Chat with **no files open or attached**. Type:

```
Write a Python function that searches a knowledge base and returns the top 3 results.
```

Record the output:

```
Did Copilot make up a KB interface?   □ Yes  □ No 

Did the output match any real file in your repo?   □ No (expected)   □ Yes

What library did Copilot assume?
_________________________________________________________________
```

**Do NOT accept this output.** It has no grounding.

---

### Step 2 — Context-anchored generation

Now open the relevant source files in your editor. In Copilot Chat, attach your repo context and type:

```
Using the actual project structure and existing modules visible in this repo,
write a Python function that searches the activities knowledge base and returns
the top 3 matching activity names for a given query string.

Scope: Add this function to src/rag/kb_search.py (create if it does not exist).
Do NOT modify src/app.py, src/tests/test_app.py, or any UAT-locked file.
Constraint: Use only libraries already present in requirements.txt.
Format: One function named search_kb with a docstring and type hints.
```

Compare outputs:

```
Contextual output — differences from baseline:
□ Used real module paths from the repo
□ Used actual library from requirements.txt
□ Function signature matched existing code patterns
□ No invented APIs

Which output would you trust to merge into main?
□ Non-contextual (Lab A Step 1)   □ Context-anchored (Lab A Step 2)

Why?
_________________________________________________________________
```

**Key lesson:** The context window is your primary quality lever. File attachment is not optional for integration code.

---

---

# PART B — RAG with Copilot Extensions & Custom Knowledge Base
## Lab 2 · Build KB Extension → Run RAGAS Eval → Gate on Faithfulness
---

### Background: What is RAG in this context?

Retrieval-Augmented Generation (RAG) means Copilot answers questions by first retrieving relevant chunks from a knowledge base, then generating a grounded answer from those chunks. Without RAG, Copilot answers from training data — which may be stale, private-knowledge-blind, or hallucinated.

**RAGAS faithfulness** measures: does the generated answer only use facts present in the retrieved context? Score of 1.0 = perfectly grounded. Score below 0.85 = the system is hallucinating.

---

### Step 1 — Create the KB data file

Create `src/rag/activities_kb.json` — a minimal knowledge base for the Mergington activities API:

```json
[
  {
    "id": "act-001",
    "title": "Chess Club",
    "description": "Weekly chess tournament for students. Max 12 participants. Runs every Thursday.",
    "max_participants": 12,
    "schedule": "Thursday 15:00–17:00"
  },
  {
    "id": "act-002",
    "title": "Basketball Team",
    "description": "Competitive basketball practice and matches. Max 10 participants. Runs Monday and Wednesday.",
    "max_participants": 10,
    "schedule": "Monday/Wednesday 16:00–18:00"
  },
  {
    "id": "act-003",
    "title": "Art Workshop",
    "description": "Creative art sessions covering painting and sculpture. Max 15 participants. Runs Friday.",
    "max_participants": 15,
    "schedule": "Friday 14:00–16:00"
  },
  {
    "id": "act-004",
    "title": "Drama Club",
    "description": "Performance preparation and script reading. Max 20 participants. Runs Tuesday.",
    "max_participants": 20,
    "schedule": "Tuesday 15:00–17:30"
  },
  {
    "id": "act-005",
    "title": "Morning Run",
    "description": "Daily 5km group run around the school grounds. Max 30 participants. No registration required.",
    "max_participants": 30,
    "schedule": "Daily 07:00–07:45"
  }
]
```

---

### Step 2 — Generate the KB search module with Copilot

Use Copilot Chat with context attached:

```
Using src/rag/activities_kb.json as the knowledge base,
generate src/rag/kb_search.py with a function named search_kb.

Task: search_kb(query: str, top_k: int = 3) → list[dict]
Returns the top_k KB entries whose title or description best matches
the query using simple keyword overlap scoring (no external vector DB).

Scope: Only create src/rag/kb_search.py. Do NOT touch src/app.py or tests.
Constraint: No new pip dependencies. Use only Python stdlib (json, pathlib).
Format: Module with search_kb function, docstring, and a __main__ block
        that runs 3 sample queries and prints results.
```

Run a quick smoke test:

```bash
python src/rag/kb_search.py
```

```
Did the __main__ block run without errors?   □ Yes   □ No — fix before continuing

Did results look relevant for the sample queries?   □ Yes   □ Partially   □ No
```

---

### Step 3 — Write the RAGAS eval harness with Copilot

Create `src/rag/eval_rag.py`. Use Copilot to generate it:

> **No OpenAI key? Use GitHub Models instead.**
> GitHub Copilot users get access to models via `https://models.inference.ai.azure.com`
> using your existing `GITHUB_TOKEN`. No separate API key required.
> In GitHub Actions, `GITHUB_TOKEN` is injected automatically — no secret to configure.

```
Generate src/rag/eval_rag.py — a RAGAS faithfulness eval harness
for the search_kb function in src/rag/kb_search.py.

Task: For each test case below, call search_kb to retrieve context chunks,
then call an LLM to generate an answer grounded in those chunks.
Measure faithfulness using the ragas library.

Test cases:
1. query: "how many people can join chess club" → expected context contains "12"
2. query: "when does basketball practice run"   → expected context contains "Monday"
3. query: "which activity allows most participants" → expected context contains "30"
4. query: "is there a daily activity"            → expected context contains "Daily"

Constraint: Read the API key from environment variable GITHUB_TOKEN (preferred)
            OR OPENAI_API_KEY as fallback. Do NOT hardcode any key.
            When using GITHUB_TOKEN, set openai_api_base to
            https://models.inference.ai.azure.com
Output: Print each test case result and overall faithfulness score.
        Exit with code 1 if faithfulness < 0.85.
Format: Script with run_ragas_eval() function and __main__ block.
```

Install RAGAS if not already present:

```bash
pip install ragas openai
```

Run the eval — choose the option that matches your setup:

```bash
# Option 1 — GitHub Copilot users (GITHUB_TOKEN, no extra key needed)
# Get your token: https://github.com/settings/tokens → classic → read:models scope
GITHUB_TOKEN=<your-github-token> python src/rag/eval_rag.py

# Option 2 — OpenAI key (if you have one)
OPENAI_API_KEY=<your-key> python src/rag/eval_rag.py
```

Record results:

```
Test case results:
1. Chess Club query:      faithfulness = ______
2. Basketball query:      faithfulness = ______
3. Most participants:     faithfulness = ______
4. Daily activity:        faithfulness = ______

Overall faithfulness score: ______

Gate check:   □ ≥ 0.85 — PASSED (safe to continue)
              □ < 0.85 — BLOCKED — iterate on search_kb before proceeding

If blocked — what did you change to improve the score?
_________________________________________________________________
```

---

### Step 4 — Add the RAGAS gate to GitHub Actions

Add a new job to `.github/workflows/eval.yml` (or create `.github/workflows/rag-eval.yml`):

```yaml
name: RAG Faithfulness Gate

on: [pull_request]

jobs:
  rag-eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install ragas openai

      - name: Run RAGAS faithfulness eval
        env:
          # GITHUB_TOKEN is injected automatically — no secret to configure.
          # eval_rag.py reads GITHUB_TOKEN first, falls back to OPENAI_API_KEY.
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python src/rag/eval_rag.py
          echo "✅ RAG faithfulness gate passed (≥ 0.85)"
        # Exit code 1 from eval_rag.py blocks the PR automatically
```

Commit:

```bash
git add src/rag/ .github/workflows/rag-eval.yml
git commit -m "feat: add RAG KB search module with RAGAS faithfulness gate

- src/rag/activities_kb.json — knowledge base
- src/rag/kb_search.py — keyword search, no external dependencies
- src/rag/eval_rag.py — RAGAS eval, exits 1 if faithfulness < 0.85
- .github/workflows/rag-eval.yml — CI gate on every PR
- Generated with GitHub Copilot assistance"
git push
```

---

---

# PART C — Text-to-SQL via Copilot
## Lab 3 · Write 5 NL → SQL Tests · Eval Correctness ≥ 90%

---

### Background: Why Text2SQL needs an eval gate

Copilot generates plausible-looking SQL that may silently:
- Miss a `WHERE` clause (returns all rows instead of filtered)
- Use string concatenation instead of parameterised queries (SQL injection)
- Select wrong columns or join wrong tables

Without automated SQL correctness tests, these errors reach production undetected.

**The M8 gate:** 5 NL → SQL test cases. At least 4 of 5 must produce correct, parameterised SQL (90% pass rate) before the PR can merge.

---

### Step 1 — Create the database schema context file

Create `src/text2sql/schema.sql` — give Copilot the schema to work from:

```sql
-- Mergington Activities Database Schema
-- Attach this file to every Text2SQL Copilot prompt

CREATE TABLE activities (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    max_participants INT NOT NULL DEFAULT 10,
    schedule    VARCHAR(100)
);

CREATE TABLE signups (
    id          SERIAL PRIMARY KEY,
    activity_id INT REFERENCES activities(id) ON DELETE CASCADE,
    student_name VARCHAR(100) NOT NULL,
    signed_up_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(activity_id, student_name)
);
```

---

### Step 2 — Generate the 5 NL → SQL pairs with Copilot

Open Copilot Chat with `src/text2sql/schema.sql` attached:

```
Using only the schema in src/text2sql/schema.sql,
generate parameterised SQL for these 5 natural language questions.

For each question, output:
  - The question (as a comment)
  - A parameterised SQL query using %s placeholders (psycopg2 style)
  - The Python parameter tuple

Questions:
1. "How many students have signed up for Chess Club?"
2. "List all activities that still have spots available."
3. "Which activities is student Alice Johnson signed up for?"
4. "Show activities with more than 10 max participants."
5. "Remove Alice Johnson from Basketball Team."

Security constraint: ALL queries must use parameterised placeholders.
No string formatting or f-strings in SQL. Any query using string
concatenation is an automatic rejection.

Format: Python dict named SQL_QUERIES with keys q1–q5.
        Each value: {"sql": "...", "params": (...)}
Save to: src/text2sql/queries.py
```

---

### Step 3 — Write the SQL correctness eval

Create `src/text2sql/eval_sql.py`:

```python
"""
Text2SQL correctness eval — M8 gate.
Checks: parameterisation, structure, expected keywords.
Pass rate must be ≥ 90% (at least 4/5) to clear the CI gate.
"""
import sys
from queries import SQL_QUERIES

TESTS = [
    {
        "id": "q1",
        "description": "Count signups for Chess Club",
        "must_contain": ["COUNT", "signups", "activities"],
        "must_not_contain": ["f\"", "f'", "% name", "+ name"],
        "must_use_params": True,
    },
    {
        "id": "q2",
        "description": "Activities with available spots",
        "must_contain": ["max_participants", "signups"],
        "must_not_contain": ["f\"", "f'"],
        "must_use_params": False,  # no user input in this query
    },
    {
        "id": "q3",
        "description": "Activities for a named student",
        "must_contain": ["signups", "activities", "student_name"],
        "must_not_contain": ["f\"", "f'", "+ student"],
        "must_use_params": True,
    },
    {
        "id": "q4",
        "description": "Activities with max_participants > 10",
        "must_contain": ["max_participants"],
        "must_not_contain": ["f\"", "f'"],
        "must_use_params": False,
    },
    {
        "id": "q5",
        "description": "Remove a student from an activity (DELETE)",
        "must_contain": ["DELETE", "signups", "student_name"],
        "must_not_contain": ["f\"", "f'", "+ student", "DROP"],
        "must_use_params": True,
    },
]


def run_eval():
    passed = 0
    for test in TESTS:
        qid = test["id"]
        entry = SQL_QUERIES.get(qid, {})
        sql = entry.get("sql", "")
        params = entry.get("params", None)

        failures = []

        for keyword in test["must_contain"]:
            if keyword.upper() not in sql.upper():
                failures.append(f"Missing keyword: {keyword}")

        for forbidden in test["must_not_contain"]:
            if forbidden in sql:
                failures.append(f"Forbidden pattern found: {forbidden}")

        if test["must_use_params"] and not params:
            failures.append("Parameterised query required but params tuple is empty/None")

        if failures:
            print(f"  FAIL [{qid}] {test['description']}")
            for f in failures:
                print(f"       → {f}")
        else:
            print(f"  PASS [{qid}] {test['description']}")
            passed += 1

    rate = passed / len(TESTS) * 100
    print(f"\nSQL correctness: {rate:.0f}% ({passed}/{len(TESTS)})")

    if rate < 90:
        print("BLOCKED: SQL correctness below 90% threshold.")
        sys.exit(1)
    print("PASSED: SQL correctness gate cleared.")


if __name__ == "__main__":
    run_eval()
```

Run the eval:

```bash
cd src/text2sql
python eval_sql.py
```

Record results:

```
q1 — Count signups:        □ PASS   □ FAIL — reason: ________________
q2 — Available spots:      □ PASS   □ FAIL — reason: ________________
q3 — Student's activities: □ PASS   □ FAIL — reason: ________________
q4 — Max participants > 10:□ PASS   □ FAIL — reason: ________________
q5 — DELETE signup:        □ PASS   □ FAIL — reason: ________________

Overall pass rate: ______ / 5 = ______%

Gate check:   □ ≥ 90% — PASSED
              □ < 90% — BLOCKED — fix failing queries before committing

Did any query use string concatenation instead of parameterisation?
□ No — all safe      □ Yes — which query: ______ — fix immediately (SQL injection risk)
```

**If any query uses string formatting instead of `%s` — reject it immediately.** This is a security failure, not just an eval failure.

---

### Step 4 — Add SQL correctness gate to CI

Add to `.github/workflows/eval.yml` or create `.github/workflows/sql-eval.yml`:

```yaml
name: Text2SQL Correctness Gate

on: [pull_request]

jobs:
  sql-eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Run SQL correctness eval
        run: |
          cd src/text2sql
          python eval_sql.py
          echo "✅ SQL correctness gate passed (≥ 90%)"
        # Exit code 1 blocks the PR
```

Commit:

```bash
git add src/text2sql/ .github/workflows/sql-eval.yml
git commit -m "feat: add Text2SQL module with correctness eval gate

- src/text2sql/schema.sql — activities DB schema
- src/text2sql/queries.py — 5 parameterised NL→SQL queries
- src/text2sql/eval_sql.py — correctness eval, exits 1 if < 90%
- .github/workflows/sql-eval.yml — CI gate on every PR
- All queries use parameterised placeholders (SQL injection safe)
- Generated with GitHub Copilot assistance"
git push
```

---

---

# PART D — Wrap RAG + Text2SQL as SKILL.md Entries
## Lab 4 · Publish Skills for M9 Router Agent Consumption
**Time:** 8 min

---

### Background

The M9 Router Agent (next module) needs to call your RAG and Text2SQL tools. It discovers them through SKILL.md entries. If the SKILL.md is missing the CONSTRAINTS section or has vague interface documentation, the router agent will either fail silently or call the wrong tool.

**Rule:** Every tool handed to an agent must have a SKILL.md with: interface spec, eval threshold, and CONSTRAINTS.

---

### Step 1 — Create the RAG skill file

Create `.github/skills/rag-kb-search.md`:

```markdown
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
```

---

### Step 2 — Create the Text2SQL skill file

Create `.github/skills/text2sql.md`:

```markdown
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
```

---

### Step 3 — Verify both skills are discoverable

```bash
ls .github/skills/
# Expected output:
# add-activity-endpoint.md   (from M6)
# rag-kb-search.md           (just created)
# text2sql.md                (just created)
```

Test discoverability from Copilot Chat:

```
@workspace List all available skills in .github/skills/ and summarise
what each one does and what eval gate it requires.
```

```
Did Copilot correctly identify all 3 skill files?   □ Yes   □ No
Did it report the eval thresholds from the CONSTRAINTS section?
□ Yes — faithfulness ≥ 0.85 and correctness ≥ 90% both mentioned
□ No — CONSTRAINTS section may be missing or malformed
```

---

### Step 4 — Commit and push all skill files

```bash
git add .github/skills/rag-kb-search.md .github/skills/text2sql.md
git commit -m "feat: add SKILL.md entries for RAG and Text2SQL tools

- .github/skills/rag-kb-search.md — interface, constraints, RAGAS threshold
- .github/skills/text2sql.md — interface, constraints, SQL correctness threshold
- Both skills ready for M9 Router Agent consumption
- DRI assigned, eval thresholds documented"
git push
```

---

---

### ✅ M8 GATE CHECKPOINT

```
CI Gates active — verify each in GitHub Actions tab:
─────────────────────────────────────────────────────────────────────
□ RAG faithfulness gate:    rag-eval.yml committed and running on PRs
□ RAG score achieved:       RAGAS faithfulness = ______ (must be ≥ 0.85)
□ SQL correctness gate:     sql-eval.yml committed and running on PRs
□ SQL score achieved:       correctness = ______ / 5 = ______% (must be ≥ 90%)
□ No SQL injection risk:    all queries use %s parameterisation — 0 f-strings in SQL
□ SKILL.md — RAG:           .github/skills/rag-kb-search.md committed with CONSTRAINTS
□ SKILL.md — Text2SQL:      .github/skills/text2sql.md committed with CONSTRAINTS
□ Both skills discoverable: Copilot @workspace can see and describe all 3 skill files
```

**Hand-off to M9:** The Router Agent in M9 will use `rag-kb-search.md` and `text2sql.md` as its tool interface. If either SKILL.md is missing the CONSTRAINTS section or the eval threshold, the router agent will either fail to call the right tool or merge untested code.

---

### M8 Reflection

```
1. Before this lab, what would have happened if you merged the Text2SQL module
   without the correctness eval?
   _________________________________________________________________

2. Which is higher risk: a RAG faithfulness of 0.82 or a SQL correctness of 80%?
   Why?
   _________________________________________________________________
   _________________________________________________________________

3. The SKILL.md CONSTRAINTS section lists the eval threshold.
   What happens if the M9 router agent uses a SKILL.md with an outdated threshold?
   _________________________________________________________________
```

**Trainer/Lead sign-off:** _______________________ ✓
