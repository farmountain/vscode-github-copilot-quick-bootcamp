# Lab 1: Data Quality Rules Engine

**Duration**: 2 hours (13:30–15:30)  
**Level**: Beginner to Intermediate  
**Focus**: Building a transaction validation system using AI assistance

## Learning Objectives

By the end of this lab, you will:

* Build a deterministic, testable rules engine for transaction validation
* Apply the 3C framework (Context, Constraints, Criteria) to structure prompts
* Use GitHub Copilot Chat and Agent Mode to generate multi-file solutions
* Write comprehensive tests for validation logic
* Create audit-ready output with structured findings
* Generate and work with synthetic data

## Business Context

You work for a retail bank that processes thousands of transactions daily. Before transactions are posted to the ledger, they must pass data quality checks. Currently, these checks are manual and error-prone. Your team needs to automate transaction validation with a rules engine that:

* Validates required fields
* Checks data formats and ranges
* Detects duplicates
* Produces audit-ready reports

**Compliance requirement**: All validation findings must be deterministic (same input → same output) and traceable (each finding linked to specific rule and record).

## Lab Overview

### What You'll Build

A Python-based data quality rules engine with:

1. **Transaction model** - Structured data representation
2. **Validation rules** - Individual, testable rule functions
3. **Rules engine** - Orchestrates rule execution and aggregates findings
4. **I/O utilities** - Read CSV, write JSON reports
5. **CLI interface** - Command-line tool for batch validation
6. **Comprehensive tests** - Unit and integration tests
7. **Synthetic data generator** - Creates test datasets

### Project Structure

```
src/day1/data_quality/
├── __init__.py
├── models.py           # Transaction and ValidationFinding models
├── rules.py            # Individual validation rule functions
├── engine.py           # Rules engine orchestration
├── io.py               # CSV/JSON I/O utilities
├── cli.py              # Command-line interface
└── README.md           # Usage documentation

tests/day1/
├── test_data_quality_rules.py    # Unit tests for rules
└── test_data_quality_engine.py   # Integration tests

src/samples/
├── synthetic_data_generator.py   # Generate test data
└── sample_transactions.csv       # Sample input file
```

---

## Part 1: Setup and Planning (15 min)

### Step 1: Understand the Requirements

**Validation rules to implement**:

1. **Required fields check**: Ensure all mandatory fields are present and non-empty
   - Required: `txn_id`, `account_id`, `amount`, `currency`, `txn_ts`
   
2. **Amount validation**: Amount must be positive
   - Rule: `amount > 0`
   - Severity: ERROR
   
3. **Currency validation**: Currency must be valid ISO-like format
   - Rule: 3 uppercase letters (e.g., USD, EUR, GBP)
   - Severity: ERROR
   
4. **Timestamp validation**: Transaction timestamp must be valid and not in far future
   - Rule: Valid ISO-8601 format, not more than 1 day in the future
   - Severity: ERROR
   
5. **Account ID format**: Account ID must match expected pattern
   - Rule: Starts with "ACC" followed by 8 digits (e.g., ACC12345678)
   - Severity: ERROR
   
6. **Duplicate detection**: Detect duplicate transaction IDs
   - Rule: No two transactions can have the same txn_id
   - Severity: ERROR

**Output format**:
```json
{
  "report_id": "DQ-20240115-120000",
  "generated_at": "2024-01-15T12:00:00Z",
  "summary": {
    "total_records": 100,
    "valid_records": 85,
    "invalid_records": 15,
    "findings_by_severity": {
      "ERROR": 18,
      "WARN": 2
    }
  },
  "findings": [
    {
      "record_index": 5,
      "txn_id": "TX12345",
      "rule": "amount_positive",
      "severity": "ERROR",
      "message": "Amount must be positive, got: -100.00"
    }
  ]
}
```

### Step 2: Plan Your Approach

Before jumping into code, answer these questions (Paul-Elder framework):

