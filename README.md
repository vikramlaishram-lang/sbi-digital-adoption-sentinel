# SBI Digital Adoption Sentinel

Pillar: SBI Hackathon @ GFF 2026 - Pillar 02 Digital Adoption

SBI Digital Adoption Sentinel turns blocked digital banking journeys into clear, safe, reviewable next steps using intent classification, customer-state evidence, SOP rules, readiness decisions, and Digital Action Receipts.

## Product

SBI Digital Adoption Sentinel is a governed digital action-readiness engine that helps customers complete blocked digital banking journeys by identifying the journey, checking available customer-state evidence, applying configurable SOP/rule logic, recommending the next safe step, and generating a Digital Action Receipt.

## Problem

Customers abandon digital journeys when they see unclear messages like `transaction failed`, `try again later`, or `visit branch`. The MVP explains what is blocking the journey and what safe next step is available.

## MVP Journeys

- Failed transaction recovery
- Nominee update readiness
- Account Aggregation consent readiness

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
pytest -q
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

## Demo Cases

- `failed_transaction_cooling_period`
- `nominee_update_missing_details`
- `account_aggregation_consent_required`

## AI Boundary

```text
The model interprets and explains.
The rule engine decides.
The receipt records.
```

The LLM supports intent extraction, conversation flow, explanation, and receipt summarisation. It does not decide eligibility, limits, risk, approvals, or banking execution.

## Claim Boundary

This MVP does not execute banking actions, connect to real SBI systems, claim access to SBI internal SOPs, or use an LLM for sensitive decisions. It uses configurable demo SOP/rule logic.
