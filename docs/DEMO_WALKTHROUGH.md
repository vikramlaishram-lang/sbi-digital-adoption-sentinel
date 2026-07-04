# Demo Walkthrough

Use this walkthrough for judges and for a 3-minute recording. Keep the story focused: the product does not execute banking actions; it diagnoses readiness and produces a reviewable Digital Action Receipt.

## Demo Pattern

Say this at the start:

```text
The MVP demonstrates three blocked digital banking journeys. I will run one customer request for each journey.
```

Use the same customer request box three times:

```text
Question 1 -> COOLING_PERIOD_ACTIVE
Question 2 -> DOCUMENT_MISSING
Question 3 -> CONSENT_REQUIRED
```

Do not make one customer question trigger all three decisions. The correct proof is:

```text
Three customer questions
-> three journey classifications
-> three readiness decisions
-> three Digital Action Receipts
```

## Three Demo Questions

| Customer question | Barrier shown | Expected journey | Expected decision | Expected receipt |
| --- | --- | --- | --- | --- |
| My IMPS transfer failed. Should I retry? | Payment recovery / trust | `failed_transaction_recovery` | `COOLING_PERIOD_ACTIVE` | `SBI-DAS-TXN-0001` |
| I want to add a nominee online. | Digital service completion | `nominee_update_readiness` | `DOCUMENT_MISSING` | `SBI-DAS-NOM-0002` |
| I want to link another bank account. | Consent-based adoption | `account_aggregation_consent_readiness` | `CONSENT_REQUIRED` | `SBI-DAS-AA-0003` |

## 3-Minute Recording Flow

```text
0:00-0:20 Opening
0:20-1:05 Failed transaction recovery
1:05-1:40 Nominee update readiness
1:40-2:15 Account Aggregation consent readiness
2:15-2:45 Digital Action Receipt + staff/review view
2:45-3:00 Closing
```

## 1. Failed Transaction Recovery -> COOLING_PERIOD_ACTIVE

This is the hero demo.

Customer request:

```text
"My IMPS transfer failed. Should I retry?"
```

Detected journey:

```text
failed_transaction_recovery
```

Evidence checked:

```text
payment_rail = IMPS
transaction_status = failed
debit_status = not_debited
beneficiary_status = newly_added
cooling_period_active = true
requested_amount = 75000
permitted_cooling_period_limit = 25000
daily_limit_exceeded = false
risk_review_flag = false
temporary_service_issue = false
reversal_status = not_required
```

Rule basis:

```text
failed_transaction.new_beneficiary_cooling_period
```

Readiness decision:

```text
COOLING_PERIOD_ACTIVE
```

Reason:

```text
The beneficiary was recently added and the safety cooling period is still active.
```

Safe next step:

```text
Wait until the cooling period ends or proceed within the permitted limit.
```

Digital Action Receipt ID:

```text
SBI-DAS-TXN-0001
```

Staff/review view summary:

```text
Shows the journey, decision, evidence-field count, matched rule basis, no missing items, no escalation required, and no branch visit required.
```

## 2. Nominee Update Readiness -> DOCUMENT_MISSING

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
account_type = savings
account_status = active
kyc_status = complete
mobile_verified = true
online_nominee_update_allowed = true
nominee_name_present = true
nominee_dob_present = false
nominee_relationship_present = false
minor_nominee = false
guardian_details_present = false
consent_declaration_done = false
risk_review_flag = false
```

Rule basis:

```text
nominee_update.required_details_missing
```

Readiness decision:

```text
DOCUMENT_MISSING
```

Reason:

```text
Required nominee details or declaration are missing.
```

Safe next step:

```text
Complete the missing details or declaration before submission.
```

Digital Action Receipt ID:

```text
SBI-DAS-NOM-0002
```

Staff/review view summary:

```text
Shows missing nominee_date_of_birth, nominee_relationship, and consent_declaration with no branch visit required.
```

## 3. Account Aggregation Consent Readiness -> CONSENT_REQUIRED

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
risk_review_flag = false
```

Rule basis:

```text
account_aggregation.consent_absent
```

Readiness decision:

```text
CONSENT_REQUIRED
```

Reason:

```text
No active consent exists for account data sharing.
```

Safe next step:

```text
Review and approve the consent scope before linking the account.
```

Digital Action Receipt ID:

```text
SBI-DAS-AA-0003
```

Staff/review view summary:

```text
Shows consent requirement, evidence-field count, matched rule basis, no branch visit required, and no escalation required.
```

## Do Not Say

- real SBI integration
- real SBI SOP access
- autonomous banking execution
- approval or rejection of banking actions
- replacement for SBI staff

## Say

- configurable demo SOP/rule logic
- mock/customer-state evidence
- readiness decision
- safe next step
- reviewable Digital Action Receipt
