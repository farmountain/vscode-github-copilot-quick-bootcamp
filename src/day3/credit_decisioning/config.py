"""Configuration module for the credit decisioning service."""
import os
from pathlib import Path


# Output directories
BASE_OUTPUT_DIR = Path("out/day3")
AUDIT_LOG_PATH = BASE_OUTPUT_DIR / "audit_log.jsonl"
DB_PATH = BASE_OUTPUT_DIR / "credit_decisioning.db"
JSON_STORE_PATH = BASE_OUTPUT_DIR / "data"

# Repository configuration
REPO_TYPE = os.getenv("REPO_TYPE", "sqlite")  # "sqlite" or "json"

# Decision thresholds
SCORE_APPROVE_THRESHOLD = int(os.getenv("SCORE_APPROVE_THRESHOLD", "70"))
SCORE_REFER_THRESHOLD = int(os.getenv("SCORE_REFER_THRESHOLD", "50"))


def setup_directories() -> None:
    """Create necessary output directories if they don't exist."""
    BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    if REPO_TYPE == "json":
        JSON_STORE_PATH.mkdir(parents=True, exist_ok=True)
        (JSON_STORE_PATH / "applications").mkdir(parents=True, exist_ok=True)
        (JSON_STORE_PATH / "decisions").mkdir(parents=True, exist_ok=True)
    
    # Ensure audit log directory exists
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


# Initialize directories on module import
setup_directories()
