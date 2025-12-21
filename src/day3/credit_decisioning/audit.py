"""Audit logger that writes to JSONL format (one JSON object per line)."""
import json
import uuid
from datetime import datetime, timezone

from . import config


def generate_request_id() -> str:
    """Generate a unique request ID.
    
    Returns:
        UUID4 as string
    """
    return f"req-{uuid.uuid4()}"


def log_decision(
    application_id: str,
    decision_id: str,
    outcome: str,
    score: int,
    reason_codes: list[str],
    derived_features: dict
) -> None:
    """Log a decision to the audit log.
    
    Args:
        application_id: Application ID
        decision_id: Decision ID
        outcome: Decision outcome (APPROVE/REFER/DECLINE)
        score: Decision score (0-100)
        reason_codes: List of reason codes
        derived_features: Dict with numeric features (dti, annual_income, etc.)
    
    Note:
        This function does NOT log raw PII (full_name, address, email).
        Only IDs and numeric features are logged.
    """
    # Create audit entry (NO RAW PII)
    audit_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "request_id": generate_request_id(),
        "application_id": application_id,
        "decision_id": decision_id,
        "outcome": outcome,
        "score": score,
        "reason_codes": reason_codes,
        "dti": derived_features.get("dti"),
        "annual_income": derived_features.get("annual_income"),
        "requested_amount": derived_features.get("requested_amount"),
        "employment_years": derived_features.get("employment_years"),
        "missed_payments_12m": derived_features.get("missed_payments_12m")
    }
    
    # Ensure parent directory exists
    config.AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Append to JSONL file (one JSON object per line)
    with open(config.AUDIT_LOG_PATH, 'a', encoding='utf-8') as f:
        # Use sort_keys=True for determinism
        json_line = json.dumps(audit_entry, sort_keys=True)
        f.write(json_line + '\n')
