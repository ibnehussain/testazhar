
# GitHub Copilot Training — Day 1 Lab Workbook Answers

## LAB 1 — AI Scope Statement

### Step 1 — AI Scope Statement

```text
AI SCOPE STATEMENT
Task:
Add a new endpoint GET /activities/{activity_name} that returns the full activity
JSON for a valid activity name and returns HTTP 404 with an error message for
unknown names. Do not change any existing routes.

In scope (files Copilot MAY touch):
- src/app.py
  - Add only the new GET /activities/{activity_name} route
- src/tests/test_app.py
  - Add tests only for the new endpoint

UAT-locked (files Copilot must NEVER modify):
- src/app.py
  - get_activities() — GET /activities
  - signup_for_activity() — POST /activities/{activity_name}/signup
  - remove_signup() — DELETE /activities/{activity_name}/signup
- src/tests/test_app.py
  - All existing tests are locked and must not be changed

Tests (must remain passing after this session):
- Existing GET /activities tests
- Existing signup tests
- Existing redirect/root tests
- Any new endpoint tests that are added for GET /activities/{activity_name}

Reviewed by: Trainer / Lead  Date: 2026-06-20
```

### Step 2 — Pair Review

```text
Reviewer: Partner Name

□ Is the Task field specific enough to prevent ambiguity?
  Yes — it clearly defines the exact route and expected status codes.

□ Does the UAT-locked list name SPECIFIC functions/files?
  Yes — it names exact functions and the test file.

□ Are all three UAT-passing route functions listed by name?
  Yes — get_activities(), signup_for_activity(), and remove_signup().

□ Is test_app.py explicitly listed as UAT-locked?
  Yes.

□ Are the test requirements specific?
  Yes — the scope says existing tests must stay green and the new endpoint must be covered.

What would you tighten? Write one suggestion here:
Use the exact route pattern GET /activities/{activity_name} and state that no
response shape for other routes can be changed.
```

### Step 3 — Self-Assessment

```text
Q1. Was your UAT-locked list specific enough?
    □ Yes — I named specific functions

Q2. Did you miss any of the three UAT-locked functions?
    □ I listed all three: get_activities(), signup_for_activity(), remove_signup()

Q3. Did you include test_app.py in the UAT-locked list?
    □ Yes

Q4. What would happen if a developer started a Copilot session
    with no scope statement?
    Copilot could accidentally modify protected routes or tests, causing regressions.
```

### ✅ M1 GATE CHECKPOINT

- [x] Written (not blank)
- [x] UAT-locked list names specific functions
- [x] All three UAT-locked route functions listed by name
- [x] `src/tests/test_app.py` listed as UAT-locked
- [x] Reviewed by the trainer or lead

---

## LAB 2 — Copilot Foundations & copilot-instructions.md

### Part A — IDE Setup

#### A3. Trigger an Inline Suggestion

```text
What did Copilot suggest?
A suggestion may appear to add a small helper or a welcoming route near the bottom
of the file after the existing endpoints.

Did it suggest touching any existing function?  □ Yes  □ No

Press ESCAPE now — do NOT accept the suggestion.
```

#### A4. Open Copilot Chat and Ask What It Sees

```text
Files Copilot reports seeing:
- src/app.py
- src/tests/test_app.py
- src/static/
- README.md
- requirements.txt

Does it know which routes have passed UAT?    □ Yes  □ No
Does it know what your test results are?      □ Yes  □ No

What does this tell you about why copilot-instructions.md matters?
Copilot can see files and repo structure, but it does not automatically know the
team's UAT rules. A copilot-instructions.md file makes those protections explicit.
```

### Part B — Write copilot-instructions.md

#### B3. Completed instructions template

