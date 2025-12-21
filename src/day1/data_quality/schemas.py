"""Data schemas for transaction validation."""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class Severity(str, Enum):
    """Issue severity levels."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Transaction(BaseModel):
    """Transaction record."""
    transaction_id: str
    account_id: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    timestamp: Optional[str] = None
    merchant_name: Optional[str] = None
    category: Optional[str] = None


class ValidationIssue(BaseModel):
    """Data quality validation issue."""
    transaction_id: str
    field: str
    rule: str
    severity: Severity
    message: str
    value: Optional[str] = None


class ValidationReport(BaseModel):
    """Aggregated validation report."""
    total_transactions: int
    valid_transactions: int
    invalid_transactions: int
    issues: List[ValidationIssue]
    issues_by_severity: dict
    issues_by_rule: dict
    timestamp: datetime = Field(default_factory=datetime.now)
