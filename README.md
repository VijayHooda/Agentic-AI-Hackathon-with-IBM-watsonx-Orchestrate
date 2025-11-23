# Agentic Sales Ops Agent — Demo (FastAPI)

Small demo project for the Agentic AI Hackathon (IBM watsonx Orchestrate).
This repository demonstrates an agentic orchestration flow: lead intake → context extraction → retrieval → plan → draft → human approval → mock execution.

## What this includes
- FastAPI backend with endpoints:
  - `GET /` → demo UI
  - `POST /api/lead` → run the agent pipeline (returns suggestion)
  - `POST /api/approve` → approve & execute suggestion (mock CRM/calendar/outbox)
  - `GET /api/analytics` and `GET /api/audit` → debug
- Simple frontend UI in `templates/index.html` + `static/app.js`
- Mock dataset in `sample_data.py`

## Run locally (30–60 seconds)
1. Install Python 3.10+ and create a venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
Start the app:

bash
Copy code
uvicorn main:app --reload --port 8000
Open http://localhost:8000 in your browser.

How to replace placeholders with IBM watsonx Orchestrate / watsonx LLM
Replace extract_context_from_lead and draft_email_lead with calls to watsonx LLM or call an orchestration agent via watsonx Orchestrate APIs.

Example approach:

Use watsonx Orchestrate to register skills: context extraction, retrieval (vector), planner, draft generator, executor.

Trigger the orchestrate flow from /api/lead (make HTTP request or webhook).

In the mock_* functions, replace with real CRM/calendar API calls (Salesforce, HubSpot, Google Calendar).

Demo Scenarios
Try inputting:

Company: Acme Cloud, Contact: Jane Doe, Painpoints: High infra cost, cloud spend optimization

Company: RetailCorp, Contact: Mike Retail, Painpoints: Real-time inventory analytics

Submission checklist
Backup video of demo

README with run steps (this file)

Basic slides (6) describing problem, solution, architecture, demo & impact

Link to repo in hackathon submission

Notes
This is a demo skeleton intended to be completed and hardened for production.

Use synthetic or anonymized data for hackathon demos to avoid PHI/PII issues.

Good luck — smash the demo.

yaml
Copy code

---

# How to use / demo (quick)

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload --port 8000`
4. Open http://localhost:8000
5. Enter a lead (try the sample inputs in README). Click **Run Agent**. Review the suggested email, edit if desired, then **Approve & Execute**. The UI will show mock CRM/Calendar/Outbox execution and analytics.

---

# Where to plug IBM watsonx Orchestrate / watsonx LLM (explicit)

- `main.py` functions to replace:
  - `extract_context_from_lead(lead)` — replace with a watsonx LLM or call to a watsonx Orchestrate extract skill. Send the lead text, ask for JSON structured output (company, contact, priority, key_pain).
  - `find_similar_deals(summary)` — replace with a Qdrant/semantic retrieval skill; feed vector embeddings from model used by watsonx.
  - `plan_next_step(context, similar_cases)` — you can use watsonx Orchestrate planner skill to generate recommended next steps.
  - `draft_email_lead(context, plan)` — call a watsonx LLM to produce professional email subject + body, constrained with templates and safety rules.
  - In `/api/approve` execution, call watsonx Orchestrate's executor agent (or directly call CRM/calendar APIs).

I included commented example pseudocode in `main.py` demonstrating how to call an external LLM endpoint using `httpx`.

---

# Quick notes & judge-pleasing pointers (so you win this in 1 hour demo)

1. **Make partner tech visible**: In your pitch / slide deck say: “Our demo uses watsonx Orchestrate (planned) — local demo shows identical flow; presto.” If you have watsonx, call it in the extraction and drafting functions.
2. **Metrics**: Use the analytics endpoint to show `leads_processed` and `auto_actions` – say "in simulation we save X minutes per lead".
3. **Human in loop**: The judge will love the approve/edit step — it shows responsibility and production realism.
4. **Backup video**: Record a short screencast of the demo (2–3 min) — if live demo flops, judges will still see flow.
5. **Slides**: 6 slides: Problem → Solution → Architecture (Mermaid) → Live Demo snapshots → Metrics & Business value → Roadmap & Ask.

---

If you want now, I can:

- Generate a **6-slide deck** (content + speaker notes) in the next 3–6 minutes.
- Produce a short **2-3 minute backup demo script** and sample narration for your recorded video.
- Swap out the placeholder LLM parts with a **concrete watsonx Orchestrate request template** if you give me your watsonx API shape (or I can draft based on common IBM patterns).

Which of those should I do next?
::contentReference[oaicite:0]{index=0}
