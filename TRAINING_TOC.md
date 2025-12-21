# Training Table of Contents

**GitHub Copilot Quick Bootcamp**: Banking-Grade Agentic Development

---

## Quick Start

* [Main README](README.md) - Overview and getting started
* [Prerequisites](docs/prerequisites.md) - What you need before starting

---

## Day 1: Foundations (VS Code + Copilot Chat + Agent Mode + Copilot CLI)

**Goal**: Learn to reliably go from task → agent prompt → multi-file change → tests/verification → readable docs using synthetic data only.

### Day 1 Overview
* **[Day 1 README](day1_foundations/README.md)** - Complete Day 1 guide and schedule

### Sessions

1. **[Session 1.1: Introduction to Agentic Development](day1_foundations/session1_1_intro_to_agentic_dev.md)** (09:00–10:30)
   - From autocomplete to agentic AI
   - Mental models and safety considerations
   - Paul-Elder critical thinking framework
   - Inversion thinking and failure modes
   - Copilot Chat basics

2. **[Session 1.2: Prompting in VS Code](day1_foundations/session1_2_prompting_in_vscode.md)** (10:45–12:15)
   - 3C Framework: Context, Constraints, Criteria
   - GitHub Copilot Chat features (slash commands, context references)
   - GitHub Copilot Agent Mode walkthrough
   - GitHub Copilot CLI essentials
   - Advanced prompting techniques

3. **[Session 1.3: Verification and Testing](day1_foundations/session1_3_verification_and_tests.md)** (17:15–17:45)
   - Verification hierarchy (syntax → unit → integration → compliance)
   - Testing strategies for AI-generated code
   - Code review checklists
   - Reflexion framework
   - Creating audit-ready evidence

### Hands-On Labs

1. **[Lab 1: Data Quality Rules Engine](day1_foundations/labs/lab1_data_quality_rules_engine.md)** (13:30–15:30)
   - Build a transaction validation system
   - Implement deterministic validation rules
   - Create audit-ready reports
   - Generate synthetic test data
   - Write comprehensive tests

2. **[Lab 2: Simple Risk Scoring Service](day1_foundations/labs/lab2_simple_risk_scoring_service.md)** (15:45–17:15)
   - Build an explainable credit risk API (FastAPI)
   - Implement deterministic scoring with reason codes
   - Create audit logging
   - Write API tests
   - Generate synthetic credit applications

### Reference Materials

* **[Day 1 Prompts Playbook](day1_foundations/prompts/day1_prompts.md)** - All copy-paste prompts for labs
  - Prompt D1-1: Generate Lab 1 code
  - Prompt D1-2: Generate Lab 2 code
  - Prompt D1-3: Add VS Code tasks
  - Prompt D1-4: Add Copilot CLI mini-bootcamp
  - Quick prompts for common tasks
  - Troubleshooting guide

---

## Day 2: Agent Workflows (VS Code + Copilot Chat + Agent Mode + Copilot CLI)

**Goal**: Run agentic workflows end-to-end: **plan → implement across multiple files → run test loops → refactor safely → automate via Copilot CLI → document/runbook**. Banking-grade patterns with NO MCP.

### Day 2 Overview
* **[Day 2 README](day2_agent_workflows/README.md)** - Complete Day 2 guide and schedule

### Sessions

1. **[Session 2.1: Agent Planning & Task Breakdown](day2_agent_workflows/session2_1_agent_planning_and_task_breakdown.md)** (09:00–10:30)
   - From epics to tasks to acceptance criteria
   - Agent Mode as a contractor (Feynman model)
   - The Epic → Task decomposition recipe
   - Paul–Elder framework applied to prompts
   - Stop points for incremental review
   - Micro-exercise: decompose a feature

2. **[Session 2.2: Multi-File Refactor + Test Loops](day2_agent_workflows/session2_2_multi_file_refactor_and_test_loops.md)** (10:45–12:15)
   - Why multi-file changes break + safety net pattern
   - Refactoring as rewiring a house (Feynman model)
   - The refactoring recipe with Agent Mode
   - Red-green-refactor cycle with test loops
   - Live demo: refactor Day 1 code safely
   - Hands-on exercise: refactor a module

3. **[Session 2.3: CLI Automation with GitHub Copilot CLI](day2_agent_workflows/session2_3_cli_automation_with_copilot_cli.md)** (Integrated throughout)
   - Introduction to `gh copilot suggest` and `gh copilot explain`
   - Safe CLI exercises (find, test, diff, count)
   - Workflow integration (test → commit automation)
   - Safety guidelines (what to automate, what to review)
   - Building test automation scripts

### Hands-On Labs

1. **[Lab 3: AML Alert Triage Pipeline](day2_agent_workflows/labs/lab3_aml_alert_triage_pipeline.md)** (13:30–15:30)
   - Build automated AML alert triage system
   - Implement deterministic heuristic rules (HIGH_VELOCITY, ROUND_AMOUNT, HIGH_AMOUNT, RAPID_REVERSAL)
   - Score alerts and assign triage priority (P1/P2/P3)
   - Generate audit-friendly outputs (JSON alerts, CSV queue, summary)
   - Multi-module implementation: schemas, rules, triage, pipeline, CLI
   - Test loops and determinism verification