* **Purpose**: What business outcome? → Automated, reliable transaction validation
* **Question**: What are we building? → A rules engine with 6 validation rules
* **Information**: What data? → CSV files with synthetic transaction data
* **Assumptions**: What constraints? → Deterministic, no external dependencies, Python 3.9+
* **Implications**: What could go wrong? → False positives/negatives, missed edge cases
* **Point of View**: Perspectives? → Developer (maintainability), Auditor (traceability), User (clarity)

---

## Part 2: Implement the Data Models (20 min)

### Step 2.1: Use Copilot to Generate the Transaction Model

**Prompt for Copilot Chat**:

```
Create a Transaction data model for a banking data quality system.

[Context]
We're building a transaction validation system. Transactions are loaded from CSV and validated against business rules.

[Constraints]
- Use Python 3.9+ with Pydantic v2 for data validation
- Use Decimal for amounts (not float)
- Use datetime for timestamps (timezone-aware)
- All fields should have type hints
- Include field descriptions

[Criteria]
Create a Pydantic BaseModel called Transaction with fields:
- txn_id: str (required, unique identifier)
- account_id: str (required, account identifier)
- amount: Decimal (required, transaction amount)
- currency: str (required, 3-letter currency code)
- txn_ts: datetime (required, transaction timestamp with timezone)
- description: str (optional, transaction description)

Also create a ValidationFinding model with fields:
- record_index: int (row number in input file)
- txn_id: str (transaction ID)
- rule: str (name of validation rule)
- severity: str (ERROR or WARN)
- message: str (human-readable description)

Include a docstring for each model explaining its purpose.
Save to src/day1/data_quality/models.py
```

**Expected output**: Copilot should generate a `models.py` file with two Pydantic models.

### Step 2.2: Review and Verify

**Review checklist**:
- [ ] Are all required fields present?
- [ ] Is Decimal used for amount (not float)?
- [ ] Are timestamps timezone-aware?
- [ ] Are there docstrings?
- [ ] Does it follow Pydantic v2 syntax?

**Verification**:
```python
# Test in a Python REPL or notebook
from src.day1.data_quality.models import Transaction, ValidationFinding
from decimal import Decimal
from datetime import datetime, UTC

# Should work
txn = Transaction(
    txn_id="TX001",
    account_id="ACC12345678",
    amount=Decimal("100.50"),
    currency="USD",
    txn_ts=datetime.now(UTC),
    description="Test transaction"
)
print(txn)
```

---

## Part 3: Implement Validation Rules (30 min)

### Step 3.1: Generate Individual Rule Functions

**Prompt for Copilot Chat**:

```
Create validation rule functions for a transaction data quality engine.

[Context]
We have a Transaction model (from models.py) and need to validate transactions against business rules.
Each rule should be a pure function that takes a Transaction and returns a ValidationFinding or None.

[Constraints]
- Use Python 3.9+ with type hints
- Each rule is a separate function for testability
- Rules are pure functions (no side effects, no external dependencies)
- Return ValidationFinding for failures, None for passes
- Include docstrings with examples

[Criteria]
Create these rule functions in src/day1/data_quality/rules.py:

1. check_required_fields(txn: Transaction, record_index: int) -> list[ValidationFinding]
   - Verify txn_id, account_id, amount, currency, txn_ts are present
   - Return list of findings (one per missing field)

2. check_amount_positive(txn: Transaction, record_index: int) -> ValidationFinding | None
   - Verify amount > 0
   - Return finding with severity ERROR if not

3. check_currency_format(txn: Transaction, record_index: int) -> ValidationFinding | None
   - Verify currency is exactly 3 uppercase letters
   - Use regex: ^[A-Z]{3}$

4. check_timestamp_valid(txn: Transaction, record_index: int) -> ValidationFinding | None
   - Verify txn_ts is not more than 1 day in the future
   - Use timezone-aware comparison

5. check_account_id_format(txn: Transaction, record_index: int) -> ValidationFinding | None
   - Verify account_id matches pattern: ACC followed by 8 digits
   - Use regex: ^ACC\d{8}$

Include imports: Transaction, ValidationFinding from models.py
Include: from datetime import datetime, timedelta, UTC
Include: import re for regex
```

