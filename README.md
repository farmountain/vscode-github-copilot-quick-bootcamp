# GitHub Copilot Banking Bootcamp

**3-Day Intensive Training: Banking-Grade AI-Assisted Development**

Learn to build production-ready financial software using VS Code + GitHub Copilot Chat + Agent Mode + CLI.

---

## 🚀 Quick Start

**New Students Start Here:**

1. 📖 **[STUDENT_GUIDE.md](STUDENT_GUIDE.md)** - Complete end-to-end guide with diagrams, learning paths, and daily breakdowns
2. 📖 **[TRAINING_TOC.md](TRAINING_TOC.md)** - Detailed table of contents for all materials
3. 📖 **[Day 1 README](day1_foundations/README.md)** - Begin your training journey

**Experienced Developers (Fast Track):**
- Jump to prompt playbooks: [Day 1](day1_foundations/prompts/day1_prompts.md) | [Day 2](day2_agent_workflows/prompts/day2_prompts.md) | [Day 3](day3_capstone/prompts/day3_prompts.md)
- Generate all code with Agent Mode, then study the implementations

---

## 📚 What You'll Learn

### Day 1: Foundations (6-8 hours)
Build single-module systems with effective prompting and comprehensive tests.

**Projects:**
- ✅ Data Quality Rules Engine (transaction validation)
- ✅ Risk Scoring Service (credit API with FastAPI)

**Skills:**
- Effective prompt engineering (3C Framework)
- GitHub Copilot Chat, Agent Mode, and CLI
- Deterministic algorithms and audit trails
- Test-driven development for AI-generated code

### Day 2: Agent Workflows (6-8 hours)
Master multi-module systems, safe refactoring, and automation.

**Projects:**
- ✅ AML Alert Triage Pipeline (fraud detection)
- ✅ PII Protection Library (masking + tokenization)

**Skills:**
- Epic → Task decomposition
- Multi-file refactoring with test loops
- CLI automation with Copilot CLI
- Banking-safe patterns (determinism, data privacy)

### Day 3: Capstone (6-8 hours)
Build complete end-to-end system with governance artifacts.

**Project:**
- ✅ Credit Decisioning Service (FastAPI + SQLite + Audit)
  - 5 REST endpoints
  - Deterministic scoring with reason codes
  - Audit logging (no PII)
  - Threat model + Risk register
  - Evidence bundle for compliance

**Skills:**
- Requirements → Architecture → Implementation → Governance
- RESTful API design with FastAPI
- Decision explainability (reason codes)
- Security threat modeling
- Evidence collection for audits

---

## 🎯 Learning Outcomes

By the end of this bootcamp, you will be able to:

✅ Write effective prompts that generate production-quality code  
✅ Build banking-grade systems with audit trails and explainability  
✅ Implement deterministic algorithms (same input → same output)  
✅ Create comprehensive test suites (unit + integration + E2E)  
✅ Apply data privacy principles (PII exclusion, data minimization)  
✅ Generate governance artifacts (threat models, risk registers)  
✅ Package evidence bundles for compliance review  
✅ Use GitHub Copilot Chat, Agent Mode, and CLI productively  

---

## 📊 Repository Structure

```
vscode-github-copilot-quick-bootcamp/
├── 📘 STUDENT_GUIDE.md              ⭐ START HERE - Complete learning guide
├── 📘 TRAINING_TOC.md                # Detailed table of contents
├── 📘 IMPLEMENTATION_SUMMARY.md      # Technical implementation notes
│
├── 📂 day1_foundations/              # Day 1: Learn basics
│   ├── README.md
│   ├── session*.md                   # Theory sessions
│   ├── labs/*.md                     # Hands-on labs
│   └── prompts/day1_prompts.md       # 🎯 Copy-paste prompts
│
├── 📂 day2_agent_workflows/          # Day 2: Advanced patterns
│   ├── README.md
│   ├── session*.md
│   ├── labs/*.md
│   └── prompts/day2_prompts.md       # 🎯 Copy-paste prompts
│
├── 📂 day3_capstone/                 # Day 3: Complete system
│   ├── README.md
│   ├── capstone_*.md                 # Requirements, architecture, runbook
│   ├── threat_model.md               # Security analysis
│   ├── risk_register.md              # Risk management
│   ├── labs/*.md
│   └── prompts/day3_prompts.md       # 🎯 Copy-paste prompts
│
├── 📂 src/                           # Your implementations go here
│   ├── day1/                         # Lab 1 + Lab 2 code
│   ├── day2/                         # Lab 3 + Lab 4 code
│   └── day3/                         # Capstone code
│
├── 📂 tests/                         # All test files
│   ├── day1/
│   ├── day2/
│   └── day3/
│
├── 📂 scripts/                       # Automation scripts
│   └── day3_collect_evidence.py      # Evidence bundle generator
│
├── 📂 .vscode/                       # VS Code configuration
│   └── tasks.json                    # One-click run commands
│
└── 📂 out/                           # Generated outputs
    └── day3/
        ├── credit_decisioning.db     # SQLite database
        ├── audit_log.jsonl           # Audit trail
        └── evidence_bundle_*.zip     # Packaged evidence
```

