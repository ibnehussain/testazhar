# LAB 6 — Building a Reusable SKILL.md (Answers)

## Part A — Skill File Template

A strong completed skill should include:

```markdown
# Skill: Add Activity Endpoint

## Description
Adds a new Flask route to the Mergington activities API (`src/app.py`).
Use when adding any new GET, POST, or DELETE endpoint that reads or
modifies the `ACTIVITIES` dictionary.

## Trigger
Use when asked to: "add a new endpoint", "add a new route", or "implement
an API for [feature name]" in the Mergington activities codebase.

## Constraints
### NEVER_MODIFY — UAT-locked
- `get_activities()` in `src/app.py`
- `signup()` in `src/app.py`
- `remove_signup()` in `src/app.py`
- All existing functions in `src/tests/test_app.py`

### Forbidden operations
- Do not restructure the `ACTIVITIES` dictionary
- Do not add new top-level imports without lead approval
- Do not change existing function signatures

### Required test outcomes
- All existing tests must pass after the skill is used
- New tests must be added for new functionality
- Coverage must not drop

## Examples
### Input
"Add GET /activities/{name}/participants that returns the participant list"

### Expected output structure
A single new Flask route function below `remove_signup()` that uses
`jsonify()` and returns HTTP 200 or 404.

## DRI
Tech Lead — <your name>

## Version
v1.0 — <today's date>
```

## Part B — Skill Verification

Correct review answers:

```text
Did the skill's CONSTRAINTS section appear to influence the output?
□ Yes — Copilot avoided the NEVER_MODIFY functions
□ No — Copilot suggested changes to a locked function

Did the output place the new function BELOW remove_signup()?
□ Yes
□ No — the placement was: <record actual placement>

Did the output include changes to any existing function?
□ No (safe to accept)
□ Yes (reject and re-scope)
```

Expected validation:

```bash
git diff --stat HEAD
# Expected: only src/app.py changed

pytest src/tests/test_app.py -v
# Expected: all original tests pass
```

## ✅ LAB 6 GATE CHECKPOINT

- [x] Skill file created and committed
- [x] All required sections are complete
- [x] UAT-locked functions are explicitly listed
- [x] DRI and version are present
- [x] Skill invocation was reviewed before accepting
