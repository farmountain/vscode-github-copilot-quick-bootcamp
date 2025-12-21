"""Tests for risk scoring rules."""

import pytest
from decimal import Decimal

from src.day1.risk_scoring.models import CreditApplication, EmploymentStatus
from src.day1.risk_scoring.scoring_rules import (
    score_credit_score,
    score_income,
    score_debt_to_income,
    score_employment,
    calculate_all_factors
)


class TestCreditScoreRules:
    """Test credit score factor."""
    
    def test_excellent_credit(self):
        """Test excellent credit score (750+)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=800,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_credit_score(app)
        assert factor.score == 100
        assert factor.weight == Decimal("0.35")
        assert factor.weighted_score == Decimal("35.0")
    
    def test_good_credit(self):
        """Test good credit score (700-749)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=720,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_credit_score(app)
        assert factor.score == 80
        assert factor.weighted_score == Decimal("28.0")
    
    def test_poor_credit(self):
        """Test poor credit score (600-649)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=620,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_credit_score(app)
        assert factor.score == 40


class TestIncomeRules:
    """Test income factor."""
    
    def test_high_income(self):
        """Test high income ($100k+)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("120000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_income(app)
        assert factor.score == 100
        assert factor.weight == Decimal("0.25")
        assert factor.weighted_score == Decimal("25.0")
    
    def test_moderate_income(self):
        """Test moderate income ($50k-$74k)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("60000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_income(app)
        assert factor.score == 60
        assert factor.weighted_score == Decimal("15.0")
    
    def test_low_income(self):
        """Test low income (<$30k)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("25000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_income(app)
        assert factor.score == 20


class TestDebtToIncomeRules:
    """Test debt-to-income ratio factor."""
    
    def test_excellent_dti(self):
        """Test excellent DTI (<20%)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("120000"),  # $10k/month
            monthly_debt_payments=Decimal("1500"),  # 15% DTI
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_debt_to_income(app)
        assert factor.score == 100
        assert factor.weight == Decimal("0.30")
        assert factor.weighted_score == Decimal("30.0")
    
    def test_good_dti(self):
        """Test good DTI (20-35%)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("60000"),  # $5k/month
            monthly_debt_payments=Decimal("1500"),  # 30% DTI
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_debt_to_income(app)
        assert factor.score == 80
        assert factor.weighted_score == Decimal("24.0")
    
    def test_risky_dti(self):
        """Test risky DTI (>50%)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("36000"),  # $3k/month
            monthly_debt_payments=Decimal("2000"),  # 66% DTI
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factor = score_debt_to_income(app)
        assert factor.score == 20


class TestEmploymentRules:
    """Test employment factor."""
    
    def test_stable_full_time(self):
        """Test stable full-time employment (3+ years)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("5"),
            requested_amount=Decimal("20000")
        )
        factor = score_employment(app)
        assert factor.score == 100
        assert factor.weight == Decimal("0.10")
        assert factor.weighted_score == Decimal("10.0")
    
    def test_new_full_time(self):
        """Test new full-time employment (<1 year)."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("0.5"),
            requested_amount=Decimal("20000")
        )
        factor = score_employment(app)
        assert factor.score == 60
    
    def test_self_employed(self):
        """Test established self-employment."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.SELF_EMPLOYED,
            years_employed=Decimal("4"),
            requested_amount=Decimal("20000")
        )
        factor = score_employment(app)
        assert factor.score == 70
    
    def test_unemployed(self):
        """Test unemployed status."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=700,
            annual_income=Decimal("75000"),
            monthly_debt_payments=Decimal("1000"),
            employment_status=EmploymentStatus.UNEMPLOYED,
            years_employed=Decimal("0"),
            requested_amount=Decimal("20000")
        )
        factor = score_employment(app)
        assert factor.score == 0


class TestCalculateAllFactors:
    """Test complete factor calculation."""
    
    def test_all_factors_calculated(self):
        """Test that all four factors are calculated."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=750,
            annual_income=Decimal("80000"),
            monthly_debt_payments=Decimal("1500"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factors = calculate_all_factors(app)
        assert len(factors) == 4
        factor_names = {f.factor for f in factors}
        assert factor_names == {"credit_score", "income", "debt_to_income", "employment"}
    
    def test_weights_sum_to_one(self):
        """Test that all factor weights sum to 1.0."""
        app = CreditApplication(
            application_id="TEST001",
            credit_score=750,
            annual_income=Decimal("80000"),
            monthly_debt_payments=Decimal("1500"),
            employment_status=EmploymentStatus.FULL_TIME,
            years_employed=Decimal("3"),
            requested_amount=Decimal("20000")
        )
        factors = calculate_all_factors(app)
        total_weight = sum(f.weight for f in factors)
        assert total_weight == Decimal("1.0")
