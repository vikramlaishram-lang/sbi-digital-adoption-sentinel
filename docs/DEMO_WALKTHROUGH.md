# Demo Walkthrough

## 1. Failed Transaction Recovery - COOLING_PERIOD_ACTIVE

Customer request:

```text
My IMPS transfer failed. Should I retry?
```

Detected journey:

```text
failed_transaction_recovery
```

Evidence checked:

```text
payment_rail = IMPS
debit_status = not_debited
beneficiary_status = newly_added
cooling_period_active = true
requested_amount = 75000
permitted_cooling_period_limit = 25000
daily_limit_exceeded = false
risk_review_flag = false
temporary_service_issue = false
```

Rule applied:

```text
failed_transaction.new_beneficiary_cooling_period
```

Readiness decision:

```text
COOLING_PERIOD_ACTIVE
```

Next safe step:

```text
Wait until the cooling period ends or proceed within the permitted limit.
```

Digital Action Receipt ID:

```text
SBI-DAS-TXN-0001
```

Staff/review view:

```text
Evidence summary, rule basis, missing items, escalation flag, and branch visit flag.
```

## 2. Nominee Update Readiness - DOCUMENT_MISSING

Customer request:

```text
I want to add a nominee online.
```

Detected journey:

```text
nominee_update_readiness
```

Evidence checked:

```text
kyc_status = complete
mobile_verified = true
online_nominee_update_allowed = true
nominee_name_present = true
nominee_dob_present = false
nominee_relationship_present = false
consent_declaration_done = false
```

Rule applied:

```text
nominee_update.required_details_missing
```

Readiness decision:

```text
DOCUMENT_MISSING
```

Next safe step:

```text
Complete nominee details and declaration before submission.
```

Digital Action Receipt ID:

```text
SBI-DAS-NOM-0002
```

Staff/review view:

```text
Missing nominee date of birth, nominee relationship, and consent declaration.
```

## 3. Account Aggregation Consent Readiness - CONSENT_REQUIRED

Customer request:

```text
I want to link another bank account.
```

Detected journey:

```text
account_aggregation_consent_readiness
```

Evidence checked:

```text
aa_consent_status = absent
consent_expired = false
selected_institution_supported = true
mobile_kyc_match = true
data_fetch_ready = true
consent_scope_acknowledged = false
```

Rule applied:

```text
account_aggregation.consent_absent
```

Readiness decision:

```text
CONSENT_REQUIRED
```

Next safe step:

```text
Review and approve the consent scope before linking the account.
```

Digital Action Receipt ID:

```text
SBI-DAS-AA-0003
```

Staff/review view:

```text
Consent requirement, evidence summary, escalation flag, and branch visit flag.
```
