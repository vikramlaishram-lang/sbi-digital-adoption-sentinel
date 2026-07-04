from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.models import MODEL_BOUNDARY_NOTE


EXPECTED = {
    "failed_transaction_cooling_period": "COOLING_PERIOD_ACTIVE",
    "nominee_update_missing_details": "DOCUMENT_MISSING",
    "account_aggregation_consent_required": "CONSENT_REQUIRED",
}


def main() -> int:
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    for case_id, expected_decision in EXPECTED.items():
        response = client.post(
            "/decide",
            json={
                "customer_id": "CUST_SMOKE",
                "message": _message_for(case_id),
                "demo_case_id": case_id,
            },
        )
        assert response.status_code == 200
        body = response.json()
        assert body["readiness_decision"] == expected_decision
        assert "receipt" in body
        assert body["receipt"]["model_boundary_note"] == MODEL_BOUNDARY_NOTE

    print("SMOKE_DEMO_PASS: true")
    print("HEALTH_OK: true")
    print("FAILED_TRANSACTION_DECISION: COOLING_PERIOD_ACTIVE")
    print("NOMINEE_UPDATE_DECISION: DOCUMENT_MISSING")
    print("ACCOUNT_AGGREGATION_DECISION: CONSENT_REQUIRED")
    print("RECEIPTS_INCLUDE_MODEL_BOUNDARY: true")
    return 0


def _message_for(case_id: str) -> str:
    return {
        "failed_transaction_cooling_period": "My IMPS transfer failed. Should I retry?",
        "nominee_update_missing_details": "I want to add a nominee online.",
        "account_aggregation_consent_required": "I want to link another bank account.",
    }[case_id]


if __name__ == "__main__":
    raise SystemExit(main())
