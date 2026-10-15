/**
 * MexConsumerPulse Dashboard JavaScript
 * Handles data fetching, markdown rendering, filtering, and agent triggers.
 */

// State
let allProblems = [];
let latestReportData = null;

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initModals();
  initActions();
  initFilters();

  // Load initial data
  loadMetrics();
  loadLatestReport();
  loadProblems();
});

// 1. Tab Navigation
function initTabs() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

      tab.classList.add("active");
      const targetId = tab.getAttribute("data-tab");
      const targetContent = document.getElementById(targetId);
      if (targetContent) targetContent.classList.add("active");
    });
  });
}

// 2. Modals & Notifications
function initModals() {
  const fbModal = document.getElementById("fb-modal");
  const btnFbSession = document.getElementById("btn-fb-session");
  const btnClose = document.getElementById("btn-close-modal");
  const btnCancel = document.getElementById("btn-modal-cancel");
  const btnLaunch = document.getElementById("btn-modal-launch-fb");

  const openModal = () => fbModal.classList.add("active");
  const closeModal = () => fbModal.classList.remove("active");

  if (btnFbSession) btnFbSession.addEventListener("click", openModal);
  if (btnClose) btnClose.addEventListener("click", closeModal);
  if (btnCancel) btnCancel.addEventListener("click", closeModal);

  if (btnLaunch) {
    btnLaunch.addEventListener("click", () => {
      showToast("Launching headed browser for Facebook login...");
      closeModal();
      fetch("/api/agents/run/facebook", { method: "POST" })
        .then(() => showToast("Facebook browser process started! Check browser window."))
        .catch(err => showToast("Error: " + err.message));
    });
  }
}

function openFbModal() {
  const fbModal = document.getElementById("fb-modal");
  if (fbModal) fbModal.classList.add("active");
}

function showToast(message) {
  const toast = document.getElementById("toast");
  const msgElem = document.getElementById("toast-message");
  if (!toast || !msgElem) return;

  msgElem.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 4000);
}

