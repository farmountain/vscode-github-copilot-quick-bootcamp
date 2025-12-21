"""Tests for validation rules."""

import pytest
from decimal import Decimal

from src.day1.data_quality.schemas import Transaction, Severity
from src.day1.data_quality.rules import (
    check_completeness,
    check_format,
    check_range,
    validate_transaction
)


class TestCompletenessRules:
    """Test completeness validation rules."""
    
    def test_valid_complete_transaction(self):
        """Test that a complete transaction has no completeness issues."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_completeness(txn)
        assert len(issues) == 0
    
    def test_missing_account_id(self):
        """Test detection of missing account_id."""
        txn = Transaction(
            transaction_id="TX001",
            account_id=None,
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_completeness(txn)
        assert len(issues) == 1
        assert issues[0].field == "account_id"
        assert issues[0].severity == Severity.HIGH
    
    def test_missing_amount(self):
        """Test detection of missing amount."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=None,
            currency="USD",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_completeness(txn)
        assert len(issues) == 1
        assert issues[0].field == "amount"
    
    def test_multiple_missing_fields(self):
        """Test detection of multiple missing fields."""
        txn = Transaction(
            transaction_id="TX001",
            account_id=None,
            amount=None,
            currency=None,
            timestamp=None
        )
        issues = check_completeness(txn)
        assert len(issues) == 4
        missing_fields = {issue.field for issue in issues}
        assert missing_fields == {"account_id", "amount", "currency", "timestamp"}


class TestFormatRules:
    """Test format validation rules."""
    
    def test_valid_formats(self):
        """Test that valid formats produce no issues."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z",
            category="dining"
        )
        issues = check_format(txn)
        assert len(issues) == 0
    
    def test_negative_amount(self):
        """Test detection of negative amount."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("-50.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_format(txn)
        assert len(issues) == 1
        assert issues[0].field == "amount"
        assert issues[0].severity == Severity.HIGH
        assert "negative" in issues[0].message.lower()
    
    def test_zero_amount(self):
        """Test detection of zero amount."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("0.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_format(txn)
        assert len(issues) == 1
        assert issues[0].field == "amount"
        assert issues[0].severity == Severity.MEDIUM
        assert "zero" in issues[0].message.lower()
    
    def test_invalid_currency(self):
        """Test detection of invalid currency code."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="ZZZ",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_format(txn)
        assert len(issues) == 1
        assert issues[0].field == "currency"
        assert issues[0].severity == Severity.MEDIUM
    
    def test_invalid_timestamp(self):
        """Test detection of invalid timestamp."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="invalid-timestamp"
        )
        issues = check_format(txn)
        assert len(issues) == 1
        assert issues[0].field == "timestamp"
        assert issues[0].severity == Severity.HIGH
    
    def test_invalid_category(self):
        """Test detection of invalid category."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z",
            category="unknown_category"
        )
        issues = check_format(txn)
        assert len(issues) == 1
        assert issues[0].field == "category"
        assert issues[0].severity == Severity.LOW


class TestRangeRules:
    """Test range validation rules."""
    
    def test_valid_ranges(self):
        """Test that values in valid ranges produce no issues."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z",
            merchant_name="Test Merchant"
        )
        issues = check_range(txn)
        assert len(issues) == 0
    
    def test_amount_exceeds_threshold(self):
        """Test detection of amount exceeding threshold."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("150000.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_range(txn)
        amount_issues = [i for i in issues if i.field == "amount"]
        assert len(amount_issues) == 1
        assert amount_issues[0].severity == Severity.MEDIUM
    
    def test_invalid_account_id_format(self):
        """Test detection of invalid account ID format."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="INVALID123",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z"
        )
        issues = check_range(txn)
        acc_issues = [i for i in issues if i.field == "account_id"]
        assert len(acc_issues) == 1
        assert acc_issues[0].severity == Severity.MEDIUM
    
    def test_missing_merchant_name(self):
        """Test detection of missing merchant name."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z",
            merchant_name=None
        )
        issues = check_range(txn)
        merchant_issues = [i for i in issues if i.field == "merchant_name"]
        assert len(merchant_issues) == 1
        assert merchant_issues[0].severity == Severity.LOW


class TestValidateTransaction:
    """Test complete transaction validation."""
    
    def test_fully_valid_transaction(self):
        """Test that a fully valid transaction produces no issues."""
        txn = Transaction(
            transaction_id="TX001",
            account_id="ACC123456",
            amount=Decimal("100.00"),
            currency="USD",
            timestamp="2024-01-15T10:00:00Z",
            merchant_name="Test Merchant",
            category="dining"
        )
        issues = validate_transaction(txn)
        assert len(issues) == 0
    
    def test_multiple_issues(self):
        """Test detection of multiple issues across different rules."""
        txn = Transaction(
            transaction_id="TX001",
            account_id=None,  # Completeness issue
            amount=Decimal("-50.00"),  # Format issue (negative)
            currency="ZZZ",  # Format issue (invalid currency)
            timestamp="2024-01-15T10:00:00Z",
            merchant_name=None  # Range issue (missing merchant)
        )
        issues = validate_transaction(txn)
        assert len(issues) >= 4
        
        # Check that issues from different rule types are present
        rules = {issue.rule for issue in issues}
        assert "completeness" in rules
        assert "format" in rules
        assert "range" in rules
