# LAB 11 — Capstone & CoP Retrospective
## Module M12 · Productivity Metrics & End-to-End Workflow

---

### Objective

Demonstrate your complete end-to-end workflow to a peer. Document one AI code-quality incident from today's labs using the CoP KB template. Confirm all 12 protection layers are active.

---

### Part A — Peer Demo

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
