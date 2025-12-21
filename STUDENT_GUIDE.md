# Complete Student Guide: GitHub Copilot Banking Bootcamp

**3-Day Training Program for Banking-Grade AI-Assisted Development**

---

## 🎯 Program Overview

This is a **hands-on, project-based bootcamp** that teaches you to build banking-grade software using VS Code + GitHub Copilot. You'll progress from basic prompting to building complete systems with audit trails, explainability, and governance.

**Who is this for?**
- Developers new to AI-assisted coding
- Banking/finance engineers who need audit-ready systems
- Anyone who wants to learn professional AI-driven development

**What you'll build:**
- Day 1: Data validation engine + Risk scoring API
- Day 2: AML alert triage system + PII protection library
- Day 3: Complete credit decisioning service with governance

---

## 📊 High-Level Training Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GITHUB COPILOT BANKING BOOTCAMP                      │
│                     (3-Day Progressive Learning Path)                    │
└─────────────────────────────────────────────────────────────────────────┘

DAY 1: FOUNDATIONS                    DAY 2: WORKFLOWS                    DAY 3: CAPSTONE
┌─────────────────────┐              ┌─────────────────────┐            ┌─────────────────────┐
│ Learn Fundamentals  │              │ Advanced Patterns    │            │ Build Complete      │
│                     │              │                      │            │ System              │
│ ┌─────────────────┐ │              │ ┌─────────────────┐ │            │ ┌─────────────────┐ │
│ │ Session 1.1     │ │              │ │ Session 2.1     │ │            │ │ Requirements    │ │
│ │ Agentic Dev     │ │              │ │ Task Planning   │ │            │ │ + Architecture  │ │
│ │ Mental Models   │ │              │ │ Epic→Task       │ │            │ │                 │ │
│ └─────────────────┘ │              │ └─────────────────┘ │            │ └─────────────────┘ │
│                     │              │                      │            │                     │
│ ┌─────────────────┐ │              │ ┌─────────────────┐ │            │ ┌─────────────────┐ │
│ │ Session 1.2     │ │──────────────▶│ │ Session 2.2     │ │────────────▶│ │ Implementation  │ │
│ │ Prompting       │ │   Builds on  │ │ Multi-File      │ │  Applies   │ │ 11 Modules      │ │
│ │ 3C Framework    │ │              │ │ Refactoring     │ │            │ │ 40+ Tests       │ │
│ └─────────────────┘ │              │ └─────────────────┘ │            │ └─────────────────┘ │
│                     │              │                      │            │                     │
│ ┌─────────────────┐ │              │ ┌─────────────────┐ │            │ ┌─────────────────┐ │
│ │ Lab 1           │ │              │ │ Lab 3           │ │            │ │ Governance      │ │
│ │ Data Quality    │ │              │ │ AML Triage      │ │            │ │ Threat Model    │ │
│ │ Rules Engine    │ │              │ │ Pipeline        │ │            │ │ Risk Register   │ │
│ └─────────────────┘ │              │ └─────────────────┘ │            │ └─────────────────┘ │
│                     │              │                      │            │                     │
│ ┌─────────────────┐ │              │ ┌─────────────────┐ │            │ ┌─────────────────┐ │
│ │ Lab 2           │ │              │ │ Lab 4           │ │            │ │ Evidence        │ │
│ │ Risk Scoring    │ │              │ │ PII Protection  │ │            │ │ Bundle          │ │
│ │ API             │ │              │ │ + Audit         │ │            │ │ (Tests+Logs)    │ │
│ └─────────────────┘ │              │ └─────────────────┘ │            │ └─────────────────┘ │
│                     │              │                      │            │                     │
│ ┌─────────────────┐ │              │ ┌─────────────────┐ │            │ ┌─────────────────┐ │
│ │ Session 1.3     │ │              │ │ Session 2.3     │ │            │ │ Demo + Review   │ │
│ │ Verification    │ │              │ │ CLI Automation  │ │            │ │                 │ │
│ │ + Reflexion     │ │              │ │ + Reflexion     │ │            │ │ + Reflexion     │ │
│ └─────────────────┘ │              │ └─────────────────┘ │            │ └─────────────────┘ │
└─────────────────────┘              └─────────────────────┘            └─────────────────────┘
        │                                     │                                   │
        │                                     │                                   │
        ▼                                     ▼                                   ▼
   Single-file                         Multi-module                      Complete system
   implementations                     systems with                      with governance
   with tests                          refactoring                       and compliance
