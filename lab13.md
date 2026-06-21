# GitHub Copilot Training — Day 1 Lab Workbook
**Participant Copy · UAT Protection Focus**

---

> **How to use this workbook**
> Each lab has a clear objective, step-by-step instructions, answer spaces, and a gate checkpoint you must complete before moving to the next module. Work through every step in order. Do not skip the "weak prompt" runs — experiencing the danger is as important as learning the protection.
>
> **Repo(fork/clone):** `https://github.com/ibnehussain/testazhar.git`
> **Branch:** Work on `main` unless a lab tells you otherwise
> **Environment:** VS Code(Locally) or GitHub Codespaces (https://github.com/codespaces)

---

---

# LAB 1 — AI Scope Statement
## Module M1 · ADLC Mindset & UAT Protection Challenge
**Duration:** 20-30 minutes
**Type:** Individual → Pair review → Group discussion

---

### Objective

Write an AI Scope Statement that correctly identifies what Copilot may and may not touch for a given task ticket. Understand why specificity in the UAT-locked list is the most critical field.

---

### Background

Before you open Copilot for any task, you must write an AI Scope Statement. It answers three questions in 3 minutes:

1. What is Copilot being asked to build?
2. What files and modules is Copilot NOT allowed to modify?
3. What tests must remain passing after this session?

This is Layer 1 of the 12-layer UAT Protection Stack.

---

### The Codebase You Are Working In

The Mergington High School activities API has this structure:

```
src/
├── app.py              ← Flask API (3 UAT-passing routes live here)
├── static/             ← Frontend HTML/CSS/JS — do not touch
└── tests/
    └── test_app.py     ← few existing passing tests — UAT-locked
```

**The three UAT-locked routes in `src/app.py`:**

| Function | Route | Status |
|---|---|---|
| `get_activities()` | `GET /activities` | UAT-PASSED — locked |
| `signup()` | `POST /activities/{name}/signup` | UAT-PASSED — locked |
| `remove_signup()` | `DELETE /activities/{name}/signup` | UAT-PASSED — locked |

---

### Task Ticket

```
Ticket #47 — Assigned to you
─────────────────────────────────────────────────────
Feature: Single Activity Detail Endpoint

Add a new endpoint to the Mergington activities API:
  GET /activities/{activity_name}

It should return the full details of that activity as JSON
with HTTP 200, or return HTTP 404 with an error message
if the activity name does not exist.

DO NOT change any existing endpoints.
─────────────────────────────────────────────────────
```

---

### Step 1 — Write Your AI Scope Statement (7-10 min)

Complete every field. Be specific — "all existing files" is not a valid UAT-locked list.

```
┌─────────────────────────────────────────────────────────┐
│  AI SCOPE STATEMENT                                     │
├─────────────────────────────────────────────────────────┤
│  Task:                                                  │
│                                                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  In scope (files Copilot MAY touch):                    │
│                                                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  UAT-locked (files Copilot must NEVER modify):          │
│                                                         │
│                                                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Tests (must remain passing after this session):        │
│                                                         │
│                                                         │
├─────────────────────────────────────────────────────────┤
│  Reviewed by: ________________________  Date: _______   │
└─────────────────────────────────────────────────────────┘
```

---

### Step 2 — Pair Review (5 min)

Swap your scope statement with the person next to you. Review theirs using this checklist:

```
Reviewer: _______________________

□ Is the Task field specific enough to prevent ambiguity?
□ Does the UAT-locked list name SPECIFIC functions/files?
  (not "all existing code" or "the whole app")
□ Are all three UAT-passing route functions listed by name?
□ Is test_app.py explicitly listed as UAT-locked?
□ Are the test requirements specific?

What would you tighten? Write one suggestion here:
________________________________________________________________
________________________________________________________________
```

---

### Step 3 — Self-Assessment

After the pair review, compare your scope statement against the model answer revealed. Complete this reflection:

```
Q1. Was your UAT-locked list specific enough?
    □ Yes — I named specific functions
    □ Partially — I named files but not functions
    □ No — I wrote something broad like "all existing files"

Q2. Did you miss any of the three UAT-locked functions?
    □ I listed all three: get_activities(), signup(), remove_signup()
    □ I missed: _________________________________________________

Q3. Did you include test_app.py in the UAT-locked list?
    □ Yes
    □ No — I will add it now

Q4. What would happen if a developer started a Copilot session
    with no scope statement?
    ____________________________________________________________
    ____________________________________________________________
```

---

### ✅ M1 GATE CHECKPOINT

**You may not proceed to Lab 2 until this gate is passed.**

Your scope statement must be:
- [ ] Written (not blank)
- [ ] UAT-locked list names specific functions — not "all existing files"
- [ ] All three UAT-locked route functions listed by name
- [ ] `src/tests/test_app.py` listed as UAT-locked
- [ ] Reviewed by the trainer or lead

**(Optional)Lead sign-off:** _______________________ ✓

---

---

# LAB 2 — Copilot Foundations & copilot-instructions.md
## Module M2 · GitHub Copilot Foundations
**Duration:** 60 minutes
**Type:** Individual lab with trainer demos

---

### Objective

Set up GitHub Copilot, understand what its context window sees, and write a `copilot-instructions.md` file that encodes your UAT protection rules as machine-readable constraints.

---

### Part A — IDE Setup (20 min)

#### A1. Open VS Code

1. Clone the repo --> 'https://github.com/ibnehussain/testazhar.git'

```

```

#### A2. Verify Copilot extension is installed and you are signed-in.

Look for the GitHub Copilot extension in Extensions Tab.

```
```
#### A3. Trigger an Inline Suggestion (observe only — do NOT accept)

1. Open `src/app.py`
2. Scroll to the bottom of the file, below the last route function
3. Press Enter twice to create a blank line
4. Type this comment:

```python
# Add a new route that returns a welcome message for the school
```

5. Press Enter and wait 1–2 seconds

```
What did Copilot suggest?
______________________________________________________________
______________________________________________________________

Did it suggest touching any existing function?  □ Yes  □ No

Press ESCAPE now — do NOT accept the suggestion.
```

#### A4. Open Copilot Chat and Ask What It Sees

1. Click the Copilot Chat icon in the left sidebar (Ctrl+Alt+I)
2. Type this exactly(Ask Mode):

```
What files can you currently see in this project?
```

3. Record the answer:

```
Files Copilot reports seeing:
______________________________________________________________
______________________________________________________________
______________________________________________________________

Does it know which routes have passed UAT?    □ Yes  □ No
Does it know what your test results are?      □ Yes  □ No

What does this tell you about why copilot-instructions.md matters?
______________________________________________________________
______________________________________________________________
```

---

### Part B — Write copilot-instructions.md (30 min)

#### B1. Understand the Context Window First

Before writing the file, review this table:

| What Copilot CAN see | What Copilot CANNOT see |
|---|---|
| Open files in your editor | Your test results |
| Recently viewed files | Which functions passed UAT |
| `copilot-instructions.md` (once created) | Your team's agreements |
| Repository files (with full context) | Your sprint board or ticket comments |

**Key insight:** The only way to make your UAT protection rules visible to Copilot is to write them in `copilot-instructions.md`.

#### B2. Create the File

In the Codespaces terminal:

```bash
mkdir -p .github
touch .github/copilot-instructions.md
```

Open the file in the editor. It will be blank.

#### B3. Write the Instructions — Complete Every Section

Fill in this template. Replace every `[placeholder]` with real content from the Mergington codebase.

```markdown
# Project: Mergington High School Activities API
# Copilot Instructions

## Purpose
[Write one sentence describing what this codebase does]

## NEVER_MODIFY — UAT-locked code
The following have passed User Acceptance Testing and must NOT be
modified by any Copilot suggestion. If Copilot suggests changes to
these, reject the suggestion immediately.

### UAT-locked route functions (src/app.py)
- `[function name 1]` — [route it handles]
- `[function name 2]` — [route it handles]
- `[function name 3]` — [route it handles]

### UAT-locked test file
- `src/tests/test_app.py` — ALL existing test functions are locked.
  Never delete, rename, or modify any existing test function.

## Scope of Copilot assistance
Copilot may help with:
- [What new features are in scope for this training session]
- [What kind of tests are acceptable]
- Documentation for new functions only

## Constraints
- [Constraint 1 — e.g. about response format]
- [Constraint 2 — e.g. about HTTP status codes]
- [Constraint 3 — e.g. about not adding new imports]
- Never suggest changes that reduce test coverage
- Never remove or rename any existing public API endpoint
```

**Completed file should look like this (fill in the blanks, then check):**

```
□ Purpose section — 1 sentence describing the app
□ NEVER_MODIFY section — lists all 3 UAT-locked functions by name
□ test_app.py explicitly listed as locked
□ Scope section — describes what new code IS allowed
□ Constraints section — at least 3 specific rules
```

#### B4. Save and Commit

```bash
git add .github/copilot-instructions.md
git commit -m "Add copilot-instructions.md with NEVER_MODIFY list"
git push
```

#### B5. Test — Does Copilot Respect the Instructions?

**Test 1: Ask Copilot to modify a locked function**

In Copilot Chat, type:

```
Refactor the signup() function in src/app.py to improve its error handling.
```

What did Copilot say or suggest?

```
□ It refused or added a disclaimer about NEVER_MODIFY
□ It still suggested changes to signup()
□ Mixed — it suggested some changes

If it still suggested changes to signup() — what does that tell you?
______________________________________________________________
______________________________________________________________
(Hint: The answer is why git diff review is mandatory — it's coming in Lab 4)
```

**Test 2: Ask Copilot about the file without the instructions file**

In Codespaces terminal, temporarily rename the file:

```bash
mv .github/copilot-instructions.md .github/copilot-instructions.md.bak
```

Now ask Copilot Chat the same question:

```
Refactor the signup() function in src/app.py to improve its error handling.
```

Compare: does Copilot behave differently without the instructions file?

```
With instructions file: ________________________________________
Without instructions file: _____________________________________

Restore the file now:
```

```bash
mv .github/copilot-instructions.md.bak .github/copilot-instructions.md
```

---

### ✅ M2 GATE CHECKPOINT

**You may not proceed to Lab 3 until this gate is passed.**

- [ ] Copilot is active and verified in your Codespace
- [ ] `.github/copilot-instructions.md` exists and is committed
- [ ] The NEVER_MODIFY section lists all 3 UAT-locked functions by name
- [ ] `src/tests/test_app.py` is listed as locked
- [ ] You have tested the file and observed Copilot's response

**(Optional)Lead sign-off:** _______________________ ✓

---

---

# LAB 3 — Prompting for Safe Code Generation
## Module M3 · Prompting for Code Generation
**Duration:** 35 minutes
**Type:** Individual → Pair comparison

---

### Objective

Identify red flags in vague prompts, rewrite them using the four-part anatomy (Task / Scope / Constraint / Format), and observe the difference in Copilot's output between weak and strong prompts.

---

### The Four-Part Prompt Anatomy

Every safe Copilot prompt has these four parts:

```
TASK        — Exactly what to build (specific, bounded)
SCOPE       — Exactly where in the codebase the code should go
              AND what must not be touched
CONSTRAINT  — Coding rules, libraries, status codes, patterns to follow
FORMAT      — How the output should look (function name, docstring, etc.)
```

---

### Prompt Review Checklist

Before running any prompt, verify all five criteria:

```
□ Does the prompt specify exactly WHAT to build?
□ Does the prompt specify what NOT to touch (UAT-locked list)?
□ Does the prompt reference test requirements?
□ Is the scope FUNCTION-LEVEL or smaller (not module-level)?
□ Does the prompt avoid red-flag words?
  (refactor, improve, clean up, rewrite, make better, update the module)
```

---

### Part A — Identify the Red Flags (10 min)

For each prompt below, identify which red flags are present and explain what could go wrong in the Mergington codebase.

---

**Prompt 1:**
```
Improve the activities endpoint.
```

Red flags present:
```
□ "Improve" — undefined improvement allows Copilot to change anything
□ "activities endpoint" — module-level, touches ALL routes
□ No constraint on what NOT to touch
□ No format specified

What would Copilot likely do to our UAT-locked routes?
_________________________________________________________________
```

---

**Prompt 2:**
```
Refactor app.py to add error handling.
```

Red flags present:
```
□ "Refactor" — broad restructuring permission
□ "app.py" — file-level scope, all functions in scope
□ "add error handling" — Copilot decides where and how
□ No UAT-locked list mentioned

Which UAT-locked function is most at risk from this prompt and why?
_________________________________________________________________
```

---

**Prompt 3:**
```
Write tests for the new feature.
```

Red flags present:
```
□ "Write tests" without specifying ADD (not replace)
□ No mention of test_app.py being locked
□ "new feature" — ambiguous, Copilot may include existing features
□ No assertion requirements specified

What is the worst-case outcome from this prompt?
_________________________________________________________________
```

---

**Prompt 4:**
```
Make the signup endpoint more robust.
```

Red flags present:
```
□ "Make more robust" — undefined scope
□ signup() is UAT-LOCKED — this prompt directly targets it
□ No constraint prevents touching test_app.py
□ "More robust" may mean changing return types or status codes

Why is this prompt especially dangerous for this codebase?
_________________________________________________________________
```

---

**Prompt 5:**
```
Fix the calculate_capacity_remaining function in app.py.
```

Red flags present (this one is closer — spot the remaining issues):
```
□ Better: targets a specific function
□ Still missing: _______________________________________________
□ Still missing: _______________________________________________
□ Still missing: _______________________________________________
```

---

### Part B — Rewrite the Prompts (15 min)

Rewrite each of the five prompts using the four-part anatomy. Your rewritten prompt must pass all five checklist criteria.

The task for all five is in the context of the Mergington app. Use the UAT-locked list from your scope statement in Lab 1.

---

**Rewrite of Prompt 1** — Add a single-activity detail endpoint

```
[Your rewrite — must include Task, Scope, Constraint, Format]




Task:




Scope:




Constraint:




Format:



```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

**Rewrite of Prompt 2** — Add error handling to the `get_activity` function ONLY

```
Task:




Scope:




Constraint:




Format:



```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

**Rewrite of Prompt 3** — Add tests for the new `get_activity` endpoint

```
Task:




Scope:




Constraint:




Format:



```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

**Rewrite of Prompt 4** — This one you must NOT rewrite

The `signup()` function is UAT-locked. The correct response to this ticket is:

```
What should you do instead of running Prompt 4?

__________________________________________________________________
__________________________________________________________________

Write the response you would send to the requester:

"Hi [name], I cannot use Copilot to modify signup() because ________
_________________________________________________________________
_________________________________________________________________"
```

---

**Rewrite of Prompt 5** — Fix the `calculate_capacity_remaining` bug (safe to modify)

```
Task:




Scope:




Constraint:




Format:



```

**Checklist:** □ What to build  □ What NOT to touch  □ Tests  □ Function-level  □ No red flags

---

### Part C — Run Both Versions and Compare (10 min)

Pick ONE of your rewrites (Prompts 1, 2, or 5 — not 4). Run both the original weak prompt AND your rewritten prompt in Copilot Chat. Do NOT accept either suggestion.

**Weak prompt result:**

```
Files Copilot's suggestion would touch (guess from the output):
__________________________________________________________________

Would it have touched any UAT-locked function?  □ Yes  □ No  □ Maybe
```

**Strong prompt result:**

```
Files Copilot's suggestion would touch:
__________________________________________________________________

Would it have touched any UAT-locked function?  □ Yes  □ No  □ Maybe
```

**What was the key difference?**

```
__________________________________________________________________
__________________________________________________________________
```

---

### ✅ M3 GATE CHECKPOINT

**Complete the Prompt Review Checklist for your Rewrite 1 before proceeding to Lab 4.**

```
PROMPT REVIEW CHECKLIST — Final Check
────────────────────────────────────────────────────────────
Prompt being reviewed: [Rewrite 1 — Add get_activity endpoint]

□ Specifies WHAT to build (function name, route, response shape)
□ Specifies what NOT to touch (names the 3 locked functions)
□ References test requirements (existing tests must stay green)
□ Function-level scope (not "update app.py" or "fix the routes")
□ No red-flag words (refactor / improve / clean / rewrite)

Ready to run?   □ YES — all 5 checked   □ NO — revise first
────────────────────────────────────────────────────────────
```

**Trainer/Lead sign-off:** _______________________ ✓

---