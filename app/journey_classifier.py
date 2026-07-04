from __future__ import annotations

from .models import JourneyClassification, JourneyType


def classify_journey(message: str) -> JourneyClassification:
    lowered = message.lower()
    if any(term in lowered for term in ("imps", "upi", "transfer failed", "payment failed", "money transfer failed")):
        return JourneyClassification(
            journey=JourneyType.FAILED_TRANSACTION_RECOVERY,
            confidence=0.95,
            matched_terms=[term for term in ("imps", "upi", "failed", "transfer", "payment") if term in lowered],
        )
    if "nominee" in lowered:
        return JourneyClassification(
            journey=JourneyType.NOMINEE_UPDATE_READINESS,
            confidence=0.95,
            matched_terms=["nominee"],
        )
    if any(term in lowered for term in ("link another bank", "connect my other bank", "account aggregator", "share my bank data")):
        return JourneyClassification(
            journey=JourneyType.ACCOUNT_AGGREGATION_CONSENT_READINESS,
            confidence=0.95,
            matched_terms=[term for term in ("link", "connect", "account aggregator", "consent") if term in lowered],
        )
    return JourneyClassification(journey=JourneyType.UNKNOWN, confidence=0.2, matched_terms=[])
