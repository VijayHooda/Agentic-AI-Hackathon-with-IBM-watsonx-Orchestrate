# main.py
# FastAPI app implementing the orchestrator demo + mock external services.

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import difflib
import uuid
import datetime
from sample_data import PAST_DEALS

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------
# Utilities / Simple "LLM" placeholders
# ---------------------------

def extract_context_from_lead(lead: dict) -> dict:
    """
    Extract structured fields from raw lead using simple heuristics.
    Replace this with watsonx LLM call for production.
    """
    name = lead.get("contact_name") or "Unknown"
    company = lead.get("company") or "Unknown"
    notes = lead.get("notes", "")
    pain = lead.get("painpoints", "")
    # simple priority heuristic
    priority = "High" if "infra" in pain.lower() or "cloud" in pain.lower() or "security" in pain.lower() else "Normal"
    return {
        "lead_id": lead.get("lead_id", str(uuid.uuid4())[:8]),
        "company": company,
        "contact_name": name,
        "priority": priority,
        "summary": f"{name} at {company}: {pain} | {notes}"
    }

def find_similar_deals(summary: str, top_k: int = 3) -> list:
    """
    Use difflib SequenceMatcher to find 'similar' past deals.
    Replace with vector search (Qdrant) or watsonx retrieval skill in production.
    """
    matches = []
    for d in PAST_DEALS:
        score = difflib.SequenceMatcher(None, summary.lower(), d["summary"].lower()).ratio()
        matches.append((score, d))
    matches.sort(key=lambda x: x[0], reverse=True)
    return [{"score": round(m[0], 3), **m[1]} for m in matches[:top_k]]

def plan_next_step(context: dict, similar_cases: list) -> dict:
    """
    Decide next action based on priority & similar cases.
    This is a simple planner; replace with orchestrator planning skill when integrating watsonx.
    """
    if context["priority"] == "High":
        action = "Schedule 30m demo"
        eta = "2 hours"
    else:
        action = "Send introductory email"
        eta = "6 hours"
    rationale = "Priority-driven. Similar cases: " + ", ".join([c["deal_id"] for c in similar_cases])
    return {"recommended_action": action, "eta": eta, "rationale": rationale}

def draft_email_lead(context: dict, plan: dict) -> dict:
    """
    Draft a simple outreach email. Replace with watsonx LLM 'email drafting' skill.
    """
    subject = f"Quick intro — {context['company']} & solution fit"
    body = (
        f"Hi {context['contact_name']},\n\n"
        f"I saw your note about {context['summary']}. We help companies like yours reduce infra costs and accelerate time-to-market.\n\n"
        f"Recommended next step: {plan['recommended_action']} (ETA: {plan['eta']}).\n\n"
        "Would you be available for a 30-minute demo this week?\n\n"
        "Best,\nSales Team\n"
    )
    return {"subject": subject, "body": body}

# ---------------------------
# In-memory "analytics" store and audit log
# ---------------------------
ANALYTICS = {
    "leads_processed": 0,
    "auto_actions": 0,
    "timestamps": []
}
AUDIT_LOG = []

# ---------------------------
# API Endpoints
# ---------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/lead")
async def api_lead(request: Request):
    payload = await request.json()
    # Step 1: Extract context
    context = extract_context_from_lead(payload)
    # Step 2: Find similar cases
    similar = find_similar_deals(context["summary"])
    # Step 3: Plan next step
    plan = plan_next_step(context, similar)
    # Step 4: Draft email
    draft = draft_email_lead(context, plan)
    # record analytics
    ANALYTICS["leads_processed"] += 1
    ANALYTICS["timestamps"].append(datetime.datetime.utcnow().isoformat())
    # record candidate audit for this suggestion
    suggestion = {
        "id": str(uuid.uuid4()),
        "context": context,
        "similar": similar,
        "plan": plan,
        "draft": draft,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    AUDIT_LOG.append({"event": "suggestion_created", "detail": suggestion, "ts": datetime.datetime.utcnow().isoformat()})
    return JSONResponse({"suggestion": suggestion, "analytics": ANALYTICS})

@app.post("/api/approve")
async def api_approve(request: Request):
    payload = await request.json()
    suggestion = payload.get("suggestion")
    editor_body = payload.get("edited_body") or suggestion["draft"]["body"]
    # Simulate action execution: update mock CRM, schedule calendar, push to outbox
    crm_result = mock_crm_update(suggestion)
    cal_result = mock_calendar_schedule(suggestion)
    outbox_result = mock_outbox_send(suggestion, editor_body)
    # analytics
    ANALYTICS["auto_actions"] += 1
    # audit
    audit_entry = {
        "event": "approved_and_executed",
        "suggestion_id": suggestion["id"],
        "crm_result": crm_result,
        "calendar_result": cal_result,
        "outbox_result": outbox_result,
        "edited_body": editor_body,
        "ts": datetime.datetime.utcnow().isoformat()
    }
    AUDIT_LOG.append(audit_entry)
    return JSONResponse({"status": "ok", "audit": audit_entry, "analytics": ANALYTICS})

# ---------------------------
# Mock external services
# ---------------------------

def mock_crm_update(suggestion: dict) -> dict:
    # Pretend to create a CRM entry
    crm_entry = {
        "crm_id": "CRM-" + suggestion["context"]["lead_id"],
        "company": suggestion["context"]["company"],
        "lead": suggestion["context"]["contact_name"],
        "status": "Contacted (pending)",
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    return crm_entry

def mock_calendar_schedule(suggestion: dict) -> dict:
    # Pretend to schedule a 30m demo
    start = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    cal = {
        "event_id": "EVT-" + suggestion["context"]["lead_id"],
        "start": start.isoformat(),
        "duration_min": 30,
        "title": f"Demo with {suggestion['context']['company']}"
    }
    return cal

def mock_outbox_send(suggestion: dict, body: str) -> dict:
    # Pretend to push email to outbox
    out = {
        "outbox_id": "OUT-" + suggestion["context"]["lead_id"],
        "to": suggestion["context"]["contact_name"],
        "subject": suggestion["draft"]["subject"],
        "body": body,
        "sent": False,  # demo: not actually sent
        "queued_at": datetime.datetime.utcnow().isoformat()
    }
    return out

@app.get("/api/analytics")
async def api_analytics():
    return JSONResponse(ANALYTICS)

@app.get("/api/audit")
async def api_audit():
    # small convenience endpoint to retrieve audit log
    return JSONResponse({"audit": AUDIT_LOG[-20:]})

# ---------------------------
# Example: where to plug IBM watsonx calls
# ---------------------------

# In production you would replace extract_context_from_lead / draft_email_lead logic
# with calls to watsonx LLM or call watsonx Orchestrate agent endpoints.
# Example pseudocode:
#
# import httpx
# async def call_watsonx(prompt: str) -> dict:
#     url = "https://api.ibm.com/watsonx/..."  # example - replace with real endpoint
#     headers = {"Authorization": f"Bearer {WATSONX_KEY}", "Content-Type": "application/json"}
#     payload = {"prompt": prompt, "max_tokens": 400}
#     async with httpx.AsyncClient() as client:
#         r = await client.post(url, headers=headers, json=payload)
#         return r.json()
#
# Use call_watsonx inside extract_context_from_lead or a separate orchestration layer.

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
