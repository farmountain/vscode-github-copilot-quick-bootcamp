# Capstone Requirements: Credit Decisioning Slice

## Document Control

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0 |
| **Date** | 2025-12-21 |
| **Owner** | Day 3 Capstone Team |
| **Status** | Final |

---

## 1. In-Scope vs. Out-of-Scope

### ✅ In Scope

1. **FastAPI REST service** with 5 endpoints
2. **Deterministic decision engine** (rule-based scoring)
3. **Reason codes** for every decision
4. **Audit logging** (JSONL format, no raw PII)
5. **Simple persistence** (SQLite OR file-based JSON)
6. **Synthetic sample data** generation
7. **Test suite** (unit + API + end-to-end)
8. **Governance artifacts** (threat model, risk register, traceability matrix)
9. **Runbook** for installation, verification, troubleshooting
10. **Evidence bundle** packaging script

### ❌ Out of Scope

1. Real customer data or production credit policies
2. Machine learning models or bias mitigation algorithms
3. Authentication/authorization (OAuth2, JWT, etc.)
4. Production security hardening (WAF, rate limiting, etc.)
5. Distributed systems, horizontal scaling, load balancing
6. Real-time fraud detection or external data enrichment
7. Regulatory reporting or compliance certification
8. User interface (web frontend)

---

## 2. Functional Requirements

### FR-1: Health Check Endpoint

- **ID:** FR-1
- **Description:** API must provide a health check endpoint
- **Acceptance Criteria:**
  - `GET /health` returns HTTP 200
  - Response body: `{"status": "ok"}`
- **Priority:** P0 (must have)

### FR-2: Submit Application

- **ID:** FR-2
- **Description:** Accept credit application submissions via API
- **Acceptance Criteria:**
  - `POST /applications` accepts JSON payload
  - Validates required fields: `full_name`, `annual_income`, `monthly_debt_payments`, `requested_amount`, `employment_years`, `missed_payments_12m`
  - Generates unique `application_id` (UUID4 or similar)
  - Stores application in repository
  - Returns HTTP 201 with `application_id`
- **Priority:** P0

### FR-3: Retrieve Application

- **ID:** FR-3
- **Description:** Fetch application details by ID
- **Acceptance Criteria:**
  - `GET /applications/{application_id}` returns full application record
  - Returns HTTP 200 if found
  - Returns HTTP 404 if not found
- **Priority:** P0

### FR-4: Compute Decision

- **ID:** FR-4
- **Description:** Compute credit decision for a given application
- **Acceptance Criteria:**
  - `POST /applications/{application_id}/decision` triggers decision engine
  - Fetches application from repository
  - Derives features: DTI, affordability, etc.
  - Runs rules engine → computes score + reason codes
  - Maps score to outcome: APPROVE (score >= 70), REFER (50-69), DECLINE (< 50)
  - Generates unique `decision_id`
  - Stores decision in repository
  - Logs decision to audit log (no raw PII)
  - Returns HTTP 201 with `decision_id`, `outcome`, `score`, `reason_codes`
- **Priority:** P0

### FR-5: Retrieve Decision

- **ID:** FR-5
- **Description:** Fetch decision details by ID
- **Acceptance Criteria:**
  - `GET /decisions/{decision_id}` returns full decision record
  - Includes `application_id`, `outcome`, `score`, `reason_codes`, `timestamp`
  - Returns HTTP 200 if found
  - Returns HTTP 404 if not found
- **Priority:** P0

### FR-6: Deterministic Scoring

- **ID:** FR-6
- **Description:** Decision engine must produce consistent results
- **Acceptance Criteria:**
  - Same application data → same score, outcome, reason codes
  - No randomness or timestamps in scoring logic
  - Reason codes in stable order (sorted or by rule precedence)
- **Priority:** P0

### FR-7: Reason Codes

- **ID:** FR-7
- **Description:** Every decision must include explainable reason codes
- **Acceptance Criteria:**
  - Each scoring adjustment generates a reason code
  - Final outcome generates a reason code (e.g., `SCORE_APPROVE_BAND`)
  - Reason codes are human-readable strings (uppercase, underscores)
  - Example: `["LOW_DTI", "CLEAN_PAYMENT_HISTORY", "STABLE_EMPLOYMENT", "SCORE_APPROVE_BAND"]`
