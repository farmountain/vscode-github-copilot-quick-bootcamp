# Lab 4 — PII Masking/Tokenization + Audit Logging

**Duration:** 15:45–17:15 (90 minutes)  
**Difficulty:** Intermediate  
**Prerequisites:** Day 2 Session 2.1 complete, understanding of data protection principles

---

## Business Context

You work in the **Data Governance** team at a bank. Development and QA teams need access to customer data for testing and debugging, but exposing real PII (Personally Identifiable Information) violates data protection regulations (GDPR, CCPA, PCI-DSS, etc.).

**Your mission:** Build a **PII Protection Library** that:
1. Masks or tokenizes sensitive fields in customer data
2. Provides deterministic tokenization (same input → same token) for referential integrity
3. Maintains an audit log of protection operations WITHOUT storing raw PII
4. Enables safe data sharing with minimal exposure principle

**Why this matters:**
- Compliance: avoid PII breaches in dev/test environments
- Auditability: track who accessed/protected data and when
- Reversibility controls: tokens can be reversed only with proper authorization
- Demonstrable best practices: show auditors you handle data responsibly

---

## Learning Objectives

By completing this lab, you will:

1. **Implement masking functions** for common PII types (email, phone, national ID)
2. **Implement deterministic tokenization** using HMAC/hashing with secret salt
3. **Design audit logs** that capture operations WITHOUT storing sensitive data
4. **Apply "least data exposure" principle** (minimize PII in outputs)
5. **Use Agent Mode** to build modular, testable data protection code

---

## Architecture Overview

```
Input: sample_customer_pii.csv
  ↓
[Mode Selection] → MASK | TOKENIZE | REDACT
  ↓
[Protection Engine] → applies transformations to PII fields
  ↓
[Audit Logger] → records operation metadata (NO raw PII)
  ↓
Outputs: protected_data.csv + audit_log.jsonl
```

**Modules you'll create:**
- `config.py` — Settings (mode, salt placeholder, field mappings)
- `masking.py` — Masking functions (partial obfuscation)
- `tokenization.py` — Deterministic token generation (HMAC-based)
- `redaction.py` — Field allowlisting and full removal
- `audit.py` — Audit logging (JSONL format)
- `cli.py` — CLI entrypoint

---

## Setup

### 1. Create Project Structure

```bash
cd d:\All_Projects\vscode-github-copilot-quick-bootcamp

# Create directories
mkdir -p src/day2/pii_protection
mkdir -p tests/day2
mkdir -p out/day2/lab4
```

### 2. Establish Baseline (Git)

```bash
git status
git checkout -b day2-lab4
# Or commit existing work
```

### 3. Create Sample PII Data

**Create `/src/samples/sample_customer_pii.csv`:**

```csv
customer_id,full_name,email,phone,national_id,address,date_of_birth,segment,account_balance
CUST001,John Smith,john.smith@example.com,+1-555-123-4567,SSN-123-45-6789,"123 Main St, New York, NY 10001",1980-05-15,PREMIUM,125000.50
CUST002,Jane Doe,jane.doe@example.com,+1-555-987-6543,SSN-987-65-4321,"456 Oak Ave, Los Angeles, CA 90001",1992-11-23,STANDARD,45000.00
CUST003,Robert Johnson,rjohnson@example.com,+1-555-246-8135,SSN-246-81-3579,"789 Pine Rd, Chicago, IL 60601",1975-03-08,VIP,500000.00
CUST004,Emily Davis,emily.d@example.com,+1-555-369-2580,SSN-369-25-8014,"321 Elm St, Houston, TX 77001",1988-07-19,STANDARD,78000.25
CUST005,Michael Brown,mbrown@example.com,+1-555-159-7531,SSN-159-75-3186,"654 Maple Dr, Phoenix, AZ 85001",1995-12-30,PREMIUM,215000.00
```

---

## Task Breakdown

### Task 1: Define Configuration (10 minutes)

**Goal:** Centralize settings for protection modes, thresholds, and field mappings.

**Agent Prompt:**
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

**Your actions:**
```bash
# Review config.py:
cat src/day2/pii_protection/config.py

git add src/day2/pii_protection/config.py
git commit -m "Add configuration for PII protection modes"
```

---

### Task 2: Implement Masking Functions (20 minutes)

**Goal:** Partial obfuscation functions for common PII types.

**Agent Prompt:**
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

**Your actions:**
```bash
pytest tests/day2/test_masking.py -v

git add src/day2/pii_protection/masking.py tests/day2/test_masking.py
git commit -m "Implement PII masking functions with tests"
```

---

### Task 3: Implement Tokenization (25 minutes)

**Goal:** Deterministic, reversible token generation using HMAC.

