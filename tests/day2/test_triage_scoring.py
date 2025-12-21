"""Tests for triage scoring logic."""

import pytest
from datetime import datetime
from decimal import Decimal

from src.day2.aml_triage.schemas import Transaction, Alert, ReasonCode
from src.day2.aml_triage import triage


def create_test_alert(reason_codes):
    """Helper to create test alerts."""
    tx = Transaction(
        transaction_id="TX001",
        account_id="ACC001",
        timestamp=datetime.now(),
        amount=Decimal("5000"),
        transaction_type="DEBIT",
        beneficiary_id="BEN001"
    )
    
    return Alert(
        alert_id="ALERT-TX001",
        transaction=tx,
        reason_codes=reason_codes,
        explanation="Test alert",
        timestamp_detected=datetime.now()
    )


class TestComputeTriageScore:
    """Tests for triage score computation."""
    
    def test_single_rule_high_velocity(self):
        """Test score for single HIGH_VELOCITY rule."""
        alert = create_test_alert([ReasonCode.HIGH_VELOCITY])
        score = triage.compute_triage_score(alert)
        assert score == 50.0
    
    def test_single_rule_round_amount(self):
        """Test score for single ROUND_AMOUNT rule."""
        alert = create_test_alert([ReasonCode.ROUND_AMOUNT])
        score = triage.compute_triage_score(alert)
        assert score == 20.0
    
    def test_single_rule_high_amount(self):
        """Test score for single HIGH_AMOUNT rule."""
        alert = create_test_alert([ReasonCode.HIGH_AMOUNT])
        score = triage.compute_triage_score(alert)
        assert score == 30.0
    
    def test_single_rule_rapid_reversal(self):
        """Test score for single RAPID_REVERSAL rule."""
        alert = create_test_alert([ReasonCode.RAPID_REVERSAL])
        score = triage.compute_triage_score(alert)
        assert score == 40.0
    
    def test_multiple_rules_stack(self):
        """Test that multiple rules stack additively."""
        alert = create_test_alert([
            ReasonCode.HIGH_VELOCITY,
            ReasonCode.ROUND_AMOUNT
        ])
        score = triage.compute_triage_score(alert)
        assert score == 70.0  # 50 + 20
    
    def test_three_rules_stack(self):
        """Test three rules stacking."""
        alert = create_test_alert([
            ReasonCode.HIGH_VELOCITY,
            ReasonCode.HIGH_AMOUNT,
            ReasonCode.RAPID_REVERSAL
        ])
        score = triage.compute_triage_score(alert)
        assert score == 120.0  # 50 + 30 + 40


class TestAssignPriority:
    """Tests for priority assignment."""
    
    def test_priority_p1_at_70(self):
        """Test P1 assigned at exactly 70."""
        priority = triage.assign_priority(70.0)
        assert priority == "P1"
    
    def test_priority_p1_above_70(self):
        """Test P1 assigned above 70."""
        priority = triage.assign_priority(80.0)
        assert priority == "P1"
    
    def test_priority_p2_at_40(self):
        """Test P2 assigned at exactly 40."""
        priority = triage.assign_priority(40.0)
        assert priority == "P2"
    
    def test_priority_p2_between_40_and_70(self):
        """Test P2 assigned between 40 and 70."""
        priority = triage.assign_priority(50.0)
        assert priority == "P2"
    
    def test_priority_p3_below_40(self):
        """Test P3 assigned below 40."""
        priority = triage.assign_priority(30.0)
        assert priority == "P3"
    
    def test_priority_p3_at_0(self):
        """Test P3 assigned at 0."""
        priority = triage.assign_priority(0.0)
        assert priority == "P3"


class TestAssignQueue:
    """Tests for queue assignment."""
    
    def test_queue_p1_high_risk(self):
        """Test P1 assigned to HIGH_RISK."""
        queue = triage.assign_queue("P1")
        assert queue == "HIGH_RISK"
    
    def test_queue_p2_medium_risk(self):
        """Test P2 assigned to MEDIUM_RISK."""
        queue = triage.assign_queue("P2")
        assert queue == "MEDIUM_RISK"
    
    def test_queue_p3_low_risk(self):
        """Test P3 assigned to LOW_RISK."""
        queue = triage.assign_queue("P3")
        assert queue == "LOW_RISK"


class TestCreateTriageDecision:
    """Tests for end-to-end triage decision creation."""
    
    def test_create_decision_p1(self):
        """Test creating P1 decision."""
        alert = create_test_alert([
            ReasonCode.HIGH_VELOCITY,
            ReasonCode.ROUND_AMOUNT
        ])
        
        decision = triage.create_triage_decision(alert)
        
        assert decision.priority == "P1"
        assert decision.triage_score == 70.0
        assert decision.assigned_queue == "HIGH_RISK"
        assert decision.alert == alert
    
    def test_create_decision_p2(self):
        """Test creating P2 decision."""
        alert = create_test_alert([
            ReasonCode.HIGH_AMOUNT,
            ReasonCode.ROUND_AMOUNT
        ])
        
        decision = triage.create_triage_decision(alert)
        
        assert decision.priority == "P2"
        assert decision.triage_score == 50.0
        assert decision.assigned_queue == "MEDIUM_RISK"
    
    def test_create_decision_p3(self):
        """Test creating P3 decision."""
        alert = create_test_alert([ReasonCode.ROUND_AMOUNT])
        
        decision = triage.create_triage_decision(alert)
        
        assert decision.priority == "P3"
        assert decision.triage_score == 20.0
        assert decision.assigned_queue == "LOW_RISK"
