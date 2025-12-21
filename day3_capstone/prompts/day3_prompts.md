# Day 3 Copilot Agent Prompts

## Overview

This document contains **copy-paste prompts** for use with **GitHub Copilot Agent Mode** in VS Code. These prompts are designed to build the Day 3 capstone: a Credit Decisioning Slice.

**How to use:**

1. Open VS Code with GitHub Copilot enabled
2. Open Copilot Chat (`Ctrl+Shift+I` or `Cmd+Shift+I`)
3. Switch to **Agent Mode** (look for agent icon or use `@workspace` scope)
4. Copy and paste the prompts below **exactly as written**
5. Review generated code before accepting
6. Run verification commands after each prompt

---

## Prompt Sequence

Execute prompts in this order:

1. **D3-0:** Generate Day 3 documentation (DONE - you're reading the docs)
2. **D3-1:** Implement capstone code
3. **D3-2:** Generate governance artifacts
4. **D3-3:** Add VS Code tasks
5. **D3-4:** Create evidence bundle

---

## Prompt D3-1: Implement Capstone Code

### D3-1a: Create Configuration Module

```
You are a GitHub Copilot coding agent.

Create the configuration module for the Day 3 credit decisioning service.

Constraints:
- No MCP.
- Banking-safe (synthetic data only).
- Professional code with type hints and docstrings.

Create file: src/day3/credit_decisioning/config.py

Requirements:
- Use pathlib.Path for all paths
- Define default paths:
  - AUDIT_LOG_PATH = Path("out/day3/audit_log.jsonl")
  - DB_PATH = Path("out/day3/credit_decisioning.db")
  - JSON_STORE_PATH = Path("out/day3/data")
- Define decision thresholds:
  - SCORE_APPROVE_THRESHOLD = 70
  - SCORE_REFER_THRESHOLD = 50
- Define REPO_TYPE = "sqlite" (or "json")
- Support environment variable overrides using os.getenv()
- Create output directories (out/day3/) if they don't exist
- Add a setup_directories() function that creates all necessary directories

Proceed now.
```

**Verification:**

```powershell
python -c "from src.day3.credit_decisioning.config import AUDIT_LOG_PATH, DB_PATH, SCORE_APPROVE_THRESHOLD; print('Config loaded successfully')"
```

---

### D3-1b: Create Pydantic Models

```
You are a GitHub Copilot coding agent.

Create Pydantic models for the Day 3 credit decisioning service.

Constraints:
- No MCP.
- Banking-safe.
- Use Pydantic v2 syntax if available, otherwise v1.

Create file: src/day3/credit_decisioning/models.py

Models needed:

1. ApplicationRequest (for POST /applications input):
   - full_name: str
   - annual_income: float (validator: must be > 0)
   - monthly_debt_payments: float (validator: must be >= 0)
   - requested_amount: float (validator: must be > 0)
   - employment_years: int (validator: must be >= 0)
   - missed_payments_12m: int (validator: must be >= 0)
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
   - score: int (validator: must be 0-100)
   - reason_codes: list[str]
   - timestamp: datetime

Use Pydantic Field with gt (greater than) and ge (greater than or equal) for numeric constraints.

Add Config class with json_encoders for datetime if needed.

Proceed now.
```

**Verification:**

```powershell
python -c "from src.day3.credit_decisioning.models import ApplicationRequest, ApplicationRecord, DecisionRecord; print('Models loaded successfully')"
```

---

### D3-1c: Create Feature Engineering Module

```
You are a GitHub Copilot coding agent.

Create feature engineering module for credit decisioning.

Constraints:
- No MCP.
- Deterministic only (no randomness).
- Professional code with type hints, docstrings, and examples.

Create file: src/day3/credit_decisioning/features.py

Functions needed:

1. calculate_dti(monthly_debt_payments: float, annual_income: float) -> float
   """Calculate debt-to-income ratio.
   
   Args:
       monthly_debt_payments: Monthly debt obligations
       annual_income: Annual income
   
   Returns:
       DTI ratio (monthly debt / monthly income)
   """
   Formula: monthly_debt_payments / (annual_income / 12)

2. calculate_affordability_ratio(requested_amount: float, annual_income: float) -> float
   """Calculate credit exposure as % of annual income.
   
   Returns:
       requested_amount / annual_income
   """

3. derive_features(application_data: dict) -> dict
   """Derive all features needed for scoring.
   
   Args:
       application_data: Dict with keys: annual_income, monthly_debt_payments, 
                        requested_amount, employment_years, missed_payments_12m
   
   Returns:
       Dict with: dti, affordability_ratio, annual_income, requested_amount,
                 employment_years, missed_payments_12m
   """
   Use calculate_dti() and calculate_affordability_ratio().

Include docstrings with examples.

Proceed now.
```

**Verification:**

```powershell
python -c "from src.day3.credit_decisioning.features import calculate_dti, derive_features; print(calculate_dti(1000, 60000)); print(derive_features({'annual_income': 60000, 'monthly_debt_payments': 1000, 'requested_amount': 15000, 'employment_years': 5, 'missed_payments_12m': 0}))"
```

---

### D3-1d: Create Rules Engine

```
You are a GitHub Copilot coding agent.

Create a deterministic rules engine for credit decisioning with explainable reason codes.

Constraints:
- No MCP.
- Completely deterministic (same input → same output).
- Reason codes must be sorted alphabetically for consistency.

Create file: src/day3/credit_decisioning/rules_engine.py

Requirements:

Function: compute_decision(features: dict) -> dict

Algorithm:
1. Start with baseline_score = 50
2. Initialize empty list: reason_codes = []

3. DTI adjustments:
   - If dti < 0.36: score += 10, reason_codes.append("LOW_DTI")
   - Elif dti >= 0.43: score -= 15, reason_codes.append("HIGH_DTI")

4. Payment history adjustments:
   - If missed_payments_12m == 0: score += 10, reason_codes.append("CLEAN_PAYMENT_HISTORY")
   - Elif missed_payments_12m in [1, 2]: score -= 5, reason_codes.append("SOME_MISSED_PAYMENTS")
   - Elif missed_payments_12m >= 3: score -= 20, reason_codes.append("POOR_PAYMENT_HISTORY")

5. Employment adjustments:
   - If employment_years > 5: score += 10, reason_codes.append("STABLE_EMPLOYMENT")
   - Elif employment_years >= 2: score += 5, reason_codes.append("MODERATE_EMPLOYMENT")

6. Credit exposure adjustments:
   - If affordability_ratio < 0.30: score += 5, reason_codes.append("LOW_CREDIT_EXPOSURE")
   - Elif affordability_ratio >= 0.50: score -= 10, reason_codes.append("HIGH_CREDIT_EXPOSURE")

7. Clip score: final_score = max(0, min(100, score))

8. Map score to outcome:
   - If final_score >= 70: outcome = "APPROVE", reason_codes.append("SCORE_APPROVE_BAND")
   - Elif final_score >= 50: outcome = "REFER", reason_codes.append("SCORE_REFER_BAND")
   - Else: outcome = "DECLINE", reason_codes.append("SCORE_DECLINE_BAND")

9. Sort reason codes alphabetically: reason_codes = sorted(reason_codes)

10. Return: {"score": final_score, "outcome": outcome, "reason_codes": reason_codes}

Input features dict must contain:
- dti: float
- affordability_ratio: float
- employment_years: int
- missed_payments_12m: int

Use type hints. Add docstring with examples.

Proceed now.
```

**Verification:**

```powershell
python -c "from src.day3.credit_decisioning.rules_engine import compute_decision; result = compute_decision({'dti': 0.30, 'affordability_ratio': 0.25, 'employment_years': 6, 'missed_payments_12m': 0}); print(f'Score: {result[\"score\"]}, Outcome: {result[\"outcome\"]}, Reasons: {result[\"reason_codes\"]}')"
```

Expected: Score 85, Outcome APPROVE

---

### D3-1e: Create Repository (SQLite Option)

```
You are a GitHub Copilot coding agent.

Create a repository module using SQLite for persistence.

Constraints:
- No MCP.
- Use sqlite3 standard library (no external DB dependencies).
- Parameterized queries (no SQL injection risk).

Create file: src/day3/credit_decisioning/repository.py

Requirements:

1. Use config.DB_PATH for database location

2. Function: init_db() -> None
   - Create tables if not exist:
     - applications table: application_id TEXT PRIMARY KEY, full_name TEXT, annual_income REAL, monthly_debt_payments REAL, requested_amount REAL, employment_years INTEGER, missed_payments_12m INTEGER, address TEXT, email TEXT, created_at TEXT
     - decisions table: decision_id TEXT PRIMARY KEY, application_id TEXT, outcome TEXT, score INTEGER, reason_codes TEXT (JSON array as string), timestamp TEXT

3. Function: create_application(app_request: ApplicationRequest) -> ApplicationRecord
   - Generate application_id using uuid.uuid4()
   - Insert into applications table
   - Set created_at to current datetime (ISO format)
   - Return ApplicationRecord

4. Function: get_application(application_id: str) -> Optional[ApplicationRecord]
   - Query applications table
   - Return ApplicationRecord or None if not found

5. Function: create_decision(application_id: str, outcome: str, score: int, reason_codes: list[str]) -> DecisionRecord
   - Generate decision_id using uuid.uuid4()
   - Insert into decisions table (serialize reason_codes as JSON string)
   - Set timestamp to current datetime (ISO format)
   - Return DecisionRecord

6. Function: get_decision(decision_id: str) -> Optional[DecisionRecord]
   - Query decisions table
   - Deserialize reason_codes from JSON string
   - Return DecisionRecord or None if not found

Import ApplicationRequest, ApplicationRecord, DecisionRecord from models.
Use json.dumps() and json.loads() for reason_codes.
Call init_db() when module loads (at top level).

Proceed now.
```

**Verification:**

```powershell
python -c "from src.day3.credit_decisioning.repository import init_db, create_application; from src.day3.credit_decisioning.models import ApplicationRequest; init_db(); app = create_application(ApplicationRequest(full_name='Test', annual_income=60000, monthly_debt_payments=1000, requested_amount=15000, employment_years=5, missed_payments_12m=0, address='123 St', email='test@test.com')); print(f'Created application: {app.application_id}')"
```

---

### D3-1f: Create Audit Logger

```
You are a GitHub Copilot coding agent.

Create an audit logger that writes to JSONL format (one JSON object per line).

Constraints:
- No MCP.
- MUST NOT log raw PII (full_name, address, email).
- MUST log only: IDs, scores, outcomes, reason codes, derived features (numeric).

Create file: src/day3/credit_decisioning/audit.py

Requirements:

1. Function: generate_request_id() -> str
   - Return a new UUID4 as string

2. Function: log_decision(
       application_id: str,
       decision_id: str,
       outcome: str,
       score: int,
       reason_codes: list[str],
       derived_features: dict
   ) -> None
   
   - Create audit entry dict with:
     - timestamp: current datetime in ISO format with timezone (use datetime.now(timezone.utc))
     - request_id: generate_request_id()
     - application_id: application_id
     - decision_id: decision_id
     - outcome: outcome
     - score: score
     - reason_codes: reason_codes
     - dti: derived_features["dti"]
     - annual_income: derived_features["annual_income"]
     - requested_amount: derived_features["requested_amount"]
     - employment_years: derived_features["employment_years"]
     - missed_payments_12m: derived_features["missed_payments_12m"]
   
   - Append to config.AUDIT_LOG_PATH as JSONL (one line per entry)
   - Use json.dumps() with sort_keys=True for determinism
   - Create parent directories if needed

Import config, json, datetime, uuid.

Proceed now.
```

**Verification:**

```powershell
python -c "from src.day3.credit_decisioning.audit import log_decision; log_decision('app-123', 'dec-456', 'APPROVE', 75, ['LOW_DTI', 'CLEAN_PAYMENT_HISTORY'], {'dti': 0.3, 'annual_income': 60000, 'requested_amount': 15000, 'employment_years': 5, 'missed_payments_12m': 0}); print('Audit entry written')"

# Verify no PII in audit log
Get-Content out/day3/audit_log.jsonl | Select-String -Pattern "full_name|address|email"
# Should return nothing (no matches)
```

---

### D3-1g: Create FastAPI Application

```
You are a GitHub Copilot coding agent.

Create the FastAPI application with 5 REST endpoints for credit decisioning.

Constraints:
- No MCP.
- Banking-safe (synthetic data).
- Professional error handling (HTTPException for 404, 422, 500).

Create file: src/day3/credit_decisioning/app.py

Requirements:

Import:
- fastapi (FastAPI, HTTPException)
- models (ApplicationRequest, ApplicationRecord, DecisionRecord)
- repository (init_db, create_application, get_application, create_decision, get_decision)
- features (derive_features)
- rules_engine (compute_decision)
- audit (log_decision)

Initialize:
- app = FastAPI(title="Credit Decisioning Service", version="1.0.0")
- Call init_db() at startup

Endpoints:

1. @app.get("/health")
   - Return: {"status": "ok"}

2. @app.post("/applications", status_code=201)
   - Input: ApplicationRequest
   - Create application in repository
   - Return: {"application_id": app_record.application_id}

3. @app.get("/applications/{application_id}")
   - Fetch application from repository
   - If not found: raise HTTPException(status_code=404, detail="Application not found")
   - Return: ApplicationRecord

4. @app.post("/applications/{application_id}/decision", status_code=201)
   - Fetch application from repository (404 if not found)
   - Convert ApplicationRecord to dict for derive_features()
   - Derive features using features.derive_features()
   - Compute decision using rules_engine.compute_decision()
   - Create decision in repository
   - Log decision using audit.log_decision(application_id, decision_id, outcome, score, reason_codes, derived_features)
   - Return: DecisionRecord

5. @app.get("/decisions/{decision_id}")
   - Fetch decision from repository
   - If not found: raise HTTPException(status_code=404, detail="Decision not found")
   - Return: DecisionRecord

Use Pydantic for automatic validation (422 errors handled by FastAPI).

Proceed now.
```

**Verification:**

```powershell
# Start API
uvicorn src.day3.credit_decisioning.app:app --reload

# In another terminal, test health endpoint
Invoke-WebRequest -Uri http://127.0.0.1:8000/health
```

Expected: `{"status":"ok"}`

---

### D3-1h: Create Sample Data Generator

```
You are a GitHub Copilot coding agent.

Create a synthetic sample data generator for credit applications.

Constraints:
- No MCP.
- Banking-safe (synthetic data only, obviously fake names/addresses).
- Include variety: safe, risky, borderline, edge cases.

Create file: src/day3/credit_decisioning/sample_data.py

Requirements:

Function: generate_samples() -> list[dict]
- Generate 10 sample applications
- Include:
  - 3 "safe" applicants (high income, low debt, no missed payments) → expect APPROVE
    - Example: annual_income=80000, monthly_debt_payments=800, requested_amount=10000, employment_years=8, missed_payments_12m=0
  - 3 "risky" applicants (low income, high debt, missed payments) → expect DECLINE
    - Example: annual_income=30000, monthly_debt_payments=1200, requested_amount=20000, employment_years=1, missed_payments_12m=5
  - 2 "borderline" (moderate risk) → expect REFER
    - Example: annual_income=50000, monthly_debt_payments=1500, requested_amount=12000, employment_years=3, missed_payments_12m=1
  - 2 "edge cases"
    - Example: DTI exactly 0.36, score exactly 70, etc.

Use names like: "Alice Safe", "Bob Risky", "Charlie Borderline", "Dana Edge"
Addresses: "123 Fake St, Testville", etc.
Emails: "alice.safe@example.com", etc.

Function: save_samples(samples: list[dict], output_path: Path) -> None
- Write samples to output_path as JSON (pretty-printed)

If __name__ == "__main__":
- Generate samples
- Print summary (count by expected outcome)
- Save to out/day3/sample_requests.json

Import: json, pathlib, config

Proceed now.
```

**Verification:**

```powershell
python -m src.day3.credit_decisioning.sample_data
Get-Content out/day3/sample_requests.json
```

---

### D3-1i: Create End-to-End Demo Script

```
You are a GitHub Copilot coding agent.

Create an end-to-end demo script that interacts with the Credit Decisioning API.

Constraints:
- No MCP.
- Assume API is running at http://127.0.0.1:8000.
- Use httpx for HTTP requests.

Create file: src/day3/credit_decisioning/demo_e2e.py

Requirements:

Function: run_demo() -> None

1. Print "=== Credit Decisioning E2E Demo ==="

2. Define 3 sample applications (dicts):
   - Sample 1: Safe applicant (expect APPROVE)
     - annual_income=70000, monthly_debt_payments=1000, requested_amount=12000, employment_years=7, missed_payments_12m=0
   - Sample 2: Risky applicant (expect DECLINE)
     - annual_income=35000, monthly_debt_payments=1500, requested_amount=20000, employment_years=1, missed_payments_12m=4
   - Sample 3: Borderline applicant (expect REFER)
     - annual_income=50000, monthly_debt_payments=1400, requested_amount=15000, employment_years=3, missed_payments_12m=1

3. For each sample:
   - POST to http://127.0.0.1:8000/applications (get application_id)
   - POST to http://127.0.0.1:8000/applications/{application_id}/decision (get decision)
   - Print: "Application {n}: {outcome} (score: {score})"
   - Print: "Reason codes: {reason_codes}"
   - Print blank line

4. Print "=== Demo Complete ==="

If __name__ == "__main__":
- Run run_demo()

Import httpx.

Use httpx.post() and response.json() to parse responses.

Proceed now.
```

**Verification:**

```powershell
# Ensure API is running
# Then run demo
python src/day3/credit_decisioning/demo_e2e.py
```

---

### D3-1j: Create Tests - Rules Engine

```
You are a GitHub Copilot coding agent.

Create pytest unit tests for the rules engine.

Constraints:
- No MCP.
- Test each scoring adjustment and reason code independently.

Create file: tests/day3/test_rules_engine.py

Test cases:

1. test_baseline_score:
   - Features with all neutral values → score == 50

2. test_low_dti_adjustment:
   - dti=0.30 (< 0.36) → score includes +10, reason_codes includes "LOW_DTI"

3. test_high_dti_adjustment:
   - dti=0.45 (>= 0.43) → score includes -15, reason_codes includes "HIGH_DTI"

4. test_clean_payment_history:
   - missed_payments_12m=0 → score includes +10, reason_codes includes "CLEAN_PAYMENT_HISTORY"

5. test_poor_payment_history:
   - missed_payments_12m=5 (>= 3) → score includes -20, reason_codes includes "POOR_PAYMENT_HISTORY"

6. test_stable_employment:
   - employment_years=8 (> 5) → score includes +10, reason_codes includes "STABLE_EMPLOYMENT"

7. test_low_credit_exposure:
   - affordability_ratio=0.25 (< 0.30) → score includes +5, reason_codes includes "LOW_CREDIT_EXPOSURE"

8. test_high_credit_exposure:
   - affordability_ratio=0.55 (>= 0.50) → score includes -10, reason_codes includes "HIGH_CREDIT_EXPOSURE"

9. test_approve_outcome:
   - Features that result in score >= 70 → outcome == "APPROVE", reason_codes includes "SCORE_APPROVE_BAND"

10. test_decline_outcome:
    - Features that result in score < 50 → outcome == "DECLINE", reason_codes includes "SCORE_DECLINE_BAND"

11. test_refer_outcome:
    - Features that result in score >= 50 and < 70 → outcome == "REFER", reason_codes includes "SCORE_REFER_BAND"

12. test_determinism:
    - Call compute_decision twice with same features → assert results are identical (score, outcome, reason_codes)

Import: from src.day3.credit_decisioning.rules_engine import compute_decision

Use pytest assertions.

Proceed now.
```

**Verification:**

```powershell
pytest tests/day3/test_rules_engine.py -v
```

---

### D3-1k: Create Tests - API Endpoints

```
You are a GitHub Copilot coding agent.

Create pytest tests for the FastAPI endpoints using TestClient.

Constraints:
- No MCP.
- Test success and error cases.

Create file: tests/day3/test_api_endpoints.py

Setup:
- Import TestClient from fastapi.testclient
- Import app from src.day3.credit_decisioning.app
- Create client = TestClient(app)

Test cases:

1. test_health_check:
   - response = client.get("/health")
   - assert response.status_code == 200
   - assert response.json() == {"status": "ok"}

2. test_create_application_success:
   - POST /applications with valid ApplicationRequest
   - assert status_code == 201
   - assert "application_id" in response.json()

3. test_create_application_invalid_income:
   - POST /applications with annual_income=-1000 (invalid)
   - assert status_code == 422 (validation error)

4. test_get_application_success:
   - POST /applications (get application_id)
   - GET /applications/{application_id}
   - assert status_code == 200
   - assert response data matches submitted data

5. test_get_application_not_found:
   - GET /applications/nonexistent-id
   - assert status_code == 404

6. test_compute_decision_success:
   - POST /applications (get application_id)
   - POST /applications/{application_id}/decision
   - assert status_code == 201
   - assert "decision_id" in response.json()
   - assert "outcome" in response.json()
   - assert "score" in response.json()
   - assert "reason_codes" in response.json()

7. test_compute_decision_application_not_found:
   - POST /applications/nonexistent-id/decision
   - assert status_code == 404

8. test_get_decision_success:
   - POST /applications (get application_id)
   - POST /applications/{application_id}/decision (get decision_id)
   - GET /decisions/{decision_id}
   - assert status_code == 200

9. test_get_decision_not_found:
   - GET /decisions/nonexistent-id
   - assert status_code == 404

Proceed now.
```

**Verification:**

```powershell
pytest tests/day3/test_api_endpoints.py -v
```

---

### D3-1l: Create Tests - End-to-End Scenarios

```
You are a GitHub Copilot coding agent.

Create end-to-end scenario tests for the credit decisioning service.

Constraints:
- No MCP.
- Test full workflows including audit log verification.

Create file: tests/day3/test_end_to_end_scenarios.py

Setup:
- Import TestClient from fastapi.testclient
- Import app from src.day3.credit_decisioning.app
- Import config from src.day3.credit_decisioning.config
- Create client = TestClient(app)

Test cases:

1. test_full_workflow_approve:
   - Submit safe application (high income, low debt, no missed payments)
   - Compute decision
   - Verify outcome == "APPROVE"
   - Verify score >= 70
   - Verify reason_codes includes "SCORE_APPROVE_BAND"

2. test_full_workflow_decline:
   - Submit risky application (low income, high debt, missed payments)
   - Compute decision
   - Verify outcome == "DECLINE"
   - Verify score < 50
   - Verify reason_codes includes "SCORE_DECLINE_BAND"

3. test_full_workflow_refer:
   - Submit borderline application (moderate risk)
   - Compute decision
   - Verify outcome == "REFER"
   - Verify score >= 50 and < 70
   - Verify reason_codes includes "SCORE_REFER_BAND"

4. test_audit_log_entry_created:
   - Submit application and compute decision
   - Read audit log file (config.AUDIT_LOG_PATH)
   - Parse JSONL (each line is a JSON object)
   - Verify at least one entry contains the application_id and decision_id
   - Verify entry has: timestamp, outcome, score, reason_codes

5. test_audit_log_no_pii:
   - Submit application with full_name, address, email
   - Compute decision
   - Read audit log file
   - Verify NO line contains the full_name, address, or email (use string search)

Use json.loads() to parse JSONL entries.

Proceed now.
```

**Verification:**

```powershell
pytest tests/day3/test_end_to_end_scenarios.py -v
```

---

### D3-1m: Create Repository Tests

```
You are a GitHub Copilot coding agent.

Create pytest tests for the repository module.

Constraints:
- No MCP.
- Test CRUD operations.

Create file: tests/day3/test_repository.py

Test cases:

1. test_create_and_get_application:
   - Create application using create_application()
   - Retrieve using get_application(application_id)
   - Verify data matches

2. test_get_application_not_found:
   - Call get_application("nonexistent-id")
   - Verify returns None

3. test_create_and_get_decision:
   - Create application
   - Create decision using create_decision()
   - Retrieve using get_decision(decision_id)
   - Verify data matches

4. test_get_decision_not_found:
   - Call get_decision("nonexistent-id")
   - Verify returns None

Import:
- from src.day3.credit_decisioning.repository import create_application, get_application, create_decision, get_decision
- from src.day3.credit_decisioning.models import ApplicationRequest

Proceed now.
```

**Verification:**

```powershell
pytest tests/day3/test_repository.py -v
```

---

### D3-1n: Create README for Capstone Implementation

```
You are a GitHub Copilot coding agent.

Create a README for the credit decisioning implementation.

Create file: src/day3/credit_decisioning/README.md

Content:

# Credit Decisioning Service

## Overview
A deterministic credit decisioning API built with FastAPI.

## Features
- 5 REST endpoints (health, applications, decisions)
- Deterministic scoring with reason codes
- Audit logging (JSONL, no PII)
- SQLite persistence
- Comprehensive test suite

## Installation
```powershell
pip install fastapi uvicorn pydantic pytest httpx
```

## Running the Service
```powershell
uvicorn src.day3.credit_decisioning.app:app --reload
```

Access:
- API: http://127.0.0.1:8000
- OpenAPI docs: http://127.0.0.1:8000/docs

## Running Tests
```powershell
pytest tests/day3/ -v
```

## Generating Sample Data
```powershell
python -m src.day3.credit_decisioning.sample_data
```

## Running Demo
```powershell
python src/day3/credit_decisioning/demo_e2e.py
```

## Verification
```powershell
# Health check
Invoke-WebRequest -Uri http://127.0.0.1:8000/health

# View audit log
Get-Content out/day3/audit_log.jsonl
```

## Architecture
See /day3_capstone/capstone_architecture.md

## Requirements
See /day3_capstone/capstone_requirements.md

Proceed now.
```

---

## Prompt D3-2: Generate Governance Artifacts

### D3-2a: Create Threat Model

```
You are a GitHub Copilot coding agent.

Create a threat model for the Day 3 capstone credit decisioning service.

Constraints:
- No MCP.
- Banking-safe context (synthetic data, internal use).
- Practical threats for a learning exercise.

Create file: day3_capstone/threat_model.md

Use the structure:
1. System Overview (brief)
2. Assets (what needs protection)
3. Threat Actors (who might attack)
4. Attack Surfaces (where vulnerabilities exist)
5. Threat Scenarios (specific threats)
6. Mitigations (how threats are addressed)
7. Testing/Verification (how to verify mitigations)

Threats to include:
- API abuse (no rate limiting, no auth)
- PII leakage via audit logs
- SQL injection (if using SQLite)
- Input validation bypass
- Audit log tampering
- Insecure defaults in config

For each threat:
- Severity: L/M/H
- Likelihood: L/M/H
- Mitigation status: Implemented / Planned / Out of Scope
- Verification method

Reference actual files (app.py, audit.py, etc.) where mitigations exist.

Proceed now.
```

---

### D3-2b: Create Risk Register

```
You are a GitHub Copilot coding agent.

Create a risk register for the Day 3 capstone.

Constraints:
- No MCP.
- Banking context (learning exercise, not production).

Create file: day3_capstone/risk_register.md

Use table format:
| Risk ID | Risk Description | Category | Likelihood | Impact | Risk Rating | Mitigation | Owner | Status |

Categories: Technical, Operational, Compliance, Data Privacy

Risk Rating: L (Low), M (Medium), H (High), C (Critical)

Include risks:
1. Non-deterministic decisions (impact: audit failures)
2. PII leakage in logs (impact: compliance violation)
3. Test failures in production (impact: incorrect decisions)
4. Audit log corruption (impact: loss of evidence)
5. Configuration errors (impact: wrong thresholds)
6. Inadequate input validation (impact: crashes, incorrect scores)
7. Incomplete requirements traceability (impact: audit findings)

For each risk:
- Mitigation strategy (specific)
- Owner (role, e.g., "Developer", "QA", "Risk Team")
- Status (Open / Mitigated / Accepted)

Proceed now.
```

---

### D3-2c: Update Requirements Traceability Matrix

```
You are a GitHub Copilot coding agent.

Update the requirements traceability matrix in day3_capstone/capstone_requirements.md.

Constraints:
- No MCP.
- Map all functional and non-functional requirements to actual implemented files.

Task:
- Review the traceability matrix in Section 8 of capstone_requirements.md
- Update the "Module/File" column with actual file paths:
  - FR-1: src/day3/credit_decisioning/app.py
  - FR-2: src/day3/credit_decisioning/app.py, models.py, repository.py
  - FR-4: src/day3/credit_decisioning/app.py, rules_engine.py, features.py, audit.py
  - (and so on for all requirements)
- Verify "Test File(s)" column matches actual test files created
- Verify "Verification Command" column has correct pytest commands

Review and update the table. Ensure all FR-1 through FR-10 and NFR-1 through NFR-4 are mapped correctly.

Proceed now.
```

---

## Prompt D3-3: Add VS Code Tasks

```
You are a GitHub Copilot coding agent.

Update .vscode/tasks.json to add Day 3 tasks for the capstone.

Constraints:
- No MCP.
- Support Windows (PowerShell) and Mac/Linux (bash).
- Tasks should be easy to run from VS Code (Ctrl+Shift+P → Tasks: Run Task).

Add these tasks:

1. "Day3: Generate Sample Applications"
   - Command: python -m src.day3.credit_decisioning.sample_data
   - Group: none
   - problemMatcher: []

2. "Day3: Run Capstone API"
   - Command: uvicorn src.day3.credit_decisioning.app:app --reload
   - Group: none
   - problemMatcher: []
   - isBackground: true (server runs in background)

3. "Day3: Run Capstone Tests"
   - Command: pytest tests/day3/ -v
   - Group: test
   - problemMatcher: []

4. "Day3: Run E2E Demo Script"
   - Command: python src/day3/credit_decisioning/demo_e2e.py
   - Group: none
   - problemMatcher: []
   - Note: API must be running first

5. "Verify-All (Day3)"
   - Depends on: "Day3: Run Capstone Tests", "Day3: Generate Sample Applications"
   - Runs tests and generates samples

If .vscode/tasks.json doesn't exist, create it. Otherwise, append to existing tasks array.

Use "type": "shell" for all tasks.

Proceed now.
```

**Verification:**

```
Ctrl+Shift+P → Tasks: Run Task → Day3: Run Capstone Tests
```

---

## Prompt D3-4: Create Evidence Bundle

```
You are a GitHub Copilot coding agent.

Create a script to collect evidence for audit review.

Constraints:
- No MCP.
- Collect synthetic outputs only (no real data).

Create file: scripts/day3_collect_evidence.py

Requirements:

Function: collect_evidence() -> None

Steps:
1. Print "=== Collecting Day 3 Evidence ==="

2. Run tests:
   - Execute: pytest tests/day3/ -v --tb=short
   - Capture output to: out/day3/test_output.txt
   - Print "Tests completed: out/day3/test_output.txt"

3. Copy audit log:
   - Copy out/day3/audit_log.jsonl to out/day3/evidence/audit_log.jsonl
   - Print "Audit log copied"

4. Create evidence manifest:
   - Write out/day3/evidence/evidence_manifest.md with:
     - "# Evidence Manifest"
     - "Generated: {timestamp}"
     - "Contents:"
     - "- test_output.txt (test results)"
     - "- audit_log.jsonl (decision audit trail, no PII)"

5. Create ZIP bundle:
   - Zip out/day3/evidence/ → out/day3/evidence_bundle.zip
   - Print "Evidence bundle created: out/day3/evidence_bundle.zip"

If __name__ == "__main__":
- Call collect_evidence()

Use subprocess for pytest, shutil for copying/zipping.

Proceed now.
```

**Verification:**

```powershell
python scripts/day3_collect_evidence.py
```

---

## Prompt D3-5: Update Training TOC

```
You are a GitHub Copilot coding agent.

Update TRAINING_TOC.md to include all Day 3 capstone materials.

Task:
Add a new section for Day 3:

## Day 3: Capstone — Credit Decisioning Slice

### Core Materials
- [Overview](day3_capstone/README.md)
- [Capstone Overview](day3_capstone/capstone_overview.md)
- [Requirements](day3_capstone/capstone_requirements.md)
- [Architecture](day3_capstone/capstone_architecture.md)
- [Runbook](day3_capstone/capstone_runbook.md)

### Governance
- [Threat Model](day3_capstone/threat_model.md)
- [Risk Register](day3_capstone/risk_register.md)

### Lab
- [Lab: Build Credit Decisioning Slice](day3_capstone/labs/capstone_build_credit_decisioning_slice.md)

### Prompts
- [Day 3 Copilot Agent Prompts](day3_capstone/prompts/day3_prompts.md)

Append this to TRAINING_TOC.md after Day 2 section.

Proceed now.
```

---

## GitHub Copilot CLI Prompts (Safe Exercises)

### CLI-1: Find Credit Decisioning Files

```bash
gh copilot suggest "find all Python files in src/day3/"
```

### CLI-2: Run Tests with Output

```bash
gh copilot suggest "run pytest on tests/day3/ with verbose output"
```

### CLI-3: Start API Server

```bash
gh copilot suggest "start uvicorn server for src.day3.credit_decisioning.app:app with auto-reload"
```

### CLI-4: View Audit Log

```bash
gh copilot suggest "display contents of out/day3/audit_log.jsonl"
```

### CLI-5: Check for PII in Audit Log

```bash
gh copilot suggest "search for strings 'full_name', 'address', or 'email' in out/day3/audit_log.jsonl"
```

### CLI-6: Create Evidence Bundle

```bash
gh copilot suggest "zip the out/day3/evidence/ directory to out/day3/evidence_bundle.zip"
```

---

## Troubleshooting Prompts

### TS-1: Fix Import Errors

```
I'm getting "ModuleNotFoundError" when importing from src.day3.credit_decisioning.

Verify:
- All directories have __init__.py files
- Python path includes project root
- Dependencies are installed (fastapi, uvicorn, pydantic, pytest, httpx)

Show me how to fix this.
```

### TS-2: Fix Non-Deterministic Results

```
My decision engine produces different reason codes on repeated runs with the same input.

Review src/day3/credit_decisioning/rules_engine.py and ensure:
- No random number generation
- Reason codes are sorted alphabetically
- No timestamp-based logic in scoring

Show me the fix.
```

### TS-3: Fix Audit Log PII Leakage

```
My audit log contains full_name, address, or email (raw PII).

Review src/day3/credit_decisioning/audit.py:
- Verify log_decision() only logs IDs and numeric features
- Exclude full_name, address, email from audit entry dict

Show me the corrected audit.py log_decision() function.
```

---

## Summary

You now have all prompts to:

1. ✅ Implement the complete credit decisioning service (D3-1)
2. ✅ Generate governance artifacts (D3-2)
3. ✅ Configure VS Code tasks (D3-3)
4. ✅ Create evidence bundles (D3-4)
5. ✅ Update training materials (D3-5)
6. ✅ Use GitHub Copilot CLI for workflow automation

**Recommended execution order:**

1. D3-1a through D3-1n (implementation + tests)
2. Verify all tests pass: `pytest tests/day3/ -v`
3. D3-2a through D3-2c (governance)
4. D3-3 (VS Code tasks)
5. D3-4 (evidence bundle)
6. D3-5 (update TOC)

**Next:** Follow [capstone_build_credit_decisioning_slice.md](../labs/capstone_build_credit_decisioning_slice.md) for step-by-step lab instructions.
