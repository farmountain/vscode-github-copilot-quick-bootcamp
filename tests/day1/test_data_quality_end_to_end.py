"""End-to-end tests for data quality validation."""

import pytest
import json
from pathlib import Path
from decimal import Decimal

from src.day1.data_quality.validator import (
    load_transactions,
    generate_report,
    write_report,
    run_validation
)
from src.day1.data_quality.schemas import Transaction, ValidationIssue, Severity


class TestLoadTransactions:
    """Test transaction loading from CSV."""
    
    def test_load_sample_transactions(self, tmp_path):
        """Test loading transactions from CSV file."""
        csv_content = """transaction_id,account_id,amount,currency,timestamp,merchant_name,category
TX001,ACC123456,100.00,USD,2024-01-15T10:00:00Z,Coffee Shop,dining
TX002,ACC789012,200.00,EUR,2024-01-15T11:00:00Z,Restaurant,dining
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        transactions = load_transactions(csv_file)
        
        assert len(transactions) == 2
        assert transactions[0].transaction_id == "TX001"
        assert transactions[0].amount == Decimal("100.00")
        assert transactions[1].transaction_id == "TX002"
    
    def test_load_with_empty_fields(self, tmp_path):
        """Test loading transactions with empty fields."""
        csv_content = """transaction_id,account_id,amount,currency,timestamp
TX001,,100.00,USD,2024-01-15T10:00:00Z
"""
        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)
        
        transactions = load_transactions(csv_file)
        
        assert len(transactions) == 1
        assert transactions[0].account_id is None


class TestGenerateReport:
    """Test report generation."""
    
    def test_report_with_no_issues(self):
        """Test report generation when all transactions are valid."""
        transactions = [
            Transaction(
                transaction_id="TX001",
                account_id="ACC123456",
                amount=Decimal("100.00"),
                currency="USD",
                timestamp="2024-01-15T10:00:00Z"
            )
        ]
        issues = []
        
        report = generate_report(transactions, issues)
        
        assert report.total_transactions == 1
        assert report.valid_transactions == 1
        assert report.invalid_transactions == 0
        assert len(report.issues) == 0
    
    def test_report_with_issues(self):
        """Test report generation with validation issues."""
        transactions = [
            Transaction(
                transaction_id="TX001",
                account_id=None,
                amount=Decimal("100.00"),
                currency="USD",
                timestamp="2024-01-15T10:00:00Z"
            )
        ]
        issues = [
            ValidationIssue(
                transaction_id="TX001",
                field="account_id",
                rule="completeness",
                severity=Severity.HIGH,
                message="Account ID is required",
                value="null"
            )
        ]
        
        report = generate_report(transactions, issues)
        
        assert report.total_transactions == 1
        assert report.valid_transactions == 0
        assert report.invalid_transactions == 1
        assert len(report.issues) == 1
        assert report.issues_by_severity["HIGH"] == 1
        assert report.issues_by_rule["completeness"] == 1


class TestWriteReport:
    """Test report writing."""
    
    def test_write_report_to_json(self, tmp_path):
        """Test writing report to JSON file."""
        transactions = [
            Transaction(
                transaction_id="TX001",
                account_id="ACC123456",
                amount=Decimal("100.00"),
                currency="USD",
                timestamp="2024-01-15T10:00:00Z"
            )
        ]
        issues = []
        report = generate_report(transactions, issues)
        
        output_file = tmp_path / "report.json"
        write_report(report, output_file)
        
        assert output_file.exists()
        
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert data["total_transactions"] == 1
        assert data["valid_transactions"] == 1


class TestRunValidation:
    """Test complete validation pipeline."""
    
    def test_end_to_end_validation(self, tmp_path):
        """Test complete validation pipeline from CSV to report."""
        csv_content = """transaction_id,account_id,amount,currency,timestamp,merchant_name,category
TX001,ACC123456,100.00,USD,2024-01-15T10:00:00Z,Coffee Shop,dining
TX002,,200.00,USD,2024-01-15T11:00:00Z,Restaurant,dining
TX003,ACC789012,-50.00,USD,2024-01-15T12:00:00Z,Store,shopping
"""
        csv_file = tmp_path / "input.csv"
        csv_file.write_text(csv_content)
        
        output_file = tmp_path / "report.json"
        
        report = run_validation(csv_file, output_file)
        
        assert report.total_transactions == 3
        assert report.invalid_transactions >= 2  # TX002 and TX003 have issues
        assert output_file.exists()
        
        # Verify specific issues
        issue_fields = {issue.field for issue in report.issues}
        assert "account_id" in issue_fields  # TX002 missing account_id
        assert "amount" in issue_fields  # TX003 negative amount
    
    def test_deterministic_output(self, tmp_path):
        """Test that running validation twice produces identical results."""
        csv_content = """transaction_id,account_id,amount,currency,timestamp
TX001,ACC123456,100.00,USD,2024-01-15T10:00:00Z
TX002,,200.00,ZZZ,invalid-timestamp
"""
        csv_file = tmp_path / "input.csv"
        csv_file.write_text(csv_content)
        
        output_file1 = tmp_path / "report1.json"
        output_file2 = tmp_path / "report2.json"
        
        report1 = run_validation(csv_file, output_file1)
        report2 = run_validation(csv_file, output_file2)
        
        # Compare reports (excluding timestamp)
        assert report1.total_transactions == report2.total_transactions
        assert report1.valid_transactions == report2.valid_transactions
        assert report1.invalid_transactions == report2.invalid_transactions
        assert len(report1.issues) == len(report2.issues)
        
        # Sort issues for comparison
        issues1 = sorted(
            [(i.transaction_id, i.field, i.rule) for i in report1.issues]
        )
        issues2 = sorted(
            [(i.transaction_id, i.field, i.rule) for i in report2.issues]
        )
        assert issues1 == issues2
