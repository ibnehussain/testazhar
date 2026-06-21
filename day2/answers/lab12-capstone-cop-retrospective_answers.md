# LAB 12 — Capstone & CoP Retrospective (Answers)

## Part A — Peer Demo

A correct demonstration sequence is:

```text
1. Show `.github/copilot-instructions.md`
2. Show `git diff --stat HEAD`
3. Show the SKILL.md
4. Show a passing PR in Actions
5. Show a blocked PR or explain which lab produced the block
```

Observer checklist sample:

```text
□ copilot-instructions.md has all 3 UAT-locked functions
□ git diff showed only expected files
□ SKILL.md has a CONSTRAINTS section
□ Passing PR shown
□ Blocked PR shown

Overall: Does the pipeline protect UAT?   □ Yes
```

## Part B — CoP KB Entry

Sample KB entry:

```text
Incident title:
Copilot suggestion weakened a test instead of adding coverage

What happened:
A prompt like "improve the test suite" could have caused existing assertions
or test structure to be changed instead of only adding new tests.

Root cause:
□ Test generation used WRITE instead of ADD

Prevention:
Gate: Coverage delta gate
How configured: block PRs if tests are removed or coverage drops

Would the 7-step pipeline have caught this?
□ Yes — at Step 3

SKILL.md update required?
□ Yes — add to CONSTRAINTS: never simplify or delete existing tests
DRI who will update: Tech Lead

CoP share:
API and QA teams
```

## Part C — 12-Layer Verification

Example final verification:

```text
Day 1 layers:
- AI Scope Statement ✓
- copilot-instructions.md ✓
- Scoped prompts ✓
- git diff review ✓

Day 2 layers:
- Coverage delta gate ✓
- SKILL.md constraints ✓
- Eval gate ✓
- 7-step pre-PR pipeline ✓
- Security scan ✓
- Human code review ✓
- Team AI policy ✓
- CoP KB ✓

Fully active layers: 12 / 12
```

## ✅ LAB 12 GATE CHECKPOINT

- [x] Peer demo completed
- [x] CoP KB entry completed
- [x] 12-layer stack verified
- [x] Sprint-1 action list recorded
