"""Tests for I/O handlers."""

import pytest
from pathlib import Path
import json
import csv
import tempfile

from src.day2.aml_triage import io
from src.day2.aml_triage.schemas import Transaction, Alert, TriageDecision, ReasonCode
from datetime import datetime
from decimal import Decimal


class TestLoadTransactions:
    """Tests for loading transactions from CSV."""
    
    def test_load_sample_transactions(self):
        """Test loading the sample transactions file."""
        sample_file = Path("src/samples/sample_transactions_day2.csv")
        
        if not sample_file.exists():
            pytest.skip("Sample data file not found")
        
        transactions = io.load_transactions(sample_file)
        
        assert len(transactions) == 20
        assert all(isinstance(t, Transaction) for t in transactions)
        
        # Check sorting by timestamp
        for i in range(len(transactions) - 1):
            assert transactions[i].timestamp <= transactions[i + 1].timestamp
    
    def test_load_transactions_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError):
            io.load_transactions(Path("nonexistent.csv"))


class TestWriteAlertsJson:
    """Tests for writing alerts to JSON."""
    
    def test_write_alerts_creates_file(self, tmp_path):
        """Test that write_alerts_json creates output file."""
        # Create test alert
        tx = Transaction(
            transaction_id="TX001",
            account_id="ACC001",
            timestamp=datetime.now(),
            amount=Decimal("5000"),
            transaction_type="DEBIT",
            beneficiary_id="BEN001"
        )
        
        alert = Alert(
            alert_id="ALERT-TX001",
            transaction=tx,
            reason_codes=[ReasonCode.HIGH_VELOCITY],
            explanation="Test alert",
            timestamp_detected=datetime.now()
        )
        
        output_path = tmp_path / "alerts.json"
        io.write_alerts_json([alert], output_path)
        
        assert output_path.exists()
        
        # Verify valid JSON
        with open(output_path) as f:
            data = json.load(f)
            assert isinstance(data, list)
            assert len(data) == 1
            assert data[0]['alert_id'] == "ALERT-TX001"


class TestWriteTriageQueueCsv:
    """Tests for writing triage queue CSV."""
    
    def test_write_queue_creates_csv(self, tmp_path):
        """Test that write_triage_queue_csv creates CSV file."""
        # Create test data
        tx = Transaction(
            transaction_id="TX001",
            account_id="ACC001",
            timestamp=datetime.now(),
            amount=Decimal("5000"),
            transaction_type="DEBIT",
            beneficiary_id="BEN001"
        )
        
        alert = Alert(
            alert_id="ALERT-TX001",
            transaction=tx,
            reason_codes=[ReasonCode.HIGH_VELOCITY, ReasonCode.ROUND_AMOUNT],
            explanation="Test alert",
            timestamp_detected=datetime.now()
        )
        
        decision = TriageDecision(
            alert=alert,
            priority="P1",
            triage_score=70.0,
            assigned_queue="HIGH_RISK"
        )
        
        output_path = tmp_path / "queue.csv"
        io.write_triage_queue_csv([decision], output_path)
        
        assert output_path.exists()
        
        # Verify CSV structure
        with open(output_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            assert len(rows) == 1
            assert rows[0]['alert_id'] == "ALERT-TX001"
            assert rows[0]['priority'] == "P1"
            assert rows[0]['triage_score'] == "70.0"
            assert "HIGH_VELOCITY" in rows[0]['reason_codes']
    
    def test_write_queue_sorts_by_score(self, tmp_path):
        """Test that CSV rows are sorted by triage_score descending."""
        # Create multiple decisions with different scores
        decisions = []
        for i, score in enumerate([30, 70, 50]):
            tx = Transaction(
                transaction_id=f"TX{i}",
                account_id="ACC001",
                timestamp=datetime.now(),
                amount=Decimal("5000"),
                transaction_type="DEBIT",
                beneficiary_id="BEN001"
            )
            
            alert = Alert(
                alert_id=f"ALERT-TX{i}",
                transaction=tx,
                reason_codes=[ReasonCode.HIGH_VELOCITY],
                explanation="Test",
                timestamp_detected=datetime.now()
            )
            
            decision = TriageDecision(
                alert=alert,
                priority="P1",
                triage_score=float(score),
                assigned_queue="HIGH_RISK"
            )
            decisions.append(decision)
        
        output_path = tmp_path / "queue.csv"
        io.write_triage_queue_csv(decisions, output_path)
        
        # Verify sorting
        with open(output_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            scores = [float(row['triage_score']) for row in rows]
            assert scores == [70.0, 50.0, 30.0]  # Descending order


class TestWriteSummary:
    """Tests for writing summary JSON."""
    
    def test_write_summary_counts_correctly(self, tmp_path):
        """Test that summary counts are accurate."""
        # Create test decisions with different priorities
        decisions = []
        
        # P1 decision
        tx1 = Transaction(
            transaction_id="TX1",
            account_id="ACC001",
            timestamp=datetime.now(),
            amount=Decimal("5000"),
            transaction_type="DEBIT",
            beneficiary_id="BEN001"
        )
        alert1 = Alert(
            alert_id="ALERT-TX1",
            transaction=tx1,
            reason_codes=[ReasonCode.HIGH_VELOCITY, ReasonCode.ROUND_AMOUNT],
            explanation="Test",
            timestamp_detected=datetime.now()
        )
        decisions.append(TriageDecision(
            alert=alert1,
            priority="P1",
            triage_score=70.0,
            assigned_queue="HIGH_RISK"
        ))
        
        # P2 decision
        tx2 = Transaction(
            transaction_id="TX2",
            account_id="ACC002",
            timestamp=datetime.now(),
            amount=Decimal("6000"),
            transaction_type="DEBIT",
            beneficiary_id="BEN002"
        )
        alert2 = Alert(
            alert_id="ALERT-TX2",
            transaction=tx2,
            reason_codes=[ReasonCode.HIGH_AMOUNT],
            explanation="Test",
            timestamp_detected=datetime.now()
        )
        decisions.append(TriageDecision(
            alert=alert2,
            priority="P2",
            triage_score=30.0,
            assigned_queue="MEDIUM_RISK"
        ))
        
        output_path = tmp_path / "summary.json"
        io.write_summary(decisions, output_path)
        
        # Verify summary
        with open(output_path) as f:
            summary = json.load(f)
            
            assert summary['total_alerts'] == 2
            assert summary['by_priority']['P1'] == 1
            assert summary['by_priority']['P2'] == 1
            assert summary['by_reason_code']['HIGH_VELOCITY'] == 1
            assert summary['by_reason_code']['HIGH_AMOUNT'] == 1
            assert summary['by_reason_code']['ROUND_AMOUNT'] == 1
