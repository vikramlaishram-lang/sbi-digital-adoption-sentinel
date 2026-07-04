from __future__ import annotations

from app.models import CustomerRequest, MODEL_BOUNDARY_NOTE
from app.readiness_decision_engine import decide_readiness
from app.receipt_generator import generate_receipt, hash_receipt_payload


def test_receipt_has_required_fields_and_hash() -> None:
    envelope = decide_readiness(CustomerRequest(customer_id="CUST_1001", message="My IMPS transfer failed. Should I retry?", demo_case_id="failed_transaction_cooling_period"))
    receipt = generate_receipt(envelope)

    assert receipt.receipt_id == "SBI-DAS-TXN-0001"
    assert receipt.model_boundary_note == MODEL_BOUNDARY_NOTE
    assert receipt.record_hash.startswith("sha256:")


def test_receipt_hash_is_deterministic() -> None:
    payload = {
        "receipt_id": "SBI-DAS-TXN-0001",
        "timestamp": "ignored",
        "customer_id": "CUST_1001",
        "customer_request": "x",
        "classified_journey": "failed_transaction_recovery",
        "evidence_checked": {"a": 1},
        "rule_basis": "rule",
        "readiness_decision": "ACTION_READY",
        "reason": "reason",
        "missing_items": [],
        "next_safe_step": "next",
        "escalation_required": False,
        "branch_visit_required": False,
        "model_boundary_note": MODEL_BOUNDARY_NOTE,
        "record_hash": "",
    }

    assert hash_receipt_payload(payload) == hash_receipt_payload(dict(payload, timestamp="different"))
