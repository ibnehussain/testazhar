
# LAB 4 — Core Coding Workflows & Mandatory git diff Review

## Part A — Feature Build: GET /activities/{name} Endpoint

### A1. Pre-flight Checks

- AI Scope Statement is written and signed off.
- `.github/copilot-instructions.md` is committed and pushed.
- Prompt Review Checklist is completed.
- Unneeded files are closed.
- The repo is on the correct branch before editing.

### A2. Scoped prompt notes

The scoped prompt should:
- identify the exact route: `GET /activities/{activity_name}`
- specify the exact location in the file
- require `HTTP 200` for valid names and `HTTP 404` for invalid names
- forbid changes to the existing locked routes

### A3. Mandatory git diff review

The correct review process is:
1. Run `git diff --stat HEAD`
2. Review `git diff src/app.py`
3. Confirm that only the intended endpoint was added
4. Re-run the test suite

### A4. Test results

The key verification command is:

```bash
pytest src/tests/test_app.py -v
```

Expected result after the endpoint work is:
- all existing tests continue to pass
- any new endpoint tests also pass

---

## Part B — Refactoring Danger Zone

The ACTIVITIES dictionary is part of the runtime data model for the API. Restructuring it without a precise plan would be risky because the locked routes depend on its current structure.

The correct response to a request like this is to decline the broad rewrite and ask for a smaller, test-backed proposal.

---

## Part C — Debug Lab

The bug in `calculate_capacity_remaining()` is caused by subtracting `len(current)` from `max_participants` when `max_participants` might be `None`. The correct fix is to guard the `None` case first.

---

## Part D — Danger Zone Checklist

- Scenario 1: REJECT if it changes a locked route.
- Scenario 2: REJECT if it renames shared logic used by protected routes.
- Scenario 3: REJECT if it replaces or deletes existing tests.
- Scenario 4: REJECT if it changes HTTP methods for an existing route.
- Scenario 5: REJECT AND REVERT if unexpected files appear in the diff.