**Expected output**: Copilot should generate `rules.py` with 5 functions.

### Step 3.2: Review and Test Individual Rules

**Manual test (create a test file or use REPL)**:

```python
from src.day1.data_quality.models import Transaction
from src.day1.data_quality.rules import check_amount_positive
from decimal import Decimal
from datetime import datetime, UTC

# Test positive amount (should pass)
txn_valid = Transaction(
    txn_id="TX001",
    account_id="ACC12345678",
    amount=Decimal("100.00"),
    currency="USD",
    txn_ts=datetime.now(UTC),
)
finding = check_amount_positive(txn_valid, 0)
assert finding is None, "Valid amount should not generate finding"

# Test negative amount (should fail)
txn_invalid = Transaction(
    txn_id="TX002",
    account_id="ACC12345678",
    amount=Decimal("-50.00"),
    currency="USD",
    txn_ts=datetime.now(UTC),
)
finding = check_amount_positive(txn_invalid, 1)
assert finding is not None, "Negative amount should generate finding"
assert finding.severity == "ERROR"
print(f"Finding: {finding.message}")
```

---

## Part 4: Implement the Rules Engine (30 min)

### Step 4.1: Generate the Engine Orchestration

**Prompt for Copilot Chat**:

```
Create a rules engine that orchestrates validation rule execution.

[Context]
We have individual rule functions in rules.py. We need an engine that:
- Loads transactions
- Applies all rules
- Detects duplicates
- Aggregates findings
- Produces a summary report

[Constraints]
- Use Python 3.9+ with type hints
- Must be deterministic (same input → same output, always)
- Must handle large datasets efficiently (streaming, not loading all in memory)
- Duplicate detection: check txn_id uniqueness across all transactions
- Sort findings by record_index for reproducibility

[Criteria]
Create src/day1/data_quality/engine.py with:

1. ValidationEngine class with method:
   validate(transactions: list[Transaction]) -> dict
   
2. The validate method should:
   - Initialize an empty findings list
   - Track seen txn_ids for duplicate detection
   - For each transaction (with index):
     - Apply all rule functions from rules.py
     - Collect findings
     - Check for duplicate txn_id (add ERROR finding if duplicate)
   - Generate summary dict with:
     - report_id (format: "DQ-YYYYMMDD-HHMMSS")
     - generated_at (ISO-8601 timestamp)
     - summary (total_records, valid_records, invalid_records, findings_by_severity)
     - findings (list of findings as dicts)
   
3. Sort findings by record_index for determinism

4. Include docstrings and type hints

Import all rule functions from rules.py
Import Transaction, ValidationFinding from models.py
```

**Expected output**: Copilot should generate `engine.py` with `ValidationEngine` class.

### Step 4.2: Add Duplicate Detection Logic

**If Copilot didn't include duplicate detection**, prompt:

```
Add duplicate transaction ID detection to the ValidationEngine.

[Context]
Current engine applies individual rules but doesn't check for duplicate txn_ids across the dataset.

[Criteria]
Modify the validate method to:
- Before processing transactions, create a set to track seen txn_ids
- For each transaction:
  - If txn_id is already in the set, add a ValidationFinding with:
    - rule: "duplicate_txn_id"
    - severity: "ERROR"
    - message: f"Duplicate transaction ID: {txn_id}"
  - Add txn_id to the set
- Ensure this happens before other rule checks
```

---

## Part 5: Implement I/O Utilities (20 min)

### Step 5.1: Generate CSV Reader and JSON Writer

**Prompt for Copilot Chat**:

```
Create I/O utilities for reading transaction CSVs and writing JSON reports.

[Context]
We need to load transactions from CSV files and write validation reports as JSON.

[Constraints]
- Use Python csv module for reading
- Use json module for writing
- Handle errors gracefully (file not found, malformed CSV, encoding issues)
- Log errors but don't crash
- Use UTF-8 encoding

[Criteria]
Create src/day1/data_quality/io.py with:

1. load_transactions_from_csv(file_path: str) -> list[Transaction]
   - Read CSV with headers: txn_id, account_id, amount, currency, txn_ts, description
   - Parse amount as Decimal
   - Parse txn_ts as datetime (support ISO-8601 format)
   - Skip rows with parsing errors (log warning with row number)
   - Return list of valid Transaction objects

2. write_report_to_json(report: dict, file_path: str) -> None
   - Write report dict to JSON file
   - Use indent=2 for readability
   - Handle file write errors gracefully

Include error handling:
- FileNotFoundError
- ValueError (for parsing errors)
- JSONDecodeError (if applicable)

Include docstrings and type hints
Import: csv, json, logging, Decimal, datetime, Transaction
```

**Expected output**: Copilot should generate `io.py` with two functions.

---

## Part 6: Implement CLI (15 min)

### Step 6.1: Generate Command-Line Interface

**Prompt for Copilot Chat**:

```
Create a command-line interface for the data quality engine.

[Context]
Users need a simple CLI to validate transaction CSVs and output JSON reports.

[Constraints]
- Use argparse for CLI arguments
- Support: --input <csv_file> --output <json_file>
- Print summary to console (total records, valid, invalid)
- Exit with code 0 for success, 1 for errors

[Criteria]
Create src/day1/data_quality/cli.py with:

1. main() function that:
   - Parses arguments: --input (required), --output (required)
   - Loads transactions using load_transactions_from_csv
   - Runs ValidationEngine
   - Writes report using write_report_to_json
   - Prints summary to console
   
2. Console output format:
   Data Quality Validation Report
   ==============================
   Total records: <n>
   Valid records: <n>
   Invalid records: <n>
   Findings: <n> errors, <n> warnings
   
   Report saved to: <output_file>

3. If __name__ == "__main__": main()

Include error handling for missing files, write errors
Import: argparse, sys, load_transactions_from_csv, write_report_to_json, ValidationEngine
```

**Expected output**: Copilot should generate `cli.py` with CLI logic.

---

## Part 7: Generate Synthetic Test Data (15 min)

### Step 7.1: Create Data Generator

**Prompt for Copilot Chat**:

```
Create a synthetic transaction data generator for testing.

[Context]
We need realistic but fake transaction data to test the validation engine.
Include both valid and invalid records to exercise all validation rules.

[Constraints]
- Generate CSV with headers: txn_id, account_id, amount, currency, txn_ts, description
- Use Python faker library or random module
- Deterministic (use fixed random seed)
- No real customer data

[Criteria]
Create src/samples/synthetic_data_generator.py with:

1. generate_transactions(num_records: int = 100, seed: int = 42) -> list[dict]
   - Generate mix of valid (80%) and invalid (20%) transactions
   - Invalid records should include:
     - Negative amounts (5%)
     - Invalid currency codes (3%)
     - Future timestamps (3%)
     - Invalid account IDs (4%)
     - Duplicate txn_ids (5%)
   
2. write_csv(transactions: list[dict], file_path: str) -> None
   - Write to CSV file

3. main() function:
   - Generate 100 transactions
   - Write to src/samples/sample_transactions.csv
   - Print summary

Use deterministic data:
- txn_id: TX{000001..000100}
- account_id: ACC{12345678..12345778} (valid pattern)
- amount: random between 0.01 and 10000.00
- currency: mostly USD, EUR, GBP; occasionally invalid (e.g., "US", "EURO")
- txn_ts: mostly recent, a few in future
- description: generic (e.g., "Purchase at Store #123")

If __name__ == "__main__": main()
```

**Expected output**: Copilot should generate `synthetic_data_generator.py`.

### Step 7.2: Generate Sample Data

**Run the generator**:
```bash
python -m src.samples.synthetic_data_generator
```

**Verify**:
- [ ] File `src/samples/sample_transactions.csv` created
- [ ] Contains ~100 records
- [ ] Mix of valid and invalid records

---

## Part 8: Write Tests (30 min)

### Step 8.1: Generate Unit Tests for Rules

**Prompt for Copilot Chat**:

```
Create comprehensive pytest unit tests for validation rules.

[Context]
We have validation rule functions in src/day1/data_quality/rules.py.
Each rule needs thorough unit tests covering happy path, edge cases, and error cases.

[Constraints]
- Use pytest framework
- Use AAA pattern (Arrange, Act, Assert)
- Use descriptive test names (test_<rule>_<scenario>)
- Use pytest fixtures for common test data
- Test each rule independently

[Criteria]
Create tests/day1/test_data_quality_rules.py with:

1. Fixture: valid_transaction() -> Transaction
   - Returns a fully valid Transaction object

2. Test classes for each rule:
   - TestAmountPositive
     - test_positive_amount_passes
     - test_negative_amount_fails
     - test_zero_amount_fails
   
   - TestCurrencyFormat
     - test_valid_three_letter_currency_passes
     - test_two_letter_currency_fails
     - test_four_letter_currency_fails
     - test_lowercase_currency_fails
     - test_empty_currency_fails
   
   - TestTimestampValid
     - test_current_timestamp_passes
     - test_past_timestamp_passes
     - test_future_timestamp_within_threshold_passes
     - test_far_future_timestamp_fails
   
   - TestAccountIdFormat
     - test_valid_account_id_passes
     - test_wrong_prefix_fails
     - test_too_few_digits_fails
     - test_too_many_digits_fails
     - test_letters_in_number_fails

Each test should:
- Create a Transaction with the scenario's data
- Call the rule function
- Assert the result (None for pass, ValidationFinding for fail)
- If fail, assert severity and message content

Import: pytest, Transaction, ValidationFinding, all rule functions, Decimal, datetime, UTC
```

**Expected output**: Copilot should generate comprehensive unit tests.

### Step 8.2: Generate Integration Tests

**Prompt for Copilot Chat**:

```
Create pytest integration tests for the complete validation engine.

[Context]
We need end-to-end tests that verify the complete workflow:
load CSV → validate → write report.

[Constraints]
- Use pytest with tmp_path fixture for file I/O
- Test with synthetic data
- Verify report structure and content
- Test both valid-only and mixed datasets

[Criteria]
Create tests/day1/test_data_quality_engine.py with:

1. test_engine_with_all_valid_transactions(tmp_path)
   - Create CSV with 5 valid transactions
   - Run engine
   - Assert: 5 valid, 0 invalid, 0 findings

2. test_engine_with_mixed_transactions(tmp_path)
   - Create CSV with 10 transactions (7 valid, 3 invalid with different rule violations)
   - Run engine
   - Assert: correct counts, findings contain expected txn_ids and rules

3. test_engine_detects_duplicates(tmp_path)
   - Create CSV with duplicate txn_ids
   - Run engine
   - Assert: duplicate findings present

4. test_end_to_end_cli_workflow(tmp_path)
   - Create input CSV
   - Run CLI (import and call main function with args)
   - Verify output JSON exists and is valid
   - Verify report structure

Each test should verify:
- Report has required fields (report_id, generated_at, summary, findings)
- Summary counts are accurate
- Findings are sorted by record_index
- Findings have required fields (record_index, txn_id, rule, severity, message)

Import: pytest, json, ValidationEngine, load_transactions_from_csv, write_report_to_json, cli
```

**Expected output**: Copilot should generate integration tests.

### Step 8.3: Run Tests

**Run all tests**:
```bash
# Run all Day 1 tests
pytest tests/day1/ -v

# Run with coverage
pytest tests/day1/ --cov=src/day1/data_quality --cov-report=html

# View coverage report
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac/Linux
```

**Verification**:
- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] No import errors

---

## Part 9: Create Documentation (10 min)

### Step 9.1: Generate README

**Prompt for Copilot Chat**:

```
Create a README for the data quality rules engine module.

[Context]
We have a complete transaction validation system with CLI, tests, and synthetic data.
Users need clear documentation on how to use it.

[Criteria]
Create src/day1/data_quality/README.md with:

1. Overview (what it does, why it exists)
2. Features (list of validation rules)
3. Installation (dependencies: pydantic, pytest)
4. Usage:
   - Generate synthetic data
   - Run CLI validation
   - Example input/output
5. Architecture (brief description of modules)
6. Testing (how to run tests)
7. Example output (sample JSON report excerpt)

Use markdown formatting, code blocks for commands, and clear section headers.
Assume audience is developers familiar with Python but new to this codebase.
```

