# Session 2.2 — Multi-File Refactor + Test Loops

**Duration:** 10:45–12:15 (90 minutes)  
**Format:** Live demo + hands-on exercises  
**Tools:** VS Code + GitHub Copilot Agent Mode + pytest

---

## Learning Objectives

By the end of this session, learners will be able to:

1. **Execute** a multi-file refactor using Agent Mode with incremental verification
2. **Run test loops** after each change to prevent regression
3. **Use git** as a safety net (commit after each verified step)
4. **Identify** when a refactor preserves behavior vs. changes it
5. **Apply** the "red-green-refactor" pattern with Copilot as the implementation engine

---

## Agenda

| Time | Activity | Duration |
|------|----------|----------|
| 10:45–11:00 | Why multi-file changes break + the safety net pattern | 15 min |
| 11:00–11:25 | Live demo: refactor Day 1 code with test verification | 25 min |
| 11:25–11:50 | Hands-on: refactor a small module with Agent Mode | 25 min |
| 11:50–12:10 | Advanced: Extract shared logic across files | 20 min |
| 12:10–12:15 | Reflexion + Q&A | 5 min |

---

## Why Multi-File Changes Break

### First Principles

When modifying multiple files simultaneously:

- **Dependency drift:** File A expects File B's old interface
- **Test coverage gaps:** Some paths aren't tested, breakage goes unnoticed
- **Merge conflicts:** If working in a team, large changes conflict
- **Debugging difficulty:** "Which change broke it?" becomes hard to answer

**The solution:** **Incremental refactor with test verification at each step.**

### The Safety Net Pattern

```
1. Commit current working state (git)
2. Make ONE focused change
3. Run tests
4. If tests pass → commit, proceed
5. If tests fail → revert or fix, then commit
6. Repeat
```

This ensures:
- Every commit is a working state
- Regressions are caught immediately
- Easy rollback if needed
- Clear history of what changed when

---

## Feynman Explanation: Refactoring as Rewiring a House

Imagine rewiring a house while people are still living in it. You can't rip out all the wiring at once. Instead:

1. **Map the current wiring** (understand the code)
2. **Plan the new layout** (design the refactor)
3. **Rewire one room at a time** (change one module)
4. **Test each room** (run tests)
5. **Keep the power on** (preserve behavior)

**Agent Mode is your electrician.** But YOU are the project manager who:
- Defines the rewiring plan
- Inspects each room after work
- Turns on the lights to verify (runs tests)
- Signs off before moving to the next room

---

## The Refactoring Recipe with Agent Mode

### Step 1: Establish Baseline

Before any refactor:

```bash
# Run all tests to ensure starting point is green
pytest -v

# Commit current state
git add .
git commit -m "Baseline before refactor"
```

### Step 2: Write the Refactor Plan

Document what will change and what will NOT change.

**Example plan:**
```
Refactor goal: Extract ReasonCode constants into shared module

Changes:
- Create /src/day2/aml_triage/constants.py with ReasonCode enum
- Update rules.py to import ReasonCode from constants
- Update triage.py to import ReasonCode from constants

Preserved behavior:
- All existing tests pass unchanged
- Alert outputs remain identical
- No new dependencies introduced

Verification:
pytest tests/day2/ -v
python -m src.day2.aml_triage.cli --input ... --outdir out/test
diff out/test/aml_alerts.json out/baseline/aml_alerts.json
```

### Step 3: Agent Prompt with Explicit Constraints

```text
You are a GitHub Copilot coding agent.

Refactor the AML triage module to extract ReasonCode into a shared constants module.

Current state:
- ReasonCode is defined in rules.py
- rules.py and triage.py both use ReasonCode

Refactor steps:
1. Create /src/day2/aml_triage/constants.py
2. Move ReasonCode enum to constants.py
3. Update imports in rules.py
4. Update imports in triage.py
5. STOP after each file change for test verification

Constraints:
- PRESERVE all existing behavior
- Do NOT change function signatures
- Do NOT add new logic
- All existing tests must pass unchanged

Verification after EACH step:
pytest tests/day2/test_aml_rules.py -v
pytest tests/day2/test_triage_scoring.py -v

Start with step 1: create constants.py. STOP for verification.
```

### Step 4: Execute in Small Increments

**Agent:** *Creates constants.py*

**You:**
```bash
pytest tests/day2/ -v  # Should still pass (no changes to logic yet)
git add src/day2/aml_triage/constants.py
git commit -m "Add constants.py with ReasonCode enum"
```

**Agent:** *Updates rules.py imports*

**You:**
```bash
pytest tests/day2/test_aml_rules.py -v  # Must pass
git add src/day2/aml_triage/rules.py
git commit -m "Update rules.py to import from constants"
```

