# SBI Digital Adoption Sentinel

Pillar: SBI Hackathon @ GFF 2026 - Pillar 02 Digital Adoption

## One-Line Pitch

SBI Digital Adoption Sentinel turns blocked digital banking journeys into clear, safe, reviewable next steps using intent classification, customer-state evidence, SOP rules, readiness decisions, and Digital Action Receipts.

## Problem

Customers often abandon digital banking journeys when they receive unclear messages such as `transaction failed`, `unable to process`, `try again later`, or `visit branch`. These messages do not explain the blocker, whether retry is safe, what requirement is missing, or when staff review is needed.

## Solution

SBI Digital Adoption Sentinel is a governed digital action-readiness engine. It identifies the customer's journey, checks available mock customer-state evidence, applies configurable demo SOP/rule logic, recommends the next safe step, and generates a Digital Action Receipt.

Core flow:

```text
Customer request
-> Digital journey classification
-> Customer-state evidence check
-> Configurable SOP/rule evaluation
-> Readiness decision
-> Safe next step
-> Digital Action Receipt
```

## MVP Journeys

- Failed Transaction Recovery: `COOLING_PERIOD_ACTIVE`
- Nominee Update Readiness: `DOCUMENT_MISSING`
- Account Aggregation Consent Readiness: `CONSENT_REQUIRED`

## Architecture

```text
Customer / Staff Request
        |
Intent & Journey Classifier
        |
Customer-State Evidence Manifest
        |
Configurable SOP / Rule Simulator
        |
Readiness Decision Engine
        |
Safe Next-Step Router
        |
Plain-Language Explanation Layer
        |
Digital Action Receipt Generator
        |
Staff / Review View
        |
Guided Completion / Escalation Recommendation
```

## Windows Quickstart Without Activation

If PowerShell activation is blocked or confusing, use the virtual environment's Python directly:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\smoke_demo.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

Optional activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation fails, use the no-activation commands above.

## macOS/Linux Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python scripts/smoke_demo.py
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

## API Examples

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/demo-cases
```

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST_1001","message":"My IMPS transfer failed. Should I retry?","demo_case_id":"failed_transaction_cooling_period"}'
```

More examples are in [docs/API_EXAMPLES.md](docs/API_EXAMPLES.md).

## Demo Flow

1. Choose `failed_transaction_cooling_period`.
2. Submit the customer request.
3. Review detected journey, evidence checklist, decision, next safe step, receipt ID, and staff/review view.
4. Repeat for nominee update and Account Aggregation consent.

The failed transaction journey is the hero demo.

## Digital Action Receipt And Staff View

Every readiness decision generates a Digital Action Receipt with:

```text
receipt ID
customer request
classified journey
evidence checked
rule basis
readiness decision
reason
next safe step
model boundary note
record hash
```

The staff/review view summarizes the same decision for consistent assisted-channel handling.

## AI Boundary

```text
The model interprets and explains. The rule engine decides. The receipt records.
```

The LLM may support intent extraction, conversation flow, explanation, and receipt summarisation. It does not decide eligibility, limits, risk, approvals, or banking execution.

## Claim Boundary

This MVP does not execute banking actions, connect to real SBI systems, claim access to SBI internal SOPs, or use an LLM for sensitive decisions. It uses configurable demo SOP/rule logic.

The MVP is a readiness and recovery layer for digital adoption, not a production banking decision system.
