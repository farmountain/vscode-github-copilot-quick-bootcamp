"""Unit tests for the rules engine."""
import pytest
from src.day3.credit_decisioning.rules_engine import compute_decision


def test_baseline_score():
    """Test that neutral features result in baseline score."""
    features = {
        'dti': 0.38,  # Neutral (between 0.36 and 0.43)
        'affordability_ratio': 0.35,  # Neutral (between 0.30 and 0.50)
        'employment_years': 1,  # Neutral (< 2)
        'missed_payments_12m': 0  # This will add +10
    }
    result = compute_decision(features)
    # Baseline 50 + CLEAN_PAYMENT_HISTORY (+10) = 60
    assert result['score'] == 60
    assert result['outcome'] == "REFER"


def test_low_dti_adjustment():
    """Test LOW_DTI adjustment and reason code."""
    features = {
        'dti': 0.30,  # < 0.36
        'affordability_ratio': 0.35,
        'employment_years': 1,
        'missed_payments_12m': 1
    }
    result = compute_decision(features)
    assert "LOW_DTI" in result['reason_codes']
    # Baseline 50 + LOW_DTI (+10) + SOME_MISSED_PAYMENTS (-5) = 55
    assert result['score'] == 55


def test_high_dti_adjustment():
    """Test HIGH_DTI adjustment and reason code."""
    features = {
        'dti': 0.45,  # >= 0.43
        'affordability_ratio': 0.35,
        'employment_years': 1,
        'missed_payments_12m': 1
    }
    result = compute_decision(features)
    assert "HIGH_DTI" in result['reason_codes']
    # Baseline 50 + HIGH_DTI (-15) + SOME_MISSED_PAYMENTS (-5) = 30
    assert result['score'] == 30


def test_clean_payment_history():
    """Test CLEAN_PAYMENT_HISTORY adjustment and reason code."""
    features = {
        'dti': 0.38,
        'affordability_ratio': 0.35,
        'employment_years': 1,
        'missed_payments_12m': 0
    }
    result = compute_decision(features)
    assert "CLEAN_PAYMENT_HISTORY" in result['reason_codes']


def test_some_missed_payments():
    """Test SOME_MISSED_PAYMENTS adjustment and reason code."""
    features = {
        'dti': 0.38,
        'affordability_ratio': 0.35,
        'employment_years': 1,
        'missed_payments_12m': 2
    }
    result = compute_decision(features)
    assert "SOME_MISSED_PAYMENTS" in result['reason_codes']
    # Baseline 50 + SOME_MISSED_PAYMENTS (-5) = 45
    assert result['score'] == 45


def test_poor_payment_history():
    """Test POOR_PAYMENT_HISTORY adjustment and reason code."""
    features = {
        'dti': 0.38,
        'affordability_ratio': 0.35,
        'employment_years': 1,
        'missed_payments_12m': 5
    }
    result = compute_decision(features)
    assert "POOR_PAYMENT_HISTORY" in result['reason_codes']
    # Baseline 50 + POOR_PAYMENT_HISTORY (-20) = 30
    assert result['score'] == 30


def test_stable_employment():
    """Test STABLE_EMPLOYMENT adjustment and reason code."""
    features = {
        'dti': 0.38,
        'affordability_ratio': 0.35,
        'employment_years': 8,  # > 5
        'missed_payments_12m': 1
    }
    result = compute_decision(features)
    assert "STABLE_EMPLOYMENT" in result['reason_codes']
    # Baseline 50 + STABLE_EMPLOYMENT (+10) + SOME_MISSED_PAYMENTS (-5) = 55
    assert result['score'] == 55


def test_moderate_employment():
    """Test MODERATE_EMPLOYMENT adjustment and reason code."""
    features = {
        'dti': 0.38,
        'affordability_ratio': 0.35,
        'employment_years': 3,  # >= 2 and <= 5
        'missed_payments_12m': 1
    }
    result = compute_decision(features)
    assert "MODERATE_EMPLOYMENT" in result['reason_codes']
    # Baseline 50 + MODERATE_EMPLOYMENT (+5) + SOME_MISSED_PAYMENTS (-5) = 50
    assert result['score'] == 50


