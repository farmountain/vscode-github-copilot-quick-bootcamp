# Day 1 — Foundations: VS Code + Copilot Chat + Agent Mode + Copilot CLI

**Banking-grade agentic development: From task → agent prompt → multi-file change → tests/verification → readable docs**

## Day 1 Outcome

By the end of Day 1, learners will be able to reliably go from *task → agent prompt → multi-file change → tests/verification → readable docs* using **synthetic data only**, with a **human review + audit mindset**.

## What You'll Learn

* How GitHub Copilot moves beyond autocomplete to agentic development
* How to craft effective prompts with clear constraints and acceptance criteria
* How to use GitHub Copilot Agent Mode to automate multi-file changes
* How to use GitHub Copilot CLI for command-line productivity
* How to verify and test AI-generated code with a banking compliance mindset
* How to maintain audit trails and documentation for regulatory requirements

## Day 1 Schedule (Full-day Flow)

| Time | Session | Description |
|------|---------|-------------|
| 09:00–10:30 | **Session 1.1** | From "autocomplete" to "agentic dev" (mental model + safety) |
| 10:45–12:15 | **Session 1.2** | Prompting in VS Code (context, constraints, acceptance criteria) |
| 13:30–15:30 | **Lab 1** | Data Quality Rules Engine (transactions, bank-style checks) |
| 15:45–17:15 | **Lab 2** | Simple Risk Scoring Service (credit apps, explainable scoring + audit log) |
| 17:15–17:45 | **Session 1.3** | Verification mindset + reflexion retro |

## Training Materials

### Sessions

1. **[Session 1.1: Introduction to Agentic Development](session1_1_intro_to_agentic_dev.md)**
   - Understanding the shift from autocomplete to agentic AI
   - Mental models for working with AI assistants
   - Safety and compliance considerations for banking contexts

2. **[Session 1.2: Prompting in VS Code](session1_2_prompting_in_vscode.md)**
   - Effective prompt engineering with the Paul-Elder framework
   - Using context, constraints, and acceptance criteria
   - GitHub Copilot Chat and Agent Mode features
   - GitHub Copilot CLI fundamentals

3. **[Session 1.3: Verification and Tests](session1_3_verification_and_tests.md)**
   - Testing AI-generated code
   - Verification mindset for banking applications
   - Reflexion and continuous improvement

### Hands-on Labs

1. **[Lab 1: Data Quality Rules Engine](labs/lab1_data_quality_rules_engine.md)**
   - Build a transaction validation system
   - Implement common banking data quality checks
   - Create deterministic, auditable results

2. **[Lab 2: Simple Risk Scoring Service](labs/lab2_simple_risk_scoring_service.md)**
   - Build an explainable credit risk scoring API
   - Implement audit logging
   - Create testable, deterministic scoring logic

### Reference Materials

* **[Day 1 Prompts Playbook](prompts/day1_prompts.md)** - All copy-paste prompts for labs

## Prerequisites

* VS Code installed with GitHub Copilot extension
* GitHub Copilot subscription (or trial)
* Python 3.9+ installed
* Git installed
* Basic Python knowledge
* Understanding of banking/financial concepts (helpful but not required)

## Quick Start: How to Run Day 1

### Option 1: Follow the Training in Order

1. **Morning Sessions** - Work through Sessions 1.1 and 1.2 to build foundational understanding
2. **Afternoon Labs** - Complete Lab 1 and Lab 2 to build hands-on skills
3. **Wrap-up** - Review Session 1.3 and conduct reflexion exercises

### Option 2: Self-Paced Code Generation (Using Copilot Agent)

If you want to generate all the code implementations quickly:

1. Open this repository in VS Code
2. Enable GitHub Copilot Agent Mode
3. Run the prompts in order from [Day 1 Prompts Playbook](prompts/day1_prompts.md):
   - **Prompt D1-1**: Generates Lab 1 code (Data Quality Rules Engine)
   - **Prompt D1-2**: Generates Lab 2 code (Risk Scoring Service)
   - **Prompt D1-3**: Adds VS Code tasks for one-click verification
   - **Prompt D1-4**: Adds Copilot CLI mini-bootcamp

### Option 3: Manual Step-by-Step Learning

Follow each lab document step-by-step, using GitHub Copilot Chat to assist you with writing the code yourself. This is the recommended approach for deepest learning.

