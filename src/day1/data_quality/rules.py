"""Validation rules for data quality checks."""

from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import List, Optional

from .schemas import Transaction, ValidationIssue, Severity


VALID_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF"}
VALID_CATEGORIES = {"dining", "shopping", "transport", "automotive", "groceries", "travel", "entertainment", "healthcare"}


def check_completeness(transaction: Transaction) -> List[ValidationIssue]:
    """Check for missing required fields.
    
    Required fields: transaction_id, account_id, amount, currency, timestamp
    
    Args:
        transaction: Transaction to validate
        
    Returns:
        List of validation issues for missing fields
    """
    issues = []
    
    required_fields = {
        "account_id": "Account ID is required",
        "amount": "Amount is required",
        "currency": "Currency is required",
        "timestamp": "Timestamp is required"
    }
    
    for field, message in required_fields.items():
        value = getattr(transaction, field)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            issues.append(ValidationIssue(
                transaction_id=transaction.transaction_id,
                field=field,
                rule="completeness",
                severity=Severity.HIGH,
                message=message,
                value=str(value) if value is not None else "null"
            ))
    
    return issues


def check_format(transaction: Transaction) -> List[ValidationIssue]:
    """Check field format validity.
    
    Validates:
    - Amount: valid decimal, not negative
    - Currency: 3-letter code from valid list
    - Timestamp: valid ISO 8601 format
    - Category: from valid list (if present)
    
    Args:
        transaction: Transaction to validate
        
    Returns:
        List of validation issues for format errors
    """
    issues = []
    
    # Check amount format and positivity
    if transaction.amount is not None:
        try:
            amount_val = Decimal(str(transaction.amount))
            if amount_val < 0:
                issues.append(ValidationIssue(
                    transaction_id=transaction.transaction_id,
                    field="amount",
                    rule="format",
                    severity=Severity.HIGH,
                    message="Amount cannot be negative",
                    value=str(transaction.amount)
                ))
            if amount_val == 0:
                issues.append(ValidationIssue(
                    transaction_id=transaction.transaction_id,
                    field="amount",
                    rule="format",
                    severity=Severity.MEDIUM,
                    message="Amount is zero",
                    value=str(transaction.amount)
                ))
        except (InvalidOperation, ValueError):
            issues.append(ValidationIssue(
                transaction_id=transaction.transaction_id,
                field="amount",
                rule="format",
                severity=Severity.HIGH,
                message="Invalid amount format",
                value=str(transaction.amount)
            ))
    
    # Check currency format
    if transaction.currency is not None:
        if transaction.currency not in VALID_CURRENCIES:
            issues.append(ValidationIssue(
                transaction_id=transaction.transaction_id,
                field="currency",
                rule="format",
                severity=Severity.MEDIUM,
                message=f"Invalid currency code. Valid codes: {', '.join(VALID_CURRENCIES)}",
                value=transaction.currency
            ))
    
    # Check timestamp format
    if transaction.timestamp is not None:
        try:
            datetime.fromisoformat(transaction.timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            issues.append(ValidationIssue(
                transaction_id=transaction.transaction_id,
                field="timestamp",
                rule="format",
                severity=Severity.HIGH,
                message="Invalid timestamp format. Expected ISO 8601 format",
                value=str(transaction.timestamp)
            ))
    
    # Check category format (if present)
    if transaction.category is not None and transaction.category.strip() != "":
        if transaction.category.lower() not in VALID_CATEGORIES:
            issues.append(ValidationIssue(
                transaction_id=transaction.transaction_id,
                field="category",
                rule="format",
                severity=Severity.LOW,
                message=f"Unknown category. Valid categories: {', '.join(VALID_CATEGORIES)}",
                value=transaction.category
            ))
    
    return issues


def check_range(transaction: Transaction) -> List[ValidationIssue]:
    """Check if values are within acceptable ranges.
    
    Validates:
    - Amount: <= 100000 (amounts above this are suspicious)
    - Account ID: proper format (ACC followed by digits)
    
    Args:
        transaction: Transaction to validate
        
    Returns:
        List of validation issues for out-of-range values
    """
    issues = []
    
    # Check amount range
    if transaction.amount is not None:
        try:
            amount_val = Decimal(str(transaction.amount))
            if amount_val > 100000:
                issues.append(ValidationIssue(
                    transaction_id=transaction.transaction_id,
                    field="amount",
                    rule="range",
                    severity=Severity.MEDIUM,
                    message="Amount exceeds maximum threshold of 100,000",
                    value=str(transaction.amount)
                ))
        except (InvalidOperation, ValueError):
            pass  # Already caught by format check
    
    # Check account ID format
    if transaction.account_id is not None:
        acc_id = str(transaction.account_id).strip()
        if not acc_id.startswith("ACC") or not acc_id[3:].isdigit():
            issues.append(ValidationIssue(
                transaction_id=transaction.transaction_id,
                field="account_id",
                rule="range",
                severity=Severity.MEDIUM,
                message="Account ID must start with 'ACC' followed by digits",
                value=transaction.account_id
            ))
    
    # Check merchant name presence
    if transaction.merchant_name is None or transaction.merchant_name.strip() == "":
        issues.append(ValidationIssue(
            transaction_id=transaction.transaction_id,
            field="merchant_name",
            rule="range",
            severity=Severity.LOW,
            message="Merchant name is missing or empty",
            value=str(transaction.merchant_name)
        ))
    
    return issues


def validate_transaction(transaction: Transaction) -> List[ValidationIssue]:
    """Run all validation rules on a transaction.
    
    Args:
        transaction: Transaction to validate
        
    Returns:
        List of all validation issues found
    """
    issues = []
    
    issues.extend(check_completeness(transaction))
    issues.extend(check_format(transaction))
    issues.extend(check_range(transaction))
    
    return issues