**Agent Prompt:**
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
   - For emails: tokenize username and domain separately (optional advanced feature)
   - For now: tokenize entire value

3. verify_token_determinism(value: str, token: str, field_name: str, secret_salt: str) -> bool
   - Re-generate token and compare
   - Used for testing reversibility logic (not for production reversal)

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

**Your actions:**
```bash
pytest tests/day2/test_tokenization.py -v

git add src/day2/pii_protection/tokenization.py tests/day2/test_tokenization.py
git commit -m "Implement deterministic tokenization with tests"
```

---

### Task 4: Implement Redaction (15 minutes)

**Goal:** Allowlist safe fields and drop sensitive ones entirely.

**Agent Prompt:**
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

**Your actions:**
```bash
pytest tests/day2/test_redaction.py -v

git add src/day2/pii_protection/redaction.py tests/day2/test_redaction.py
git commit -m "Implement field redaction/allowlisting with tests"
```

---

### Task 5: Implement Audit Logging (20 minutes)

**Goal:** Log protection operations WITHOUT storing raw PII.

**Agent Prompt:**
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

**Your actions:**
```bash
pytest tests/day2/test_audit.py -v

git add src/day2/pii_protection/audit.py tests/day2/test_audit.py
git commit -m "Implement audit logging (no PII stored) with tests"
```

---

### Task 6: Build CLI Orchestrator (15 minutes)

**Goal:** Tie everything together with a command-line interface.

**Agent Prompt:**
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
2. Read input CSV into list of dicts (use csv.DictReader or pandas)
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
- Handle errors gracefully (file not found, invalid mode)
- Type hints and docstrings

Also create /src/day2/pii_protection/__init__.py (can be empty)

Manual test (not automated pytest):
python -m src.day2.pii_protection.cli --mode MASK --input src/samples/sample_customer_pii.csv --output out/day2/lab4/masked.csv

Verify:
- out/day2/lab4/masked.csv contains masked data
- out/day2/lab4/audit_log.jsonl contains audit entry
- No raw PII in audit log

STOP after creating cli.py.
```

**Your actions:**
```bash
# Test MASK mode:
python -m src.day2.pii_protection.cli --mode MASK --input src/samples/sample_customer_pii.csv --output out/day2/lab4/masked.csv

# Check output:
head out/day2/lab4/masked.csv
cat out/day2/lab4/audit_log.jsonl

# Test TOKENIZE mode:
python -m src.day2.pii_protection.cli --mode TOKENIZE --input src/samples/sample_customer_pii.csv --output out/day2/lab4/tokenized.csv

# Check audit log (should have 2 entries now):
cat out/day2/lab4/audit_log.jsonl

git add src/day2/pii_protection/cli.py src/day2/pii_protection/__init__.py
git commit -m "Add CLI orchestrator for PII protection"
```

---

### Task 7: Documentation and README (10 minutes)

**Agent Prompt:**
```text
Create /src/day2/pii_protection/README.md documenting the PII protection library.

Include:

1. Overview (purpose, use cases)
2. Architecture (modules and responsibilities)
3. Protection modes:
   - MASK: partial obfuscation (examples)
   - TOKENIZE: deterministic tokens (examples)
   - REDACT: field removal (examples)
4. Usage examples:
   - CLI commands for each mode
   - Before/after examples (synthetic data)
5. Audit logging:
   - What's logged (fields processed, counts, timestamps)
   - What's NOT logged (raw PII values)
   - How to review audit logs
6. Security considerations:
   - NOT production-ready (training only)
   - Secret salt management (use env vars, never hardcode)
   - Tokens are not encryption
   - Recommend Azure Key Vault / HashiCorp Vault for real tokenization
7. Compliance notes:
   - Demonstrates "data minimization" principle (GDPR)
   - Shows audit trail for data access (required by many regulations)
   - Explains reversibility controls (tokenization with vault)

Format: Clear sections, code blocks, warnings for production use.

STOP after creating README.md.
```

**Your actions:**
```bash
cat src/day2/pii_protection/README.md

