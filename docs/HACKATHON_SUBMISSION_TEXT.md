# Hackathon Submission Text

## Project Title

SBI Digital Adoption Sentinel

## Pillar Selected

SBI Hackathon @ GFF 2026 - Pillar 02 Digital Adoption

## Brief Description

SBI Digital Adoption Sentinel is a governed digital action-readiness engine that helps customers complete blocked digital banking journeys. It identifies the customer's journey, checks available customer-state evidence such as KYC status, account status, consent state, transaction status, limits, cooling periods, document completeness, and review flags, applies configurable SOP/rule logic, recommends the next safe step, and generates a Digital Action Receipt.

The MVP focuses on three high-friction digital adoption journeys: failed transaction recovery, nominee update readiness, and Account Aggregation consent readiness. The system does not autonomously execute banking actions or make sensitive eligibility/risk decisions. The LLM supports intent extraction and customer-friendly explanation, while the rule engine determines the readiness decision. Each output becomes a reviewable decision record for customer clarity, staff consistency, and audit-friendly traceability.

## Proposed Solution / Business Model

The solution can be embedded into SBI digital channels, staff assistance screens, or call-centre workflows as a bounded AI-assisted readiness and recovery layer. It reduces repeated failed attempts, avoidable branch visits, and inconsistent guidance while increasing trust in digital journeys.

## Technology Stack

```text
Python
FastAPI
Pydantic
pytest
Uvicorn
Deterministic configurable rule engine
Simple HTML demo UI
```

## Process Flow / Architecture

```text
Customer / Staff Request
-> Intent & Journey Classifier
-> Customer-State Evidence Manifest
-> Configurable SOP / Rule Simulator
-> Readiness Decision Engine
-> Safe Next-Step Router
-> Plain-Language Explanation Layer
-> Digital Action Receipt Generator
-> Staff / Review View
-> Guided Completion / Escalation Recommendation
```

## Demo Video Script

1. Open the home demo screen.
2. Select `failed_transaction_cooling_period`.
3. Show the customer request and decision `COOLING_PERIOD_ACTIVE`.
4. Show evidence checked, next safe step, Digital Action Receipt, and staff/review view.
5. Repeat briefly for nominee update and Account Aggregation consent.
6. Close with the AI boundary: The model interprets and explains. The rule engine decides. The receipt records.

## GitHub Repository Link

https://github.com/vikramlaishram-lang/sbi-digital-adoption-sentinel

## Claim Boundary

This MVP does not execute banking actions. It does not connect to real SBI systems. It does not claim access to SBI internal SOPs. It uses configurable demo SOP/rule logic. It does not make sensitive eligibility, risk, approval, or limit decisions using an LLM.

The MVP creates audit-friendly, reviewable decision records. It is not a production decision system and does not approve or reject banking actions.