- **Priority:** P0

### FR-8: Audit Logging

- **ID:** FR-8
- **Description:** Log all decisions to an audit trail
- **Acceptance Criteria:**
  - Audit log format: JSONL (one JSON object per line)
  - Each entry includes: `timestamp`, `request_id`, `application_id`, `decision_id`, `outcome`, `score`, `reason_codes`
  - Audit log does NOT include raw PII (`full_name`, `address`, `email`)
  - Audit log includes derived features used in scoring (DTI, income, etc.)
  - Default location: `out/day3/audit_log.jsonl`
- **Priority:** P0

### FR-9: Synthetic Sample Data

- **ID:** FR-9
- **Description:** Provide sample applications for testing
- **Acceptance Criteria:**
  - Generator creates 10+ sample applications
  - Includes variety: some risky (low score), some safe (high score)
  - Output to `out/day3/sample_requests.json` or similar
- **Priority:** P1 (should have)

### FR-10: Repository Operations

- **ID:** FR-10
- **Description:** Persist applications and decisions
- **Acceptance Criteria:**
  - Choose ONE: SQLite OR file-based JSON store
  - Support create and read operations for applications
  - Support create and read operations for decisions
  - IDs are deterministic (UUID4 is acceptable)
  - Data can be retrieved for verification
- **Priority:** P0

---

## 3. Non-Functional Requirements

### NFR-1: Determinism

- **ID:** NFR-1
- **Description:** System must produce reproducible results
- **Acceptance Criteria:**
  - Same input → same output (score, outcome, reason codes)
  - No random number generation in decision logic
  - Timestamps do not affect scores
- **Priority:** P0

### NFR-2: Explainability

- **ID:** NFR-2
- **Description:** Decisions must be fully explainable
- **Acceptance Criteria:**
  - Reason codes map to specific rule logic
  - Score breakdown can be reconstructed from reason codes
  - Audit log enables decision replay
- **Priority:** P0

### NFR-3: Data Privacy

- **ID:** NFR-3
- **Description:** Protect customer PII in logs
- **Acceptance Criteria:**
  - Audit log excludes `full_name`, `address`, `email`
  - Only IDs and numeric features logged
  - Repository may store full data (for retrieval), but logs must not
- **Priority:** P0

### NFR-4: Testability

- **ID:** NFR-4
- **Description:** System must be fully testable
- **Acceptance Criteria:**
  - Unit tests for rules engine (each adjustment)
  - API tests using FastAPI TestClient
  - End-to-end scenario tests
  - All tests pass with `pytest`
- **Priority:** P0

### NFR-5: Performance (Basic)

- **ID:** NFR-5
- **Description:** System should respond quickly for demo purposes
- **Acceptance Criteria:**
  - API endpoints respond in < 1 second for typical requests
  - No performance tuning required (this is a learning exercise)
- **Priority:** P2 (nice to have)

---

## 4. API Contract Summary

### Endpoint: GET /health

**Request:**

```
GET /health
```

**Response (200 OK):**

```json
{
  "status": "ok"
}
```

---

### Endpoint: POST /applications

**Request:**

```http
POST /applications
Content-Type: application/json

{
  "full_name": "Jane Doe",
  "annual_income": 65000,
  "monthly_debt_payments": 1200,
  "requested_amount": 15000,
  "employment_years": 5,
  "missed_payments_12m": 0,
  "address": "123 Main St, Springfield",
  "email": "jane.doe@example.com"
}
```

**Response (201 Created):**

```json
{
  "application_id": "app-a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

---

### Endpoint: GET /applications/{application_id}

**Request:**

```
GET /applications/app-a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

**Response (200 OK):**

```json
{
  "application_id": "app-a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "full_name": "Jane Doe",
  "annual_income": 65000,
  "monthly_debt_payments": 1200,
  "requested_amount": 15000,
  "employment_years": 5,
  "missed_payments_12m": 0,
  "address": "123 Main St, Springfield",
  "email": "jane.doe@example.com",
  "created_at": "2025-12-21T10:30:45Z"
}
```

**Response (404 Not Found):**

```json
{
  "detail": "Application not found"
}
```

---

### Endpoint: POST /applications/{application_id}/decision

**Request:**

