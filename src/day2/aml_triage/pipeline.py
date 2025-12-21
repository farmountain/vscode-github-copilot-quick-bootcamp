"""AML Alert Triage Pipeline orchestrator.

This module ties together all components into an end-to-end pipeline.
"""

from datetime import datetime
from pathlib import Path
from typing import List

from . import io, rules, triage
from .schemas import Alert, Transaction, TriageDecision


def generate_alerts(transactions: List[Transaction]) -> List[Alert]:
    """Generate alerts by applying all AML rules to transactions.
    
    For each transaction:
    1. Check all rules
    2. Collect triggered reason codes
    3. If any rules trigger, create Alert
    4. Generate unique alert_id
    5. Add explanation
    
    Args:
        transactions: List of Transaction objects (should be sorted by timestamp)
        
    Returns:
        List of Alert objects sorted by timestamp
        
    Example:
        >>> alerts = generate_alerts(transactions)
        >>> len(alerts)
        8
    """
    alerts = []
    
    for transaction in transactions:
        reason_codes = []
        context = {}
        
        # Check HIGH_VELOCITY rule
        velocity_result = rules.check_high_velocity(
            transactions,
            transaction.account_id,
            window_seconds=60
        )
        if velocity_result:
            reason_codes.append(velocity_result)
            # Count transactions in window for context
            account_txns = [t for t in transactions if t.account_id == transaction.account_id]
            context['velocity_count'] = len([
                t for t in account_txns
                if abs((t.timestamp - transaction.timestamp).total_seconds()) <= 60
            ])
        
        # Check ROUND_AMOUNT rule
        round_result = rules.check_round_amount(transaction)
        if round_result:
            reason_codes.append(round_result)
            context['amount'] = str(transaction.amount)
        
        # Check HIGH_AMOUNT rule
        high_amount_result = rules.check_high_amount(transaction)
        if high_amount_result:
            reason_codes.append(high_amount_result)
            context['amount'] = str(transaction.amount)
            context['threshold'] = "10000"
        
        # Check RAPID_REVERSAL rule
        reversal_result = rules.check_rapid_reversal(
            transactions,
            transaction,
            window_seconds=300
        )
        if reversal_result:
            reason_codes.append(reversal_result)
            context['window'] = 300
        
        # Create alert if any rules triggered
        if reason_codes:
            # Generate explanations for all triggered codes
            explanations = [
                rules.get_explanation(code, context)
                for code in reason_codes
            ]
            
            alert = Alert(
                alert_id=f"ALERT-{transaction.transaction_id}",
                transaction=transaction,
                reason_codes=reason_codes,
                explanation="; ".join(explanations),
                timestamp_detected=datetime.now()
            )
            alerts.append(alert)
    
    # Sort by transaction timestamp for determinism
    alerts.sort(key=lambda a: a.transaction.timestamp)
    
    return alerts


def run_pipeline(input_csv: Path, output_dir: Path) -> dict:
    """Run the complete AML triage pipeline.
    
    Steps:
    1. Load transactions from CSV
    2. Generate alerts by applying rules
    3. Create triage decisions for all alerts
    4. Write outputs:
       - aml_alerts.json
       - triage_queue.csv
       - summary.json
    
    Args:
        input_csv: Path to input CSV file
        output_dir: Directory for output files
        
    Returns:
        Summary dictionary with statistics
        
    Example:
        >>> summary = run_pipeline(
        ...     Path("sample_transactions.csv"),
        ...     Path("out/day2/lab3")
        ... )
        >>> print(summary['total_alerts'])
        8
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load transactions
    transactions = io.load_transactions(input_csv)
    
    # Handle edge case: no transactions
    if not transactions:
        return {
            "total_alerts": 0,
            "total_transactions": 0,
            "message": "No transactions to process"
        }
    
    # Generate alerts
    alerts = generate_alerts(transactions)
    
    # Handle edge case: no alerts generated
    if not alerts:
        summary = {
            "total_alerts": 0,
            "total_transactions": len(transactions),
            "message": "No alerts generated"
        }
        # Still write summary
        io.write_summary([], output_dir / "summary.json")
        return summary
    
    # Create triage decisions
    decisions = [triage.create_triage_decision(alert) for alert in alerts]
    
    # Write outputs
    io.write_alerts_json(alerts, output_dir / "aml_alerts.json")
    io.write_triage_queue_csv(decisions, output_dir / "triage_queue.csv")
    io.write_summary(decisions, output_dir / "summary.json")
    
    # Return summary
    by_priority = {}
    for decision in decisions:
        by_priority[decision.priority] = by_priority.get(decision.priority, 0) + 1
    
    return {
        "total_alerts": len(alerts),
        "total_transactions": len(transactions),
        "by_priority": by_priority,
        "output_dir": str(output_dir)
    }
