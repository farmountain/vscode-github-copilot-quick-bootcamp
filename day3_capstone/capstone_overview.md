# Capstone Overview: Credit Decisioning Slice

## Executive Summary

The Day 3 capstone is a **mini end-to-end credit decisioning system** that demonstrates banking-grade engineering practices using VS Code + GitHub Copilot.

You will build a REST API service that:

1. Accepts credit applications
2. Validates and enriches data
3. Computes deterministic decisions using rule-based scoring
4. Returns decisions with **explainable reason codes**
5. Records all decisions in an **audit log** (protecting PII)

This system demonstrates the **complete lifecycle** of a compliance-ready financial service.

---

## System Vision

### The Problem

Banks need to make credit decisions that are:

- **Consistent:** Same inputs always produce same outputs
- **Explainable:** Every decision must have clear reasons
- **Auditable:** Regulatory compliance requires decision trails
- **Safe:** Must protect customer PII
- **Testable:** Must prove correctness under scrutiny

### The Solution

A lightweight **Credit Decisioning Slice** that:

- Uses deterministic rules (no ML black boxes)
- Generates reason codes for every adjustment
- Logs decisions without storing raw PII
- Provides full test coverage
- Includes governance artifacts

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   Credit Decisioning API                  │
│                      (FastAPI Service)                    │
└──────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ Application │      │  Decision   │      │    Audit    │
│ Repository  │      │   Engine    │      │   Logger    │
└─────────────┘      └─────────────┘      └─────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  SQLite or  │      │    Rules    │      │    JSONL    │
│   JSON DB   │      │   + Scores  │      │  Audit Log  │
└─────────────┘      └─────────────┘      └─────────────┘
```

---

## Key Components

### 1. REST API (FastAPI)

Five endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/applications` | POST | Submit new application |
| `/applications/{id}` | GET | Retrieve application |
| `/applications/{id}/decision` | POST | Compute decision |
| `/decisions/{id}` | GET | Retrieve decision record |

### 2. Validation Layer

- Input validation using Pydantic models
- Business rule validation (e.g., income > 0, DTI thresholds)
- Data type enforcement

### 3. Feature Engineering

Derives decision-relevant features:

- **Debt-to-Income (DTI):** `monthly_debt_payments / monthly_income`
- **Affordability:** `requested_amount / (annual_income * affordability_factor)`
- **Stability Score:** Based on employment years and address tenure

### 4. Decision Engine (Rule-Based)

Deterministic scoring algorithm:

```
baseline_score = 50

# Adjustments (each produces a reason code)
- DTI < 0.36: +10 ("LOW_DTI")
- DTI >= 0.36 and < 0.43: +0 (neutral)
- DTI >= 0.43: -15 ("HIGH_DTI")

- No missed payments: +10 ("CLEAN_PAYMENT_HISTORY")
- 1-2 missed payments: -5 ("SOME_MISSED_PAYMENTS")
- 3+ missed payments: -20 ("POOR_PAYMENT_HISTORY")

- Employment > 5 years: +10 ("STABLE_EMPLOYMENT")
- Employment 2-5 years: +5 ("MODERATE_EMPLOYMENT")
- Employment < 2 years: +0

- Requested amount < 30% annual income: +5 ("LOW_CREDIT_EXPOSURE")
- Requested amount >= 50% annual income: -10 ("HIGH_CREDIT_EXPOSURE")

final_score = clip(baseline_score + adjustments, 0, 100)

# Decision bands
- score >= 70: APPROVE
- score >= 50 and < 70: REFER
- score < 50: DECLINE
```

### 5. Reason Codes

Every adjustment generates a **reason code** following the pattern:

- Positive adjustments: e.g., `LOW_DTI`, `CLEAN_PAYMENT_HISTORY`
- Negative adjustments: e.g., `HIGH_DTI`, `POOR_PAYMENT_HISTORY`
- Final decision: e.g., `SCORE_APPROVE_BAND`, `SCORE_DECLINE_BAND`

Reason codes are:

- Stable (deterministic ordering)
- Actionable (customer can understand what to improve)
- Auditable (regulator can trace decision logic)

### 6. Audit Logger

Writes to **JSONL** (JSON Lines) format:

```json
{"timestamp": "2025-12-21T10:30:45Z", "request_id": "req-123", "application_id": "app-456", "decision_id": "dec-789", "outcome": "APPROVE", "score": 75, "reason_codes": ["LOW_DTI", "CLEAN_PAYMENT_HISTORY", "STABLE_EMPLOYMENT", "SCORE_APPROVE_BAND"]}
```

**Critical:** Audit log does NOT contain:

- Full names
- Addresses
- Email addresses
- Other raw PII

It logs only:

- IDs (synthetic)
- Numeric features used in scoring
- Decision outcomes and reason codes

### 7. Repository (Persistence-Lite)

Two options (choose one):

- **SQLite:** Simple relational database (good for structured queries)
- **File-based JSON:** Applications and decisions stored as JSON files

Requirements:

- Support create/read operations
- Deterministic ID generation (UUID4 is fine)
- Stable serialization (for reproducibility)

---

## Data Flow

### Scenario: Submit and Decide on Application