```markdown
# Project: Mergington High School Activities API
# Copilot Instructions

## Purpose
This repository provides a FastAPI service for viewing and managing school activities.

## NEVER_MODIFY — UAT-locked code
The following have passed User Acceptance Testing and must NOT be modified by any
Copilot suggestion.

### UAT-locked route functions (src/app.py)
- `get_activities()` — GET /activities
- `signup_for_activity()` — POST /activities/{activity_name}/signup
- `remove_signup()` — DELETE /activities/{activity_name}/signup

### UAT-locked test file
- `src/tests/test_app.py` — ALL existing test functions are locked. Never delete,
  rename, or modify any existing test function.

## Scope of Copilot assistance
Copilot may help with:
- Adding the new GET /activities/{activity_name} endpoint
- Adding tests for the new endpoint only
- Updating docs that describe the new endpoint and its behavior

## Constraints
- Keep all existing public APIs unchanged unless the ticket explicitly allows a new route
- Preserve the current response behavior for locked routes
- Return 404 with a clear error payload for unknown activity names
- Do not add imports unless they are clearly needed
- Never suggest changes that reduce test coverage
- Never remove or rename any existing public API endpoint
```

#### B5. Test — Does Copilot Respect the Instructions?

```text
Test 1: Ask Copilot to modify a locked function
Prompt:
Refactor the signup() function in src/app.py to improve its error handling.

What did Copilot say or suggest?
□ It refused or added a disclaimer about NEVER_MODIFY
□ It still suggested changes to signup()
□ Mixed — it suggested some changes

If it still suggested changes to signup() — what does that tell you?
It means the instructions were not strong enough or were not being followed.
This is why git diff review is mandatory after every session.
```

```text
Test 2: Ask Copilot about the file without the instructions file
With instructions file:
Copilot should be more likely to avoid changing locked code and focus on the new endpoint.

Without instructions file:
Copilot may suggest broader edits that risk protected routes or tests.

Restore the file now:
(restore .github/copilot-instructions.md)
```

### ✅ M2 GATE CHECKPOINT

- [x] Copilot is active and verified in your Codespace
- [x] `.github/copilot-instructions.md` exists and is committed
- [x] The NEVER_MODIFY section lists all 3 UAT-locked functions by name
- [x] `src/tests/test_app.py` is listed as locked
- [x] You have tested the file and observed Copilot's response

---

## LAB 3 — Prompting for Safe Code Generation

### Part A — Identify the Red Flags

**Prompt 1**
```text
Improve the activities endpoint.
```
Red flags:
- "Improve" is vague
- "activities endpoint" is too broad and could affect multiple routes
- No constraint about what must not be touched
- No output format

What would Copilot likely do to our UAT-locked routes?
It could change the existing activities listing or signup logic instead of just adding the new detail endpoint.

---

**Prompt 2**
```text
Refactor app.py to add error handling.
```
Red flags:
- "Refactor" is too broad
- "app.py" is file-level scope
- No specific behavior is described
- No UAT-locked list is named

Which UAT-locked function is most at risk from this prompt and why?
`signup_for_activity()` is most at risk because the prompt invites changes to error behavior for a route that must remain unchanged.

---

**Prompt 3**
```text
Write tests for the new feature.
```
Red flags:
- No exact file is specified
- No assertions are defined
- "new feature" is ambiguous
- No guidance about preserving existing tests

What is the worst-case outcome from this prompt?
Copilot could add tests that do not match the expected API behavior or accidentally change the locked test suite.

---

**Prompt 4**
```text
Make the signup endpoint more robust.
```
Red flags:
- Targets a UAT-locked route directly
- "More robust" is vague
- No constraint to preserve current behavior

Why is this prompt especially dangerous for this codebase?
It could change status codes, payload formats, or the signup logic in code that has already passed UAT.

---

**Prompt 5**
```text
Fix the calculate_capacity_remaining function in app.py.
```
Red flags:
- Better because it names a specific function
- Still missing: exact expected behavior
- Still missing: what must not be touched
- Still missing: which tests should verify the fix

---

### Part B — Rewrite the Prompts

**Rewrite of Prompt 1**

```text
Task:
Add a GET /activities/{activity_name} endpoint that returns full activity JSON for a valid name.

Scope:
Only edit src/app.py to add the new route. Do not modify get_activities(), signup_for_activity(), or remove_signup().

Constraint:
Return HTTP 200 for valid activity names and HTTP 404 with a clear error payload for unknown names. Keep all other routes unchanged.

Format:
Add one route handler and preserve the existing JSON style used by the API.
```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

