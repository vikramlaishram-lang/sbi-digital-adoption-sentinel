from __future__ import annotations

import subprocess
import sys


def test_smoke_demo_script() -> None:
    result = subprocess.run([sys.executable, "scripts/smoke_demo.py"], check=True, capture_output=True, text=True)
    output = result.stdout

    assert "SMOKE_DEMO_PASS: true" in output
    assert "FAILED_TRANSACTION_DECISION: COOLING_PERIOD_ACTIVE" in output
    assert "NOMINEE_UPDATE_DECISION: DOCUMENT_MISSING" in output
    assert "ACCOUNT_AGGREGATION_DECISION: CONSENT_REQUIRED" in output
