# Day 1 Prompts Playbook

**Quick reference**: Copy-paste prompts for generating Day 1 code and content.

---

## Overview

This playbook contains all the prompts referenced in the Day 1 training materials. These prompts are designed to be pasted directly into **GitHub Copilot Agent Mode** in VS Code to generate lab code, tests, and supporting materials.

**Important**: Always review generated code before running. Apply the verification checklist from Session 1.3.

---

## Setup: How to Use These Prompts

1. **Open VS Code** in your training repository
2. **Open GitHub Copilot Chat** (sidebar icon or `Ctrl+Shift+I` / `Cmd+Shift+I`)
3. **Enable Agent Mode** by typing `@workspace` in your prompt
4. **Paste a prompt** from this playbook
5. **Review the proposed plan** and approve
6. **Review all file changes** in the diff view
7. **Run tests** to verify correctness

---

## Prompt D1-1: Implement Lab 1 Code (Data Quality Rules Engine)

**Purpose**: Generate all code for Lab 1 (transaction validation system)

**When to use**: After completing Session 1.2, ready to build Lab 1

```
You are a GitHub Copilot coding agent.

Implement Lab 1 starter solution code for a "Data Quality Rules Engine" using Python.

Constraints:
- No MCP.
- Synthetic data only.
- Design for auditability and deterministic results.
- Keep it simple, readable, and test-first.

Create this code structure:
 /src/day1/data_quality/
   __init__.py
   models.py               (TransactionRecord dataclass / pydantic model)
   rules.py                (individual rule functions, each returns structured findings)
   engine.py               (applies rules, aggregates findings, produces summary)
   io.py                   (load CSV, write results JSON)
   cli.py                  (CLI: validate a CSV and output JSON report)
   README.md               (how to run)
 /tests/day1/
   test_data_quality_rules.py
   test_data_quality_engine.py

Rules to implement (minimum):
- Required fields present (txn_id, account_id, amount, currency, txn_ts)
- amount > 0
- currency is ISO-like 3 uppercase letters (simple regex)
- txn_ts parseable as ISO-8601, not in the far future (configurable threshold)
- account_id format check (simple pattern e.g. ACC followed by digits)
- Duplicate txn_id detection

Outputs:
- A JSON report listing findings per record + overall summary counts by severity (ERROR/WARN).
- Deterministic ordering of findings.

Add synthetic sample file generation:
- Create /src/samples/synthetic_data_generator.py (if not already) with a function to generate a small transactions CSV including a few invalid rows for demo.
- Ensure /src/samples/sample_transactions.csv exists (small sample).

Verification:
- Add pytest tests covering each rule and end-to-end engine output.
- Add instructions in /src/day1/data_quality/README.md with commands:
  - python -m src.samples.synthetic_data_generator
  - python -m src.day1.data_quality.cli --input ... --output ...
  - pytest -q

Finally:
- Update /tests/README.md to mention how to run Day 1 tests.
- Summarize created files and how to run them.

Proceed now.
```

**Expected outcome**:
- Complete Lab 1 codebase generated
- All tests passing
- README with usage instructions

**Verification steps**:
1. Run: `python -m src.samples.synthetic_data_generator`
2. Run: `python -m src.day1.data_quality.cli --input src/samples/sample_transactions.csv --output output/dq_report.json`
3. Run: `pytest tests/day1/test_data_quality*.py -v`
4. Review output JSON report

---

## Prompt D1-2: Implement Lab 2 Code (Risk Scoring Service)

**Purpose**: Generate all code for Lab 2 (credit risk scoring API)

**When to use**: After completing Lab 1, ready to build Lab 2

