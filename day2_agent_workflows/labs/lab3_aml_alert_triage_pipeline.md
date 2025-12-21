# Lab 3 — AML Alert Triage Pipeline

**Duration:** 13:30–15:30 (2 hours)  
**Difficulty:** Intermediate  
**Prerequisites:** Day 1 labs complete, Day 2 Session 2.1 and 2.2 complete

---

## Business Context

You work in the **Financial Crimes Prevention** team at a bank. The compliance team receives thousands of transaction alerts daily from various monitoring systems. Many alerts are false positives, overwhelming analysts.

**Your mission:** Build an automated **AML Alert Triage Pipeline** that:
1. Reads synthetic transaction data
2. Applies deterministic AML-like heuristic rules
3. Scores alerts by risk priority
4. Generates a triage queue for analyst review
5. Produces audit evidence showing which rules triggered and why

**Why this matters:**
- Analysts can focus on high-priority alerts (P1) first
- Deterministic rules are explainable for regulatory review
- Audit trail shows decision provenance
- System can be tested and validated before production use

---

## Learning Objectives

By completing this lab, you will:

1. **Use Agent Mode** to implement a multi-module Python pipeline with clear stop points
2. **Write prompts** that constrain scope, define interfaces, and specify verification
3. **Implement deterministic rules** that produce reproducible results for audit
4. **Run test loops** after each implementation step
5. **Generate audit-friendly outputs** (alerts with reason codes, triage queue, summary reports)

---

## Architecture Overview

```
Input: sample_transactions.csv
  ↓
[Feature Extraction] → derives velocity counts, round-amount flags, etc.
  ↓
[Rule Engine] → applies AML rules, generates reason codes
  ↓
[Triage Scorer] → computes priority scores (P1/P2/P3)
  ↓
[Output Writers] → JSON alerts, CSV queue, summary stats
```

**Modules you'll create:**
- `schemas.py` — Pydantic models (Transaction, Alert, TriageDecision)
- `rules.py` — AML heuristic rules returning reason codes
- `features.py` — Feature extraction (velocity, patterns)
- `triage.py` — Priority scoring logic
- `pipeline.py` — Orchestration
- `io.py` — Input/output handling
- `cli.py` — CLI entrypoint

---

## Setup

### 1. Create Project Structure

```bash
cd d:\All_Projects\vscode-github-copilot-quick-bootcamp

# Create directories
mkdir -p src/day2/aml_triage
mkdir -p tests/day2
mkdir -p out/day2/lab3
mkdir -p src/samples
```

### 2. Establish Baseline (Git)

```bash
git status
# If clean, create a new branch:
git checkout -b day2-lab3

# Or commit existing work:
git add .
git commit -m "Baseline before Lab 3"
```

### 3. Generate Sample Data (if not exists)

If `src/samples/sample_transactions.csv` doesn't exist from Day 1, create it:

**Sample transactions CSV format:**
```csv
transaction_id,account_id,timestamp,amount,transaction_type,beneficiary_id,currency
TX001,ACC001,2024-01-15T10:00:00Z,5000.00,DEBIT,BEN123,USD
TX002,ACC001,2024-01-15T10:00:30Z,5000.00,DEBIT,BEN124,USD
TX003,ACC001,2024-01-15T10:01:00Z,5000.00,DEBIT,BEN125,USD
TX004,ACC002,2024-01-15T10:05:00Z,15000.00,CREDIT,BEN126,USD
TX005,ACC003,2024-01-15T10:10:00Z,100.00,DEBIT,BEN127,USD
TX006,ACC001,2024-01-15T10:15:00Z,9999.99,CREDIT,BEN128,USD
TX007,ACC004,2024-01-15T10:20:00Z,3000.00,DEBIT,BEN129,USD
TX008,ACC004,2024-01-15T10:20:15Z,3000.00,CREDIT,BEN129,USD
```

**Create the file manually or use Copilot:**
```text
Create /src/samples/sample_transactions_day2.csv with 20 synthetic bank transactions including:
- Fields: transaction_id, account_id, timestamp, amount, transaction_type, beneficiary_id, currency
- Include examples that trigger HIGH_VELOCITY (3+ txns in 60s for same account)
- Include ROUND_AMOUNT examples (5000.00, 10000.00)
- Include HIGH_AMOUNT examples (>10000)
- Include RAPID_REVERSAL pattern (debit followed by credit to same beneficiary)
- All timestamps in ISO format
- Use deterministic data (no randomness)
```

