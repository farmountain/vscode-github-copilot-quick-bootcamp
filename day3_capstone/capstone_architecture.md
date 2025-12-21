# Capstone Architecture: Credit Decisioning Slice

## Document Control

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0 |
| **Date** | 2025-12-21 |
| **Architect** | Day 3 Capstone Team |
| **Status** | Final |

---

## 1. Architecture Overview

### 1.1 System Context

```
┌─────────────────────────────────────────────────────────────┐
│                   External Actors                            │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Customer   │    │     Risk     │    │   Auditor    │  │
│  │  Application │    │  Analyst     │    │              │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                    │          │
└─────────┼───────────────────┼────────────────────┼──────────┘
          │                   │                    │
          │  HTTP/REST        │  HTTP/REST         │  File Access
          ▼                   ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│         Credit Decisioning Service (FastAPI)                 │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    API Layer                            │ │
│  │  GET /health                                            │ │
│  │  POST /applications                                     │ │
│  │  GET /applications/{id}                                 │ │
│  │  POST /applications/{id}/decision                       │ │
│  │  GET /decisions/{id}                                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                 Business Logic Layer                    │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │ │
│  │  │Validation│  │ Features │  │  Rules   │             │ │
│  │  │          │  │Engineering│  │  Engine  │             │ │
│  │  └──────────┘  └──────────┘  └──────────┘             │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  Data Access Layer                      │ │
│  │  ┌──────────────┐         ┌──────────────┐            │ │
│  │  │  Repository  │         │ Audit Logger │            │ │
│  │  │ (SQLite/JSON)│         │   (JSONL)    │            │ │
│  │  └──────────────┘         └──────────────┘            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
          │                                   │
          ▼                                   ▼
┌─────────────────────┐         ┌─────────────────────┐
│   Applications &    │         │     Audit Log       │
│  Decisions Storage  │         │  (audit_log.jsonl)  │
│  (SQLite or JSON)   │         │                     │
└─────────────────────┘         └─────────────────────┘
```

### 1.2 Design Principles

1. **Separation of Concerns:** API, business logic, and data access are cleanly separated
2. **Dependency Injection:** Configuration and dependencies passed explicitly
3. **Single Responsibility:** Each module has one clear purpose
4. **Testability:** All components can be tested in isolation
5. **Explainability:** Every decision step produces audit trails
6. **Determinism:** No randomness; same input → same output
7. **Data Minimization:** Logs exclude raw PII

---

## 2. Component Architecture

### 2.1 Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      app.py (FastAPI)                        │
│  - Endpoint definitions                                      │
│  - Request/response handling                                 │
│  - Dependency injection setup                                │
└─────────┬──────────────────────────────────────────┬────────┘
          │                                          │
          │                                          │
┌─────────▼──────────┐                   ┌───────────▼─────────┐
│    models.py       │                   │   validation.py     │
│  - Pydantic models │                   │  - Input validation │
│  - Request/response│                   │  - Business rules   │
│    schemas         │                   │    checks           │
└────────────────────┘                   └─────────────────────┘
                                                     │
          ┌──────────────────────────────────────────┤
          │                                          │
┌─────────▼──────────┐                   ┌───────────▼─────────┐
│   features.py      │                   │  rules_engine.py    │
│  - DTI calculation │                   │  - Scoring logic    │
│  - Affordability   │                   │  - Reason codes     │
│  - Feature derivation│──────────────────▶ - Decision bands    │
└────────────────────┘                   └─────────────────────┘
                                                     │
          ┌──────────────────────────────────────────┤
          │                                          │
┌─────────▼──────────┐                   ┌───────────▼─────────┐
│  repository.py     │                   │     audit.py        │
│  - Application CRUD│                   │  - JSONL logging    │
│  - Decision CRUD   │                   │  - PII exclusion    │
│  - Storage abstraction│                 │  - Append-only log  │
└────────────────────┘                   └─────────────────────┘
          │                                          │
          ▼                                          ▼
