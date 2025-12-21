"""PII redaction functions."""

from typing import Dict, Set


def redact_fields(record: Dict[str, str], fields_to_redact: Set[str]) -> Dict[str, str]:
    """Redact (remove) specific fields from a record.
    
    Args:
        record: Dictionary of field:value pairs
        fields_to_redact: Set of field names to redact
        
    Returns:
        Record with redacted fields removed
    """
    redacted = {}
    
    for field, value in record.items():
        if field not in fields_to_redact:
            redacted[field] = value
    
    return redacted


def allowlist_fields(record: Dict[str, str], allowed_fields: Set[str]) -> Dict[str, str]:
    """Keep only allowlisted fields, redact everything else.
    
    Args:
        record: Dictionary of field:value pairs
        allowed_fields: Set of field names to keep
        
    Returns:
        Record with only allowlisted fields
    """
    allowlisted = {}
    
    for field, value in record.items():
        if field in allowed_fields:
            allowlisted[field] = value
    
    return allowlisted
