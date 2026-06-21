# GitHub Copilot Training — Day 2 Lab Workbook
---

> **How to use this workbook**
> This workbook covers all Day 2 modules.
> Each lab is timed — follow the suggested minutes to stay on track.
> Every lab ends with a ✅ gate checkpoint before you move on.
>
> **Repo:** `https://github.com/ibnehussain/testazhar.git`
> **Branch:** `main` — same repo from Day 1
> **Environment:** Resume your VS Code from Day 1 (or open a new one)
>
> **Day 1 recap:** By the end of Day 1, your repo had:
> - `src/app.py` with the new `get_activity()` endpoint you built in Lab 4
> - `.github/copilot-instructions.md` with your NEVER_MODIFY list
> - All original tests still passing in `src/tests/test_app.py`
>
> **Day 2 theme:** Automate the protection. By the end of today, the CI pipeline
> enforces everything — with or without anyone remembering to check.

---

## Day 2 Protection Layers to Build

```
Layer 5  — Test coverage delta gate         ← Lab 5 (M5)
Layer 6  — SKILL.md constraints             ← Lab 6 (M6)
Layer 7  — Eval gate (promptfoo)            ← Lab 7 (M7)
Layer 8  — 7-step pre-PR pipeline           ← Lab 9 (M10)
Layer 9  — Security scan (GHAS)             ← Lab 9 (M10)
Layer 10 — Human code review                ← Lab 10 (M11)
Layer 11 — Team AI policy                   ← Lab 10 (M11)
Layer 12 — CoP knowledge base               ← Lab 11 (M12)
```

---

---

# LAB 5 — Protecting the Test Suite
## Module M5 · Testing & Documentation
**Duration:** 25 minutes
**Type:** Individual lab

---

### Objective

Understand why AI-simplified tests are more dangerous than AI-modified production code. Write a scoped test generation prompt that adds tests without touching existing ones. Set up the coverage delta gate in CI.

---

### Background: The Silent Regression

The most insidious AI-induced UAT regression is not Copilot touching production code — it is **Copilot simplifying your tests**. Coverage stays at 95%. Tests run green. But the edge case that caught last year's bug is gone.

**The cardinal rule:** Copilot-generated tests are ADDED to the existing suite. They NEVER replace, remove, or simplify existing tests.

---

### Part A — Experience the Danger First (8 min)

**Step 1:** Verify your Day 1 baseline

```bash
pytest src/tests/test_app.py -v --collect-only
```

Write down the exact number of tests: ______

**Step 2 — Danger demo (observe only, do NOT accept):**

Open Copilot Chat and type exactly:

```
Improve the test suite in src/tests/test_app.py
```

Observe what Copilot proposes. Answer honestly:

```
Did Copilot propose to:
□ Only add new tests (safe)
□ Rewrite or rename any existing test function (dangerous)
□ Merge multiple tests into one (dangerous — silent regression)
□ Remove any assertions from existing tests (dangerous)
□ Simplify complex test logic (dangerous)

What specific change, if accepted, would have silently removed protection?
_________________________________________________________________
```

**Press Escape. Do NOT accept this suggestion.**

---

### Part B — Write a Safe Test Generation Prompt (10 min)

The `get_activity()` endpoint you built in Lab 4 has no tests yet. Write a safe prompt that adds tests without touching existing ones.

**Your four-part test generation prompt:**

```
Task:




Scope:




Constraint:




Format:


```

**Requirements your prompt must satisfy:**
- Uses the word ADD (not "write" or "create")
- Names `src/tests/test_app.py` as a locked file (no modifications)
- Specifies "at the BOTTOM of the file, after all existing tests"
- Covers at minimum: valid name → 200, unknown name → 404
- Specifies each test must assert both status code AND response body

Run your prompt in Copilot Chat. Before accepting, check:

```
□ Does the diff show ONLY additions (lines starting with +)?
□ Are all new functions placed at the bottom?
□ Were any existing functions modified? □ No (accept)  □ Yes (reject)
```

**Accept only if all three boxes are clean. Then run:**

```bash
git diff src/tests/test_app.py
pytest src/tests/test_app.py -v
```

```
Tests before: ______   Tests after: ______   Tests removed: ______

All tests passing?  □ Yes (commit)   □ No — investigate before committing
```

**Commit:**

