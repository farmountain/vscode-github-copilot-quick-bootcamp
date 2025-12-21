"""Input/output handlers for AML Triage Pipeline.

This module handles reading transaction data and writing alert outputs.
"""

import csv
import json
from pathlib import Path
from typing import List

from .schemas import Alert, Transaction, TriageDecision


def load_transactions(csv_path: Path) -> List[Transaction]:
    """Load transactions from CSV file.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of Transaction objects sorted by timestamp
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid
        
    Example:
        >>> transactions = load_transactions(Path("sample_transactions.csv"))
        >>> len(transactions)
        20
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Transaction file not found: {csv_path}")
    
    transactions = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                transaction = Transaction(**row)
                transactions.append(transaction)
            except Exception as e:
                raise ValueError(f"Invalid transaction data in row: {row}. Error: {e}")
    
    # Sort by timestamp to ensure deterministic processing
    transactions.sort(key=lambda t: t.timestamp)
    
    return transactions


def write_alerts_json(alerts: List[Alert], output_path: Path) -> None:
    """Write alerts to JSON file.
    
    Args:
        alerts: List of Alert objects
        output_path: Path to output JSON file
        
    Example:
        >>> write_alerts_json(alerts, Path("out/aml_alerts.json"))
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Convert to dictionaries with proper serialization
    alerts_data = []
    for alert in alerts:
        alert_dict = alert.model_dump(mode='json')
        alerts_data.append(alert_dict)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(alerts_data, f, indent=2, default=str)


def write_triage_queue_csv(decisions: List[TriageDecision], output_path: Path) -> None:
    """Write triage queue to CSV file.
    
    CSV columns:
    - alert_id
    - account_id
    - amount
    - priority
    - triage_score
    - reason_codes (comma-separated)
    - queue
    
    Rows are sorted by triage_score descending (highest priority first).
    
    Args:
        decisions: List of TriageDecision objects
        output_path: Path to output CSV file
        
    Example:
        >>> write_triage_queue_csv(decisions, Path("out/triage_queue.csv"))
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Sort by triage_score descending, then by alert_id for determinism
    sorted_decisions = sorted(
        decisions,
        key=lambda d: (-d.triage_score, d.alert.alert_id)
    )
    
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = [
            'alert_id', 'account_id', 'amount', 'priority',
            'triage_score', 'reason_codes', 'queue'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for decision in sorted_decisions:
            writer.writerow({
                'alert_id': decision.alert.alert_id,
                'account_id': decision.alert.transaction.account_id,
                'amount': str(decision.alert.transaction.amount),
                'priority': decision.priority,
                'triage_score': decision.triage_score,
                'reason_codes': ','.join(code.value for code in decision.alert.reason_codes),
                'queue': decision.assigned_queue
            })


def write_summary(decisions: List[TriageDecision], output_path: Path) -> None:
    """Write summary statistics to JSON file.
    
    Summary includes:
    - total_alerts: count
    - by_priority: {P1: count, P2: count, P3: count}
    - by_reason_code: {HIGH_VELOCITY: count, ...}
    - by_queue: {HIGH_RISK: count, ...}
    
    Args:
        decisions: List of TriageDecision objects
        output_path: Path to output JSON file
        
    Example:
        >>> write_summary(decisions, Path("out/summary.json"))
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Count by priority
    by_priority = {"P1": 0, "P2": 0, "P3": 0}
    for decision in decisions:
        by_priority[decision.priority] += 1
    
    # Count by reason code
    by_reason_code = {}
    for decision in decisions:
        for code in decision.alert.reason_codes:
            by_reason_code[code.value] = by_reason_code.get(code.value, 0) + 1
    
    # Count by queue
    by_queue = {}
    for decision in decisions:
        by_queue[decision.assigned_queue] = by_queue.get(decision.assigned_queue, 0) + 1
    
    summary = {
        "total_alerts": len(decisions),
        "by_priority": by_priority,
        "by_reason_code": by_reason_code,
        "by_queue": by_queue
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
