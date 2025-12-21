"""Tests for audit logging."""

import pytest
from pathlib import Path
from datetime import datetime

from src.day2.pii_protection.audit import (
    AuditEntry,
    write_audit_entry,
    read_audit_log,
    generate_audit_summary
)


class TestAuditEntry:
    """Test audit entry model."""
    
    def test_create_audit_entry(self):
        """Test creating audit entry."""
        entry = AuditEntry(
            operation="MASK",
            record_id="CUST001",
            fields_protected=["email", "phone"]
        )
        assert entry.operation == "MASK"
        assert entry.record_id == "CUST001"
        assert len(entry.fields_protected) == 2
        assert isinstance(entry.timestamp, datetime)


class TestWriteAuditEntry:
    """Test audit entry writing."""
    
    def test_write_single_entry(self, tmp_path):
        """Test writing single audit entry."""
        audit_log = tmp_path / "audit.jsonl"
        
        entry = AuditEntry(
            operation="MASK",
            record_id="CUST001",
            fields_protected=["email"]
        )
        
        write_audit_entry(entry, audit_log)
        
        assert audit_log.exists()
        content = audit_log.read_text()
        assert "MASK" in content
        assert "CUST001" in content
    
    def test_append_multiple_entries(self, tmp_path):
        """Test appending multiple audit entries."""
        audit_log = tmp_path / "audit.jsonl"
        
        entry1 = AuditEntry(
            operation="MASK",
            record_id="CUST001",
            fields_protected=["email"]
        )
        entry2 = AuditEntry(
            operation="TOKENIZE",
            record_id="CUST002",
            fields_protected=["phone"]
        )
        
        write_audit_entry(entry1, audit_log)
        write_audit_entry(entry2, audit_log)
        
        lines = audit_log.read_text().strip().split('\n')
        assert len(lines) == 2


class TestReadAuditLog:
    """Test audit log reading."""
    
    def test_read_empty_log(self, tmp_path):
        """Test reading empty audit log."""
        audit_log = tmp_path / "audit.jsonl"
        entries = read_audit_log(audit_log)
        assert len(entries) == 0
    
    def test_read_single_entry(self, tmp_path):
        """Test reading single audit entry."""
        audit_log = tmp_path / "audit.jsonl"
        
        entry = AuditEntry(
            operation="MASK",
            record_id="CUST001",
            fields_protected=["email"]
        )
        write_audit_entry(entry, audit_log)
        
        entries = read_audit_log(audit_log)
        assert len(entries) == 1
        assert entries[0].operation == "MASK"
        assert entries[0].record_id == "CUST001"
    
    def test_read_multiple_entries(self, tmp_path):
        """Test reading multiple audit entries."""
        audit_log = tmp_path / "audit.jsonl"
        
        for i in range(3):
            entry = AuditEntry(
                operation="MASK",
                record_id=f"CUST{i:03d}",
                fields_protected=["email"]
            )
            write_audit_entry(entry, audit_log)
        
        entries = read_audit_log(audit_log)
        assert len(entries) == 3


class TestGenerateAuditSummary:
    """Test audit summary generation."""
    
    def test_summary_empty_log(self, tmp_path):
        """Test summary of empty audit log."""
        audit_log = tmp_path / "audit.jsonl"
        summary = generate_audit_summary(audit_log)
        
        assert summary["total_operations"] == 0
        assert summary["unique_records"] == 0
    
    def test_summary_with_entries(self, tmp_path):
        """Test summary with multiple entries."""
        audit_log = tmp_path / "audit.jsonl"
        
        # Write entries
        entries = [
            AuditEntry(operation="MASK", record_id="CUST001", fields_protected=["email"]),
            AuditEntry(operation="MASK", record_id="CUST002", fields_protected=["phone"]),
            AuditEntry(operation="TOKENIZE", record_id="CUST001", fields_protected=["ssn"]),
        ]
        
        for entry in entries:
            write_audit_entry(entry, audit_log)
        
        summary = generate_audit_summary(audit_log)
        
        assert summary["total_operations"] == 3
        assert summary["unique_records"] == 2  # CUST001, CUST002
        assert summary["operations_by_type"]["MASK"] == 2
        assert summary["operations_by_type"]["TOKENIZE"] == 1
        assert summary["fields_protected_count"] == 3


class TestNoPiiInLogs:
    """Test that PII is never logged."""
    
    def test_no_pii_in_audit_entry(self, tmp_path):
        """Test that audit entries never contain actual PII values."""
        audit_log = tmp_path / "audit.jsonl"
        
        # Simulate protecting PII
        pii_email = "john.doe@example.com"
        pii_phone = "555-123-4567"
        
        entry = AuditEntry(
            operation="MASK",
            record_id="CUST001",
            fields_protected=["email", "phone"]
        )
        
        write_audit_entry(entry, audit_log)
        
        # Read audit log content
        content = audit_log.read_text()
        
        # Assert that actual PII values are NOT in the audit log
        assert pii_email not in content
        assert pii_phone not in content
        
        # Assert that only metadata is logged
        assert "MASK" in content
        assert "CUST001" in content
        assert "email" in content
        assert "phone" in content
