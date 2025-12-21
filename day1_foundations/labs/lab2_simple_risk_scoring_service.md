# Lab 2: Simple Risk Scoring Service

**Duration**: 90 minutes (15:45–17:15)  
**Level**: Intermediate  
**Focus**: Building an explainable credit risk API with audit logging

## Learning Objectives

By the end of this lab, you will:

* Build a RESTful API using FastAPI with AI assistance
* Implement explainable risk scoring logic (deterministic, auditable)
* Create comprehensive audit logging for compliance
* Write API tests using FastAPI TestClient
* Generate synthetic credit application data
* Apply the 3C framework to API design prompts
* Create production-ready API documentation

## Business Context

You work for a bank's credit risk team. Loan officers use a risk scoring system to evaluate credit applications. The current system is:
* Manual and time-consuming
* Inconsistent across officers
* Not auditable (no record of how decisions were made)

Your team needs to build an **explainable risk scoring service** that:
* Provides consistent risk scores (0-100 scale)
* Categorizes applications into risk bands (LOW, MEDIUM, HIGH)
* Explains every decision with reason codes
* Logs every scoring request for audit trails
* Operates deterministically (same input → same output)

**Compliance requirements**:
* Every scoring decision must be traceable
* Reason codes must be clear and standardized
* No PII should be logged (only application IDs and synthetic fields)
* All timestamps in UTC

## Lab Overview

### What You'll Build

A FastAPI-based risk scoring service with:

1. **API endpoints** - REST API for health checks and scoring
2. **Scoring logic** - Deterministic, rule-based risk scoring
3. **Explainability** - Reason codes for every score component
4. **Audit logging** - JSONL audit trail for all requests
5. **Data models** - Pydantic models for request/response validation
6. **Comprehensive tests** - Unit tests for scoring, API tests for endpoints
7. **Documentation** - Auto-generated OpenAPI/Swagger docs

### Project Structure

```
src/day1/risk_scoring_service/
├── __init__.py
├── app.py              # FastAPI application and routes
├── models.py           # Pydantic request/response models
├── scoring.py          # Risk scoring logic with reason codes
├── audit.py            # Audit logging functionality
├── config.py           # Configuration (paths, thresholds)
├── README.md           # API documentation
└── audit_log.jsonl     # Audit trail (generated at runtime)

tests/day1/
├── test_risk_scoring.py    # Unit tests for scoring logic
└── test_risk_api.py        # API integration tests

src/samples/
├── synthetic_credit_apps.py    # Generate test credit applications
└── sample_credit_apps.json     # Sample application data
```

---

## Part 1: Setup and Planning (10 min)

### Step 1: Understand the Requirements

**Scoring inputs** (credit application fields):
* `application_id`: Unique identifier (synthetic)
* `annual_income`: Applicant's annual income (Decimal)
* `debt`: Current debt amount (Decimal)
* `employment_years`: Years at current employer (int)
* `missed_payments_12m`: Number of missed payments in last 12 months (int)
* `requested_amount`: Loan amount requested (Decimal)

**Scoring outputs**:
* `risk_score`: Numeric score from 0-100 (100 = lowest risk, 0 = highest risk)
* `risk_band`: Category (LOW, MEDIUM, HIGH)
* `reason_codes`: List of codes explaining the score
* `request_id`: Unique ID for tracing this request

**Scoring logic** (simplified, deterministic):
1. Start with baseline score: 50
2. Adjust based on debt-to-income ratio:
   - DTI < 0.2: +20 points (reason: LOW_DTI)
   - DTI 0.2-0.4: +10 points (reason: MODERATE_DTI)
   - DTI > 0.4: -20 points (reason: HIGH_DTI)
3. Adjust based on missed payments:
   - 0 missed: +15 points (reason: CLEAN_PAYMENT_HISTORY)
   - 1-2 missed: +0 points (reason: SOME_MISSED_PAYMENTS)
   - 3+ missed: -25 points (reason: POOR_PAYMENT_HISTORY)
4. Adjust based on employment tenure:
   - < 1 year: -10 points (reason: LOW_TENURE)
   - 1-3 years: +0 points (reason: MODERATE_TENURE)
   - 3+ years: +10 points (reason: HIGH_TENURE)
