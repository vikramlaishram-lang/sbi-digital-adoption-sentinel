from __future__ import annotations

from .models import ReadinessDecisionCode, SafeNextAction


NEXT_ACTIONS = {
    ReadinessDecisionCode.ACTION_READY: SafeNextAction(
        next_safe_step="Proceed with the digital journey after reviewing the details.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.DOCUMENT_MISSING: SafeNextAction(
        next_safe_step="Complete the missing details or declaration before submission.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.CONSENT_REQUIRED: SafeNextAction(
        next_safe_step="Review and approve the consent scope before linking the account.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.CONSENT_EXPIRED: SafeNextAction(
        next_safe_step="Create a fresh consent before continuing.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.COOLING_PERIOD_ACTIVE: SafeNextAction(
        next_safe_step="Wait until the cooling period ends or proceed within the permitted limit.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.LIMIT_EXCEEDED: SafeNextAction(
        next_safe_step="Retry with an amount within the available limit or wait for limit reset.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.KYC_UPDATE_REQUIRED: SafeNextAction(
        next_safe_step="Complete or update KYC before continuing digitally.",
        escalation_required=True,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.INSTITUTION_NOT_SUPPORTED: SafeNextAction(
        next_safe_step="Select a supported institution or use an alternate assisted channel.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.BRANCH_REVIEW_REQUIRED: SafeNextAction(
        next_safe_step="Use assisted branch or staff review for this request.",
        escalation_required=True,
        branch_visit_required=True,
    ),
    ReadinessDecisionCode.RISK_REVIEW_REQUIRED: SafeNextAction(
        next_safe_step="Route the case to authorized bank review. Sensitive review logic is not exposed.",
        escalation_required=True,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.TEMPORARY_SERVICE_ISSUE: SafeNextAction(
        next_safe_step="Wait for service recovery or check transaction/reversal status before retrying.",
        escalation_required=False,
        branch_visit_required=False,
    ),
    ReadinessDecisionCode.NOT_ALLOWED: SafeNextAction(
        next_safe_step="This digital action is not currently allowed for the available state.",
        escalation_required=True,
        branch_visit_required=False,
    ),
}


def route_next_action(decision: ReadinessDecisionCode) -> SafeNextAction:
    return NEXT_ACTIONS[decision]
