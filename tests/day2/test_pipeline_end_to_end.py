"""End-to-end tests for AML triage pipeline."""

import pytest
from pathlib import Path
import tempfile
import json
import csv

from src.day2.aml_triage import pipeline


class TestGenerateAlerts:
    """Tests for alert generation."""
    
    def test_generate_alerts_from_sample_data(self, tmp_path):
        """Test alert generation with sample transactions."""
        # Use the sample data file
        sample_file = Path("src/samples/sample_transactions_day2.csv")
        
        if not sample_file.exists():
            pytest.skip("Sample data file not found")
        
        from src.day2.aml_triage.io import load_transactions
        transactions = load_transactions(sample_file)
        
        alerts = pipeline.generate_alerts(transactions)
        
        # Should generate some alerts from the sample data
        assert len(alerts) > 0
        
        # Verify alert structure
        for alert in alerts:
            assert alert.alert_id.startswith("ALERT-")
            assert len(alert.reason_codes) > 0
            assert alert.explanation != ""
    
    def test_alerts_sorted_by_timestamp(self, tmp_path):
        """Test that alerts are sorted by transaction timestamp."""
        sample_file = Path("src/samples/sample_transactions_day2.csv")
        
        if not sample_file.exists():
            pytest.skip("Sample data file not found")
        
        from src.day2.aml_triage.io import load_transactions
        transactions = load_transactions(sample_file)
        
        alerts = pipeline.generate_alerts(transactions)
        
        # Check sorting
        for i in range(len(alerts) - 1):
            assert alerts[i].transaction.timestamp <= alerts[i + 1].transaction.timestamp


class TestRunPipeline:
    """Tests for full pipeline execution."""
    
    def test_run_pipeline_end_to_end(self, tmp_path):
        """Test complete pipeline with sample data."""
        sample_file = Path("src/samples/sample_transactions_day2.csv")
        
        if not sample_file.exists():
            pytest.skip("Sample data file not found")
        
        output_dir = tmp_path / "output"
        
        # Run pipeline
        summary = pipeline.run_pipeline(sample_file, output_dir)
        
        # Check summary
        assert summary['total_transactions'] == 20
        assert summary['total_alerts'] > 0
        assert 'by_priority' in summary
        
        # Check output files exist
        assert (output_dir / "aml_alerts.json").exists()
        assert (output_dir / "triage_queue.csv").exists()
        assert (output_dir / "summary.json").exists()
    
    def test_pipeline_outputs_valid_json(self, tmp_path):
        """Test that pipeline outputs are valid JSON."""
        sample_file = Path("src/samples/sample_transactions_day2.csv")
        
        if not sample_file.exists():
            pytest.skip("Sample data file not found")
        
        output_dir = tmp_path / "output"
        pipeline.run_pipeline(sample_file, output_dir)
        
        # Verify alerts JSON is valid
        with open(output_dir / "aml_alerts.json") as f:
            alerts_data = json.load(f)
            assert isinstance(alerts_data, list)
            assert len(alerts_data) > 0
        
        # Verify summary JSON is valid
        with open(output_dir / "summary.json") as f:
            summary_data = json.load(f)
            assert 'total_alerts' in summary_data
            assert 'by_priority' in summary_data
    
    def test_pipeline_outputs_valid_csv(self, tmp_path):
        """Test that triage queue CSV is valid."""
        sample_file = Path("src/samples/sample_transactions_day2.csv")
        
        if not sample_file.exists():
            pytest.skip("Sample data file not found")
        
        output_dir = tmp_path / "output"
        pipeline.run_pipeline(sample_file, output_dir)
        
        # Verify CSV is valid
        with open(output_dir / "triage_queue.csv") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
            assert len(rows) > 0
            
            # Check required columns
            first_row = rows[0]
            assert 'alert_id' in first_row
            assert 'account_id' in first_row
            assert 'priority' in first_row
            assert 'triage_score' in first_row
            assert 'reason_codes' in first_row
    
    def test_pipeline_determinism(self, tmp_path):
        """Test that pipeline produces identical results on repeated runs."""
        sample_file = Path("src/samples/sample_transactions_day2.csv")
        
        if not sample_file.exists():
            pytest.skip("Sample data file not found")
        
        output_dir1 = tmp_path / "run1"
        output_dir2 = tmp_path / "run2"
        
        # Run pipeline twice
        summary1 = pipeline.run_pipeline(sample_file, output_dir1)
        summary2 = pipeline.run_pipeline(sample_file, output_dir2)
        
        # Summaries should match
        assert summary1['total_alerts'] == summary2['total_alerts']
        assert summary1['total_transactions'] == summary2['total_transactions']
        
        # Load and compare alerts (timestamps may differ, so check IDs)
        with open(output_dir1 / "aml_alerts.json") as f:
            alerts1 = json.load(f)
        
        with open(output_dir2 / "aml_alerts.json") as f:
            alerts2 = json.load(f)
        
        # Same number of alerts
        assert len(alerts1) == len(alerts2)
        
        # Same alert IDs in same order
        alert_ids1 = [a['alert_id'] for a in alerts1]
        alert_ids2 = [a['alert_id'] for a in alerts2]
        assert alert_ids1 == alert_ids2
    
    def test_pipeline_handles_no_alerts(self, tmp_path):
        """Test pipeline handles case with no alerts generated."""
        # Create CSV with transactions that won't trigger any rules
        test_csv = tmp_path / "no_alerts.csv"
        with open(test_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['transaction_id', 'account_id', 'timestamp', 'amount', 'transaction_type', 'beneficiary_id', 'currency'])
            writer.writerow(['TX001', 'ACC001', '2024-01-15T10:00:00Z', '100.50', 'DEBIT', 'BEN001', 'USD'])
        
        output_dir = tmp_path / "output"
        
        summary = pipeline.run_pipeline(test_csv, output_dir)
        
        # Should handle gracefully
        assert summary['total_alerts'] == 0
        assert summary['total_transactions'] == 1
