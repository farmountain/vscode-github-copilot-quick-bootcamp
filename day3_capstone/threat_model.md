# Threat Model: Credit Decisioning Service

## Document Control

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0 |
| **Date** | 2025-12-21 |
| **Owner** | Day 3 Capstone Security Team |
| **Classification** | Internal Training |

---

## 1. System Overview

The Credit Decisioning Service is a FastAPI-based application that:

- Accepts credit applications via REST API
- Computes deterministic credit decisions using rule-based scoring
- Returns explainable reason codes for every decision
- Logs decisions to an audit trail (JSONL format)
- Persists applications and decisions in SQLite database

**Context:** This is a learning exercise using synthetic data only. The threat model reflects realistic banking considerations but assumes simplified deployment (local development, no production security hardening).

---

## 2. Assets to Protect

### 2.1 Data Assets

| Asset | Description | Sensitivity | Protection Goal |
|-------|-------------|-------------|-----------------|
| **Application Data** | Customer PII (name, address, email, income, debt) | HIGH | Confidentiality |
| **Decision Records** | Outcomes, scores, reason codes | MEDIUM | Integrity, Availability |
| **Audit Log** | Decision trail for compliance | HIGH | Integrity, Availability |
| **Database** | SQLite file with applications and decisions | HIGH | Confidentiality, Integrity |

### 2.2 Code Assets

| Asset | Description | Sensitivity | Protection Goal |
|-------|-------------|-------------|-----------------|
| **Rules Engine** | Decision logic and thresholds | MEDIUM | Integrity, Confidentiality |
| **API Endpoints** | Service interface | MEDIUM | Availability |

---

## 3. Threat Actors

### Internal Threats

- **Malicious Developer**: Could modify rules or access data
- **Curious Analyst**: May attempt to extract PII from logs
- **Misconfigured System**: Unintentional exposure (e.g., audit log published publicly)

### External Threats (Out of Scope for Capstone)

- **External Attackers**: Network-level attacks (assumes internal network for training)
- **DDoS**: Availability attacks (no rate limiting implemented)

---

## 4. Attack Surfaces

### 4.1 API Endpoints

**Exposure:**

- 5 REST endpoints exposed on `http://127.0.0.1:8000`
- No authentication/authorization

**Attack Vectors:**

- API abuse (unlimited requests)
- Injection attacks (SQL injection, input manipulation)
- Enumeration (guessing IDs)

### 4.2 Data Storage

**Exposure:**

- SQLite database file: `out/day3/credit_decisioning.db`
- Audit log file: `out/day3/audit_log.jsonl`

**Attack Vectors:**

- File system access (if attacker gains local access)
- Database corruption
- Audit log tampering

### 4.3 Input Validation

**Exposure:**

- User-controlled input (application data)

**Attack Vectors:**

- Negative numbers (e.g., negative income)
- Extreme values (e.g., `income = float('inf')`)
- SQL injection via string fields
- Script injection via string fields

---

## 5. Threat Scenarios

### T-1: PII Leakage via Audit Logs

**Threat:** Audit log accidentally includes raw PII (full_name, address, email), violating data minimization principles.

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Likelihood** | MEDIUM |
| **Impact** | Compliance violation, privacy breach |
| **Attack Vector** | Developer error in `audit.py` logs full application record instead of derived features |
| **Mitigation** | `audit.py` explicitly excludes PII fields; logs only IDs and numeric features |
| **Status** | ✅ Mitigated |
| **Verification** | `pytest tests/day3/test_end_to_end_scenarios.py::test_audit_log_no_pii` |
| **Reference** | [src/day3/credit_decisioning/audit.py](../src/day3/credit_decisioning/audit.py) |

---

### T-2: SQL Injection

**Threat:** Attacker injects SQL code via input fields (e.g., `full_name = "'; DROP TABLE applications; --"`).

