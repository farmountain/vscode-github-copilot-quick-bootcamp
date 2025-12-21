# Risk Scoring Service

A credit risk assessment system that evaluates loan applications using a multi-factor scoring model.

## Overview

The Risk Scoring Service assesses credit risk by evaluating four key factors:

1. **Credit Score** (35% weight): Credit history quality
2. **Income** (25% weight): Annual income level
3. **Debt-to-Income Ratio** (30% weight): Monthly debt burden
4. **Employment** (10% weight): Employment stability

Each factor is scored 0-100, then weighted to produce a final risk score (0-100). The system determines risk level and makes lending decisions automatically.

## Architecture

```
src/day1/risk_scoring/
├── __init__.py           # Package initialization
├── models.py             # Pydantic models (CreditApplication, RiskScore, RiskFactor)
├── scoring_rules.py      # Individual risk factor scoring functions
├── risk_engine.py        # Risk assessment orchestrator
└── cli.py                # Command-line interface
```

## Risk Assessment Logic

### Scoring Rules

**Credit Score (35% weight)**
- 750+: 100 points (excellent)
- 700-749: 80 points (good)
- 650-699: 60 points (fair)
- 600-649: 40 points (poor)
- <600: 20 points (very poor)

**Income (25% weight)**
- $100k+: 100 points
- $75k-$99k: 80 points
- $50k-$74k: 60 points
- $30k-$49k: 40 points
- <$30k: 20 points

**Debt-to-Income Ratio (30% weight)**
- <20%: 100 points (excellent)
- 20-35%: 80 points (good)
- 36-43%: 60 points (acceptable)
- 44-50%: 40 points (risky)
- >50%: 20 points (very risky)

**Employment (10% weight)**
- Full-time 3+ years: 100 points
- Full-time 1-3 years: 80 points
- Full-time <1 year: 60 points
- Self-employed 3+ years: 70 points
- Self-employed <3 years: 50 points
- Part-time: 40 points
- Retired: 50 points
- Unemployed: 0 points

### Risk Level Classification

- **LOW risk**: Total score ≥ 70
- **MEDIUM risk**: Total score 50-69
- **HIGH risk**: Total score < 50

### Lending Decisions

- **LOW risk**: Automatically **APPROVED**
- **MEDIUM risk**:
  - If loan-to-income ratio < 0.5: **APPROVED**
  - Otherwise: **MANUAL_REVIEW**
- **HIGH risk**: Automatically **DECLINED**

## Usage

### Command Line

```powershell
# Assess credit applications
python -m src.day1.risk_scoring.cli --input src/samples/sample_credit_applications.json --output out/day1/lab2/risk_assessments.json
```

### Python API

```python
from pathlib import Path
from decimal import Decimal
from src.day1.risk_scoring.models import CreditApplication, EmploymentStatus
from src.day1.risk_scoring.risk_engine import assess_risk

app = CreditApplication(
    application_id="APP001",
    credit_score=720,
    annual_income=Decimal("75000"),
    monthly_debt_payments=Decimal("1200"),
    employment_status=EmploymentStatus.FULL_TIME,
    years_employed=Decimal("3"),
    requested_amount=Decimal("25000")
)

assessment = assess_risk(app)
print(f"Risk Score: {assessment.total_score}/100")
print(f"Risk Level: {assessment.risk_level.value}")
print(f"Decision: {assessment.decision.value}")
```

## Input Format

JSON array of credit applications:

```json
[
  {
    "application_id": "APP001",
    "credit_score": 780,
    "annual_income": 95000,
    "monthly_debt_payments": 1200,
    "employment_status": "FULL_TIME",
    "years_employed": 5.5,
    "requested_amount": 25000
  }
]
```

## Output Format

JSON array of risk assessments:

```json
[
  {
    "application_id": "APP001",
    "risk_factors": [
      {
        "factor": "credit_score",
        "score": 100,
        "weight": 0.35,
        "weighted_score": 35.0,
        "reason": "Excellent credit score"
      }
    ],
    "total_score": 88,
    "risk_level": "LOW",
    "decision": "APPROVED",
    "timestamp": "2024-01-15T10:00:00"
  }
]
```

## Testing

```powershell
# Run all tests
pytest tests/day1/test_risk*.py -v

# Run with coverage
pytest tests/day1/test_risk*.py --cov=src.day1.risk_scoring --cov-report=term-missing
```

## Determinism Guarantees

The risk scoring system is fully deterministic:
- Same application data always produces identical scores
- No random or time-dependent factors (except timestamp)
- Suitable for automated decisioning and audit trails

## Sample Data

The included [sample_credit_applications.json](../../../src/samples/sample_credit_applications.json) contains 8 synthetic applications covering various risk profiles:

- Excellent applicants (HIGH credit score, LOW DTI)
- Poor applicants (LOW credit score, HIGH DTI, unemployment)
- Medium risk applicants (mixed factors)

## Extension Points

To customize the risk model:

1. Adjust factor weights in [scoring_rules.py](scoring_rules.py)
2. Modify scoring thresholds in individual factor functions
3. Add new factors by creating new scoring functions
4. Update decision logic in [risk_engine.py](risk_engine.py)