```
1. POST /applications
   → Validate input (Pydantic)
   → Generate application_id
   → Store in repository
   → Return application_id

2. POST /applications/{application_id}/decision
   → Fetch application from repository
   → Extract/derive features (DTI, affordability, etc.)
   → Run rules engine → compute score + reason codes
   → Map score to outcome (APPROVE/REFER/DECLINE)
   → Generate decision_id
   → Store decision in repository
   → Log to audit log (no raw PII)
   → Return decision_id + outcome + reasons

3. GET /decisions/{decision_id}
   → Fetch decision from repository
   → Return full decision record
```

---

## Determinism and Reproducibility

**Why it matters:** In banking, you must be able to **replay decisions** for audit or dispute resolution.

**How we achieve it:**

1. **No randomness:** All rules are deterministic
2. **Stable reason code ordering:** Sorted alphabetically or by rule precedence
3. **Fixed timestamps:** Can use ISO format with millisecond precision
4. **Version-controlled rules:** Decision logic is in code (rules_engine.py)
5. **Idempotent APIs:** Same input → same output

**Verification:**

Run the same application through twice:

```bash
# Request 1
curl -X POST .../applications -d @sample1.json
curl -X POST .../applications/app-123/decision

# Request 2 (identical input)
curl -X POST .../applications -d @sample1.json
curl -X POST .../applications/app-456/decision

# Outcomes, scores, and reason codes MUST match
```

---

## Explainability (Reason Codes)

Reason codes serve three audiences:

### 1. Customer (Applicant)

"Your application was **declined** due to:

- HIGH_DTI (debt-to-income ratio too high)
- POOR_PAYMENT_HISTORY (3+ missed payments in last 12 months)
- SCORE_DECLINE_BAND (final score below threshold)

**Recommendations:** Reduce outstanding debt and maintain timely payments."

### 2. Risk/Compliance Team

"Decision `dec-789` scored `42` due to:

- Baseline: 50
- DTI adjustment: -15 (DTI=0.48)
- Payment history: -20 (missed_payments_12m=4)
- Employment: +5 (employment_years=3)
- Credit exposure: -10 (requested $15k on $25k income)
- Final: 42 → DECLINE"

### 3. Auditor/Regulator

"The decision engine applied the following rule set version `v1.0`:

- Rules are deterministic and documented in `rules_engine.py`
- All reason codes map to specific rule clauses
- No discriminatory features used (no race, gender, etc.)
- Audit log confirms consistent application of rules"

---

## Security and Privacy

### Threat Mitigation

| Threat | Mitigation |
|--------|------------|
| PII leakage in logs | Audit log excludes raw PII; logs only IDs and numeric features |
| Injection attacks | Pydantic validation; no dynamic SQL (if using SQLite, use parameterized queries) |
| Unauthorized access | Out of scope for capstone; assume internal network or future auth layer |
| Audit log tampering | File permissions; future: append-only storage or signed logs |
| Insecure defaults | All config in `config.py`; no hardcoded secrets |

### Data Minimization

- **In memory:** Full application data (for processing)
- **In repository:** Full application + decision records (for retrieval)
- **In audit log:** Only IDs + derived features + decision metadata (no raw PII)

---

## Testing Strategy

### Unit Tests

- Rules engine: test each adjustment produces correct reason codes
- Feature engineering: test DTI, affordability calculations
- Validation: test Pydantic models reject invalid inputs

### API Tests

- Use FastAPI TestClient
- Test each endpoint: success cases + error cases
- Verify response schemas

### End-to-End Tests

- Submit application → compute decision → fetch decision
- Verify reason codes match expected logic
- Check audit log entry created

### Negative Tests

- Invalid inputs (negative income, missing fields)
- Non-existent IDs
- Edge cases (DTI exactly 0.36, score exactly 70)

---

## Governance Artifacts

### 1. Requirements Traceability Matrix

Maps each requirement to:

- Module/file implementing it
- Test file(s) verifying it
- Verification command

### 2. Threat Model

Identifies:

- Attack surfaces (API endpoints, audit log)
- Threats (PII leakage, injection, tampering)
- Mitigations (validation, data minimization, file permissions)
- Test/verification hooks

### 3. Risk Register

Documents:

- Risk description
- Likelihood + impact
- Risk rating (L/M/H)
- Mitigation strategy
- Owner (role)

### 4. Runbook

Covers:

- How to install and run
- How to verify correctness
- How to troubleshoot common issues
- How to create evidence bundle for audit

---

## Success Criteria

Your capstone is **complete** when:

- ✅ All 5 API endpoints work correctly
- ✅ Tests pass (unit + API + end-to-end)
- ✅ Decisions are deterministic and reproducible
- ✅ Reason codes are present and accurate
- ✅ Audit log contains decisions without raw PII
- ✅ Threat model and risk register are documented
- ✅ Requirements map to code and tests
- ✅ Runbook enables independent verification
- ✅ Evidence bundle packages all outputs

---

## Beyond the Capstone

This capstone is a **teaching slice**. In production, you would add:

- **Authentication/Authorization:** OAuth2, JWT, RBAC
- **Model Risk Management:** Bias testing, fairness metrics
- **Real-time Monitoring:** Prometheus, Grafana, alerts
- **Distributed Tracing:** OpenTelemetry for observability
- **Shadow Decisioning:** Compare new models against baseline
- **Regulatory Reporting:** Automated report generation
- **Data Lineage:** Track data provenance and transformations

But the **core principles** remain:

- Determinism + explainability
- Audit trails + data protection
- Requirements traceability + test coverage
- Governance artifacts + runbooks

---

**Next:** Review [capstone_requirements.md](capstone_requirements.md) for detailed specifications.