**Rewrite of Prompt 2**

```text
Task:
Add explicit error handling for the new get_activity() route so unknown names return a clean 404 response.

Scope:
Only edit the get_activity() handler in src/app.py. Do not modify any other route functions.

Constraint:
Do not change the behavior of get_activities(), signup_for_activity(), or remove_signup(). Keep the existing tests passing.

Format:
Return a JSON error payload with an HTTP 404 status when the activity does not exist.
```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

**Rewrite of Prompt 3**

```text
Task:
Add tests that verify GET /activities/{activity_name} returns the activity details for valid names and a 404 error for invalid names.

Scope:
Only modify src/tests/test_app.py to add tests for the new endpoint. Do not rename or delete existing tests.

Constraint:
Do not change existing route behavior. Keep the same assertion style and test structure.

Format:
Add two test functions that assert status codes and response payloads.
```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

**Rewrite of Prompt 4** — This one you must NOT rewrite

```text
What should you do instead of running Prompt 4?
Do not ask Copilot to modify signup_for_activity(). Instead, explain that the route is UAT-locked and must remain unchanged.

Write the response you would send to the requester:
"Hi [name], I cannot use Copilot to modify signup_for_activity() because it is one of the UAT-locked routes and changing it would risk breaking existing behavior."
```

---

**Rewrite of Prompt 5**

```text
Task:
Fix the calculate_capacity_remaining() bug so the remaining capacity is computed correctly.

Scope:
Only edit calculate_capacity_remaining() and directly related tests.

Constraint:
Do not modify any UAT-locked routes or change public API response shapes.

Format:
Return the corrected numeric value and add a test that verifies the expected result.
```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

### Part C — Run Both Versions and Compare

```text
Weak prompt result:
Copilot may guess that the task involves editing multiple endpoints or changing response behavior broadly.

Would it have touched any UAT-locked function?  □ Yes  □ No  □ Maybe

Strong prompt result:
Copilot should narrow the suggestion to the single new endpoint and avoid changes to locked routes.

Would it have touched any UAT-locked function?  □ Yes  □ No  □ Maybe

What was the key difference?
The strong prompt clearly defines the task, scope, constraints, and format, which reduces the chance of accidental changes.
```

### ✅ M3 GATE CHECKPOINT

```text
PROMPT REVIEW CHECKLIST — Final Check
Prompt being reviewed: Rewrite 1 — Add get_activity endpoint

□ Specifies WHAT to build (function name, route, response shape)
□ Specifies what NOT to touch (names the 3 locked functions)
□ References test requirements (existing tests must stay green)
□ Function-level scope (not "update app.py" or "fix the routes")
□ No red-flag words (refactor / improve / clean / rewrite)

Ready to run?   □ YES — all 5 checked   □ NO — revise first
```

---

## LAB 4 — Core Coding Workflows & Mandatory git diff Review

### A1. Pre-flight Checks

```text
Tests passing before Copilot session: 5 / 5

List the test names:
1. test_get_activities_returns_all
2. test_get_activities_has_expected_fields
3. test_signup_success
4. test_signup_invalid_activity
5. test_root_redirects
```

### A2. Run Your Scoped Prompt

```text
Does the suggested function name match what was requested?
□ Yes: get_activity

Does the suggestion appear to be in the right location (below remove_signup)?
□ Yes

Does the suggestion include any changes to existing functions?
□ No changes to existing functions

Does the suggestion use jsonify()?
□ Yes

Does it return 404 for not-found activities?
□ Yes
```

### A3. Mandatory git diff Review

```text
Files changed and line counts:
- src/app.py (1 new route added)

Were any unexpected files touched?   □ No
```

```text
Was get_activities() modified?              □ No (good)
Was signup_for_activity() modified?         □ No (good)
Was remove_signup() modified?               □ No (good)
Was a new function added below remove_signup()?  □ Yes (good)
```

### A4. Run the Tests

```text
Tests passing after Copilot session: 5 / 5

Any tests that were passing before that are now failing?
□ None — all 5 original tests still pass
```

### Part B — The Refactoring Danger Zone

#### B1. The ACTIVITIES dictionary question

