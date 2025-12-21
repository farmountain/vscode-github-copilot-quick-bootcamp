"""Risk scoring rules and factor calculations."""

from decimal import Decimal

from .models import CreditApplication, RiskFactor, EmploymentStatus


def score_credit_score(application: CreditApplication) -> RiskFactor:
    """Score based on credit score.
    
    Rules:
    - 750+: Score 100 (excellent)
    - 700-749: Score 80 (good)
    - 650-699: Score 60 (fair)
    - 600-649: Score 40 (poor)
    - <600: Score 20 (very poor)
    
    Weight: 0.35 (35%)
    
    Args:
        application: Credit application
        
    Returns:
        RiskFactor for credit score
    """
    credit_score = application.credit_score
    weight = Decimal("0.35")
    
    if credit_score >= 750:
        score = 100
        reason = "Excellent credit score"
    elif credit_score >= 700:
        score = 80
        reason = "Good credit score"
    elif credit_score >= 650:
        score = 60
        reason = "Fair credit score"
    elif credit_score >= 600:
        score = 40
        reason = "Poor credit score"
    else:
        score = 20
        reason = "Very poor credit score"
    
    weighted_score = Decimal(score) * weight
    
    return RiskFactor(
        factor="credit_score",
        score=score,
        weight=weight,
        weighted_score=weighted_score,
        reason=reason
    )


def score_income(application: CreditApplication) -> RiskFactor:
    """Score based on annual income.
    
    Rules:
    - $100k+: Score 100 (high income)
    - $75k-$99k: Score 80 (good income)
    - $50k-$74k: Score 60 (moderate income)
    - $30k-$49k: Score 40 (low income)
    - <$30k: Score 20 (very low income)
    
    Weight: 0.25 (25%)
    
    Args:
        application: Credit application
        
    Returns:
        RiskFactor for income
    """
    income = application.annual_income
    weight = Decimal("0.25")
    
    if income >= 100000:
        score = 100
        reason = "High income"
    elif income >= 75000:
        score = 80
        reason = "Good income"
    elif income >= 50000:
        score = 60
        reason = "Moderate income"
    elif income >= 30000:
        score = 40
        reason = "Low income"
    else:
        score = 20
        reason = "Very low income"
    
    weighted_score = Decimal(score) * weight
    
    return RiskFactor(
        factor="income",
        score=score,
        weight=weight,
        weighted_score=weighted_score,
        reason=reason
    )


def score_debt_to_income(application: CreditApplication) -> RiskFactor:
    """Score based on debt-to-income ratio.
    
    DTI = monthly_debt_payments / (annual_income / 12)
    
    Rules:
    - DTI < 20%: Score 100 (excellent)
    - DTI 20-35%: Score 80 (good)
    - DTI 36-43%: Score 60 (acceptable)
    - DTI 44-50%: Score 40 (risky)
    - DTI > 50%: Score 20 (very risky)
    
    Weight: 0.30 (30%)
    
    Args:
        application: Credit application
        
    Returns:
        RiskFactor for DTI
    """
    monthly_income = application.annual_income / 12
    dti = (application.monthly_debt_payments / monthly_income) * 100
    weight = Decimal("0.30")
    
    if dti < 20:
        score = 100
        reason = f"Excellent DTI ({dti:.1f}%)"
    elif dti < 36:
        score = 80
        reason = f"Good DTI ({dti:.1f}%)"
    elif dti < 44:
        score = 60
        reason = f"Acceptable DTI ({dti:.1f}%)"
    elif dti < 51:
        score = 40
        reason = f"Risky DTI ({dti:.1f}%)"
    else:
        score = 20
        reason = f"Very risky DTI ({dti:.1f}%)"
    
    weighted_score = Decimal(score) * weight
    
    return RiskFactor(
        factor="debt_to_income",
        score=score,
        weight=weight,
        weighted_score=weighted_score,
        reason=reason
    )


def score_employment(application: CreditApplication) -> RiskFactor:
    """Score based on employment status and tenure.
    
    Rules:
    - FULL_TIME with 3+ years: Score 100
    - FULL_TIME with 1-3 years: Score 80
    - FULL_TIME with <1 year: Score 60
    - SELF_EMPLOYED with 3+ years: Score 70
    - SELF_EMPLOYED with <3 years: Score 50
    - PART_TIME: Score 40
    - RETIRED: Score 50
    - UNEMPLOYED: Score 0
    
    Weight: 0.10 (10%)
    
    Args:
        application: Credit application
        
    Returns:
        RiskFactor for employment
    """
    status = application.employment_status
    years = application.years_employed
    weight = Decimal("0.10")
    
    if status == EmploymentStatus.FULL_TIME:
        if years >= 3:
            score = 100
            reason = "Stable full-time employment"
        elif years >= 1:
            score = 80
            reason = "Full-time employment"
        else:
            score = 60
            reason = "New full-time employment"
    elif status == EmploymentStatus.SELF_EMPLOYED:
        if years >= 3:
            score = 70
            reason = "Established self-employment"
        else:
            score = 50
            reason = "New self-employment"
    elif status == EmploymentStatus.PART_TIME:
        score = 40
        reason = "Part-time employment"
    elif status == EmploymentStatus.RETIRED:
        score = 50
        reason = "Retired (fixed income)"
    else:  # UNEMPLOYED
        score = 0
        reason = "No employment"
    
    weighted_score = Decimal(score) * weight
    
    return RiskFactor(
        factor="employment",
        score=score,
        weight=weight,
        weighted_score=weighted_score,
        reason=reason
    )


def calculate_all_factors(application: CreditApplication) -> list[RiskFactor]:
    """Calculate all risk factors for an application.
    
    Args:
        application: Credit application
        
    Returns:
        List of all risk factors
    """
    return [
        score_credit_score(application),
        score_income(application),
        score_debt_to_income(application),
        score_employment(application)
    ]
