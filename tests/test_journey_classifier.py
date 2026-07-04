from __future__ import annotations

from app.journey_classifier import classify_journey
from app.models import JourneyType


def test_journey_classifier_maps_sample_messages() -> None:
    assert classify_journey("My IMPS transfer failed. Should I retry?").journey == JourneyType.FAILED_TRANSACTION_RECOVERY
    assert classify_journey("I want to add a nominee online.").journey == JourneyType.NOMINEE_UPDATE_READINESS
    assert classify_journey("I want to link another bank account.").journey == JourneyType.ACCOUNT_AGGREGATION_CONSENT_READINESS
