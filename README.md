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
