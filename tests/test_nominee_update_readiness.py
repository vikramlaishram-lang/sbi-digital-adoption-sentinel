from __future__ import annotations

from app.models import CustomerRequest, ReadinessDecisionCode
from app.readiness_decision_engine import decide_readiness


def test_nominee_update_missing_details() -> None:
    envelope = decide_readiness(CustomerRequest(customer_id="CUST_2002", message="I want to add a nominee online.", demo_case_id="nominee_update_missing_details"))

    assert envelope.readiness_decision == ReadinessDecisionCode.DOCUMENT_MISSING
    assert envelope.missing_items == ["nominee_date_of_birth", "nominee_relationship", "consent_declaration"]