```
POST /applications/app-a1b2c3d4-e5f6-7890-abcd-ef1234567890/decision
```

**Response (201 Created):**

```json
{
  "decision_id": "dec-f1e2d3c4-b5a6-7890-cdef-ab1234567890",
  "application_id": "app-a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "outcome": "APPROVE",
  "score": 75,
  "reason_codes": [
    "CLEAN_PAYMENT_HISTORY",
    "LOW_CREDIT_EXPOSURE",
    "LOW_DTI",
    "SCORE_APPROVE_BAND",
    "STABLE_EMPLOYMENT"
  ],
  "timestamp": "2025-12-21T10:31:12Z"
}
```

**Response (404 Not Found):**

```json
{
  "detail": "Application not found"
}
```

---

### Endpoint: GET /decisions/{decision_id}

**Request:**

```
GET /decisions/dec-f1e2d3c4-b5a6-7890-cdef-ab1234567890
```

**Response (200 OK):**

```json
{
  "decision_id": "dec-f1e2d3c4-b5a6-7890-cdef-ab1234567890",
  "application_id": "app-a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "outcome": "APPROVE",
  "score": 75,
  "reason_codes": [
    "CLEAN_PAYMENT_HISTORY",
    "LOW_CREDIT_EXPOSURE",
    "LOW_DTI",
    "SCORE_APPROVE_BAND",
    "STABLE_EMPLOYMENT"
  ],
  "timestamp": "2025-12-21T10:31:12Z"
}
```

**Response (404 Not Found):**

```json
{
  "detail": "Decision not found"
}
```

---

## 5. Decision Engine Rules

### Baseline Score

```
baseline_score = 50
```

### Scoring Adjustments

Each adjustment generates a **reason code**:

| Condition | Adjustment | Reason Code |
|-----------|------------|-------------|
| DTI < 0.36 | +10 | `LOW_DTI` |
| DTI >= 0.36 and < 0.43 | +0 | *(no reason code)* |
| DTI >= 0.43 | -15 | `HIGH_DTI` |
| missed_payments_12m == 0 | +10 | `CLEAN_PAYMENT_HISTORY` |
| missed_payments_12m in [1, 2] | -5 | `SOME_MISSED_PAYMENTS` |
| missed_payments_12m >= 3 | -20 | `POOR_PAYMENT_HISTORY` |
| employment_years > 5 | +10 | `STABLE_EMPLOYMENT` |
| employment_years in [2, 5] | +5 | `MODERATE_EMPLOYMENT` |
| employment_years < 2 | +0 | *(no reason code)* |
| requested_amount < (annual_income * 0.30) | +5 | `LOW_CREDIT_EXPOSURE` |
| requested_amount >= (annual_income * 0.50) | -10 | `HIGH_CREDIT_EXPOSURE` |
| *(otherwise)* | +0 | *(no reason code)* |

### Final Score

```python
final_score = max(0, min(100, baseline_score + sum(adjustments)))
```

### Decision Bands

| Score Range | Outcome | Reason Code |
|-------------|---------|-------------|
| >= 70 | APPROVE | `SCORE_APPROVE_BAND` |
| >= 50 and < 70 | REFER | `SCORE_REFER_BAND` |
| < 50 | DECLINE | `SCORE_DECLINE_BAND` |

---

## 6. Audit Log Requirements

### Format: JSONL (JSON Lines)

Each line is a valid JSON object:

```jsonl
{"timestamp": "2025-12-21T10:30:45.123Z", "request_id": "req-abc123", "application_id": "app-xyz789", "decision_id": "dec-def456", "outcome": "APPROVE", "score": 75, "reason_codes": ["LOW_DTI", "CLEAN_PAYMENT_HISTORY", "STABLE_EMPLOYMENT", "SCORE_APPROVE_BAND"], "dti": 0.22, "annual_income": 65000, "requested_amount": 15000, "missed_payments_12m": 0, "employment_years": 5}
```

### Required Fields

- `timestamp` (ISO 8601 format)
- `request_id` (generated per request)
- `application_id`
- `decision_id`
- `outcome` (APPROVE | REFER | DECLINE)
- `score` (0-100)
- `reason_codes` (array of strings)

### Optional Fields (Derived Features)

- `dti` (debt-to-income ratio)
- `annual_income` (numeric)
- `requested_amount` (numeric)
- `missed_payments_12m` (numeric)
- `employment_years` (numeric)

