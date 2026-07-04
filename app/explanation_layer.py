from __future__ import annotations

from .models import DigitalActionEnvelope, MODEL_BOUNDARY_NOTE


def customer_explanation(envelope: DigitalActionEnvelope) -> str:
    return f"{envelope.reason} Next safe step: {envelope.next_safe_step}"


def model_boundary_note() -> str:
    return MODEL_BOUNDARY_NOTE