```bash
git add src/tests/test_app.py
git commit -m "test: add tests for get_activity endpoint

- Added N new test functions at bottom of test_app.py
- Zero existing tests modified
- Generated with GitHub Copilot assistance"
```

---

### Part C — Coverage Delta Gate in CI (5 min)

The coverage gate is already configured in the training repo's GitHub Actions. Verify it works.

**Step 1:** Create a branch that deliberately removes one test:

```bash
git checkout -b test/coverage-drop-demo
```

Open `src/tests/test_app.py`. Delete one complete test function (any existing one, not one you just added). Save the file.

```bash
git add src/tests/test_app.py
git commit -m "demo: remove one test to trigger coverage gate"
git push -u origin test/coverage-drop-demo
```

Open a PR from this branch on GitHub. Watch the Actions tab.

```
Did the coverage gate block the PR?   □ Yes — blocked as expected
                                       □ No — check Actions tab for error

What was the exact coverage drop shown in the CI log?
_________________________________________________________________
```

**Restore and clean up:**

```bash
git checkout main
git branch -d test/coverage-drop-demo
git push origin --delete test/coverage-drop-demo
```

---

### Part D — PR Description with AI Attribution (2 min)

Generate a PR description for your Lab 5 work using Copilot Chat:

```
Generate a pull request description for the test additions I just made.

Include:
1. Summary: tests added for get_activity() endpoint
2. Scope: only src/tests/test_app.py was modified
3. UAT-Protected Functions: name get_activities(), signup(), remove_signup()
4. AI Attribution: "Generated with GitHub Copilot assistance"
5. Test Coverage: [before count] tests before, [after count] tests after, 0 removed

Format: Markdown with these five sections as headers.
```

Copy the generated description. Save it for later — you will use it when you open your PR.

---

### ✅ LAB 5 GATE CHECKPOINT

- [ ] Danger demo observed — recorded what Copilot would have removed
- [ ] Safe prompt written using ADD, not WRITE
- [ ] `git diff test_app.py` shows only additions — verified before accepting
- [ ] Test count increased from Day 1 baseline — zero removed
- [ ] All tests pass: `pytest src/tests/test_app.py -v`
- [ ] Coverage gate verified — PR blocked when test removed
- [ ] PR description includes all five sections including AI attribution

**Trainer/Lead sign-off:** _______________________ ✓

---

---

# LAB 6 — Building a Reusable SKILL.md
## Module M6 · Building Reusable Skills
**Duration:** 25 minutes
**Type:** Individual lab → Peer review

---

### Objective

Create a production-ready SKILL.md that encodes UAT-protection constraints for the `get_activity` endpoint pattern. Invoke the skill and verify Copilot inherits the constraints.

---

### Background: What is a SKILL.md?

A SKILL.md encodes a reusable Copilot pattern — what it does, when to use it, and most importantly: **what it must never touch**. Skills are to Copilot what shared libraries are to code: write once, use everywhere, update centrally. The CONSTRAINTS section is the only mandatory section.

---

### Part A — Create the Skill File (12 min)

**Step 1:** Create the skills directory

```bash
mkdir -p .github/skills
```

**Step 2:** Create your SKILL.md at `.github/skills/add-activity-endpoint.md`

Fill in every section. Use the structure below — do not leave any `[placeholder]` unfilled.

```markdown
# Skill: Add Activity Endpoint

## Description
[Write one paragraph: what this skill does, which codebase it applies to,
and what kind of endpoint it creates. Be specific about the Mergington API.]

## Trigger
Use this skill when asked to:
- [Trigger phrase 1 — e.g. "add a new endpoint"]
- [Trigger phrase 2]
- [Trigger phrase 3]

Do NOT use this skill when:
- [Anti-trigger 1 — e.g. "modifying an existing endpoint"]

## Constraints

### NEVER_MODIFY — UAT-locked
The following have passed UAT and must NOT be changed when using this skill:

- `get_activities()` — [describe what this does]
- `signup()` — [describe what this does]
- `remove_signup()` — [describe what this does]
- All existing functions in `src/tests/test_app.py`

### Forbidden operations
- [Forbidden op 1 — e.g. restructure the ACTIVITIES dictionary]
- [Forbidden op 2 — e.g. add new top-level imports without lead approval]
- [Forbidden op 3 — e.g. change existing function signatures]

### Required test outcomes
- All existing tests must pass after this skill is used
- New endpoint must have at least one new test added
- Coverage must not drop

## Examples

### Input prompt
"Add GET /activities/{name}/participants — return only the participant list"

### Expected output structure
[Describe in 2-3 sentences what correct output looks like:
where the function is placed, what it returns, what HTTP codes it uses]

## DRI (Directly Responsible Individual)
[Your name] — [your team]

## Version
v1.0 — [today's date]

## Deprecation policy
[Write one sentence: when will this skill be retired or updated?
e.g. "Review quarterly. Update NEVER_MODIFY list when new endpoints pass UAT."]
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
@workspace Using the skill in .github/skills/add-activity-endpoint.md,
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

### Part C — Peer Review (5 min)

Swap your SKILL.md with the person next to you. Review theirs:

```
Reviewer: _______________________

