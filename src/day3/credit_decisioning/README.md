# Credit Decisioning Service

## Overview

A deterministic credit decisioning API built with FastAPI that provides explainable credit decisions with reason codes, audit logging, and comprehensive test coverage.

## Features

- **5 REST Endpoints**: Health check, applications CRUD, decisions
- **Deterministic Scoring**: Rule-based decision engine with no randomness
- **Reason Codes**: Every decision includes explainable reason codes
- **Audit Logging**: JSONL format audit trail (no raw PII)
- **SQLite Persistence**: Simple, reliable storage
- **Comprehensive Tests**: Unit, API, and end-to-end test suites

## Installation

```powershell
# Install dependencies
pip install fastapi uvicorn pydantic pytest httpx
```

## Running the Service

```powershell
# Start API server with auto-reload
uvicorn src.day3.credit_decisioning.app:app --reload
```

### Access Points

- **API Base**: http://127.0.0.1:8000
- **OpenAPI Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

## Running Tests

```powershell
# Run all Day 3 tests
pytest tests/day3/ -v

# Run specific test modules
pytest tests/day3/test_rules_engine.py -v
pytest tests/day3/test_api_endpoints.py -v
pytest tests/day3/test_end_to_end_scenarios.py -v
```

## Generating Sample Data

```powershell
# Generate synthetic sample applications
python -m src.day3.credit_decisioning.sample_data
```

Output: `out/day3/sample_requests.json`

## Running Demo

```powershell
# Ensure API is running first, then:
python src/day3/credit_decisioning/demo_e2e.py
```

## Quick Verification

```powershell
# Health check
Invoke-WebRequest -Uri http://127.0.0.1:8000/health

# View audit log
Get-Content out/day3/audit_log.jsonl

# Check database
sqlite3 out/day3/credit_decisioning.db "SELECT COUNT(*) FROM applications;"
```

## API Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{"status": "ok"}
```

### POST /applications

Submit a new credit application.

**Request Body:**
```json
{
  "full_name": "Jane Doe",
  "annual_income": 65000,
  "monthly_debt_payments": 1200,
  "requested_amount": 15000,
  "employment_years": 5,
  "missed_payments_12m": 0,
  "address": "123 Main St",
  "email": "jane@example.com"
}
```

**Response (201 Created):**
```json
{
  "application_id": "app-<uuid>"
}
```

### GET /applications/{application_id}

Retrieve an application by ID.

**Response (200 OK):**
```json
{
  "application_id": "app-<uuid>",
  "full_name": "Jane Doe",
  "annual_income": 65000,
  ...
}
```

### POST /applications/{application_id}/decision

Compute credit decision for an application.

**Response (201 Created):**
```json
{
  "decision_id": "dec-<uuid>",
  "application_id": "app-<uuid>",
  "outcome": "APPROVE",
  "score": 75,
  "reason_codes": [
    "CLEAN_PAYMENT_HISTORY",
    "LOW_DTI",
    "STABLE_EMPLOYMENT",
    "SCORE_APPROVE_BAND"
  ],
  "timestamp": "2025-12-21T10:45:00Z"
}
```

### GET /decisions/{decision_id}

Retrieve a decision by ID.

**Response (200 OK):**
```json
{
  "decision_id": "dec-<uuid>",
  ...
}
```

## Decision Logic

### Scoring Algorithm

1. **Baseline Score**: 50
2. **Adjustments** based on:
   - Debt-to-Income Ratio (DTI)
   - Payment History
   - Employment Stability
   - Credit Exposure
3. **Final Score**: Clipped to [0, 100]
4. **Outcome Bands**:
   - APPROVE: score >= 70
   - REFER: score >= 50 and < 70
   - DECLINE: score < 50

### Reason Codes

Every adjustment produces a reason code:

- `LOW_DTI`: DTI < 0.36 (+10)
- `HIGH_DTI`: DTI >= 0.43 (-15)
- `CLEAN_PAYMENT_HISTORY`: No missed payments (+10)
- `POOR_PAYMENT_HISTORY`: 3+ missed payments (-20)
- `STABLE_EMPLOYMENT`: > 5 years (+10)
- `LOW_CREDIT_EXPOSURE`: Requested < 30% income (+5)
- `HIGH_CREDIT_EXPOSURE`: Requested >= 50% income (-10)
- `SCORE_APPROVE_BAND`, `SCORE_REFER_BAND`, `SCORE_DECLINE_BAND`

## Architecture

See [/day3_capstone/capstone_architecture.md](../../day3_capstone/capstone_architecture.md)

## Requirements

See [/day3_capstone/capstone_requirements.md](../../day3_capstone/capstone_requirements.md)

## Runbook

See [/day3_capstone/capstone_runbook.md](../../day3_capstone/capstone_runbook.md)

## Governance

- **Threat Model**: [/day3_capstone/threat_model.md](../../day3_capstone/threat_model.md)
- **Risk Register**: [/day3_capstone/risk_register.md](../../day3_capstone/risk_register.md)

## Troubleshooting

### Port Already in Use

```powershell
# Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port
uvicorn src.day3.credit_decisioning.app:app --reload --port 8001
```

### Module Not Found

```powershell
# Ensure dependencies are installed
pip install fastapi uvicorn pydantic pytest httpx

# Verify Python path includes project root
$env:PYTHONPATH = (Get-Location).Path
```

### Audit Log Not Created

```powershell
# Create output directory manually
New-Item -ItemType Directory -Force -Path out/day3
```

## License

See [LICENSE](../../../LICENSE)

## Related Materials

- [Day 3 Lab Guide](../../day3_capstone/labs/capstone_build_credit_decisioning_slice.md)
- [Day 3 Prompts](../../day3_capstone/prompts/day3_prompts.md)
- [Training TOC](../../TRAINING_TOC.md)