```
You are a GitHub Copilot coding agent.

Implement Lab 2 starter solution code for an "Explainable Risk Scoring Service" using Python + FastAPI.

Constraints:
- No MCP.
- Synthetic data only.
- Explicit explainability: score must include reason codes.
- Add an audit log (local file JSON lines) for each scoring request (no sensitive data; only synthetic fields).
- Deterministic scoring.

Create this code structure:
 /src/day1/risk_scoring_service/
   __init__.py
   app.py                 (FastAPI app, routes)
   models.py              (Pydantic request/response)
   scoring.py             (pure scoring logic returns score + reason codes)
   audit.py               (append JSONL entries with timestamp, request_id, decision, reasons)
   config.py              (paths, thresholds, environment defaults)
   README.md              (how to run)
 /tests/day1/
   test_risk_scoring.py   (unit tests for scoring logic)
   test_risk_api.py       (FastAPI tests using TestClient)

API:
- GET /health
- POST /score
Request fields (synthetic): application_id, annual_income, debt, employment_years, missed_payments_12m, requested_amount
Response: risk_score (0-100), risk_band (LOW/MEDIUM/HIGH), reason_codes[], request_id

Scoring approach (simple rules, deterministic):
- Start at baseline 50
- Adjust based on debt-to-income, missed payments, employment years, requested_amount
- Clip to 0..100
- Map to risk_band thresholds
- Provide reason codes for each adjustment (e.g. "HIGH_DTI", "RECENT_MISSED_PAYMENTS", "LOW_TENURE")

Audit log:
- Write JSON Lines to /src/day1/risk_scoring_service/audit_log.jsonl by default
- Each entry includes: ts, request_id, application_id, score, band, reason_codes
- Keep it minimal and synthetic

Verification:
- Provide commands in README.md:
  - uvicorn src.day1.risk_scoring_service.app:app --reload
  - curl example POST
  - pytest -q

Finally:
- Update TRAINING_TOC.md if needed to link new README.
- Summarize created files and how to run.

Proceed now.
```

**Expected outcome**:
- Complete Lab 2 codebase generated
- FastAPI application running
- All tests passing
- Swagger/OpenAPI docs available at /docs

**Verification steps**:
1. Run: `uvicorn src.day1.risk_scoring_service.app:app --reload --port 8000`
2. Open browser: http://localhost:8000/docs
3. Test endpoint: `curl -X POST http://localhost:8000/score -H "Content-Type: application/json" -d '{"application_id":"APP-001","annual_income":75000,"debt":15000,"employment_years":5,"missed_payments_12m":0,"requested_amount":20000}'`
4. Run: `pytest tests/day1/test_risk*.py -v`
5. Check audit log: `cat src/day1/risk_scoring_service/audit_log.jsonl`

---

## Prompt D1-3: Add VS Code Tasks for Day 1

**Purpose**: Create VS Code tasks for one-click verification

**When to use**: After Labs 1 and 2 are complete

```
Update .vscode/tasks.json to add Day 1 tasks:
- "Day1: Generate Synthetic Data" (runs synthetic_data_generator.py)
- "Day1: Run Data Quality CLI Demo" (runs the data quality CLI against sample CSV and writes output)
- "Day1: Run Tests" (pytest -q)
- "Day1: Run Risk API" (uvicorn command)
- "Verify-All (Day1)" that runs: generate data -> tests (and optionally a quick CLI demo)

Constraints:
- No MCP.
- Support Windows + Mac/Linux (use OS-specific command blocks where needed).
Also update .vscode/START_HERE.md to mention these Day 1 tasks.
Summarize your changes.
```

**Expected outcome**:
- `.vscode/tasks.json` updated with Day 1 tasks
- Can run tasks via Terminal > Run Task menu
- `.vscode/START_HERE.md` updated

**Verification steps**:
1. Open VS Code Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Type "Tasks: Run Task"
3. Verify Day 1 tasks appear in the list
4. Run "Verify-All (Day1)" task

---

## Prompt D1-4: Add Copilot CLI Mini-Bootcamp

**Purpose**: Create documentation for GitHub Copilot CLI usage

**When to use**: After main Day 1 content is complete (optional enhancement)

```
Create /day1_foundations/session1_2_copilot_cli_mini_bootcamp.md

Include:
- What GitHub Copilot CLI is used for in this training
- Safe usage rules (no sensitive data)
- 6 short exercises (5 minutes each) using:
  - gh copilot suggest (for a command)
  - gh copilot explain (to explain a command)
  - using --target shell when relevant
- Use examples aligned to Day 1 labs:
  - running pytest
  - finding files
  - grepping logs
  - formatting code
- Add troubleshooting tips (auth, missing extension, PATH)
Update /day1_foundations/README.md and /TRAINING_TOC.md to link this mini-bootcamp.
Proceed now.
```

**Expected outcome**:
- New mini-bootcamp document created
- Exercises for practicing Copilot CLI
- Updated navigation links

---

## Quick Prompts for Common Lab Tasks

### Generate a Pydantic Model

```
Create a Pydantic model for [description].

[Context]
[Describe the use case]

[Constraints]
- Use Pydantic v2
- Include field validation
- Use appropriate types (Decimal for money, datetime for timestamps)

[Criteria]
Fields:
- [field_name]: [type] ([description, validation rules])
- ...

Include docstring and field descriptions for API documentation.
```

### Generate Unit Tests

