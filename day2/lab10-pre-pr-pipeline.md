# LAB 9 — The 7-Step Pre-PR Pipeline
## Module M10 · Productizing Copilot Workflows
**Type:** Individual lab

---

### Objective

Assemble all CI gates built today into a single 7-step pre-PR pipeline. Configure branch protection so no PR can open until all steps pass. Verify both a passing and a blocking scenario.

---

### Background: "No Breaks Before the PR"

A PR is not a draft — it is a claim that code is ready for human review. Every automated check that can be run before the PR must run before the PR. The pipeline is the enforcer.

**The 7 steps:**

| Step | What | Gate |
|---|---|---|
| 1 | Copilot generates | Scoped prompt + AI Scope Statement |
| 2 | Linter (Ruff) | `ruff check src/` |
| 3 | Unit tests | All existing tests pass |
| 4 | Eval gate | ≥ 80% pass rate (promptfoo) |
| 5 | Security scan | 0 high/critical findings |
| 6 | Auto-docs | AI-attributed PR description generated |
| 7 | PR opens | Only if steps 2–6 all pass |

---

### Part A — Build the Pre-PR Pipeline (15 min)

Create `.github/workflows/pre-pr.yml`:

```yaml
name: Pre-PR Pipeline

on: [pull_request]

jobs:
  pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: "Step 1 — Checkout"
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: "Step 2 — Linter (Ruff)"
        run: |
          pip install ruff
          ruff check src/app.py src/tests/test_app.py
          echo "✅ Step 2: Linter passed"

      - name: "Step 3 — Unit tests (UAT regression check)"
        run: |
          pip install -r requirements.txt
          pytest src/tests/test_app.py -v --tb=short
          echo "✅ Step 3: All existing tests pass"
        # Failure here = UAT regression. PR blocked.

      - name: "Step 4 — Eval gate (≥ 80% pass rate)"
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          npm install -g promptfoo
          promptfoo eval --output results.json
          python3 -c "
          import json, sys
          with open('results.json') as f:
              d = json.load(f)
          s = d['results']['stats']
          rate = s['successes'] / s['total'] * 100
          print(f'Eval pass rate: {rate:.1f}%')
          if rate < 80:
              print('BLOCKED: Eval pass rate below 80%')
              sys.exit(1)
          print('✅ Step 4: Eval gate passed')
          "

      - name: "Step 5 — Security scan"
        uses: github/super-linter@v5
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          VALIDATE_PYTHON_FLAKE8: true
          DEFAULT_BRANCH: main
          LINTER_RULES_PATH: /
          PYTHON_FLAKE8_CONFIG_FILE: .flake8

      - name: "Step 6 & 7 — Pipeline summary (PR may open)"
        if: success()
        run: |
          echo "════════════════════════════════════════════"
          echo "✅ ALL 6 CHECKS PASSED"
          echo "Step 7: PR draft may now be opened."
          echo "Include AI attribution in PR description."
          echo "════════════════════════════════════════════"
```

Also create a minimal `.flake8` to avoid Step 5 false positives:

```ini
[flake8]
max-line-length = 120
ignore = E501,W503
```

**Commit everything:**

```bash
git add .github/workflows/pre-pr.yml .flake8
git commit -m "ci: add 7-step pre-PR pipeline"
git push
```

---

### Part B — Test: Passing PR (5 min)

Your current `main` branch (with Labs 5–8 committed) should pass all steps.

Create a feature branch:

```bash
git checkout -b feature/lab9-pipeline-test
```

Add one small, clean change to `src/app.py` — for example, a comment at the end of the file:

```python
# Lab 9: 7-step pipeline verified
```

```bash
git add src/app.py
git commit -m "test: verify 7-step pipeline passes"
git push -u origin feature/lab9-pipeline-test
```

Open a PR on GitHub. Watch the Actions tab.

```
Step 2 (Linter):    □ Passed   □ Failed
Step 3 (Tests):     □ Passed   □ Failed
Step 4 (Eval gate): □ Passed   □ Failed
Step 5 (Security):  □ Passed   □ Failed
All 6 passed?:      □ Yes — PR opened   □ No — which step failed?
_________________________________________________________________
```

---

### Part C — Test: Blocking PR + Productization Checklist (5 min)

**Blocking test:** Go back to the PR. Edit `src/tests/test_app.py` on the PR branch — delete one test function. Commit to the PR branch.

```
Did Step 3 (unit tests) catch the deletion and block the PR?
□ Yes — blocked as expected
□ No — check if pytest is running correctly
```

Restore the test and re-push. Confirm PR becomes green again.

**Productization checklist:** Check each item for your Lab 5–8 work:

```
□ Code quality: Linter passes on all changed files
□ Test coverage: Test count increased, 0 tests removed, coverage up
□ Eval pass-rate: promptfoo 100% locally, ≥ 80% in CI
□ Security: GHAS scan runs — 0 high/critical findings
□ Documentation: PR description has AI attribution + UAT-protected functions
□ SKILL.md currency: DRI assigned, version pinned, deprecation policy written
□ Reviewer sign-off: (you will complete this in Lab 11 with a peer)

How many items are fully green?  ______ / 7
```

**Merge the clean PR when it passes all steps.**

```bash
git checkout main
git branch -d feature/lab9-pipeline-test
```

---

### ✅ LAB 9 GATE CHECKPOINT

- [ ] `.github/workflows/pre-pr.yml` committed with all 7 steps
- [ ] Passing PR demonstrated — all 6 checks green, PR opens
- [ ] Blocking PR demonstrated — Step 3 caught test deletion, PR blocked
- [ ] PR restored to clean state and merged
- [ ] Productization checklist completed — gaps identified

**Trainer/Lead sign-off:** _______________________ ✓
