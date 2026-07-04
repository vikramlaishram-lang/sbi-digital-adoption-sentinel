# Architecture

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

The rule engine is deterministic. The LLM boundary is intentionally narrow and optional.