---

## Task Breakdown

### Task 1: Define Schemas (15 minutes)

**Goal:** Create Pydantic models for type safety and validation.

**Agent Prompt:**
```text
You are a GitHub Copilot coding agent.

Create /src/day2/aml_triage/schemas.py with Pydantic models for the AML triage pipeline.

Models needed:
1. Transaction
   - transaction_id: str
   - account_id: str
   - timestamp: datetime (parsed from ISO string)
   - amount: Decimal (for precision)
   - transaction_type: Literal["DEBIT", "CREDIT"]
   - beneficiary_id: str
   - currency: str (default "USD")

2. ReasonCode (Enum)
   - HIGH_VELOCITY
   - ROUND_AMOUNT
   - HIGH_AMOUNT
   - RAPID_REVERSAL
   - NEW_BENEFICIARY

3. Alert
   - alert_id: str (generated from transaction_id)
   - transaction: Transaction
   - reason_codes: List[ReasonCode]
   - explanation: str (human-readable reason)
   - timestamp_detected: datetime

4. TriageDecision
   - alert: Alert
   - priority: Literal["P1", "P2", "P3"]
   - triage_score: float
   - assigned_queue: str (e.g., "HIGH_RISK", "MEDIUM_RISK", "LOW_RISK")

Constraints:
- Use Pydantic v2 syntax if available, else v1
- Add example values in docstrings
- Use Decimal for monetary amounts
- All timestamps as datetime objects

Verification:
- Create /tests/day2/test_schemas.py with basic validation tests
- Test: valid transaction parses correctly
- Test: invalid transaction raises ValidationError

Run: pytest tests/day2/test_schemas.py -v

STOP after creating schemas.py and test_schemas.py. Wait for verification.
```

**Your actions:**
```bash
# After agent creates files:
pytest tests/day2/test_schemas.py -v

# If tests pass:
git add src/day2/aml_triage/schemas.py tests/day2/test_schemas.py
git commit -m "Add Pydantic schemas for AML triage"
```

---

### Task 2: Implement Rule Functions (30 minutes)

**Goal:** Create deterministic rule functions that detect suspicious patterns.

**Agent Prompt:**
```text
You are a GitHub Copilot coding agent.

Create /src/day2/aml_triage/rules.py with AML heuristic rule functions.

Import schemas from ./schemas (Transaction, ReasonCode)

Implement these rule functions:

1. check_high_velocity(transactions: List[Transaction], target_account: str, window_seconds: int = 60) -> Optional[ReasonCode]
   - Returns HIGH_VELOCITY if 3+ transactions for target_account occur within window_seconds
   - Transactions must be sorted by timestamp
   - Return None if rule doesn't trigger

2. check_round_amount(transaction: Transaction) -> Optional[ReasonCode]
   - Returns ROUND_AMOUNT if amount is divisible by 100 (e.g., 5000.00, 10000.00)
   - Return None otherwise

3. check_high_amount(transaction: Transaction, threshold: Decimal = Decimal("10000")) -> Optional[ReasonCode]
   - Returns HIGH_AMOUNT if transaction amount >= threshold
   - Return None otherwise

4. check_rapid_reversal(transactions: List[Transaction], target_transaction: Transaction, window_seconds: int = 300) -> Optional[ReasonCode]
   - Returns RAPID_REVERSAL if target_transaction is a DEBIT and there's a matching CREDIT to same beneficiary within window
   - Match criteria: same account_id, same beneficiary_id, similar amount (within 1%), opposite type
   - Return None otherwise

5. get_explanation(reason_code: ReasonCode, context: dict) -> str
   - Returns human-readable explanation for each reason code
   - context dict contains relevant details (e.g., velocity count, amount, etc.)

Constraints:
- Pure functions (no side effects)
- Deterministic (no randomness)
- Type hints on all parameters and returns
- Docstrings with examples

Also create /tests/day2/test_aml_rules.py with pytest tests for each rule:
- Test HIGH_VELOCITY: 4 transactions in 30s → triggers, 2 transactions → doesn't trigger
- Test ROUND_AMOUNT: 5000.00 → triggers, 4999.99 → doesn't
- Test HIGH_AMOUNT: 15000 → triggers, 9999 → doesn't
- Test RAPID_REVERSAL: debit + credit within 5 min → triggers
- Test get_explanation: generates correct strings for each reason code

Verification:
pytest tests/day2/test_aml_rules.py -v

STOP after completing rules.py and test_aml_rules.py.
```