┌────────────────────┐                   ┌─────────────────────┐
│   SQLite or JSON   │                   │   audit_log.jsonl   │
│  (applications +   │                   │  (decision records) │
│    decisions)      │                   │                     │
└────────────────────┘                   └─────────────────────┘

┌────────────────────┐                   ┌─────────────────────┐
│    config.py       │                   │   sample_data.py    │
│  - Paths           │                   │  - Synthetic data   │
│  - Thresholds      │                   │    generator        │
│  - Repo config     │                   │                     │
└────────────────────┘                   └─────────────────────┘
```

### 2.2 Module Descriptions

#### app.py

**Responsibilities:**

- Define FastAPI application instance
- Implement 5 REST endpoints
- Handle HTTP request/response lifecycle
- Coordinate calls to business logic and data layers

**Key Endpoints:**

- `GET /health` → health check
- `POST /applications` → create application
- `GET /applications/{id}` → retrieve application
- `POST /applications/{id}/decision` → compute decision
- `GET /decisions/{id}` → retrieve decision

**Dependencies:**

- models.py (Pydantic schemas)
- repository.py (data access)
- rules_engine.py (scoring logic)
- audit.py (decision logging)
- config.py (configuration)

#### models.py

**Responsibilities:**

- Define Pydantic models for request/response validation
- Ensure data type safety

**Key Models:**

```python
ApplicationRequest  # POST /applications payload
ApplicationRecord   # Stored application data + metadata
DecisionRecord      # Stored decision data + metadata
ApplicationResponse # GET /applications response
DecisionResponse    # GET /decisions response
```

#### validation.py

**Responsibilities:**

- Business rule validation (e.g., income > 0, DTI thresholds)
- Input sanitation
- Custom validators beyond Pydantic schema validation

**Example Checks:**

- `annual_income` must be > 0
- `requested_amount` must be > 0
- `employment_years` must be >= 0
- `missed_payments_12m` must be >= 0

#### features.py

**Responsibilities:**

- Derive scoring features from raw application data
- Calculate DTI (debt-to-income ratio)
- Calculate affordability proxy
- Extract/transform data for rules engine

**Key Functions:**

```python
def calculate_dti(monthly_debt_payments: float, annual_income: float) -> float:
    """Returns monthly debt / monthly income"""
    
def calculate_affordability_ratio(requested_amount: float, annual_income: float) -> float:
    """Returns requested_amount / annual_income"""
```

#### rules_engine.py

**Responsibilities:**

- Implement deterministic scoring logic
- Generate reason codes for each adjustment
- Map final score to decision outcome (APPROVE/REFER/DECLINE)

**Key Functions:**

```python
def compute_decision(application_data: dict) -> dict:
    """
    Returns:
    {
        "score": int (0-100),
        "outcome": str (APPROVE/REFER/DECLINE),
        "reason_codes": list[str]
    }
    """
```

**Algorithm:**

1. Start with baseline score (50)
2. Apply adjustments based on features:
   - DTI adjustment
   - Payment history adjustment
   - Employment stability adjustment
   - Credit exposure adjustment
3. Clip score to [0, 100]
4. Map score to outcome band
5. Return score + outcome + reason codes (sorted)

#### repository.py

**Responsibilities:**

- Persist and retrieve applications
- Persist and retrieve decisions
- Abstract storage mechanism (SQLite OR file-based JSON)

**Key Functions:**

```python
def create_application(app_data: ApplicationRequest) -> ApplicationRecord
def get_application(application_id: str) -> Optional[ApplicationRecord]
def create_decision(decision_data: dict) -> DecisionRecord
def get_decision(decision_id: str) -> Optional[DecisionRecord]
```

**Storage Options:**

- **Option A (SQLite):** Two tables: `applications`, `decisions`
- **Option B (File-based JSON):** Two directories: `applications/`, `decisions/`

#### audit.py

**Responsibilities:**

- Log decision events to JSONL file
- Exclude raw PII (full_name, address, email)
- Include IDs, scores, outcomes, reason codes, derived features

**Key Functions:**

```python
def log_decision(
    application_id: str,
    decision_id: str,
    outcome: str,
    score: int,
    reason_codes: list[str],
    derived_features: dict
) -> None:
    """Append decision to audit_log.jsonl"""