**Agent:** *Updates triage.py imports*

**You:**
```bash
pytest tests/day2/ -v  # All tests must pass
git add src/day2/aml_triage/triage.py
git commit -m "Update triage.py to import from constants"
```

### Step 5: Final Verification

```bash
# Run full test suite
pytest -v

# Run end-to-end pipeline and compare outputs
python -m src.day2.aml_triage.cli --input src/samples/sample_transactions.csv --outdir out/after_refactor

# Compare with baseline (should be identical)
diff out/baseline/aml_alerts.json out/after_refactor/aml_alerts.json
```

If outputs match → refactor successful!

---

## Test Loop Pattern

### The Red-Green-Refactor Cycle

**Traditional TDD:**
1. **Red:** Write failing test
2. **Green:** Write minimal code to pass
3. **Refactor:** Improve code while keeping tests green

**With Agent Mode:**
1. **Baseline Green:** Ensure all tests pass
2. **Refactor:** Agent makes changes
3. **Verify Green:** Run tests immediately
4. **Commit Green:** Save verified state
5. **Repeat**

### Test Loop Commands

After EVERY agent change:

```bash
# Quick smoke test (fast)
pytest tests/day2/test_aml_rules.py -q

# Full suite (thorough)
pytest tests/day2/ -v

# With coverage (find untested code)
pytest tests/day2/ --cov=src.day2.aml_triage --cov-report=term-missing
```

### When Tests Fail

**DO NOT ask agent to "fix tests."** First, determine:

