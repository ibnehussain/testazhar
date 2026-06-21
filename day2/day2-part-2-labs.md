
---

# LAB 9 — The 7-Step Pre-PR Pipeline
## Module M10 · Productizing Copilot Workflows
**Duration:** 25 minutes
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

---

---

# LAB 10 — Responsible AI, Security & Team Governance
## Module M11 · Responsible AI, Security & Compliance
**Duration:** 15 minutes
**Type:** Individual review → Group workshop (pairs or threes)

---

### Objective

Identify security risks in AI-generated code patterns. Draft a team AI policy covering the five mandatory sections. Verify the security scan is active for your repo.

---

### Part A — Security Code Review (5 min)

Below are three code snippets that Copilot commonly generates when given vague prompts. For each, identify the security risk and write the safe version.

---

**Snippet 1:**

```python
# Copilot generated this when asked to "query users by email"
query = f"SELECT * FROM users WHERE email = '{email}'"
cursor.execute(query)
```

```
Security risk: _________________________________________________

Safe version:
_________________________________________________________________
_________________________________________________________________
```

---

**Snippet 2:**

```python
# Copilot generated this when asked to "add file download"
filename = request.args.get("file")
with open(f"uploads/{filename}") as f:
    return f.read()
```

```
Security risk: _________________________________________________

Safe version:
_________________________________________________________________
_________________________________________________________________
```

---

**Snippet 3:**

```python
# Copilot generated this when asked to "add admin endpoint"
ADMIN_TOKEN = "secret-admin-key-2024"
if request.headers.get("Authorization") == ADMIN_TOKEN:
    return admin_dashboard()
```

```
Security risk: _________________________________________________

Safe version:
_________________________________________________________________
_________________________________________________________________
```

**Check:** Do any of these patterns appear anywhere in your `src/app.py`? If yes, fix them now and commit before proceeding.

```
Any of these patterns found in src/app.py?   □ No — all clean
                                              □ Yes — fixed and committed
```

---

### Part B — Verify GHAS Security Scan (2 min)

The security scan runs as Step 5 in your pre-PR pipeline. Verify it is active:

1. Go to your repo on GitHub
2. Go to **Security** tab → **Code scanning**
3. Verify GitHub Advanced Security is enabled

```
GHAS status:   □ Enabled — scanning active
               □ Not enabled — ask trainer for environment-specific instructions

Has any alert been raised on your current code?   □ No   □ Yes — describe:
_________________________________________________________________
```

---

### Part C — Draft Your Team AI Policy (8 min)

**Work in pairs or threes.** Draft the five mandatory sections of your team's AI policy for the Mergington activities API. Be specific — write actual values, not descriptions of what you would put.

```
╔══════════════════════════════════════════════════════════════════════╗
║  TEAM AI POLICY — Mergington Activities API                         ║
║  Version: 1.0   DRI: [your name]   Review date: [3 months out]      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Section 1: Acceptance criteria                                      ║
║  Before accepting any Copilot suggestion, the developer must:        ║
║  □ _______________________________________________________________   ║
║  □ _______________________________________________________________   ║
║  □ _______________________________________________________________   ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Section 2: Mandatory gates (non-negotiable, even under pressure)    ║
║  □ _______________________________________________________________   ║
║  □ _______________________________________________________________   ║
║  □ _______________________________________________________________   ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Section 3: UAT protection rules                                     ║
║  Always-locked functions: get_activities(), signup(), remove_signup()║
║  Always-locked files: src/tests/test_app.py                          ║
║  Who can update this list: ______________________________________    ║
║  How to update: PR required? □ Yes  □ No   Approved by: ___________ ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Section 4: Gate bypass conditions                                   ║
║  Under what circumstances may a gate be bypassed?                    ║
║  _______________________________________________________________      ║
║  Who approves: ________________   What is logged: ________________   ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  Section 5: Post-incident process                                    ║
║  If AI-induced regression reaches production:                        ║
║  Step 1: ____________________________________________________        ║
║  Step 2: ____________________________________________________        ║
║  Step 3: ____________________________________________________        ║
║  Step 4: ____________________________________________________        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

### ✅ LAB 10 GATE CHECKPOINT

- [ ] All 3 security code snippets reviewed — risks identified and safe versions written
- [ ] No vulnerable patterns found in `src/app.py` (or found and fixed)
- [ ] GHAS status verified in Security tab
- [ ] Team AI policy drafted — all 5 sections have specific, non-placeholder content
- [ ] Section 2 (Mandatory gates) includes: coverage gate, eval gate, security scan, human review
- [ ] Section 5 (Post-incident) includes: rollback → root cause → KB entry → CoP share

**Trainer/Lead sign-off:** _______________________ ✓

---

---

# LAB 11 — Capstone & CoP Retrospective
## Module M12 · Productivity Metrics & End-to-End Workflow
**Duration:** 15 minutes
**Type:** Peer demo + Individual retrospective

---

### Objective

Demonstrate your complete end-to-end workflow to a peer. Document one AI code-quality incident from today's labs using the CoP KB template. Confirm all 12 protection layers are active.

---

### Part A — Peer Demo (7 min)

Swap with the person next to you. Each person gets 3 minutes to demonstrate. The question is not "is the code perfect?" — it is "does the pipeline protect UAT?"

**Demonstrator runs through this sequence:**

```
Sequence to demo (3 minutes):
─────────────────────────────────────────────────────────────────

