"""Repository module using SQLite for persistence."""
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Optional

from .models import ApplicationRequest, ApplicationRecord, DecisionRecord
from . import config


def init_db() -> None:
    """Initialize database tables if they don't exist."""
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    # Create applications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            application_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            annual_income REAL NOT NULL,
            monthly_debt_payments REAL NOT NULL,
            requested_amount REAL NOT NULL,
            employment_years INTEGER NOT NULL,
            missed_payments_12m INTEGER NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    
    # Create decisions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            decision_id TEXT PRIMARY KEY,
            application_id TEXT NOT NULL,
            outcome TEXT NOT NULL,
            score INTEGER NOT NULL,
            reason_codes TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (application_id) REFERENCES applications(application_id)
        )
    """)
    
    conn.commit()
    conn.close()


def create_application(app_request: ApplicationRequest) -> ApplicationRecord:
    """Create a new application in the repository.
    
    Args:
        app_request: Application request data
    
    Returns:
        ApplicationRecord with generated application_id and timestamp
    """
    application_id = f"app-{uuid.uuid4()}"
    created_at = datetime.now(timezone.utc)
    
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO applications (
            application_id, full_name, annual_income, monthly_debt_payments,
            requested_amount, employment_years, missed_payments_12m,
            address, email, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        application_id,
        app_request.full_name,
        app_request.annual_income,
        app_request.monthly_debt_payments,
        app_request.requested_amount,
        app_request.employment_years,
        app_request.missed_payments_12m,
        app_request.address,
        app_request.email,
        created_at.isoformat()
    ))
    
    conn.commit()
    conn.close()
    
    return ApplicationRecord(
        application_id=application_id,
        full_name=app_request.full_name,
        annual_income=app_request.annual_income,
        monthly_debt_payments=app_request.monthly_debt_payments,
        requested_amount=app_request.requested_amount,
        employment_years=app_request.employment_years,
        missed_payments_12m=app_request.missed_payments_12m,
        address=app_request.address,
        email=app_request.email,
        created_at=created_at
    )


def get_application(application_id: str) -> Optional[ApplicationRecord]:
    """Retrieve an application by ID.
    
    Args:
        application_id: Application ID to retrieve
    
    Returns:
        ApplicationRecord if found, None otherwise
    """
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT application_id, full_name, annual_income, monthly_debt_payments,
               requested_amount, employment_years, missed_payments_12m,
               address, email, created_at
        FROM applications
        WHERE application_id = ?
    """, (application_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None
    
    return ApplicationRecord(
        application_id=row[0],
        full_name=row[1],
        annual_income=row[2],
        monthly_debt_payments=row[3],
        requested_amount=row[4],
        employment_years=row[5],
        missed_payments_12m=row[6],
        address=row[7],
        email=row[8],
        created_at=datetime.fromisoformat(row[9])
    )


def create_decision(
    application_id: str,
    outcome: str,
    score: int,
    reason_codes: list[str]
) -> DecisionRecord:
    """Create a new decision in the repository.
    
    Args:
        application_id: Associated application ID
        outcome: Decision outcome (APPROVE/REFER/DECLINE)
        score: Decision score (0-100)
        reason_codes: List of reason codes
    
    Returns:
        DecisionRecord with generated decision_id and timestamp
    """
    decision_id = f"dec-{uuid.uuid4()}"
    timestamp = datetime.now(timezone.utc)
    
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    # Serialize reason_codes as JSON
    reason_codes_json = json.dumps(reason_codes)
    
    cursor.execute("""
        INSERT INTO decisions (
            decision_id, application_id, outcome, score, reason_codes, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        decision_id,
        application_id,
        outcome,
        score,
        reason_codes_json,
        timestamp.isoformat()
    ))
    
    conn.commit()
    conn.close()
    
    return DecisionRecord(
        decision_id=decision_id,
        application_id=application_id,
        outcome=outcome,  # type: ignore
        score=score,
        reason_codes=reason_codes,
        timestamp=timestamp
    )


def get_decision(decision_id: str) -> Optional[DecisionRecord]:
    """Retrieve a decision by ID.
    
    Args:
        decision_id: Decision ID to retrieve
    
    Returns:
        DecisionRecord if found, None otherwise
    """
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT decision_id, application_id, outcome, score, reason_codes, timestamp
        FROM decisions
        WHERE decision_id = ?
    """, (decision_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return None
    
    # Deserialize reason_codes from JSON
    reason_codes = json.loads(row[4])
    
    return DecisionRecord(
        decision_id=row[0],
        application_id=row[1],
        outcome=row[2],  # type: ignore
        score=row[3],
        reason_codes=reason_codes,
        timestamp=datetime.fromisoformat(row[5])
    )


# Initialize database on module import
init_db()
