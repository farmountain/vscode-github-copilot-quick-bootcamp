# Risk Register: Credit Decisioning Service

## Document Control

| Attribute | Value |
|-----------|-------|
| **Version** | 1.0 |
| **Date** | 2025-12-21 |
| **Owner** | Day 3 Capstone Project Team |
| **Review Frequency** | Before each milestone |

---

## 1. Purpose

This risk register identifies technical, operational, and compliance risks for the Credit Decisioning Service capstone project. Each risk includes:

- **Risk ID**: Unique identifier
- **Description**: What could go wrong
- **Category**: Type of risk (Technical, Operational, Compliance, Data)
- **Likelihood**: Probability (Low, Medium, High)
- **Impact**: Severity (Low, Medium, High, Critical)
- **Risk Score**: Likelihood × Impact (1-4 scale)
- **Mitigation Strategy**: How we reduce the risk
- **Owner**: Who is responsible
- **Status**: Current state (Open, Mitigated, Accepted)

---

## 2. Risk Assessment Matrix

### Risk Scoring

| Likelihood | Low Impact (1) | Medium Impact (2) | High Impact (3) | Critical Impact (4) |
|------------|----------------|-------------------|-----------------|---------------------|
| **High (3)** | 3 | 6 | 9 | 12 |
| **Medium (2)** | 2 | 4 | 6 | 8 |
| **Low (1)** | 1 | 2 | 3 | 4 |

**Risk Priority:**

- **12+**: Critical - Immediate action required
- **6-9**: High - Address before deployment
- **3-5**: Medium - Monitor and mitigate
- **1-2**: Low - Accept or defer

---

## 3. Active Risks

### R-1: Non-Deterministic Decision Engine

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-1 |
| **Category** | Technical |
| **Description** | Decision engine produces different outcomes for identical inputs, making decisions irreproducible and audit trails invalid. |
| **Root Cause** | Use of random numbers, timestamps, or uncontrolled external state in scoring logic. |
| **Likelihood** | Low (1) |
| **Impact** | Critical (4) |
| **Risk Score** | 4 |
| **Consequences** | - Regulatory non-compliance<br>- Inability to reproduce decisions for appeals<br>- Failed audits<br>- Loss of customer trust |
| **Mitigation Strategy** | 1. Rules engine uses only deterministic logic (no random, no timestamps)<br>2. Reason codes sorted alphabetically for consistent output<br>3. Automated test verifies determinism (`test_determinism`)<br>4. Code review checklist flags non-deterministic patterns |
| **Residual Risk** | 1 (Low) |
| **Owner** | Development Team |
| **Status** | ✅ Mitigated |
| **Verification** | `pytest tests/day3/test_rules_engine.py::test_determinism` |
| **Last Reviewed** | 2025-12-21 |

---

### R-2: PII Leakage in Audit Logs

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-2 |
| **Category** | Compliance / Data Privacy |
| **Description** | Audit log accidentally includes raw PII (names, addresses, emails), violating data minimization and GDPR/CCPA principles. |
| **Root Cause** | Developer error logging entire application object instead of derived features only. |
| **Likelihood** | Medium (2) |
| **Impact** | High (3) |
| **Risk Score** | 6 |
| **Consequences** | - Privacy breach<br>- Regulatory fines (GDPR: up to 4% revenue)<br>- Reputational damage<br>- Customer lawsuits |
| **Mitigation Strategy** | 1. `audit.py` explicitly excludes PII fields (full_name, address, email)<br>2. Logs only IDs and numeric derived features<br>3. Automated test verifies no PII in audit file (`test_audit_log_no_pii`)<br>4. Code review checklist requires privacy review for any audit.py changes |
| **Residual Risk** | 2 (Low) |
| **Owner** | Security Team / Data Privacy Officer |
| **Status** | ✅ Mitigated |
| **Verification** | `pytest tests/day3/test_end_to_end_scenarios.py::test_audit_log_no_pii` |
| **Last Reviewed** | 2025-12-21 |

---

