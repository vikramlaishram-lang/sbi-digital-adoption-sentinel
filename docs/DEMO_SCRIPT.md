# Demo Script

## 1. Failed transaction recovery - cooling period active

Intent: My IMPS transfer failed. Should I retry?

Evidence: newly added beneficiary, cooling period active, requested amount above permitted cooling-period limit.

Policy/rule: `failed_transaction.new_beneficiary_cooling_period`

Decision: `COOLING_PERIOD_ACTIVE`

Safe next step: Wait until the cooling period ends or proceed within the permitted limit.

Receipt: `SBI-DAS-TXN-0001`

Staff/review view: shows checked evidence, rule basis, decision, and no branch visit requirement.

## 2. Nominee update readiness - missing nominee details

Intent: I want to add a nominee online.

Evidence: KYC complete, online nominee update allowed, nominee DOB missing, relationship missing, declaration missing.

Policy/rule: `nominee_update.required_details_missing`

Decision: `DOCUMENT_MISSING`

Safe next step: Complete nominee details and declaration before submission.

Receipt: `SBI-DAS-NOM-0002`

Staff/review view: shows missing items and no branch visit requirement.

## 3. Account Aggregation consent readiness - consent required

Intent: I want to link another bank account.

Evidence: consent absent, institution supported, mobile/KYC match true, data fetch ready.

Policy/rule: `account_aggregation.consent_absent`

Decision: `CONSENT_REQUIRED`

Safe next step: Review and approve the consent scope before linking the account.

Receipt: `SBI-DAS-AA-0003`

Staff/review view: shows consent requirement and no branch visit requirement.
