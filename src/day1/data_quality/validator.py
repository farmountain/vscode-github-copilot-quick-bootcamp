"""Main validation orchestrator."""

import csv
import json
from pathlib import Path
from typing import List
from collections import defaultdict

from .schemas import Transaction, ValidationIssue, ValidationReport, Severity
from .rules import validate_transaction


def load_transactions(csv_path: Path) -> List[Transaction]:
    """Load transactions from CSV file.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of Transaction objects
    """
    transactions = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert empty strings to None
            cleaned_row = {k: (v if v.strip() else None) for k, v in row.items()}
            transactions.append(Transaction(**cleaned_row))
    
    return transactions


def generate_report(
    transactions: List[Transaction],
    all_issues: List[ValidationIssue]
) -> ValidationReport:
    """Generate validation report with statistics.
    
    Args:
        transactions: List of all transactions
        all_issues: List of all validation issues
        
    Returns:
        ValidationReport with aggregated statistics
    """
    # Count transactions with issues
    transactions_with_issues = set(issue.transaction_id for issue in all_issues)
    
    # Group by severity
    issues_by_severity = defaultdict(int)
    for issue in all_issues:
        issues_by_severity[issue.severity.value] += 1
    
    # Group by rule
    issues_by_rule = defaultdict(int)
    for issue in all_issues:
        issues_by_rule[issue.rule] += 1
    
    return ValidationReport(
        total_transactions=len(transactions),
        valid_transactions=len(transactions) - len(transactions_with_issues),
        invalid_transactions=len(transactions_with_issues),
        issues=all_issues,
        issues_by_severity=dict(issues_by_severity),
        issues_by_rule=dict(issues_by_rule)
    )


def write_report(report: ValidationReport, output_path: Path) -> None:
    """Write validation report to JSON file.
    
    Args:
        report: ValidationReport to write
        output_path: Path to output JSON file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report.model_dump(mode='json'), f, indent=2, default=str)


def run_validation(input_csv: Path, output_json: Path) -> ValidationReport:
    """Run complete validation pipeline.
    
    Args:
        input_csv: Path to input CSV file
        output_json: Path to output JSON report
        
    Returns:
        ValidationReport with results
    """
    # Load transactions
    transactions = load_transactions(input_csv)
    
    # Validate all transactions
    all_issues = []
    for transaction in transactions:
        issues = validate_transaction(transaction)
        all_issues.extend(issues)
    
    # Generate report
    report = generate_report(transactions, all_issues)
    
    # Write report
    write_report(report, output_json)
    
    return report