```

---

## 📁 Repository Structure Map

```
vscode-github-copilot-quick-bootcamp/
│
├── 📘 README.md                              # Start here - project overview
├── 📘 TRAINING_TOC.md                        # Complete table of contents
├── 📘 IMPLEMENTATION_SUMMARY.md              # Technical implementation notes
│
├── 📂 day1_foundations/                      # DAY 1: Foundation Skills
│   ├── 📘 README.md                          # Day 1 overview + schedule
│   ├── 📄 session1_1_intro_to_agentic_dev.md    # Theory: Mental models
│   ├── 📄 session1_2_prompting_in_vscode.md     # Practice: 3C Framework
│   ├── 📄 session1_3_verification_and_tests.md  # Practice: Testing mindset
│   ├── 📂 labs/
│   │   ├── 📄 lab1_data_quality_rules_engine.md # Build: Validation system
│   │   └── 📄 lab2_simple_risk_scoring_service.md # Build: Risk API
│   └── 📂 prompts/
│       └── 📄 day1_prompts.md                # 🎯 Copy-paste prompts for labs
│
├── 📂 day2_agent_workflows/                  # DAY 2: Advanced Workflows
│   ├── 📘 README.md                          # Day 2 overview + schedule
│   ├── 📄 session2_1_agent_planning_and_task_breakdown.md  # Plan features
│   ├── 📄 session2_2_multi_file_refactor_and_test_loops.md # Safe refactoring
│   ├── 📄 session2_3_cli_automation_with_copilot_cli.md    # CLI automation
│   ├── 📂 labs/
│   │   ├── 📄 lab3_aml_alert_triage_pipeline.md # Build: AML system
│   │   └── 📄 lab4_pii_masking_and_audit_logging.md # Build: PII protection
│   └── 📂 prompts/
│       └── 📄 day2_prompts.md                # 🎯 Copy-paste prompts for labs
│
├── 📂 day3_capstone/                         # DAY 3: Complete System
│   ├── 📘 README.md                          # Capstone overview
│   ├── 📄 capstone_overview.md               # System vision
│   ├── 📄 capstone_requirements.md           # FR/NFR + traceability
│   ├── 📄 capstone_architecture.md           # Component design
│   ├── 📄 capstone_runbook.md                # Operations guide
│   ├── 📄 threat_model.md                    # Security analysis
│   ├── 📄 risk_register.md                   # Risk management
│   ├── 📂 labs/
│   │   └── 📄 capstone_build_credit_decisioning_slice.md # Build everything
│   └── 📂 prompts/
│       └── 📄 day3_prompts.md                # 🎯 Copy-paste prompts
│
├── 📂 src/                                   # YOUR CODE GOES HERE
│   ├── 📂 day1/                              # Day 1 implementations
│   │   ├── 📂 data_quality/                  # Lab 1: Data validation
│   │   │   ├── rules.py
│   │   │   ├── validator.py
│   │   │   ├── schemas.py
│   │   │   ├── cli.py
│   │   │   └── README.md
│   │   └── 📂 risk_scoring/                  # Lab 2: Risk scoring
│   │       ├── risk_engine.py
│   │       ├── scoring_rules.py
│   │       ├── models.py
│   │       ├── cli.py
│   │       └── README.md
│   │
│   ├── 📂 day2/                              # Day 2 implementations
│   │   ├── 📂 aml_triage/                    # Lab 3: AML triage
│   │   │   ├── schemas.py
│   │   │   ├── rules.py
│   │   │   ├── triage.py
│   │   │   ├── pipeline.py
│   │   │   ├── io.py
│   │   │   ├── cli.py
│   │   │   └── README.md
│   │   └── 📂 pii_protection/                # Lab 4: PII protection
│   │       ├── config.py
│   │       ├── masking.py
│   │       ├── tokenization.py
│   │       ├── redaction.py
│   │       ├── audit.py
│   │       ├── cli.py
│   │       └── README.md
│   │
│   ├── 📂 day3/                              # Day 3 capstone
│   │   └── 📂 credit_decisioning/            # Complete system
│   │       ├── config.py
│   │       ├── models.py
│   │       ├── features.py
│   │       ├── rules_engine.py
│   │       ├── repository.py
│   │       ├── audit.py
│   │       ├── app.py                        # FastAPI application
│   │       ├── sample_data.py
│   │       ├── demo_e2e.py
│   │       └── README.md
│   │
│   └── 📂 samples/                           # Sample data files
│       ├── sample_transactions.csv
│       ├── sample_credit_applications.json
│       ├── sample_transactions_day2.csv
│       └── sample_customer_pii.csv
│
├── 📂 tests/                                 # ALL YOUR TESTS GO HERE
│   ├── 📂 day1/                              # Day 1 tests
│   │   ├── test_data_quality_rules.py
│   │   ├── test_data_quality_end_to_end.py
│   │   ├── test_risk_engine.py
│   │   └── test_risk_scoring_rules.py
│   ├── 📂 day2/                              # Day 2 tests
│   │   ├── test_schemas.py
│   │   ├── test_aml_rules.py
│   │   ├── test_triage_scoring.py
│   │   ├── test_io.py
│   │   ├── test_pipeline_end_to_end.py
│   │   ├── test_masking.py
│   │   ├── test_tokenization.py
│   │   └── test_audit.py
│   └── 📂 day3/                              # Day 3 tests
│       ├── test_rules_engine.py
│       ├── test_api_endpoints.py
│       ├── test_end_to_end_scenarios.py
│       └── test_repository.py
│
├── 📂 scripts/                               # Automation scripts
│   └── day3_collect_evidence.py              # Evidence bundle generator
│
├── 📂 .vscode/                               # VS Code configuration
│   └── tasks.json                            # One-click run commands
│
└── 📂 out/                                   # Generated outputs
    ├── 📂 day1/
    ├── 📂 day2/
    └── 📂 day3/
        ├── credit_decisioning.db             # SQLite database
        ├── audit_log.jsonl                   # Audit trail
        ├── 📂 evidence/                      # Evidence bundle
        └── evidence_bundle_<timestamp>.zip   # Packaged evidence
