"""API endpoint tests using FastAPI TestClient."""
import pytest
from fastapi.testclient import TestClient

from src.day3.credit_decisioning.app import app


client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_application_success():
    """Test creating an application with valid data."""
    application_data = {
        "full_name": "Test Applicant",
        "annual_income": 60000,
        "monthly_debt_payments": 1000,
        "requested_amount": 15000,
        "employment_years": 5,
        "missed_payments_12m": 0,
        "address": "123 Test St",
        "email": "test@example.com"
    }
    
    response = client.post("/applications", json=application_data)
    assert response.status_code == 201
    data = response.json()
    assert "application_id" in data
    assert data["application_id"].startswith("app-")


def test_create_application_invalid_income():
    """Test creating an application with invalid income."""
    application_data = {
        "full_name": "Test Applicant",
        "annual_income": -1000,  # Invalid: negative
        "monthly_debt_payments": 1000,
        "requested_amount": 15000,
        "employment_years": 5,
        "missed_payments_12m": 0,
        "address": "123 Test St",
        "email": "test@example.com"
    }
    
    response = client.post("/applications", json=application_data)
    assert response.status_code == 422  # Validation error


def test_create_application_missing_field():
    """Test creating an application with missing required field."""
    application_data = {
        "full_name": "Test Applicant",
        # Missing annual_income
        "monthly_debt_payments": 1000,
        "requested_amount": 15000,
        "employment_years": 5,
        "missed_payments_12m": 0,
        "address": "123 Test St",
        "email": "test@example.com"
    }
    
    response = client.post("/applications", json=application_data)
    assert response.status_code == 422


def test_get_application_success():
    """Test retrieving an application by ID."""
    # First, create an application
    application_data = {
        "full_name": "Test Applicant",
        "annual_income": 60000,
        "monthly_debt_payments": 1000,
        "requested_amount": 15000,
        "employment_years": 5,
        "missed_payments_12m": 0,
        "address": "123 Test St",
        "email": "test@example.com"
    }
    
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    # Then, retrieve it
    response = client.get(f"/applications/{application_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["application_id"] == application_id
    assert data["full_name"] == "Test Applicant"
    assert data["annual_income"] == 60000


def test_get_application_not_found():
    """Test retrieving a non-existent application."""
    response = client.get("/applications/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_compute_decision_success():
    """Test computing a decision for an application."""
    # Create an application
    application_data = {
        "full_name": "Test Applicant",
        "annual_income": 70000,
        "monthly_debt_payments": 1000,
        "requested_amount": 12000,
        "employment_years": 6,
        "missed_payments_12m": 0,
        "address": "123 Test St",
        "email": "test@example.com"
    }
    
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    # Compute decision
    response = client.post(f"/applications/{application_id}/decision")
    assert response.status_code == 201
    data = response.json()
    
    assert "decision_id" in data
    assert data["decision_id"].startswith("dec-")
    assert data["application_id"] == application_id
    assert "outcome" in data
    assert data["outcome"] in ["APPROVE", "REFER", "DECLINE"]
    assert "score" in data
    assert 0 <= data["score"] <= 100
    assert "reason_codes" in data
    assert len(data["reason_codes"]) > 0


def test_compute_decision_application_not_found():
    """Test computing a decision for a non-existent application."""
    response = client.post("/applications/nonexistent-id/decision")
    assert response.status_code == 404


def test_get_decision_success():
    """Test retrieving a decision by ID."""
    # Create application and compute decision
    application_data = {
        "full_name": "Test Applicant",
        "annual_income": 60000,
        "monthly_debt_payments": 1000,
        "requested_amount": 15000,
        "employment_years": 5,
        "missed_payments_12m": 0,
        "address": "123 Test St",
        "email": "test@example.com"
    }
    
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    decision_response = client.post(f"/applications/{application_id}/decision")
    decision_id = decision_response.json()["decision_id"]
    
    # Retrieve decision
    response = client.get(f"/decisions/{decision_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["decision_id"] == decision_id
    assert data["application_id"] == application_id


def test_get_decision_not_found():
    """Test retrieving a non-existent decision."""
    response = client.get("/decisions/nonexistent-id")
    assert response.status_code == 404


def test_full_workflow_safe_application():
    """Test full workflow with a safe application (should APPROVE)."""
    application_data = {
        "full_name": "Safe Applicant",
        "annual_income": 80000,
        "monthly_debt_payments": 800,
        "requested_amount": 10000,
        "employment_years": 8,
        "missed_payments_12m": 0,
        "address": "456 Safe St",
        "email": "safe@example.com"
    }
    
    # Create application
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    # Compute decision
    decision_response = client.post(f"/applications/{application_id}/decision")
    decision_data = decision_response.json()
    
    # Verify APPROVE outcome (safe applicant)
    assert decision_data["score"] >= 70
    assert decision_data["outcome"] == "APPROVE"
    assert "SCORE_APPROVE_BAND" in decision_data["reason_codes"]


def test_full_workflow_risky_application():
    """Test full workflow with a risky application (should DECLINE)."""
    application_data = {
        "full_name": "Risky Applicant",
        "annual_income": 30000,
        "monthly_debt_payments": 1200,
        "requested_amount": 20000,
        "employment_years": 1,
        "missed_payments_12m": 5,
        "address": "789 Risky Rd",
        "email": "risky@example.com"
    }
    
    # Create application
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    # Compute decision
    decision_response = client.post(f"/applications/{application_id}/decision")
    decision_data = decision_response.json()
    
    # Verify DECLINE outcome (risky applicant)
    assert decision_data["score"] < 50
    assert decision_data["outcome"] == "DECLINE"
    assert "SCORE_DECLINE_BAND" in decision_data["reason_codes"]
