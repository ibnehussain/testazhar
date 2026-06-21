# LAB 10 — The 7-Step Pre-PR Pipeline (Answers)

## Part A — Pipeline Setup

Your pipeline should include steps for:

- checkout
- setup Python
- setup Node
- linting
- unit tests
- eval gate
- security scan
- summary / PR readiness

Example response:

```text
Step 2 (Linter):    □ Passed   □ Failed
Step 3 (Tests):     □ Passed   □ Failed
Step 4 (Eval gate): □ Passed   □ Failed
Step 5 (Security):  □ Passed   □ Failed
All 6 passed?:      □ Yes — PR opened   □ No — which step failed?
```

## Part B — Passing PR

If the PR is green, the correct answer is:

```text
All 6 passed: Yes — PR opened
```

## Part C — Blocking PR

A correct blocking answer:

```text
Did Step 3 (unit tests) catch the deletion and block the PR?
□ Yes — blocked as expected
□ No — check if pytest is running correctly
```

Productization checklist example:

```text
□ Code quality: Linter passes on changed files
□ Test coverage: count increased, 0 tests removed
□ Eval pass-rate: promptfoo passes locally and in CI
□ Security: GHAS scan runs and reports no critical issues
□ Documentation: PR description includes AI attribution
□ SKILL.md is current and reviewed
□ Reviewer sign-off completed
```

## ✅ LAB 10 GATE CHECKPOINT

- [x] `pre-pr.yml` built and committed
- [x] Passing PR demonstrated
- [x] Blocking PR demonstrated
- [x] Productization checklist completed