5. Adjust based on requested amount vs income:
   - Requested < 30% annual income: +10 points (reason: AFFORDABLE_AMOUNT)
   - Requested 30-50% annual income: +0 points (reason: MODERATE_AMOUNT)
   - Requested > 50% annual income: -15 points (reason: HIGH_AMOUNT)
6. Clip final score to [0, 100]
7. Map to risk band:
   - 70-100: LOW
   - 40-69: MEDIUM
   - 0-39: HIGH

**Audit log entry format** (JSONL):
```json
{"timestamp": "2024-01-15T12:00:00Z", "request_id": "REQ-abc123", "application_id": "APP-001", "score": 72, "band": "LOW", "reason_codes": ["LOW_DTI", "CLEAN_PAYMENT_HISTORY", "HIGH_TENURE", "AFFORDABLE_AMOUNT"]}
```

### Step 2: Define API Endpoints

**API specification**:

1. `GET /health`
   - Returns: `{"status": "healthy"}`
   - Use: Health check for monitoring

2. `POST /score`
   - Request body: Credit application fields (JSON)
   - Response: Risk score, band, reason codes, request ID
   - Side effect: Appends entry to audit log

---

## Part 2: Implement Configuration (10 min)

### Step 2.1: Generate Configuration Module

**Prompt for Copilot Chat**:

```
Create a configuration module for the risk scoring service.

[Context]
We need centralized configuration for paths, thresholds, and environment settings.

[Constraints]
- Use Python 3.9+ with type hints
- Support environment variables (with sensible defaults)
- No hardcoded paths in business logic

[Criteria]
Create src/day1/risk_scoring_service/config.py with:

1. Class: ServiceConfig (dataclass or Pydantic BaseSettings)
   Fields:
   - audit_log_path: str (default: "src/day1/risk_scoring_service/audit_log.jsonl")
   - risk_band_thresholds: dict (default: {"LOW": 70, "MEDIUM": 40, "HIGH": 0})
   - max_future_days: int (default: 1, for timestamp validation)
   
2. Function: get_config() -> ServiceConfig
   - Returns singleton instance of ServiceConfig
   - Loads from environment variables if present

Include docstrings explaining each config field.
```

**Expected output**: Copilot generates `config.py` with configuration class.

---

## Part 3: Implement Data Models (15 min)

### Step 3.1: Generate Request and Response Models

**Prompt for Copilot Chat**:

```
Create Pydantic data models for the risk scoring API.

[Context]
We're building a FastAPI service for credit risk scoring.
Need models for API requests and responses with validation.

[Constraints]
- Use Python 3.9+ with Pydantic v2
- Use Decimal for monetary amounts
- All fields should have descriptions (for API docs)
- Include validation (positive amounts, valid ranges)

[Criteria]
Create src/day1/risk_scoring_service/models.py with:

1. CreditApplication (request model):
   - application_id: str (required, unique identifier)
   - annual_income: Decimal (required, must be > 0)
   - debt: Decimal (required, must be >= 0)
   - employment_years: int (required, must be >= 0)
   - missed_payments_12m: int (required, must be >= 0)
   - requested_amount: Decimal (required, must be > 0)
   
   Add Pydantic validators:
   - annual_income and requested_amount must be positive
   - debt and missed_payments must be non-negative
   
   Include Field descriptions for API documentation.

2. RiskBand (enum):
   - LOW, MEDIUM, HIGH

3. RiskScore (response model):
   - request_id: str
   - application_id: str
   - risk_score: int (0-100)
   - risk_band: RiskBand
   - reason_codes: list[str]
   
Include docstrings and examples in Field descriptions.
```

**Expected output**: Copilot generates `models.py` with three models/enums.

### Step 3.2: Verify Models

**Test in Python REPL**:
```python
from src.day1.risk_scoring_service.models import CreditApplication, RiskScore, RiskBand
from decimal import Decimal

# Valid application
app = CreditApplication(
    application_id="APP-001",
    annual_income=Decimal("75000"),
    debt=Decimal("15000"),
    employment_years=5,
    missed_payments_12m=0,
    requested_amount=Decimal("20000")
)
print(app)

# Should raise validation error (negative income)
try:
    bad_app = CreditApplication(
        application_id="APP-002",
        annual_income=Decimal("-1000"),  # Invalid
        debt=Decimal("0"),
        employment_years=0,
        missed_payments_12m=0,
        requested_amount=Decimal("1000")
    )
except Exception as e:
    print(f"Validation error (expected): {e}")
```

