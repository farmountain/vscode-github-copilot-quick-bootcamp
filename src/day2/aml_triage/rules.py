"""AML heuristic rule functions.

This module implements deterministic AML detection rules that identify
suspicious transaction patterns.
"""

from decimal import Decimal
from typing import List, Optional

from .schemas import ReasonCode, Transaction


def check_high_velocity(
    transactions: List[Transaction],
    target_account: str,
    window_seconds: int = 60
) -> Optional[ReasonCode]:
    """Check if account has 3+ transactions within time window.
    
    This rule detects potential structuring behavior where a customer
    breaks up large transactions into smaller ones to avoid reporting thresholds.
    
    Args:
        transactions: List of transactions (must be sorted by timestamp)
        target_account: Account ID to check
        window_seconds: Time window in seconds (default 60)
        
    Returns:
        ReasonCode.HIGH_VELOCITY if triggered, None otherwise
        
    Example:
        >>> txns = [tx1, tx2, tx3, tx4]  # 4 txns in 30 seconds
        >>> check_high_velocity(txns, "ACC001", window_seconds=60)
        ReasonCode.HIGH_VELOCITY
    """
    account_txns = [t for t in transactions if t.account_id == target_account]
    
    if len(account_txns) < 3:
        return None
    
    # Check each transaction as potential start of window
    for i in range(len(account_txns) - 2):
        start_time = account_txns[i].timestamp
        count = 1
        
        for j in range(i + 1, len(account_txns)):
            time_diff = (account_txns[j].timestamp - start_time).total_seconds()
            if time_diff <= window_seconds:
                count += 1
            else:
                break
        
        if count >= 3:
            return ReasonCode.HIGH_VELOCITY
    
    return None


def check_round_amount(transaction: Transaction) -> Optional[ReasonCode]:
    """Check if transaction amount is a round number (divisible by 100).
    
    Round amounts like 5000.00 or 10000.00 can indicate structured transactions
    designed to avoid detection.
    
    Args:
        transaction: Transaction to check
        
    Returns:
        ReasonCode.ROUND_AMOUNT if triggered, None otherwise
        
    Example:
        >>> tx = Transaction(amount=Decimal("5000.00"), ...)
        >>> check_round_amount(tx)
        ReasonCode.ROUND_AMOUNT
    """
    if transaction.amount % 100 == 0:
        return ReasonCode.ROUND_AMOUNT
    return None


def check_high_amount(
    transaction: Transaction,
    threshold: Decimal = Decimal("10000")
) -> Optional[ReasonCode]:
    """Check if transaction amount exceeds threshold.
    
    High-value transactions require additional scrutiny for AML compliance.
    
    Args:
        transaction: Transaction to check
        threshold: Amount threshold (default 10000)
        
    Returns:
        ReasonCode.HIGH_AMOUNT if triggered, None otherwise
        
    Example:
        >>> tx = Transaction(amount=Decimal("15000.00"), ...)
        >>> check_high_amount(tx)
        ReasonCode.HIGH_AMOUNT
    """
    if transaction.amount >= threshold:
        return ReasonCode.HIGH_AMOUNT
    return None


def check_rapid_reversal(
    transactions: List[Transaction],
    target_transaction: Transaction,
    window_seconds: int = 300
) -> Optional[ReasonCode]:
    """Check for rapid reversal pattern (debit followed by credit).
    
    Rapid reversals can indicate testing of stolen credentials or
    attempts to create confusion in transaction monitoring systems.
    
    Args:
        transactions: List of all transactions (sorted by timestamp)
        target_transaction: The transaction to check
        window_seconds: Time window in seconds (default 300 = 5 minutes)
        
    Returns:
        ReasonCode.RAPID_REVERSAL if triggered, None otherwise
        
    Example:
        >>> debit = Transaction(transaction_type="DEBIT", amount=3000, ...)
        >>> credit = Transaction(transaction_type="CREDIT", amount=3000, ...)
        >>> check_rapid_reversal([debit, credit], debit, 300)
        ReasonCode.RAPID_REVERSAL
    """
    # Only check if target is a DEBIT
    if target_transaction.transaction_type != "DEBIT":
        return None
    
    # Look for matching CREDIT within window
    for txn in transactions:
        # Must be after target transaction
        if txn.timestamp <= target_transaction.timestamp:
            continue
        
        # Check time window
        time_diff = (txn.timestamp - target_transaction.timestamp).total_seconds()
        if time_diff > window_seconds:
            break
        
        # Check if it's a matching reversal
        if (
            txn.transaction_type == "CREDIT"
            and txn.account_id == target_transaction.account_id
            and txn.beneficiary_id == target_transaction.beneficiary_id
            and abs(txn.amount - target_transaction.amount) / target_transaction.amount < Decimal("0.01")  # Within 1%
        ):
            return ReasonCode.RAPID_REVERSAL
    
    return None


def get_explanation(reason_code: ReasonCode, context: dict) -> str:
    """Generate human-readable explanation for a reason code.
    
    Args:
        reason_code: The triggered reason code
        context: Dictionary with contextual information
        
    Returns:
        Human-readable explanation string
        
    Example:
        >>> get_explanation(ReasonCode.HIGH_VELOCITY, {"count": 4, "window": 60})
        "High velocity: 4 transactions detected within 60 seconds"
    """
    explanations = {
        ReasonCode.HIGH_VELOCITY: f"High velocity: {context.get('count', 'Multiple')} transactions detected within {context.get('window', 60)} seconds",
        ReasonCode.ROUND_AMOUNT: f"Round amount: Transaction amount {context.get('amount', '')} is a round number (divisible by 100)",
        ReasonCode.HIGH_AMOUNT: f"High amount: Transaction amount {context.get('amount', '')} exceeds threshold of {context.get('threshold', 10000)}",
        ReasonCode.RAPID_REVERSAL: f"Rapid reversal: Debit followed by matching credit within {context.get('window', 300)} seconds",
        ReasonCode.NEW_BENEFICIARY: f"New beneficiary: First transaction to beneficiary {context.get('beneficiary_id', 'unknown')}"
    }
    
    return explanations.get(reason_code, f"Alert triggered: {reason_code.value}")