### Excluded Fields (Raw PII)

- `full_name`
- `address`
- `email`
- `phone_number`
- `ssn`

---

## 7. Test Plan and Acceptance Criteria

### Unit Tests

| Test ID | Test Description | Expected Result |
|---------|------------------|-----------------|
| UT-1 | DTI < 0.36 → score +10, reason code `LOW_DTI` | Pass |
| UT-2 | DTI >= 0.43 → score -15, reason code `HIGH_DTI` | Pass |
| UT-3 | missed_payments_12m == 0 → +10, `CLEAN_PAYMENT_HISTORY` | Pass |
| UT-4 | missed_payments_12m >= 3 → -20, `POOR_PAYMENT_HISTORY` | Pass |
| UT-5 | employment_years > 5 → +10, `STABLE_EMPLOYMENT` | Pass |
| UT-6 | requested_amount < 30% income → +5, `LOW_CREDIT_EXPOSURE` | Pass |
| UT-7 | Score >= 70 → APPROVE, `SCORE_APPROVE_BAND` | Pass |
| UT-8 | Score < 50 → DECLINE, `SCORE_DECLINE_BAND` | Pass |

### API Tests

| Test ID | Test Description | Expected Result |
|---------|------------------|-----------------|
| AT-1 | GET /health returns 200 OK | Pass |
| AT-2 | POST /applications with valid data returns 201 + application_id | Pass |
| AT-3 | POST /applications with missing fields returns 422 | Pass |
| AT-4 | GET /applications/{id} returns 200 + application data | Pass |
| AT-5 | GET /applications/{invalid_id} returns 404 | Pass |
| AT-6 | POST /applications/{id}/decision returns 201 + decision | Pass |
| AT-7 | GET /decisions/{id} returns 200 + decision data | Pass |
| AT-8 | GET /decisions/{invalid_id} returns 404 | Pass |

### End-to-End Tests

| Test ID | Test Description | Expected Result |
|---------|------------------|-----------------|
| E2E-1 | Submit application → compute decision → fetch decision | All endpoints return expected data |
| E2E-2 | Submit risky application → expect DECLINE | outcome == DECLINE, score < 50 |
| E2E-3 | Submit safe application → expect APPROVE | outcome == APPROVE, score >= 70 |
| E2E-4 | Verify reason codes match scoring logic | Reason codes present and accurate |
| E2E-5 | Verify audit log entry created | JSONL file contains decision entry |

### Negative Tests

| Test ID | Test Description | Expected Result |
|---------|------------------|-----------------|
| NT-1 | Submit application with negative income | 422 Unprocessable Entity |
| NT-2 | Submit application with missing required field | 422 Unprocessable Entity |
| NT-3 | Compute decision for non-existent application | 404 Not Found |
| NT-4 | Fetch non-existent decision | 404 Not Found |
| NT-5 | Edge case: DTI exactly 0.36 | Neutral adjustment (no penalty) |
| NT-6 | Edge case: score exactly 70 | outcome == APPROVE |

---

## 8. Requirements Traceability Matrix