---

## Part 4: Implement Scoring Logic (20 min)

### Step 4.1: Generate Scoring Function

**Prompt for Copilot Chat**:

```
Create deterministic risk scoring logic with explainability.

[Context]
We need a pure function that calculates a credit risk score based on application data.
The function must be deterministic (same input → same output, always) and explainable (return reason codes).

[Constraints]
- Use Python 3.9+ with type hints
- Pure function (no side effects, no randomness)
- Return score and reason codes
- Use Decimal for calculations to avoid float precision issues

[Criteria]
Create src/day1/risk_scoring_service/scoring.py with:

1. Function: calculate_risk_score(app: CreditApplication) -> tuple[int, list[str]]
   
   Logic:
   - Start with baseline: 50
   - Calculate DTI (debt / annual_income)
   - Adjust score based on:
     a) DTI ratio:
        - < 0.2: +20, reason "LOW_DTI"
        - 0.2-0.4: +10, reason "MODERATE_DTI"
        - > 0.4: -20, reason "HIGH_DTI"
     b) Missed payments:
        - 0: +15, reason "CLEAN_PAYMENT_HISTORY"
        - 1-2: +0, reason "SOME_MISSED_PAYMENTS"
        - 3+: -25, reason "POOR_PAYMENT_HISTORY"
     c) Employment years:
        - < 1: -10, reason "LOW_TENURE"
        - 1-3: +0, reason "MODERATE_TENURE"
        - 3+: +10, reason "HIGH_TENURE"
     d) Requested amount ratio (requested / annual_income):
        - < 0.3: +10, reason "AFFORDABLE_AMOUNT"
        - 0.3-0.5: +0, reason "MODERATE_AMOUNT"
        - > 0.5: -15, reason "HIGH_AMOUNT"
   - Clip score to [0, 100]
   - Return (score, reason_codes)

2. Function: determine_risk_band(score: int) -> RiskBand
   - 70-100: RiskBand.LOW
   - 40-69: RiskBand.MEDIUM
   - 0-39: RiskBand.HIGH

Include:
- Docstrings with examples
- Type hints
- Comments explaining each scoring rule
- Import CreditApplication, RiskBand from models.py
- Import Decimal for DTI calculation
```

**Expected output**: Copilot generates `scoring.py` with two functions.

### Step 4.2: Manually Test Scoring Logic

**Test different scenarios**:
```python
from src.day1.risk_scoring_service.models import CreditApplication
from src.day1.risk_scoring_service.scoring import calculate_risk_score, determine_risk_band
from decimal import Decimal

# High-quality applicant
good_app = CreditApplication(
    application_id="APP-GOOD",
    annual_income=Decimal("100000"),
    debt=Decimal("10000"),  # DTI = 0.1 (low)
    employment_years=5,
    missed_payments_12m=0,
    requested_amount=Decimal("25000")  # 25% of income
)
score, reasons = calculate_risk_score(good_app)
band = determine_risk_band(score)
print(f"Good app: Score={score}, Band={band}, Reasons={reasons}")
# Expected: High score, LOW band, positive reasons

# High-risk applicant
bad_app = CreditApplication(
    application_id="APP-BAD",
    annual_income=Decimal("30000"),
    debt=Decimal("20000"),  # DTI = 0.67 (high)
    employment_years=0,
    missed_payments_12m=5,
    requested_amount=Decimal("20000")  # 67% of income
)
score, reasons = calculate_risk_score(bad_app)
band = determine_risk_band(score)
print(f"Bad app: Score={score}, Band={band}, Reasons={reasons}")
# Expected: Low score, HIGH band, negative reasons
```

---

## Part 5: Implement Audit Logging (15 min)

### Step 5.1: Generate Audit Logger

**Prompt for Copilot Chat**:

