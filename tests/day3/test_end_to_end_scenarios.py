"""End-to-end scenario tests for credit decisioning service."""
import json
import pytest
from fastapi.testclient import TestClient

from src.day3.credit_decisioning.app import app
from src.day3.credit_decisioning import config


client = TestClient(app)


def test_full_workflow_approve():
    """Test full workflow with safe application → APPROVE."""
    application_data = {
        "full_name": "Alice Safe",
        "annual_income": 80000,
        "monthly_debt_payments": 800,
        "requested_amount": 10000,
        "employment_years": 8,
        "missed_payments_12m": 0,
        "address": "456 Oak St",
        "email": "alice.safe@example.com"
    }
    
    # Submit application
    create_response = client.post("/applications", json=application_data)
    assert create_response.status_code == 201
    application_id = create_response.json()["application_id"]
    
    # Compute decision
    decision_response = client.post(f"/applications/{application_id}/decision")
    assert decision_response.status_code == 201
    decision_data = decision_response.json()
    
    # Verify APPROVE
    assert decision_data["outcome"] == "APPROVE"
    assert decision_data["score"] >= 70
    assert "SCORE_APPROVE_BAND" in decision_data["reason_codes"]
    assert "LOW_DTI" in decision_data["reason_codes"]
    assert "CLEAN_PAYMENT_HISTORY" in decision_data["reason_codes"]


def test_full_workflow_decline():
    """Test full workflow with risky application → DECLINE."""
    application_data = {
        "full_name": "Bob Risky",
        "annual_income": 30000,
        "monthly_debt_payments": 1200,
        "requested_amount": 20000,
        "employment_years": 1,
        "missed_payments_12m": 5,
        "address": "111 Danger Rd",
        "email": "bob.risky@example.com"
    }
    
    # Submit application
    create_response = client.post("/applications", json=application_data)
    assert create_response.status_code == 201
    application_id = create_response.json()["application_id"]
    
    # Compute decision
    decision_response = client.post(f"/applications/{application_id}/decision")
    assert decision_response.status_code == 201
    decision_data = decision_response.json()
    
    # Verify DECLINE
    assert decision_data["outcome"] == "DECLINE"
    assert decision_data["score"] < 50
    assert "SCORE_DECLINE_BAND" in decision_data["reason_codes"]
    assert "HIGH_DTI" in decision_data["reason_codes"]
    assert "POOR_PAYMENT_HISTORY" in decision_data["reason_codes"]


def test_full_workflow_refer():
    """Test full workflow with borderline application → REFER."""
    application_data = {
        "full_name": "Carol Borderline",
        "annual_income": 50000,
        "monthly_debt_payments": 1400,
        "requested_amount": 15000,
        "employment_years": 3,
        "missed_payments_12m": 1,
        "address": "444 Middle St",
        "email": "carol.borderline@example.com"
    }
    
    # Submit application
    create_response = client.post("/applications", json=application_data)
    assert create_response.status_code == 201
    application_id = create_response.json()["application_id"]
    
    # Compute decision
    decision_response = client.post(f"/applications/{application_id}/decision")
    assert decision_response.status_code == 201
    decision_data = decision_response.json()
    
    # Verify REFER
    assert decision_data["outcome"] == "REFER"
    assert 50 <= decision_data["score"] < 70
    assert "SCORE_REFER_BAND" in decision_data["reason_codes"]


