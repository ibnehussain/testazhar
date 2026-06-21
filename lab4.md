
---

# LAB 4 — Core Coding Workflows & Mandatory git diff Review
## Module M4 · Core Coding Workflows with Copilot
**Duration:** 20-30 minutes
**Type:** Individual lab

---

### Objective

Use Copilot to build a real feature using your scoped prompt from Lab 3. After each Copilot session, run the mandatory git diff review. Debug a broken function using the trust-but-verify workflow. Identify and refuse dangerous suggestions.

---

## Part A — Feature Build: GET /activities/{name} Endpoint (30 min)

### A1. Pre-flight Checks

Before touching Copilot, complete every item:

```
□ AI Scope Statement from Lab 1 is written and signed off
□ .github/copilot-instructions.md is committed and pushed
□ Prompt Review Checklist for my rewritten Prompt 1 — all 5 ticked
□ I have closed all files I don't need (static/, requirements.txt)
□ I am on the main branch (run: git status)
```

**Run this to confirm your starting state:**

```bash
git status
git log --oneline -3
pytest src/tests/test_app.py -v
```

Record the test results before any Copilot session:

```
Tests passing before Copilot session: _5 passed_____ / ______

List the test names (you'll need these for comparison later):
1.src/tests/test_app.py::test_get_activities_returns_all PASSED
2.src/tests/test_app.py::test_get_activities_has_expected_fields PASSED
3.src/tests/test_app.py::test_signup_success PASSED
4.src/tests/test_app.py::test_signup_invalid_activity PASSED
5.src/tests/test_app.py::test_root_redirects PASSED
1. _____________________________________________________________
2. _____________________________________________________________
3. _____________________________________________________________
4. _____________________________________________________________
5. _____________________________________________________________
6. _____________________________________________________________
7. _____________________________________________________________
8. _____________________________________________________________
```

### A2. Run Your Scoped Prompt

Copy your rewritten Prompt 1 from Lab 3 into Copilot Chat. If your rewrite was not signed off, use this prompt:

```
Add a new Flask route function called `get_activity` to src/app.py.

Task: Implement GET /activities/<string:activity_name> that returns
the full details of that activity as JSON with HTTP 200. If the
activity name does not exist in the activities dictionary, return
{"error": "Activity not found"} with HTTP 404.

Scope: Add this new function BELOW the remove_signup() function.
Do NOT modify get_activities(), signup(), or remove_signup().
Do NOT touch src/tests/test_app.py or any file in src/static/.

Constraint: Use jsonify() for all responses. Return HTTP 200 or 404
only. Do not add any new import statements. Do not change the
ACTIVITIES dictionary.

Format: Single function named get_activity with a one-line docstring.
```

**Before accepting the suggestion, answer these questions:**

```
Does the suggested function name match what was requested?
□ Yes: get_activity     □ No — it was named: yes : get_activity ___________________

Does the suggestion appear to be in the right location (below remove_signup)?
□ Yes     □ No — it appears to be placed at: _yes - below signup__________________

Does the suggestion include any changes to existing functions?
□ No changes to existing functions
□ Yes — it touches: ____no, it didn't touch existing functionality_______________________________________

Does the suggestion use jsonify()?
□ Yes     □ No  - used JSON Response

Does it return 404 for not-found activities?
□ Yes     □  - Yes
```

**If all answers are correct, accept the suggestion (Tab or Apply in editor).**

**If any answer is wrong, press Escape. Refine the prompt and try again.**

### A3. Mandatory git diff Review

**Run this immediately after accepting — do not skip this step:**

```bash
git diff --stat HEAD
```

Record the output:

```
Files changed and line counts:
__________________________________________________________________
__________________________________________________________________

Were any unexpected files touched?   □ No   □ Yes — which: ________

If yes: STOP. Reject the change (git checkout -- [filename]) and
escalate to the trainer.
```

**Now review the actual diff:**

```bash
git diff src/app.py
```

Answer:

```
Was get_activities() modified?              □ No (good)  □ Yes (STOP)
Was signup() modified?                      □ No (good)  □ Yes (STOP)
Was remove_signup() modified?               □ No (good)  □ Yes (STOP)
Was a new function added below remove_signup()?  □ Yes (good)  □ No
```

### A4. Run the Tests

```bash
pytest src/tests/test_app.py -v
```

```
Tests passing after Copilot session: ______ / ______

Any tests that were passing before that are now failing?
□ None — all 8 original tests still pass
□ Yes — the following tests now fail: __________________________
```

If any previously passing test now fails: this is a UAT regression. Do NOT commit. Run:

```bash
git checkout -- src/app.py
```

Then re-scope your prompt more carefully and start Part A again.

### A5. Commit Only If All Gates Pass