```

---

## 🚀 Getting Started: Your Learning Path

### Prerequisites Checklist

Before you start, ensure you have:

- [ ] **VS Code** installed (latest version)
- [ ] **GitHub Copilot** extension installed and activated
- [ ] **GitHub Copilot subscription** (or free trial)
- [ ] **Python 3.10+** installed (`python --version`)
- [ ] **pip** package manager working (`pip --version`)
- [ ] **Git** installed and configured (`git --version`)
- [ ] Basic Python knowledge (functions, classes, imports)
- [ ] Understanding of REST APIs (helpful but not required)

### Installation Steps

```powershell
# 1. Clone the repository
git clone https://github.com/your-org/vscode-github-copilot-quick-bootcamp.git
cd vscode-github-copilot-quick-bootcamp

# 2. Create Python virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR: source venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install fastapi uvicorn pydantic pytest httpx pytest-cov

# 4. Verify installation
python -c "import fastapi, pydantic, pytest; print('✅ All dependencies installed')"

# 5. Open in VS Code
code .
```

### Verify GitHub Copilot is Working

1. Open VS Code
2. Press `Ctrl+Shift+P` → Type "GitHub Copilot: Chat"
3. In the chat panel, type: `@workspace what is this project about?`
4. You should see Copilot respond with context about the bootcamp

✅ If it responds, you're ready to start!

---

## 📚 Day-by-Day Learning Guide

### 🟢 Day 1: Foundations (6-8 hours)

**Goal:** Learn to prompt Copilot effectively and build single-module systems with tests.

#### Morning: Theory + Prompting (3 hours)

**Step 1: Session 1.1 - Mental Models (90 min)**
- 📖 Read: [day1_foundations/session1_1_intro_to_agentic_dev.md](day1_foundations/session1_1_intro_to_agentic_dev.md)
- 🎯 Learn: How AI coding assistants work differently from autocomplete
- 🎯 Learn: Mental models (Feynman contractor, Paul-Elder thinking)
- 🎯 Learn: Safety considerations for banking code

**Key Concepts:**
- **Agentic AI** = AI that can plan, execute, verify (not just autocomplete)
- **Feynman model** = Treat Copilot like a contractor (you provide specs, they build)
- **Paul-Elder framework** = Every prompt needs purpose, constraints, verification
- **Inversion thinking** = Think "what could go wrong?" before coding

**Step 2: Session 1.2 - Prompting Mastery (90 min)**
- 📖 Read: [day1_foundations/session1_2_prompting_in_vscode.md](day1_foundations/session1_2_prompting_in_vscode.md)
- 🎯 Learn: 3C Framework (Context, Constraints, Criteria)
- 🎯 Practice: GitHub Copilot Chat features (`@workspace`, `/explain`, `/tests`)
- 🎯 Practice: GitHub Copilot Agent Mode (multi-file generation)
- 🎯 Practice: GitHub Copilot CLI (`gh copilot suggest`, `gh copilot explain`)

**Hands-on Exercise:**
```
Open Copilot Chat and try:
1. "@workspace explain how Day 1 labs work"
2. "/explain what is deterministic code"
3. "Generate a Python function to validate email format with tests"
```

#### Afternoon: Hands-On Labs (3-4 hours)

**Step 3: Lab 1 - Data Quality Rules Engine (2 hours)**
- 📖 Read: [day1_foundations/labs/lab1_data_quality_rules_engine.md](day1_foundations/labs/lab1_data_quality_rules_engine.md)
- 📋 Open: [day1_foundations/prompts/day1_prompts.md](day1_foundations/prompts/day1_prompts.md) → Find **Prompt D1-1**

**What You'll Build:**
```
Transaction Validator
├── rules.py          # Validation rules (amount > 0, valid date, etc.)
├── validator.py      # Orchestrates validation
├── schemas.py        # Data models (Pydantic)
├── cli.py            # Command-line interface
└── tests/            # Pytest test suite
```

**Learning Outcomes:**
✅ Generate multi-file code with one prompt  
✅ Implement deterministic validation rules  
✅ Write comprehensive test suites  
✅ Use Pydantic for data validation  
✅ Create CLI with argparse  

**How to Execute:**
```powershell
# Option A: Use Agent Mode with Prompt D1-1 (Fast)
# Copy Prompt D1-1 from day1_prompts.md
# Paste into Copilot Agent Mode
# Review generated code

# Option B: Build step-by-step with Copilot Chat (Learning)
# Follow lab1_data_quality_rules_engine.md instructions
# Use Copilot Chat to assist with each function