2. **[Lab 4: PII Masking/Tokenization + Audit Logging](day2_agent_workflows/labs/lab4_pii_masking_and_audit_logging.md)** (15:45–17:15)
   - Build PII protection library
   - Implement masking functions (email, phone, national ID, address, DOB)
   - Implement deterministic tokenization (HMAC-based)
   - Field redaction and allowlisting
   - Audit logging without storing raw PII
   - Multi-mode CLI (MASK, TOKENIZE, REDACT)

### Reference Materials

* **[Day 2 Prompts Document](day2_agent_workflows/prompts/day2_prompts.md)** - All copy-paste prompts for labs
  - Session 2.1 micro-exercise prompts
  - Session 2.2 refactoring exercise prompts
  - Lab 3 prompts (schemas, rules, triage, I/O, pipeline, CLI)
  - Lab 4 prompts (config, masking, tokenization, redaction, audit, CLI)
  - General-purpose prompts (explain, test generation, security review)

---

## Day 3: Capstone — Credit Decisioning Slice (VS Code + Copilot Chat + Agent Mode + Copilot CLI)

**Goal**: Deliver a **mini end-to-end system slice** with clear architecture, requirements traceability, implementation across multiple modules, tests, audit trail, decision explainability, deterministic behavior, runbook, threat model, risk register, and reproducible demo.

### Day 3 Overview
* **[Day 3 README](day3_capstone/README.md)** - Complete Day 3 guide and schedule

### Core Materials

* **[Capstone Overview](day3_capstone/capstone_overview.md)** - System vision, high-level architecture, key components
* **[Capstone Requirements](day3_capstone/capstone_requirements.md)** - Functional/non-functional requirements, API contracts, decision rules, acceptance criteria, requirements traceability matrix
* **[Capstone Architecture](day3_capstone/capstone_architecture.md)** - Component architecture, data flow diagrams, data model, technology stack, design patterns
* **[Capstone Runbook](day3_capstone/capstone_runbook.md)** - Installation, configuration, running the service, verification steps, troubleshooting, evidence bundle creation

### Governance Artifacts

* **[Threat Model](day3_capstone/threat_model.md)** - Attack surfaces, threat scenarios, mitigations, verification
* **[Risk Register](day3_capstone/risk_register.md)** - Risk descriptions, likelihood/impact ratings, mitigation strategies

### Lab

* **[Lab: Build Credit Decisioning Slice](day3_capstone/labs/capstone_build_credit_decisioning_slice.md)** (13:30–16:30)
  - Build FastAPI REST service (5 endpoints)
  - Implement deterministic decision engine with reason codes
  - Create audit logging (JSONL format, no raw PII)
  - Build repository layer (SQLite or file-based JSON)
  - Generate synthetic sample data
  - Write comprehensive test suite (unit + API + end-to-end)
  - Create end-to-end demo script
  - Package evidence bundle for audit review

### Reference Materials

* **[Day 3 Copilot Agent Prompts](day3_capstone/prompts/day3_prompts.md)** - All copy-paste prompts for capstone
  - Prompt D3-1: Implement capstone code (modules a-n)
  - Prompt D3-2: Generate governance artifacts
  - Prompt D3-3: Add VS Code tasks
  - Prompt D3-4: Create evidence bundle
  - Prompt D3-5: Update training TOC
  - GitHub Copilot CLI exercises (6 safe commands)
  - Troubleshooting prompts

---

## Reference Documentation

### Frameworks and Templates

* [Paul-Elder Critical Thinking Framework](docs/frameworks/paul_elder_framework.md)
* [Feynman Explanation Template](docs/frameworks/feynman_template.md)
* [Inversion Thinking Guide](docs/frameworks/inversion_thinking.md)
* [Reflexion Framework](docs/frameworks/reflexion_framework.md)

### Templates

* [Prompt Template (3C Framework)](docs/templates/prompt_template.md)
* [Test Suite Template](docs/templates/test_suite_template.md)
* [API Documentation Template](docs/templates/api_doc_template.md)
* [Code Review Checklist](docs/templates/code_review_checklist.md)

### Additional Resources

* [Banking Safety Guidelines](docs/banking_safety_guidelines.md)
* [Compliance Checklist](docs/compliance_checklist.md)
* [Troubleshooting Guide](docs/troubleshooting.md)
* [Glossary](docs/glossary.md)

---

## Quick Navigation

### By Role

**For Developers**:
* Start with [Day 1 README](day1_foundations/README.md)
* Use [Prompts Playbook](day1_foundations/prompts/day1_prompts.md) for quick reference
* Check [Troubleshooting Guide](docs/troubleshooting.md) when stuck

**For Instructors**:
* Review all session materials in order
* Use session timings and agendas for planning
* Adapt exercises based on learner pace

