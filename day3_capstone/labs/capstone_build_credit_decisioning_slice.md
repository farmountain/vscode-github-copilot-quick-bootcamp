# Lab: Build the Credit Decisioning Slice

## Lab Overview

**Duration:** 3 hours  
**Difficulty:** Advanced  
**Prerequisites:** Completion of Day 1 and Day 2 labs

In this capstone lab, you will use **GitHub Copilot Agent Mode** to build a complete credit decisioning service with:

- FastAPI REST API (5 endpoints)
- Deterministic decision engine with reason codes
- Audit logging (JSONL format, no raw PII)
- Simple persistence (SQLite or file-based JSON)
- Comprehensive test suite
- Governance artifacts

---

## Learning Objectives

By the end of this lab, you will:

1. ✅ Use Copilot Agent Mode for multi-file, multi-module implementation
2. ✅ Implement banking-grade deterministic decision logic
3. ✅ Generate explainable reason codes for every decision
4. ✅ Create audit trails that protect sensitive data
5. ✅ Write comprehensive test suites (unit + API + end-to-end)
6. ✅ Produce governance artifacts (threat model, risk register)
7. ✅ Package evidence bundles for audit review

---

## Lab Architecture

You will build this structure:

```
src/day3/credit_decisioning/
├── __init__.py
├── app.py                 # FastAPI routes
├── models.py              # Pydantic models
├── validation.py          # Input validation
├── features.py            # Feature engineering (DTI, etc.)
├── rules_engine.py        # Scoring + reason codes
├── repository.py          # Persistence (SQLite or JSON)
├── audit.py               # JSONL audit logger
├── config.py              # Configuration
├── sample_data.py         # Synthetic data generator
├── demo_e2e.py            # End-to-end demo script
└── README.md

tests/day3/
├── test_rules_engine.py
├── test_repository.py
├── test_api_endpoints.py
└── test_end_to_end_scenarios.py
```

---

## Prerequisites

### 1. Install Dependencies

```powershell
pip install fastapi uvicorn pydantic pytest httpx
```

### 2. Verify Installation

```powershell
python -c "import fastapi, uvicorn, pydantic, pytest, httpx; print('Ready!')"
```

---

## Lab Phases

### Phase 1: Architecture and Requirements Review (15 min)

**Objective:** Understand the system before building.

**Tasks:**

1. Read [capstone_requirements.md](../capstone_requirements.md)
2. Review [capstone_architecture.md](../capstone_architecture.md)
3. Study the decision engine rules (scoring adjustments and reason codes)
4. Identify the 5 API endpoints you'll implement

**Key Questions:**

- What makes a decision "deterministic"?
- Why do we exclude raw PII from audit logs?
- How do reason codes enable explainability?

---

### Phase 2: Implement Core Modules (60 min)

**Objective:** Build the decision engine, features, and repository.

#### Task 2.1: Create Configuration Module

**File:** `src/day3/credit_decisioning/config.py`

**Copilot Prompt:**

```
Create a configuration module for the credit decisioning service.

Requirements:
- Define paths: AUDIT_LOG_PATH, DB_PATH, JSON_STORE_PATH
- Define decision thresholds: SCORE_APPROVE_THRESHOLD (70), SCORE_REFER_THRESHOLD (50)
- Define REPO_TYPE: "sqlite" or "json" (default: "sqlite")
- Support environment variable overrides using os.getenv()
- Create output directories if they don't exist

Use Path from pathlib. Ensure out/day3/ directory is created.
```

#### Task 2.2: Create Pydantic Models

**File:** `src/day3/credit_decisioning/models.py`

**Copilot Prompt:**