### R-3: Test Suite Gaps

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-3 |
| **Category** | Technical / Quality |
| **Description** | Test suite does not cover critical edge cases, leading to undetected bugs in production. |
| **Root Cause** | Incomplete test planning, time pressure, lack of negative test cases. |
| **Likelihood** | Medium (2) |
| **Impact** | Medium (2) |
| **Risk Score** | 4 |
| **Consequences** | - Bugs discovered in production<br>- Incorrect decisions<br>- Service downtime<br>- Emergency hotfixes |
| **Mitigation Strategy** | 1. Test plan in capstone_requirements.md lists 30+ test cases<br>2. Test suite covers: unit tests (15+), API tests (8+), E2E tests (7+), repository tests (6+)<br>3. Tests include edge cases (DTI=0.36, score=70), negative cases (404 errors), and critical safety checks (PII exclusion)<br>4. Code coverage target: >80% (can be measured with pytest-cov) |
| **Residual Risk** | 3 (Medium) |
| **Owner** | QA Team / Development Team |
| **Status** | ✅ Mitigated (comprehensive test suite) |
| **Verification** | Run `pytest tests/day3/ -v --cov=src.day3` and review coverage report |
| **Last Reviewed** | 2025-12-21 |

---

### R-4: Database Corruption / Data Loss

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-4 |
| **Category** | Operational |
| **Description** | SQLite database becomes corrupted or deleted, losing all application and decision records. |
| **Root Cause** | Disk failure, power loss during write, accidental file deletion, concurrent write conflicts. |
| **Likelihood** | Low (1) |
| **Impact** | High (3) |
| **Risk Score** | 3 |
| **Consequences** | - Loss of historical decisions<br>- Inability to reproduce decisions for appeals<br>- Compliance violations<br>- Customer impact |
| **Mitigation Strategy** | 1. SQLite ACID transactions protect against corruption<br>2. Connection commit/close pattern in repository.py<br>3. Database file stored in `out/day3/` with clear naming<br>4. RECOMMENDATION: Implement daily backups (out of scope for capstone) |
| **Residual Risk** | 2 (Low with backups) |
| **Owner** | Operations Team |
| **Status** | ⚠️ Partially Mitigated (SQLite built-in protection only) |
| **Verification** | Manual: verify database file exists after crash/restart |
| **Last Reviewed** | 2025-12-21 |

---

### R-5: Configuration Drift

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-5 |
| **Category** | Operational |
| **Description** | Production configuration differs from tested configuration, causing incorrect behavior. |
| **Root Cause** | Manual environment variable overrides, undocumented changes, missing config validation. |
| **Likelihood** | Medium (2) |
| **Impact** | High (3) |
| **Risk Score** | 6 |
| **Consequences** | - Systemic decision errors<br>- Compliance violations<br>- Customer impact<br>- Difficult debugging |
| **Mitigation Strategy** | 1. `config.py` defines safe defaults<br>2. Environment variables override only when explicitly set<br>3. Tests validate expected behavior with default config<br>4. RECOMMENDATION: Config validation at startup (check thresholds are sane)<br>5. RECOMMENDATION: Immutable infrastructure (infrastructure-as-code) |
| **Residual Risk** | 4 (Medium) |
| **Owner** | DevOps Team |
| **Status** | ⚠️ Partially Mitigated (defaults + tests) |
| **Verification** | `pytest tests/day3/test_rules_engine.py` validates score bands |
| **Last Reviewed** | 2025-12-21 |

---

### R-6: Input Validation Failures

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-6 |
| **Category** | Technical / Security |
| **Description** | Invalid input bypasses validation, causing crashes, incorrect decisions, or security vulnerabilities (e.g., SQL injection). |
| **Root Cause** | Missing validators, incorrect constraints, edge cases not handled. |
| **Likelihood** | Low (1) |
| **Impact** | High (3) |
| **Risk Score** | 3 |
| **Consequences** | - Service crashes<br>- Incorrect decisions<br>- Security vulnerabilities<br>- Data corruption |
| **Mitigation Strategy** | 1. Pydantic Field validators enforce constraints (gt=0, ge=0)<br>2. FastAPI returns 422 Unprocessable Entity for invalid input<br>3. Repository uses parameterized queries (SQL injection protection)<br>4. Tests verify rejection of invalid inputs (`test_create_application_invalid_income`) |
| **Residual Risk** | 1 (Low) |
| **Owner** | Development Team |
| **Status** | ✅ Mitigated |
| **Verification** | `pytest tests/day3/test_api_endpoints.py` (negative test cases) |
| **Last Reviewed** | 2025-12-21 |