| Requirement ID | Description | Module/File | Test File(s) | Verification Command |
|----------------|-------------|-------------|--------------|----------------------|
| FR-1 | Health check endpoint | [src/day3/credit_decisioning/app.py](../src/day3/credit_decisioning/app.py#L19) | [tests/day3/test_api_endpoints.py](../tests/day3/test_api_endpoints.py) | `pytest tests/day3/test_api_endpoints.py::test_health_check -v` |
| FR-2 | Submit application | [app.py](../src/day3/credit_decisioning/app.py#L23), [models.py](../src/day3/credit_decisioning/models.py#L10), [repository.py](../src/day3/credit_decisioning/repository.py#L30) | [tests/day3/test_api_endpoints.py](../tests/day3/test_api_endpoints.py) | `pytest tests/day3/test_api_endpoints.py::test_create_application -v` |
| FR-3 | Retrieve application | [app.py](../src/day3/credit_decisioning/app.py#L36), [repository.py](../src/day3/credit_decisioning/repository.py#L58) | [tests/day3/test_api_endpoints.py](../tests/day3/test_api_endpoints.py) | `pytest tests/day3/test_api_endpoints.py::test_get_application -v` |
| FR-4 | Compute decision | [app.py](../src/day3/credit_decisioning/app.py#L47), [rules_engine.py](../src/day3/credit_decisioning/rules_engine.py#L10), [features.py](../src/day3/credit_decisioning/features.py#L10), [audit.py](../src/day3/credit_decisioning/audit.py#L10) | [tests/day3/test_api_endpoints.py](../tests/day3/test_api_endpoints.py) | `pytest tests/day3/test_api_endpoints.py::test_compute_decision -v` |
| FR-5 | Retrieve decision | [app.py](../src/day3/credit_decisioning/app.py#L80), [repository.py](../src/day3/credit_decisioning/repository.py#L130) | [tests/day3/test_api_endpoints.py](../tests/day3/test_api_endpoints.py) | `pytest tests/day3/test_api_endpoints.py::test_get_decision -v` |
| FR-6 | Deterministic scoring | [rules_engine.py](../src/day3/credit_decisioning/rules_engine.py#L10) | [tests/day3/test_rules_engine.py](../tests/day3/test_rules_engine.py) | `pytest tests/day3/test_rules_engine.py::test_determinism -v` |
| FR-7 | Reason codes | [rules_engine.py](../src/day3/credit_decisioning/rules_engine.py#L10) | [tests/day3/test_rules_engine.py](../tests/day3/test_rules_engine.py) | `pytest tests/day3/test_rules_engine.py -v -k reason` |
| FR-8 | Audit logging | [audit.py](../src/day3/credit_decisioning/audit.py#L10) | [tests/day3/test_end_to_end_scenarios.py](../tests/day3/test_end_to_end_scenarios.py) | `pytest tests/day3/test_end_to_end_scenarios.py::test_audit_log_entry_created -v` |
| FR-9 | Synthetic sample data | [sample_data.py](../src/day3/credit_decisioning/sample_data.py) | *(manual verification)* | `python -m src.day3.credit_decisioning.sample_data` |
| FR-10 | Repository operations | [repository.py](../src/day3/credit_decisioning/repository.py) | [tests/day3/test_repository.py](../tests/day3/test_repository.py) | `pytest tests/day3/test_repository.py -v` |
| NFR-1 | Determinism | [rules_engine.py](../src/day3/credit_decisioning/rules_engine.py#L10) | [tests/day3/test_rules_engine.py](../tests/day3/test_rules_engine.py) | `pytest tests/day3/test_rules_engine.py::test_determinism -v` |
| NFR-2 | Explainability | [rules_engine.py](../src/day3/credit_decisioning/rules_engine.py#L10) | [tests/day3/test_rules_engine.py](../tests/day3/test_rules_engine.py) | `pytest tests/day3/test_rules_engine.py -v -k reason` |
| NFR-3 | Data privacy | [audit.py](../src/day3/credit_decisioning/audit.py#L10) | [tests/day3/test_end_to_end_scenarios.py](../tests/day3/test_end_to_end_scenarios.py) | `pytest tests/day3/test_end_to_end_scenarios.py::test_audit_log_no_pii -v` |
| NFR-4 | Testability | [tests/day3/](../tests/day3/) (all test files) | All tests | `pytest tests/day3/ -v` |

---

## 9. Acceptance Criteria Summary

The capstone is **COMPLETE** when:

1. ✅ All 5 API endpoints are implemented and working
2. ✅ Decision engine produces deterministic scores and outcomes
3. ✅ Every decision includes accurate reason codes
4. ✅ Audit log records decisions without raw PII
5. ✅ Repository supports create/read for applications and decisions
6. ✅ All unit tests pass (rules engine, features, validation)
7. ✅ All API tests pass (endpoints, error handling)
8. ✅ All end-to-end tests pass (submit → decide → fetch)
9. ✅ Negative tests pass (invalid inputs, edge cases)
10. ✅ Synthetic sample data generator works
11. ✅ Threat model and risk register are documented
12. ✅ Requirements map to code and tests (traceability matrix)
13. ✅ Runbook enables independent installation and verification
14. ✅ Evidence bundle can be created and reviewed

---

## 10. Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-21 | Capstone Team | Initial requirements document |

---

**Next:** Review [capstone_architecture.md](capstone_architecture.md) for design details.