```bash
git add src/app.py
git commit -m "feat: add GET /activities/{name} endpoint

- New get_activity() function added below remove_signup()
- Returns 200 with activity details or 404 with error message
- Generated with GitHub Copilot assistance
- UAT-locked functions verified untouched (git diff reviewed)
- All 8 existing tests pass"

git push
```

---

## Part B — The Refactoring Danger Zone

### B1. The Tempting Prompt

The ACTIVITIES dictionary at the top of `src/app.py` contains the school's activity data. Imagine a colleague has left this comment in a PR review:

> *"The ACTIVITIES dict is getting unwieldy. Can you ask Copilot to restructure it into a proper data class or separate JSON file?"*

**Before running any prompt, answer:**

```
Is the ACTIVITIES dictionary referenced by any UAT-locked function?
□ Yes — which functions use it?
  ________________________________________________________________

If Copilot restructures it (e.g. changes it from a dict to a class),
what would happen to the existing routes that reference it?
  ________________________________________________________________

Is this a task that should use Copilot at all?
□ Yes — it's not in the NEVER_MODIFY list
□ No — it's too risky because the UAT-locked routes depend on it
□ Maybe — only with an extremely precise scope constraint
```

### B2. Run the Dangerous Prompt Anyway (observe only)

In Copilot Chat, type:

```
The ACTIVITIES dictionary in app.py is getting long.
Clean it up and make it more maintainable.
```

**Do NOT accept the suggestion. Observe what Copilot proposes.**

```
What does Copilot suggest doing with the ACTIVITIES dictionary?
__________________________________________________________________
__________________________________________________________________

If accepted, which UAT-locked functions would likely break?
__________________________________________________________________

Would the existing tests catch this immediately?   □ Yes   □ No
Explain:
__________________________________________________________________

Press ESCAPE. Do not accept this suggestion.
```

### B3. Write the Correct Response

This is a request that should be declined in its current form, or approached very differently.

```
Write the message you would send back to the colleague:

"Hi, I've looked at the ACTIVITIES dictionary restructuring request.
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

If we do want to restructure this, the safe approach would be:
_________________________________________________________________
_________________________________________________________________"
```

**The rule you have just applied:**

```
Write it in your own words (one sentence):
__________________________________________________________________
__________________________________________________________________
```

---

## Part C — Debug Lab: Trust but Verify

There is a broken function in `src/app.py` called `calculate_capacity_remaining`. The trainer added it intentionally.

### C1. Find and Read the Function

In Codespaces, scroll to the bottom of `src/app.py`. Find `calculate_capacity_remaining`.

```
What does the function try to do?
__________________________________________________________________

What is the bug (read the code before asking Copilot)?
__________________________________________________________________

When would this bug trigger?
__________________________________________________________________
```

### C2. Ask Copilot to Explain — Not Fix

In Copilot Chat, paste the function and the error you would see:

```
This function crashes in production. Before suggesting a fix,
explain WHY it crashes and in exactly which scenario:

def calculate_capacity_remaining(activity):
    """Returns remaining capacity for an activity."""
    max_participants = activity.get("max_participants")
    current = activity.get("participants", [])
    return max_participants - len(current)

Error seen: TypeError: unsupported operand type(s) for -: 'NoneType' and 'int'
```

**Record Copilot's explanation:**

```
Copilot's explanation:
__________________________________________________________________
__________________________________________________________________
__________________________________________________________________

Is this explanation correct?   □ Yes   □ Partially   □ No

How do you know? (What in the code confirms or contradicts it?)
__________________________________________________________________
__________________________________________________________________
```

**Critical rule:** If the explanation is wrong, the fix will be wrong. Only proceed to the fix if the explanation is correct.

### C3. Ask for a Scoped Fix

If the explanation was correct, ask for the fix with a constraint:

```
Fix only the None check in calculate_capacity_remaining.
If max_participants is None, return None (meaning unlimited capacity).
Do NOT change the function name, parameters, docstring, or any other
line. Do NOT touch any other function in app.py.
```

**Before accepting the fix, check:**

```
Does the fix add a None check before the subtraction?
□ Yes    □ No — re-prompt

Does it change ONLY the return line or add only a guard clause?
□ Only changes what was asked    □ Changes other lines too (reject)

Accept the fix (if both above are Yes). Then:
```

```bash
git diff src/app.py
```

```
How many lines changed?  ______

Did any other function change?   □ No (good)   □ Yes (reject and redo)
```

```bash
pytest src/tests/test_app.py -v
```

```
All 8 tests still pass?   □ Yes (commit)   □ No (investigate)
```

### C4. Commit the Fix

```bash
git add src/app.py
git commit -m "fix: handle None max_participants in calculate_capacity_remaining

- Added None guard before subtraction
- Returns None when activity has no participant cap
- Verified via Copilot Chat explanation (correct), git diff (1 line changed),
  and all 8 existing tests passing"
git push
```

---

## Part D — DANGER ZONE Checklist (10 min)

Without running Copilot, decide what you would do for each scenario. Circle your answer.