1. Show your .github/copilot-instructions.md
   "My NEVER_MODIFY list includes: [read the 3 functions]"

2. Show a recent git diff --stat HEAD
   "Only these files changed. No UAT-locked files were touched."

3. Show your SKILL.md
   "The CONSTRAINTS section inherited these rules to any developer
   who uses the skill."

4. Show a passing PR in the Actions tab
   "All 6 pipeline steps passed. The PR opened automatically."

5. Show a blocked PR in the Actions tab (or describe which lab produced it)
   "The pipeline blocked this PR at Step [N] because [reason]."
─────────────────────────────────────────────────────────────────
```

**Observer fills in:**

```
Observer: _______________________

□ copilot-instructions.md has all 3 UAT-locked functions
□ git diff showed only expected files — no UAT-locked file touched
□ SKILL.md has a CONSTRAINTS section with functions named
□ Passing PR shown — all steps green
□ Blocked PR shown — specific step that blocked it: _______________

Overall: Does the pipeline protect UAT?   □ Yes   □ Partially   □ No

One thing the demonstrator could strengthen:
_________________________________________________________________
```

---

### Part B — CoP Knowledge Base Entry (8 min)

Every AI-induced incident from this training is a learning opportunity. Document one real incident from Labs 5–9 using the KB template below.

If nothing went wrong in your labs, use the Lab 5 danger demo (where "Improve the test suite" would have silently removed test assertions) as your incident.

```
══════════════════════════════════════════════════════════════════
  COMMUNITY OF PRACTICE — AI INCIDENT KB ENTRY
══════════════════════════════════════════════════════════════════

Incident title:
_________________________________________________________________

What happened:
[Describe specifically: which prompt, which file was touched, what
would have changed if not caught]

_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

Root cause:
Which gate was missing or bypassed?
□ No AI Scope Statement
□ copilot-instructions.md absent or stale
□ Prompt used red-flag word without constraint
□ git diff review was skipped
□ Test generation used WRITE instead of ADD
□ Eval gate was not yet in place
□ HITL review skipped in Agent Mode
□ Gate was bypassed under pressure
□ Other: ______________________________________________

Prevention:
Which gate, once in place, would have caught this before UAT?

Gate: ____________________   How configured: ___________________

Would the 7-step pipeline from Lab 9 have caught this?
□ Yes — at Step: ______   □ No — additional gate needed: ________

SKILL.md update required?
□ No — existing SKILL.md constraint already covers this
□ Yes — add to CONSTRAINTS section: ___________________________
         DRI who will update: _________________________________

CoP share:
Which other teams could encounter this same pattern?
_________________________________________________________________

Action: Share this KB entry with: ______________________________
══════════════════════════════════════════════════════════════════
```

---

### Part C — Complete 12-Layer Stack Verification

Mark each layer as active (✓), partially active (~), or not yet built (✗):

```
Day 1 — Manual protection layers:
  Layer 1   AI Scope Statement       □ ✓  □ ~  □ ✗
  Layer 2   copilot-instructions.md  □ ✓  □ ~  □ ✗
  Layer 3   Scoped prompts           □ ✓  □ ~  □ ✗
  Layer 4   git diff review          □ ✓  □ ~  □ ✗

Day 2 — Automated protection layers:
  Layer 5   Coverage delta gate      □ ✓  □ ~  □ ✗
  Layer 6   SKILL.md constraints     □ ✓  □ ~  □ ✗
  Layer 7   Eval gate (promptfoo)    □ ✓  □ ~  □ ✗
  Layer 8   7-step pre-PR pipeline   □ ✓  □ ~  □ ✗
  Layer 9   Security scan (GHAS)     □ ✓  □ ~  □ ✗
  Layer 10  Human code review        □ ✓  □ ~  □ ✗
  Layer 11  Team AI policy           □ ✓  □ ~  □ ✗
  Layer 12  CoP knowledge base       □ ✓  □ ~  □ ✗