```
Create Pydantic models for the credit decisioning service.

Models needed:
1. ApplicationRequest (for POST /applications):
   - full_name: str
   - annual_income: float (must be > 0)
   - monthly_debt_payments: float (must be >= 0)
   - requested_amount: float (must be > 0)
   - employment_years: int (must be >= 0)
   - missed_payments_12m: int (must be >= 0)
   - address: str
   - email: EmailStr

2. ApplicationRecord (stored in repository):
   - application_id: str
   - All fields from ApplicationRequest
   - created_at: datetime

3. DecisionRecord (stored in repository):
   - decision_id: str
   - application_id: str
   - outcome: Literal["APPROVE", "REFER", "DECLINE"]
   - score: int
   - reason_codes: list[str]
   - timestamp: datetime

Use Pydantic validators to enforce constraints.
```

#### Task 2.3: Create Feature Engineering Module

**File:** `src/day3/credit_decisioning/features.py`

**Copilot Prompt:**

```
Create a feature engineering module for credit decisioning.

Functions needed:
1. calculate_dti(monthly_debt_payments: float, annual_income: float) -> float
   - Returns debt-to-income ratio: monthly_debt_payments / (annual_income / 12)

2. calculate_affordability_ratio(requested_amount: float, annual_income: float) -> float
   - Returns requested_amount / annual_income

3. derive_features(application: ApplicationRecord) -> dict
   - Returns a dict with: dti, affordability_ratio, annual_income, requested_amount, employment_years, missed_payments_12m

Include docstrings and type hints.
```

#### Task 2.4: Create Rules Engine

**File:** `src/day3/credit_decisioning/rules_engine.py`

**Copilot Prompt:**

```
Create a deterministic rules engine for credit decisioning.

Requirements:
- Start with baseline_score = 50
- Apply adjustments based on features:
  
  DTI adjustments:
  - dti < 0.36: +10, reason code "LOW_DTI"
  - dti >= 0.43: -15, reason code "HIGH_DTI"
  
  Payment history adjustments:
  - missed_payments_12m == 0: +10, reason code "CLEAN_PAYMENT_HISTORY"
  - missed_payments_12m in [1, 2]: -5, reason code "SOME_MISSED_PAYMENTS"
  - missed_payments_12m >= 3: -20, reason code "POOR_PAYMENT_HISTORY"
  
  Employment adjustments:
  - employment_years > 5: +10, reason code "STABLE_EMPLOYMENT"
  - employment_years in [2, 5]: +5, reason code "MODERATE_EMPLOYMENT"
  
  Credit exposure adjustments:
  - affordability_ratio < 0.30: +5, reason code "LOW_CREDIT_EXPOSURE"
  - affordability_ratio >= 0.50: -10, reason code "HIGH_CREDIT_EXPOSURE"

- Clip final score to [0, 100]
- Map score to outcome:
  - score >= 70: APPROVE, add "SCORE_APPROVE_BAND"
  - score >= 50 and < 70: REFER, add "SCORE_REFER_BAND"
  - score < 50: DECLINE, add "SCORE_DECLINE_BAND"

- Sort reason codes alphabetically for determinism

Function signature:
def compute_decision(features: dict) -> dict:
    # Returns: {"score": int, "outcome": str, "reason_codes": list[str]}
```

**Verification:**

```powershell
# Test with sample data
python -c "from src.day3.credit_decisioning.rules_engine import compute_decision; print(compute_decision({'dti': 0.30, 'affordability_ratio': 0.25, 'employment_years': 6, 'missed_payments_12m': 0}))"
```

Expected: High score, APPROVE outcome

---

### Phase 3: Implement Repository and Audit (45 min)

#### Task 3.1: Create Repository (Choose SQLite or JSON)

**File:** `src/day3/credit_decisioning/repository.py`

**Copilot Prompt (SQLite):**

```
Create a repository module using SQLite for persistence.

Requirements:
- Two tables: applications, decisions
- Functions:
  - create_application(app_request: ApplicationRequest) -> ApplicationRecord
    - Generate UUID4 for application_id
    - Insert into applications table
    - Return ApplicationRecord
  - get_application(application_id: str) -> Optional[ApplicationRecord]
  - create_decision(application_id: str, outcome: str, score: int, reason_codes: list[str]) -> DecisionRecord
    - Generate UUID4 for decision_id
    - Insert into decisions table
    - Return DecisionRecord
  - get_decision(decision_id: str) -> Optional[DecisionRecord]

- Use sqlite3 module
- Database path from config.DB_PATH
- Create tables if not exist (in init_db() function)
- Use parameterized queries (no SQL injection risk)
```

