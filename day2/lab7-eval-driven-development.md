# LAB 7 — Eval-Driven Development
## Module M7 · Eval-Driven Development (EDD)
**Type:** Individual lab

---

### Objective

Use a `promptfooconfig.yaml` that validates your Copilot prompt before you use it in production. Add the eval gate to GitHub Actions so it blocks PRs automatically.

---

### Background: Why EDD?

Manual review fails in three ways: inconsistency, speed pressure, and lag. EDD flips the order — you define what "correct" looks like **before** writing the code. The pipeline enforces it automatically, on every PR, regardless of whether anyone remembers.

**The EDD principle:** Write the eval before you build the system. If the eval passes, the system is correct. If it fails, the PR is blocked.

---

### Part A — Write Your First Eval

**Step 1:** Verify promptfooconfig.yaml file exists in you repo



### Part B — Add the Eval Gate to GitHub Actions

**Step 1:** Verify `.github/workflows/eval.yml` file exists


**Step 2:** Verify the gate works with a test PR

Create a branch with a deliberately broken prompt (change the `not-contains` assertion value to something that WILL be in the output):

```bash
git checkout -b test/eval-gate-demo
```

Edit `promptfooconfig.yaml`. In any assertion, change `not-contains` to `contains`. This forces the assertion to look for the UAT-locked function name, which will fail:

Example:

```yaml
  - description: "Output does NOT contain modification of get_activities"
    assert:
      - type: contains
        value: "def get_activities"yz"
```

Push and open a PR:

```bash
git add promptfooconfig.yml
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

### Part C — Add One More Assertion

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

- [ ] `.github/workflows/eval.yml` committed and pushing to `main` triggers the gate
- [ ] Demo PR confirmed blocked by the eval gate
- [ ] PR cleaned up — demo branch deleted
- [ ] Custom assertion added for test-file scope

**Trainer/Lead sign-off:** _______________________ ✓
