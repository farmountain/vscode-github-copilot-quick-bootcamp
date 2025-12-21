# Data Quality Rules Engine

A deterministic transaction validation system that checks banking transaction data for completeness, format correctness, and range violations.

## Overview

This engine validates transaction data against three categories of rules:

1. **Completeness Rules** (HIGH severity): Check for missing required fields
2. **Format Rules** (HIGH/MEDIUM severity): Validate data formats and types
3. **Range Rules** (MEDIUM/LOW severity): Check for out-of-range or suspicious values

## Architecture

```
src/day1/data_quality/
├── __init__.py           # Package initialization
├── schemas.py            # Pydantic models (Transaction, ValidationIssue, ValidationReport)
├── rules.py              # Validation rule implementations
├── validator.py          # Main validation orchestrator
└── cli.py                # Command-line interface
```

## Validation Rules

### Completeness Rules (HIGH Severity)
- **account_id**: Must be present
- **amount**: Must be present
- **currency**: Must be present
- **timestamp**: Must be present

### Format Rules (HIGH/MEDIUM/LOW Severity)
- **amount**: Must be valid decimal, cannot be negative (HIGH), zero amounts flagged (MEDIUM)
- **currency**: Must be 3-letter code from valid list: USD, EUR, GBP, JPY, CAD, AUD, CHF (MEDIUM)
- **timestamp**: Must be valid ISO 8601 format (HIGH)
- **category**: Must be from valid list if present: dining, shopping, transport, automotive, groceries, travel, entertainment, healthcare (LOW)

### Range Rules (MEDIUM/LOW Severity)
- **amount**: Must not exceed 100,000 (MEDIUM)
- **account_id**: Must start with "ACC" followed by digits (MEDIUM)
- **merchant_name**: Should be present (LOW)

## Usage

### Command Line

```powershell
# Validate transactions
python -m src.day1.data_quality.cli --input src/samples/sample_transactions.csv --output out/day1/lab1/validation_report.json
```

### Python API

```python
from pathlib import Path
from src.day1.data_quality.validator import run_validation

report = run_validation(
    input_csv=Path("src/samples/sample_transactions.csv"),
    output_json=Path("out/day1/lab1/validation_report.json")
)

print(f"Valid: {report.valid_transactions}/{report.total_transactions}")
```

## Output Format

The validation report is a JSON file with the following structure:

```json
{
  "total_transactions": 15,
  "valid_transactions": 8,
  "invalid_transactions": 7,
  "issues": [
    {
      "transaction_id": "TX006",
      "field": "account_id",
      "rule": "completeness",
      "severity": "HIGH",
      "message": "Account ID is required",
      "value": "null"
    }
  ],
  "issues_by_severity": {
    "HIGH": 5,
    "MEDIUM": 3,
    "LOW": 2
  },
  "issues_by_rule": {
    "completeness": 4,
    "format": 4,
    "range": 2
  },
  "timestamp": "2024-01-15T10:00:00"
}
```

## Testing

```powershell
# Run all tests
pytest tests/day1/test_data_quality*.py -v

# Run with coverage
pytest tests/day1/test_data_quality*.py --cov=src.day1.data_quality --cov-report=term-missing
```

## Determinism Guarantees

The validation engine is fully deterministic:
- Same input CSV always produces identical validation results
- Issue detection order is consistent
- No random or time-dependent logic (except for report timestamp)
- Ideal for regression testing and CI/CD pipelines

## Sample Data

The included [sample_transactions.csv](../../../src/samples/sample_transactions.csv) contains 15 synthetic transactions with various validation issues:

- Missing account IDs
- Negative amounts
- Invalid currencies
- Invalid timestamps
- Missing merchant names
- Out-of-range amounts

## Extension Points

To add new validation rules:

1. Add rule function to [rules.py](rules.py)
2. Call from `validate_transaction()` function
3. Return list of `ValidationIssue` objects
4. Add tests in `tests/day1/test_data_quality_rules.py`