```
Scenario 1:
Copilot suggests adding a try/except block inside get_activities().
Action: ACCEPT / REJECT / REVIEW CAREFULLY

Why: _____________________________________________________________

───────────────────────────────────────────────────────────────────

Scenario 2:
Copilot's suggestion for your new endpoint also renames an existing
helper function used by signup().
Action: ACCEPT / REJECT / REVIEW CAREFULLY

Why: _____________________________________________________________

───────────────────────────────────────────────────────────────────

Scenario 3:
Copilot suggests a new test that replaces two existing tests with
one combined test (same coverage, cleaner code).
Action: ACCEPT / REJECT / REVIEW CAREFULLY

Why: _____________________________________________________________

───────────────────────────────────────────────────────────────────

Scenario 4:
Copilot suggests adding a new route decorator to an existing function
to make it handle both GET and POST requests.
Action: ACCEPT / REJECT / REVIEW CAREFULLY

Why: _____________________________________________________________

───────────────────────────────────────────────────────────────────

Scenario 5:
After your session, git diff --stat HEAD shows that static/index.js
was modified even though you only asked Copilot to update app.py.
Action: ACCEPT THE JS CHANGE / REJECT AND REVERT / ASK THE TRAINER

Why: _____________________________________________________________
```

---

### ✅ M4 GATE CHECKPOINT

Run this now. Show the output to your trainer before Day 1 ends.

```bash
git diff --stat HEAD
```

```
Output (paste or describe):
__________________________________________________________________
__________________________________________________________________

Any unexpected files?   □ No — only intentional changes
                        □ Yes — I have escalated to the trainer

Final test run:
```

```bash
pytest src/tests/test_app.py -v
```

```
All original 8 tests passing?   □ Yes   □ No — investigating

Commit hash of your work today (git log --oneline -1):
__________________________________________________________________
```

**Trainer/Lead sign-off:** _______________________ ✓

---

---

# DAY 1 — END OF DAY REFLECTION

**Complete before leaving. Takes 5 minutes.**

```
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

───────────────────────────────────────────────────────────────────

2. The most surprising thing I learned today:

   ______________________________________________________________
   ______________________________________________________________

3. The habit I am most likely to forget in production:

   ______________________________________________________________

   What reminder will I put in place?

   ______________________________________________________________

4. One question I still have:

   ______________________________________________________________
   ______________________________________________________________

───────────────────────────────────────────────────────────────────

5. Day 2 preview — what tomorrow's labs will build on top of today:

   Lab 5 (M5) — Test protection: ensuring Copilot-generated tests
                 ADD to the suite and never replace existing ones

   Lab 6 (M6) — SKILL.md: encoding your UAT rules in reusable,
                 shareable team assets

   Lab 7 (M7) — Eval-driven development: automated regression
                 detection in CI so the pipeline catches what
                 manual review missed

   Lab 8 (M10) — The 7-step pre-PR pipeline: no PR opens
                  unless all gates pass automatically
```

---

---

# REFERENCE — Day 1 Quick Cards

Cut out and keep at your desk during labs.

```
┌──────────────────────────────────────────────┐
│  FOUR-PART PROMPT ANATOMY                    │
│                                              │
│  TASK        What to build (specific)        │
│  SCOPE       Where it goes + what NOT to     │
│              touch (name the functions)      │
│  CONSTRAINT  Coding rules, libraries,        │
│              status codes                    │
│  FORMAT      Function name, docstring,       │
│              return shape                    │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  ALWAYS REJECT THESE                         │
│                                              │
│  • Any change to a NEVER_MODIFY function     │
│  • Any test deletion or simplification       │
│  • Restructuring of the ACTIVITIES dict      │
│  • Unparameterised SQL strings               │
│  • New dependencies not in scope statement   │
│  • Changes to static/ files                  │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  AFTER EVERY COPILOT SESSION                 │
│                                              │
│  git diff --stat HEAD                        │
│  git diff src/app.py                         │
│  pytest src/tests/test_app.py -v             │
│                                              │
│  If unexpected files appear → STOP           │
│  If any test fails → STOP                    │
│  If both clean → commit with attribution     │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  PROMPT REVIEW CHECKLIST (run before every   │
│  Copilot code generation prompt)             │
│                                              │
│  □ What to BUILD specified?                  │
│  □ What NOT to touch specified?              │
│  □ Test requirements specified?              │
│  □ Function-level scope (not module)?        │
│  □ No red-flag words?                        │
│    (refactor/improve/clean/rewrite)          │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  MERGINGTON UAT-LOCKED FUNCTIONS             │
│                                              │
│  get_activities()  — GET /activities         │
│  signup()          — POST /…/signup          │
│  remove_signup()   — DELETE /…/signup        │
│                                              │
│  src/tests/test_app.py — ALL tests locked    │
└──────────────────────────────────────────────┘
```

---