```
Create an audit logging module for the risk scoring service.

[Context]
We need to log every risk scoring request for compliance and audit purposes.
Logs should be append-only, timestamped, and contain no PII.

[Constraints]
- Use Python 3.9+
- Write to JSONL (JSON Lines) format
- Use UTC timestamps
- Thread-safe (multiple requests may happen concurrently)
- No PII (only synthetic IDs and scores)

[Criteria]
Create src/day1/risk_scoring_service/audit.py with:

1. Function: log_scoring_request(
     request_id: str,
     application_id: str,
     score: int,
     band: RiskBand,
     reason_codes: list[str],
     log_path: str = None
   ) -> None
   
   Logic:
   - Create log entry dict with:
     - timestamp (ISO-8601 UTC)
     - request_id
     - application_id (synthetic, safe to log)
     - score
     - band (as string)
     - reason_codes (list)
   - Append to log file as single JSON line
   - Create log file if doesn't exist
   - Use file locking or append mode for thread safety
   - If log_path is None, get from config

2. Function: read_audit_log(log_path: str = None) -> list[dict]
   - Read all entries from audit log
   - Parse each line as JSON
   - Return list of entries
   - For testing/verification purposes

Include:
- Error handling (file write errors)
- Docstrings
- Type hints
- Import json, datetime, config
```

**Expected output**: Copilot generates `audit.py` with logging functions.

### Step 5.2: Test Audit Logging

**Manual test**:
```python
from src.day1.risk_scoring_service.audit import log_scoring_request, read_audit_log
from src.day1.risk_scoring_service.models import RiskBand

# Log a test entry
log_scoring_request(
    request_id="REQ-TEST-001",
    application_id="APP-TEST-001",
    score=75,
    band=RiskBand.LOW,
    reason_codes=["LOW_DTI", "CLEAN_PAYMENT_HISTORY"]
)

# Read back
entries = read_audit_log()
print(f"Audit log has {len(entries)} entries")
print(f"Latest: {entries[-1]}")
```

---

## Part 6: Implement FastAPI Application (20 min)

### Step 6.1: Generate FastAPI App

**Prompt for Copilot Chat**:

```
Create a FastAPI application for the risk scoring service.

[Context]
We need a REST API with health check and scoring endpoints.
API should validate inputs, call scoring logic, log to audit trail, and return results.

[Constraints]
- Use FastAPI framework
- Use Pydantic models for validation
- Generate unique request IDs (UUID)
- Include CORS middleware (for future frontend)
- Include error handling

[Criteria]
Create src/day1/risk_scoring_service/app.py with:

1. FastAPI app instance with:
   - Title: "Credit Risk Scoring Service"
   - Description: "Explainable risk scoring API for credit applications"
   - Version: "1.0.0"

2. CORS middleware (allow all origins for dev)

3. GET /health endpoint:
   - Returns: {"status": "healthy", "service": "risk-scoring"}

4. POST /score endpoint:
   - Accepts: CreditApplication (Pydantic model validates)
   - Generates unique request_id (UUID)
   - Calls calculate_risk_score
   - Calls determine_risk_band
   - Logs to audit trail
   - Returns: RiskScore model
   
5. Error handling:
   - ValidationError → 422 with details
   - Unexpected errors → 500 with generic message

Include:
- Import FastAPI, CORSMiddleware
- Import models: CreditApplication, RiskScore, RiskBand
- Import scoring: calculate_risk_score, determine_risk_band
- Import audit: log_scoring_request
- Import uuid for request IDs
- Docstrings for endpoints (appear in Swagger docs)

Add root endpoint (GET /) that returns:
{"message": "Credit Risk Scoring API", "docs": "/docs"}
```

**Expected output**: Copilot generates `app.py` with FastAPI application.

### Step 6.2: Test API Locally

**Start the server**:
```bash
# Install dependencies if needed
pip install fastapi uvicorn python-multipart

# Run the API
uvicorn src.day1.risk_scoring_service.app:app --reload --port 8000
```

**Test with curl** (in another terminal):
```bash
# Health check
curl http://localhost:8000/health

# Score a good application
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{
    "application_id": "APP-001",
    "annual_income": 100000,
    "debt": 10000,
    "employment_years": 5,
    "missed_payments_12m": 0,
    "requested_amount": 25000
  }'

# Score a risky application
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{
    "application_id": "APP-002",
    "annual_income": 30000,
    "debt": 20000,
    "employment_years": 0,
    "missed_payments_12m": 5,
    "requested_amount": 20000
  }'
```

**View Swagger docs**:
Open browser to: http://localhost:8000/docs