```

**Audit Log Entry Example:**

```json
{
  "timestamp": "2025-12-21T10:30:45.123Z",
  "request_id": "req-abc123",
  "application_id": "app-xyz789",
  "decision_id": "dec-def456",
  "outcome": "APPROVE",
  "score": 75,
  "reason_codes": ["LOW_DTI", "CLEAN_PAYMENT_HISTORY", "STABLE_EMPLOYMENT", "SCORE_APPROVE_BAND"],
  "dti": 0.22,
  "annual_income": 65000,
  "requested_amount": 15000,
  "missed_payments_12m": 0,
  "employment_years": 5
}
```

#### config.py

**Responsibilities:**

- Centralize configuration (paths, thresholds, repo type)
- Provide defaults with environment variable overrides

**Key Settings:**

```python
AUDIT_LOG_PATH = "out/day3/audit_log.jsonl"
REPO_TYPE = "sqlite"  # or "json"
DB_PATH = "out/day3/credit_decisioning.db"
JSON_STORE_PATH = "out/day3/data/"
SCORE_APPROVE_THRESHOLD = 70
SCORE_REFER_THRESHOLD = 50
```

#### sample_data.py

**Responsibilities:**

- Generate synthetic sample applications
- Include variety: risky, safe, edge cases

**Output Example:**

```json
[
  {
    "full_name": "Alice Safe",
    "annual_income": 80000,
    "monthly_debt_payments": 800,
    "requested_amount": 10000,
    "employment_years": 8,
    "missed_payments_12m": 0,
    "address": "456 Oak St",
    "email": "alice@example.com"
  },
  {
    "full_name": "Bob Risky",
    "annual_income": 30000,
    "monthly_debt_payments": 1200,
    "requested_amount": 20000,
    "employment_years": 1,
    "missed_payments_12m": 5,
    "address": "789 Pine St",
    "email": "bob@example.com"
  }
]
```

---

## 3. Data Flow Diagrams

### 3.1 Submit Application Flow

```
Client                API (app.py)         Models          Repository
  │                        │                  │                │
  │  POST /applications    │                  │                │
  ├───────────────────────▶│                  │                │
  │                        │  Validate (Pydantic)             │
  │                        ├──────────────────▶│                │
  │                        │                  │                │
  │                        │  Generate application_id         │
  │                        │                  │                │
  │                        │  create_application()            │
  │                        ├─────────────────────────────────▶│
  │                        │                  │  Store in DB  │
  │                        │                  │◀───────────────┤
  │                        │  ApplicationRecord               │
  │                        │◀─────────────────────────────────┤
  │                        │                  │                │
  │  201 Created           │                  │                │
  │  {application_id}      │                  │                │
  │◀───────────────────────┤                  │                │
  │                        │                  │                │
