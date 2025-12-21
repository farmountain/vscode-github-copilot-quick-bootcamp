"""FastAPI application for credit decisioning service."""
from fastapi import FastAPI, HTTPException

from .models import ApplicationRequest, ApplicationRecord, DecisionRecord
from . import repository
from . import features
from . import rules_engine
from . import audit


# Initialize FastAPI application
app = FastAPI(
    title="Credit Decisioning Service",
    description="Deterministic credit decisioning API with explainable reason codes",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    """Health check endpoint.
    
    Returns:
        Status indicator
    """
    return {"status": "ok"}


@app.post("/applications", status_code=201)
def create_application(application: ApplicationRequest):
    """Submit a new credit application.
    
    Args:
        application: Application request data
    
    Returns:
        Application ID
    """
    app_record = repository.create_application(application)
    return {"application_id": app_record.application_id}


@app.get("/applications/{application_id}")
def get_application(application_id: str) -> ApplicationRecord:
    """Retrieve an application by ID.
    
    Args:
        application_id: Application ID
    
    Returns:
        Application record
    
    Raises:
        HTTPException: 404 if application not found
    """
    app_record = repository.get_application(application_id)
    
    if app_record is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    return app_record


@app.post("/applications/{application_id}/decision", status_code=201)
def compute_decision(application_id: str) -> DecisionRecord:
    """Compute credit decision for an application.
    
    Args:
        application_id: Application ID
    
    Returns:
        Decision record with outcome, score, and reason codes
    
    Raises:
        HTTPException: 404 if application not found
    """
    # Fetch application
    app_record = repository.get_application(application_id)
    if app_record is None:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Convert to dict for feature derivation
    app_data = {
        'annual_income': app_record.annual_income,
        'monthly_debt_payments': app_record.monthly_debt_payments,
        'requested_amount': app_record.requested_amount,
        'employment_years': app_record.employment_years,
        'missed_payments_12m': app_record.missed_payments_12m
    }
    
    # Derive features
    derived_features = features.derive_features(app_data)
    
    # Compute decision
    decision_result = rules_engine.compute_decision(derived_features)
    
    # Create decision record
    decision_record = repository.create_decision(
        application_id=application_id,
        outcome=decision_result['outcome'],
        score=decision_result['score'],
        reason_codes=decision_result['reason_codes']
    )
    
    # Log decision (NO RAW PII)
    audit.log_decision(
        application_id=application_id,
        decision_id=decision_record.decision_id,
        outcome=decision_result['outcome'],
        score=decision_result['score'],
        reason_codes=decision_result['reason_codes'],
        derived_features=derived_features
    )
    
    return decision_record


@app.get("/decisions/{decision_id}")
def get_decision(decision_id: str) -> DecisionRecord:
    """Retrieve a decision by ID.
    
    Args:
        decision_id: Decision ID
    
    Returns:
        Decision record
    
    Raises:
        HTTPException: 404 if decision not found
    """
    decision_record = repository.get_decision(decision_id)
    
    if decision_record is None:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    return decision_record