# Verify it works:
pytest tests/day1/test_data_quality_rules.py -v
python -m src.day1.data_quality.cli --help
```

**Step 4: Lab 2 - Risk Scoring Service (2 hours)**
- 📖 Read: [day1_foundations/labs/lab2_simple_risk_scoring_service.md](day1_foundations/labs/lab2_simple_risk_scoring_service.md)
- 📋 Open: [day1_foundations/prompts/day1_prompts.md](day1_foundations/prompts/day1_prompts.md) → Find **Prompt D1-2**

**What You'll Build:**
```
Risk Scoring API (FastAPI)
├── risk_engine.py      # Core scoring algorithm
├── scoring_rules.py    # Business rules (DTI, payment history)
├── models.py           # Pydantic models
├── cli.py              # Command-line interface
└── tests/              # API + unit tests
```

**Learning Outcomes:**
✅ Build REST API with FastAPI  
✅ Implement explainable scoring (reason codes)  
✅ Create audit logging (JSONL format)  
✅ Test API endpoints with TestClient  
✅ Ensure deterministic results  

**How to Execute:**
```powershell
# Generate code with Prompt D1-2
# Copy from day1_prompts.md → Paste into Agent Mode

# Verify it works:
pytest tests/day1/test_risk_engine.py -v
uvicorn src.day1.risk_scoring.app:app --reload
# Visit http://127.0.0.1:8000/docs
```

**Step 5: Session 1.3 - Verification (30 min)**
- 📖 Read: [day1_foundations/session1_3_verification_and_tests.md](day1_foundations/session1_3_verification_and_tests.md)
- 🎯 Learn: Verification hierarchy (syntax → unit → integration → audit)
- 🎯 Learn: Reflexion framework (learn from mistakes)

**Reflexion Exercise:**
Answer these questions:
1. Did Copilot generate deterministic code (same input → same output)?
2. Did tests cover edge cases (negative numbers, empty strings)?
3. Did audit logs exclude sensitive data (PII)?
4. What would you do differently next time?

---

### 🟡 Day 2: Advanced Workflows (6-8 hours)

**Goal:** Manage multi-module systems, safe refactoring, and automation.

#### Morning: Planning + Refactoring (3 hours)

**Step 1: Session 2.1 - Task Planning (90 min)**
- 📖 Read: [day2_agent_workflows/session2_1_agent_planning_and_task_breakdown.md](day2_agent_workflows/session2_1_agent_planning_and_task_breakdown.md)
- 🎯 Learn: Epic → Task decomposition
- 🎯 Learn: Stop points for incremental review
- 🎯 Practice: Break down a feature into agent-friendly tasks

**Key Concepts:**
- **Epic** = High-level feature (e.g., "Build AML triage system")
- **Task** = Implementable unit with clear done criteria (e.g., "Implement HIGH_VELOCITY rule")
- **Stop point** = Review checkpoint (e.g., "Stop after generating schemas")

**Micro-Exercise:**
```
Epic: "Add email notification to risk scoring API"
Break it down into tasks:
Task 1: Add email config (SMTP settings)
Task 2: Create email template with decision details
Task 3: Add send_email() function
Task 4: Integrate into risk API endpoint
Task 5: Add tests for email sending
```

**Step 2: Session 2.2 - Safe Refactoring (90 min)**
- 📖 Read: [day2_agent_workflows/session2_2_multi_file_refactor_and_test_loops.md](day2_agent_workflows/session2_2_multi_file_refactor_and_test_loops.md)
- 🎯 Learn: Red-green-refactor cycle
- 🎯 Learn: Test loops (run tests after every change)
- 🎯 Practice: Refactor Day 1 code safely

**Refactoring Recipe:**
1. **Red:** Write failing test for new behavior
2. **Green:** Make test pass (minimum code)
3. **Refactor:** Clean up code while keeping tests green
4. **Commit:** Save progress with `git commit`

**Hands-on Exercise:**
```
Refactor Lab 1 to use a config file instead of hardcoded values:
1. Create config.py with validation thresholds
2. Update rules.py to use config values
3. Run tests (should still pass)
4. Commit changes
```

#### Afternoon: Multi-Module Labs (4 hours)

**Step 3: Lab 3 - AML Alert Triage Pipeline (2 hours)**
- 📖 Read: [day2_agent_workflows/labs/lab3_aml_alert_triage_pipeline.md](day2_agent_workflows/labs/lab3_aml_alert_triage_pipeline.md)
- 📋 Open: [day2_agent_workflows/prompts/day2_prompts.md](day2_agent_workflows/prompts/day2_prompts.md)

**What You'll Build:**
```
AML Triage System
├── schemas.py        # AlertTransaction, AlertReason, TriageQueue
├── rules.py          # HIGH_VELOCITY, ROUND_AMOUNT, HIGH_AMOUNT, RAPID_REVERSAL
├── triage.py         # Scoring + priority assignment (P1/P2/P3)
├── pipeline.py       # Orchestration: load → detect → score → output
├── io.py             # CSV/JSON readers and writers
├── cli.py            # Command-line interface
└── tests/            # Comprehensive test suite
```

**Learning Outcomes:**
✅ Build deterministic heuristic rules  
✅ Orchestrate multi-step pipelines  
✅ Generate audit-friendly outputs (JSON + CSV)  
✅ Test for determinism and false positives  

**How to Execute:**
```powershell
# Use prompts from day2_prompts.md in sequence:
# Prompt 2.1a: Generate schemas
# Prompt 2.1b: Generate rules
# Prompt 2.1c: Generate triage logic
# ... etc

