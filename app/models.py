from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


MODEL_BOUNDARY_NOTE = "The model interprets and explains. The rule engine decides. The receipt records."


class JourneyType(StrEnum):
    FAILED_TRANSACTION_RECOVERY = "failed_transaction_recovery"
    NOMINEE_UPDATE_READINESS = "nominee_update_readiness"
    ACCOUNT_AGGREGATION_CONSENT_READINESS = "account_aggregation_consent_readiness"
    UNKNOWN = "unknown"


class ReadinessDecisionCode(StrEnum):
    ACTION_READY = "ACTION_READY"
    DOCUMENT_MISSING = "DOCUMENT_MISSING"
    CONSENT_REQUIRED = "CONSENT_REQUIRED"
    CONSENT_EXPIRED = "CONSENT_EXPIRED"
    COOLING_PERIOD_ACTIVE = "COOLING_PERIOD_ACTIVE"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    KYC_UPDATE_REQUIRED = "KYC_UPDATE_REQUIRED"
    INSTITUTION_NOT_SUPPORTED = "INSTITUTION_NOT_SUPPORTED"
    BRANCH_REVIEW_REQUIRED = "BRANCH_REVIEW_REQUIRED"
    RISK_REVIEW_REQUIRED = "RISK_REVIEW_REQUIRED"
    TEMPORARY_SERVICE_ISSUE = "TEMPORARY_SERVICE_ISSUE"
    NOT_ALLOWED = "NOT_ALLOWED"


class CustomerRequest(BaseModel):
    customer_id: str
    message: str
    demo_case_id: str | None = None


class JourneyClassification(BaseModel):
    journey: JourneyType
    confidence: float
    matched_terms: list[str] = Field(default_factory=list)


class EvidenceManifest(BaseModel):
    journey: JourneyType
    evidence: dict[str, Any]


class ReadinessDecision(BaseModel):
    decision: ReadinessDecisionCode
    reason: str
    staff_reason: str
    missing_items: list[str] = Field(default_factory=list)
    rule_basis: str


class SafeNextAction(BaseModel):
    next_safe_step: str
    escalation_required: bool
    branch_visit_required: bool


class DigitalActionEnvelope(BaseModel):
    customer_id: str
    customer_request: str
    classified_journey: JourneyType
    evidence_checked: dict[str, Any]
    rule_basis: str
    readiness_decision: ReadinessDecisionCode
    reason: str
    staff_reason: str
    missing_items: list[str] = Field(default_factory=list)
    next_safe_step: str
    escalation_required: bool
    branch_visit_required: bool


class DigitalActionReceipt(BaseModel):
    receipt_id: str
    timestamp: str
    customer_id: str
    customer_request: str
    classified_journey: JourneyType
    evidence_checked: dict[str, Any]
    rule_basis: str
    readiness_decision: ReadinessDecisionCode
    reason: str
    missing_items: list[str] = Field(default_factory=list)
    next_safe_step: str
    escalation_required: bool
    branch_visit_required: bool
    model_boundary_note: str = MODEL_BOUNDARY_NOTE
    record_hash: str


class StaffReviewView(BaseModel):
    receipt_id: str
    journey: JourneyType
    decision: ReadinessDecisionCode
    evidence_summary: str
    missing_items: list[str]
    escalation_required: bool
    branch_visit_required: bool