```
Create pytest unit tests for [module/function].

[Context]
[Describe what the code does]

[Constraints]
- Use pytest framework
- AAA pattern (Arrange, Act, Assert)
- Descriptive test names

[Criteria]
Test cases to cover:
- Happy path: [describe]
- Edge cases: [describe]
- Error cases: [describe]

Include fixtures for common test data.
```

### Generate API Endpoint

```
Create a FastAPI endpoint for [purpose].

[Context]
[Describe the business need]

[Constraints]
- Use FastAPI
- Use Pydantic for validation
- Include error handling

[Criteria]
Endpoint: [METHOD] [/path]
Request: [describe request model]
Response: [describe response model]
Business logic: [describe]

Include docstring for Swagger documentation.
```

### Generate Documentation

```
Create a README for [module/service].

[Context]
[Describe what the code does]

[Criteria]
Include:
- Overview
- Features
- Installation/dependencies
- Usage examples (with commands)
- Architecture (brief)
- Testing instructions
- Example input/output

Use markdown formatting with code blocks.
```

---

## Advanced Prompting Tips

### Tip 1: Be Specific About File Structure

Instead of:
> "Create a rules engine"

Use:
> "Create src/rules.py with functions: check_amount(), check_currency(), check_timestamp(). Each function takes a Transaction and returns ValidationFinding or None."

### Tip 2: Reference Existing Code

```
Using the Transaction model in #file:src/models.py, create a validation function that checks...
```

### Tip 3: Specify Test Requirements

Always add:
> "Include pytest tests in tests/test_[module].py covering happy path, edge cases, and error cases."

### Tip 4: Request Documentation

Always add:
> "Include docstrings with examples. Create README.md with usage instructions and commands."

### Tip 5: Enforce Constraints

Be explicit:
> "Must be deterministic (same input → same output). Use Decimal for money (not float). No external API calls."

---

## Verification Checklist (Apply to All Generated Code)

After running any prompt, verify:

### Functional Correctness
- [ ] Does the code do what the prompt specified?
- [ ] Do all tests pass?
- [ ] Are edge cases handled?

### Code Quality
- [ ] Is the code readable and well-structured?
- [ ] Are there docstrings and type hints?
- [ ] Is it idiomatic Python?

### Banking/Compliance
- [ ] No hardcoded credentials or secrets?
- [ ] No PII in logs?
- [ ] Is behavior deterministic (if required)?
- [ ] Are errors handled gracefully?

### Testing
- [ ] Do unit tests cover core logic?
- [ ] Do integration tests cover workflows?
- [ ] Is test coverage >80%?

### Documentation
- [ ] Is there a README?
- [ ] Are usage examples provided?
- [ ] Are commands copy-pasteable?

---

## Troubleshooting

### If Copilot generates incorrect code:

1. **Review the prompt**: Was it specific enough?
2. **Add constraints**: Be more explicit about requirements
3. **Provide examples**: Show expected input/output
4. **Reference context**: Use `#file:` to point to existing code
5. **Iterate**: Use multi-turn conversation to refine

### If tests fail:

1. **Read the error**: What's actually failing?
2. **Check imports**: Are all dependencies installed?
3. **Verify data**: Is test data correct?
4. **Re-prompt**: Ask Copilot to fix the specific failing test

### If code doesn't match requirements:

1. **Be more specific**: Add explicit acceptance criteria
2. **Use examples**: "For input X, expect output Y"
3. **Break it down**: Generate one function at a time
4. **Review incrementally**: Test each piece before moving on

---

## Additional Resources

* [Session 1.2: Prompting in VS Code](../session1_2_prompting_in_vscode.md) - Detailed prompting techniques
* [Lab 1: Data Quality Rules Engine](../labs/lab1_data_quality_rules_engine.md) - Complete lab instructions
* [Lab 2: Risk Scoring Service](../labs/lab2_simple_risk_scoring_service.md) - Complete lab instructions
* [GitHub Copilot Documentation](https://docs.github.com/en/copilot)

---

## Summary: Day 1 Prompt Workflow

1. **Plan**: Define requirements using Paul-Elder framework
2. **Prompt**: Use 3C framework (Context, Constraints, Criteria)
3. **Generate**: Run prompt in Agent Mode
4. **Review**: Check diffs carefully
5. **Test**: Run tests and verify output
6. **Iterate**: Refine if needed
7. **Document**: Ensure README and docs are clear

**Remember**: AI is your assistant, you're the lead. Always review, always test, always verify.

---

**Navigation**:
* [Back to Day 1 README](../README.md)
* [Session 1.2: Prompting in VS Code](../session1_2_prompting_in_vscode.md)