def test_audit_log_entry_created():
    """Test that audit log entry is created after decision."""
    application_data = {
        "full_name": "Dave Audit",
        "annual_income": 60000,
        "monthly_debt_payments": 1000,
        "requested_amount": 15000,
        "employment_years": 5,
        "missed_payments_12m": 0,
        "address": "789 Audit Ave",
        "email": "dave.audit@example.com"
    }
    
    # Submit and compute decision
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    decision_response = client.post(f"/applications/{application_id}/decision")
    decision_id = decision_response.json()["decision_id"]
    
    # Read audit log
    if config.AUDIT_LOG_PATH.exists():
        with open(config.AUDIT_LOG_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Find entry with our decision_id
        found = False
        for line in lines:
            entry = json.loads(line)
            if entry.get("decision_id") == decision_id:
                found = True
                # Verify entry structure
                assert "timestamp" in entry
                assert "request_id" in entry
                assert "application_id" in entry
                assert entry["application_id"] == application_id
                assert "outcome" in entry
                assert "score" in entry
                assert "reason_codes" in entry
                break
        
        assert found, f"Decision {decision_id} not found in audit log"


def test_audit_log_no_pii():
    """Test that audit log does NOT contain raw PII."""
    application_data = {
        "full_name": "Eve Privacy",
        "annual_income": 55000,
        "monthly_debt_payments": 1100,
        "requested_amount": 14000,
        "employment_years": 4,
        "missed_payments_12m": 0,
        "address": "999 Private Ln",
        "email": "eve.privacy@example.com"
    }
    
    # Submit and compute decision
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    decision_response = client.post(f"/applications/{application_id}/decision")
    decision_id = decision_response.json()["decision_id"]
    
    # Read entire audit log content as text
    if config.AUDIT_LOG_PATH.exists():
        with open(config.AUDIT_LOG_PATH, 'r', encoding='utf-8') as f:
            audit_content = f.read()
        
        # Verify NO raw PII in audit log
        assert "Eve Privacy" not in audit_content, "full_name found in audit log (PII leak!)"
        assert "999 Private Ln" not in audit_content, "address found in audit log (PII leak!)"
        assert "eve.privacy@example.com" not in audit_content, "email found in audit log (PII leak!)"
        
        # Verify decision_id IS present (sanity check)
        assert decision_id in audit_content, "decision_id not found in audit log"


def test_deterministic_decisions():
    """Test that identical applications produce identical decisions."""
    application_data = {
        "full_name": "Frank Deterministic",
        "annual_income": 65000,
        "monthly_debt_payments": 1300,
        "requested_amount": 13000,
        "employment_years": 5,
        "missed_payments_12m": 0,
        "address": "888 Stable St",
        "email": "frank.deterministic@example.com"
    }
    
    # Submit first application
    create_response1 = client.post("/applications", json=application_data)
    application_id1 = create_response1.json()["application_id"]
    decision_response1 = client.post(f"/applications/{application_id1}/decision")
    decision1 = decision_response1.json()
    
    # Submit identical second application
    create_response2 = client.post("/applications", json=application_data)
    application_id2 = create_response2.json()["application_id"]
    decision_response2 = client.post(f"/applications/{application_id2}/decision")
    decision2 = decision_response2.json()
    
    # Verify deterministic outputs (same score, outcome, reason codes)
    assert decision1["score"] == decision2["score"]
    assert decision1["outcome"] == decision2["outcome"]
    assert decision1["reason_codes"] == decision2["reason_codes"]


def test_retrieve_decision_round_trip():
    """Test that decision can be retrieved after creation."""
    application_data = {
        "full_name": "Grace Retrieval",
        "annual_income": 70000,
        "monthly_debt_payments": 1000,
        "requested_amount": 12000,
        "employment_years": 7,
        "missed_payments_12m": 0,
        "address": "777 Fetch Rd",
        "email": "grace.retrieval@example.com"
    }
    
    # Submit and compute decision
    create_response = client.post("/applications", json=application_data)
    application_id = create_response.json()["application_id"]
    
    decision_response = client.post(f"/applications/{application_id}/decision")
    decision_data = decision_response.json()
    decision_id = decision_data["decision_id"]
    
    # Retrieve decision by ID
    retrieve_response = client.get(f"/decisions/{decision_id}")
    assert retrieve_response.status_code == 200
    retrieved_decision = retrieve_response.json()
    
    # Verify data matches
    assert retrieved_decision["decision_id"] == decision_id
    assert retrieved_decision["application_id"] == application_id
    assert retrieved_decision["outcome"] == decision_data["outcome"]
    assert retrieved_decision["score"] == decision_data["score"]
    assert retrieved_decision["reason_codes"] == decision_data["reason_codes"]
