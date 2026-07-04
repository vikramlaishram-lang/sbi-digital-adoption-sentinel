from __future__ import annotations

from app.models import CustomerRequest, ReadinessDecisionCode
from app.readiness_decision_engine import decide_readiness


def test_account_aggregation_absent_consent() -> None:
    envelope = decide_readiness(CustomerRequest(customer_id="CUST_3003", message="I want to link another bank account.", demo_case_id="account_aggregation_consent_required"))

    assert envelope.readiness_decision == ReadinessDecisionCode.CONSENT_REQUIRED
    assert envelope.next_safe_step == "Review and approve the consent scope before linking the account."