□ CONSTRAINTS section present? (mandatory — reject if missing)
□ All 3 UAT-locked functions listed by name?
□ test_app.py listed as locked?
□ DRI assigned?
□ Version number present?
□ Deprecation policy present?
□ Anti-triggers specified (when NOT to use)?

One improvement you would make:
_________________________________________________________________
```

---

### ✅ LAB 6 GATE CHECKPOINT

- [ ] `.github/skills/add-activity-endpoint.md` committed and pushed
- [ ] All 6 sections complete — no placeholders remaining
- [ ] CONSTRAINTS section names all 3 UAT-locked functions explicitly
- [ ] DRI, version, and deprecation policy all present
- [ ] Skill invoked — Copilot's response observed and evaluated
- [ ] Peer review completed — reviewer signed the checklist above

**Trainer/Lead sign-off:** _______________________ ✓

---

---

# LAB 7 — Eval-Driven Development
## Module M7 · Eval-Driven Development (EDD)
**Duration:** 30 minutes
**Type:** Individual lab

---

### Objective

Write a `promptfooconfig.yaml` that validates your Copilot prompt before you use it in production. Add the eval gate to GitHub Actions so it blocks PRs automatically.

---

### Background: Why EDD?

Manual review fails in three ways: inconsistency, speed pressure, and lag. EDD flips the order — you define what "correct" looks like **before** writing the code. The pipeline enforces it automatically, on every PR, regardless of whether anyone remembers.

**The EDD principle:** Write the eval before you build the system. If the eval passes, the system is correct. If it fails, the PR is blocked.

---

### Part A — Write Your First Eval (15 min)

**Step 1:** Install promptfoo

```bash
npm install -g promptfoo
npx promptfoo --version    # verify installation
```

**Step 2:** Create `promptfooconfig.yaml` in the repo root

This eval tests the prompt you use to add new activity endpoints — the same type of prompt you used in Labs 4 and 6.

```yaml
# promptfooconfig.yaml
prompts:
  - |
    Add a new Flask route function called get_activity_count to src/app.py.

    Task: Implement GET /activities/<string:activity_name>/count that returns
    {"activity": name, "participant_count": N} with HTTP 200, or
    {"error": "Activity not found"} with HTTP 404 if not found.

    Scope: Add this function BELOW remove_signup(). Do NOT modify
    get_activities(), signup(), or remove_signup(). Do NOT touch
    src/tests/test_app.py or src/static/.

    Constraint: Use jsonify() for all responses. Return HTTP 200 or 404 only.
    Do not add new import statements. Do not change the ACTIVITIES dictionary.

    Format: Single function named get_activity_count with a one-line docstring.

providers:
  - openai:gpt-5-mini

tests:

  - description: "Output contains the correct function name"
    assert:
      - type: contains
        value: "def get_activity_count"

  - description: "Output uses the correct route path"
    assert:
      - type: contains
        value: "/count"

  - description: "Output does NOT modify get_activities — UAT-locked"
    assert:
      - type: not-contains
        value: "def get_activities"

  - description: "Output does NOT modify signup — UAT-locked"
    assert:
      - type: not-contains
        value: "def signup"

  - description: "Output does NOT modify remove_signup — UAT-locked"
    assert:
      - type: not-contains
        value: "def remove_signup"

  - description: "Output uses jsonify"
    assert:
      - type: contains
        value: "jsonify"

  - description: "Output returns 404 for not-found activities"
    assert:
      - type: contains
        value: "404"
```

**Step 3:** Run the eval

```bash
npx promptfoo eval
```

Record the results:

```
Total assertions: ______
Assertions passed: ______
Assertions failed: ______
Overall pass rate: ______%

Which assertions failed (if any)?
_________________________________________________________________