# Verify:
pytest tests/day2/test_pipeline_end_to_end.py -v
python -m src.day2.aml_triage.cli analyze --input src/samples/sample_transactions_day2.csv
```

**Step 4: Lab 4 - PII Protection + Audit (2 hours)**
- 📖 Read: [day2_agent_workflows/labs/lab4_pii_masking_and_audit_logging.md](day2_agent_workflows/labs/lab4_pii_masking_and_audit_logging.md)
- 📋 Open: [day2_agent_workflows/prompts/day2_prompts.md](day2_agent_workflows/prompts/day2_prompts.md)

**What You'll Build:**
```
PII Protection Library
├── config.py         # Configuration (salt for tokenization)
├── masking.py        # mask_email(), mask_phone(), mask_national_id()
├── tokenization.py   # tokenize() - deterministic HMAC tokens
├── redaction.py      # redact_fields() - remove sensitive fields
├── audit.py          # log_operation() - audit without PII
├── cli.py            # Multi-mode CLI (MASK, TOKENIZE, REDACT)
└── tests/            # Test determinism + PII exclusion
```

**Learning Outcomes:**
✅ Implement deterministic masking functions  
✅ Use HMAC for tokenization (same input → same token)  
✅ Audit without storing raw PII  
✅ Test that PII never appears in logs  

**How to Execute:**
```powershell
# Generate with prompts from day2_prompts.md

# Verify:
pytest tests/day2/test_masking.py -v
pytest tests/day2/test_audit.py -v
python -m src.day2.pii_protection.cli mask --input src/samples/sample_customer_pii.csv
```

**Step 5: Session 2.3 - CLI Automation (integrated)**
- 📖 Read: [day2_agent_workflows/session2_3_cli_automation_with_copilot_cli.md](day2_agent_workflows/session2_3_cli_automation_with_copilot_cli.md)
- 🎯 Practice: Use `gh copilot suggest` for commands
- 🎯 Practice: Use `gh copilot explain` for understanding code

**CLI Exercises:**
```powershell
# Ask Copilot CLI to suggest commands:
gh copilot suggest "find all Python files in tests directory"
gh copilot suggest "count lines of code in src/day2"
gh copilot suggest "run pytest with verbose output and coverage"

# Ask Copilot CLI to explain:
gh copilot explain "pytest -v --cov=src.day2"
```

---

### 🔴 Day 3: Capstone Project (6-8 hours)

**Goal:** Build complete credit decisioning system with governance artifacts.

#### Morning: Architecture + Planning (2.5 hours)

**Step 1: Read Core Documentation (90 min)**

Read in this order:
1. 📖 [day3_capstone/README.md](day3_capstone/README.md) - Overview
2. 📖 [day3_capstone/capstone_overview.md](day3_capstone/capstone_overview.md) - System vision
3. 📖 [day3_capstone/capstone_requirements.md](day3_capstone/capstone_requirements.md) - Requirements (FR/NFR)
4. 📖 [day3_capstone/capstone_architecture.md](day3_capstone/capstone_architecture.md) - Design

**What You'll Understand:**
- System boundaries (what's in scope, what's not)
- API contracts (5 endpoints)
- Decision algorithm (baseline + adjustments)
- Data flow (application → decision → audit)
- Non-functional requirements (determinism, explainability, data privacy)

**Step 2: Review Governance Documents (45 min)**

5. 📖 [day3_capstone/threat_model.md](day3_capstone/threat_model.md) - Security threats
6. 📖 [day3_capstone/risk_register.md](day3_capstone/risk_register.md) - Risk management

**What You'll Learn:**
- Common threats (SQL injection, PII leakage, audit tampering)
- Mitigations (Pydantic validation, parameterized queries, PII exclusion)
- Risk prioritization (likelihood × impact)

#### Afternoon: Build the System (4 hours)

**Step 3: Capstone Lab - Build Everything (3 hours)**
- 📖 Read: [day3_capstone/labs/capstone_build_credit_decisioning_slice.md](day3_capstone/labs/capstone_build_credit_decisioning_slice.md)
- 📋 Open: [day3_capstone/prompts/day3_prompts.md](day3_capstone/prompts/day3_prompts.md)

**What You'll Build:**
```
Credit Decisioning Service (Complete System)
├── config.py              # Configuration (thresholds, paths)
├── models.py              # Pydantic models (ApplicationRequest, DecisionRecord)
├── features.py            # Feature engineering (DTI, affordability)
├── rules_engine.py        # Deterministic scoring + reason codes
├── repository.py          # SQLite persistence (CRUD operations)
├── audit.py               # JSONL audit logger (NO PII)
├── app.py                 # FastAPI with 5 endpoints
├── sample_data.py         # Synthetic data generator
├── demo_e2e.py            # End-to-end demo script
├── README.md              # Implementation docs
└── tests/
    ├── test_rules_engine.py          # 15+ unit tests
    ├── test_api_endpoints.py         # 8+ API tests
    ├── test_end_to_end_scenarios.py  # 7+ E2E tests (includes PII check!)
    └── test_repository.py            # 6+ persistence tests