// 3. Header Action Buttons
function initActions() {
  const btnRunSwarm = document.getElementById("btn-run-swarm");
  const btnExportCsv = document.getElementById("btn-export-csv");
  const btnDownloadMd = document.getElementById("btn-download-md");

  if (btnRunSwarm) {
    btnRunSwarm.addEventListener("click", () => {
      showToast("Triggering full autonomous agent swarm run...");
      fetch("/api/agents/run/all", { method: "POST" })
        .then(res => res.json())
        .then(data => {
          showToast("Swarm run initiated in background! Updating live data...");
          setTimeout(() => {
            loadMetrics();
            loadLatestReport();
            loadProblems();
          }, 4000);
        })
        .catch(err => showToast("Failed to run swarm: " + err.message));
    });
  }

  if (btnExportCsv) {
    btnExportCsv.addEventListener("click", () => {
      window.location.href = "/api/exports/csv";
    });
  }

  if (btnDownloadMd) {
    btnDownloadMd.addEventListener("click", () => {
      if (!latestReportData || !latestReportData.markdown_content) {
        showToast("No report currently available to download.");
        return;
      }
      const blob = new Blob([latestReportData.markdown_content], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `mexico_consumer_report_${latestReportData.report_date || "latest"}.md`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  // Regional Report Switcher
  const regionSelect = document.getElementById("select-report-region");
  if (regionSelect) {
    regionSelect.addEventListener("change", (e) => {
      const selected = e.target.value;
      showToast(`Loading ${selected} intelligence report...`);
      loadLatestReport(selected);
    });
  }

  initWhatsAppHandler();
}

function initWhatsAppHandler() {
  const btnLoadSample = document.getElementById("btn-wa-load-sample");
  const btnParse = document.getElementById("btn-wa-parse");
  const chatInput = document.getElementById("wa-chat-input");
  const groupInput = document.getElementById("wa-group-name");
  const cityInput = document.getElementById("wa-city");
  const resultsPanel = document.getElementById("wa-results-panel");
  const extractedGrid = document.getElementById("wa-extracted-problems");

  if (btnLoadSample) {
    btnLoadSample.addEventListener("click", () => {
      chatInput.value = `[14/10/26, 08:15:30] +52 55 9876 5432: Buenos días vecinos de Calle Ámsterdam. ¿A ustedes les está saliendo agua en los grifos? En el edificio 42 no cae ni una gota desde anoche.
[14/10/26, 08:17:10] Vecino Juan Depto 301: Hola, aquí en el 48 tampoco cae agua de Sacmex. Hablamos a la alcaldía y dicen que hay fuga principal en Insurgentes y van a tandeo todo el fin de semana.
[14/10/26, 08:22:45] Mariana Condesa: ¿Alguien tiene el contacto de una pipa de agua particular confiable? Los del teléfono de siempre quieren cobrar $2,200 pesos por 5,000 litros y dicen que tardan 8 horas en llegar.
[14/10/26, 09:30:12] +52 55 4321 8765: Oigan vecinos, aviso urgente: no contraten a un señor que se hace llamar 'Maestro Carlos' para reparar calentadores. Nos cobró $1,500 de anticipo de refacciones y nos dejó el boiler desarmado y ya no contesta las llamadas ni WhatsApp.
[14/10/26, 11:05:00] Alberto R: ¿Alguien sabe si CFE avisó de corte de luz para hoy? En la esquina de Parras se escuchó un tronido fuerte en el transformador y varios departamentos nos quedamos a oscuras.`;
      showToast("Sample Condesa chat loaded! Click 'Scrub & Ingest Chat' to process.");
    });
  }

  if (btnParse) {
    btnParse.addEventListener("click", async () => {
      const chatText = chatInput.value.trim();
      if (!chatText) {
        showToast("Please paste chat text or click 'Load Sample Chat'.");
        return;
      }

      showToast("Scrubbing PII and extracting problems via WhatsAppVecinosAgent...");
      try {
        const res = await fetch("/api/whatsapp/import", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_text: chatText,
            group_name: groupInput.value || "Chat de Vecinos",
            city: cityInput.value || "Mexico City (CDMX)"
          })
        });

        const data = await res.json();
        showToast(`Successfully extracted ${data.extracted_count} problems! Updating database...`);

        if (data.problems && data.problems.length > 0) {
          resultsPanel.style.display = "block";
          extractedGrid.innerHTML = data.problems.map(p => `
            <div class="problem-card">
              <div class="problem-card-header">
                <span class="problem-category-badge">${p.category}</span>
                <span class="problem-urgency">🔴🔴🔴🔴 ${p.urgency}/5</span>
              </div>
              <h4 class="problem-title">${escapeHtml(p.title)}</h4>
              <p class="problem-content">${escapeHtml(p.content)}</p>
              <div class="problem-meta-row">
                <span class="meta-pill">📍 ${escapeHtml(p.city)} (${escapeHtml(p.colonia || "General")})</span>
                <span class="meta-pill">🛡️ PII Scrubbed</span>
              </div>
              ${p.venture_concept ? `
                <div class="problem-opp-box">
                  <div class="problem-opp-title">💡 Venture Hypothesis</div>
                  <div><strong>${escapeHtml(p.venture_concept)}</strong>: ${escapeHtml(p.solution_summary || "")}</div>
                </div>
              ` : ''}
            </div>
          `).join("");
        }

        // Refresh global metrics & problems
        loadMetrics();
        loadProblems();
        loadLatestReport();

      } catch (err) {
        showToast("Error processing WhatsApp chat: " + err.message);
      }
    });
  }
}

// 4. Load Metrics
async function loadMetrics() {
  try {
    const res = await fetch("/api/metrics");
    const data = await res.json();

    document.getElementById("val-total-problems").textContent = data.total_problems || "0";
    document.getElementById("val-urgent-problems").textContent = data.urgent_problems_count || "0";
    
    // Top category
    const byCat = data.by_category || {};
    const topCat = Object.keys(byCat).length ? Object.keys(byCat).reduce((a, b) => byCat[a] > byCat[b] ? a : b) : "Infrastructure";
    document.getElementById("val-top-category").textContent = topCat.split("&")[0].trim();

    // Audience split
    const aud = data.by_audience || {};
    const local = aud["Local"] || 0;
    const expat = aud["Expat"] || 0;
    const shared = aud["Both"] || 0;
    document.getElementById("val-audience-split").textContent = `${local}L / ${expat}E / ${shared}S`;

  } catch (e) {
    console.error("Failed to load metrics:", e);
  }
}

// 5. Load Latest Daily Report (Regional or National)
async function loadLatestReport(region = "All") {
  const container = document.getElementById("report-rendered-markdown");
  const execBox = document.getElementById("exec-summary-box");
  const titleDisplay = document.getElementById("report-title-display");
  const metaDisplay = document.getElementById("report-meta-display");
  const regionBadge = document.getElementById("report-region-badge");

  try {
    container.innerHTML = `<div class="loading-state"><div class="spinner"></div><span>Loading ${region} intelligence briefing...</span></div>`;
    
    const res = await fetch(`/api/reports/latest?region=${encodeURIComponent(region)}`);
    const data = await res.json();
    latestReportData = data;

    if (!data || !data.markdown_content) {
      container.innerHTML = `<p>No report generated yet for ${region}. Click 'Run Agent Swarm' to compile.</p>`;
      return;
    }

    titleDisplay.textContent = data.report_title || `${region} Consumer Problem Intelligence Report`;
    metaDisplay.textContent = `Report Key: ${data.report_date} • 100% Ley Federal Data-Protected • Scope: ${region}`;
    if (regionBadge) regionBadge.textContent = region;

    // Executive summary bullets
    if (data.executive_summary) {
      const bullets = data.executive_summary.split("\n").filter(l => l.trim().length > 0);
      execBox.innerHTML = `
        <h4 style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: var(--accent-green); margin-bottom: 10px;">
          ✦ Executive Briefing Takeaways (${region})
        </h4>
        <ul>
          ${bullets.map(b => `<li>${formatMarkdownText(b.replace(/^-\s*/, ''))}</li>`).join("")}
        </ul>
      `;
      execBox.style.display = "block";
    } else {
      execBox.style.display = "none";
    }

    // Render markdown content
    container.innerHTML = parseMarkdownToHtml(data.markdown_content);

  } catch (e) {
    console.error("Failed to load latest report:", e);
    container.innerHTML = "<p>Error loading daily report.</p>";
  }
}

// 6. Load & Filter Problems
async function loadProblems() {
  const grid = document.getElementById("problems-grid");
  const counter = document.getElementById("records-counter");

  try {
    const res = await fetch("/api/problems?limit=300");
    allProblems = await res.json();
    renderFilteredProblems();
    renderVentureOpportunities(allProblems);
  } catch (e) {
    console.error("Failed to load problems:", e);
    grid.innerHTML = "<p>Error loading problem records.</p>";
  }
}

function initFilters() {
  const citySelect = document.getElementById("filter-city");
  const catSelect = document.getElementById("filter-category");
  const audSelect = document.getElementById("filter-audience");
  const searchInput = document.getElementById("search-input");

  const triggerFilter = () => renderFilteredProblems();

  if (citySelect) citySelect.addEventListener("change", triggerFilter);
  if (catSelect) catSelect.addEventListener("change", triggerFilter);
  if (audSelect) audSelect.addEventListener("change", triggerFilter);
  if (searchInput) searchInput.addEventListener("input", triggerFilter);
}

function renderFilteredProblems() {
  const grid = document.getElementById("problems-grid");
  const counter = document.getElementById("records-counter");

  const cityVal = document.getElementById("filter-city")?.value || "All";
  const catVal = document.getElementById("filter-category")?.value || "All";
  const audVal = document.getElementById("filter-audience")?.value || "All";
  const query = (document.getElementById("search-input")?.value || "").toLowerCase().trim();

  const filtered = allProblems.filter(p => {
    if (cityVal !== "All" && !p.city.toLowerCase().includes(cityVal.toLowerCase())) return false;
    if (catVal !== "All" && p.category !== catVal) return false;
    if (audVal !== "All" && p.audience !== audVal) return false;
    if (query) {
      const matchText = `${p.title} ${p.content} ${p.problem_summary} ${p.colonia} ${p.matched_slang}`.toLowerCase();
      if (!matchText.includes(query)) return false;
    }
    return true;
  });

  counter.textContent = `Showing ${filtered.length} of ${allProblems.length} monitored problems`;

  if (!filtered.length) {
    grid.innerHTML = `<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-muted);">
      No consumer problems found matching these criteria.
    </div>`;
    return;
  }

  grid.innerHTML = filtered.map(p => {
    const urgencyStars = "🔴".repeat(p.urgency || 3);
    const audienceTag = p.audience === "Expat" ? "🇺🇸 Expats" : (p.audience === "Local" ? "🇲🇽 Locals" : "👥 Shared");
    
    return `
      <div class="problem-card">
        <div>
          <div class="problem-card-header">
            <span class="problem-category-badge">${p.category}</span>
            <span class="problem-urgency">${urgencyStars} ${p.urgency}/5</span>
          </div>

          <h4 class="problem-title">${escapeHtml(p.title)}</h4>
          <p class="problem-content">${escapeHtml(p.content ? p.content.slice(0, 160) + "..." : p.problem_summary)}</p>

          <div class="problem-meta-row">
            <span class="meta-pill">📍 ${escapeHtml(p.city)} (${escapeHtml(p.colonia || "General")})</span>
            <span class="meta-pill">${audienceTag}</span>
            <span class="meta-pill">🔗 ${escapeHtml(p.source_platform)}</span>
          </div>
        </div>

        ${p.venture_concept ? `
          <div class="problem-opp-box">
            <div class="problem-opp-title">💡 Market Solution Concept</div>
            <div><strong>${escapeHtml(p.venture_concept)}</strong>: ${escapeHtml(p.solution_summary || "")}</div>
          </div>
        ` : ''}
      </div>
    `;
  }).join("");
}

// 7. Render Venture Opportunities Matrix
function renderVentureOpportunities(problems) {
  const container = document.getElementById("ventures-grid");
  if (!container) return;

  const uniqueVentures = [];
  const conceptsSeen = new Set();

  problems.forEach(p => {
    if (p.venture_concept && !conceptsSeen.has(p.venture_concept)) {
      conceptsSeen.add(p.venture_concept);
      uniqueVentures.push(p);
    }
  });

  if (!uniqueVentures.length) {
    container.innerHTML = "<p>No venture hypotheses synthesized yet.</p>";
    return;
  }

  container.innerHTML = uniqueVentures.map(v => {
    return `
      <div class="venture-card glass-panel">
        <div class="venture-header">
          <span class="venture-badge">${v.category}</span>
          <h3 class="venture-concept">💡 ${escapeHtml(v.venture_concept)}</h3>
          <p class="venture-desc">${escapeHtml(v.solution_summary || "Automated tech platform addressing chronic consumer pain points in Mexican metropolitan hubs.")}</p>
        </div>

        <div class="venture-tags">
          <span class="meta-pill">Target: ${escapeHtml(v.audience)}</span>
          <span class="meta-pill">Location: ${escapeHtml(v.city)}</span>
          <span class="meta-pill">Signal: ${escapeHtml(v.source_platform)}</span>
        </div>
      </div>
    `;
  }).join("");
}

// 8. Trigger Single Agent
function triggerSingleAgent(agentName) {
  showToast(`Starting ${agentName} agent in background...`);
  fetch(`/api/agents/run/${agentName}`, { method: "POST" })
    .then(r => r.json())
    .then(d => {
      showToast(`Agent '${agentName}' triggered successfully.`);
      setTimeout(() => {
        loadMetrics();
        loadLatestReport();
        loadProblems();
      }, 3500);
    })
    .catch(e => showToast("Error triggering agent: " + e.message));
}

// 9. Markdown Parser Utility
function parseMarkdownToHtml(md) {
  if (!md) return "";
  let html = md;

  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Blockquotes
  html = html.replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>');

  // Bold & Italic
  html = html.replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/gim, '<em>$1</em>');
  html = html.replace(/`(.*?)`/gim, '<code>$1</code>');

  // Tables
  const tableRegex = /\|(.+)\|[\r\n]+\|[-:| ]+\|[\r\n]+((?:\|.+\|[\r\n]*)+)/g;
  html = html.replace(tableRegex, (match, header, body) => {
    const headers = header.split('|').map(h => h.trim()).filter(Boolean);
    const rows = body.trim().split('\n').map(r => r.split('|').map(c => c.trim()).filter(Boolean));

    const ths = headers.map(h => `<th>${h}</th>`).join('');
    const trs = rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('');
    return `<table><thead><tr>${ths}</tr></thead><tbody>${trs}</tbody></table>`;
  });

  // Lists
  html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
  html = html.replace(/<\/li>\n<li>/g, '</li><li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // Paragraphs
  html = html.split('\n\n').map(p => {
    p = p.trim();
    if (!p.startsWith('<h') && !p.startsWith('<ul') && !p.startsWith('<table') && !p.startsWith('<blockquote') && p.length > 0) {
      return `<p>${p}</p>`;
    }
    return p;
  }).join('\n');

  return html;
}

function formatMarkdownText(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>');
}

function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
