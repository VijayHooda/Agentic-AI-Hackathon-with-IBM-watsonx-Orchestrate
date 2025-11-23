// static/app.js
async function getJSON(url, opts) {
  const r = await fetch(url, opts);
  return await r.json();
}

document.getElementById("runBtn").addEventListener("click", async () => {
  const company = document.getElementById("company").value || "Acme Cloud";
  const contact_name = document.getElementById("contact_name").value || "Jane Doe";
  const role = document.getElementById("role").value || "CTO";
  const painpoints = document.getElementById("painpoints").value || "High infra costs, cloud overspend";
  const notes = document.getElementById("notes").value || "";

  const lead = {
    "lead_id": "L-" + Math.random().toString(36).substring(2,8),
    "company": company,
    "contact_name": contact_name,
    "role": role,
    "painpoints": painpoints,
    "notes": notes
  };

  document.getElementById("suggestionArea").innerHTML = "<div class='card'>Processing…</div>";

  const res = await getJSON("/api/lead", {
    method: "POST",
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(lead)
  });

  showSuggestion(res.suggestion);
  updateAnalytics(res.analytics);
});

function showSuggestion(sug) {
  const s = sug.suggestion;
  const html = `
    <div class="card">
      <h3>Suggestion</h3>
      <p><strong>Lead:</strong> ${s.context.contact_name} @ ${s.context.company}</p>
      <p><strong>Priority:</strong> ${s.context.priority}</p>
      <p><strong>Plan:</strong> ${s.plan.recommended_action} (ETA: ${s.plan.eta})</p>
      <p><strong>Rationale:</strong> ${s.plan.rationale}</p>
      <h4>Similar past cases</h4>
      <ul>
        ${s.similar.map(x => `<li>${x.deal_id} — ${x.company} [score: ${x.score}] — ${x.outcome}</li>`).join('')}
      </ul>
      <h4>Draft Email</h4>
      <label>Subject</label>
      <input id="email_subject" value="${escapeHtml(s.draft.subject)}"/>
      <label>Body</label>
      <textarea id="email_body" rows="6">${escapeHtml(s.draft.body)}</textarea>
      <div style="margin-top:8px;">
        <button id="approveBtn">Approve & Execute</button>
      </div>
    </div>
  `;
  document.getElementById("suggestionArea").innerHTML = html;

  document.getElementById("approveBtn").addEventListener("click", async () => {
    const edited_body = document.getElementById("email_body").value;
    const payload = { suggestion: s, edited_body };
    const res = await getJSON("/api/approve", {
      method: "POST",
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    // show execution result
    const out = `
      <div class="card">
        <h3>Execution Result</h3>
        <pre>${JSON.stringify(res.audit, null, 2)}</pre>
        <p class="muted">Mock CRM/Calendar/Outbox updated (demo mode).</p>
      </div>
    `;
    document.getElementById("suggestionArea").innerHTML = out;
    updateAnalytics(res.analytics);
    loadAudit();
  });
}

function escapeHtml(unsafe) {
    return unsafe
         .replaceAll('&','&amp;')
         .replaceAll('<','&lt;')
         .replaceAll('>','&gt;');
}

async function updateAnalytics(analytics) {
  document.getElementById("analytics").innerText = JSON.stringify(analytics, null, 2);
}

async function loadAudit() {
  const r = await getJSON("/api/audit");
  document.getElementById("audit").innerText = JSON.stringify(r.audit, null, 2);
}
