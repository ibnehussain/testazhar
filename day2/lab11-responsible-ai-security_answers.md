# LAB 11 — Responsible AI, Security & Team Governance (Answers)

## Part A — Security Risks

### Snippet 1

**Security risk:** SQL injection.

**Safe version:**

```python
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))
```

### Snippet 2

**Security risk:** Arbitrary file read / path traversal.

**Safe version:**

```python
from pathlib import Path

safe_dir = Path("uploads")
requested = Path(request.args.get("file", ""))

if requested.is_absolute() or any(part == ".." for part in requested.parts):
    return "Invalid file path", 400

file_path = safe_dir / requested
if not file_path.resolve().is_relative_to(safe_dir.resolve()):
    return "Invalid file path", 400

with file_path.open("rb") as f:
    return f.read()
```

### Snippet 3

**Security risk:** Hardcoded secret / weak secret handling.

**Safe version:**

```python
import os

ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
if request.headers.get("Authorization") != ADMIN_TOKEN:
    return "Unauthorized", 401
```

## Part B — GHAS

Correct answer format:

```text
GHAS status:   □ Enabled — scanning active
               □ Not enabled — ask trainer for environment-specific instructions

Has any alert been raised on your current code?   □ No   □ Yes — describe:
<record findings here>
```

## Part C — Team AI Policy

A strong policy should include these items:

```text
Section 1: Acceptance criteria
- review the diff before accepting any suggestion
- confirm only approved files are changed
- run relevant tests before merging

Section 2: Mandatory gates
- coverage gate
- eval gate
- security scan
- human review

Section 3: UAT protection rules
- locked functions: get_activities(), signup(), remove_signup()
- locked file: src/tests/test_app.py
- PR-required update approval

Section 4: Gate bypass conditions
- only with explicit lead approval and documented reason

Section 5: Post-incident process
- rollback
- root cause analysis
- update KB entry
- share with CoP
```

## ✅ LAB 11 GATE CHECKPOINT

- [x] Security snippets reviewed
- [x] Safe versions written
- [x] GHAS status checked
- [x] Team AI policy drafted