---

### R-7: Incomplete Requirements Traceability

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-7 |
| **Category** | Process / Compliance |
| **Description** | Requirements are not traceable to implementation and tests, making it impossible to verify complete implementation. |
| **Root Cause** | Missing traceability matrix, undocumented changes, requirements creep. |
| **Likelihood** | Medium (2) |
| **Impact** | Medium (2) |
| **Risk Score** | 4 |
| **Consequences** | - Failed audits<br>- Missing features discovered late<br>- Difficult impact analysis for changes<br>- Compliance violations |
| **Mitigation Strategy** | 1. Requirements Traceability Matrix in capstone_requirements.md maps FR/NFR to modules and tests<br>2. Each requirement includes verification command<br>3. Regular reviews ensure matrix stays current<br>4. All code changes must reference requirement ID |
| **Residual Risk** | 2 (Low) |
| **Owner** | Technical Lead / BA Team |
| **Status** | ✅ Mitigated (matrix exists and complete) |
| **Verification** | Review Section 8 of capstone_requirements.md |
| **Last Reviewed** | 2025-12-21 |

---

### R-8: Audit Log Tampering

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-8 |
| **Category** | Security / Compliance |
| **Description** | Attacker with file system access modifies or deletes audit log entries to hide fraudulent activity. |
| **Root Cause** | Audit log stored as plain JSONL file with standard file permissions; no cryptographic integrity protection. |
| **Likelihood** | Medium (2) |
| **Impact** | High (3) |
| **Risk Score** | 6 |
| **Consequences** | - Loss of audit trail<br>- Inability to detect fraud<br>- Compliance violations<br>- Legal liability |
| **Mitigation Strategy** | 1. Append-only design (existing entries not modified)<br>2. File permissions restrict access (OS-level)<br>3. RECOMMENDATION: Cryptographically sign each entry (out of scope)<br>4. RECOMMENDATION: Use immutable storage (e.g., AWS S3 with object lock) |
| **Residual Risk** | 5 (Medium - accepted for capstone) |
| **Owner** | Security Team |
| **Status** | ⚠️ Partially Mitigated (basic file permissions) |
| **Verification** | Manual: verify file permissions on `out/day3/audit_log.jsonl` |
| **Last Reviewed** | 2025-12-21 |

---

### R-9: Dependency Vulnerabilities

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-9 |
| **Category** | Security |
| **Description** | Third-party dependencies (FastAPI, Pydantic, SQLite) contain known security vulnerabilities. |
| **Root Cause** | Outdated libraries, unpatched CVEs, supply chain attacks. |
| **Likelihood** | Medium (2) |
| **Impact** | High (3) |
| **Risk Score** | 6 |
| **Consequences** | - Security breaches<br>- Data exposure<br>- Service compromise<br>- Compliance violations |
| **Mitigation Strategy** | 1. Use recent stable versions (FastAPI 0.115+, Pydantic v2)<br>2. RECOMMENDATION: Run `pip-audit` or `safety check` regularly<br>3. RECOMMENDATION: Dependabot or Renovate for automated updates<br>4. Pin versions in requirements.txt for reproducibility |
| **Residual Risk** | 4 (Medium) |
| **Owner** | Security Team / Development Team |
| **Status** | ⚠️ Accepted Risk (manual review for training) |
| **Verification** | Run `pip-audit` (requires installation) |
| **Last Reviewed** | 2025-12-21 |

---

### R-10: Insufficient Monitoring

