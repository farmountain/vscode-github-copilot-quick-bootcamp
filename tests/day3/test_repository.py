"""Repository tests for application and decision persistence."""
import pytest

from src.day3.credit_decisioning.repository import (
    create_application,
    get_application,
    create_decision,
    get_decision
)
from src.day3.credit_decisioning.models import ApplicationRequest


def test_create_and_get_application():
    """Test creating and retrieving an application."""
    app_request = ApplicationRequest(
        full_name="Test User",
        annual_income=60000,
        monthly_debt_payments=1000,
        requested_amount=15000,
        employment_years=5,
        missed_payments_12m=0,
        address="123 Test St",
        email="test@example.com"
    )
    
    # Create application
    app_record = create_application(app_request)
    assert app_record.application_id.startswith("app-")
    assert app_record.full_name == "Test User"
    assert app_record.annual_income == 60000
    
    # Retrieve application
    retrieved = get_application(app_record.application_id)
    assert retrieved is not None
    assert retrieved.application_id == app_record.application_id
    assert retrieved.full_name == app_record.full_name
    assert retrieved.annual_income == app_record.annual_income


def test_get_application_not_found():
    """Test retrieving a non-existent application."""
    result = get_application("nonexistent-id")
    assert result is None


def test_create_and_get_decision():
    """Test creating and retrieving a decision."""
    # First create an application
    app_request = ApplicationRequest(
        full_name="Test User",
        annual_income=60000,
        monthly_debt_payments=1000,
        requested_amount=15000,
        employment_years=5,
        missed_payments_12m=0,
        address="123 Test St",
        email="test@example.com"
    )
    app_record = create_application(app_request)
    
    # Create decision
    decision_record = create_decision(
        application_id=app_record.application_id,
        outcome="APPROVE",
        score=75,
        reason_codes=["LOW_DTI", "CLEAN_PAYMENT_HISTORY", "SCORE_APPROVE_BAND"]
    )
    
    assert decision_record.decision_id.startswith("dec-")
    assert decision_record.application_id == app_record.application_id
    assert decision_record.outcome == "APPROVE"
    assert decision_record.score == 75
    
    # Retrieve decision
    retrieved = get_decision(decision_record.decision_id)
    assert retrieved is not None
    assert retrieved.decision_id == decision_record.decision_id
    assert retrieved.application_id == decision_record.application_id
    assert retrieved.outcome == decision_record.outcome
    assert retrieved.score == decision_record.score
    assert retrieved.reason_codes == decision_record.reason_codes


def test_get_decision_not_found():
    """Test retrieving a non-existent decision."""
    result = get_decision("nonexistent-id")
    assert result is None


def test_multiple_applications():
    """Test creating multiple applications."""
    app_request1 = ApplicationRequest(
        full_name="User 1",
        annual_income=60000,
        monthly_debt_payments=1000,
        requested_amount=15000,
        employment_years=5,
        missed_payments_12m=0,
        address="123 Test St",
        email="user1@example.com"
    )
    
    app_request2 = ApplicationRequest(
        full_name="User 2",
        annual_income=70000,
        monthly_debt_payments=1200,
        requested_amount=18000,
        employment_years=7,
        missed_payments_12m=1,
        address="456 Test Ave",
        email="user2@example.com"
    )
    
    # Create both applications
    app1 = create_application(app_request1)
    app2 = create_application(app_request2)
    
    # Verify they have different IDs
    assert app1.application_id != app2.application_id
    
    # Verify both can be retrieved
    retrieved1 = get_application(app1.application_id)
    retrieved2 = get_application(app2.application_id)
    
    assert retrieved1 is not None
    assert retrieved2 is not None
    assert retrieved1.full_name == "User 1"
    assert retrieved2.full_name == "User 2"


def test_decision_reason_codes_persistence():
    """Test that reason codes list is properly persisted and retrieved."""
    app_request = ApplicationRequest(
        full_name="Test User",
        annual_income=60000,
        monthly_debt_payments=1000,
        requested_amount=15000,
        employment_years=5,
        missed_payments_12m=0,
        address="123 Test St",
        email="test@example.com"
    )
    app_record = create_application(app_request)
    
    reason_codes = [
        "CLEAN_PAYMENT_HISTORY",
        "LOW_DTI",
        "MODERATE_EMPLOYMENT",
        "SCORE_REFER_BAND"
    ]
    
    decision_record = create_decision(
        application_id=app_record.application_id,
        outcome="REFER",
        score=65,
        reason_codes=reason_codes
    )
    
    # Retrieve and verify reason codes
    retrieved = get_decision(decision_record.decision_id)
    assert retrieved is not None
    assert retrieved.reason_codes == reason_codes
    assert len(retrieved.reason_codes) == 4
