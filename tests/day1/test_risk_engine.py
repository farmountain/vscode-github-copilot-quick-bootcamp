"""Tests for risk assessment engine."""

import pytest
from decimal import Decimal

from src.day1.risk_scoring.models import (
    CreditApplication,
    EmploymentStatus,
    RiskLevel,
    Decision
)
from src.day1.risk_scoring.risk_engine import (
    compute_total_score,
    determine_risk_level,
    make_decision,
    assess_risk
)
from src.day1.risk_scoring.scoring_rules import calculate_all_factors


class TestComputeTotalScore:
    """Test total score computation."""
    
    def test_perfect_score(self):
        """Test computation with perfect scores."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=800,
            annual_income=Decimal("150000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("5"),
            requested_amount=Decimal("20000")
        )
        factors = calculate_all_factors(app)
        total_score = compute_total_score(factors)
        assert total_score == 100
    
    def test_low_score(self):
        """Test computation with low scores."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=550,
            annual_income=Decimal("25000"),
            monthly_debt_payments=Decimal("1500"),
            employment_status=EmploymentStatus.UNEMPLOYED,
            years_employed=Decimal("0"),
            requested_amount=Decimal("10000")
        )
        factors = calculate_all_factors(app)
        total_score = compute_total_score(factors)
        assert total_score < 30


class TestDetermineRiskLevel:
    """Test risk level determination."""
    
    def test_low_risk(self):
        """Test LOW risk classification (70+)."""
        risk_level = determine_risk_level(85)
        assert risk_level == RiskLevel.LOW
    
    def test_medium_risk(self):
        """Test MEDIUM risk classification (50-69)."""
        risk_level = determine_risk_level(60)
        assert risk_level == RiskLevel.MEDIUM
    
    def test_high_risk(self):
        """Test HIGH risk classification (<50)."""
        risk_level = determine_risk_level(40)
        assert risk_level == RiskLevel.HIGH
    
    def test_boundary_low_medium(self):
        """Test boundary between LOW and MEDIUM risk."""
        assert determine_risk_level(70) == RiskLevel.LOW
        assert determine_risk_level(69) == RiskLevel.MEDIUM
    
    def test_boundary_medium_high(self):
        """Test boundary between MEDIUM and HIGH risk."""
        assert determine_risk_level(50) == RiskLevel.MEDIUM
        assert determine_risk_level(49) == RiskLevel.HIGH


class TestMakeDecision:
    """Test lending decision logic."""
    
    def test_low_risk_approved(self):
        """Test LOW risk is always approved."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=800,
            annual_income=Decimal("100000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("5"),
            requested_amount=Decimal("50000")
        )
        decision = make_decision(RiskLevel.LOW, app)
        assert decision == Decision.APPROVED
    
    def test_medium_risk_low_lti_approved(self):
        """Test MEDIUM risk with low LTI is approved."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("100000"),
            monthly_debt_payments=Decimal("2000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("2"),
            requested_amount=Decimal("40000")  # LTI = 0.4 < 0.5
        )
        decision = make_decision(RiskLevel.MEDIUM, app)
        assert decision == Decision.APPROVED
    
    def test_medium_risk_high_lti_manual_review(self):
        """Test MEDIUM risk with high LTI requires manual review."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("50000"),
            monthly_debt_payments=Decimal("1500"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("2"),
            requested_amount=Decimal("30000")  # LTI = 0.6 >= 0.5
        )
        decision = make_decision(RiskLevel.MEDIUM, app)
        assert decision == Decision.MANUAL_REVIEW
    
    def test_high_risk_declined(self):
        """Test HIGH risk is always declined."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=550,
            annual_income=Decimal("30000"),
            monthly_debt_payments=Decimal("1500"),
            employment_status=EmploymentStatus.PART_TIME,
            years_employed=Decimal("1"),
            requested_amount=Decimal("10000")
        )
        decision = make_decision(RiskLevel.HIGH, app)
        assert decision == Decision.DECLINED


class TestAssessRisk:
    """Test complete risk assessment."""
    
    def test_excellent_applicant(self):
        """Test assessment of excellent applicant."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=800,
            annual_income=Decimal("120000"),
            monthly_debt_payments=Decimal("1500"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("5"),
            requested_amount=Decimal("30000")
        )
        assessment = assess_risk(app)
        
        assert assessment.application_id == "TEST001"
        assert assessment.total_score >= 80
        assert assessment.risk_level == RiskLevel.LOW
        assert assessment.decision == Decision.APPROVED
        assert len(assessment.risk_factors) == 4
    
    def test_poor_applicant(self):
        """Test assessment of poor applicant."""
        app = CreditApplication(
            application_id="TEST002",
            credit_score=550,
            annual_income=Decimal("25000"),
            monthly_debt_payments=Decimal("1200"),
            employment_status=EmploymentStatus.UNEMPLOYED,
            years_employed=Decimal("0"),
            requested_amount=Decimal("10000")
        )
        assessment = assess_risk(app)
        
        assert assessment.total_score < 40
        assert assessment.risk_level == RiskLevel.HIGH
        assert assessment.decision == Decision.DECLINED
    
    def test_medium_risk_applicant(self):
        """Test assessment of medium risk applicant."""
        app = CreditApplication(
            application_id="TEST003",
            credit_score=680,
            annual_income=Decimal("55000"),
            monthly_debt_payments=Decimal("1400"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("1.5"),
            requested_amount=Decimal("20000")
        )
        assessment = assess_risk(app)
        
        assert 50 <= assessment.total_score < 70
        assert assessment.risk_level == RiskLevel.MEDIUM
        assert assessment.decision in [Decision.APPROVED, Decision.MANUAL_REVIEW]
    
    def test_deterministic_assessment(self):
        """Test that assessment is deterministic."""
        app = CreditApplication(
            application_id="TEST004",
            credit_score=720,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1200"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("25000")
        )
        
        assessment1 = assess_risk(app)
        assessment2 = assess_risk(app)
        
        assert assessment1.total_score == assessment2.total_score
        assert assessment1.risk_level == assessment2.risk_level
        assert assessment1.decision == assessment2.decision
