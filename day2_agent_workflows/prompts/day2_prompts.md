# Day 2 — Copilot Agent Prompts (Copy-Paste Ready)

This document contains all prompts for Day 2 training exercises and labs. These prompts are designed to be pasted directly into **GitHub Copilot Agent Mode** in VS Code.

---

## Table of Contents

1. [Session 2.1 Micro-Exercises](#session-21-micro-exercises)
2. [Session 2.2 Refactoring Exercises](#session-22-refactoring-exercises)
3. [Lab 3: AML Alert Triage Pipeline](#lab-3-aml-alert-triage-pipeline)
4. [Lab 4: PII Masking/Tokenization](#lab-4-pii-maskingtokenization)
5. [General-Purpose Prompts](#general-purpose-prompts)

---

## Session 2.1 Micro-Exercises

### Exercise: Decompose a Feature into Tasks

**Prompt:**
```text
You are a GitHub Copilot assistant helping me decompose a feature into agent-friendly tasks.

Feature: "Velocity Checker for Transaction Monitoring"
Business goal: Flag accounts with unusual transaction frequency to detect potential fraud.

Please help me:
1. Break this feature into 2-3 user stories
2. For the first user story, break it into 3-4 technical tasks
3. For one task, write detailed acceptance criteria
4. Draft an agent prompt for that task (include scope, constraints, verification commands, and a STOP point)

Format the output clearly with sections for Stories, Tasks, Acceptance Criteria, and Agent Prompt.
```

---

## Session 2.2 Refactoring Exercises

### Exercise 1: Extract Constants

**Prompt:**
```text
You are a GitHub Copilot coding agent.

Refactor the current file to extract all magic numbers and hardcoded strings into a constants module.

Requirements:
- Create a new file: constants.py in the same directory
- Define clear constant names (UPPERCASE_WITH_UNDERSCORES)
- Update all references in the current file to use imported constants
- Preserve all existing behavior

Constraints:
- Do NOT change any logic
- All existing tests must pass unchanged
- Add docstrings to constants explaining their purpose

Verification:
pytest tests/ -v

STOP after creating constants.py. Wait for my verification before updating the main file.
```

### Exercise 2: Extract Function

**Prompt:**
```text
You are a GitHub Copilot coding agent.

Refactor the selected code block to extract it into a separate, well-named function.

Requirements:
- Create a new function with a descriptive name
- Add type hints for all parameters and return value
- Add a docstring explaining what the function does
- Replace the original code block with a call to the new function
- Ensure the function is testable in isolation

Constraints:
- Preserve existing behavior exactly
- Function should be pure if possible (no side effects)

Verification:
pytest tests/test_<module>.py -v

STOP after creating the function. I will review before proceeding.
```

### Exercise 3: Multi-File Refactor

**Prompt:**
```text
You are a GitHub Copilot coding agent.

Refactor the <module_name> module to improve separation of concerns.

Current state:
- All logic in one file: <file_name>.py (approx. <X> lines)

Refactor goals:
1. Extract data models to models.py (Pydantic schemas or dataclasses)
2. Extract business logic to <logic_module>.py
3. Keep <file_name>.py as orchestrator only
4. Extract constants to constants.py if any exist

Process:
- Create models.py first, STOP for verification
- Create <logic_module>.py, STOP for verification
- Update <file_name>.py, STOP for verification
- Run full test suite

Constraints:
- Preserve all existing behavior
- All tests must pass unchanged
- Add type hints to all new functions

Verification after each step:
pytest tests/ -v

Start with step 1: Create models.py. STOP after completion.
```

---

## Lab 3: AML Alert Triage Pipeline

### Prompt L3-1: Create Schemas

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

### Prompt L3-2: Implement Rule Functions

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

### Prompt L3-3: Implement Triage Scoring

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

### Prompt L3-4: Implement I/O Handlers

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

### Prompt L3-5: Build Pipeline Orchestrator

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

### Prompt L3-6: Create CLI Entrypoint

```text
Create /src/day2/aml_triage/cli.py as the CLI entrypoint.

Use argparse.

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

---

## Lab 4: PII Masking/Tokenization

### Prompt L4-1: Create Configuration

```text
You are a GitHub Copilot coding agent.

Create /src/day2/pii_protection/config.py for PII protection settings.

Define:

1. ProtectionMode enum (MASK, TOKENIZE, REDACT)

2. Config class (or dict) with:
   - mode: ProtectionMode (default MASK)
   - secret_salt: str (placeholder for env var, default "TRAINING_SALT_NOT_FOR_PROD")
   - pii_fields: List[str] = ["full_name", "email", "phone", "national_id", "address", "date_of_birth"]
   - safe_fields: List[str] = ["customer_id", "segment", "account_balance"]
   - output_dir: Path (default "out/day2/lab4")
   - audit_log_path: Path (default "{output_dir}/audit_log.jsonl")

3. load_config() function:
   - Reads from environment variables if present (PROTECTION_MODE, SECRET_SALT)
   - Falls back to defaults
   - Returns Config instance

Constraints:
- Type hints on all fields
- Docstrings explaining each setting
- Warning comment: "This is for training only. In production, use proper secrets management (Azure Key Vault, AWS Secrets Manager, etc.)"

No tests required for this module (it's just configuration).

STOP after creating config.py.
```

### Prompt L4-2: Implement Masking Functions

```text
Create /src/day2/pii_protection/masking.py with masking functions.

Implement:

1. mask_email(email: str) -> str
   - Show first char of username + domain
   - Example: "john.smith@example.com" → "j*****@example.com"

2. mask_phone(phone: str) -> str
   - Show last 4 digits only
   - Example: "+1-555-123-4567" → "***-***-4567"

3. mask_national_id(national_id: str) -> str
   - Show last 4 characters only
   - Example: "SSN-123-45-6789" → "***-**-6789"

4. mask_name(name: str) -> str
   - Show first initial + last initial
   - Example: "John Smith" → "J*** S****"

5. mask_address(address: str) -> str
   - Show city and state/zip only, redact street
   - Example: "123 Main St, New York, NY 10001" → "[REDACTED], New York, NY 10001"
   - Use simple heuristic: split by comma, redact first part

6. mask_date_of_birth(dob: str) -> str
   - Show year only
   - Example: "1980-05-15" → "1980-**-**"

7. mask_field(field_name: str, value: str) -> str
   - Dispatcher function: calls appropriate mask function based on field name
   - Raises ValueError for unknown field types

Constraints:
- Handle edge cases (empty strings, None, malformed inputs)
- Return "[INVALID]" for unparseable inputs
- Type hints and docstrings
- Pure functions (no side effects)

Also create /tests/day2/test_masking.py:
- Test each mask function with valid inputs
- Test edge cases (empty, None, malformed)
- Test mask_field dispatcher

Verification:
pytest tests/day2/test_masking.py -v

STOP after completing masking.py and tests.
```

### Prompt L4-3: Implement Tokenization

```text
Create /src/day2/pii_protection/tokenization.py for deterministic tokenization.

Use hashlib and hmac from Python standard library.

Implement:

1. generate_token(value: str, field_name: str, secret_salt: str) -> str
   - Use HMAC-SHA256: hmac.new(secret_salt.encode(), value.encode(), hashlib.sha256)
   - Encode digest as hex string
   - Prefix with field type for clarity: f"TOKEN_{field_name.upper()}_{hex_digest[:16]}"
   - Example: "john.smith@example.com" → "TOKEN_EMAIL_3f7a2b9c1e8d4f56"
   
2. tokenize_field(field_name: str, value: str, secret_salt: str) -> str
   - Wrapper for generate_token with field-specific handling
   - For now: tokenize entire value

3. verify_token_determinism(value: str, token: str, field_name: str, secret_salt: str) -> bool
   - Re-generate token and compare
   - Used for testing reversibility logic

Constraints:
- Deterministic: same input + same salt = same token always
- Token length manageable (not full hash, truncate to 16 hex chars after prefix)
- Type hints and docstrings
- Warning comment: "Tokens are NOT encryption. Do not use for sensitive data that requires true reversibility. For real tokenization, use a vault service (e.g., Azure Purview, HashiCorp Vault)."

Also create /tests/day2/test_tokenization.py:
- Test generate_token: same input produces same token
- Test different salts produce different tokens
- Test verify_token_determinism
- Test tokenize_field for various PII types

Verification:
pytest tests/day2/test_tokenization.py -v

STOP after completing tokenization.py and tests.
```

### Prompt L4-4: Implement Redaction

```text
Create /src/day2/pii_protection/redaction.py for field allowlisting.

Implement:

1. redact_fields(record: dict, pii_fields: List[str]) -> dict
   - Remove keys listed in pii_fields
   - Return new dict (don't mutate input)
   - Keep all other fields

2. allowlist_fields(record: dict, safe_fields: List[str]) -> dict
   - Keep ONLY keys listed in safe_fields
   - Return new dict
   - More restrictive than redact_fields

3. redact_or_allowlist(record: dict, mode: str, pii_fields: List[str], safe_fields: List[str]) -> dict
   - If mode == "REDACT": remove pii_fields
   - If mode == "ALLOWLIST": keep only safe_fields
   - Else: raise ValueError

Constraints:
- Don't mutate input records
- Type hints and docstrings

Also create /tests/day2/test_redaction.py:
- Test redact_fields: PII removed, safe fields remain
- Test allowlist_fields: only safe fields remain
- Test redact_or_allowlist: both modes

Verification:
pytest tests/day2/test_redaction.py -v

STOP after completing redaction.py and tests.
```

### Prompt L4-5: Implement Audit Logging

```text
Create /src/day2/pii_protection/audit.py for audit logging.

Use JSONL format (one JSON object per line) for append-friendly logging.

Implement:

1. AuditEntry (Pydantic model or dataclass):
   - timestamp: datetime (ISO format)
   - request_id: str (unique per operation, e.g., UUID)
   - operation: Literal["MASK", "TOKENIZE", "REDACT"]
   - input_file: str (filename only, no full path)
   - output_file: str
   - fields_processed: List[str] (field names, NOT values)
   - record_count: int
   - mode_config: dict (e.g., {"salt_used": True, "version": "1.0"})
   - user: str (placeholder: "SYSTEM" or env var USER)

2. write_audit_entry(entry: AuditEntry, log_path: Path) -> None
   - Append entry as JSON line to log_path
   - Create file if not exists
   - Use append mode ("a")

3. read_audit_log(log_path: Path) -> List[AuditEntry]
   - Read all entries from JSONL file
   - Parse into AuditEntry objects
   - Return list

4. generate_audit_summary(log_path: Path) -> dict
   - Count operations by type
   - Count records processed
   - List unique input files
   - Return summary dict

Constraints:
- CRITICAL: Do NOT log raw PII values (log field names only)
- Include request_id for tracing
- Timestamp in ISO format
- Type hints and docstrings

Also create /tests/day2/test_audit.py:
- Test write_audit_entry: creates JSONL file
- Test read_audit_log: parses entries correctly
- Test generate_audit_summary: aggregates correctly
- Test NO PII in logs: verify no sensitive values written

Verification:
pytest tests/day2/test_audit.py -v

STOP after completing audit.py and tests.
```

### Prompt L4-6: Create CLI Orchestrator

```text
Create /src/day2/pii_protection/cli.py as the CLI entrypoint.

Use argparse.

CLI interface:
python -m src.day2.pii_protection.cli --mode <MASK|TOKENIZE|REDACT> --input <csv_path> --output <csv_path>

Arguments:
- --mode: MASK, TOKENIZE, or REDACT (required)
- --input: input CSV file (required)
- --output: output CSV file (default: out/day2/lab4/protected_data.csv)
- --audit-log: audit log file (default: out/day2/lab4/audit_log.jsonl)

Behavior:
1. Load config (secret salt from env or default)
2. Read input CSV into list of dicts
3. For each record:
   - If mode=MASK: apply masking.mask_field to all pii_fields
   - If mode=TOKENIZE: apply tokenization.tokenize_field to all pii_fields
   - If mode=REDACT: apply redaction.allowlist_fields with safe_fields
4. Write protected records to output CSV
5. Write audit entry to log
6. Print summary:
   - "Protected X records"
   - "Mode: {mode}"
   - "Output: {output_path}"
   - "Audit log: {audit_log_path}"

Constraints:
- Generate unique request_id per run (use uuid.uuid4())
- Handle errors gracefully
- Type hints and docstrings

Also create /src/day2/pii_protection/__init__.py (can be empty)

Manual test:
python -m src.day2.pii_protection.cli --mode MASK --input src/samples/sample_customer_pii.csv --output out/day2/lab4/masked.csv

STOP after creating cli.py.
```

---

## General-Purpose Prompts

### Explain Existing Code

```text
Explain the following code in banking/compliance terms:

[Paste code here]

Explain:
- What business problem does this solve?
- What are the key logic steps?
- What are potential edge cases or failure modes?
- What would an auditor want to verify about this code?
```

### Generate Tests for Existing Code

```text
Generate pytest tests for the following function:

[Paste function here]

Requirements:
- Test happy path (valid inputs)
- Test edge cases (empty, None, boundary values)
- Test error cases (invalid inputs, exceptions)
- Use descriptive test names
- Add docstrings explaining what each test verifies
```

### Add Type Hints and Docstrings

```text
Add comprehensive type hints and docstrings to the following code:

[Paste code here]

Requirements:
- Type hints on all function parameters and return values
- Docstrings in Google or NumPy style
- Include parameter descriptions, return value descriptions, and examples
- Note any exceptions that might be raised
```

### Review Code for Security Issues

```text
Review the following code for security and data protection issues:

[Paste code here]

Check for:
- PII exposure (logging, error messages, outputs)
- Secrets in code (hardcoded passwords, tokens, keys)
- Injection vulnerabilities (SQL, command injection)
- Insecure defaults
- Missing input validation

Provide specific recommendations for each issue found.
```

### Generate Sample Data

```text
Generate synthetic sample data for testing.

Requirements:
- Format: CSV
- Fields: [list fields]
- Number of rows: [X]
- Constraints:
  - All data must be synthetic (no real customer info)
  - Include edge cases: [describe]
  - Deterministic (no randomness)
  - Include examples that trigger specific logic: [describe]

Output the CSV content directly (no code, just the CSV text).
```

---

## Tips for Writing Effective Prompts

### ✅ Do:
- **Be specific** about file paths, module names, function signatures
- **Include acceptance criteria** and verification commands
- **Use STOP points** for incremental review
- **Specify constraints** (no MCP, deterministic, type hints, etc.)
- **Request tests** alongside implementation
- **Provide context** about the business domain (banking, compliance)

### ❌ Don't:
- Write vague prompts like "implement an AML system" (too broad)
- Skip verification commands (how will you know it works?)
- Ask for everything at once (break into steps)
- Forget to specify test requirements
- Omit constraints (agent will make assumptions)

---

## Example of a Well-Structured Prompt

```text
You are a GitHub Copilot coding agent.

[GOAL]
Create /path/to/module.py that implements [specific functionality].

[REQUIREMENTS]
1. [Specific requirement 1]
2. [Specific requirement 2]
3. [Specific requirement 3]

[CONSTRAINTS]
- No MCP
- Deterministic (no randomness)
- Type hints on all functions
- Docstrings in Google style
- Pure functions where possible

[TESTS]
Create /path/to/test_module.py with pytest tests:
- Test [scenario 1]
- Test [scenario 2]
- Test [edge case]

[VERIFICATION]
pytest /path/to/test_module.py -v

[STOP POINT]
STOP after creating module.py and test_module.py. Wait for my verification before proceeding.
```

---

## Using These Prompts

1. **Copy the prompt** you need from this document
2. **Customize placeholders** (e.g., `<module_name>`, file paths)
3. **Paste into Copilot Agent Mode** in VS Code
4. **Review the agent's output** before accepting
5. **Run verification commands** (tests, CLI runs)
6. **Commit working state** before proceeding to next step

**Remember:** Agent Mode is powerful but requires your oversight. Always verify outputs, run tests, and maintain control via stop points.
