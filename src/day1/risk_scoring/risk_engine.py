"""Risk assessment engine."""

from decimal import Decimal

from .models import CreditApplication, RiskScore, RiskLevel, Decision
from .scoring_rules import calculate_all_factors


def compute_total_score(factors: list) -> int:
    """Compute total risk score from weighted factors.
    
    Args:
        factors: List of RiskFactor objects
        
    Returns:
        Total score (0-100)
    """
    total = sum(factor.weighted_score for factor in factors)
    return int(total)


def determine_risk_level(total_score: int) -> RiskLevel:
    """Determine risk level from total score.
    
    Rules:
    - 70+: LOW risk
    - 50-69: MEDIUM risk
    - <50: HIGH risk
    
    Args:
        total_score: Total weighted score
        
    Returns:
        RiskLevel
    """
    if total_score >= 70:
        return RiskLevel.LOW
    elif total_score >= 50:
        return RiskLevel.MEDIUM
    else:
        return RiskLevel.HIGH


def make_decision(
    risk_level: RiskLevel,
    application: CreditApplication
) -> Decision:
    """Make lending decision based on risk level and loan-to-income ratio.
    
    Rules:
    - LOW risk: APPROVED
    - MEDIUM risk: 
      - If requested_amount / annual_income < 0.5: APPROVED
      - Else: MANUAL_REVIEW
    - HIGH risk: DECLINED
    
    Args:
        risk_level: Risk assessment level
        application: Credit application
        
    Returns:
        Decision
    """
    if risk_level == RiskLevel.LOW:
        return Decision.APPROVED
    
    elif risk_level == RiskLevel.MEDIUM:
        lti_ratio = application.requested_amount / application.annual_income
        if lti_ratio < Decimal("0.5"):
            return Decision.APPROVED
        else:
            return Decision.MANUAL_REVIEW
    
    else:  # HIGH risk
        return Decision.DECLINED


def assess_risk(application: CreditApplication) -> RiskScore:
    """Perform complete risk assessment.
    
    Args:
        application: Credit application
        
    Returns:
        RiskScore with assessment results
    """
    # Calculate all risk factors
    factors = calculate_all_factors(application)
    
    # Compute total score
    total_score = compute_total_score(factors)
    
    # Determine risk level
    risk_level = determine_risk_level(total_score)
    
    # Make decision
    decision = make_decision(risk_level, application)
    
    return RiskScore(
        application_id=application.application_id,
        risk_factors=factors,
        total_score=total_score,
        risk_level=risk_level,
        decision=decision
    )
