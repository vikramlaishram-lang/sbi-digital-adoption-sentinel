# API Examples

## GET /health

```bash
curl http://127.0.0.1:8000/health
```

Response:

```json
{"status":"ok","product":"SBI Digital Adoption Sentinel"}
```

## GET /demo-cases

```bash
curl http://127.0.0.1:8000/demo-cases
```

Response includes:

```json
["failed_transaction_cooling_period","nominee_update_missing_details","account_aggregation_consent_required"]
```

## POST /decide - Failed Transaction

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST_1001","message":"My IMPS transfer failed. Should I retry?","demo_case_id":"failed_transaction_cooling_period"}'
```

Key response fields:

```json
{
  "journey": "failed_transaction_recovery",
  "readiness_decision": "COOLING_PERIOD_ACTIVE",
  "receipt": {"receipt_id": "SBI-DAS-TXN-0001"}
}
```

## POST /decide - Nominee Update

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST_2002","message":"I want to add a nominee online.","demo_case_id":"nominee_update_missing_details"}'
```

Key response fields:

```json
{
  "journey": "nominee_update_readiness",
  "readiness_decision": "DOCUMENT_MISSING",
  "receipt": {"receipt_id": "SBI-DAS-NOM-0002"}
}
```

## POST /decide - Account Aggregation

```bash
curl -X POST http://127.0.0.1:8000/decide \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST_3003","message":"I want to link another bank account.","demo_case_id":"account_aggregation_consent_required"}'
```

Key response fields:

```json
{
  "journey": "account_aggregation_consent_readiness",
  "readiness_decision": "CONSENT_REQUIRED",
  "receipt": {"receipt_id": "SBI-DAS-AA-0003"}
}
```

## GET /receipts/{receipt_id}

```bash
curl http://127.0.0.1:8000/receipts/SBI-DAS-TXN-0001
```

Returns the generated Digital Action Receipt if it has been created during the current app session.

## GET /staff-view/{receipt_id}

```bash
curl http://127.0.0.1:8000/staff-view/SBI-DAS-TXN-0001
```

Returns:

```json
{
  "receipt_id": "SBI-DAS-TXN-0001",
  "journey": "failed_transaction_recovery",
  "decision": "COOLING_PERIOD_ACTIVE",
  "missing_items": [],
  "escalation_required": false,
  "branch_visit_required": false
}
```