1. **Is the test wrong?** (Does it test behavior that shouldn't be preserved?)
2. **Is the code wrong?** (Did refactor accidentally change behavior?)

**Debugging process:**
```bash
# Run single failing test with verbose output
pytest tests/day2/test_aml_rules.py::test_high_velocity -vv

# Check what changed
git diff

# If code is wrong: revert and re-prompt agent with clearer constraints
git checkout -- src/day2/aml_triage/rules.py

# If test is wrong: update test to match new expected behavior (rare for refactors)
```

---

## Live Demo: Refactor Day 1 Code

### Scenario

We'll refactor Day 1's data quality rules engine to improve maintainability.

**Current issues:**
- Rule logic mixed with I/O logic
- Hard to test rules in isolation
- No shared constants for severity levels

**Refactor goals:**
1. Extract rule functions into separate module
2. Create constants.py for severity levels
3. Improve type hints and docstrings

### Demo Steps

#### Step 1: Establish Baseline
```bash
cd day1_foundations/labs
pytest tests/ -v  # Ensure green
git status  # Check clean state
```

#### Step 2: Write Refactor Prompt

```text
Refactor /day1_foundations/labs/solution_lab1/rules_engine.py:

1. Create constants.py with Severity enum (HIGH, MEDIUM, LOW)
2. Extract rule functions to rules.py (check_completeness, check_format, check_range)
3. Keep rules_engine.py as orchestrator (load data, apply rules, write report)
4. Add type hints and docstrings

Constraints:
- Preserve all behavior
- All tests pass unchanged
- Deterministic outputs

STOP after creating constants.py. Wait for verification.
```

#### Step 3: Execute with Agent Mode

*Agent creates constants.py*

```bash
pytest tests/test_rules.py -v  # Should pass
git add constants.py && git commit -m "Add Severity constants"
```

*Agent creates rules.py*

```bash
pytest tests/test_rules.py -v  # Should pass
git add rules.py && git commit -m "Extract rule functions"
```

*Agent updates rules_engine.py*

```bash
pytest tests/ -v  # All tests pass
git add rules_engine.py && git commit -m "Update orchestrator to use extracted rules"
```

#### Step 4: Verify Behavior Preserved

```bash
# Run end-to-end
python rules_engine.py --input sample_data.csv --output out/report.json

# Compare with baseline
diff out/baseline_report.json out/report.json
# Should show no differences
```

---

## Hands-On Exercise: Refactor a Small Module (25 minutes)

### Your Task

Refactor the **risk scoring service** from Day 1 Lab 2.

**Current state:**
- All logic in one file: `risk_scorer.py`
- Scoring rules hard-coded in main function

**Refactor goals:**
1. Extract scoring rules to `scoring_rules.py`
2. Create `models.py` with Pydantic schemas for Customer and RiskScore
3. Add configuration in `config.py` (thresholds, weights)

### Instructions

1. **Establish baseline:**
   ```bash
   cd day1_foundations/labs/solution_lab2
   pytest tests/ -v
   git add . && git commit -m "Baseline before refactor"
   ```

2. **Write your refactor plan** (on paper or in a comment)

3. **Prompt Agent Mode:**
   ```text
   Refactor /day1_foundations/labs/solution_lab2/risk_scorer.py into 3 modules:
   - models.py (Pydantic schemas)
   - scoring_rules.py (rule functions)
   - config.py (thresholds, weights)
   
   Preserve all behavior. Tests must pass unchanged.
   
   STOP after creating models.py. I will verify.
   ```

4. **Execute incrementally:**
   - After each file: run `pytest tests/ -v`
   - After each successful test: `git commit`

5. **Final verification:**
   ```bash
   pytest tests/ -v
   python risk_scorer.py --input sample_customers.csv --output out/scores.json
   diff out/baseline_scores.json out/scores.json
   ```

### Success Criteria

✅ All tests pass  
✅ Output file identical to baseline  
✅ At least 3 git commits (one per module)  
✅ Code more modular and testable

---

## Advanced: Extract Shared Logic Across Files

### Scenario

Multiple modules duplicate the same validation logic.

**Example:** Both `rules.py` and `triage.py` validate transaction timestamps.

**Current (duplicated):**
```python
# In rules.py
def validate_timestamp(ts: str) -> datetime:
    return datetime.fromisoformat(ts)

# In triage.py
def validate_timestamp(ts: str) -> datetime:
    return datetime.fromisoformat(ts)
```

**Goal:** Extract to `utils.py` and reuse.

### Agent Prompt for Cross-File Extraction

```text
Extract duplicate timestamp validation logic to /src/day2/aml_triage/utils.py

Steps:
1. Create utils.py with validate_timestamp function
2. Update rules.py to import from utils
3. Update triage.py to import from utils
4. Remove duplicate definitions

Verification after EACH step:
pytest tests/day2/ -v

Constraints:
- Preserve all behavior
- Add type hints
- Add docstring explaining timezone handling

Start with step 1. STOP for verification.
```

### Verification Strategy

```bash
# After utils.py created
pytest tests/day2/ -v

# After rules.py updated
pytest tests/day2/test_aml_rules.py -v
git add src/day2/aml_triage/rules.py && git commit -m "Use utils.validate_timestamp in rules"

# After triage.py updated
pytest tests/day2/ -v
git add src/day2/aml_triage/triage.py && git commit -m "Use utils.validate_timestamp in triage"
```

---

## Common Refactoring Patterns

### Pattern 1: Extract Function
**When:** Logic block is repeated or too complex  
**How:** Create new function, replace call sites  
**Verify:** Tests pass, outputs identical

### Pattern 2: Extract Module
**When:** File > 300 lines or multiple responsibilities  
**How:** Split into logical modules (models, rules, orchestrator)  
**Verify:** Import paths updated, tests pass

### Pattern 3: Introduce Constant/Enum
**When:** Magic numbers/strings appear multiple times  
**How:** Define in constants.py, update references  
**Verify:** Behavior unchanged, more maintainable

### Pattern 4: Improve Type Hints
**When:** Functions lack type annotations  
**How:** Add type hints incrementally  
**Verify:** Run `mypy` (if configured), tests pass

---

## Inversion: What NOT to Refactor

❌ **Don't refactor without tests.** Write tests first if needed.  
❌ **Don't change behavior during refactor.** Separate refactor commits from feature commits.  
❌ **Don't refactor everything at once.** Small steps, verify each.  
❌ **Don't skip verification.** "It looks right" ≠ "It is right."

---

## Reflexion Checklist

After each refactor session, ask:

✅ **Did I establish a baseline?** (Tests green, outputs captured)  
✅ **Did I commit after each verified step?** (Not one giant commit)  
✅ **Did I preserve behavior?** (Tests pass, outputs match)  
✅ **Did I improve code quality?** (More modular, readable, maintainable)  
✅ **Can I explain what changed and why?** (Clear commit messages)

**Red flags:**
- Tests failing after refactor → behavior changed (bad)
- No git commits → can't rollback if needed
- Agent made changes you didn't understand → review carefully

---

## Key Takeaways

1. **Refactor in small, verified increments.** One module at a time.
2. **Run tests after EVERY change.** Catch regressions immediately.
3. **Use git as a safety net.** Commit after each green test run.
4. **Preserve behavior during refactor.** Separate refactor from new features.
5. **Agent Mode accelerates refactoring** but YOU control the pace and verify each step.

---

## Next Steps

- **Session 2.3** will show how to automate these verification steps using GitHub Copilot CLI.
- **Lab 3** will require you to apply multi-file implementation patterns with test loops.

---

**Practice prompt:**
```text
Refactor my current file to extract magic numbers into constants. 
Preserve all behavior. Provide verification commands. STOP after constants file created.
```
