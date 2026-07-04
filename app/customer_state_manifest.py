from __future__ import annotations

from .demo_data_loader import load_demo_cases
from .journey_classifier import classify_journey
from .models import CustomerRequest, EvidenceManifest, JourneyType


def build_evidence_manifest(request: CustomerRequest) -> EvidenceManifest:
    demo_cases = load_demo_cases()
    if request.demo_case_id and request.demo_case_id in demo_cases:
        case = demo_cases[request.demo_case_id]
        return EvidenceManifest(journey=JourneyType(case["journey"]), evidence=dict(case["evidence"]))
    classification = classify_journey(request.message)
    return EvidenceManifest(journey=classification.journey, evidence={})
