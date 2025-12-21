"""PII tokenization functions."""

import hashlib
import hmac
from typing import Dict


def generate_token(value: str, secret_key: str) -> str:
    """Generate deterministic token using HMAC-SHA256.
    
    Same value + secret_key always produces same token.
    
    Args:
        value: Value to tokenize
        secret_key: Secret key for HMAC
        
    Returns:
        Hexadecimal token (64 characters)
    """
    if not value:
        return "TOKEN_EMPTY"
    
    # Generate HMAC-SHA256 hash
    token = hmac.new(
        secret_key.encode('utf-8'),
        value.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return f"TOKEN_{token[:16].upper()}"


def tokenize_field(field_name: str, value: str, secret_key: str) -> str:
    """Tokenize field value.
    
    Args:
        field_name: Name of the field
        value: Value to tokenize
        secret_key: Secret key for HMAC
        
    Returns:
        Token
    """
    # Include field name in token for better uniqueness
    combined = f"{field_name}:{value}"
    return generate_token(combined, secret_key)


def tokenize_record(
    record: Dict[str, str],
    fields_to_tokenize: set,
    secret_key: str
) -> Dict[str, str]:
    """Tokenize specific fields in a record.
    
    Args:
        record: Dictionary of field:value pairs
        fields_to_tokenize: Set of field names to tokenize
        secret_key: Secret key for HMAC
        
    Returns:
        Record with tokenized fields
    """
    tokenized = record.copy()
    
    for field in fields_to_tokenize:
        if field in tokenized:
            tokenized[field] = tokenize_field(field, tokenized[field], secret_key)
    
    return tokenized


def verify_token_determinism(value: str, token: str, field_name: str, secret_key: str) -> bool:
    """Verify that token is deterministic (same input produces same token).
    
    Args:
        value: Original value
        token: Previously generated token
        field_name: Field name
        secret_key: Secret key
        
    Returns:
        True if token matches, False otherwise
    """
    regenerated_token = tokenize_field(field_name, value, secret_key)
    return regenerated_token == token