**Copilot Prompt (JSON files):**

```
Create a repository module using file-based JSON storage.

Requirements:
- Two directories: applications/, decisions/
- Functions:
  - create_application(app_request: ApplicationRequest) -> ApplicationRecord
    - Generate UUID4 for application_id
    - Save as applications/{application_id}.json
    - Return ApplicationRecord
  - get_application(application_id: str) -> Optional[ApplicationRecord]
    - Read from applications/{application_id}.json
  - create_decision(application_id: str, outcome: str, score: int, reason_codes: list[str]) -> DecisionRecord
    - Generate UUID4 for decision_id
    - Save as decisions/{decision_id}.json
    - Return DecisionRecord
  - get_decision(decision_id: str) -> Optional[DecisionRecord]
    - Read from decisions/{decision_id}.json

- Use json module and pathlib
- Storage path from config.JSON_STORE_PATH
- Create directories if not exist
```

#### Task 3.2: Create Audit Logger

**File:** `src/day3/credit_decisioning/audit.py`

**Copilot Prompt:**

```
Create an audit logger that writes decisions to JSONL format.

Requirements:
- Function: log_decision(application_id, decision_id, outcome, score, reason_codes, derived_features)
- Write to config.AUDIT_LOG_PATH
- Format: one JSON object per line (JSONL)
- Include fields: timestamp (ISO 8601), request_id (generated UUID), application_id, decision_id, outcome, score, reason_codes
- Include derived features: dti, annual_income, requested_amount, employment_years, missed_payments_12m
- EXCLUDE raw PII: full_name, address, email
- Append to file (create if not exists)
- Use json.dumps() and file.write()

Include a generate_request_id() helper that returns a UUID.
```

---

### Phase 4: Implement FastAPI Endpoints (60 min)

#### Task 4.1: Create FastAPI Application

**File:** `src/day3/credit_decisioning/app.py`

**Copilot Prompt:**

```
Create a FastAPI application with 5 endpoints for credit decisioning.

Endpoints:
1. GET /health
   - Returns: {"status": "ok"}

2. POST /applications
   - Request body: ApplicationRequest
   - Create application in repository
   - Return: {"application_id": str}
   - Status: 201 Created

3. GET /applications/{application_id}
   - Fetch application from repository
   - Return: ApplicationRecord
   - Status: 200 OK or 404 Not Found

4. POST /applications/{application_id}/decision
   - Fetch application from repository (404 if not found)
   - Derive features using features.derive_features()
   - Compute decision using rules_engine.compute_decision()
   - Create decision in repository
   - Log decision using audit.log_decision() (with features, not raw PII)
   - Return: DecisionRecord
   - Status: 201 Created

5. GET /decisions/{decision_id}
   - Fetch decision from repository
   - Return: DecisionRecord
   - Status: 200 OK or 404 Not Found

Import:
- FastAPI, HTTPException
- models, repository, features, rules_engine, audit, config

Initialize repository (call init_db() if using SQLite).

Use Pydantic models for request/response validation.
```

#### Task 4.2: Verify API Works

```powershell
# Start API
uvicorn src.day3.credit_decisioning.app:app --reload

# In another terminal, test health endpoint
Invoke-WebRequest -Uri http://127.0.0.1:8000/health
```

Expected: `{"status": "ok"}`

---

### Phase 5: Implement Tests (45 min)

#### Task 5.1: Unit Tests for Rules Engine

**File:** `tests/day3/test_rules_engine.py`

**Copilot Prompt:**

