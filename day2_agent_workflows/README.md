# Day 2 — Agent Workflows (VS Code + Copilot Chat + Agent Mode + Copilot CLI)

**Focus:** Agentic workflows for multi-file implementation, test loops, refactoring, and automation  
**Level:** Intermediate  
**Duration:** Full day (6 hours of instruction + labs)

---

## Overview

Day 2 teaches learners how to **manage GitHub Copilot Agent Mode** as a tool for delivering small systems end-to-end. Instead of writing code directly, learners act as **project managers** for the agent, providing:

- Clear scope and constraints
- Stop points for incremental review
- Verification commands (tests, CLI runs)
- Audit-friendly requirements (determinism, traceability)

**Outcome:** By the end of Day 2, learners can run an agentic workflow from **plan → implement → test → refactor → automate → document** for banking-grade features.

---

## Prerequisites

- **Day 1 complete:** Prompting fundamentals, inline code generation, testing
- **VS Code installed** with GitHub Copilot extension
- **GitHub Copilot CLI installed** (`gh copilot`)
- **Python 3.10+** installed with pytest
- **Git** configured and working

---

## Day 2 Schedule

| Time | Activity | Duration |
|------|----------|----------|
| 09:00–10:30 | [Session 2.1: Agent Planning & Task Breakdown](session2_1_agent_planning_and_task_breakdown.md) | 90 min |
| 10:30–10:45 | Break | 15 min |
| 10:45–12:15 | [Session 2.2: Multi-File Refactor + Test Loops](session2_2_multi_file_refactor_and_test_loops.md) | 90 min |
| 12:15–13:30 | Lunch Break | 75 min |
| 13:30–15:30 | [Lab 3: AML Alert Triage Pipeline](labs/lab3_aml_alert_triage_pipeline.md) | 120 min |
| 15:30–15:45 | Break | 15 min |
| 15:45–17:15 | [Lab 4: PII Masking/Tokenization + Audit Logging](labs/lab4_pii_masking_and_audit_logging.md) | 90 min |
| 17:15–17:45 | Reflexion Retro + Wrap | 30 min |

---

## Learning Objectives

By the end of Day 2, learners will be able to:

1. **Decompose** large features into agent-friendly tasks with clear acceptance criteria
2. **Write prompts** that constrain scope, define interfaces, and specify verification
3. **Use stop points** to control Agent Mode execution and review incremental work
4. **Execute multi-file refactors** safely with test loops and git commits
5. **Build audit-friendly systems** (deterministic, traceable, documented)
6. **Automate verification** using GitHub Copilot CLI for command suggestions
7. **Apply banking-safe patterns** (AML rules, PII protection, audit logging)

---

## Knowledge Framework

Day 2 is built on these principles:

### First Principles
- **Big tasks fail unless decomposed.** The agent needs scope, interfaces, done criteria, and verification.
- **Multi-file changes require stop points.** Stop after plan, scaffolding, tests, integration, docs.
- **Tests prevent regressions.** Run tests after every change.
- **Git is a safety net.** Commit after each verified step.

### Feynman Mental Model
- **Agent Mode is a contractor.** You provide blueprints (specs), materials (inputs), building codes (constraints), inspection checklist (tests), and staged approvals (stop points).
- **You are the project manager.** You verify work at each stage and control the pace.

### Paul–Elder Critical Thinking (Applied to Prompts)
Every prompt should address:
- **Purpose:** Why this task exists (business goal, risk management)
- **Question:** What specific question we're answering
- **Information:** Data schemas, inputs, outputs, existing code to reference
- **Assumptions:** Make explicit (no MCP, synthetic data, deterministic)
- **Implications:** What happens if this fails (false positives, audit issues, PII leaks)
- **Point of View:** Developer, analyst, auditor, compliance officer

