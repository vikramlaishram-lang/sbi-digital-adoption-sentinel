from __future__ import annotations

from .models import EvidenceManifest, JourneyType, ReadinessDecision, ReadinessDecisionCode


def evaluate_rules(manifest: EvidenceManifest) -> ReadinessDecision:
    if manifest.journey == JourneyType.FAILED_TRANSACTION_RECOVERY:
        return _failed_transaction(manifest.evidence)
    if manifest.journey == JourneyType.NOMINEE_UPDATE_READINESS:
        return _nominee_update(manifest.evidence)
    if manifest.journey == JourneyType.ACCOUNT_AGGREGATION_CONSENT_READINESS:
        return _account_aggregation(manifest.evidence)
    return ReadinessDecision(
        decision=ReadinessDecisionCode.NOT_ALLOWED,
        reason="The request could not be mapped to a supported digital adoption journey.",
        staff_reason="Unknown journey classification.",
        rule_basis="unknown_journey_not_allowed",
    )


def _failed_transaction(e: dict) -> ReadinessDecision:
    if e.get("risk_review_flag"):
        return _decision(ReadinessDecisionCode.RISK_REVIEW_REQUIRED, "A review flag is present.", "failed_transaction.risk_review_flag")
    if e.get("temporary_service_issue"):
        return _decision(ReadinessDecisionCode.TEMPORARY_SERVICE_ISSUE, "A temporary service issue is affecting this journey.", "failed_transaction.temporary_service_issue")
    if e.get("daily_limit_exceeded"):
        return _decision(ReadinessDecisionCode.LIMIT_EXCEEDED, "The daily transaction limit has been exceeded.", "failed_transaction.daily_limit_exceeded")
    if (
        e.get("beneficiary_status") == "newly_added"
        and e.get("cooling_period_active")
        and float(e.get("requested_amount", 0)) > float(e.get("permitted_cooling_period_limit", 0))
    ):
        return _decision(ReadinessDecisionCode.COOLING_PERIOD_ACTIVE, "The beneficiary was recently added and the safety cooling period is still active.", "failed_transaction.new_beneficiary_cooling_period")
    if e.get("debit_status") == "debited" and e.get("reversal_status") == "pending":
        return _decision(ReadinessDecisionCode.TEMPORARY_SERVICE_ISSUE, "Debit/reversal status is pending, so retry is not yet safe.", "failed_transaction.reversal_pending")
    return _decision(ReadinessDecisionCode.ACTION_READY, "Available checks indicate the customer may retry safely.", "failed_transaction.all_checks_pass")


def _nominee_update(e: dict) -> ReadinessDecision:
    if e.get("risk_review_flag"):
        return _decision(ReadinessDecisionCode.RISK_REVIEW_REQUIRED, "A review flag is present.", "nominee_update.risk_review_flag")
    if e.get("kyc_status") != "complete":
        return _decision(ReadinessDecisionCode.KYC_UPDATE_REQUIRED, "KYC must be complete before nominee update.", "nominee_update.kyc_incomplete")
    if e.get("online_nominee_update_allowed") is False:
        return _decision(ReadinessDecisionCode.BRANCH_REVIEW_REQUIRED, "Online nominee update is not available for this account state.", "nominee_update.online_not_allowed")
    missing = []
    if not e.get("nominee_dob_present"):
        missing.append("nominee_date_of_birth")
    if not e.get("nominee_relationship_present"):
        missing.append("nominee_relationship")
    if not e.get("consent_declaration_done"):
        missing.append("consent_declaration")
    if e.get("minor_nominee") and not e.get("guardian_details_present"):
        missing.append("guardian_details")
    if missing:
        return _decision(ReadinessDecisionCode.DOCUMENT_MISSING, "Required nominee details or declaration are missing.", "nominee_update.required_details_missing", missing)
    return _decision(ReadinessDecisionCode.ACTION_READY, "Available checks indicate nominee update can proceed.", "nominee_update.all_checks_pass")


def _account_aggregation(e: dict) -> ReadinessDecision:
    if e.get("risk_review_flag"):
        return _decision(ReadinessDecisionCode.RISK_REVIEW_REQUIRED, "A review flag is present.", "account_aggregation.risk_review_flag")
    if e.get("selected_institution_supported") is False:
        return _decision(ReadinessDecisionCode.INSTITUTION_NOT_SUPPORTED, "The selected institution is not supported for this demo consent flow.", "account_aggregation.institution_not_supported")
    if e.get("mobile_kyc_match") is False:
        return _decision(ReadinessDecisionCode.KYC_UPDATE_REQUIRED, "Mobile/KYC match is required before continuing.", "account_aggregation.mobile_kyc_mismatch")
    if e.get("aa_consent_status") == "absent":
        return _decision(ReadinessDecisionCode.CONSENT_REQUIRED, "No active consent exists for account data sharing.", "account_aggregation.consent_absent")
    if e.get("consent_expired"):
        return _decision(ReadinessDecisionCode.CONSENT_EXPIRED, "The existing consent has expired.", "account_aggregation.consent_expired")
    if e.get("consent_scope_acknowledged") is False:
        return _decision(ReadinessDecisionCode.CONSENT_REQUIRED, "Consent scope must be acknowledged before linking.", "account_aggregation.scope_not_acknowledged")
    return _decision(ReadinessDecisionCode.ACTION_READY, "Available checks indicate account aggregation can proceed.", "account_aggregation.all_checks_pass")


def _decision(code: ReadinessDecisionCode, reason: str, rule_basis: str, missing: list[str] | None = None) -> ReadinessDecision:
    return ReadinessDecision(
        decision=code,
        reason=reason,
        staff_reason=f"Rule matched: {rule_basis}",
        missing_items=missing or [],
        rule_basis=rule_basis,
    )
