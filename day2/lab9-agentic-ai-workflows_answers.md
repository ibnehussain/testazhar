# LAB 9 — Agentic AI Workflows (Answers)

## Part A — Agent Mode Setup

Expected response:

```text
Are the 3 UAT-locked functions still listed?   □ Yes   □ No — update now
```

## Part B — HITL Review

Example safe review form:

```text
HITL REVIEW — IS IT SAFE TO APPROVE?
Files the agent proposes to modify:
1. src/app.py
2. src/tests/test_app.py
3. (optional) docs only

Any UAT-locked functions in the change list?
□ No — safe to proceed
□ Yes — REJECT

Does the plan touch src/static/ or any file outside the declared scope?
□ No
□ Yes — REDIRECT

Does the plan include any destructive action (DELETE, DROP, truncate)?
□ No
□ Yes — REJECT immediately

Are both src/app.py and src/tests/test_app.py in the plan?
□ Both listed

DECISION:   □ APPROVE
```

## Part C — Post-Execution Review

Expected checks:

```text
Files changed by the agent:
src/app.py
src/tests/test_app.py

Any unexpected file in the diff?   □ No (expected)   □ Yes — STOP

All original tests still passing?   □ Yes   □ No — which failed?
<record any failures>

New tests added by agent?   □ Yes — how many: <count>   □ No
```

Reflection:

```text
Did the agent RESPECT the copilot-instructions.md NEVER_MODIFY list?
□ Yes — it avoided all three UAT-locked functions
□ No — it touched: <record the exact file/function>
```

## ✅ LAB 9 GATE CHECKPOINT

- [x] Agent Mode enabled and verified
- [x] NEVER_MODIFY list reviewed before execution
- [x] HITL review completed before approval
- [x] Agent output reviewed for scope and safety
- [x] Tests checked after execution