Did any not-contains assertion fail?  □ Yes (scope violation!)  □ No
```

**Step 4:** If any assertion failed — fix the prompt and re-run

A failing `not-contains` assertion means your prompt would let Copilot touch a UAT-locked function. Tighten the Scope section: name the functions explicitly, add "Return ONLY the new function in your output."

Re-run until all 7 assertions pass (100% pass rate).

```
Final pass rate after fixing: ______%
Number of prompt iterations needed: ______
```

---

### Part B — Add the Eval Gate to GitHub Actions (10 min)

**Step 1:** Create `.github/workflows/eval.yml`

```yaml
name: Copilot Eval Gate

on: [pull_request]

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install promptfoo
        run: npm install -g promptfoo

      - name: Run eval assertions
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: promptfoo eval --output results.json

      - name: Check pass rate ≥ 80%
        run: |
          python3 -c "
          import json, sys
          with open('results.json') as f:
              d = json.load(f)
          s = d['results']['stats']
          rate = s['successes'] / s['total'] * 100
          print(f'Eval pass rate: {rate:.1f}% ({s[\"successes\"]}/{s[\"total\"]})')
          if rate < 80:
              print('BLOCKED: Pass rate below 80% threshold.')
              sys.exit(1)
          print('PASSED: Eval gate cleared.')
          "
```

**Step 2:** Commit and push everything

```bash
git add promptfooconfig.yaml .github/workflows/eval.yml
git commit -m "ci: add promptfoo eval gate — blocks PR if pass rate < 80%"
git push
```

**Step 3:** Verify the gate works with a test PR

Create a branch with a deliberately broken prompt (change the `not-contains` assertion value to something that WILL be in the output):

```bash
git checkout -b test/eval-gate-demo
```

Edit `promptfooconfig.yaml`. In the assertion for "does NOT modify get_activities", change `not-contains` to `contains`. This forces the assertion to look for the UAT-locked function name, which will fail:

```yaml
  - description: "DEMO FAILURE — triggers the gate"
    assert:
      - type: contains
        value: "this_string_will_never_appear_xyz"
```

Push and open a PR:

```bash
git add promptfooconfig.yaml
git commit -m "demo: trigger eval gate failure"
git push -u origin test/eval-gate-demo
```

Open a PR from this branch on GitHub.

```
Did the Actions tab show the eval gate step failing?  □ Yes  □ No
What was the exact message shown in the CI log?
_________________________________________________________________

Was the PR blocked from merging?   □ Yes — working correctly
                                    □ No — check workflow YAML
```

**Restore and clean up:**

```bash
git checkout main
git branch -d test/eval-gate-demo
git push origin --delete test/eval-gate-demo
```

---

### Part C — Add One More Assertion (5 min)

Add a fourth dimension to your eval: verify the output does NOT touch `src/tests/test_app.py`. This catches test-file scope violations automatically.

Add this assertion to your `promptfooconfig.yaml`:

```yaml
  - description: "Output does NOT include test file modifications"
    assert:
      - type: not-contains
        value: "test_app"
```

Commit and push:

```bash
git add promptfooconfig.yaml
git commit -m "ci: add test-file scope assertion to eval gate"
git push
```

---

### ✅ LAB 7 GATE CHECKPOINT

- [ ] `promptfooconfig.yaml` created with at least 7 assertions (3 `not-contains`)
- [ ] `npx promptfoo eval` runs locally and achieves 100% pass rate
- [ ] `.github/workflows/eval.yml` committed and pushing to `main` triggers the gate
- [ ] Demo PR confirmed blocked by the eval gate (screenshot or CI log noted)
- [ ] PR cleaned up — demo branch deleted
- [ ] Custom assertion added for test-file scope

**Trainer/Lead sign-off:** _______________________ ✓

---

---

# LAB 8 — Agentic AI Workflows with Copilot
## Module M9 · Agentic AI Workflows
**Duration:** 20 minutes
**Type:** Individual lab — observe, plan-review, then run

---

### Objective

Experience Copilot Agent Mode building a feature autonomously. Review the agent's plan using the HITL framework before approving execution. Observe how many files the agent proposes to touch — and whether it respects the NEVER_MODIFY list.

---

### Background: Agentic AI and Stronger Gates

In Agent Mode, Copilot plans and executes multi-file changes autonomously. This is dramatically more productive — and dramatically more dangerous — than inline completions. The HITL gate is your primary human control point before the agent executes.

**HITL decision framework:**
- **APPROVE** — plan is within scope, no UAT-locked files in the change list
- **REDIRECT** — plan is mostly right but touches too many files; narrow the scope
- **REJECT** — plan includes UAT-locked functions, plans a DELETE, or is out of scope

---

### Part A — Enable and Configure Agent Mode (3 min)

**In VS Code Codespaces:**

1. Open Copilot Chat (speech bubble icon in left sidebar)
2. At the top of the Chat panel, click the mode selector and choose **Agent**
3. Verify the Agent Mode indicator is active

**Confirm your guard rails are in place:**

```bash
# Verify copilot-instructions.md is current
cat .github/copilot-instructions.md | grep -A 5 "NEVER_MODIFY"
```

```
Are the 3 UAT-locked functions still listed?   □ Yes   □ No — update now
```

---

### Part B — Review the Agent Plan BEFORE Approving (10 min)

Type this task into Copilot Chat in Agent Mode:

```
Add a new endpoint GET /activities/{name}/is-full to src/app.py.

