# API Examples

Run the app first:

```bash
uvicorn app.main:app --reload
```

## GET /health

```bash
curl http://127.0.0.1:8000/health
```

Expected key output:

```json
{
  "status": "ok",
  "product": "SBI Digital Adoption Sentinel"
}
```

## GET /demo-cases

```bash
curl http://127.0.0.1:8000/demo-cases
```

Expected key output:

```json
[
  "failed_transaction_cooling_period",
  "nominee_update_missing_details",
  "account_aggregation_consent_required"
]
```

## POST /decide - failed_transaction_cooling_period

Request:

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST_1001","message":"My IMPS transfer failed. Should I retry?","demo_case_id":"failed_transaction_cooling_period"}'
```

Request JSON:

```json
{
  "customer_id": "CUST_1001",
  "message": "My IMPS transfer failed. Should I retry?",
  "demo_case_id": "failed_transaction_cooling_period"
}
```

Expected key output:

```text
journey = failed_transaction_recovery
readiness_decision = COOLING_PERIOD_ACTIVE
next_safe_step = Wait until the cooling period ends or proceed within the permitted limit.
receipt_id = SBI-DAS-TXN-0001
model_boundary_note = The model interprets and explains. The rule engine decides. The receipt records.
```

## POST /decide - nominee_update_missing_details

Request:

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST_2002","message":"I want to add a nominee online.","demo_case_id":"nominee_update_missing_details"}'
```

Request JSON:

```json
{
  "customer_id": "CUST_2002",
  "message": "I want to add a nominee online.",
  "demo_case_id": "nominee_update_missing_details"
}
```

Expected key output:

```text
journey = nominee_update_readiness
readiness_decision = DOCUMENT_MISSING
next_safe_step = Complete the missing details or declaration before submission.
receipt_id = SBI-DAS-NOM-0002
model_boundary_note = The model interprets and explains. The rule engine decides. The receipt records.
```

## POST /decide - account_aggregation_consent_required

Request:

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST_3003","message":"I want to link another bank account.","demo_case_id":"account_aggregation_consent_required"}'
```

Request JSON:

```json
{
  "customer_id": "CUST_3003",
  "message": "I want to link another bank account.",
  "demo_case_id": "account_aggregation_consent_required"
}
```

Expected key output:

```text
journey = account_aggregation_consent_readiness
readiness_decision = CONSENT_REQUIRED
next_safe_step = Review and approve the consent scope before linking the account.
receipt_id = SBI-DAS-AA-0003
model_boundary_note = The model interprets and explains. The rule engine decides. The receipt records.
```

## GET /receipts/{receipt_id}

Create a receipt first with `POST /decide`, then run:

```bash
curl http://127.0.0.1:8000/receipts/SBI-DAS-TXN-0001
```

Expected key output:

```text
receipt_id = SBI-DAS-TXN-0001
classified_journey = failed_transaction_recovery
readiness_decision = COOLING_PERIOD_ACTIVE
record_hash = sha256:...
```

## GET /staff-view/{receipt_id}

Create a receipt first with `POST /decide`, then run:

```bash
curl http://127.0.0.1:8000/staff-view/SBI-DAS-TXN-0001
```

Expected key output:

```text
receipt_id = SBI-DAS-TXN-0001
journey = failed_transaction_recovery
decision = COOLING_PERIOD_ACTIVE
missing_items = []
escalation_required = false
branch_visit_required = false
```