```

### 3.2 Compute Decision Flow

```
Client      API         Repository    Features    Rules      Audit
  │          │              │             │        Engine      Log
  │          │              │             │          │         │
  │  POST    │              │             │          │         │
  │ /app/id/ │              │             │          │         │
  │ decision │              │             │          │         │
  ├─────────▶│              │             │          │         │
  │          │ get_application(id)        │          │         │
  │          ├─────────────▶│             │          │         │
  │          │ AppRecord    │             │          │         │
  │          │◀─────────────┤             │          │         │
  │          │              │             │          │         │
  │          │ derive_features()          │          │         │
  │          ├────────────────────────────▶│          │         │
  │          │ {dti, affordability, ...}  │          │         │
  │          │◀────────────────────────────┤          │         │
  │          │              │             │          │         │
  │          │ compute_decision(features)  │          │         │
  │          ├─────────────────────────────────────▶│         │
  │          │ {score, outcome, reasons}  │          │         │
  │          │◀─────────────────────────────────────┤         │
  │          │              │             │          │         │
  │          │ create_decision()          │          │         │
  │          ├─────────────▶│             │          │         │
  │          │ DecisionRecord             │          │         │
  │          │◀─────────────┤             │          │         │
  │          │              │             │          │         │
  │          │ log_decision(id, score, outcome, reasons, features)│
  │          ├──────────────────────────────────────────────────▶│
  │          │              │             │          │  Append  │
  │          │              │             │          │  to JSONL│
  │          │              │             │          │◀─────────┤
  │          │              │             │          │          │
  │  201     │              │             │          │          │
  │  Created │              │             │          │          │
  │ {decision_id, outcome, score, reasons}          │          │
  │◀─────────┤              │             │          │          │
  │          │              │             │          │          │
```

### 3.3 Retrieve Decision Flow

```
Client                API (app.py)              Repository
  │                        │                         │
  │  GET /decisions/{id}   │                         │
  ├───────────────────────▶│                         │
  │                        │  get_decision(id)       │
  │                        ├────────────────────────▶│
  │                        │  DecisionRecord or None │
  │                        │◀────────────────────────┤
  │                        │                         │
  │  200 OK or 404         │                         │
  │  DecisionResponse      │                         │
  │◀───────────────────────┤                         │
  │                        │                         │
