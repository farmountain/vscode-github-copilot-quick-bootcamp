# Session 2.1 — Agent Planning & Task Breakdown

**Duration:** 09:00–10:30 (90 minutes)  
**Format:** Presentation + live demos + micro-exercises  
**Tools:** VS Code + GitHub Copilot Chat + Agent Mode

---

## Learning Objectives

By the end of this session, learners will be able to:

1. **Decompose** a large engineering epic into agent-friendly tasks with clear acceptance criteria
2. **Write prompts** that constrain the agent's scope and provide verification commands
3. **Use stop points** to control Agent Mode execution (plan → implement → verify → document)
4. **Apply** Paul–Elder critical thinking to prompt design (purpose, assumptions, implications)
5. **Identify** when to invoke Agent Mode vs. when to use Copilot Chat inline

---

## Agenda

| Time | Activity | Duration |
|------|----------|----------|
| 09:00–09:15 | Why big tasks fail + the decomposition principle | 15 min |
| 09:15–09:35 | Feynman explanation: Agent Mode as a contractor | 20 min |
| 09:35–10:00 | The Epic → Task decomposition recipe (live demo) | 25 min |
| 10:00–10:20 | Micro-exercise: decompose a small feature | 20 min |
| 10:20–10:30 | Reflexion + Q&A | 10 min |

---

## Why Big Tasks Fail

### First Principles

**Agent Mode is powerful but not omniscient.** Without clear constraints, it will:

- Make unjustified assumptions about requirements
- Create code that compiles but doesn't meet business logic
- Skip verification steps
- Produce non-deterministic or untestable outputs

**The solution:** Treat the agent like a **remote contractor**. Provide:

1. **Scope** — what to build, what NOT to build
2. **Interfaces** — expected inputs, outputs, data schemas
3. **Done criteria** — what "complete" means (tests, docs, outputs)
4. **Verification commands** — how you'll inspect their work

### Inversion Thinking: What NOT to Do

❌ **Bad prompt:**
```
"Implement an AML alert system"
```

**What goes wrong:**
- Agent invents features you didn't ask for
- No tests, or tests that don't reflect real requirements
- Output format unknown
- Can't reproduce results

✅ **Good prompt:**
```
"Implement an AML alert triage system that:
- Reads synthetic transactions from /src/samples/sample_transactions.csv
- Applies 3 deterministic rules: HIGH_VELOCITY, ROUND_AMOUNT, HIGH_AMOUNT
- Outputs alerts as JSON to /out/day2/aml_alerts.json
- Includes pytest tests that verify each rule independently
- Provides a CLI command: python -m src.day2.aml_triage.cli --input ... --outdir ...
- All outputs must be deterministic (stable sort order)
- STOP after creating file structure and schemas for review"
```

**What's better:**
- Clear inputs and outputs
- Explicit rules (no invention)
- Testability built-in
- Stop point for review

---

## Feynman Explanation: Agent Mode as a Contractor

### The Mental Model

Imagine you hire a contractor to build a small shed. You don't hand them a hammer and say "build something nice." You provide:

- **Blueprints** (the spec)
- **Materials list** (dependencies, inputs)
- **Building codes** (constraints, rules)
- **Inspection checklist** (tests, acceptance criteria)
- **Staged approvals** (foundation → framing → roof → finished)

**Agent Mode works the same way.**

- **Blueprints** = your prompt with scope and interfaces
- **Materials** = input files, sample data, existing code to reference
- **Building codes** = constraints (no MCP, synthetic data only, deterministic)
- **Inspection checklist** = tests, verification commands, expected outputs
- **Staged approvals** = stop points (after planning, after scaffolding, after tests pass)

### Contractor Communication Pattern

**You:** "Here's what I need built, here's the spec, here are the materials, here's how I'll inspect it. Start with the foundation and stop for my approval."

**Agent:** *Creates file structure and schemas*

**You:** *Reviews structure* "Good, proceed with implementing the rules module."

**Agent:** *Implements rules.py with tests*

**You:** *Runs tests* "Tests pass, now integrate into the pipeline."

This **iterative delivery** prevents:
- Over-implementation
- Undetected bugs compounding
- Wasted work if requirements change

---