**Expected output**: Copilot should generate a comprehensive README.

---

## Part 10: Verification and Demo (10 min)

### Step 10.1: Run Complete Workflow

**Execute these commands**:

```bash
# Step 1: Generate synthetic data
python -m src.samples.synthetic_data_generator

# Step 2: Validate transactions
python -m src.day1.data_quality.cli \
  --input src/samples/sample_transactions.csv \
  --output output/dq_report.json

# Step 3: View report
cat output/dq_report.json  # or type on Windows

# Step 4: Run tests
pytest tests/day1/ -v
```

**Verification checklist**:
- [ ] Synthetic data CSV generated successfully
- [ ] CLI runs without errors
- [ ] JSON report created with expected structure
- [ ] Console output shows summary
- [ ] All tests pass

### Step 10.2: Review the Output

**Open the JSON report** and verify:
- [ ] `report_id` is present and unique
- [ ] `generated_at` timestamp is correct
- [ ] `summary` section has accurate counts
- [ ] `findings` array contains validation failures
- [ ] Each finding has `record_index`, `txn_id`, `rule`, `severity`, `message`
- [ ] Findings are sorted by `record_index`

---

## Part 11: Reflexion (10 min)

### Individual Reflexion

Take 5 minutes to answer these questions:

**What did Copilot do well?**
* Which code was immediately usable?
* Where did Copilot save you time?

**Where did Copilot struggle?**
* What code needed fixing?
* What did you need to re-prompt?

**What evidence do you have that your code works?**
* What tests passed?
* What verification steps did you complete?

**What would you do differently next time?**
* How would you improve your prompts?
* What would you test more thoroughly?

### Group Discussion (5 min)

Share with your lab partner or group:
* One surprising success
* One challenge you overcame
* One lesson learned about prompting

---

## Success Criteria

You've successfully completed Lab 1 if:

- [x] All required modules created (models, rules, engine, io, cli)
- [x] All 6 validation rules implemented
- [x] Duplicate detection working
- [x] Synthetic data generator working
- [x] Unit tests pass (>80% coverage)
- [x] Integration tests pass
- [x] CLI produces valid JSON reports
- [x] Documentation is clear and complete

---

## Auditor's Lens: What Evidence Would You Show?

If an auditor asked "How do you know this validation system works correctly?", you would show:

1. **Test results**: pytest output showing all tests pass
2. **Coverage report**: >80% code coverage
3. **Sample reports**: JSON outputs with synthetic data
4. **Code review**: Well-documented, readable code
5. **Determinism proof**: Run same input twice, get identical output

**Exercise**: Run the validation twice on the same input and diff the outputs:
```bash
python -m src.day1.data_quality.cli --input src/samples/sample_transactions.csv --output report1.json
python -m src.day1.data_quality.cli --input src/samples/sample_transactions.csv --output report2.json
diff report1.json report2.json  # Should be identical except timestamp
```

---

## Extension Challenges (Optional)

If you finish early, try these:

1. **Add a new rule**: Implement a rule to detect unusually large amounts (>$50,000)
2. **Add severity levels**: Implement WARN severity for minor issues
3. **Add batch processing**: Modify CLI to accept a directory of CSV files
4. **Add HTML report**: Generate an HTML summary report with charts
5. **Add performance profiling**: Measure time per rule and optimize

---

## What's Next?

Proceed to **[Lab 2: Simple Risk Scoring Service](lab2_simple_risk_scoring_service.md)** to build an explainable risk scoring API with audit logging.

---

**Navigation**:
* [Back to Day 1 README](../README.md)
* [Session 1.1: Intro to Agentic Dev](../session1_1_intro_to_agentic_dev.md)
* [Session 1.2: Prompting in VS Code](../session1_2_prompting_in_vscode.md)
* [Lab 2: Risk Scoring Service](lab2_simple_risk_scoring_service.md)