```

**Execution Steps:**

```powershell
# Step 1: Generate all code with Prompt D3-1
# Open day3_prompts.md → Copy Prompt D3-1 → Paste into Agent Mode
# Agent will create 11 modules + 4 test files

# Step 2: Verify tests pass
pytest tests/day3/ -v

# Step 3: Generate sample data
python -m src.day3.credit_decisioning.sample_data

# Step 4: Run API server
uvicorn src.day3.credit_decisioning.app:app --reload
# Visit http://127.0.0.1:8000/docs

# Step 5: Run end-to-end demo
python -m src.day3.credit_decisioning.demo_e2e
```

**Critical Test:** Verify no PII in audit log
```powershell
pytest tests/day3/test_end_to_end_scenarios.py::test_audit_log_no_pii -v
# This test MUST pass - it verifies full_name, address, email NOT in audit file
```

**Step 4: VS Code Tasks + Evidence Bundle (30 min)**

```powershell
# Add VS Code tasks (already done via Prompt D3-3)
# Open Command Palette (Ctrl+Shift+P) → "Tasks: Run Task"
# Try: "Day3: Run Capstone Tests"

# Generate evidence bundle
python scripts/day3_collect_evidence.py
# This creates: out/day3/evidence_bundle_<timestamp>.zip
```

**Step 5: Review Runbook (30 min)**
- 📖 Read: [day3_capstone/capstone_runbook.md](day3_capstone/capstone_runbook.md)
- 🎯 Practice: Follow troubleshooting scenarios
- 🎯 Practice: Review audit log checklist

#### Final: Demo + Reflexion (30 min)

**Demo Checklist:**
- [ ] All 5 API endpoints working
- [ ] Decision engine returns deterministic scores
- [ ] Reason codes explain every adjustment
- [ ] Audit log created (check `out/day3/audit_log.jsonl`)
- [ ] Audit log does NOT contain PII (verify manually)
- [ ] All tests pass (40+ tests)
- [ ] Database created (check `out/day3/credit_decisioning.db`)
- [ ] Evidence bundle generated

**Reflexion Questions:**
1. What was the hardest part of the capstone?
2. Did Agent Mode generate code that worked first try?
3. How did you verify determinism?
4. How did you verify PII exclusion?
5. What governance artifact was most valuable?
6. What would you do differently in production?

---

## 🎓 Learning Outcomes by Day

### Day 1: You Can Now...
✅ Write effective prompts using 3C Framework (Context, Constraints, Criteria)  
✅ Use GitHub Copilot Chat, Agent Mode, and CLI productively  
✅ Generate single-module systems with tests  
✅ Implement deterministic algorithms (no randomness)  
✅ Create audit trails (JSONL logs)  
✅ Write comprehensive test suites (unit + integration)  
✅ Apply banking safety mindset (data validation, explainability)  

### Day 2: You Can Now...
✅ Decompose epics into agent-friendly tasks  
✅ Build multi-module systems (5+ interconnected modules)  
✅ Execute safe refactors with test loops  
✅ Implement AML heuristic rules (velocity, amounts, patterns)  
✅ Build PII protection libraries (masking, tokenization, redaction)  
✅ Automate workflows with GitHub Copilot CLI  
✅ Apply reflexion framework (continuous improvement)  

### Day 3: You Can Now...
✅ Build complete end-to-end systems from requirements to evidence  
✅ Implement RESTful APIs with FastAPI (5+ endpoints)  
✅ Design deterministic decision engines with reason codes  
✅ Create governance artifacts (threat models, risk registers, runbooks)  
✅ Implement requirements traceability (FR/NFR → code → tests)  
✅ Generate evidence bundles for audit review  
✅ Deliver banking-grade software with AI assistance  

---

## 🛠️ Tools Reference

### GitHub Copilot Features Used

| Feature | Purpose | When to Use |
|---------|---------|-------------|
| **Copilot Inline** | Code completion as you type | Writing functions, variables |
| **Copilot Chat** | Ask questions about code | Understanding, debugging |
| **@workspace** | Ask about entire project | Project overview, file locations |
| **/explain** | Explain code snippet | Understanding complex logic |
| **/tests** | Generate tests | After writing functions |
| **Agent Mode** | Multi-file generation | Building modules from prompts |
| **Copilot CLI** | Command suggestions | Terminal productivity |

### VS Code Tasks (One-Click Commands)

Press `Ctrl+Shift+P` → "Tasks: Run Task" → Select:

**Day 1 Tasks:**
- `Day1: Run Data Quality CLI` - Test Lab 1
- `Day1: Run Risk Scoring CLI` - Test Lab 2

**Day 2 Tasks:**
- `Day2: Run AML Triage CLI` - Test Lab 3
- `Day2: Run PII Protection CLI` - Test Lab 4

**Day 3 Tasks:**
- `Day3: Generate Sample Applications` - Create test data
- `Day3: Run Capstone API Server` - Start FastAPI (background)
- `Day3: Run Capstone Tests` - Run all tests
- `Day3: Run E2E Demo Script` - Demo full workflow
- `Day3: Verify All (Composite)` - Run everything

### Common Commands Cheat Sheet

```powershell
# Run specific test file
pytest tests/day1/test_data_quality_rules.py -v

