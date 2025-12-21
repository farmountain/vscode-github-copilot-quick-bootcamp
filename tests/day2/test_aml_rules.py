"""Tests for AML rule functions."""

import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from src.day2.aml_triage.schemas import Transaction, ReasonCode
from src.day2.aml_triage import rules


def create_transaction(tx_id, account_id, timestamp, amount, tx_type="DEBIT", beneficiary="BEN001"):
    """Helper to create test transactions."""
    return Transaction(
        transaction_id=tx_id,
        account_id=account_id,
        timestamp=timestamp,
        amount=Decimal(str(amount)),
        transaction_type=tx_type,
        beneficiary_id=beneficiary,
        currency="USD"
    )


class TestHighVelocity:
    """Tests for high velocity rule."""
    
    def test_high_velocity_triggers_with_4_transactions_in_30_seconds(self):
        """Test HIGH_VELOCITY triggers when 4 transactions occur in 30 seconds."""
        base_time = datetime(2024, 1, 15, 10, 0, 0)
        transactions = [
            create_transaction("TX1", "ACC001", base_time, 1000),
            create_transaction("TX2", "ACC001", base_time + timedelta(seconds=10), 1000),
            create_transaction("TX3", "ACC001", base_time + timedelta(seconds=20), 1000),
            create_transaction("TX4", "ACC001", base_time + timedelta(seconds=30), 1000),
        ]
        
        result = rules.check_high_velocity(transactions, "ACC001", window_seconds=60)
        assert result == ReasonCode.HIGH_VELOCITY
    
    def test_high_velocity_does_not_trigger_with_2_transactions(self):
        """Test HIGH_VELOCITY doesn't trigger with only 2 transactions."""
        base_time = datetime(2024, 1, 15, 10, 0, 0)
        transactions = [
            create_transaction("TX1", "ACC001", base_time, 1000),
            create_transaction("TX2", "ACC001", base_time + timedelta(seconds=10), 1000),
        ]
        
        result = rules.check_high_velocity(transactions, "ACC001", window_seconds=60)
        assert result is None
    
    def test_high_velocity_does_not_trigger_when_spread_out(self):
        """Test HIGH_VELOCITY doesn't trigger when transactions are spread out."""
        base_time = datetime(2024, 1, 15, 10, 0, 0)
        transactions = [
            create_transaction("TX1", "ACC001", base_time, 1000),
            create_transaction("TX2", "ACC001", base_time + timedelta(seconds=70), 1000),
            create_transaction("TX3", "ACC001", base_time + timedelta(seconds=140), 1000),
        ]
        
        result = rules.check_high_velocity(transactions, "ACC001", window_seconds=60)
        assert result is None


class TestRoundAmount:
    """Tests for round amount rule."""
    
    def test_round_amount_triggers_for_5000(self):
        """Test ROUND_AMOUNT triggers for 5000.00."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 5000.00)
        result = rules.check_round_amount(tx)
        assert result == ReasonCode.ROUND_AMOUNT
    
    def test_round_amount_triggers_for_10000(self):
        """Test ROUND_AMOUNT triggers for 10000.00."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 10000.00)
        result = rules.check_round_amount(tx)
        assert result == ReasonCode.ROUND_AMOUNT
    
    def test_round_amount_does_not_trigger_for_4999_99(self):
        """Test ROUND_AMOUNT doesn't trigger for 4999.99."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 4999.99)
        result = rules.check_round_amount(tx)
        assert result is None
    
    def test_round_amount_does_not_trigger_for_5001(self):
        """Test ROUND_AMOUNT doesn't trigger for 5001.00."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 5001.00)
        result = rules.check_round_amount(tx)
        assert result is None


class TestHighAmount:
    """Tests for high amount rule."""
    
    def test_high_amount_triggers_for_15000(self):
        """Test HIGH_AMOUNT triggers for 15000."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 15000)
        result = rules.check_high_amount(tx)
        assert result == ReasonCode.HIGH_AMOUNT
    
    def test_high_amount_triggers_at_threshold_10000(self):
        """Test HIGH_AMOUNT triggers at exactly 10000."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 10000)
        result = rules.check_high_amount(tx)
        assert result == ReasonCode.HIGH_AMOUNT
    
    def test_high_amount_does_not_trigger_for_9999(self):
        """Test HIGH_AMOUNT doesn't trigger for 9999."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 9999)
        result = rules.check_high_amount(tx)
        assert result is None
    
    def test_high_amount_custom_threshold(self):
        """Test HIGH_AMOUNT with custom threshold."""
        tx = create_transaction("TX1", "ACC001", datetime.now(), 5000)
        result = rules.check_high_amount(tx, threshold=Decimal("5000"))
        assert result == ReasonCode.HIGH_AMOUNT


class TestRapidReversal:
    """Tests for rapid reversal rule."""
    
    def test_rapid_reversal_triggers_for_debit_credit_pair(self):
        """Test RAPID_REVERSAL triggers for debit followed by credit."""
        base_time = datetime(2024, 1, 15, 10, 0, 0)
        transactions = [
            create_transaction("TX1", "ACC001", base_time, 3000, "DEBIT", "BEN123"),
            create_transaction("TX2", "ACC001", base_time + timedelta(seconds=120), 3000, "CREDIT", "BEN123"),
        ]
        
        result = rules.check_rapid_reversal(transactions, transactions[0], window_seconds=300)
        assert result == ReasonCode.RAPID_REVERSAL
    
    def test_rapid_reversal_does_not_trigger_for_credit(self):
        """Test RAPID_REVERSAL doesn't trigger if target is CREDIT."""
        base_time = datetime(2024, 1, 15, 10, 0, 0)
        transactions = [
            create_transaction("TX1", "ACC001", base_time, 3000, "CREDIT", "BEN123"),
            create_transaction("TX2", "ACC001", base_time + timedelta(seconds=120), 3000, "DEBIT", "BEN123"),
        ]
        
        result = rules.check_rapid_reversal(transactions, transactions[0], window_seconds=300)
        assert result is None
    
    def test_rapid_reversal_does_not_trigger_outside_window(self):
        """Test RAPID_REVERSAL doesn't trigger if reversal is outside time window."""
        base_time = datetime(2024, 1, 15, 10, 0, 0)
        transactions = [
            create_transaction("TX1", "ACC001", base_time, 3000, "DEBIT", "BEN123"),
            create_transaction("TX2", "ACC001", base_time + timedelta(seconds=400), 3000, "CREDIT", "BEN123"),
        ]
        
        result = rules.check_rapid_reversal(transactions, transactions[0], window_seconds=300)
        assert result is None


class TestGetExplanation:
    """Tests for explanation generation."""
    
    def test_get_explanation_high_velocity(self):
        """Test explanation for HIGH_VELOCITY."""
        explanation = rules.get_explanation(
            ReasonCode.HIGH_VELOCITY,
            {"count": 4, "window": 60}
        )
        assert "4 transactions" in explanation
        assert "60 seconds" in explanation
    
    def test_get_explanation_round_amount(self):
        """Test explanation for ROUND_AMOUNT."""
        explanation = rules.get_explanation(
            ReasonCode.ROUND_AMOUNT,
            {"amount": "5000.00"}
        )
        assert "5000.00" in explanation
        assert "round number" in explanation
    
    def test_get_explanation_high_amount(self):
        """Test explanation for HIGH_AMOUNT."""
        explanation = rules.get_explanation(
            ReasonCode.HIGH_AMOUNT,
            {"amount": "15000", "threshold": 10000}
        )
        assert "15000" in explanation
        assert "10000" in explanation
