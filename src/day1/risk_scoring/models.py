"""Data models for risk scoring."""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class EmploymentStatus(str, Enum):
    """Employment status categories."""
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    UNEMPLOYED = "UNEMPLOYED"
    RETIRED = "RETIRED"


class RiskLevel(str, Enum):
    """Risk assessment levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Decision(str, Enum):
    """Lending decision outcomes."""
    APPROVED = "APPROVED"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    DECLINED = "DECLINED"


class CreditApplication(BaseModel):
    """Credit application data."""
    application_id: str
    credit_score: int = Field(ge=300, le=850)
    annual_income: Decimal = Field(gt=0)
    monthly_debt_payments: Decimal = Field(ge=0)
    employment_status: EmploymentStatus
    years_employed: Decimal = Field(ge=0)
    requested_amount: Decimal = Field(gt=0)


class RiskFactor(BaseModel):
    """Individual risk factor assessment."""
    factor: str
    score: int
    weight: Decimal
    weighted_score: Decimal
    reason: str


class RiskScore(BaseModel):
    """Complete risk assessment result."""
    application_id: str
    risk_factors: List[RiskFactor]
    total_score: int
    risk_level: RiskLevel
    decision: Decision
    timestamp: datetime = Field(default_factory=datetime.now)
