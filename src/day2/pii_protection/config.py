"""Configuration for PII protection modes."""

from enum import Enum
from typing import Set
from pydantic import BaseModel


class ProtectionMode(str, Enum):
    """PII protection modes."""
    MASK = "MASK"  # Visual masking (e.g., ***)
    TOKENIZE = "TOKENIZE"  # Replace with deterministic token
    REDACT = "REDACT"  # Complete removal


class Config(BaseModel):
    """PII protection configuration."""
    mode: ProtectionMode
    secret_key: str  # For tokenization HMAC
    fields_to_protect: Set[str]
    audit_enabled: bool = True