| Attribute | Value |
|-----------|-------|
| **Risk ID** | R-10 |
| **Category** | Operational |
| **Description** | Lack of monitoring means anomalies (e.g., spike in DECLINE decisions) go undetected. |
| **Root Cause** | No observability tooling (metrics, logs, alerts) implemented. |
| **Likelihood** | High (3) |
| **Impact** | Medium (2) |
| **Risk Score** | 6 |
| **Consequences** | - Delayed incident detection<br>- Prolonged outages<br>- Business impact<br>- Customer dissatisfaction |
| **Mitigation Strategy** | 1. OUT OF SCOPE for capstone<br>2. RECOMMENDATION: Log aggregation (e.g., ELK stack)<br>3. RECOMMENDATION: Metrics (Prometheus + Grafana)<br>4. RECOMMENDATION: Alerts on anomalies (e.g., >50% DECLINE rate) |
| **Residual Risk** | 6 (High - accepted for training) |
| **Owner** | Operations Team |
| **Status** | ⚠️ Accepted Risk (out of scope) |
| **Verification** | N/A |
| **Last Reviewed** | 2025-12-21 |

---

## 4. Closed/Retired Risks

*(None at this time - all risks are active)*

---

## 5. Risk Summary Dashboard

| Category | Critical (12+) | High (6-9) | Medium (3-5) | Low (1-2) | Total |
|----------|----------------|------------|--------------|-----------|-------|
| **Technical** | 0 | 0 | 2 | 2 | 4 |
| **Security** | 0 | 1 | 1 | 0 | 2 |
| **Operational** | 0 | 2 | 1 | 0 | 3 |
| **Compliance** | 0 | 1 | 0 | 0 | 1 |
| **Total** | 0 | 4 | 4 | 2 | 10 |

### Status Summary

- ✅ **Mitigated**: 4 risks (R-1, R-2, R-3, R-6)
- ⚠️ **Partially Mitigated**: 4 risks (R-4, R-5, R-7, R-8)
- ⚠️ **Accepted Risk**: 2 risks (R-9, R-10)

---

## 6. Risk Ownership

| Owner | Risk IDs | Count |
|-------|----------|-------|
| Development Team | R-1, R-3, R-6, R-9 | 4 |
| Security Team | R-2, R-8, R-9 | 3 |
| Operations Team | R-4, R-10 | 2 |
| DevOps Team | R-5 | 1 |
| Technical Lead / BA | R-7 | 1 |

---

## 7. Action Items

### Immediate (Before Deployment)

1. **R-2**: Confirm PII exclusion test passes (`pytest tests/day3/test_end_to_end_scenarios.py::test_audit_log_no_pii`)
2. **R-7**: Complete Requirements Traceability Matrix with actual file paths

### Short-Term (Next Sprint)

3. **R-4**: Implement database backup script (daily snapshots)
4. **R-5**: Add config validation at startup (check thresholds are in valid range)
5. **R-9**: Run `pip-audit` and update dependencies with known CVEs

### Long-Term (Production Hardening)

6. **R-8**: Implement cryptographically signed audit logs
7. **R-10**: Deploy observability stack (metrics + logs + alerts)
8. **R-9**: Set up automated dependency scanning (Dependabot)

---

## 8. Lessons Learned for Future Capstones

### What Went Well

- ✅ Early identification of PII leakage risk led to explicit exclusion design
- ✅ Determinism risk addressed through automated testing
- ✅ Comprehensive test suite reduces quality risk

### Areas for Improvement

- ⚠️ Add monitoring earlier in design (not as an afterthought)
- ⚠️ Consider authentication/authorization from Day 1 (even if mocked)
- ⚠️ Include database backup strategy in initial architecture

---

## 9. Related Documents

- [Threat Model](threat_model.md) - Security-focused threat analysis
- [Capstone Requirements](capstone_requirements.md) - Functional and non-functional requirements
- [Capstone Architecture](capstone_architecture.md) - System design and ADRs
- [Capstone Runbook](capstone_runbook.md) - Operations and troubleshooting

---

## 10. Review Schedule

| Review Type | Frequency | Next Review |
|-------------|-----------|-------------|
| Risk Register Update | Weekly during development | 2025-12-28 |
| Risk Assessment | Before each milestone | Before D3-3 |
| Post-Mortem | After incidents | As needed |
| Annual Review | Yearly | 2026-12-21 |

---

**Document Version History**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-21 | Project Team | Initial risk register |
