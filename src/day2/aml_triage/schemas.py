"""Data models for AML Alert Triage Pipeline.

This module defines Pydantic models for type safety and validation.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Literal

from pydantic import BaseModel, Field, field_validator


class ReasonCode(str, Enum):
    """Enumeration of AML alert reason codes."""
    
    HIGH_VELOCITY = "HIGH_VELOCITY"
    ROUND_AMOUNT = "ROUND_AMOUNT"
    HIGH_AMOUNT = "HIGH_AMOUNT"
    RAPID_REVERSAL = "RAPID_REVERSAL"
    NEW_BENEFICIARY = "NEW_BENEFICIARY"


class Transaction(BaseModel):
    """Represents a single financial transaction.
    
    Example:
        transaction = Transaction(
            transaction_id="TX001",
            account_id="ACC001",
            timestamp="2024-01-15T10:00:00Z",
            amount="5000.00",
            transaction_type="DEBIT",
            beneficiary_id="BEN123",
            currency="USD"
        )
    """
    
    transaction_id: str
    account_id: str
    timestamp: datetime
    amount: Decimal
    transaction_type: Literal["DEBIT", "CREDIT"]
    beneficiary_id: str
    currency: str = "USD"
    
    @field_validator('timestamp', mode='before')
    @classmethod
    def parse_timestamp(cls, v):
        """Parse ISO format timestamp strings."""
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace('Z', '+00:00'))
        return v
    
    @field_validator('amount', mode='before')
    @classmethod
    def parse_amount(cls, v):
        """Parse amount as Decimal for precision."""
        if not isinstance(v, Decimal):
            return Decimal(str(v))
        return v


class Alert(BaseModel):
    """Represents an AML alert triggered by one or more rules.
    
    Example:
        alert = Alert(
            alert_id="ALERT-TX001",
            transaction=transaction_obj,
            reason_codes=[ReasonCode.HIGH_VELOCITY, ReasonCode.ROUND_AMOUNT],
            explanation="Multiple suspicious patterns detected",
            timestamp_detected=datetime.now()
        )
    """
    
    alert_id: str
    transaction: Transaction
    reason_codes: List[ReasonCode]
    explanation: str
    timestamp_detected: datetime


class TriageDecision(BaseModel):
    """Represents a triage decision for an alert.
    
    Example:
        decision = TriageDecision(
            alert=alert_obj,
            priority="P1",
            triage_score=80.0,
            assigned_queue="HIGH_RISK"
        )
    """
    
    alert: Alert
    priority: Literal["P1", "P2", "P3"]
    triage_score: float
    assigned_queue: str