**Verify audit log**:
```bash
# View audit entries
cat src/day1/risk_scoring_service/audit_log.jsonl

# Or in Python
python -c "from src.day1.risk_scoring_service.audit import read_audit_log; print(read_audit_log())"
```

---

## Part 7: Write Tests (30 min)

### Step 7.1: Generate Unit Tests for Scoring Logic

**Prompt for Copilot Chat**:

```
Create comprehensive pytest unit tests for risk scoring logic.

[Context]
We have deterministic scoring functions in scoring.py that need thorough unit tests.

[Constraints]
- Use pytest framework
- Test all scoring rules independently
- Test boundary conditions
- Verify reason codes are correct

[Criteria]
Create tests/day1/test_risk_scoring.py with:

1. Test class: TestRiskScoring

2. Test methods:
   
   test_baseline_score():
   - Create application with neutral values (all adjustments = 0)
   - Verify score = 50 (baseline)
   
   test_low_dti_bonus():
   - Create application with DTI < 0.2
   - Verify score includes +20 adjustment
   - Verify "LOW_DTI" in reason codes
   
   test_high_dti_penalty():
   - Create application with DTI > 0.4
   - Verify score includes -20 adjustment
   - Verify "HIGH_DTI" in reason codes
   
   test_clean_payment_history_bonus():
   - Create application with 0 missed payments
   - Verify "CLEAN_PAYMENT_HISTORY" in reason codes
   
   test_poor_payment_history_penalty():
   - Create application with 3+ missed payments
   - Verify "POOR_PAYMENT_HISTORY" in reason codes
   
   test_high_tenure_bonus():
   - Create application with 3+ employment years
   - Verify "HIGH_TENURE" in reason codes
   
   test_affordable_amount_bonus():
   - Create application with requested < 30% income
   - Verify "AFFORDABLE_AMOUNT" in reason codes
   
   test_score_clipping():
   - Create application that would score > 100
   - Verify score is clipped to 100
   - Create application that would score < 0
   - Verify score is clipped to 0
   
   test_risk_band_mapping():
   - Test determine_risk_band(75) -> RiskBand.LOW
   - Test determine_risk_band(50) -> RiskBand.MEDIUM
   - Test determine_risk_band(35) -> RiskBand.HIGH
   - Test boundary: determine_risk_band(70) -> RiskBand.LOW
   - Test boundary: determine_risk_band(69) -> RiskBand.MEDIUM
   - Test boundary: determine_risk_band(40) -> RiskBand.MEDIUM
   - Test boundary: determine_risk_band(39) -> RiskBand.HIGH

Use descriptive test names and AAA pattern.
Import: pytest, CreditApplication, Decimal, calculate_risk_score, determine_risk_band, RiskBand
```

**Expected output**: Copilot generates comprehensive unit tests.

### Step 7.2: Generate API Integration Tests

**Prompt for Copilot Chat**:

```
Create pytest integration tests for the FastAPI application.

[Context]
We need to test the complete API workflow: request → validation → scoring → audit → response.

[Constraints]
- Use pytest with FastAPI TestClient
- Use tmp_path for temporary audit log (don't pollute real log)
- Test both successful and error scenarios
- Verify audit log entries

[Criteria]
Create tests/day1/test_risk_api.py with:

1. Fixture: client() -> TestClient
   - Creates TestClient for the FastAPI app
   - Overrides config to use temporary audit log path

2. Test: test_health_endpoint(client)
   - GET /health
   - Assert status 200
   - Assert response contains "healthy"

3. Test: test_score_endpoint_valid_application(client, tmp_path)
   - POST /score with valid application
   - Assert status 200
   - Assert response has required fields (request_id, risk_score, risk_band, reason_codes)
   - Assert risk_score is in [0, 100]
   - Assert reason_codes is non-empty list

4. Test: test_score_endpoint_high_risk_application(client)
   - POST /score with high-risk profile (high DTI, missed payments, etc.)
   - Assert risk_band is HIGH

5. Test: test_score_endpoint_low_risk_application(client)
   - POST /score with low-risk profile
   - Assert risk_band is LOW

6. Test: test_score_endpoint_invalid_application(client)
   - POST /score with invalid data (negative income)
   - Assert status 422 (validation error)

7. Test: test_audit_log_entry_created(client, tmp_path)
   - Configure client to use tmp_path for audit log
   - POST /score
   - Read audit log file
   - Assert entry exists with correct fields

8. Test: test_deterministic_scoring(client)
   - POST /score with same application twice
   - Assert both responses have same risk_score and reason_codes

Import: pytest, TestClient, app, CreditApplication, Decimal, json
```