# Run all tests for a day
pytest tests/day1/ -v
pytest tests/day2/ -v
pytest tests/day3/ -v

# Run with coverage report
pytest tests/day3/ -v --cov=src.day3.credit_decisioning --cov-report=term-missing

# Run specific test function
pytest tests/day3/test_end_to_end_scenarios.py::test_audit_log_no_pii -v

# Start FastAPI server
uvicorn src.day3.credit_decisioning.app:app --reload --port 8000

# Generate sample data
python -m src.day3.credit_decisioning.sample_data

# Run CLI tools
python -m src.day1.data_quality.cli --help
python -m src.day2.aml_triage.cli --help
python -m src.day2.pii_protection.cli --help

# Collect evidence bundle
python scripts/day3_collect_evidence.py
```

---

## 🔍 How to Navigate This Repository

### Learning Path 1: Structured (Recommended for First Time)

**Follow this exact order:**

1. Start: [README.md](README.md)
2. Day 1: [day1_foundations/README.md](day1_foundations/README.md)
   - Session 1.1 → Session 1.2 → Lab 1 → Lab 2 → Session 1.3
3. Day 2: [day2_agent_workflows/README.md](day2_agent_workflows/README.md)
   - Session 2.1 → Session 2.2 → Lab 3 → Lab 4 → Session 2.3
4. Day 3: [day3_capstone/README.md](day3_capstone/README.md)
   - Read docs → Build system → Generate artifacts → Demo
5. End: Complete reflexion exercises at end of each day

### Learning Path 2: Fast Track (For Experienced Developers)

**Generate all code quickly, then study it:**

1. Read: [TRAINING_TOC.md](TRAINING_TOC.md) - Understand structure
2. Generate Day 1: Use [day1_foundations/prompts/day1_prompts.md](day1_foundations/prompts/day1_prompts.md) → Prompts D1-1, D1-2
3. Generate Day 2: Use [day2_agent_workflows/prompts/day2_prompts.md](day2_agent_workflows/prompts/day2_prompts.md) → All prompts
4. Generate Day 3: Use [day3_capstone/prompts/day3_prompts.md](day3_capstone/prompts/day3_prompts.md) → Prompt D3-1
5. Study: Read generated code, understand patterns, run all tests

### Learning Path 3: Reference (When You Need Specific Information)

**Jump to what you need:**

| Need | Go To |
|------|-------|
| Understand prompting | [day1_foundations/session1_2_prompting_in_vscode.md](day1_foundations/session1_2_prompting_in_vscode.md) |
| Copy-paste prompts | `day*/prompts/*.md` files |
| Build specific lab | `day*/labs/*.md` files |
| Understand architecture | [day3_capstone/capstone_architecture.md](day3_capstone/capstone_architecture.md) |
| Troubleshoot | [day3_capstone/capstone_runbook.md](day3_capstone/capstone_runbook.md) |
| Security threats | [day3_capstone/threat_model.md](day3_capstone/threat_model.md) |
| All topics | [TRAINING_TOC.md](TRAINING_TOC.md) |

---

## 🎯 Success Criteria: How to Know You're Done

### Day 1 Complete When...
- [ ] All Day 1 tests pass: `pytest tests/day1/ -v` ✅
- [ ] Data Quality CLI works: `python -m src.day1.data_quality.cli --help` ✅
- [ ] Risk Scoring API works: Visit `http://127.0.0.1:8000/docs` ✅
- [ ] You can explain 3C Framework (Context, Constraints, Criteria)
- [ ] You understand deterministic vs non-deterministic code

### Day 2 Complete When...
- [ ] All Day 2 tests pass: `pytest tests/day2/ -v` ✅
- [ ] AML pipeline generates alerts: Check `out/day2/alerts_*.json` ✅
- [ ] PII masking works: Output has `***` instead of emails ✅
- [ ] You can decompose an epic into tasks
- [ ] You can refactor code safely with test loops

### Day 3 Complete When...
- [ ] All Day 3 tests pass: `pytest tests/day3/ -v` ✅
- [ ] All 5 API endpoints work: Test via `/docs` ✅
- [ ] Audit log excludes PII: `test_audit_log_no_pii` passes ✅
- [ ] Evidence bundle created: `python scripts/day3_collect_evidence.py` ✅
- [ ] You can explain the decision algorithm
- [ ] You can navigate the threat model and risk register

---

## 📝 Tips for Success

### General Tips

1. **Don't skip the theory sessions** - Mental models matter for effective AI usage
2. **Read documentation before prompting** - Understand what you're building
3. **Use Agent Mode for bulk generation** - Let AI handle boilerplate
4. **Use Copilot Chat for learning** - Ask "why" and "how" questions
5. **Always run tests** - Verify AI-generated code works correctly
6. **Commit frequently** - Use git to save progress after each module

### Prompting Tips

**Good Prompt:**
```
Build a Python function to calculate debt-to-income ratio.
Input: annual_income (float), total_monthly_debt (float)
Output: dti (float, range 0.0 to 1.0)
Constraints: Handle zero income by returning 1.0 (worst DTI)
Include: Docstring, type hints, 3 pytest test cases
```

**Bad Prompt:**
```
Make a DTI function
```

### Testing Tips

1. **Run tests after every change** - Catch regressions early
2. **Test edge cases** - Zero values, negative numbers, empty strings
3. **Test determinism** - Same input → same output (run test twice)
4. **Test PII exclusion** - Read audit files, assert no sensitive data
5. **Test error handling** - Invalid inputs should return proper errors

### Debugging Tips

```powershell
# If imports fail:
python -c "import sys; print(sys.path)"  # Check PYTHONPATH

# If tests fail with "module not found":
pip install -e .  # Install package in editable mode

# If API won't start:
uvicorn src.day3.credit_decisioning.app:app --reload --log-level debug

# If database is corrupted:
rm out/day3/credit_decisioning.db  # Delete and regenerate

# If confused:
gh copilot explain "pytest --cov=src.day3"  # Ask Copilot CLI
```

---

## 🔗 Key Concepts Reference

### Deterministic Code
**Definition:** Same input always produces same output (no random numbers, no timestamps affecting logic)  
**Why:** Banking systems must be reproducible for audits  
**Example:** Score = baseline + adjustment (never uses `random.randint()`)

### Reason Codes
**Definition:** Human-readable explanations for decisions  
**Why:** Regulatory requirement (explain why credit was denied)  
**Example:** `["HIGH_DTI", "POOR_PAYMENT_HISTORY", "SCORE_DECLINE_BAND"]`

### Audit Trail
**Definition:** Immutable log of all decisions  
**Why:** Compliance and forensics  
**Format:** JSONL (one JSON object per line, append-only)  
**Critical:** Must exclude raw PII (name, address, email)

### Data Minimization
**Definition:** Only store/log what's necessary  
**Why:** GDPR, CCPA compliance  
**Example:** Log DTI ratio (derived feature), NOT income and debt (raw PII)

### 3C Framework (Prompting)
- **Context:** What are we building? (problem space, inputs, outputs)
- **Constraints:** What rules must we follow? (no MCP, use Pydantic, deterministic)
- **Criteria:** How do we know it's done? (tests pass, API responds, audit log created)

### Test Hierarchy
1. **Syntax:** Code compiles/runs without errors
2. **Unit:** Individual functions work correctly
3. **Integration:** Modules work together
4. **End-to-End:** Full user workflows succeed
5. **Compliance:** Determinism, PII exclusion, audit trails verified

---

## 📞 Support and Resources

### When You're Stuck

1. **Check the runbook:** [day3_capstone/capstone_runbook.md](day3_capstone/capstone_runbook.md) - Troubleshooting section
2. **Ask Copilot Chat:** `@workspace why are my tests failing?`
3. **Ask Copilot CLI:** `gh copilot explain "<error message>"`
4. **Review session materials:** Re-read relevant session docs
5. **Check test output:** `pytest -v` shows which test failed and why

### Additional Learning Resources

- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **Pytest Documentation:** https://docs.pytest.org/
- **GitHub Copilot Docs:** https://docs.github.com/copilot

---

## 🎉 Congratulations!

If you've completed all three days, you now have:

✅ **Skills:** AI-assisted development for banking-grade systems  
✅ **Knowledge:** Prompting, testing, governance, compliance  
✅ **Portfolio:** 3 complete projects (data quality, AML, credit decisioning)  
✅ **Artifacts:** Code, tests, docs, threat models, evidence bundles  

**Next Steps:**
1. Apply these patterns to your real projects
2. Customize labs for your specific domain
3. Share learnings with your team
4. Continue practicing with new features

**Remember:** AI is a tool, not a replacement. You're the architect, engineer, and auditor. Use Copilot to accelerate, but always verify, test, and think critically.

---

## 📄 License and Attribution

This training material is provided for educational purposes. All code examples use synthetic data only.

**Version:** 1.0  
**Last Updated:** December 21, 2025  
**Maintained By:** GitHub Copilot Banking Bootcamp Team

---

**Ready to start?** → [Day 1 README](day1_foundations/README.md)