## Core Principles (Banking-Grade Development)

### First Principles

* **Copilot is a powerful text-to-code assistant, not a truth engine**
* The only reliable "truth" is:
  1. **Your acceptance criteria**
  2. **Tests + runnable verification**
  3. **Reviewable diffs**

### Feynman-Style Mental Model

* **Copilot Chat** = "talking to a teammate"
* **Agent Mode** = "teammate who can actually edit files and run steps"
* **You** = "team lead who defines success, reviews, and approves"
* **Tests/Tasks** = "bank controls and reconciliations—proof you didn't break things"

### Paul-Elder Critical Thinking Framework

For every request to Copilot/Agent, state:

* **Purpose**: What outcome do we want?
* **Question**: What are we building/changing?
* **Information**: What files/data do we rely on? (synthetic only)
* **Assumptions**: What constraints? What are we *not* doing?
* **Implications**: What could go wrong in a bank context? (audit, PII, model risk)
* **Point of view**: Developer + reviewer + auditor perspectives

### Inversion Thinking (How Projects Fail)

* Vague prompts → wrong code
* No tests → silent failure
* No logging/audit trail → compliance rejection
* "Copy-paste sensitive data" → policy breach
* No deterministic behavior → irreproducible results

### Reflexion Loop (After Every Session/Lab)

* What did the agent do well?
* Where did it hallucinate or overreach?
* What evidence do we have it works?
* What guardrail did we miss?

## Banking Safety Rules (Day 1)

✅ **DO**:
* Use synthetic data only
* Include explicit acceptance criteria in every prompt
* Write tests before or alongside implementation
* Create audit trails (logs, diffs, test outputs)
* Review all AI-generated code before running
* Use deterministic logic (no random seeds in production patterns)
* Document assumptions and limitations

❌ **DON'T**:
* Never use real customer data, PII, or credentials
* Never blindly accept generated code without review
* Never skip testing "because AI wrote it"
* Never assume AI understands your compliance requirements
* Never commit secrets or API keys (even accidentally)

## Tools and Commands

### VS Code Tasks (after running Prompt D1-3)

Use VS Code's task runner (Terminal > Run Task) for quick operations:

* `Day1: Generate Synthetic Data`
* `Day1: Run Data Quality CLI Demo`
* `Day1: Run Tests`
* `Day1: Run Risk API`
* `Verify-All (Day1)` - runs all verification steps

### Command Line Quick Reference

```bash
# Generate synthetic data
python -m src.samples.synthetic_data_generator

# Run Lab 1 (Data Quality)
python -m src.day1.data_quality.cli --input src/samples/sample_transactions.csv --output output/dq_report.json

# Run Lab 2 (Risk Scoring API)
uvicorn src.day1.risk_scoring_service.app:app --reload

# Run tests
pytest tests/day1/ -v

# Run all tests quietly
pytest -q
```

### GitHub Copilot CLI

```bash
# Get command suggestions
gh copilot suggest "find all python files modified today"

# Explain a command
gh copilot explain "pytest -v --cov=src tests/"

# Target specific shell
gh copilot suggest --target shell "list files by size"
```

## Success Criteria for Day 1

By the end of Day 1, you should be able to:

* [ ] Articulate the difference between autocomplete and agentic development
* [ ] Write effective prompts using the Paul-Elder framework
* [ ] Use GitHub Copilot Agent Mode to generate multi-file solutions
* [ ] Use GitHub Copilot CLI for command-line productivity
* [ ] Write and run tests for AI-generated code
* [ ] Create audit trails and documentation
* [ ] Apply reflexion to evaluate AI outputs
* [ ] Identify common failure modes and how to avoid them

## What's Next?

After completing Day 1, you'll be ready for:

* **Day 2**: Advanced patterns with Model Context Protocol (MCP)
* **Day 3**: Real-world banking workflows and integrations

## Support and Resources

* [Main Training TOC](../TRAINING_TOC.md)
* [Day 1 Prompts Playbook](prompts/day1_prompts.md)
* Lab-specific README files in `/src/day1/`

---

**Remember**: The goal isn't to let AI write all your code. The goal is to learn how to work *with* AI as a force multiplier while maintaining professional standards, testing discipline, and audit readiness.