```
Create pytest unit tests for the rules engine.

Test cases:
1. test_low_dti_adjustment: dti < 0.36 → score adjustment +10, reason code "LOW_DTI"
2. test_high_dti_adjustment: dti >= 0.43 → score adjustment -15, reason code "HIGH_DTI"
3. test_clean_payment_history: missed_payments_12m == 0 → +10, "CLEAN_PAYMENT_HISTORY"
4. test_poor_payment_history: missed_payments_12m >= 3 → -20, "POOR_PAYMENT_HISTORY"
5. test_stable_employment: employment_years > 5 → +10, "STABLE_EMPLOYMENT"
6. test_low_credit_exposure: affordability < 0.30 → +5, "LOW_CREDIT_EXPOSURE"
7. test_high_credit_exposure: affordability >= 0.50 → -10, "HIGH_CREDIT_EXPOSURE"
8. test_approve_outcome: score >= 70 → outcome "APPROVE", reason code "SCORE_APPROVE_BAND"
9. test_decline_outcome: score < 50 → outcome "DECLINE", reason code "SCORE_DECLINE_BAND"
10. test_determinism: same features → same score, outcome, reason codes (call twice, assert equal)

Import: from src.day3.credit_decisioning.rules_engine import compute_decision
```

#### Task 5.2: API Tests

**File:** `tests/day3/test_api_endpoints.py`

**Copilot Prompt:**

```
Create pytest API tests using FastAPI TestClient.

Test cases:
1. test_health_check: GET /health → 200, {"status": "ok"}
2. test_create_application: POST /applications with valid data → 201, application_id returned
3. test_create_application_invalid: POST /applications with negative income → 422
4. test_get_application: POST application, then GET /applications/{id} → 200, data matches
5. test_get_application_not_found: GET /applications/{invalid_id} → 404
6. test_compute_decision: POST application, POST decision, verify outcome and reason codes
7. test_get_decision: POST application, POST decision, GET /decisions/{id} → 200
8. test_get_decision_not_found: GET /decisions/{invalid_id} → 404

Use FastAPI TestClient:
from fastapi.testclient import TestClient
from src.day3.credit_decisioning.app import app

client = TestClient(app)
```

#### Task 5.3: End-to-End Tests

**File:** `tests/day3/test_end_to_end_scenarios.py`

**Copilot Prompt:**

```
Create end-to-end scenario tests for the credit decisioning service.

Test cases:
1. test_full_workflow_approve: Submit safe application → compute decision → verify APPROVE outcome
2. test_full_workflow_decline: Submit risky application → compute decision → verify DECLINE outcome
3. test_audit_log_entry: Submit application, compute decision, verify audit log contains entry
4. test_audit_log_no_pii: Submit application, compute decision, verify audit log does NOT contain full_name, address, email

Use TestClient. Read audit log file (config.AUDIT_LOG_PATH) and parse JSONL.
```

#### Task 5.4: Run Tests

```powershell
pytest tests/day3/ -v
```

Expected: All tests pass.

---

### Phase 6: Generate Sample Data and Demo (30 min)

#### Task 6.1: Create Sample Data Generator

**File:** `src/day3/credit_decisioning/sample_data.py`

**Copilot Prompt:**

```
Create a sample data generator for credit applications.

Requirements:
- Generate 10 sample applications
- Include variety:
  - 3 "safe" (high income, low debt, no missed payments) → expect APPROVE
  - 3 "risky" (low income, high debt, missed payments) → expect DECLINE
  - 2 "borderline" (moderate risk) → expect REFER
  - 2 "edge cases" (e.g., DTI exactly 0.36, score exactly 70)
- Save to out/day3/sample_requests.json
- If run as script (__name__ == "__main__"), print samples and save file

Use realistic but synthetic data (names like "Alice Safe", "Bob Risky").
```

**Run:**

```powershell
python -m src.day3.credit_decisioning.sample_data
```

#### Task 6.2: Create End-to-End Demo Script

**File:** `src/day3/credit_decisioning/demo_e2e.py`

**Copilot Prompt:**