---

## 🛠️ Prerequisites

Before starting, ensure you have:

- [ ] **VS Code** installed (latest version)
- [ ] **GitHub Copilot** extension installed and activated
- [ ] **GitHub Copilot subscription** (or free trial)
- [ ] **Python 3.10+** installed
- [ ] **pip** package manager working
- [ ] **Git** installed and configured
- [ ] Basic Python knowledge
- [ ] Understanding of REST APIs (helpful but not required)

### Installation

```powershell
# Clone repository
git clone https://github.com/your-org/vscode-github-copilot-quick-bootcamp.git
cd vscode-github-copilot-quick-bootcamp

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# OR: source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install fastapi uvicorn pydantic pytest httpx pytest-cov

# Verify
python -c "import fastapi, pydantic, pytest; print('✅ Ready to start!')"

# Open in VS Code
code .
```

---

## 📖 How to Use This Bootcamp

### Option 1: Structured Learning (Recommended for First Time)
Follow day-by-day in order:
1. Read [STUDENT_GUIDE.md](STUDENT_GUIDE.md) for complete overview
2. Start [Day 1](day1_foundations/README.md) → [Day 2](day2_agent_workflows/README.md) → [Day 3](day3_capstone/README.md)
3. Complete all sessions and labs sequentially
4. Do reflexion exercises at end of each day

### Option 2: Fast Track (For Experienced Developers)
Generate all code quickly, then study:
1. Read [TRAINING_TOC.md](TRAINING_TOC.md) to understand structure
2. Use prompt playbooks to generate all implementations
3. Run all tests to verify: `pytest tests/ -v`
4. Study generated code to understand patterns

### Option 3: Reference Mode (When You Need Specific Info)
Jump to what you need:
- **Learn prompting:** [day1_foundations/session1_2_prompting_in_vscode.md](day1_foundations/session1_2_prompting_in_vscode.md)
- **Build specific lab:** Check `day*/labs/*.md`
- **Copy prompts:** Use `day*/prompts/*.md` files
- **Troubleshoot:** [day3_capstone/capstone_runbook.md](day3_capstone/capstone_runbook.md)

---

## 🎓 Success Criteria

### You've Completed This Bootcamp When...

**Day 1:**
- [x] All tests pass: `pytest tests/day1/ -v`
- [x] You can explain the 3C prompting framework
- [x] You understand deterministic vs non-deterministic code

**Day 2:**
- [x] All tests pass: `pytest tests/day2/ -v`
- [x] You can decompose epics into agent-friendly tasks
- [x] You can refactor safely with test loops

**Day 3:**
- [x] All tests pass: `pytest tests/day3/ -v`
- [x] All 5 API endpoints work
- [x] Audit log excludes PII (test_audit_log_no_pii passes)
- [x] Evidence bundle created
- [x] You can explain threat models and risk registers

---

## 🔧 Quick Commands

```powershell
# Run all tests
pytest tests/ -v

# Run Day 3 capstone tests
pytest tests/day3/ -v

# Start Day 3 API server
uvicorn src.day3.credit_decisioning.app:app --reload

# Generate Day 3 sample data
python -m src.day3.credit_decisioning.sample_data

# Run Day 3 end-to-end demo
python -m src.day3.credit_decisioning.demo_e2e

# Collect evidence bundle
python scripts/day3_collect_evidence.py

# Use VS Code tasks (Ctrl+Shift+P → "Tasks: Run Task")
# - Day3: Run Capstone Tests
# - Day3: Run Capstone API Server
# - Day3: Verify All (Composite)
```

---

## 💡 Key Concepts

- **Deterministic Code:** Same input → same output (required for audits)
- **Reason Codes:** Explainable decisions (regulatory requirement)
- **Audit Trail:** Immutable log without PII (JSONL format)
- **Data Minimization:** Only log what's necessary (GDPR/CCPA)
- **3C Framework:** Context + Constraints + Criteria (effective prompting)
- **Test Hierarchy:** Syntax → Unit → Integration → E2E → Compliance

---

## 🤝 Support

- **Documentation:** Check [STUDENT_GUIDE.md](STUDENT_GUIDE.md) for comprehensive help
- **Troubleshooting:** See [day3_capstone/capstone_runbook.md](day3_capstone/capstone_runbook.md)
- **Ask Copilot:** Use `@workspace` in Copilot Chat
- **Ask CLI:** Use `gh copilot explain "<error>"`

---

## 📄 License

This training material is provided for educational purposes. All code examples use synthetic data only.

---

**Ready to start?** → [STUDENT_GUIDE.md](STUDENT_GUIDE.md) → [Day 1 README](day1_foundations/README.md)