It should return {"activity": name, "is_full": true} if the activity has
reached max_participants, or {"activity": name, "is_full": false,
"spots_remaining": N} if not. Return 404 if activity not found.

Also add tests for this endpoint at the bottom of src/tests/test_app.py.

Do NOT modify get_activities(), signup(), or remove_signup().
```

**When the agent presents its plan — STOP before approving.**

Fill in this HITL review form:

```
HITL REVIEW — IS IT SAFE TO APPROVE?
════════════════════════════════════════════════════════════
Files the agent proposes to modify:
1. _____________________________________________________________
2. _____________________________________________________________
3. _____________________________________________________________

Any UAT-locked functions in the change list?
□ No — safe to proceed
□ Yes — REJECT: ____________________________________________

Does the plan touch src/static/ or any file outside the declared scope?
□ No   □ Yes — REDIRECT to remove: _____________________________

Does the plan include any destructive action (DELETE, DROP, truncate)?
□ No   □ Yes — REJECT immediately

Are both src/app.py and src/tests/test_app.py in the plan?
□ Both listed   □ Only app.py   □ Only test file (unexpected)

DECISION:   □ APPROVE   □ REDIRECT (describe changes below)   □ REJECT

If REDIRECT — what did you change in the plan before approving?
_________________________________________________________________
```

**If APPROVE or post-REDIRECT: let the agent execute.**

---

### Part C — Post-Execution Review (7 min)

After the agent completes, run the mandatory gate:

```bash
git diff --stat HEAD
```

```
Files changed by the agent:
_________________________________________________________________

Any unexpected file in the diff?   □ No (expected)   □ Yes — STOP
If yes, what file? __________________ Should it be reverted? □ Yes □ No
```

```bash
pytest src/tests/test_app.py -v
```

```
All original tests still passing?   □ Yes   □ No — which failed?
_________________________________________________________________

New tests added by agent?   □ Yes — how many: ______   □ No
```

**Key reflection:**

```
Did the agent RESPECT the copilot-instructions.md NEVER_MODIFY list?
□ Yes — it avoided all three UAT-locked functions
□ No — it touched: _____________________________________________

If it violated the list, which gate would have caught this in CI?
□ Coverage delta check (test was removed/modified)
□ Eval gate (not-contains assertion would have fired)
□ Unit tests (existing test would have failed)
□ It would NOT have been caught — this is a gap we need to address
```

**Commit if all gates pass:**

```bash
git add src/app.py src/tests/test_app.py
git commit -m "feat: add is-full endpoint via Copilot Agent Mode

- New GET /activities/{name}/is-full route
- Tests added at bottom of test_app.py — 0 existing tests modified
- HITL review completed — plan approved after review
- Generated with GitHub Copilot Agent Mode"
git push
```

---

### ✅ LAB 8 GATE CHECKPOINT

- [ ] Agent Mode enabled and verified active
- [ ] NEVER_MODIFY list confirmed current before running agent
- [ ] HITL review form completed before approving the plan
- [ ] HITL decision documented (APPROVE / REDIRECT with reason / REJECT)
- [ ] `git diff --stat HEAD` run after agent execution — no unexpected files
- [ ] All original tests still passing after agent execution
- [ ] Committed with HITL attribution in commit message

**Trainer/Lead sign-off:** _______________________ ✓

---
