"""Triage scoring and priority assignment.

This module implements the scoring logic for assigning priority levels
to AML alerts based on triggered rules.
"""

from typing import Literal

from .schemas import Alert, ReasonCode, TriageDecision


def compute_triage_score(alert: Alert) -> float:
    """Compute numerical triage score based on reason codes.
    
    Scoring logic:
    - HIGH_VELOCITY: +50 points
    - ROUND_AMOUNT: +20 points
    - HIGH_AMOUNT: +30 points
    - RAPID_REVERSAL: +40 points
    - NEW_BENEFICIARY: +25 points
    
    Multiple reason codes stack additively.
    
    Args:
        alert: Alert to score
        
    Returns:
        Total triage score as float
        
    Example:
        >>> alert = Alert(reason_codes=[ReasonCode.HIGH_VELOCITY, ReasonCode.ROUND_AMOUNT], ...)
        >>> compute_triage_score(alert)
        70.0
    """
    score_map = {
        ReasonCode.HIGH_VELOCITY: 50,
        ReasonCode.ROUND_AMOUNT: 20,
        ReasonCode.HIGH_AMOUNT: 30,
        ReasonCode.RAPID_REVERSAL: 40,
        ReasonCode.NEW_BENEFICIARY: 25
    }
    
    total_score = sum(score_map.get(code, 0) for code in alert.reason_codes)
    return float(total_score)


def assign_priority(triage_score: float) -> Literal["P1", "P2", "P3"]:
    """Assign priority level based on triage score.
    
    Priority levels:
    - P1 (Critical): score >= 70
    - P2 (High): score >= 40 and < 70
    - P3 (Medium): score < 40
    
    Args:
        triage_score: Numerical triage score
        
    Returns:
        Priority level (P1, P2, or P3)
        
    Example:
        >>> assign_priority(80.0)
        'P1'
    """
    if triage_score >= 70:
        return "P1"
    elif triage_score >= 40:
        return "P2"
    else:
        return "P3"


def assign_queue(priority: str) -> str:
    """Assign queue name based on priority level.
    
    Queue assignments:
    - P1 → "HIGH_RISK"
    - P2 → "MEDIUM_RISK"
    - P3 → "LOW_RISK"
    
    Args:
        priority: Priority level (P1, P2, or P3)
        
    Returns:
        Queue name string
        
    Example:
        >>> assign_queue("P1")
        'HIGH_RISK'
    """
    queue_map = {
        "P1": "HIGH_RISK",
        "P2": "MEDIUM_RISK",
        "P3": "LOW_RISK"
    }
    return queue_map.get(priority, "LOW_RISK")


def create_triage_decision(alert: Alert) -> TriageDecision:
    """Create complete triage decision for an alert.
    
    Orchestrates: compute score → assign priority → assign queue
    
    Args:
        alert: Alert to triage
        
    Returns:
        TriageDecision object with priority and queue assignment
        
    Example:
        >>> decision = create_triage_decision(alert)
        >>> print(decision.priority, decision.assigned_queue)
        P1 HIGH_RISK
    """
    score = compute_triage_score(alert)
    priority = assign_priority(score)
    queue = assign_queue(priority)
    
    return TriageDecision(
        alert=alert,
        priority=priority,
        triage_score=score,
        assigned_queue=queue
    )
