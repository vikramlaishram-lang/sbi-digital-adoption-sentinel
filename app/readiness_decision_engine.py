from __future__ import annotations

from .customer_state_manifest import build_evidence_manifest
from .models import CustomerRequest, DigitalActionEnvelope
from .safe_next_action_router import route_next_action
from .sop_rule_engine import evaluate_rules


def decide_readiness(request: CustomerRequest) -> DigitalActionEnvelope:
    manifest = build_evidence_manifest(request)
    decision = evaluate_rules(manifest)
    next_action = route_next_action(decision.decision)
    return DigitalActionEnvelope(
        customer_id=request.customer_id,
        customer_request=request.message,
        classified_journey=manifest.journey,
        evidence_checked=manifest.evidence,
        rule_basis=decision.rule_basis,
        readiness_decision=decision.decision,
        reason=decision.reason,
        staff_reason=decision.staff_reason,
        missing_items=decision.missing_items,
        next_safe_step=next_action.next_safe_step,
        escalation_required=next_action.escalation_required,
        branch_visit_required=next_action.branch_visit_required,
    )
