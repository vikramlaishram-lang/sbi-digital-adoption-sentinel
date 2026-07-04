from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "product": "SBI Digital Adoption Sentinel"}


def test_decide_returns_receipt_and_staff_view() -> None:
    response = client.post(
        "/decide",
        json={
            "customer_id": "CUST_1001",
            "message": "My IMPS transfer failed. Should I retry?",
            "demo_case_id": "failed_transaction_cooling_period",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["readiness_decision"] == "COOLING_PERIOD_ACTIVE"
    assert data["receipt"]["receipt_id"] == "SBI-DAS-TXN-0001"

    staff = client.get(f"/staff-view/{data['receipt']['receipt_id']}")
    assert staff.status_code == 200
    assert staff.json()["decision"] == "COOLING_PERIOD_ACTIVE"