```text
Is the ACTIVITIES dictionary referenced by any UAT-locked function?
□ Yes — get_activities() and signup_for_activity() use it.

If Copilot restructures it, what would happen to the existing routes?
The existing routes would likely break because they depend on the dictionary structure.

Is this a task that should use Copilot at all?
□ No — it's too risky because the UAT-locked routes depend on it
```

#### B2. Dangerous prompt response

```text
What does Copilot suggest doing with the ACTIVITIES dictionary?
It may propose converting the dictionary to a class or separate storage model.

If accepted, which UAT-locked functions would likely break?
get_activities() and signup_for_activity() would likely break.

Would the existing tests catch this immediately?
□ Yes
Explain:
The current tests assert the route behavior and dictionary shape used by the API.
```

#### B3. Correct response to colleague

```text
"Hi, I've looked at the ACTIVITIES dictionary restructuring request.
This would be risky because the locked routes depend on the current dictionary shape.
If we do want to restructure this, the safe approach would be to do it in a
separate, fully scoped experiment with regression tests before changing production code."
```

### Part C — Debug Lab: Trust but Verify

```text
What does the function try to do?
It tries to compute how many participants are still allowed to join an activity.

What is the bug?
The code subtracts a number from `max_participants` without checking whether
`max_participants` is None.

When would this bug trigger?
It triggers when an activity exists but has no numeric participant cap.
```

```text
Copilot's explanation:
The crash happens because `max_participants` can be `None`, so the subtraction
attempts to do `None - len(current)` and Python raises a TypeError.

Is this explanation correct?
□ Yes

How do you know?
The error message explicitly shows the subtraction is between `NoneType` and `int`.
```

```text
Does the fix add a None check before the subtraction?
□ Yes

Does it change only the return line or add only a guard clause?
□ Only changes what was asked

How many lines changed?
1

Did any other function change?
□ No (good)

All 5 tests still pass?
□ Yes
```

### Part D — Danger Zone Checklist

```text
Scenario 1:
Copilot suggests adding a try/except block inside get_activities().
Action: REJECT
Why: This is a UAT-locked route and the prompt should stay focused on the new endpoint.

Scenario 2:
Copilot's suggestion for your new endpoint also renames an existing helper function used by signup().
Action: REJECT
Why: Renaming shared logic can break protected routes.

Scenario 3:
Copilot suggests a new test that replaces two existing tests with one combined test.
Action: REJECT
Why: Existing tests must not be deleted or replaced.

Scenario 4:
Copilot suggests adding a new route decorator to an existing function to make it handle both GET and POST requests.
Action: REJECT
Why: This would change API behavior for a protected route.

Scenario 5:
After your session, git diff --stat HEAD shows that static/index.js was modified.
Action: REJECT AND REVERT
Why: Unrequested frontend files are out of scope and should not be changed.
```

### ✅ M4 GATE CHECKPOINT

```text
All original 5 tests passing?   □ Yes
Commit hash of your work today (git log --oneline -1):
<record the latest commit hash here>
```

---

# DAY 1 — END OF DAY REFLECTION

```text
1. Today I added these protection layers:

   Layer 1 — AI Scope Statement:
   □ Written for Ticket #47
   □ UAT-locked list is specific (not "all existing files")

   Layer 2 — copilot-instructions.md:
   □ Created, committed, and pushed
   □ NEVER_MODIFY section is complete

   Layer 3 — Scoped prompts (four-part anatomy):
   □ Completed Lab 3 rewrites
   □ Used a scoped prompt for the feature build in Lab 4

   Layer 4 — git diff review:
   □ Ran git diff --stat HEAD after every session
   □ Verified no unexpected files were touched

2. The most surprising thing I learned today:
   The safest workflows come from being explicit about what is in scope and what must stay unchanged.

3. The habit I am most likely to forget in production:
   Reviewing git diff before accepting a suggestion.

4. One question I still have:
   How do I make the instructions file strong enough to block risky suggestions automatically?

5. Day 2 preview — what tomorrow's labs will build on top of today:
   Lab 5 will build on test protection, Lab 6 will add reusable skills, and Lab 7 will add CI-style regression checks.
```