## The Epic → Task Decomposition Recipe

### Step-by-Step Process

#### 1. Start with the Epic (Business Goal)

**Example Epic:**
> "As a compliance analyst, I need an automated alert triage pipeline so that high-risk transactions are prioritized for review."

#### 2. Extract User Stories

Break the epic into user-facing capabilities:

**Story 1:** Generate alerts from transaction rules  
**Story 2:** Assign triage priority based on risk scoring  
**Story 3:** Output a triage queue for analyst review  
**Story 4:** Provide audit evidence of rule execution  

#### 3. Break Stories into Technical Tasks

For **Story 1** (Generate alerts from transaction rules):

**Tasks:**
- T1.1: Define Transaction and Alert schemas (Pydantic models)
- T1.2: Implement rule functions (HIGH_VELOCITY, ROUND_AMOUNT, HIGH_AMOUNT)
- T1.3: Write unit tests for each rule
- T1.4: Create rule runner that applies all rules to a transaction stream
- T1.5: Add deterministic reason code generation

#### 4. Add Acceptance Criteria to Each Task

**Task T1.2: Implement rule functions**

**Acceptance Criteria:**
- ✅ HIGH_VELOCITY rule triggers when 3+ transactions occur for same account_id within 60 seconds
- ✅ ROUND_AMOUNT rule triggers when amount is divisible by 100
- ✅ HIGH_AMOUNT rule triggers when amount > 10000 (configurable threshold)
- ✅ Each rule returns a ReasonCode enum + explanation string
- ✅ Rules are pure functions (no side effects, testable in isolation)

**Verification:**
```bash
pytest tests/day2/test_aml_rules.py -v
```

#### 5. Write the Agent Prompt for ONE Task

**Prompt for T1.2:**
```text
You are a GitHub Copilot coding agent.

Implement AML alert rule functions in /src/day2/aml_triage/rules.py

Requirements:
- Define ReasonCode enum (HIGH_VELOCITY, ROUND_AMOUNT, HIGH_AMOUNT)
- Implement 3 functions:
  - check_high_velocity(transactions: List[Transaction], account_id: str, lookback_seconds: int = 60) -> Optional[ReasonCode]
  - check_round_amount(transaction: Transaction) -> Optional[ReasonCode]
  - check_high_amount(transaction: Transaction, threshold: float = 10000) -> Optional[ReasonCode]
- Each function returns ReasonCode if triggered, None otherwise
- Use Pydantic Transaction model from schemas.py (assume it exists with fields: id, account_id, amount, timestamp)

Also create /tests/day2/test_aml_rules.py with pytest tests:
- Test HIGH_VELOCITY with 4 transactions in 30s → triggers
- Test HIGH_VELOCITY with 2 transactions in 30s → does not trigger
- Test ROUND_AMOUNT with 5000.00 → triggers
- Test ROUND_AMOUNT with 4999.99 → does not trigger
- Test HIGH_AMOUNT with 15000 → triggers
- Test HIGH_AMOUNT with 9999 → does not trigger

Verification:
pytest tests/day2/test_aml_rules.py -v

Constraints:
- No MCP
- Deterministic (no randomness)
- Type hints on all functions
- Docstrings explaining each rule's logic

STOP after completing rules.py and test_aml_rules.py. Do not implement other modules yet.
```

---

## Paul–Elder Critical Thinking Framework Applied to Prompts

Every agent prompt should address these elements:

### 1. Purpose
**Why does this task exist?**

*Example:* "This rule detects potential structuring behavior (breaking large transactions into smaller amounts to avoid reporting thresholds)."

### 2. Question
**What specific question are we answering?**

*Example:* "Which transactions exhibit round-amount patterns indicative of suspicious activity?"

### 3. Information
**What data/context does the agent need?**

*Example:*
- Transaction schema (fields, types)
- Sample input file path
- Expected output format
- Existing code to reference or integrate with

### 4. Assumptions
**What are we assuming (that might not hold)?**

*Example:*
- Transactions are pre-sorted by timestamp
- No missing data (all fields present)
- Synthetic data only (no real customer info)
- No ML required (rules-based only)

**Make assumptions explicit** in the prompt so the agent doesn't have to guess.

### 5. Implications
**What are the consequences if this fails?**

