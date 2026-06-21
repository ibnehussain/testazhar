# LAB 6 — Building a Reusable SKILL.md
## Module M6 · Building Reusable Skills
**Type:** Individual lab 

---

### Objective

Create a production-ready SKILL.md that encodes UAT-protection constraints for the `get_activity` endpoint pattern. Invoke the skill and verify Copilot inherits the constraints.

---

### Background: What is a SKILL.md?

A SKILL.md encodes a reusable Copilot pattern — what it does, when to use it, and most importantly: **what it must never touch**. Skills are to Copilot what shared libraries are to code: write once, use everywhere, update centrally. The CONSTRAINTS section is the only mandatory section.

---

### Part A — Use the Skill File 

**Step 1:** Create the skills directory

```bash
mkdir -p .github/skills
```

**Step 2:** Create your SKILL.md at `.github/skills/add-activity-endpoint.md`

Do not leave any `[placeholder]` unfilled.

```markdown
# Skill: Add Activity Endpoint

## Description
Adds a new Flask route to the Mergington activities API (src/app.py).
Use when adding any new GET, POST, or DELETE endpoint that reads or
modifies the ACTIVITIES dictionary.

## Trigger
Use when asked to: "add a new endpoint", "add a new route", "implement
an API for [feature name]" in the Mergington activities codebase.

## Constraints
### NEVER_MODIFY — UAT-locked
- get_activities() in src/app.py
- signup() in src/app.py
- remove_signup() in src/app.py
- All existing functions in src/tests/test_app.py

### Forbidden operations
- Do not restructure the ACTIVITIES dictionary
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
A single new Flask route function below remove_signup() that uses
jsonify() and returns HTTP 200 or 404.

## DRI
Tech Lead — [name]
## Version
v1.0 — [date]


```

---

### Part B — Invoke the Skill and Verify (8 min)

**Step 1:** Commit your SKILL.md

```bash
git add .github/skills/add-activity-endpoint.md
git commit -m "feat: add SKILL.md for activity endpoint pattern"
git push
```

**Step 2:** Invoke the skill from Copilot Chat

```
Using the skill in .github/skills/add-activity-endpoint.md,
add a new endpoint GET /activities/{name}/is-full that returns
{"activity": name, "is_full": true/false} based on whether the
activity has reached its max_participants limit.

Return 200 with the result, or 404 if activity not found.
```

**Step 3:** Review Copilot's response — before accepting:

```
Did the skill's CONSTRAINTS section appear to influence the output?
□ Yes — Copilot avoided the NEVER_MODIFY functions
□ No — Copilot suggested changes to a locked function

Did the output place the new function BELOW remove_signup()?
□ Yes   □ No — the placement was: _____________________________

Did the output include changes to any existing function?
□ No (safe to accept)   □ Yes (reject and re-scope)
```

**If safe: accept → run git diff → run pytest → commit**

```bash
git diff --stat HEAD
# Expected: only src/app.py changed

pytest src/tests/test_app.py -v
# Expected: all original tests pass
```

---

---

### ✅ LAB 6 GATE CHECKPOINT

- [ ] `.github/skills/add-activity-endpoint.md` committed and pushed
- [ ] All 6 sections complete — no placeholders remaining
- [ ] CONSTRAINTS section names all 3 UAT-locked functions explicitly
- [ ] DRI, version, and deprecation policy all present
- [ ] Skill invoked — Copilot's response observed and evaluated

**Trainer/Lead sign-off:** _______________________ ✓