**Expected output**: Copilot generates API integration tests.

### Step 7.3: Run Tests

**Run all tests**:
```bash
# Run all Day 1 tests
pytest tests/day1/ -v

# Run only risk scoring tests
pytest tests/day1/test_risk_scoring.py -v

# Run only API tests
pytest tests/day1/test_risk_api.py -v

# Run with coverage
pytest tests/day1/ --cov=src/day1/risk_scoring_service --cov-report=html
```

**Verification**:
- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] Determinism test passes (critical for banking)

---

## Part 8: Generate Synthetic Test Data (10 min)

### Step 8.1: Create Credit Application Generator

**Prompt for Copilot Chat**:

```
Create a synthetic credit application data generator.

[Context]
We need realistic but fake credit application data for testing and demos.

[Constraints]
- Generate JSON file with credit applications
- Use deterministic random seed
- Mix of low, medium, and high risk profiles
- No real customer data

[Criteria]
Create src/samples/synthetic_credit_apps.py with:

1. Function: generate_credit_applications(count: int = 20, seed: int = 42) -> list[dict]
   - Generate mix:
     - 40% low risk (high income, low debt, good history)
     - 40% medium risk (moderate values)
     - 20% high risk (high debt, missed payments, low tenure)
   - Fields:
     - application_id: APP-{001..count}
     - annual_income: 30,000 to 150,000
     - debt: 0 to 100,000
     - employment_years: 0 to 20
     - missed_payments_12m: 0 to 10
     - requested_amount: 5,000 to 50,000
   
2. Function: write_json(apps: list[dict], file_path: str) -> None
   - Write to JSON file with indent=2

3. main() function:
   - Generate 20 applications
   - Write to src/samples/sample_credit_apps.json
   - Print summary (counts by risk profile)

Use deterministic seed for reproducibility.
If __name__ == "__main__": main()
```

**Expected output**: Copilot generates synthetic data generator.

### Step 8.2: Generate and Use Sample Data

**Generate data**:
```bash
python -m src.samples.synthetic_credit_apps
```

**Test with generated data**:
```python
import json
import requests

# Load sample applications
with open("src/samples/sample_credit_apps.json") as f:
    apps = json.load(f)

# Score first 3 applications
for app in apps[:3]:
    response = requests.post("http://localhost:8000/score", json=app)
    result = response.json()
    print(f"{app['application_id']}: Score={result['risk_score']}, Band={result['risk_band']}")
```

---

## Part 9: Create Documentation (10 min)

### Step 9.1: Generate README

**Prompt for Copilot Chat**:

```
Create comprehensive documentation for the risk scoring service.

[Context]
We have a complete FastAPI service with scoring, audit logging, and tests.
Users need clear documentation on how to use the API.

[Criteria]
Create src/day1/risk_scoring_service/README.md with:

1. Overview (what it does, why it exists)
2. Features (explainability, audit logging, determinism)
3. Installation (dependencies: fastapi, uvicorn, pydantic)
4. Running the Service (uvicorn command)
5. API Endpoints:
   - GET /health (with example curl)
   - POST /score (with example request/response)
6. Scoring Logic (brief explanation of rules and reason codes)
7. Risk Bands (LOW/MEDIUM/HIGH thresholds)
8. Audit Logging (where logs are stored, format)
9. Testing (how to run tests)
10. Example Workflows (end-to-end scenarios)

Include:
- Code blocks for commands and JSON examples
- Clear section headers
- Explanation of reason codes
- Note about synthetic data usage
```

**Expected output**: Copilot generates comprehensive README.

---

## Part 10: Verification and Demo (10 min)

### Step 10.1: Run Complete Workflow

**Execute**:
```bash
# Step 1: Generate synthetic applications
python -m src.samples.synthetic_credit_apps

# Step 2: Start API (in one terminal)
uvicorn src.day1.risk_scoring_service.app:app --reload --port 8000

# Step 3: Run tests (in another terminal)
pytest tests/day1/test_risk_*.py -v

# Step 4: Test API manually
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d @src/samples/sample_credit_apps.json

# Step 5: View audit log
cat src/day1/risk_scoring_service/audit_log.jsonl | jq .
```

