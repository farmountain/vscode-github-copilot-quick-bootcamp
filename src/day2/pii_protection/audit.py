"""Audit logging for PII operations."""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from pydantic import BaseModel, Field


class AuditEntry(BaseModel):
    """Audit log entry."""
    timestamp: datetime = Field(default_factory=datetime.now)
    operation: str  # MASK, TOKENIZE, REDACT
    record_id: str
    fields_protected: List[str]
    user: str = "system"
    
    # CRITICAL: No PII in audit logs
    # Store only metadata, never actual PII values


def write_audit_entry(entry: AuditEntry, audit_log_path: Path) -> None:
    """Write audit entry to JSONL file.
    
    Args:
        entry: Audit entry to write
        audit_log_path: Path to audit log file (JSONL format)
    """
    audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Append to JSONL file
    with open(audit_log_path, 'a', encoding='utf-8') as f:
        f.write(entry.model_dump_json() + '\n')


def read_audit_log(audit_log_path: Path) -> List[AuditEntry]:
    """Read all entries from audit log.
    
    Args:
        audit_log_path: Path to audit log file
        
    Returns:
        List of audit entries
    """
    if not audit_log_path.exists():
        return []
    
    entries = []
    with open(audit_log_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                entries.append(AuditEntry(**data))
    
    return entries


def generate_audit_summary(audit_log_path: Path) -> Dict[str, int]:
    """Generate summary statistics from audit log.
    
    Args:
        audit_log_path: Path to audit log file
        
    Returns:
        Dictionary of summary statistics
    """
    entries = read_audit_log(audit_log_path)
    
    summary = {
        "total_operations": len(entries),
        "operations_by_type": {},
        "unique_records": len(set(e.record_id for e in entries)),
        "fields_protected_count": sum(len(e.fields_protected) for e in entries)
    }
    
    # Count by operation type
    for entry in entries:
        op_type = entry.operation
        summary["operations_by_type"][op_type] = summary["operations_by_type"].get(op_type, 0) + 1
    
    return summary
