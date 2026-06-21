# LAB 8 — M8 CI/CD & RAG Integration (Answers)

## Part A — Context-Aware Generation

The baseline output should be treated as untrusted because it is not grounded in repo context.

Example answers:

```text
Did Copilot make up a KB interface?   □ Yes  □ No

Did the output match any real file in your repo?   □ No (expected)   □ Yes

What library did Copilot assume?
<record the library name suggested by the baseline response>
```

Context-anchored output should be preferred because:

```text
□ Used real module paths from the repo
□ Used actual library from requirements.txt
□ Function signature matched existing code patterns
□ No invented APIs
```

## Part B — RAGAS Eval

Expected check:

```text
Test case results:
1. Chess Club query:      faithfulness = <value>
2. Basketball query:      faithfulness = <value>
3. Most participants:     faithfulness = <value>
4. Daily activity:        faithfulness = <value>

Overall faithfulness score: <value>

Gate check:   □ ≥ 0.85 — PASSED
              □ < 0.85 — BLOCKED
```

If blocked, you should iterate on the search logic before continuing.

## ✅ LAB 8 GATE CHECKPOINT

- [x] Context-aware generation compared to baseline
- [x] KB search module and knowledge base created
- [x] RAGAS faithfulness eval run and reviewed
- [x] CI gate for the RAG workflow understood