**Verification checklist**:
- [ ] Synthetic data generated successfully
- [ ] API starts without errors
- [ ] Health endpoint responds
- [ ] Scoring endpoint accepts valid requests
- [ ] Scoring endpoint rejects invalid requests (422)
- [ ] Responses include all required fields
- [ ] Reason codes are present and meaningful
- [ ] Audit log entries created
- [ ] All tests pass

### Step 10.2: Test Determinism (Critical for Banking)

**Determinism test**:
```bash
# Score same application twice
curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{
    "application_id": "APP-DETERMINISM-TEST",
    "annual_income": 75000,
    "debt": 15000,
    "employment_years": 5,
    "missed_payments_12m": 1,
    "requested_amount": 20000
  }' > result1.json

curl -X POST http://localhost:8000/score \
  -H "Content-Type: application/json" \
  -d '{
    "application_id": "APP-DETERMINISM-TEST",
    "annual_income": 75000,
    "debt": 15000,
    "employment_years": 5,
    "missed_payments_12m": 1,
    "requested_amount": 20000
  }' > result2.json

# Compare (should be identical except request_id)
diff <(jq 'del(.request_id)' result1.json) <(jq 'del(.request_id)' result2.json)
# No output = identical (success!)
```

---

## Part 11: Reflexion (5 min)

### Individual Reflexion

**What did Copilot do well in Lab 2?**
* What code was immediately usable?
* Where did Copilot excel (API setup, tests, models)?

**Where did Copilot need guidance?**
* What needed correction?
* What business logic required clarification?

**How confident are you in this code for production?**
* What additional testing would you add?
* What compliance checks would you add?
* What documentation would you add?

---

## Success Criteria

You've successfully completed Lab 2 if:

- [x] FastAPI application runs without errors
- [x] Health endpoint responds correctly
- [x] Score endpoint validates inputs and returns structured responses
- [x] Scoring logic is deterministic (same input → same output)
- [x] Reason codes explain every score component
- [x] Audit log captures every request
- [x] Unit tests pass (>80% coverage)
- [x] API integration tests pass
- [x] Swagger/OpenAPI docs are accessible
- [x] Documentation is clear and complete

---

## Auditor's Lens: Compliance Evidence

**What would you show an auditor?**

1. **Determinism proof**: Results of determinism test (same input → same output)
2. **Audit trail**: JSONL log with all requests, timestamps, scores, reasons
3. **Explainability**: Reason codes for every decision
4. **Test coverage**: pytest coverage report >80%
5. **Input validation**: Pydantic validation preventing invalid data
6. **API documentation**: Swagger docs showing all endpoints and schemas

**Exercise**: Generate an audit report:
```python
# Create audit report summary
from src.day1.risk_scoring_service.audit import read_audit_log

entries = read_audit_log()
print(f"Total scoring requests: {len(entries)}")
print(f"Risk band distribution:")
print(f"  LOW: {sum(1 for e in entries if e['band'] == 'LOW')}")
print(f"  MEDIUM: {sum(1 for e in entries if e['band'] == 'MEDIUM')}")
print(f"  HIGH: {sum(1 for e in entries if e['band'] == 'HIGH')}")
```

---

## Extension Challenges (Optional)

1. **Add batch scoring**: Endpoint that accepts multiple applications
2. **Add score history**: Store historical scores for an application_id
3. **Add metrics endpoint**: Return statistics (avg score, band distribution)
4. **Add rate limiting**: Prevent abuse with rate limiting middleware
5. **Add authentication**: Add API key authentication
6. **Add model versioning**: Track which scoring logic version was used

---

## What's Next?

Congratulations! You've completed Day 1 labs. You should now:

1. Proceed to **Session 1.3** for wrap-up and reflexion
2. Review both labs and consolidate learnings
3. Prepare questions for Day 2 (Model Context Protocol)

---

**Navigation**:
* [Back to Day 1 README](../README.md)
* [Session 1.3: Verification and Tests](../session1_3_verification_and_tests.md)
* [Lab 1: Data Quality Rules Engine](lab1_data_quality_rules_engine.md)
