"""Tests for AML triage schemas."""

import pytest
from datetime import datetime
from decimal import Decimal

from src.day2.aml_triage.schemas import Transaction, Alert, ReasonCode, TriageDecision


def test_transaction_valid():
    """Test that valid transaction data parses correctly."""
    tx = Transaction(
        transaction_id="TX001",
        account_id="ACC001",
        timestamp="2024-01-15T10:00:00Z",
        amount="5000.00",
        transaction_type="DEBIT",
        beneficiary_id="BEN123",
        currency="USD"
    )
    
    assert tx.transaction_id == "TX001"
    assert tx.account_id == "ACC001"
    assert isinstance(tx.timestamp, datetime)
    assert tx.amount == Decimal("5000.00")
    assert tx.transaction_type == "DEBIT"
    assert tx.currency == "USD"


def test_transaction_invalid_type():
    """Test that invalid transaction type raises ValidationError."""
    with pytest.raises(Exception):  # Pydantic ValidationError
        Transaction(
            transaction_id="TX001",
            account_id="ACC001",
            timestamp="2024-01-15T10:00:00Z",
            amount="5000.00",
            transaction_type="INVALID",  # Not DEBIT or CREDIT
            beneficiary_id="BEN123"
        )


def test_transaction_amount_precision():
    """Test that amounts are stored as Decimal for precision."""
    tx = Transaction(
        transaction_id="TX001",
        account_id="ACC001",
        timestamp="2024-01-15T10:00:00Z",
        amount="123.456",
        transaction_type="DEBIT",
        beneficiary_id="BEN123"
    )
    
    assert isinstance(tx.amount, Decimal)
    assert tx.amount == Decimal("123.456")


def test_alert_creation():
    """Test Alert model creation."""
    tx = Transaction(
        transaction_id="TX001",
        account_id="ACC001",
        timestamp="2024-01-15T10:00:00Z",
        amount="5000.00",
        transaction_type="DEBIT",
        beneficiary_id="BEN123"
    )
    
    alert = Alert(
        alert_id="ALERT-TX001",
        transaction=tx,
        reason_codes=[ReasonCode.HIGH_VELOCITY, ReasonCode.ROUND_AMOUNT],
        explanation="Multiple suspicious patterns detected",
        timestamp_detected=datetime.now()
    )
    
    assert alert.alert_id == "ALERT-TX001"
    assert len(alert.reason_codes) == 2
    assert ReasonCode.HIGH_VELOCITY in alert.reason_codes


def test_triage_decision_creation():
    """Test TriageDecision model creation."""
    tx = Transaction(
        transaction_id="TX001",
        account_id="ACC001",
        timestamp="2024-01-15T10:00:00Z",
        amount="5000.00",
        transaction_type="DEBIT",
        beneficiary_id="BEN123"
    )
    
    alert = Alert(
        alert_id="ALERT-TX001",
        transaction=tx,
        reason_codes=[ReasonCode.HIGH_VELOCITY],
        explanation="High velocity detected",
        timestamp_detected=datetime.now()
    )
    
    decision = TriageDecision(
        alert=alert,
        priority="P1",
        triage_score=80.0,
        assigned_queue="HIGH_RISK"
    )
    
    assert decision.priority == "P1"
    assert decision.triage_score == 80.0
    assert decision.assigned_queue == "HIGH_RISK"
