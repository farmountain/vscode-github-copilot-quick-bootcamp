# AML Alert Triage Pipeline

A deterministic alert triage system for Anti-Money Laundering (AML) transaction monitoring.

## Overview

This pipeline processes financial transactions and generates prioritized alerts based on AML heuristic rules. It's designed for banking environments where deterministic, auditable, and explainable results are critical.

**Key Features:**
- Deterministic rule-based detection (no ML, no randomness)
- Audit-friendly outputs with reason codes and explanations
- Priority-based triage (P1/P2/P3)
- Synthetic data only (no real customer information)

## Architecture

```
Input: CSV transactions
  ↓
[Rules Engine] → Applies AML heuristic rules
  ↓
[Alert Generator] → Creates alerts with reason codes
  ↓
[Triage Scorer] → Assigns priority (P1/P2/P3)
  ↓
Outputs: JSON alerts, CSV queue, summary stats
```

### Modules

- **`schemas.py`**: Pydantic models (Transaction, Alert, TriageDecision, ReasonCode)
- **`rules.py`**: AML heuristic rule functions
- **`triage.py`**: Priority scoring and queue assignment
- **`io.py`**: Input/output handlers (CSV/JSON)
- **`pipeline.py`**: End-to-end orchestration
- **`cli.py`**: Command-line interface

## AML Rules

### 1. HIGH_VELOCITY
Detects 3+ transactions for the same account within 60 seconds.

**Risk:** Potential structuring behavior (breaking large transactions into smaller ones to avoid reporting thresholds).

**Score:** +50 points

### 2. ROUND_AMOUNT
Detects amounts divisible by 100 (e.g., 5000.00, 10000.00).

**Risk:** Round amounts can indicate structured transactions designed to avoid detection.

**Score:** +20 points

### 3. HIGH_AMOUNT
Detects transactions >= $10,000.

**Risk:** High-value transactions require additional scrutiny for AML compliance.

**Score:** +30 points

### 4. RAPID_REVERSAL
Detects debit followed by matching credit to same beneficiary within 5 minutes.

**Risk:** Testing of stolen credentials or creating confusion in monitoring systems.

**Score:** +40 points

### 5. NEW_BENEFICIARY (Future)
Detects first transaction to a new beneficiary for an account.

**Risk:** Unusual recipient patterns can indicate account takeover or fraud.

**Score:** +25 points

## Triage Priority

Alerts are assigned priority based on total score:

- **P1 (Critical):** Score >= 70 → HIGH_RISK queue
- **P2 (High):** Score >= 40 and < 70 → MEDIUM_RISK queue
- **P3 (Medium):** Score < 40 → LOW_RISK queue

Multiple rules stack additively (e.g., HIGH_VELOCITY + ROUND_AMOUNT = 70 points = P1).

## Installation

### Requirements

```bash
pip install pydantic
```

### Setup

```bash
# From repository root
cd vscode-github-copilot-quick-bootcamp

# Verify sample data exists
ls src/samples/sample_transactions_day2.csv
```

## Usage

### Command-Line Interface

```bash
python -m src.day2.aml_triage.cli \
    --input src/samples/sample_transactions_day2.csv \
    --outdir out/day2/lab3
```

**Arguments:**
- `--input`: Path to input CSV file (required)
- `--outdir`: Output directory for results (default: `out/day2/lab3`)

### Sample Run

```bash
$ python -m src.day2.aml_triage.cli --input src/samples/sample_transactions_day2.csv --outdir out/day2/lab3

AML Alert Triage Pipeline
==================================================
Input file: src/samples/sample_transactions_day2.csv
Output directory: out/day2/lab3

✓ Pipeline completed successfully!

Processed 20 transactions
Generated 8 alerts

Priority breakdown:
  P1 (Critical): 4
  P2 (High):     3
  P3 (Medium):   1

Outputs written to: out/day2/lab3/
  - aml_alerts.json
  - triage_queue.csv
  - summary.json
```

## Outputs

### 1. `aml_alerts.json`

JSON array of alerts with full details:

```json
[
  {
    "alert_id": "ALERT-TX001",
    "transaction": {
      "transaction_id": "TX001",
      "account_id": "ACC001",
      "timestamp": "2024-01-15T10:00:00Z",
      "amount": "5000.00",
      "transaction_type": "DEBIT",
      "beneficiary_id": "BEN123"
    },
    "reason_codes": ["HIGH_VELOCITY", "ROUND_AMOUNT"],
    "explanation": "High velocity: 4 transactions detected within 60 seconds; Round amount: Transaction amount 5000.00 is a round number",
    "timestamp_detected": "2024-12-21T15:30:00Z"
  }
]
```

### 2. `triage_queue.csv`

Analyst-friendly queue sorted by priority (highest first):

```csv
alert_id,account_id,amount,priority,triage_score,reason_codes,queue
ALERT-TX001,ACC001,5000.00,P1,70.0,HIGH_VELOCITY,ROUND_AMOUNT,HIGH_RISK
ALERT-TX005,ACC002,15000.00,P2,50.0,HIGH_AMOUNT,ROUND_AMOUNT,MEDIUM_RISK
...
```

### 3. `summary.json`

Statistical summary:

```json
{
  "total_alerts": 8,
  "by_priority": {
    "P1": 4,
    "P2": 3,
    "P3": 1
  },
  "by_reason_code": {
    "HIGH_VELOCITY": 5,
    "ROUND_AMOUNT": 6,
    "HIGH_AMOUNT": 3,
    "RAPID_REVERSAL": 2
  },
  "by_queue": {
    "HIGH_RISK": 4,
    "MEDIUM_RISK": 3,
    "LOW_RISK": 1
  }
}
```

## Testing

### Run All Tests

```bash
pytest tests/day2/ -v
```

### Run Specific Test Modules

```bash
# Test schemas
pytest tests/day2/test_schemas.py -v

# Test AML rules
pytest tests/day2/test_aml_rules.py -v

# Test triage scoring
pytest tests/day2/test_triage_scoring.py -v

# Test I/O handlers
pytest tests/day2/test_io.py -v

# Test end-to-end pipeline
pytest tests/day2/test_pipeline_end_to_end.py -v
```

### Test Coverage

```bash
pytest tests/day2/ --cov=src.day2.aml_triage --cov-report=term-missing
```

## Determinism Guarantees

For audit and compliance purposes, this pipeline is **fully deterministic**:

1. **Same input always produces same output**
   - No randomness (no `random`, no UUIDs in alert logic)
   - Stable sorting (by timestamp, then alert_id)
   - Fixed thresholds (no dynamic adjustments)

2. **Verification:**
   ```bash
   # Run twice and compare
   python -m src.day2.aml_triage.cli --input sample.csv --outdir run1
   python -m src.day2.aml_triage.cli --input sample.csv --outdir run2
   diff run1/aml_alerts.json run2/aml_alerts.json
   # Should show no differences (except timestamp_detected)
   ```

3. **Audit Trail:**
   - Every alert includes reason codes
   - Explanations trace back to specific rules
   - Transactions retained in alert objects
   - Priority assignment is transparent and rule-based

## Limitations & Production Considerations

**This is a training/demonstration system. NOT production-ready.**

### Limitations

- **Synthetic data only**: No real customer data, no PII
- **Simple heuristics**: Real AML systems use ML, network analysis, behavioral models
- **No persistence**: Results written to files, not a database
- **No real-time processing**: Batch processing only
- **No case management**: No workflow for analyst review/disposition
- **No regulatory reporting**: No SAR (Suspicious Activity Report) generation

### For Production

1. **Data Security:**
   - Encrypt data at rest and in transit
   - Use secrets management (Azure Key Vault, AWS Secrets Manager)
   - Implement access controls (RBAC)
   - Audit all data access

2. **Scalability:**
   - Use distributed processing (Spark, Dask)
   - Stream processing for real-time alerts (Kafka, Event Hubs)
   - Database persistence (PostgreSQL, Cosmos DB)

3. **Compliance:**
   - Regulatory reporting (SAR, CTR)
   - Case management workflows
   - Alert disposition tracking
   - Audit log retention (7+ years)

4. **Advanced Detection:**
   - Machine learning models
   - Network analysis (beneficiary graphs)
   - Behavioral baselines
   - External data enrichment (sanctions lists, PEP databases)

5. **Monitoring:**
   - Model performance tracking
   - False positive/negative rates
   - Alert resolution times
   - System uptime/SLAs

## Design Notes

### After Refactor (Session 2.2)

This codebase demonstrates clean separation of concerns:

- **Schemas:** Type-safe data models with validation
- **Rules:** Pure functions, easily testable in isolation
- **Triage:** Scoring logic separated from rule logic
- **I/O:** Input/output handling decoupled from business logic
- **Pipeline:** Thin orchestration layer

**Benefits:**
- Easy to add new rules (extend `rules.py`)
- Easy to adjust scoring (modify `triage.py`)
- Easy to test (each module has focused unit tests)
- Easy to understand (each file has single responsibility)

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError: No module named 'src'`:

```bash
# Ensure you're running from repository root
cd vscode-github-copilot-quick-bootcamp

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Pydantic Version Issues

This code uses Pydantic v2 syntax. If using Pydantic v1:

```bash
pip install --upgrade pydantic
```

### CSV Parsing Errors

Ensure CSV has correct format:
- Header row: `transaction_id,account_id,timestamp,amount,transaction_type,beneficiary_id,currency`
- Timestamps in ISO format: `2024-01-15T10:00:00Z`
- No missing fields

## Contributing

When adding new rules:

1. Define new `ReasonCode` in `schemas.py`
2. Implement rule function in `rules.py`
3. Add scoring in `triage.py` (`compute_triage_score`)
4. Update explanation in `rules.get_explanation()`
5. Write tests in `tests/day2/test_aml_rules.py`

## License

This is training material for internal use. Not licensed for external distribution.

## Support

For questions or issues:
- Review [Lab 3 instructions](../../day2_agent_workflows/labs/lab3_aml_alert_triage_pipeline.md)
- Check [Day 2 prompts document](../../day2_agent_workflows/prompts/day2_prompts.md)
- Ask your trainer or post in training Slack channel

---

**Built with GitHub Copilot Agent Mode for Day 2 Lab 3**
