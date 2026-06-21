# LAB 5 — Protecting the Test Suite
## Module M5 · Testing & Documentation
**Type:** Individual lab

---

### Objective

Understand why AI-simplified tests are more dangerous than AI-modified production code. Write a scoped test generation prompt that adds tests without touching existing ones. Set up the coverage delta gate in CI.

---

### Background: The Silent Regression

The most insidious AI-induced UAT regression is not Copilot touching production code — it is **Copilot simplifying your tests**. Coverage stays at 95%. Tests run green. But the edge case that caught last year's bug is gone.

**The cardinal rule:** Copilot-generated tests are ADDED to the existing suite. They NEVER replace, remove, or simplify existing tests.

---

### Part A — Experience the Danger First

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

### Part B — Use a Safe Test Generation Prompt

The `get_activity()` endpoint you built in Lab 4 has no tests yet. Use a safe prompt that adds tests without touching existing ones.

**Your four-part test generation prompt:**

```
Add new unit tests for the get_activity() route to src/tests/test_app.py.

Task: Write pytest test functions that cover:
  1. Valid activity name → returns 200 and full details
  2. Unknown activity name → returns 404 and {"error": "Activity not found"}
  3. Empty string name → returns 404

Scope: Add these as NEW functions at the BOTTOM of test_app.py, after all
existing tests. Do NOT modify, delete, or rename any existing test function.

Constraint: Use the Flask test client. Each test must assert both status
code AND response body. Do not touch src/app.py.

Format: Three separate test functions, each named test_get_activity_[scenario].


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

### Part C — Coverage Delta Gate in CI

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

### Part D — PR Description with AI Attribution

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