*Example:*
- False negatives → miss real suspicious activity
- False positives → waste analyst time
- Non-deterministic output → can't reproduce for audit
- Over-logging PII → compliance violation

### 6. Point of View
**Whose perspective matters?**

*Example:*
- Developer (maintainability, testability)
- Analyst (usable output format, clear reason codes)
- Auditor (traceability, evidence retention)
- Compliance (no PII leakage, deterministic)

---

## Stop Points: Controlling Agent Mode Execution

### The Stop Points Pattern

DO NOT let Agent Mode run uncontrolled to "completion." Use explicit stop points:

#### Stop Point 1: After Planning
**Agent outputs:** File structure, module responsibilities, interface definitions  
**You review:** Does this match requirements? Any missing pieces?

#### Stop Point 2: After Scaffolding
**Agent outputs:** Empty/stub files with schemas and function signatures  
**You review:** Are interfaces correct? Do schemas match sample data?

#### Stop Point 3: After Core Implementation
**Agent outputs:** Implemented functions with tests  
**You review:** Run tests. Do they pass? Is logic correct?

#### Stop Point 4: After Integration
**Agent outputs:** End-to-end pipeline working with sample data  
**You review:** Run full pipeline. Check outputs. Deterministic? Auditable?

#### Stop Point 5: After Documentation
**Agent outputs:** README, runbook, verification commands  
**You review:** Can a new developer run this? Are all commands documented?

### How to Add Stop Points to Prompts

Add explicit instructions:

```text
STOP after creating file structure. Wait for approval before implementing.
```

```text
STOP after writing tests. Do not implement the integration module yet.
```

```text
Create schemas.py and rules.py, then STOP. I will review before you continue.
```

---

## Micro-Exercise 1: Decompose a Small Feature (20 minutes)

### Scenario

**Epic:** "As a risk analyst, I need a velocity checker that flags accounts with unusual transaction frequency."

### Your Task

1. **Write 2–3 user stories** for this epic
2. **Break ONE story into 3–4 technical tasks**
3. **Write acceptance criteria** for ONE task
4. **Draft an agent prompt** for that task (include scope, verification, stop point)

### Use This Template

```text
Epic: [business goal]

Story 1: [user-facing capability]
Story 2: [another capability]

Task 1.1: [technical task]
  Acceptance Criteria:
  - ✅ [criterion 1]
  - ✅ [criterion 2]
  
  Verification: [command to run]

Agent Prompt for Task 1.1:
---
[Your prompt here with scope, constraints, verification, STOP instruction]
---
```

### Paste Your Work into Copilot Chat

After drafting, paste into Copilot Chat and ask:
```
Review my task decomposition and agent prompt. What's missing? What assumptions did I leave implicit?
```

---

## Reflexion Checklist (End of Session)

Ask yourself:

✅ **Did I provide clear scope?** (What to build, what NOT to build)  
✅ **Did I specify interfaces?** (Input/output formats, schemas)  
✅ **Did I define "done"?** (Tests, verification commands)  
✅ **Did I add stop points?** (Prevent runaway agent work)  
✅ **Did I make assumptions explicit?** (No guessing)  
✅ **Did I consider multiple perspectives?** (Dev, analyst, auditor)

**Red flags:**
- Prompt longer than 30 lines → probably too complex, break it down
- No verification command → how will you know it works?
- No stop point → agent might over-implement
- No constraints → agent will invent features

---

## Key Takeaways

1. **Big tasks fail unless decomposed.** Use Epic → Stories → Tasks → Acceptance Criteria.
2. **Treat Agent Mode like a contractor:** provide spec, materials, inspection checklist, staged approvals.
3. **Use stop points** to maintain control and review work incrementally.
4. **Make assumptions explicit** (use Paul–Elder framework).
5. **Always include verification commands** in your prompts (tests, CLI runs, expected outputs).

---

## Next Steps

- **Session 2.2** will show how to execute multi-file refactors with test loops using the decomposition techniques learned today.
- **Lab 3** will give you hands-on practice applying this framework to build an AML Alert Triage Pipeline.

---

**Questions?** Open Copilot Chat and ask:
```
What are best practices for writing agent prompts with clear stop points?
```
