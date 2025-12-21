# PII Protection Library

A comprehensive library for masking, tokenizing, and redacting personally identifiable information (PII) with full audit logging.

## Overview

The PII Protection Library provides three protection modes:

1. **MASK**: Visual masking for display (e.g., `ab***@ex***.com`)
2. **TOKENIZE**: Deterministic token replacement (e.g., `TOKEN_A1B2C3D4E5F6`)
3. **REDACT**: Complete field removal

All operations are logged to an audit trail (without storing actual PII values).

## Architecture

```
src/day2/pii_protection/
├── __init__.py           # Package initialization
├── config.py             # Configuration models (ProtectionMode, Config)
├── masking.py            # Masking functions (mask_email, mask_phone, etc.)
├── tokenization.py       # Tokenization using HMAC-SHA256
├── redaction.py          # Field redaction/removal
├── audit.py              # Audit logging (JSONL format)
└── cli.py                # Command-line interface
```

## Protection Modes

### MASK Mode

Visual masking that preserves format while hiding sensitive data:

- **Email**: `john.doe@example.com` → `jo***@ex***.com`
- **Phone**: `555-123-4567` → `***-***-4567`
- **SSN**: `123-45-6789` → `***-**-6789`
- **Name**: `John Doe` → `J*** D***`
- **Address**: `123 Main St` → `*** *** ***`
- **DOB**: `1985-03-15` → `**/**/1985`

### TOKENIZE Mode

Deterministic tokenization using HMAC-SHA256:

- Same value + secret key always produces same token
- Different values produce different tokens
- Tokens are irreversible without secret key
- Format: `TOKEN_A1B2C3D4E5F6` (16 hex characters)

### REDACT Mode

Complete field removal:

- Fields are removed from output records
- Supports allowlist mode (keep only specified fields)

## Usage

### Command Line

```powershell
# Mask PII fields
python -m src.day2.pii_protection.cli `
  --input src/samples/sample_customer_pii.csv `
  --output out/day2/lab4/masked_data.csv `
  --mode MASK `
  --fields email,phone,ssn

# Tokenize PII fields
python -m src.day2.pii_protection.cli `
  --input src/samples/sample_customer_pii.csv `
  --output out/day2/lab4/tokenized_data.csv `
  --mode TOKENIZE `
  --fields email,phone,ssn `
  --secret-key your-secret-key

# Redact PII fields
python -m src.day2.pii_protection.cli `
  --input src/samples/sample_customer_pii.csv `
  --output out/day2/lab4/redacted_data.csv `
  --mode REDACT `
  --fields email,phone,ssn,address,date_of_birth
```

### Python API

```python
from src.day2.pii_protection.masking import mask_email, mask_phone
from src.day2.pii_protection.tokenization import tokenize_field
from src.day2.pii_protection.redaction import redact_fields

# Masking
masked_email = mask_email("john.doe@example.com")
# Result: "jo***@ex***.com"

masked_phone = mask_phone("555-123-4567")
# Result: "***-***-4567"

# Tokenization
token = tokenize_field("email", "john.doe@example.com", "secret-key")
# Result: "TOKEN_A1B2C3D4E5F6"

# Redaction
record = {"customer_id": "CUST001", "email": "john@example.com", "name": "John"}
redacted = redact_fields(record, {"email"})
# Result: {"customer_id": "CUST001", "name": "John"}
```

## Audit Logging

All protection operations are logged to a JSONL audit file:

```json
{"timestamp": "2024-01-15T10:00:00", "operation": "MASK", "record_id": "CUST001", "fields_protected": ["email", "phone"], "user": "system"}
{"timestamp": "2024-01-15T10:00:01", "operation": "TOKENIZE", "record_id": "CUST002", "fields_protected": ["ssn"], "user": "system"}
```

**CRITICAL**: Audit logs contain only metadata, never actual PII values.

### Audit Summary

```python
from pathlib import Path
from src.day2.pii_protection.audit import generate_audit_summary

summary = generate_audit_summary(Path("out/day2/lab4/audit.jsonl"))
print(f"Total operations: {summary['total_operations']}")
print(f"Unique records: {summary['unique_records']}")
print(f"Operations by type: {summary['operations_by_type']}")
```

## Testing

```powershell
# Run all tests
pytest tests/day2/test_masking.py tests/day2/test_tokenization.py tests/day2/test_audit.py -v

# Run with coverage
pytest tests/day2/test_*.py --cov=src.day2.pii_protection --cov-report=term-missing
```

## Security Considerations

1. **Secret Key**: Change default secret key in production
2. **Audit Logs**: Never log actual PII values
3. **Tokenization**: Use strong secret keys (min 32 characters)
4. **Access Control**: Restrict access to audit logs
5. **Data Retention**: Define audit log retention policies

## Determinism Guarantees

- **Masking**: Deterministic (same value → same masked value)
- **Tokenization**: Deterministic with same secret key
- **Redaction**: Deterministic (same fields removed)
- **Audit Logs**: Deterministic metadata (timestamp is only variable)

## Sample Data

The included [sample_customer_pii.csv](../../../src/samples/sample_customer_pii.csv) contains 5 synthetic customer records with:

- Customer IDs
- Full names
- Email addresses
- Phone numbers
- Social Security Numbers (SSNs)
- Dates of birth
- Street addresses

## Extension Points

To add new PII field types:

1. Add masking function to [masking.py](masking.py)
2. Update `mask_field()` to recognize new field types
3. Add tests in `tests/day2/test_masking.py`