Fully active layers: ______ / 12

Layers still partial or missing — your sprint-1 action list:
_________________________________________________________________
_________________________________________________________________
```

---

### ✅ LAB 11 GATE CHECKPOINT (Final Gate of Day 2)

- [ ] Peer demo completed — observer signed the checklist above
- [ ] CoP KB entry completed — incident named, root cause identified, prevention gate specified
- [ ] SKILL.md update decision made (yes/no, with reason)
- [ ] 12-layer stack verified — score recorded above
- [ ] Sprint-1 action list written for any partial/missing layers

**Trainer/Lead sign-off:** _______________________ ✓

---

---

# DAY 2 — END OF TRAINING REFLECTION

**Complete before leaving. Takes 3 minutes.**

```
1. Today I activated these protection layers:

   Layer 5 — Coverage delta gate       □ Active in CI
   Layer 6 — SKILL.md constraints      □ SKILL.md created, peer-reviewed
   Layer 7 — Eval gate (promptfoo)     □ Running in GitHub Actions
   Layer 8 — 7-step pre-PR pipeline    □ All 7 steps running
   Layer 9 — Security scan             □ GHAS active
   Layer 10 — Human code review        □ Peer demo completed
   Layer 11 — Team AI policy           □ All 5 sections drafted
   Layer 12 — CoP knowledge base       □ First KB entry written

──────────────────────────────────────────────────────────────────

2. The single most important habit I will take back to my team:

   ______________________________________________________________
   ______________________________________________________________

3. The gate my team is most likely to skip under pressure:

   ______________________________________________________________

   What I will do to prevent this:

   ______________________________________________________________
   ______________________________________________________________

4. First action I will take tomorrow morning:

   ______________________________________________________________

──────────────────────────────────────────────────────────────────

5. The 4 principles — write them from memory (no peeking):

   1. AI ________________; humans are ________________.
   2. ________________ but ________________.
   3. ________________ before you ________________.
   4. ________________ it ________________.

   (Answers: accelerates / accountable · Trust / verify ·
    Scope / generate · Catch / early)
```

---

---

# REFERENCE — Day 2 Quick Cards

Cut out and keep.

```
┌────────────────────────────────────────────┐
│  DAY 2 PROTECTION GATES — AT A GLANCE      │
│                                            │
│  Layer 5:  Coverage delta gate             │
│            pytest --cov → CI blocks drop   │
│                                            │
│  Layer 6:  SKILL.md CONSTRAINTS            │
│            DRI + version + deprecation     │
│                                            │
│  Layer 7:  Eval gate (promptfoo)           │
│            ≥ 80% pass rate, not-contains   │
│            for every UAT-locked function   │
│                                            │
│  Layer 8:  7-step pre-PR pipeline          │
│            Linter → Tests → Eval →         │
│            GHAS → Docs → PR opens          │
│                                            │
│  Layer 9:  Security scan (GHAS)            │
│            0 high/critical — PR blocked    │
│                                            │
│  Layers 10–12: Human gates                 │
│            Review · Policy · CoP KB        │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  HITL DECISION FRAMEWORK                   │
│                                            │
│  APPROVE — plan is within scope,           │
│    no UAT-locked files in change list      │
│                                            │
│  REDIRECT — mostly right but touches too   │
│    many files; narrow scope, re-approve    │
│                                            │
│  REJECT — plan includes UAT-locked         │
│    functions, a DELETE, or out-of-scope    │
│    changes; reject and re-scope task       │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  EVAL ASSERTION TYPES                      │
│                                            │
│  contains: "value"                         │
│    → output MUST include this string       │
│    Use for: function names, libraries,     │
│    HTTP status codes, route patterns       │
│                                            │
│  not-contains: "value"                     │
│    → output must NOT include this          │
│    Use for: UAT-locked function names,     │
│    test file names, forbidden patterns     │
│                                            │
│  80% threshold = at most 1 of 5 can fail  │
│  Critical assertions (not-contains for     │
│  UAT-locked) should be the first ones     │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  CoP INCIDENT FORMULA                      │
│                                            │
│  What happened                             │
│  → Root cause: which gate was missing?     │
│  → Prevention: which gate catches this?    │
│  → SKILL.md update: yes/no + what          │
│  → CoP share: who else needs to know?      │
│                                            │
│  AI incident → KB entry → SKILL.md update  │
│  → CoP share → next team is protected      │
└────────────────────────────────────────────┘
```

---