```
Create an end-to-end demo script that uses the API.

Requirements:
- Import httpx (for HTTP requests)
- Assume API is running at http://127.0.0.1:8000
- Submit 3 sample applications (one safe, one risky, one borderline)
- For each:
  - POST /applications
  - POST /applications/{id}/decision
  - Print outcome, score, reason codes
- Use httpx.post() and httpx.get()
- Print formatted output with headers and summaries

If __name__ == "__main__", run the demo.
```

**Run:**

```powershell
# In one terminal: start API
uvicorn src.day3.credit_decisioning.app:app --reload

# In another terminal: run demo
python src/day3/credit_decisioning/demo_e2e.py
```

Expected: Demo submits applications and prints decisions.

---

### Phase 7: Governance Artifacts (30 min)

**Note:** Governance artifacts are created via Prompt D3-2 (see [day3_prompts.md](../prompts/day3_prompts.md)).

Tasks:

1. Create threat model using prompt D3-2
2. Create risk register using prompt D3-2
3. Update requirements traceability matrix

These are separate from the code implementation but are part of the capstone deliverables.

---

## Evaluation Criteria

Your capstone will be evaluated on:

### 1. Completeness (25 points)

- [ ] All 5 API endpoints implemented and working
- [ ] Decision engine with reason codes
- [ ] Audit logger (JSONL format)
- [ ] Repository (SQLite or JSON)
- [ ] Sample data generator
- [ ] E2E demo script

### 2. Correctness (25 points)

- [ ] All tests pass (unit + API + end-to-end)
- [ ] Decisions are deterministic (same input → same output)
- [ ] Reason codes match scoring logic
- [ ] Audit log format correct

### 3. Explainability (15 points)

- [ ] Reason codes present for every decision
- [ ] Reason codes are accurate and stable
- [ ] Decision logic traceable to requirements

### 4. Safety (15 points)

- [ ] Audit log excludes raw PII (full_name, address, email)
- [ ] Input validation prevents invalid data
- [ ] No hardcoded secrets or credentials

### 5. Traceability (10 points)

- [ ] Requirements map to code modules
- [ ] Requirements map to tests
- [ ] Traceability matrix complete

### 6. Governance (10 points)

- [ ] Threat model documented
- [ ] Risk register documented
- [ ] Runbook enables verification

---

## Troubleshooting

### Issue: Copilot Agent generates incomplete code

**Solution:** Break down prompts into smaller tasks. Use follow-up prompts like "Now add error handling" or "Add type hints and docstrings."

### Issue: Tests fail with import errors

**Solution:** Verify directory structure. Add `__init__.py` files to make directories Python packages.

### Issue: Audit log is empty

**Solution:** Check that decisions are being computed. Verify `audit.log_decision()` is called in `app.py` POST /applications/{id}/decision endpoint.

### Issue: Non-deterministic reason codes

**Solution:** Ensure reason codes are sorted (e.g., `sorted(reason_codes)` in rules engine).

---

## Next Steps

After completing this lab:

1. Run all tests: `pytest tests/day3/ -v`
2. Start API and run demo: `python src/day3/credit_decisioning/demo_e2e.py`
3. Review audit log: `Get-Content out/day3/audit_log.jsonl`
4. Create evidence bundle: `python scripts/day3_collect_evidence.py`
5. Review governance artifacts: threat_model.md, risk_register.md

---

## Bonus Challenges (Optional)

1. **Add validation endpoint:** `POST /applications/{id}/validate` that checks application data without computing decision
2. **Add decision history:** `GET /applications/{id}/decisions` returns all decisions for an application
3. **Add reason code explanations:** Create a mapping of reason codes to human-readable explanations
4. **Add API versioning:** `/v1/applications`, `/v2/applications`
5. **Add OpenAPI tags:** Group endpoints by category (applications, decisions)

---

**Congratulations!** You've built a banking-grade credit decisioning system with GitHub Copilot Agent Mode.

**Related Documents:**

- [Capstone Requirements](../capstone_requirements.md)
- [Capstone Architecture](../capstone_architecture.md)
- [Capstone Runbook](../capstone_runbook.md)
- [Day 3 Prompts](../prompts/day3_prompts.md)
