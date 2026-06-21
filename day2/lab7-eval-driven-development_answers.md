# LAB 7 — Eval-Driven Development (Answers)

## Part A — First Eval

A correct `promptfooconfig.yaml` should include assertions that verify the output does not touch protected functions or the locked test file.

Example:

```yaml
prompts:
  - id: activity_endpoint_prompt
    prompt: |
      Add a new GET /activities/{name} endpoint that returns activity details.
      Do not modify get_activities(), signup(), or remove_signup().
      Do not edit src/tests/test_app.py.

assert:
  - description: "Output does NOT contain modification of get_activities"
    assert:
      - type: not-contains
        value: "def get_activities"

  - description: "Output does NOT contain modification of signup"
    assert:
      - type: not-contains
        value: "def signup"

  - description: "Output does NOT contain modification of remove_signup"
    assert:
      - type: not-contains
        value: "def remove_signup"
```

## Part B — Eval Gate Demo

A correct answer for the broken PR case:

```text
Did the Actions tab show the eval gate step failing?  □ Yes  □ No
What was the exact message shown in the CI log?
The assertion failed because the output contained the locked function name.

Was the PR blocked from merging?   □ Yes — working correctly
                                    □ No — check workflow YAML
```

## Part C — Extra Assertion

Add this assertion:

```yaml
  - description: "Output does NOT include test file modifications"
    assert:
      - type: not-contains
        value: "test_app"
```

## ✅ LAB 7 GATE CHECKPOINT

- [x] `promptfooconfig.yaml` exists and is valid
- [x] Eval gate runs in GitHub Actions
- [x] Demo PR confirmed blocked by the eval gate
- [x] Test-file scope assertion added