git add src/day2/pii_protection/README.md
git commit -m "Add documentation for PII protection library"
```

---

## Acceptance Criteria

### Functional Requirements

✅ **MASK mode works correctly**
- All PII fields partially obfuscated
- Safe fields remain unchanged
- Human-readable format preserved

✅ **TOKENIZE mode is deterministic**
- Same input + same salt = same token
- Different inputs = different tokens
- Tokens have consistent format

✅ **REDACT mode removes sensitive fields**
- PII fields not in output
- Safe fields remain
- No data leakage

✅ **Audit logging captures operations**
- Each run logged with timestamp, mode, field names, counts
- NO raw PII values in logs
- Audit log is append-only (JSONL)

✅ **CLI works end-to-end**
- Can run all three modes
- Outputs written correctly
- User-friendly messages

### Testing Requirements

✅ **Unit tests for all modules**
- masking, tokenization, redaction, audit
- All tests pass: `pytest tests/day2/ -v`

✅ **Edge case handling**
- Empty inputs, malformed data, missing fields
- No crashes, graceful error messages

### Security Requirements

✅ **No PII in audit logs**
- Verified by test: test_no_pii_in_audit_logs
- Manual inspection of audit_log.jsonl

✅ **Secret salt not hardcoded**
- Loaded from environment variable or safe default
- Warning in code about production secrets management

✅ **Minimal data exposure**
- REDACT mode shows only safe fields
- MASK mode preserves minimal necessary info

---

## Verification Commands

```bash
# Run all tests
pytest tests/day2/ -k pii -v

# Test MASK mode
python -m src.day2.pii_protection.cli --mode MASK --input src/samples/sample_customer_pii.csv --output out/day2/lab4/masked.csv
head out/day2/lab4/masked.csv

# Test TOKENIZE mode
python -m src.day2.pii_protection.cli --mode TOKENIZE --input src/samples/sample_customer_pii.csv --output out/day2/lab4/tokenized.csv
head out/day2/lab4/tokenized.csv

# Test REDACT mode
python -m src.day2.pii_protection.cli --mode REDACT --input src/samples/sample_customer_pii.csv --output out/day2/lab4/redacted.csv
head out/day2/lab4/redacted.csv

# Check audit log (NO PII should appear)
cat out/day2/lab4/audit_log.jsonl | grep -i "john" || echo "No PII found (good!)"

# Test determinism (tokenization)
python -m src.day2.pii_protection.cli --mode TOKENIZE --input src/samples/sample_customer_pii.csv --output out/day2/lab4/tokenized1.csv
python -m src.day2.pii_protection.cli --mode TOKENIZE --input src/samples/sample_customer_pii.csv --output out/day2/lab4/tokenized2.csv
diff out/day2/lab4/tokenized1.csv out/day2/lab4/tokenized2.csv
# Should show no differences
```

---

## Auditor's Lens: Evidence to Retain

Auditors and compliance officers will look for:

✅ **Data minimization principle** — Do you expose only necessary data?  
✅ **Access logging** — Can you show who accessed/protected data and when?  
✅ **Reversibility controls** — For tokenization, how do you control de-tokenization?  
✅ **Secure storage** — Where are secret salts stored? (Should be secrets manager, not code)  
✅ **Testing coverage** — Have you tested edge cases and verified no PII leakage?  
✅ **Documentation** — Is protection logic documented for audit review?

**In this lab, you've demonstrated:**
- ✅ MASK/REDACT minimize data exposure
- ✅ Audit log tracks operations (NO PII stored)
- ✅ Tokenization is deterministic (testable, reproducible)
- ✅ Warning comments about production secrets management
- ✅ Comprehensive tests including "no PII in logs" test
- ✅ README documents modes, security considerations, compliance notes

---

## Reflexion Questions

After completing the lab:

1. **Where could PII leak?** (Logs? Error messages? Temp files?)
2. **Is tokenization truly secure?** What are its limitations vs. encryption?
3. **How would you implement de-tokenization** with proper access controls?
4. **What additional audit metadata** would a real system need? (User ID, purpose, approval?)
5. **How would you test** that no PII appears in logs? (Automated scan?)
6. **What would change for production?** (Vault integration, key rotation, access policies)

---

## Extension Challenges (Optional)

If you finish early:

1. **Implement de-tokenization** with access control check (mock authorization)
2. **Add date-based pseudonymization** (e.g., shift dates by random but consistent offset)
3. **Create HTML report** showing before/after examples (synthetic data only)
4. **Add format-preserving encryption (FPE)** for credit card numbers using FF3-1 algorithm (via `ff3` library)
5. **Implement audit log rotation** (archive logs older than N days)

---

## Key Takeaways

1. **Data minimization is key:** Only expose what's necessary for the task.
2. **Audit without exposing:** Log operations, not sensitive values.
3. **Determinism enables testing:** Same input → same output → reproducible for audit.
4. **This is a pattern, not production code:** Real systems need vault services, key rotation, access policies.
5. **Agent Mode accelerates implementation** but YOU must verify security properties.

---

## Next Steps

After Day 2 labs:
- **Reflexion Retro (17:15–17:45):** Share learnings, discuss "what would audit want to see?"
- **Day 3 (optional):** MCP integration for enterprise workflows

---

**Need help?** Ask Copilot Chat:
```
How do I implement HMAC-based tokenization in Python securely?
```

or

```
What are best practices for audit logging in banking applications?
```
