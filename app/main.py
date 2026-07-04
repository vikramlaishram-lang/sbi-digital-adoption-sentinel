from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from .demo_data_loader import load_demo_cases
from .explanation_layer import customer_explanation
from .models import CustomerRequest
from .readiness_decision_engine import decide_readiness
from .receipt_generator import generate_receipt, staff_view_from_receipt


app = FastAPI(title="SBI Digital Adoption Sentinel")
RECEIPTS: dict[str, dict] = {}


@app.get("/", response_class=HTMLResponse)
def demo_page() -> str:
    cases = load_demo_cases()
    options = "\n".join(f"<option value='{case_id}'>{case_id}</option>" for case_id in cases)
    return f"""
<!doctype html>
<html>
<head>
  <title>SBI Digital Adoption Sentinel</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #17202a; }}
    textarea, select, input {{ width: 100%; padding: 8px; margin: 6px 0 14px; }}
    button {{ padding: 10px 14px; }}
    pre {{ background: #f4f6f8; padding: 16px; overflow: auto; white-space: pre-wrap; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
    .pitch {{ max-width: 980px; line-height: 1.45; }}
  </style>
</head>
<body>
  <h1>SBI Digital Adoption Sentinel</h1>
  <p><strong>Pillar 02: Digital Adoption</strong></p>
  <p class="pitch">SBI Digital Adoption Sentinel turns blocked digital banking journeys into clear, safe, reviewable next steps using intent classification, customer-state evidence, SOP rules, readiness decisions, and Digital Action Receipts.</p>
  <div class="grid">
    <section>
      <h2>Customer Request</h2>
      <label>Demo case selector</label>
      <select id="case">{options}</select>
      <label>Customer message</label>
      <textarea id="message">My IMPS transfer failed. Should I retry?</textarea>
      <button onclick="decide()">Decide Readiness</button>
    </section>
    <section>
      <h2>Decision, Receipt, and Staff Review View</h2>
      <pre id="output">Run a demo case to see:
- Customer request
- Detected journey
- Evidence checklist
- Decision
- Next safe step
- Receipt ID
- Staff/review view</pre>
    </section>
  </div>
  <script>
    async function decide() {{
      const body = {{
        customer_id: "CUST_DEMO",
        message: document.getElementById("message").value,
        demo_case_id: document.getElementById("case").value
      }};
      const response = await fetch("/decide", {{method: "POST", headers: {{"Content-Type": "application/json"}}, body: JSON.stringify(body)}});
      const data = await response.json();
      const staff = await fetch("/staff-view/" + data.receipt.receipt_id).then(r => r.json());
      const evidence = Object.entries(data.evidence_checked).map(([key, value]) => `- ${{key}}: ${{value}}`).join("\\n");
      document.getElementById("output").textContent =
`Customer request:
${{body.message}}

Detected journey:
${{data.journey}}

Evidence checked:
${{evidence}}

Decision: ${{data.readiness_decision}}

Reason:
${{data.reason}}

Safe next step:
${{data.next_safe_step}}

Receipt ID:
${{data.receipt.receipt_id}}

Digital Action Receipt content:
${{JSON.stringify(data.receipt, null, 2)}}

Staff/review view:
${{JSON.stringify(staff, null, 2)}}

Model boundary note:
${{data.receipt.model_boundary_note}}`;
    }}
  </script>
</body>
</html>
"""


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "product": "SBI Digital Adoption Sentinel"}


@app.get("/demo-cases")
def demo_cases() -> list[str]:
    return list(load_demo_cases().keys())


@app.post("/decide")
def decide(request: CustomerRequest) -> dict:
    envelope = decide_readiness(request)
    receipt = generate_receipt(envelope)
    receipt_dict = receipt.model_dump(mode="json")
    RECEIPTS[receipt.receipt_id] = receipt_dict
    return {
        "journey": envelope.classified_journey,
        "readiness_decision": envelope.readiness_decision,
        "reason": envelope.reason,
        "next_safe_step": envelope.next_safe_step,
        "explanation": customer_explanation(envelope),
        "evidence_checked": envelope.evidence_checked,
        "receipt": receipt_dict,
    }


@app.get("/receipts/{receipt_id}")
def receipt_lookup(receipt_id: str) -> dict:
    if receipt_id not in RECEIPTS:
        raise HTTPException(status_code=404, detail="receipt not found")
    return RECEIPTS[receipt_id]


@app.get("/staff-view/{receipt_id}")
def staff_view(receipt_id: str) -> dict:
    if receipt_id not in RECEIPTS:
        raise HTTPException(status_code=404, detail="receipt not found")
    from .models import DigitalActionReceipt

    receipt = DigitalActionReceipt(**RECEIPTS[receipt_id])
    return staff_view_from_receipt(receipt)