**Your actions:**
```bash
pytest tests/day2/test_aml_rules.py -v

# Review test output carefully
# If any failures, review logic with agent

# If all pass:
git add src/day2/aml_triage/rules.py tests/day2/test_aml_rules.py
git commit -m "Implement AML rule functions with tests"
```

---

### Task 3: Implement Triage Scoring (20 minutes)

**Goal:** Assign priority levels based on rule combinations.

**Agent Prompt:**
```text
You are a GitHub Copilot coding agent.

Create /src/day2/aml_triage/triage.py for alert priority scoring.

Import schemas (Alert, TriageDecision, ReasonCode)

Implement:

1. compute_triage_score(alert: Alert) -> float
   - Scoring logic:
     - HIGH_VELOCITY: +50 points
     - ROUND_AMOUNT: +20 points
     - HIGH_AMOUNT: +30 points
     - RAPID_REVERSAL: +40 points
     - NEW_BENEFICIARY: +25 points
   - Multiple reason codes stack (additive)
   - Return total score as float

2. assign_priority(triage_score: float) -> Literal["P1", "P2", "P3"]
   - P1: score >= 70
   - P2: score >= 40 and < 70
   - P3: score < 40

3. assign_queue(priority: str) -> str
   - P1 → "HIGH_RISK"
   - P2 → "MEDIUM_RISK"
   - P3 → "LOW_RISK"

4. create_triage_decision(alert: Alert) -> TriageDecision
   - Orchestrates: compute score → assign priority → assign queue
   - Returns TriageDecision object

Constraints:
- Deterministic scoring (no randomness)
- Pure functions
- Type hints and docstrings

Also create /tests/day2/test_triage_scoring.py:
- Test compute_triage_score: single rule, multiple rules
- Test assign_priority: boundary cases (exactly 70, 40)
- Test assign_queue: all priority levels
- Test create_triage_decision: end-to-end for sample alert

Verification:
pytest tests/day2/test_triage_scoring.py -v

STOP after completing triage.py and tests.
```

**Your actions:**
```bash
pytest tests/day2/test_triage_scoring.py -v
git add src/day2/aml_triage/triage.py tests/day2/test_triage_scoring.py
git commit -m "Implement triage scoring logic with tests"
```

---

### Task 4: Implement I/O Handlers (15 minutes)

**Goal:** Read CSV input, write JSON/CSV outputs.

**Agent Prompt:**
```text
Create /src/day2/aml_triage/io.py for input/output handling.

Implement:

1. load_transactions(csv_path: Path) -> List[Transaction]
   - Read CSV using pandas or csv module
   - Parse into Transaction Pydantic models
   - Sort by timestamp (ascending)
   - Return list

2. write_alerts_json(alerts: List[Alert], output_path: Path) -> None
   - Serialize alerts to JSON
   - Use Pydantic's .model_dump_json() or .dict()
   - Pretty-print (indent=2)
   - Include timestamp in ISO format

3. write_triage_queue_csv(decisions: List[TriageDecision], output_path: Path) -> None
   - Write CSV with columns:
     - alert_id, account_id, amount, priority, triage_score, reason_codes (comma-separated), queue
   - Sort by triage_score descending (highest priority first)

4. write_summary(decisions: List[TriageDecision], output_path: Path) -> None
   - Write JSON summary:
     - total_alerts: count
     - by_priority: {P1: count, P2: count, P3: count}
     - by_reason_code: {HIGH_VELOCITY: count, ...}
     - by_queue: {HIGH_RISK: count, ...}

Constraints:
- Use pathlib.Path for file paths
- Handle errors gracefully (e.g., file not found)
- Type hints and docstrings

Tests in /tests/day2/test_io.py:
- Test load_transactions: loads sample CSV correctly
- Test write_alerts_json: writes valid JSON
- Test write_triage_queue_csv: sorts correctly, all columns present
- Test write_summary: counts match input data

Verification:
pytest tests/day2/test_io.py -v

STOP after completing io.py and tests.
```

**Your actions:**
```bash
pytest tests/day2/test_io.py -v
git add src/day2/aml_triage/io.py tests/day2/test_io.py
git commit -m "Implement I/O handlers with tests"
```

