"""Deterministic rules engine for credit decisioning with explainable reason codes."""
from . import config


def compute_decision(features: dict) -> dict:
    """Compute credit decision based on features.
    
    Args:
        features: Dict containing:
            - dti: float (debt-to-income ratio)
            - affordability_ratio: float (requested amount / annual income)
            - employment_years: int
            - missed_payments_12m: int
    
    Returns:
        Dict with:
            - score: int (0-100)
            - outcome: str (APPROVE/REFER/DECLINE)
            - reason_codes: list[str] (sorted alphabetically)
    
    Example:
        >>> features = {
        ...     'dti': 0.30,
        ...     'affordability_ratio': 0.25,
        ...     'employment_years': 6,
        ...     'missed_payments_12m': 0
        ... }
        >>> result = compute_decision(features)
        >>> result['score']
        85
        >>> result['outcome']
        'APPROVE'
        >>> 'LOW_DTI' in result['reason_codes']
        True
    """
    # Extract features
    dti = features['dti']
    affordability_ratio = features['affordability_ratio']
    employment_years = features['employment_years']
    missed_payments_12m = features['missed_payments_12m']
    
    # Start with baseline score
    score = 50
    reason_codes = []
    
    # DTI adjustments
    if dti < 0.36:
        score += 10
        reason_codes.append("LOW_DTI")
    elif dti >= 0.43:
        score -= 15
        reason_codes.append("HIGH_DTI")
    
    # Payment history adjustments
    if missed_payments_12m == 0:
        score += 10
        reason_codes.append("CLEAN_PAYMENT_HISTORY")
    elif missed_payments_12m in [1, 2]:
        score -= 5
        reason_codes.append("SOME_MISSED_PAYMENTS")
    elif missed_payments_12m >= 3:
        score -= 20
        reason_codes.append("POOR_PAYMENT_HISTORY")
    
    # Employment adjustments
    if employment_years > 5:
        score += 10
        reason_codes.append("STABLE_EMPLOYMENT")
    elif employment_years >= 2:
        score += 5
        reason_codes.append("MODERATE_EMPLOYMENT")
    
    # Credit exposure adjustments
    if affordability_ratio < 0.30:
        score += 5
        reason_codes.append("LOW_CREDIT_EXPOSURE")
    elif affordability_ratio >= 0.50:
        score -= 10
        reason_codes.append("HIGH_CREDIT_EXPOSURE")
    
    # Clip score to [0, 100]
    final_score = max(0, min(100, score))
    
    # Map score to outcome
    if final_score >= config.SCORE_APPROVE_THRESHOLD:
        outcome = "APPROVE"
        reason_codes.append("SCORE_APPROVE_BAND")
    elif final_score >= config.SCORE_REFER_THRESHOLD:
        outcome = "REFER"
        reason_codes.append("SCORE_REFER_BAND")
    else:
        outcome = "DECLINE"
        reason_codes.append("SCORE_DECLINE_BAND")
    
    # Sort reason codes alphabetically for determinism
    reason_codes = sorted(reason_codes)
    
    return {
        "score": final_score,
        "outcome": outcome,
        "reason_codes": reason_codes
    }