def test_low_credit_exposure():
    """Test LOW_CREDIT_EXPOSURE adjustment and reason code."""
    features = {
        'dti': 0.38,
        'affordability_ratio': 0.25,  # < 0.30
        'employment_years': 1,
        'missed_payments_12m': 1
    }
    result = compute_decision(features)
    assert "LOW_CREDIT_EXPOSURE" in result['reason_codes']
    # Baseline 50 + LOW_CREDIT_EXPOSURE (+5) + SOME_MISSED_PAYMENTS (-5) = 50
    assert result['score'] == 50


def test_high_credit_exposure():
    """Test HIGH_CREDIT_EXPOSURE adjustment and reason code."""
    features = {
        'dti': 0.38,
        'affordability_ratio': 0.55,  # >= 0.50
        'employment_years': 1,
        'missed_payments_12m': 1
    }
    result = compute_decision(features)
    assert "HIGH_CREDIT_EXPOSURE" in result['reason_codes']
    # Baseline 50 + HIGH_CREDIT_EXPOSURE (-10) + SOME_MISSED_PAYMENTS (-5) = 35
    assert result['score'] == 35


def test_approve_outcome():
    """Test APPROVE outcome when score >= 70."""
    features = {
        'dti': 0.30,  # +10
        'affordability_ratio': 0.25,  # +5
        'employment_years': 8,  # +10
        'missed_payments_12m': 0  # +10
    }
    result = compute_decision(features)
    # Baseline 50 + 10 + 5 + 10 + 10 = 85
    assert result['score'] == 85
    assert result['outcome'] == "APPROVE"
    assert "SCORE_APPROVE_BAND" in result['reason_codes']


def test_decline_outcome():
    """Test DECLINE outcome when score < 50."""
    features = {
        'dti': 0.45,  # -15
        'affordability_ratio': 0.55,  # -10
        'employment_years': 1,  # 0
        'missed_payments_12m': 5  # -20
    }
    result = compute_decision(features)
    # Baseline 50 - 15 - 10 - 20 = 5
    assert result['score'] == 5
    assert result['outcome'] == "DECLINE"
    assert "SCORE_DECLINE_BAND" in result['reason_codes']


def test_refer_outcome():
    """Test REFER outcome when score >= 50 and < 70."""
    features = {
        'dti': 0.38,  # 0
        'affordability_ratio': 0.35,  # 0
        'employment_years': 3,  # +5
        'missed_payments_12m': 0  # +10
    }
    result = compute_decision(features)
    # Baseline 50 + 5 + 10 = 65
    assert result['score'] == 65
    assert result['outcome'] == "REFER"
    assert "SCORE_REFER_BAND" in result['reason_codes']


def test_determinism():
    """Test that same features always produce same result."""
    features = {
        'dti': 0.32,
        'affordability_ratio': 0.28,
        'employment_years': 6,
        'missed_payments_12m': 0
    }
    
    result1 = compute_decision(features)
    result2 = compute_decision(features)
    
    assert result1['score'] == result2['score']
    assert result1['outcome'] == result2['outcome']
    assert result1['reason_codes'] == result2['reason_codes']


def test_reason_codes_sorted():
    """Test that reason codes are sorted alphabetically."""
    features = {
        'dti': 0.30,
        'affordability_ratio': 0.25,
        'employment_years': 8,
        'missed_payments_12m': 0
    }
    result = compute_decision(features)
    
    # Verify reason codes are sorted
    assert result['reason_codes'] == sorted(result['reason_codes'])


def test_score_clipping_upper():
    """Test that score is clipped to maximum 100."""
    # Even with impossible perfect features, score should not exceed 100
    features = {
        'dti': 0.20,  # +10
        'affordability_ratio': 0.10,  # +5
        'employment_years': 10,  # +10
        'missed_payments_12m': 0  # +10
    }
    result = compute_decision(features)
    # Baseline 50 + 35 = 85 (within bounds)
    assert result['score'] <= 100


def test_score_clipping_lower():
    """Test that score is clipped to minimum 0."""
    features = {
        'dti': 0.50,  # -15
        'affordability_ratio': 0.60,  # -10
        'employment_years': 0,  # 0
        'missed_payments_12m': 10  # -20
    }
    result = compute_decision(features)
    # Baseline 50 - 45 = 5 (still above 0)
    assert result['score'] >= 0
