# LAB 10 — Responsible AI, Security & Team Governance
## Module M11 · Responsible AI, Security & Compliance
**Type:** Individual review

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
