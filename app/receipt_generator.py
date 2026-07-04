from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from .models import DigitalActionEnvelope, DigitalActionReceipt, JourneyType, MODEL_BOUNDARY_NOTE


PREFIXES = {
    JourneyType.FAILED_TRANSACTION_RECOVERY: "SBI-DAS-TXN",
    JourneyType.NOMINEE_UPDATE_READINESS: "SBI-DAS-NOM",
    JourneyType.ACCOUNT_AGGREGATION_CONSENT_READINESS: "SBI-DAS-AA",
}
DEMO_RECEIPTS = {
    JourneyType.FAILED_TRANSACTION_RECOVERY: "SBI-DAS-TXN-0001",
    JourneyType.NOMINEE_UPDATE_READINESS: "SBI-DAS-NOM-0002",
    JourneyType.ACCOUNT_AGGREGATION_CONSENT_READINESS: "SBI-DAS-AA-0003",
}


def generate_receipt(envelope: DigitalActionEnvelope) -> DigitalActionReceipt:
    receipt_id = DEMO_RECEIPTS.get(envelope.classified_journey, f"{PREFIXES.get(envelope.classified_journey, 'SBI-DAS-GEN')}-0000")
    payload = {
        "receipt_id": receipt_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "customer_id": envelope.customer_id,
        "customer_request": envelope.customer_request,
        "classified_journey": envelope.classified_journey,
        "evidence_checked": envelope.evidence_checked,
        "rule_basis": envelope.rule_basis,
        "readiness_decision": envelope.readiness_decision,
        "reason": envelope.reason,
        "missing_items": envelope.missing_items,
        "next_safe_step": envelope.next_safe_step,
        "escalation_required": envelope.escalation_required,
        "branch_visit_required": envelope.branch_visit_required,
        "model_boundary_note": MODEL_BOUNDARY_NOTE,
        "record_hash": "",
    }
    payload["record_hash"] = hash_receipt_payload(payload)
    return DigitalActionReceipt(**payload)


def hash_receipt_payload(payload: dict) -> str:
    canonical = dict(payload)
    canonical["record_hash"] = ""
    canonical["timestamp"] = ""
    text = json.dumps(canonical, sort_keys=True, separators=(",", ":"), default=str)
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def staff_view_from_receipt(receipt: DigitalActionReceipt) -> dict:
    return {
        "receipt_id": receipt.receipt_id,
        "journey": receipt.classified_journey,
        "decision": receipt.readiness_decision,
        "evidence_summary": f"{len(receipt.evidence_checked)} evidence fields checked; rule={receipt.rule_basis}",
        "missing_items": receipt.missing_items,
        "escalation_required": receipt.escalation_required,
        "branch_visit_required": receipt.branch_visit_required,
    }