```

---

## 4. Data Model

### 4.1 Application Entity

```python
{
  "application_id": "app-uuid",
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

### 4.2 Decision Entity

```python
{
  "decision_id": "dec-uuid",
  "application_id": "app-uuid",
  "outcome": "APPROVE",  # APPROVE | REFER | DECLINE
  "score": 75,           # 0-100
  "reason_codes": [
    "LOW_DTI",
    "CLEAN_PAYMENT_HISTORY",
    "STABLE_EMPLOYMENT",
    "SCORE_APPROVE_BAND"
  ],
  "timestamp": "2025-12-21T10:31:12Z"
}
```

### 4.3 Audit Log Entry

```python
{
  "timestamp": "2025-12-21T10:31:12.123Z",
  "request_id": "req-abc123",
  "application_id": "app-uuid",
  "decision_id": "dec-uuid",
  "outcome": "APPROVE",
  "score": 75,
  "reason_codes": ["LOW_DTI", "CLEAN_PAYMENT_HISTORY", ...],
  "dti": 0.22,
  "annual_income": 65000,
  "requested_amount": 15000,
  "missed_payments_12m": 0,
  "employment_years": 5
}
```

**Note:** No `full_name`, `address`, or `email` in audit log.

---

## 5. Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **API Framework** | FastAPI | Modern, fast, auto-generates OpenAPI docs, Pydantic integration |
| **Data Validation** | Pydantic | Type safety, automatic validation, serialization |
| **Persistence** | SQLite OR JSON files | Lightweight, no external dependencies, suitable for learning |
| **Testing** | pytest + httpx | Standard Python testing, FastAPI TestClient support |
| **Logging** | Python `logging` + custom JSONL | Standard library, simple append-only audit trail |
| **Language** | Python 3.10+ | Modern syntax, widespread banking adoption |

---

## 6. Deployment View (Local Development)

```
┌─────────────────────────────────────────────────────────────┐
│                    Developer Workstation                     │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │               VS Code + Copilot                      │   │
│  │  - Edit code                                         │   │
│  │  - Run tests (pytest)                                │   │
│  │  - Start API (uvicorn)                               │   │
│  │  - View logs and outputs                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │           FastAPI Service (Local)                    │   │
│  │  uvicorn src.day3.credit_decisioning.app:app        │   │
│  │  --reload --host 127.0.0.1 --port 8000               │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Filesystem Storage                      │   │
│  │  out/day3/                                           │   │
│  │    ├── credit_decisioning.db (if SQLite)            │   │
│  │    ├── data/ (if JSON files)                         │   │
│  │    │   ├── applications/                             │   │
│  │    │   └── decisions/                                │   │
│  │    └── audit_log.jsonl                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Access:**

- API: `http://127.0.0.1:8000`
- OpenAPI docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

---

## 7. Security Architecture (Simplified)

| Layer | Security Control | Status in Capstone |
|-------|------------------|--------------------|
| **API** | Authentication/Authorization | ❌ Out of scope (assume internal network) |
| **API** | Input Validation | ✅ Pydantic models + custom validators |
| **API** | Rate Limiting | ❌ Out of scope |
| **Data** | PII Minimization in Logs | ✅ Audit log excludes raw PII |
| **Data** | Encryption at Rest | ❌ Out of scope (file system permissions only) |
| **Data** | Encryption in Transit | ❌ Out of scope (local development uses HTTP) |
| **Audit** | Tamper-Evident Logs | ⚠️ Basic (append-only file; no signing) |
| **Config** | Secrets Management | ❌ Out of scope (no secrets in capstone) |

**Note:** This is a **learning exercise** with synthetic data. Production systems require full security hardening.

---

## 8. Scalability Considerations (Out of Scope for Capstone)

If this system were production-grade, you would add:

1. **Horizontal Scaling:** Load balancer + multiple API instances
2. **Database:** PostgreSQL with connection pooling
3. **Caching:** Redis for frequently accessed applications/decisions
4. **Async Processing:** Message queue (RabbitMQ, Kafka) for decision computations
5. **Distributed Tracing:** OpenTelemetry for observability
6. **Monitoring:** Prometheus + Grafana for metrics and alerts

For the capstone, we keep it **simple and synchronous**.

---

## 9. Design Patterns Applied

| Pattern | Where Used | Purpose |
|---------|------------|---------|
| **Layered Architecture** | API → Business → Data | Separation of concerns |
| **Repository Pattern** | `repository.py` | Abstract storage mechanism |
| **Factory Pattern** | `sample_data.py` | Generate test data |
| **Strategy Pattern** | Rules engine | Pluggable scoring rules (future) |
| **Singleton Pattern** | FastAPI app instance | Single app object |
| **Dependency Injection** | FastAPI dependencies | Pass config/repo to endpoints |

---

## 10. Error Handling Strategy

| Error Type | HTTP Status | Response Example |
|------------|-------------|------------------|
| Validation error (Pydantic) | 422 Unprocessable Entity | `{"detail": [{"loc": ["body", "annual_income"], "msg": "field required"}]}` |
| Resource not found | 404 Not Found | `{"detail": "Application not found"}` |
| Internal server error | 500 Internal Server Error | `{"detail": "Internal server error"}` |
| Invalid request (business logic) | 400 Bad Request | `{"detail": "Income must be positive"}` |

**Error Logging:**

- All errors logged to `logs/api.log` (standard Python logging)
- Audit log only records successful decisions

---

## 11. Testing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Test Pyramid                           │
│                                                              │
│                        ┌─────┐                               │
│                        │ E2E │  (End-to-End Tests)          │
│                        └─────┘                               │
│                      ┌─────────┐                             │
│                      │   API   │  (API Tests)                │
│                      └─────────┘                             │
│                  ┌───────────────┐                           │
│                  │      Unit      │  (Unit Tests)            │
│                  └───────────────┘                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Unit Tests (Base)

- Test individual functions in isolation
- Mock external dependencies
- Fast execution
- Examples: `test_rules_engine.py`, `test_features.py`

### API Tests (Middle)

- Test API endpoints using FastAPI TestClient
- In-memory or test database
- Examples: `test_api_endpoints.py`

### End-to-End Tests (Top)

- Test full workflows: submit → decide → fetch
- Verify audit log entries
- Examples: `test_end_to_end_scenarios.py`

---

## 12. Extensibility Points

Future enhancements could add:

1. **Pluggable Rules Engine:** Load rules from configuration or database
2. **ML Model Integration:** Replace rule-based scoring with ML predictions
3. **External Data Enrichment:** Call credit bureaus, fraud detection APIs
4. **Multi-Tenant Support:** Partition data by organization
5. **Versioned Decisions:** Track rule version used for each decision
6. **Appeal Workflow:** Allow customers to dispute decisions
7. **Real-Time Monitoring:** Dashboard showing approval rates, score distributions

---

## 13. Constraints and Assumptions

### Constraints

- **No real data:** Synthetic only
- **No production security:** Simplified for learning
- **Single-threaded:** Synchronous processing
- **Local deployment:** No cloud infrastructure
- **Simple persistence:** SQLite or file-based JSON

### Assumptions

- **Internal use only:** No authentication required
- **Trusted network:** HTTP (not HTTPS)
- **Small scale:** < 1000 applications in demo
- **Deterministic:** No time-based variations in scoring

---

## 14. Architecture Decision Records (ADRs)

### ADR-1: Use FastAPI for REST API

**Decision:** Use FastAPI instead of Flask or Django.

**Rationale:**

- Modern, fast (ASGI-based)
- Automatic OpenAPI documentation
- Pydantic integration for type safety
- Growing adoption in financial services

**Consequences:**

- Team must learn FastAPI (minimal learning curve)
- Excellent developer experience

---

### ADR-2: Use SQLite or File-Based JSON for Persistence

**Decision:** Support both SQLite and file-based JSON; let user choose.

**Rationale:**

- No external database dependencies (PostgreSQL, MySQL)
- Suitable for learning and local development
- SQLite: structured queries, ACID transactions
- JSON files: simple, human-readable

**Consequences:**

- Not production-grade (no horizontal scaling)
- Sufficient for capstone scope

---

### ADR-3: Use JSONL for Audit Logging

**Decision:** Use JSON Lines (JSONL) format for audit logs.

**Rationale:**

- Each line is a valid JSON object (easy to parse)
- Append-only (sequential writes)
- Standard format in log aggregation tools (Splunk, ELK)
- No complex database schema needed

**Consequences:**

- Must manually manage log rotation (out of scope for capstone)
- Simple grep/jq queries for audit review

---

### ADR-4: Exclude Raw PII from Audit Logs

**Decision:** Audit logs must NOT contain `full_name`, `address`, `email`.

**Rationale:**

- Regulatory best practice (GDPR, CCPA)
- Minimize data exposure in logs
- Audit logs often have wider access than operational databases

**Consequences:**

- Cannot reconstruct full application from audit log alone
- Must join with repository for full context (acceptable)

---

### ADR-5: Deterministic Scoring (No ML)

**Decision:** Use rule-based, deterministic scoring (no machine learning).

**Rationale:**

- Full explainability (every adjustment traceable)
- Reproducible (same input → same output)
- Simpler for teaching purposes
- Easier to audit and validate

**Consequences:**

- Less predictive accuracy than ML models
- Suitable for capstone learning objectives

---

## 15. Architecture Validation Checklist

| Concern | Addressed? | Evidence |
|---------|------------|----------|
| Modularity | ✅ | Clear separation: API, business logic, data |
| Testability | ✅ | Unit, API, and E2E tests |
| Explainability | ✅ | Reason codes for every decision |
| Auditability | ✅ | JSONL audit log with decision trail |
| Data Privacy | ✅ | PII excluded from audit logs |
| Determinism | ✅ | Rule-based scoring, no randomness |
| Extensibility | ✅ | Repository abstraction, pluggable rules (future) |
| Simplicity | ✅ | Minimal dependencies, local deployment |

---

**Next:** Review [capstone_runbook.md](capstone_runbook.md) for operational procedures.