### Inversion Thinking (What to Avoid)
- ❌ "Implement everything" prompts (too broad)
- ❌ No test loop (code compiles but logic breaks)
- ❌ Over-logging sensitive fields
- ❌ Non-deterministic results (can't reproduce for audit)
- ❌ No stop points (agent runs away with implementation)

### Reflexion Loop (End of Each Lab)
- Where did the agent make unjustified assumptions?
- What failed first in tests and why?
- Did we keep outputs deterministic and auditable?
- Did we log minimal necessary info?
- What evidence would audit want to see?

---

## Sessions

### [Session 2.1 — Agent Planning & Task Breakdown](session2_1_agent_planning_and_task_breakdown.md)

**Duration:** 90 minutes  
**Topics:**
- Why big tasks fail + the decomposition principle
- Feynman explanation: Agent Mode as a contractor
- The Epic → Task decomposition recipe (live demo)
- Paul–Elder critical thinking applied to prompts
- Stop points: controlling agent execution
- Micro-exercise: decompose a feature and write an agent prompt

**Key Takeaway:** Treat Agent Mode like a remote contractor. Provide spec, materials, inspection checklist, and staged approvals.

---

### [Session 2.2 — Multi-File Refactor + Test Loops](session2_2_multi_file_refactor_and_test_loops.md)

**Duration:** 90 minutes  
**Topics:**
- Why multi-file changes break + the safety net pattern
- Feynman explanation: refactoring as rewiring a house
- The refactoring recipe with Agent Mode (baseline → plan → execute → verify)
- Test loop pattern: red-green-refactor cycle
- Live demo: refactor Day 1 code with incremental verification
- Hands-on exercise: refactor a small module
- Advanced: extract shared logic across files

**Key Takeaway:** Refactor in small, verified increments. Run tests after EVERY change. Use git as a safety net.

---

### [Session 2.3 — CLI Automation with GitHub Copilot CLI](session2_3_cli_automation_with_copilot_cli.md)

**Duration:** Integrated throughout labs (micro-exercises)  
**Topics:**
- Introduction to `gh copilot suggest` and `gh copilot explain`
- Safe CLI exercises (find files, run tests, check diffs, count lines)
- Workflow integration (test → commit, find-and-replace, generate scripts)
- Safety guidelines (what to automate, what requires review, what to never automate)
- Building a test automation script with Copilot CLI assistance

**Key Takeaway:** Copilot CLI accelerates command discovery and explanation, but YOU review before executing.

---

## Labs

### [Lab 3 — AML Alert Triage Pipeline](labs/lab3_aml_alert_triage_pipeline.md)

**Duration:** 2 hours  
**Scenario:** Build an automated AML (Anti-Money Laundering) alert triage system that:
- Reads synthetic transactions from CSV
- Applies deterministic heuristic rules (HIGH_VELOCITY, ROUND_AMOUNT, HIGH_AMOUNT, RAPID_REVERSAL)
- Scores alerts and assigns triage priority (P1/P2/P3)
- Outputs audit-friendly reports (JSON alerts, CSV queue, summary stats)

**Learning Goals:**
- Use Agent Mode to implement a multi-module pipeline with stop points
- Write prompts with clear scope, interfaces, and verification commands
- Implement deterministic rules (same input → same output for audit)
- Run test loops after each module
- Generate audit evidence (reason codes, provenance, traceability)

**Modules Built:** schemas.py, rules.py, triage.py, io.py, pipeline.py, cli.py

**Verification:** pytest + CLI runs + determinism checks (run twice, diff outputs)

---

### [Lab 4 — PII Masking/Tokenization + Audit Logging](labs/lab4_pii_masking_and_audit_logging.md)

**Duration:** 90 minutes  
**Scenario:** Build a PII protection library that:
- Masks sensitive fields (email, phone, national ID, address, DOB)
- Tokenizes fields deterministically (HMAC-based, same input → same token)
- Redacts fields entirely (allowlist safe fields only)
- Logs protection operations WITHOUT storing raw PII

**Learning Goals:**
- Implement masking functions for common PII types
- Implement deterministic tokenization using HMAC/hashing
- Design audit logs that capture metadata (NO sensitive values)
- Apply "least data exposure" principle
- Use Agent Mode to build modular, testable data protection code

**Modules Built:** config.py, masking.py, tokenization.py, redaction.py, audit.py, cli.py

**Verification:** pytest + CLI runs (MASK/TOKENIZE/REDACT modes) + audit log inspection (no PII present)

---

## Prompts

All copy-paste ready prompts for Day 2 exercises and labs are available in:

**[Day 2 Prompts Document](prompts/day2_prompts.md)**

This includes:
- Session 2.1 micro-exercise prompts
- Session 2.2 refactoring exercise prompts
- Lab 3 prompts (6 tasks: schemas, rules, triage, I/O, pipeline, CLI)
- Lab 4 prompts (6 tasks: config, masking, tokenization, redaction, audit, CLI)
- General-purpose prompts (explain code, generate tests, add type hints, review security)

---

## How to Run Day 2 (Quickstart)

### 1. Setup

```bash
# Navigate to workspace
cd d:\All_Projects\vscode-github-copilot-quick-bootcamp

# Verify Python and pytest
python --version  # Should be 3.10+
pytest --version

# Verify GitHub Copilot CLI
gh copilot --version
```

### 2. Session 2.1 (Agent Planning)

- Read [Session 2.1 document](session2_1_agent_planning_and_task_breakdown.md)
- Complete micro-exercise: decompose a feature
- Practice writing agent prompts with stop points

### 3. Session 2.2 (Multi-File Refactor)

- Read [Session 2.2 document](session2_2_multi_file_refactor_and_test_loops.md)
- Follow live demo: refactor Day 1 code
- Hands-on exercise: refactor a small module from Day 1

### 4. Lab 3 (AML Alert Triage Pipeline)

```bash
# Create branch
git checkout -b day2-lab3

# Follow lab instructions
open day2_agent_workflows/labs/lab3_aml_alert_triage_pipeline.md

# Copy prompts from prompts document
open day2_agent_workflows/prompts/day2_prompts.md

# Paste prompts into Copilot Agent Mode
# Execute tasks 1-7 with stop points and verification

# Verify final implementation
pytest tests/day2/ -v
python -m src.day2.aml_triage.cli --input src/samples/sample_transactions_day2.csv --outdir out/day2/lab3
ls out/day2/lab3/
```

### 5. Lab 4 (PII Masking/Tokenization)

```bash
# Create branch
git checkout -b day2-lab4

# Follow lab instructions
open day2_agent_workflows/labs/lab4_pii_masking_and_audit_logging.md

# Use prompts from prompts document
# Execute tasks 1-6

# Verify final implementation
pytest tests/day2/ -k pii -v
python -m src.day2.pii_protection.cli --mode MASK --input src/samples/sample_customer_pii.csv --output out/day2/lab4/masked.csv
cat out/day2/lab4/audit_log.jsonl
```

### 6. Reflexion Retro (17:15–17:45)

Review with your cohort:
- What surprised you about using Agent Mode?
- Where did the agent make assumptions you had to correct?
- What stop points were most valuable?
- What evidence artifacts would auditors want to see?
- What would you change for production use?

---

## Verification Checklist

After completing Day 2, you should have:

✅ **Lab 3 complete:**
- [ ] AML triage pipeline working end-to-end
- [ ] All tests pass: `pytest tests/day2/test_aml*.py -v`
- [ ] CLI produces expected outputs
- [ ] Outputs are deterministic (run twice, diff shows no changes)
- [ ] README.md documents architecture and usage

✅ **Lab 4 complete:**
- [ ] PII protection library working end-to-end
- [ ] All tests pass: `pytest tests/day2/test_*masking*.py tests/day2/test_*tokenization*.py -v`
- [ ] CLI works for MASK, TOKENIZE, and REDACT modes
- [ ] Audit log contains NO raw PII (verified manually)
- [ ] README.md documents modes, security considerations, compliance notes

✅ **Git commits:**
- [ ] Multiple commits showing incremental progress (not one giant commit)
- [ ] Commit messages describe what changed and why
- [ ] Each commit represents a working state (tests pass)

✅ **Understanding:**
- [ ] Can explain Epic → Story → Task decomposition
- [ ] Can write agent prompts with scope, constraints, verification, stop points
- [ ] Can run test loops after code changes
- [ ] Can use GitHub Copilot CLI for safe command suggestions
- [ ] Can identify what evidence auditors need (reason codes, audit logs, determinism)

---

## Key Takeaways

1. **Decompose before implementing.** Epic → Stories → Tasks → Acceptance Criteria → Prompts.
2. **Agent Mode is a contractor.** Provide spec, materials, inspection checklist, staged approvals.
3. **Stop points maintain control.** Review after plan, scaffolding, tests, integration, docs.
4. **Tests are your safety net.** Run after EVERY change to catch regressions immediately.
5. **Git enables experimentation.** Commit after each verified step so you can rollback if needed.
6. **Audit-friendly = deterministic + traceable.** Same input → same output. Log operations, not PII.
7. **Copilot CLI accelerates learning.** Use `gh copilot explain` before running unfamiliar commands.

---

## Next Steps

### Continue Learning

- **Day 3 (optional):** MCP (Model Context Protocol) integration for enterprise workflows
- **Practice:** Apply Day 2 patterns to your own projects (refactor a module, implement a small feature)
- **Explore:** GitHub Copilot Extensions marketplace for domain-specific tools

### Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [GitHub Copilot CLI Documentation](https://cli.github.com/manual/gh_copilot)
- [Pydantic Documentation](https://docs.pydantic.dev/) (for data validation)
- [pytest Documentation](https://docs.pytest.org/) (for testing)

---

## Troubleshooting

### Common Issues

**Issue:** Agent Mode generates code that doesn't match requirements  
**Solution:** Make your prompt more specific. Include explicit constraints, examples, and a STOP point for review.

**Issue:** Tests fail after agent makes changes  
**Solution:** Review git diff. Did behavior change unintentionally? Revert and re-prompt with clearer constraints.

**Issue:** Agent over-implements (adds features you didn't ask for)  
**Solution:** Add explicit "DO NOT" constraints. Use STOP points more frequently.

**Issue:** Copilot CLI suggests a destructive command  
**Solution:** Always use `gh copilot explain` first. If you don't understand it, don't run it.

**Issue:** Outputs aren't deterministic (different each run)  
**Solution:** Check for randomness, timestamps, or unsorted collections. Sort outputs explicitly. Use fixed seeds if random generation is needed (though avoid in banking).

---

## Feedback

We welcome feedback on Day 2 training materials!

- What worked well?
- What was confusing?
- What would you add or change?
- How would you rate the pacing?

Share feedback with your trainer or via [repository issues](../../README.md).

---

**Let's build banking-grade systems with agentic workflows! 🚀**
