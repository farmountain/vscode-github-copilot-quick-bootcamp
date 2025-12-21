"""Pydantic models for credit decisioning service."""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, EmailStr, Field, field_validator


class ApplicationRequest(BaseModel):
    """Request model for creating a credit application."""
    
    full_name: str = Field(..., min_length=1, description="Applicant's full name")
    annual_income: float = Field(..., gt=0, description="Annual income (must be > 0)")
    monthly_debt_payments: float = Field(..., ge=0, description="Monthly debt payments (must be >= 0)")
    requested_amount: float = Field(..., gt=0, description="Requested credit amount (must be > 0)")
    employment_years: int = Field(..., ge=0, description="Years of employment (must be >= 0)")
    missed_payments_12m: int = Field(..., ge=0, description="Missed payments in last 12 months (must be >= 0)")
    address: str = Field(..., min_length=1, description="Applicant's address")
    email: EmailStr = Field(..., description="Applicant's email address")


class ApplicationRecord(BaseModel):
    """Stored application record with metadata."""
    
    application_id: str
    full_name: str
    annual_income: float
    monthly_debt_payments: float
    requested_amount: float
    employment_years: int
    missed_payments_12m: int
    address: str
    email: str
    created_at: datetime


class DecisionRecord(BaseModel):
    """Stored decision record."""
    
    decision_id: str
    application_id: str
    outcome: Literal["APPROVE", "REFER", "DECLINE"]
    score: int = Field(..., ge=0, le=100, description="Decision score (0-100)")
    reason_codes: list[str]
    timestamp: datetime
