from __future__ import annotations

from app.models import CustomerRequest, ReadinessDecisionCode
from app.readiness_decision_engine import decide_readiness


def test_failed_transaction_cooling_period_case() -> None:
    envelope = decide_readiness(CustomerRequest(customer_id="CUST_1001", message="My IMPS transfer failed. Should I retry?", demo_case_id="failed_transaction_cooling_period"))

    assert envelope.readiness_decision == ReadinessDecisionCode.COOLING_PERIOD_ACTIVE
    assert envelope.next_safe_step == "Wait until the cooling period ends or proceed within the permitted limit."


def test_failed_transaction_risk_flag_overrides() -> None:
    from app.models import EvidenceManifest, JourneyType
    from app.sop_rule_engine import evaluate_rules

    decision = evaluate_rules(EvidenceManifest(journey=JourneyType.FAILED_TRANSACTION_RECOVERY, evidence={"risk_review_flag": True}))

    assert decision.decision == ReadinessDecisionCode.RISK_REVIEW_REQUIRED
