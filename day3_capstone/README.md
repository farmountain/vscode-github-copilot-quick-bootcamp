# Day 3 — Capstone: Credit Decisioning Slice

## Overview

Day 3 is the **capstone delivery day** where you integrate everything learned in Days 1 and 2 to build a **mini end-to-end credit decisioning system** using VS Code + GitHub Copilot Chat + Agent Mode + GitHub Copilot CLI.

**Key outcome:** A banking-grade system slice with clear architecture, full test coverage, audit trails, decision explainability, and governance artifacts.

---

## What You'll Build

A **Credit Decisioning Service** (FastAPI-based) that:

- Accepts credit applications via REST API
- Validates and enriches application data
- Computes deterministic credit decisions with **reason codes**
- Records all decisions in an **audit log** (no raw PII)
- Provides full explainability and traceability
- Includes governance artifacts (threat model, risk register, runbook)

---

## Day 3 Structure

| Time | Session | Content |
|------|---------|---------|
| 09:00–10:30 | **Session 3.1** | Capstone framing + architecture + governance |
| 10:45–12:15 | **Session 3.2** | Build strategy + agent stage gates + test loops |
| 13:30–16:30 | **Capstone Lab** | Build the system (API + rules + audit + tests) |
| 16:30–17:15 | **Hardening** | Security checks + negative tests + docs |
| 17:15–17:45 | **Demo + Retro** | Evidence-based walkthrough + evaluation |

---

## Directory Structure

```
day3_capstone/
├── README.md (this file)
├── capstone_overview.md
├── capstone_requirements.md
├── capstone_architecture.md
├── capstone_runbook.md
├── threat_model.md
├── risk_register.md
├── labs/
│   └── capstone_build_credit_decisioning_slice.md
└── prompts/
    └── day3_prompts.md
```

---

## Quick Start (How to Run Day 3 Capstone)

### Prerequisites

```bash
# Python 3.10+ with dependencies
pip install fastapi uvicorn pydantic pytest httpx
```

### Step 1: Generate Documentation (Prompt D3-0)

Already done! You're reading it.

### Step 2: Implement the Service (Prompt D3-1)

Use the prompts in [prompts/day3_prompts.md](prompts/day3_prompts.md) with GitHub Copilot Agent Mode to:

- Generate the FastAPI service
- Implement deterministic decision rules with reason codes
- Create persistence layer (SQLite or file-based)
- Add audit logging (JSONL format, no raw PII)
- Build comprehensive test suite

### Step 3: Add Governance Artifacts (Prompt D3-2)

Generate:

- Threat model
- Risk register
- Requirements traceability matrix

### Step 4: Configure VS Code Tasks (Prompt D3-3)

One-click commands for:

- Running the API server
- Executing tests
- Generating sample data
- Running end-to-end demos

### Step 5: Create Evidence Bundle (Prompt D3-4)

Package all outputs for audit review:

- Test results
- Audit logs
- Sample decisions
- Evidence manifest

---

## Running the Capstone (Manual Steps)

Once implemented via the prompts:

```bash
# 1. Start the API server
uvicorn src.day3.credit_decisioning.app:app --reload

# 2. In another terminal, run tests
pytest tests/day3/ -v

# 3. Generate sample applications
python -m src.day3.credit_decisioning.sample_data

# 4. Run end-to-end demo
python src/day3/credit_decisioning/demo_e2e.py

# 5. Check audit log
cat out/day3/audit_log.jsonl
```

---

## Key Learning Objectives

By the end of Day 3, you will:

1. ✅ Architect a multi-module system with clear contracts
2. ✅ Use Copilot Agent Mode for complex multi-file implementations
3. ✅ Implement deterministic business logic with full explainability
4. ✅ Build comprehensive test suites (unit + API + end-to-end)
5. ✅ Create audit trails that protect sensitive data
6. ✅ Produce governance artifacts (threat model, risk register)
7. ✅ Package evidence for audit review
8. ✅ Use GitHub Copilot CLI for workflow automation

---

## Banking-Grade Requirements

This capstone teaches you to build systems that satisfy:

- **Traceability:** Every requirement maps to code and tests
- **Auditability:** Every decision has explainable reason codes
- **Safety:** No raw PII in logs; least-privilege data exposure
- **Reproducibility:** Deterministic outputs; stable demos
- **Evidence:** Test results + audit logs + runbook

---

## What's In Scope vs. Out of Scope

### ✅ In Scope

- FastAPI REST API with 5 endpoints
- Deterministic rule-based decision engine
- Reason codes for every decision
- Audit log (JSONL format)
- Simple persistence (SQLite or file-based JSON)
- Unit, API, and end-to-end tests
- Governance artifacts
- Runbook and verification commands

### ❌ Out of Scope

- Real customer data or production credit policies
- Machine learning models
- Production-grade security (auth/authz)
- Real-time fraud detection
- Distributed systems or horizontal scaling

---

## Next Steps

1. Read [capstone_overview.md](capstone_overview.md) for the full system vision
2. Review [capstone_requirements.md](capstone_requirements.md) for detailed specs
3. Study [capstone_architecture.md](capstone_architecture.md) for design patterns
4. Follow [labs/capstone_build_credit_decisioning_slice.md](labs/capstone_build_credit_decisioning_slice.md)
5. Use [prompts/day3_prompts.md](prompts/day3_prompts.md) with Copilot Agent Mode

---

## Support and Troubleshooting

See [capstone_runbook.md](capstone_runbook.md) for:

- Installation issues
- API startup problems
- Test failures
- Audit log verification
- Evidence bundle creation

---

## Evaluation Criteria

Your capstone will be assessed on:

1. **Completeness:** All 5 API endpoints working
2. **Correctness:** Tests pass; decisions are deterministic
3. **Explainability:** Reason codes present and accurate
4. **Safety:** No raw PII in audit logs
5. **Traceability:** Requirements map to code and tests
6. **Governance:** Threat model and risk register complete
7. **Reproducibility:** Demo runs reliably; evidence bundle packages cleanly

---

**Ready to build?** Start with [labs/capstone_build_credit_decisioning_slice.md](labs/capstone_build_credit_decisioning_slice.md)!