**For Auditors/Reviewers**:
* Focus on verification sections in each session
* Review [Banking Safety Guidelines](docs/banking_safety_guidelines.md)
* Check [Compliance Checklist](docs/compliance_checklist.md)

### By Task

**Setting up your environment**:
1. [Prerequisites](docs/prerequisites.md)
2. [Day 1 README - Quick Start](day1_foundations/README.md#quick-start-how-to-run-day-1)

**Learning to prompt effectively**:
1. [Session 1.2: Prompting in VS Code](day1_foundations/session1_2_prompting_in_vscode.md)
2. [Prompt Template (3C Framework)](docs/templates/prompt_template.md)
3. [Prompts Playbook](day1_foundations/prompts/day1_prompts.md)

**Building your first project**:
1. [Lab 1: Data Quality Rules Engine](day1_foundations/labs/lab1_data_quality_rules_engine.md)
2. [Lab 2: Risk Scoring Service](day1_foundations/labs/lab2_simple_risk_scoring_service.md)

**Testing and verification**:
1. [Session 1.3: Verification and Testing](day1_foundations/session1_3_verification_and_tests.md)
2. [Test Suite Template](docs/templates/test_suite_template.md)
3. [Code Review Checklist](docs/templates/code_review_checklist.md)

---

## Progress Tracking

Use this checklist to track your progress through the bootcamp:

### Day 1: Foundations
- [ ] Completed Session 1.1 (Intro to Agentic Dev)
- [ ] Completed Session 1.2 (Prompting in VS Code)
- [ ] Completed Lab 1 (Data Quality Rules Engine)
  - [ ] All code generated
  - [ ] All tests passing
  - [ ] Verified with sample data
- [ ] Completed Lab 2 (Risk Scoring Service)
  - [ ] API running
  - [ ] All tests passing
  - [ ] Audit log working
- [ ] Completed Session 1.3 (Verification and Testing)
- [ ] Day 1 Reflexion completed

### Day 2: Agent Workflows
- [ ] Completed Session 2.1 (Agent Planning & Task Breakdown)
- [ ] Completed Session 2.2 (Multi-File Refactor + Test Loops)
- [ ] Completed Session 2.3 (CLI Automation with Copilot CLI)
- [ ] Completed Lab 3 (AML Alert Triage Pipeline)
  - [ ] All modules implemented
  - [ ] All tests passing
  - [ ] Determinism verified
- [ ] Completed Lab 4 (PII Masking/Tokenization + Audit Logging)
  - [ ] All masking functions working
  - [ ] Tokenization verified
  - [ ] Audit log excluding PII
- [ ] Day 2 Reflexion completed

### Day 3: Capstone — Credit Decisioning Slice
- [ ] Reviewed Capstone Overview
- [ ] Reviewed Capstone Requirements
- [ ] Reviewed Capstone Architecture
- [ ] Completed Capstone Lab (Build Credit Decisioning Slice)
  - [ ] All 5 API endpoints implemented
  - [ ] Decision engine with reason codes working
  - [ ] Audit log excluding PII verified
  - [ ] All tests passing (unit + API + E2E)
  - [ ] Evidence bundle created
- [ ] Reviewed Threat Model
- [ ] Reviewed Risk Register
- [ ] Day 3 Reflexion completed

---

## Success Criteria

By the end of this bootcamp, you should be able to:

### Day 1 Outcomes
- [x] Articulate the difference between autocomplete and agentic development
- [x] Write effective prompts using the 3C framework
- [x] Use GitHub Copilot Chat and Agent Mode effectively
- [x] Use GitHub Copilot CLI for command-line productivity
- [x] Write comprehensive tests for AI-generated code
- [x] Apply verification and reflexion techniques
- [x] Create audit-ready documentation and evidence

### Day 2 Outcomes
- [x] Plan and decompose features using agent-friendly prompts
- [x] Execute multi-file refactors safely with test loops
- [x] Automate workflows using GitHub Copilot CLI
- [x] Build banking-grade systems with deterministic behavior
- [x] Implement comprehensive audit logging without PII leakage
- [x] Write test suites that verify critical safety properties

### Day 3 Outcomes
- [x] Build mini end-to-end system slices from requirements to evidence
- [x] Implement deterministic decision engines with explainability
- [x] Create audit-ready documentation (requirements traceability, architecture, runbook)
- [x] Generate governance artifacts (threat models, risk registers)
- [x] Package evidence bundles for compliance review
- [x] Apply banking-grade engineering practices end-to-end

---

## Support

* **Questions during training**: Ask your instructor or use the dedicated Q&A sessions
* **Technical issues**: See [Troubleshooting Guide](docs/troubleshooting.md)
* **Feedback**: Share your experiences in the Day 1/2/3 Reflexion sessions

---

## Version History

* **v1.0.0** (2024-01-15): Initial Day 1 content release
  - Sessions 1.1, 1.2, 1.3
  - Labs 1 and 2
  - Prompts playbook
  - Core frameworks and templates

---

**Ready to start?** → [Day 1 README](day1_foundations/README.md)