---

### Task 5: Build the Pipeline Orchestrator (20 minutes)

**Goal:** Tie all modules together into an end-to-end pipeline.

**Agent Prompt:**
```text
Create /src/day2/aml_triage/pipeline.py to orchestrate the full AML triage workflow.

Import: schemas, rules, triage, io

Implement:

1. generate_alerts(transactions: List[Transaction]) -> List[Alert]
   - For each transaction:
     - Check all rules (high_velocity, round_amount, high_amount, rapid_reversal)
     - Collect triggered reason codes
     - If any rules trigger, create Alert
     - Generate unique alert_id (e.g., "ALERT-{transaction_id}")
     - Add explanation using rules.get_explanation
   - Return list of alerts
   - Sort alerts by timestamp

2. run_pipeline(input_csv: Path, output_dir: Path) -> dict
   - Load transactions from input_csv
   - Generate alerts
   - Create triage decisions for all alerts
   - Write outputs:
     - {output_dir}/aml_alerts.json
     - {output_dir}/triage_queue.csv
     - {output_dir}/summary.json
   - Return summary dict

Constraints:
- Deterministic: same input always produces same output
- All outputs in specified output_dir
- Handle edge cases (no alerts generated, empty input)

Tests in /tests/day2/test_pipeline_end_to_end.py:
- Test generate_alerts: sample transactions → expected alerts
- Test run_pipeline: full end-to-end with sample data
- Verify outputs exist and contain expected data
- Test determinism: run twice, outputs identical

Verification:
pytest tests/day2/test_pipeline_end_to_end.py -v

STOP after completing pipeline.py and tests.
```

**Your actions:**
```bash
pytest tests/day2/test_pipeline_end_to_end.py -v
git add src/day2/aml_triage/pipeline.py tests/day2/test_pipeline_end_to_end.py
git commit -m "Implement pipeline orchestrator with end-to-end tests"
```

---

### Task 6: Create CLI Entrypoint (10 minutes)

**Goal:** Provide a command-line interface for running the pipeline.

**Agent Prompt:**
```text
Create /src/day2/aml_triage/cli.py as the CLI entrypoint.

Use argparse or click (prefer argparse for simplicity).

CLI interface:
python -m src.day2.aml_triage.cli --input <csv_path> --outdir <output_directory>

Arguments:
- --input: path to input CSV (required)
- --outdir: output directory for results (default: out/day2/lab3)

Behavior:
- Parse arguments
- Validate input file exists
- Create output directory if not exists
- Call pipeline.run_pipeline
- Print summary to console:
  - "Processed X transactions"
  - "Generated Y alerts"
  - "Priority breakdown: P1=A, P2=B, P3=C"
  - "Outputs written to {outdir}"

Also create /src/day2/aml_triage/__init__.py (can be empty)

Constraints:
- User-friendly error messages
- Return exit code 0 on success, 1 on error

Manual test (not automated):
python -m src.day2.aml_triage.cli --input src/samples/sample_transactions_day2.csv --outdir out/day2/lab3

STOP after creating cli.py.
```

**Your actions:**
```bash
# Manual test:
python -m src.day2.aml_triage.cli --input src/samples/sample_transactions_day2.csv --outdir out/day2/lab3

# Check outputs:
ls out/day2/lab3/
cat out/day2/lab3/summary.json

# If works correctly:
git add src/day2/aml_triage/cli.py src/day2/aml_triage/__init__.py
git commit -m "Add CLI entrypoint for AML triage pipeline"
```

---

### Task 7: Create README and Documentation (10 minutes)

**Goal:** Document how to run the pipeline and interpret results.

**Agent Prompt:**
```text
Create /src/day2/aml_triage/README.md documenting the AML Alert Triage Pipeline.

Include:

1. Overview (what it does, why it exists)
2. Architecture diagram (text-based is fine)
3. Rule descriptions (what each rule detects)
4. Installation requirements
5. Usage examples:
   - Run with sample data
   - Run tests
   - Interpret outputs
6. Output file descriptions:
   - aml_alerts.json: structure and fields
   - triage_queue.csv: columns and sort order
   - summary.json: statistics
7. Determinism guarantees (for audit)
8. Limitations (synthetic data, not production-ready)

Format: Clear sections, code blocks for commands, examples of output snippets.

STOP after creating README.md.
```