| Attribute | Value |
|-----------|-------|
| **Severity** | CRITICAL |
| **Likelihood** | LOW (Pydantic validation + parameterized queries) |
| **Impact** | Data loss, unauthorized access |
| **Attack Vector** | Malicious input in POST /applications |
| **Mitigation** | Parameterized queries in `repository.py` (no string concatenation); Pydantic validation for data types |
| **Status** | ✅ Mitigated |
| **Verification** | Code review of `repository.py`; all queries use `?` placeholders |
| **Reference** | [src/day3/credit_decisioning/repository.py](../src/day3/credit_decisioning/repository.py#L30) |

---

### T-3: API Abuse (No Rate Limiting)

**Threat:** Attacker floods API with requests, causing denial of service or resource exhaustion.

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Likelihood** | HIGH (no rate limiting) |
| **Impact** | Service unavailability, resource exhaustion |
| **Attack Vector** | Unlimited POST requests to `/applications` or `/applications/{id}/decision` |
| **Mitigation** | OUT OF SCOPE for capstone (would require rate limiting middleware, e.g., slowapi) |
| **Status** | ⚠️ Accepted Risk (training exercise) |
| **Verification** | N/A |
| **Recommendation** | In production: implement rate limiting (e.g., 100 requests/minute per IP) |

---

### T-4: Unauthorized Access (No Authentication)

**Threat:** Anyone with network access can submit applications, compute decisions, and retrieve records.

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Likelihood** | HIGH (no auth implemented) |
| **Impact** | Unauthorized decision generation, data access |
| **Attack Vector** | Direct API calls without credentials |
| **Mitigation** | OUT OF SCOPE for capstone (would require OAuth2, JWT, API keys) |
| **Status** | ⚠️ Accepted Risk (internal training network assumed) |
| **Verification** | N/A |
| **Recommendation** | In production: implement OAuth2 with role-based access control (RBAC) |

---

### T-5: Input Validation Bypass

**Threat:** Attacker submits invalid data that bypasses validation, causing incorrect decisions or crashes.

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Likelihood** | LOW (Pydantic validation enforced) |
| **Impact** | Incorrect decisions, service crash |
| **Attack Vector** | Edge cases (e.g., `annual_income = 0`, `missed_payments_12m = -1`) |
| **Mitigation** | Pydantic Field validators enforce `gt=0`, `ge=0` constraints; FastAPI returns 422 for invalid input |
| **Status** | ✅ Mitigated |
| **Verification** | `pytest tests/day3/test_api_endpoints.py::test_create_application_invalid_income` |
| **Reference** | [src/day3/credit_decisioning/models.py](../src/day3/credit_decisioning/models.py#L10) |

---

### T-6: Audit Log Tampering

**Threat:** Attacker modifies or deletes audit log entries to hide fraudulent activity.

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Likelihood** | MEDIUM (file system access required) |
| **Impact** | Loss of audit trail, compliance violation |
| **Attack Vector** | Direct file system access to `out/day3/audit_log.jsonl` |
| **Mitigation** | PARTIAL: File permissions restrict access (depends on OS); append-only design |
| **Status** | ⚠️ Partially Mitigated (basic file permissions) |
| **Verification** | Manual: verify file permissions on `out/day3/audit_log.jsonl` |
| **Recommendation** | In production: use append-only storage (e.g., AWS S3 with object lock) or cryptographically signed logs |

---

### T-7: Database Corruption

**Threat:** Database file becomes corrupted due to concurrent writes, crashes, or disk errors.

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Likelihood** | LOW (SQLite handles concurrency) |
| **Impact** | Data loss, service unavailability |
| **Attack Vector** | Multiple processes writing to database simultaneously, disk failure |
| **Mitigation** | SQLite ACID transactions; connection commit/close pattern in `repository.py` |
| **Status** | ✅ Mitigated (SQLite built-in protection) |
| **Verification** | Code review: verify all DB operations use commit() |
| **Recommendation** | Regular backups (out of scope for capstone) |

---

### T-8: Configuration Errors

**Threat:** Incorrect configuration (e.g., wrong score thresholds) leads to incorrect decisions.

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Likelihood** | MEDIUM (manual configuration) |
| **Impact** | Systemic decision errors, compliance violations |
| **Attack Vector** | Developer accidentally sets `SCORE_APPROVE_THRESHOLD = 10` |
| **Mitigation** | Default values in `config.py`; environment variables override only when explicit; tests validate expected outcomes |
| **Status** | ✅ Mitigated (defaults + tests) |
| **Verification** | `pytest tests/day3/test_rules_engine.py` validates score bands |
| **Reference** | [src/day3/credit_decisioning/config.py](../src/day3/credit_decisioning/config.py#L16) |

---

### T-9: Non-Deterministic Decisions

**Threat:** Decision engine produces different outputs for same input, causing audit failures.

| Attribute | Value |
|-----------|-------|
| **Severity** | CRITICAL (in production) |
| **Likelihood** | LOW (deterministic design) |
| **Impact** | Unable to reproduce decisions, regulatory non-compliance |
| **Attack Vector** | Random number generation in rules engine, timestamp-based logic |
| **Mitigation** | Rules engine uses only deterministic logic; reason codes sorted alphabetically |
| **Status** | ✅ Mitigated |
| **Verification** | `pytest tests/day3/test_rules_engine.py::test_determinism` |
| **Reference** | [src/day3/credit_decisioning/rules_engine.py](../src/day3/credit_decisioning/rules_engine.py#L67) |

---

### T-10: Information Disclosure via Error Messages

**Threat:** Detailed error messages expose system internals (e.g., database structure, file paths).

| Attribute | Value |
|-----------|-------|
| **Severity** | LOW |
| **Likelihood** | MEDIUM |
| **Impact** | Information leakage aids further attacks |
| **Attack Vector** | Trigger errors (e.g., malformed requests) and inspect error responses |
| **Mitigation** | FastAPI default error handling; HTTPException with generic messages ("Application not found") |
| **Status** | ✅ Partially Mitigated (generic messages) |
| **Verification** | Manual: test error responses for verbosity |
| **Recommendation** | In production: use custom exception handlers to sanitize error messages |

---

## 6. Mitigation Summary

| Threat ID | Threat | Severity | Status | Verification Method |
|-----------|--------|----------|--------|---------------------|
| T-1 | PII Leakage in Audit Logs | HIGH | ✅ Mitigated | `test_audit_log_no_pii` |
| T-2 | SQL Injection | CRITICAL | ✅ Mitigated | Code review (parameterized queries) |
| T-3 | API Abuse | MEDIUM | ⚠️ Accepted Risk | N/A (out of scope) |
| T-4 | No Authentication | HIGH | ⚠️ Accepted Risk | N/A (out of scope) |
| T-5 | Input Validation Bypass | MEDIUM | ✅ Mitigated | `test_create_application_invalid_income` |
| T-6 | Audit Log Tampering | HIGH | ⚠️ Partial | File permissions (manual) |
| T-7 | Database Corruption | MEDIUM | ✅ Mitigated | SQLite ACID guarantees |
| T-8 | Configuration Errors | HIGH | ✅ Mitigated | `test_rules_engine.py` |
| T-9 | Non-Deterministic Decisions | CRITICAL | ✅ Mitigated | `test_determinism` |
| T-10 | Information Disclosure | LOW | ✅ Partial | Manual testing |

---

## 7. Recommendations for Production

If this capstone were deployed to production, implement:

1. **Authentication & Authorization**: OAuth2/JWT with RBAC
2. **Rate Limiting**: Protect against API abuse (e.g., 100 req/min per user)
3. **TLS/HTTPS**: Encrypt data in transit
4. **Database Encryption**: Encrypt SQLite database at rest
5. **Audit Log Signing**: Cryptographically sign audit entries for tamper-evidence
6. **Secret Management**: Use vault (e.g., Azure Key Vault) for sensitive config
7. **Monitoring & Alerting**: Detect anomalies (e.g., spike in DECLINE decisions)
8. **WAF**: Web Application Firewall to filter malicious requests
9. **Regular Pen Testing**: Identify new vulnerabilities
10. **Compliance Review**: GDPR, CCPA, SOC 2 audits

---

## 8. Threat Model Maintenance

This threat model should be updated:

- When new features are added (e.g., external data enrichment APIs)
- After security incidents or near-misses
- During quarterly security reviews
- When regulatory requirements change

---

## 9. Related Documents

- [Capstone Requirements](capstone_requirements.md)
- [Capstone Architecture](capstone_architecture.md)
- [Risk Register](risk_register.md)
- [Capstone Runbook](capstone_runbook.md)

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-21 | Security Team | Initial threat model |
