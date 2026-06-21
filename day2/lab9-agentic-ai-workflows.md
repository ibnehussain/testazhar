# LAB 8 — Agentic AI Workflows with Copilot
## Module M9 · Agentic AI Workflows
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

### Part A — Enable and Configure Agent Mode

**In VS Code or Codespaces:**

1. Open Copilot Chat
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

### Part B — Review the Agent Plan BEFORE Approving

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

### Part C — Post-Execution Review

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