**Your actions:**
```bash
# Review README:
cat src/day2/aml_triage/README.md

git add src/day2/aml_triage/README.md
git commit -m "Add documentation for AML triage pipeline"
```

---

## Acceptance Criteria

### Functional Requirements

✅ **Pipeline processes transactions and generates alerts**
- All rules implemented correctly
- Reason codes assigned accurately
- Alerts contain required fields

✅ **Triage scoring is deterministic**
- Same input → same output every time
- Stable sort order (by score descending, then alert_id)

✅ **Outputs are audit-friendly**
- JSON alerts include reason codes and explanations
- CSV queue is analyst-readable
- Summary provides statistics

✅ **CLI works end-to-end**
- Can run: `python -m src.day2.aml_triage.cli --input ... --outdir ...`
- Outputs written to specified directory
- User-friendly console messages

### Testing Requirements

✅ **Unit tests for all modules**
- schemas, rules, triage, io, pipeline
- All tests pass: `pytest tests/day2/ -v`

✅ **End-to-end test**
- Full pipeline run with sample data
- Outputs validated

✅ **Determinism test**
- Run twice, diff outputs → identical

### Documentation Requirements

✅ **README.md exists**
- Explains architecture
- Provides usage examples
- Documents outputs

✅ **Code comments**
- Docstrings on all functions
- Inline comments for complex logic

---

## Verification Commands

```bash
# Run all tests
pytest tests/day2/ -v

# Run with coverage
pytest tests/day2/ --cov=src.day2.aml_triage --cov-report=term-missing

# Run pipeline manually
python -m src.day2.aml_triage.cli --input src/samples/sample_transactions_day2.csv --outdir out/day2/lab3

# Check outputs
ls -lh out/day2/lab3/
cat out/day2/lab3/summary.json
head out/day2/lab3/triage_queue.csv

# Test determinism
python -m src.day2.aml_triage.cli --input src/samples/sample_transactions_day2.csv --outdir out/day2/lab3_run1
python -m src.day2.aml_triage.cli --input src/samples/sample_transactions_day2.csv --outdir out/day2/lab3_run2
diff out/day2/lab3_run1/aml_alerts.json out/day2/lab3_run2/aml_alerts.json
# Should show no differences
```

---

## Auditor's Lens: Evidence to Retain

When building production systems, auditors will look for:

✅ **Rule logic documentation** — What does each rule detect? Why those thresholds?  
✅ **Reason code traceability** — Can we trace each alert back to the rule(s) that triggered it?  
✅ **Determinism proof** — Can we reproduce results for a given input?  
✅ **Test coverage** — Are all rules tested? Edge cases covered?  
✅ **Change history** — Git commits showing when rules changed and why  
✅ **Output retention** — Alerts and triage decisions logged for review

**In this lab, you've created:**
- ✅ Documented rules in README
- ✅ Reason codes in alert outputs
- ✅ Deterministic pipeline (verified by tests)
- ✅ Unit and end-to-end tests
- ✅ Git commit history
- ✅ JSON/CSV outputs for audit trail

---

## Reflexion Questions

After completing the lab, ask yourself:

1. **Where did the agent make assumptions?** Did you catch them in code review?
2. **Which stop points were most valuable?** (After schemas? After rules?)
3. **Did tests catch any bugs?** What would have happened without them?
4. **Is the output truly deterministic?** How did you verify?
5. **Could an auditor reproduce your results?** What evidence did you provide?
6. **What would you change** for a production version? (Better logging? Config management? Database persistence?)

---

## Extension Challenges (Optional)

If you finish early, try:

1. **Add a NEW_BENEFICIARY rule** that flags first-time beneficiaries for an account
2. **Implement time-based windowing** that processes transactions in batches (e.g., hourly)
3. **Add configurable thresholds** via YAML/JSON config file
4. **Generate HTML report** summarizing alerts with charts (use matplotlib or Plotly)
5. **Add logging** with appropriate levels (INFO for pipeline steps, WARNING for edge cases)

---

## Next Lab

**Lab 4** will focus on **PII protection patterns** (masking, tokenization, audit logging) to handle sensitive data safely.

---

**Need help?** Ask Copilot Chat:
```
I'm stuck on the HIGH_VELOCITY rule. How do I count transactions within a time window efficiently?
```

or

```
My triage tests are failing. How do I debug pytest failures effectively?
```
