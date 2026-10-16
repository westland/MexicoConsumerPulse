/**
 * MexConsumerPulse Dashboard JavaScript
 * Handles dual-language switching (ES / EN), data fetching, markdown rendering,
 * product voids, Mercado Libre México intelligence, and agent swarm triggers.
 */

// Global State
let currentLang = "es";
let currentRegion = "All";
let currentVoidOrigin = "All";
let allProblems = [];
let allProductVoids = [];
let allMLProducts = [];
let currentMLType = "ALL";
let currentMLCategory = "ALL";
let latestReportData = null;

// Comprehensive Bilingual Translation Dictionary
const TRANSLATIONS = {
  es: {
    // Header & Brand
    "tagline": "Enjambre Autónomo de Inteligencia del Consumidor",
    "swarm-status-text": "Enjambre Listo • Ciclo Diario Activo",
    "btn-export-csv-text": "Exportar CSV",
    "btn-fb-session-text": "Sesión FB",
    "btn-run-swarm-text": "Ejecutar Enjambre",

    // KPI Cards
    "kpi-label-total": "Problemas Verificados Monitoreados",
    "kpi-footer-total": "En CDMX, GDL, MTY, Mérida, Nacional",
    "kpi-label-urgent": "Alertas de Alta Urgencia (4-5)",
    "kpi-footer-urgent": "Fallas críticas de servicio y legales",
    "kpi-label-top-cat": "Vector Dominante de Fricción",
    "kpi-footer-top-cat": "Mayor frecuencia de quejas",
    "kpi-label-audience": "Proporción Demográfica",
    "kpi-footer-audience": "Locales vs Extranjeros vs Compartido",

    // Navigation Tabs
    "tab-text-report": "Informe Diario de Inteligencia",
    "tab-text-explorer": "Explorador de Problemas y Datos",
    "tab-text-product-voids": "🎁 \"Ojalá Vendieran Esto\" (Vacíos e Importaciones)",
    "tab-text-ventures": "Matriz de Oportunidades de Negocio",
    "tab-text-whatsapp": "Ingesta de WhatsApp Vecinos",
    "tab-text-mercadolibre": "🛒 Mercado Libre México",
    "tab-text-agents": "🤖 Operaciones y Reporte de Agentes",

    // Tab 1: Daily Intelligence Report
    "badge-pill-report": "Informe Ejecutivo Diario",
    "label-report-region": "Alcance del Informe:",
    "opt-reg-all": "🇲🇽 Reporte Nacional Multiciudad",
    "opt-reg-merida": "🌴 Reporte Mérida y Península de Yucatán",
    "opt-reg-cdmx": "🏙️ Ciudad de México (CDMX)",
    "opt-reg-gdl": "🌮 Guadalajara (GDL)",
    "opt-reg-mty": "⛰️ Monterrey (MTY)",
    "btn-download-md-text": "Descargar Markdown",
    "report-meta-display": "Sintetizado por el Enjambre Autónomo de Agentes",

    // Tab 2: Explorer
    "label-filter-city": "Ciudad / Región",
    "opt-city-all": "Todas las Regiones",
    "label-filter-cat": "Categoría",
    "opt-cat-all": "Todas las Categorías",
    "label-filter-aud": "Población Objetivo",
    "opt-aud-all": "Todas las Poblaciones",
    "opt-aud-local": "🇲🇽 Residentes Locales",
    "opt-aud-expat": "🇺🇸 Expats / Extranjeros",
    "search-input": "Buscar por colonia, modismo o palabra clave (ej. sarro, SAT, depósito, CFE)...",

    // Tab 3: Product Voids
    "badge-pill-voids": "Demanda de Importación & Arbitraje",
    "voids-title-heading": "🎁 Vacíos de Producto: \"Ojalá Vendieran Esto en México\"",
    "voids-desc-text": "Monitoreo de productos extranjeros disponibles en EE.UU., China, Japón y Europa que los consumidores mexicanos buscan activamente pero no pueden comprar en tiendas locales debido a falta de distribución formal o trabas regulatorias.",
    "void-filter-label": "Filtrar por Origen:",
    "void-btn-all": "🌍 Todos los Orígenes",
    "void-btn-usa": "🇺🇸 Comercio EE. UU.",
    "void-btn-china": "🇨🇳 Directo de China",
    "void-btn-japan": "🇯🇵 Japón y Corea",
    "void-btn-europe": "🇪🇺 Europa",
    "void-search-input": "Buscar producto no disponible...",
    "btn-toggle-wish-text": "+ Sugerir Producto Deseado",
    "wish-panel-title": "✦ Sugiere un Producto que Quisieras que se Vendiera en México",
    "wish-panel-desc": "Contribuye a la base de investigación. Las sugerencias son procesadas por el Agente de Síntesis para formular hipótesis de mercado.",
    "label-wish-prod": "Nombre del Producto y Marca",
    "label-wish-origin": "Disponible en (País de Origen)",
    "label-wish-city": "Tu Ciudad / Región",
    "label-wish-desc": "¿Por qué no se vende / Cómo lo consigues actualmente?",
    "btn-cancel-wish": "Cancelar",
    "btn-submit-wish": "Enviar al Enjambre de Investigación",

    // Tab 4: Ventures
    "ventures-title-heading": "💡 Oportunidades Directas de Mercado e Hipótesis de Negocio",
    "ventures-desc-text": "Estos conceptos de startup y modelos de negocio se sintetizan automáticamente a partir de quejas de alta fricción, vacíos crónicos de servicio y problemas comunitarios en ciudades mexicanas.",

    // Tab 5: WhatsApp
    "wa-title-heading": "💬 Analizador Comunitario de \"Chat de Vecinos\" de WhatsApp",
    "wa-desc-text": "El grupo vecinal de WhatsApp es el sensor más rápido en tiempo real para cortes de agua, variaciones de voltaje y fraudes en México. Pega líneas de chat o carga el ejemplo de la Condesa.",
    "btn-wa-load-sample": "Cargar Chat de Ejemplo",
    "btn-wa-parse": "Anonimizar e Ingerir Chat",
    "wa-results-title": "✦ Problemas Comunitarios Extraídos",

    // Tab 6: Mercado Libre México
    "ml-live-badge": "Solo Mercado Libre México (mercadolibre.com.mx)",
    "ml-tab-title": "Mercado Libre México: Hot New Products y Fallas en Productos Existentes",
    "ml-tab-subtitle": "Scraping dual y análisis continuo en mercadolibre.com.mx: 1) Detección de artículos en tendencia y nuevos productos con alta aceleración de demanda; 2) Extracción de quejas, fallas de calidad y reseñas críticas (1-3 estrellas) por sarro en Yucatán, variaciones de CFE y clima tropical.",
    "btn-run-ml-label": "Ejecutar Scraper Dual MLM",
    "btn-visit-ml-label": "Visitar MLM ↗",
    "ml-kpi-hot-label": "🔥 Hot New Products Monitoreados",
    "ml-kpi-hot-sub": "Baterías LiFePO4, Minisplits Solares, IoT Tinacos",
    "ml-kpi-problems-label": "⚠️ Fallas Críticas Identificadas",
    "ml-kpi-problems-sub": "Sarro kárstico, Picos CFE, Humedad 90%+",
    "ml-kpi-rating-label": "Reseñas Verificadas Analizadas",
    "ml-kpi-rating-sub": "Citas textuales de compradores mexicanos",
    "ml-kpi-price-label": "Rango de Precios en MXN",
    "ml-kpi-price-sub": "Precios en pesos mexicanos con envío nacional",
    "ml-filter-all-label": "Todos los Artículos",
    "ml-filter-hot-label": "🔥 Hot New Products & Tendencias",
    "ml-filter-problems-label": "⚠️ Fallas en Productos Existentes (1-3 ⭐)",
    "ml-cat-label": "Categoría:",

    // Tab 7: Agents
    "audit-badge-title": "Auditoría Ejecutiva del Enjambre",
    "audit-badge-agents": "8/8 Agentes Operativos",
    "audit-title-heading": "Actividad de los Agentes Autónomos",
    "audit-desc-text": "Auditoría completa de recolección de datos, anonimización de datos personales (PII), análisis de modismos mexicanos y síntesis de oportunidades en urbes mexicanas.",
    "btn-run-full-swarm-text": "Ejecutar Enjambre Completo",
    "btn-run-ml-text": "Ejecutar Agente Mercado Libre"
  },
  en: {
    // Header & Brand
    "tagline": "Autonomous Consumer Intelligence Swarm",
    "swarm-status-text": "Swarm Operational • Daily Cycle Active",
    "btn-export-csv-text": "Export CSV",
    "btn-fb-session-text": "FB Session",
    "btn-run-swarm-text": "Run Agent Swarm",

    // KPI Cards
    "kpi-label-total": "Verified Monitored Problems",
    "kpi-footer-total": "In CDMX, GDL, MTY, Mérida, National",
    "kpi-label-urgent": "High-Urgency Alerts (4-5)",
    "kpi-footer-urgent": "Critical service & legal disputes",
    "kpi-label-top-cat": "Dominant Friction Vector",
    "kpi-footer-top-cat": "Highest complaint frequency",
    "kpi-label-audience": "Demographic Ratio",
    "kpi-footer-audience": "Locals vs Expats vs Shared",

    // Navigation Tabs
    "tab-text-report": "Daily Intelligence Report",
    "tab-text-explorer": "Problem & Data Explorer",
    "tab-text-product-voids": "🎁 \"I Wish They Sold This\" (Voids & Imports)",
    "tab-text-ventures": "Venture Opportunity Matrix",
    "tab-text-whatsapp": "WhatsApp Vecinos Ingestion",
    "tab-text-mercadolibre": "🛒 Mercado Libre Mexico",
    "tab-text-agents": "🤖 Agent Operations & Reports",

    // Tab 1: Daily Intelligence Report
    "badge-pill-report": "Executive Daily Report",
    "label-report-region": "Report Scope:",
    "opt-reg-all": "🇲🇽 National Multi-City Report",
    "opt-reg-merida": "🌴 Mérida & Yucatán Peninsula Report",
    "opt-reg-cdmx": "🏙️ Mexico City (CDMX)",
    "opt-reg-gdl": "🌮 Guadalajara (GDL)",
    "opt-reg-mty": "⛰️ Monterrey (MTY)",
    "btn-download-md-text": "Download Markdown",
    "report-meta-display": "Synthesized by Autonomous Agent Swarm",

    // Tab 2: Explorer
    "label-filter-city": "City / Region",
    "opt-city-all": "All Regions",
    "label-filter-cat": "Category",
    "opt-cat-all": "All Categories",
    "label-filter-aud": "Target Audience",
    "opt-aud-all": "All Audiences",
    "opt-aud-local": "🇲🇽 Local Residents",
    "opt-aud-expat": "🇺🇸 Expats / Foreigners",
    "opt-aud-both": "👥 Shared",
    "search-input": "Search by colonia, slang, or keyword (e.g. sarro, SAT, deposit, CFE)...",

    // Tab 3: Product Voids
    "badge-pill-voids": "Import Demand & Arbitrage",
    "voids-title-heading": "🎁 Product Voids: \"I Wish They Sold This in Mexico\"",
    "voids-desc-text": "Monitoring foreign consumer goods available in the US, China, Japan, and Europe that Mexican consumers actively search for but cannot purchase domestically due to regulatory or distribution barriers.",
    "void-filter-label": "Filter by Origin:",
    "void-btn-all": "All Origins",
    "void-btn-usa": "🇺🇸 USA Retail",
    "void-btn-china": "🇨🇳 China Direct",
    "void-btn-japan": "🇯🇵 Japan & Korea",
    "void-btn-europe": "🇪🇺 Europe Direct",
    "void-search-input": "Search product voids (e.g. countertop dishwasher, seasonings, sunscreens, smart relays)...",
    "btn-toggle-wish-text": "+ Submit Wishlist Item",
    "wish-panel-title": "✦ Suggest a Product You Wish Was Sold in Mexico",
    "wish-panel-desc": "Contribute to the research database. Suggestions are synthesized by the NLP Engine to formulate startup hypotheses.",
    "label-wish-prod": "Product Name & Brand",
    "label-wish-origin": "Available in (Origin Country)",
    "label-wish-city": "Your City / Region",
    "label-wish-desc": "Why isn't it sold / How do you currently obtain it?",
    "btn-cancel-wish": "Cancel",
    "btn-submit-wish": "Submit to Research Swarm",

    // Tab 4: Ventures
    "ventures-title-heading": "💡 Direct Market Opportunities & Venture Hypotheses",
    "ventures-desc-text": "These startup concepts and business models are synthesized automatically from high-friction complaints and chronic service voids across Mexican cities.",

    // Tab 5: WhatsApp
    "wa-title-heading": "💬 WhatsApp 'Vecinos' Community Chat Parser",
    "wa-desc-text": "Paste exported residential chat logs from Mexican neighborhood groups (Condesa, Roma, Mérida Norte). Automatically scrubs phone numbers, names, and addresses under Mexican privacy law.",
    "btn-wa-load-sample": "Load Sample Chat (Condesa)",
    "btn-wa-parse": "Scrub PII & Ingest Chat",
    "wa-results-title": "✦ Extracted Community Problems",

    // Tab 6: Mercado Libre México
    "ml-live-badge": "Exclusively Mercado Libre Mexico (mercadolibre.com.mx)",
    "ml-tab-title": "Mercado Libre Mexico: Hot New Products & Existing Product Failures",
    "ml-tab-subtitle": "Dual scraping & intelligence from mercadolibre.com.mx: 1) Identification of breakout trending products and rapid-growth innovations; 2) Extraction of customer complaints, defect reports, and critical 1-3 star reviews caused by Yucatan limestone water, CFE grid surges, and tropical climate.",
    "btn-run-ml-label": "Run Dual MLM Scraper",
    "btn-visit-ml-label": "Visit MLM ↗",
    "ml-kpi-hot-label": "🔥 Tracked Hot New Products",
    "ml-kpi-hot-sub": "LiFePO4 Batteries, Solar ACs, IoT Tinaco Switches",
    "ml-kpi-problems-label": "⚠️ Critical Failure Alerts",
    "ml-kpi-problems-sub": "Limestone scaling, CFE surges & 90%+ humidity",
    "ml-kpi-rating-label": "Verified Buyer Reviews Analyzed",
    "ml-kpi-rating-sub": "Direct customer quotes from Mexican shoppers",
    "ml-kpi-price-label": "Price Range (MXN)",
    "ml-kpi-price-sub": "MXN peso pricing with nationwide shipping",
    "ml-filter-all-label": "All Products",
    "ml-filter-hot-label": "🔥 Hot New Products & Trends",
    "ml-filter-problems-label": "⚠️ Existing Product Problems (1-3 ⭐)",
    "ml-cat-label": "Category:",

    // Tab 7: Agents
    "audit-badge-title": "Swarm Executive Audit",
    "audit-badge-agents": "8/8 Agents Operational",
    "audit-title-heading": "Autonomous Agent Activity & Dossiers",
    "audit-desc-text": "Full audit of data collection, PII sanitization under Mexican law, modismos scoring, and startup synthesis across Mexican cities.",
    "btn-run-full-swarm-text": "Run Full Agent Swarm",
    "btn-run-ml-text": "Run Mercado Libre Agent"
  }
};

// Initialization on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  initLanguage();
  initTabs();
  initModals();
  initActions();
  initFilters();
  initProductVoids();

  // Load datasets
  loadMetrics();
  loadLatestReport(currentRegion, currentLang);
  loadProblems();
  loadProductVoids();
  loadMercadoLibreProducts();
});

// 1. Language Switcher Initialization & Handler
function initLanguage() {
  const path = window.location.pathname.toLowerCase();
  const urlParams = new URLSearchParams(window.location.search);
  const paramLang = urlParams.get("lang");
  const storedLang = localStorage.getItem("mex_pulse_lang");

  if (path === "/en" || paramLang === "en") {
    currentLang = "en";
  } else if (path === "/es" || paramLang === "es") {
    currentLang = "es";
  } else if (storedLang === "en" || storedLang === "es") {
    currentLang = storedLang;
  } else {
    currentLang = "es"; // Default Spanish
  }

  // Bind Buttons
  const btnEs = document.getElementById("btn-lang-es");
  const btnEn = document.getElementById("btn-lang-en");

  if (btnEs) {
    btnEs.addEventListener("click", () => setLanguage("es"));
  }
  if (btnEn) {
    btnEn.addEventListener("click", () => setLanguage("en"));
  }

  setLanguage(currentLang, false);
}

function setLanguage(lang, triggerReload = true) {
  currentLang = (lang === "en") ? "en" : "es";
  localStorage.setItem("mex_pulse_lang", currentLang);
  document.documentElement.lang = currentLang;

  // Toggle active button
  const btnEs = document.getElementById("btn-lang-es");
  const btnEn = document.getElementById("btn-lang-en");
  if (btnEs && btnEn) {
    if (currentLang === "es") {
      btnEs.classList.add("active");
      btnEn.classList.remove("active");
    } else {
      btnEn.classList.add("active");
      btnEs.classList.remove("active");
    }
  }

  // Update dynamic translations
  const dict = TRANSLATIONS[currentLang] || TRANSLATIONS.es;
  for (const [id, text] of Object.entries(dict)) {
    const el = document.getElementById(id);
    if (el) {
      if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
        el.placeholder = text;
      } else {
        el.textContent = text;
      }
    }
  }

  // Update document title
  if (currentLang === "es") {
    document.title = "MexConsumerPulse | Inteligencia del Consumidor Urbano en México";
  } else {
    document.title = "MexConsumerPulse | Mexican Urban Consumer Problems & Market Intelligence";
  }

  if (triggerReload) {
    showToast(currentLang === "es" ? "Idioma cambiado a Español 🇲🇽" : "Language switched to English 🇺🇸");
    loadLatestReport(currentRegion, currentLang);
    renderFilteredProblems();
    filterAndRenderProductVoids();
    renderMercadoLibreProducts(getFilteredMLProducts());
  }
}

// 2. Tab Navigation
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

// 3. Modals & Notifications
function initModals() {
  const fbModal = document.getElementById("fb-modal");
  const btnFbSession = document.getElementById("btn-fb-session");
  const btnClose = document.getElementById("btn-close-modal");
  const btnCancel = document.getElementById("btn-modal-cancel");
  const btnLaunch = document.getElementById("btn-modal-launch-fb");

  const openModal = () => fbModal && fbModal.classList.add("active");
  const closeModal = () => fbModal && fbModal.classList.remove("active");

  if (btnFbSession) btnFbSession.addEventListener("click", openModal);
  if (btnClose) btnClose.addEventListener("click", closeModal);
  if (btnCancel) btnCancel.addEventListener("click", closeModal);

  if (btnLaunch) {
    btnLaunch.addEventListener("click", () => {
      showToast(currentLang === "es" ? "Solicitando inicio de sesión interactivo..." : "Requesting interactive login session...");
      btnLaunch.disabled = true;

      fetch("/api/agents/login/facebook", { method: "POST" })
        .then(res => res.json())
        .then(data => {
          btnLaunch.disabled = false;
          if (data.status === "cloud_notice") {
            // User is browsing on remote server (pulse-mexico.com)
            alert(
              "⚠️ AVISO DE SERVIDOR EN LA NUBE:\n\n" +
              data.message + "\n\n" +
              "👉 Comando: " + data.command + "\n" +
              "👉 O archivo: " + data.bat_file
            );
          } else {
            // Local machine: browser popped open!
            showToast(currentLang === "es" ? "¡Ventana de Chromium abierta en tu escritorio! Inicia sesión para guardar cookies." : "Chromium window opened on your desktop! Log in to save session cookies.");
            closeModal();
          }
        })
        .catch(err => {
          btnLaunch.disabled = false;
          showToast("Error: " + err.message);
        });
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
  setTimeout(() => toast.classList.remove("show"), 3800);
}

// 4. Header Actions
function initActions() {
  const btnRunSwarm = document.getElementById("btn-run-swarm");
  const btnExportCsv = document.getElementById("btn-export-csv");
  const btnDownloadMd = document.getElementById("btn-download-md");

  if (btnRunSwarm) {
    btnRunSwarm.addEventListener("click", () => {
      showToast(currentLang === "es" ? "Ejecutando enjambre autónomo de agentes..." : "Triggering full autonomous agent swarm run...");
      fetch("/api/agents/run/all", { method: "POST" })
        .then(res => res.json())
        .then(() => {
          showToast(currentLang === "es" ? "Enjambre iniciado en segundo plano. Actualizando datos..." : "Swarm run initiated! Updating live data...");
          setTimeout(() => {
            loadMetrics();
            loadLatestReport(currentRegion, currentLang);
            loadProblems();
            loadMercadoLibreProducts();
          }, 4000);
        })
        .catch(err => showToast("Error: " + err.message));
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
        showToast(currentLang === "es" ? "No hay informe disponible para descargar." : "No report currently available to download.");
        return;
      }
      const blob = new Blob([latestReportData.markdown_content], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `mexico_consumer_report_${latestReportData.report_date || "latest"}_${currentLang}.md`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  // Regional Report Selector
  const regionSelect = document.getElementById("select-report-region");
  if (regionSelect) {
    regionSelect.addEventListener("change", (e) => {
      currentRegion = e.target.value;
      showToast(currentLang === "es" ? `Cargando informe de ${currentRegion}...` : `Loading ${currentRegion} intelligence report...`);
      loadLatestReport(currentRegion, currentLang);
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
      showToast(currentLang === "es" ? "Chat de muestra cargado. Haga clic en 'Limpiar PII e Ingerir'." : "Sample Condesa chat loaded!");
    });
  }

  if (btnParse) {
    btnParse.addEventListener("click", async () => {
      const chatText = chatInput.value.trim();
      if (!chatText) {
        showToast(currentLang === "es" ? "Pegue texto del chat antes de continuar." : "Please paste chat text.");
        return;
      }

      showToast(currentLang === "es" ? "Anonimizando PII y procesando problemas vecinales..." : "Scrubbing PII and extracting problems...");
      try {
        const res = await fetch("/api/whatsapp/import", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_text: chatText,
            group_name: groupInput?.value || "Chat de Vecinos Condesa",
            city: cityInput?.value || "Mexico City (CDMX)"
          })
        });

        const data = await res.json();
        showToast(currentLang === "es" ? `¡Se extrajeron ${data.extracted_count} problemas con éxito!` : `Extracted ${data.extracted_count} problems!`);

        if (data.problems && data.problems.length > 0) {
          resultsPanel.style.display = "block";
          extractedGrid.innerHTML = data.problems.map(p => `
            <div class="problem-card">
              <div class="problem-card-header">
                <span class="problem-category-badge">${escapeHtml(p.category)}</span>
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
                  <div class="problem-opp-title">💡 ${currentLang === "es" ? "Hipótesis de Negocio" : "Venture Hypothesis"}</div>
                  <div><strong>${escapeHtml(p.venture_concept)}</strong>: ${escapeHtml(p.solution_summary || "")}</div>
                </div>
              ` : ''}
            </div>
          `).join("");
        }

        loadMetrics();
        loadProblems();
        loadLatestReport(currentRegion, currentLang);
      } catch (err) {
        showToast("Error: " + err.message);
      }
    });
  }
}

// 5. Load Metrics
async function loadMetrics() {
  try {
    const res = await fetch("/api/metrics");
    const data = await res.json();

    document.getElementById("val-total-problems").textContent = data.total_problems || "0";
    document.getElementById("val-urgent-problems").textContent = data.urgent_problems_count || "0";
    
    const byCat = data.by_category || {};
    const topCat = Object.keys(byCat).length ? Object.keys(byCat).reduce((a, b) => byCat[a] > byCat[b] ? a : b) : "Infrastructure";
    document.getElementById("val-top-category").textContent = topCat.split("&")[0].trim();

    const aud = data.by_audience || {};
    const local = aud["Local"] || 0;
    const expat = aud["Expat"] || 0;
    const shared = aud["Both"] || 0;
    document.getElementById("val-audience-split").textContent = `${local}L / ${expat}E / ${shared}S`;
  } catch (e) {
    console.error("Failed to load metrics:", e);
  }
}

// 6. Load Latest Daily Report (Dual Language)
async function loadLatestReport(region = "All", lang = currentLang) {
  const container = document.getElementById("report-rendered-markdown");
  const execBox = document.getElementById("exec-summary-box");
  const titleDisplay = document.getElementById("report-title-display");
  const metaDisplay = document.getElementById("report-meta-display");
  const regionBadge = document.getElementById("report-region-badge");

  try {
    container.innerHTML = `<div class="loading-state"><div class="spinner"></div><span>${lang === "es" ? "Cargando informe ejecutivo de inteligencia..." : `Loading ${region} intelligence briefing...`}</span></div>`;
    
    const res = await fetch(`/api/reports/latest?region=${encodeURIComponent(region)}&lang=${lang}`);
    const data = await res.json();
    latestReportData = data;

    if (!data || !data.markdown_content) {
      container.innerHTML = `<p>${lang === "es" ? "Aún no se ha generado informe para esta región. Haga clic en 'Ejecutar Enjambre'." : `No report generated yet for ${region}. Click 'Run Agent Swarm'.`}</p>`;
      return;
    }

    titleDisplay.textContent = data.report_title || `${region} Consumer Problem Intelligence Report`;
    metaDisplay.textContent = `Report Key: ${data.report_date} • 100% Ley Federal Data-Protected • Scope: ${region} • ${lang.toUpperCase()}`;
    if (regionBadge) regionBadge.textContent = region;

    // Executive summary bullets
    if (data.executive_summary) {
      const bullets = data.executive_summary.split("\n").filter(l => l.trim().length > 0);
      execBox.innerHTML = `
        <h4 style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: var(--accent-green); margin-bottom: 10px;">
          ✦ ${lang === "es" ? `Puntos Clave del Resumen Ejecutivo (${region})` : `Executive Briefing Takeaways (${region})`}
        </h4>
        <ul>
          ${bullets.map(b => `<li>${formatMarkdownText(b.replace(/^-\s*/, ''))}</li>`).join("")}
        </ul>
      `;
      execBox.style.display = "block";
    } else {
      execBox.style.display = "none";
    }

    container.innerHTML = parseMarkdownToHtml(data.markdown_content);
  } catch (e) {
    console.error("Failed to load latest report:", e);
    container.innerHTML = "<p>Error loading daily report.</p>";
  }
}

// 7. Load & Filter Problems
async function loadProblems() {
  const grid = document.getElementById("problems-grid");
  try {
    const res = await fetch("/api/problems?limit=300");
    allProblems = await res.json();
    renderFilteredProblems();
    renderVentureOpportunities(allProblems);
  } catch (e) {
    console.error("Failed to load problems:", e);
    if (grid) grid.innerHTML = "<p>Error loading problem records.</p>";
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
  if (!grid) return;

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

  if (counter) {
    counter.textContent = (currentLang === "es")
      ? `Mostrando ${filtered.length} de ${allProblems.length} problemas monitoreados`
      : `Showing ${filtered.length} of ${allProblems.length} monitored problems`;
  }

  if (!filtered.length) {
    grid.innerHTML = `<div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-muted);">
      ${currentLang === "es" ? "No se encontraron problemas que coincidan con estos criterios." : "No consumer problems found matching these criteria."}
    </div>`;
    return;
  }

  grid.innerHTML = filtered.map(p => {
    const urgencyStars = "🔴".repeat(p.urgency || 3);
    const audienceTag = p.audience === "Expat" ? "🇺🇸 Expats" : (p.audience === "Local" ? "🇲🇽 Locales" : "👥 Compartido");
    
    return `
      <div class="problem-card">
        <div>
          <div class="problem-card-header">
            <span class="problem-category-badge">${escapeHtml(p.category)}</span>
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
            <div class="problem-opp-title">💡 ${currentLang === "es" ? "Concepto de Solución" : "Market Solution Concept"}</div>
            <div><strong>${escapeHtml(p.venture_concept)}</strong>: ${escapeHtml(p.solution_summary || "")}</div>
          </div>
        ` : ''}
      </div>
    `;
  }).join("");
}

// 8. Render Venture Opportunities Matrix
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
    container.innerHTML = `<p>${currentLang === "es" ? "Aún no hay hipótesis sintetizadas." : "No venture hypotheses synthesized yet."}</p>`;
    return;
  }

  container.innerHTML = uniqueVentures.map(v => {
    return `
      <div class="venture-card glass-panel">
        <div class="venture-header">
          <span class="venture-badge">${escapeHtml(v.category)}</span>
          <h3 class="venture-concept">💡 ${escapeHtml(v.venture_concept)}</h3>
          <p class="venture-desc">${escapeHtml(v.solution_summary || "Oportunidad de mercado para resolver fricciones recurrentes de consumidores en México.")}</p>
        </div>

        <div class="venture-tags">
          <span class="meta-pill">Población: ${escapeHtml(v.audience)}</span>
          <span class="meta-pill">Ubicación: ${escapeHtml(v.city)}</span>
          <span class="meta-pill">Fuente: ${escapeHtml(v.source_platform)}</span>
        </div>
      </div>
    `;
  }).join("");
}

// 9. Mercado Libre México Dual Intelligence Loader & Renderer
function filterMLByType(type) {
  currentMLType = type;
  const btnAll = document.getElementById("ml-filter-all");
  const btnHot = document.getElementById("ml-filter-hot");
  const btnProb = document.getElementById("ml-filter-problems");

  if (btnAll) btnAll.classList.toggle("active", type === "ALL");
  if (btnHot) btnHot.classList.toggle("active", type === "HOT_NEW_PRODUCT");
  if (btnProb) btnProb.classList.toggle("active", type === "EXISTING_PRODUCT_PROBLEMS");

  renderMercadoLibreProducts(getFilteredMLProducts());
}

function filterMLByCategory(cat) {
  currentMLCategory = cat;
  renderMercadoLibreProducts(getFilteredMLProducts());
}

function getFilteredMLProducts() {
  return allMLProducts.filter(item => {
    const matchesType = (currentMLType === "ALL") || (item.product_type === currentMLType);
    const matchesCat = (currentMLCategory === "ALL") || (item.category === currentMLCategory);
    return matchesType && matchesCat;
  });
}

async function loadMercadoLibreProducts() {
  const grid = document.getElementById("mercadolibre-products-grid");
  try {
    const res = await fetch("/api/mercadolibre/products?limit=100");
    allMLProducts = await res.json();

    // Update Quick Stats
    const hotCount = allMLProducts.filter(p => p.product_type === "HOT_NEW_PRODUCT").length;
    const problemCount = allMLProducts.filter(p => p.product_type === "EXISTING_PRODUCT_PROBLEMS").length;
    const countBadge = document.getElementById("ml-count-badge");
    const hotEl = document.getElementById("ml-stat-hot");
    const probEl = document.getElementById("ml-stat-problems");
    const rangeEl = document.getElementById("ml-stat-range");
    const reviewsEl = document.getElementById("ml-stat-reviews");

    if (countBadge) {
      countBadge.textContent = `${allMLProducts.length} ${currentLang === "es" ? "Artículos Analizados" : "Analyzed Items"}`;
    }
    if (hotEl) {
      hotEl.textContent = `${hotCount} ${currentLang === "es" ? "Artículos" : "Items"}`;
    }
    if (probEl) {
      probEl.textContent = `${problemCount} ${currentLang === "es" ? "Defectos" : "Flaws"}`;
    }

    if (allMLProducts.length > 0) {
      const prices = allMLProducts.map(p => p.price_mxn).filter(p => p > 0);
      if (prices.length > 0 && rangeEl) {
        const minP = Math.min(...prices);
        const maxP = Math.max(...prices);
        rangeEl.textContent = `$${minP.toLocaleString()} – $${maxP.toLocaleString()}`;
      }

      const totalReviews = allMLProducts.reduce((sum, p) => sum + (p.review_count || 0), 0);
      if (reviewsEl) {
        reviewsEl.textContent = `${totalReviews.toLocaleString()}+ ${currentLang === "es" ? "Opiniones" : "Reviews"}`;
      }
    }

    renderMercadoLibreProducts(getFilteredMLProducts());
  } catch (err) {
    console.error("Failed to load Mercado Libre products:", err);
    if (grid) grid.innerHTML = "<p>Error loading Mercado Libre data.</p>";
  }
}

function renderMercadoLibreProducts(products) {
  const grid = document.getElementById("mercadolibre-products-grid");
  if (!grid) return;

  if (!products.length) {
    grid.innerHTML = `
      <div class="empty-state glass-panel" style="grid-column: 1 / -1; padding: 40px; text-align: center;">
        <span style="font-size: 38px;">🛒</span>
        <h3 style="margin-top: 10px; color: #fff;">${currentLang === "es" ? "No se encontraron productos con estos filtros" : "No products found matching filters"}</h3>
        <p style="color: var(--text-muted); font-size: 13px; max-width: 500px; margin: 6px auto;">
          ${currentLang === "es" ? "Pruebe seleccionando 'Todos los Artículos' o ejecute el scraper dual para cosechar datos frescos." : "Try selecting 'All Products' or run the dual scraper to harvest fresh data."}
        </p>
      </div>
    `;
    return;
  }

  grid.innerHTML = products.map(item => {
    const isHot = item.product_type === "HOT_NEW_PRODUCT";
    const reviews = item.reviews || [];
    const ratingStars = "⭐".repeat(Math.min(5, Math.max(1, Math.round(item.rating || (isHot ? 5 : 3)))));
    const cardClass = isHot ? "ml-card-hot" : "ml-card-problem";
    const badgeHtml = isHot
      ? `<span class="ml-badge-hot">${escapeHtml(item.trend_badge || "🔥 MÁS VENDIDO #1")}</span>`
      : `<span class="ml-badge-problem">${escapeHtml(item.trend_badge || "⚠️ FALLA REGIONAL")}</span>`;

    return `
      <div class="problem-card glass-panel ${cardClass}" style="display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <!-- Card Header -->
          <div class="problem-card-header">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
              <span class="badge badge-ml">🛒 ${escapeHtml(item.mlm_id || "MLM México")}</span>
              ${badgeHtml}
            </div>
            <span class="ml-rating-tag" style="${isHot ? '' : 'color: var(--accent-red); font-weight: 800;'}">
              ${ratingStars} ${Number(item.rating || 0).toFixed(1)}/5 (${item.review_count} ${currentLang === "es" ? "op." : "rev."})
            </span>
          </div>

          <!-- Product Title -->
          <h4 class="problem-title" style="color: #fff; font-size: 15px; margin: 12px 0 6px; line-height: 1.35;">
            ${escapeHtml(item.title)}
          </h4>

          <!-- Price & Seller Location -->
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin: 8px 0 12px; flex-wrap: wrap; gap: 6px;">
            <div class="ml-price-tag">$${Number(item.price_mxn || 0).toLocaleString()} MXN</div>
            <div class="ml-seller-loc">📍 ${escapeHtml(item.seller_location || "México (Envío Full)")}</div>
          </div>

          <!-- Trend Growth or Failure Mode Banner -->
          ${isHot ? `
            ${item.demand_growth ? `
              <div style="margin: 8px 0;">
                <div class="ml-growth-tag">
                  📈 <strong>${currentLang === "es" ? "Aceleración de Demanda:" : "Demand Growth:"}</strong> ${escapeHtml(item.demand_growth)}
                </div>
              </div>
            ` : ''}

            <div style="background: rgba(0, 230, 153, 0.06); border-left: 2px solid var(--accent-green); padding: 8px 12px; border-radius: 4px; margin: 8px 0; font-size: 12px; color: var(--text-main);">
              <strong style="color: var(--accent-green);">💡 ${currentLang === "es" ? "Factor Clave de Adopción en México:" : "Adoption Driver in Mexico:"}</strong>
              <div style="margin-top: 2px;">${escapeHtml(item.problem_summary || "Alta demanda por resiliencia y ahorro energético en hogares mexicanos.")}</div>
            </div>
          ` : `
            <div style="background: rgba(255, 71, 87, 0.08); border-left: 2px solid var(--accent-red); padding: 8px 12px; border-radius: 4px; margin: 8px 0; font-size: 12px; color: var(--text-main);">
              <strong style="color: var(--accent-red);">💥 ${currentLang === "es" ? "Falla Regional Crítica en México:" : "Critical Failure Mode in Mexico:"}</strong>
              <div style="margin-top: 2px;">${escapeHtml(item.failure_mode || item.problem_summary || "Incompatibilidad reportada con infraestructura local mexicana.")}</div>
            </div>
          `}

          <!-- Customer Verbatim Quotes from mercadolibre.com.mx -->
          <div style="margin: 10px 0;">
            <div style="font-size: 11px; font-weight: 700; color: #ffe600; text-transform: uppercase; letter-spacing: 0.4px;">
              ${isHot 
                ? (currentLang === "es" ? "💬 Reseñas Verificadas de Compradores en México:" : "💬 Verified Buyer Reviews on MLM:")
                : (currentLang === "es" ? "⚠️ Quejas Verificadas de Compradores (1-3 ⭐):" : "⚠️ Verified Critical Complaints (1-3 ⭐):")}
            </div>
            ${reviews.slice(0, 3).map(r => `
              <div class="ml-review-card" style="${isHot ? '' : 'border-left-color: var(--accent-red);'}">"${escapeHtml(r)}"</div>
            `).join("")}
          </div>

          <!-- Solution / Current Workaround -->
          <div style="background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 4px; padding: 8px 12px; margin: 8px 0; font-size: 11px;">
            <span style="color: var(--text-dim); font-weight: 700;">${currentLang === "es" ? "SOLUCIÓN ACTUAL / EN EL MERCADO" : "CURRENT WORKAROUND"}:</span>
            <div style="color: var(--text-main); margin-top: 2px;">${escapeHtml(item.solution_found || "Adquisición de adaptadores o reemplazo frecuente.")}</div>
          </div>
        </div>

        <div>
          <!-- Venture Concept / Startup Opportunity -->
          ${item.venture_concept ? `
            <div class="problem-opp-box" style="margin-top: 10px; border-color: ${isHot ? 'rgba(255, 152, 0, 0.35)' : 'rgba(255, 230, 0, 0.3)'};">
              <div class="problem-opp-title" style="color: ${isHot ? '#ff9800' : '#ffe600'};">
                💡 ${isHot 
                  ? (currentLang === "es" ? "Oportunidad de Mercado & Expansión D2C" : "Market Opportunity & D2C Scaling")
                  : (currentLang === "es" ? "Oportunidad de Rediseño / Emprendimiento" : "Redesign & Venture Opportunity")}
              </div>
              <div style="font-size: 12px; margin-top: 3px;"><strong>${escapeHtml(item.venture_concept)}</strong></div>
            </div>
          ` : ''}

          <!-- External Link Button -->
          <div style="margin-top: 12px; display: flex; justify-content: flex-end;">
            <a href="${escapeHtml(item.url || 'https://www.mercadolibre.com.mx/')}" target="_blank" class="btn btn-secondary btn-sm" style="font-size: 11px;">
              ${currentLang === "es" ? "Ver Artículo en Mercado Libre ↗" : "View on Mercado Libre ↗"}
            </a>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

// 10. Product Voids Handler
function initProductVoids() {
  const filterBtns = document.querySelectorAll(".void-filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentVoidOrigin = btn.getAttribute("data-origin") || "All";
      filterAndRenderProductVoids();
    });
  });

  const searchInput = document.getElementById("void-search-input");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      filterAndRenderProductVoids();
    });
  }

  const toggleBtn = document.getElementById("btn-toggle-wish-form");
  const cancelBtn = document.getElementById("btn-cancel-wish");
  const formPanel = document.getElementById("wish-submit-panel");

  if (toggleBtn && formPanel) {
    toggleBtn.addEventListener("click", () => {
      const isHidden = formPanel.style.display === "none" || !formPanel.style.display;
      formPanel.style.display = isHidden ? "block" : "none";
      if (isHidden) {
        document.getElementById("wish-product-name")?.focus();
      }
    });
  }

  if (cancelBtn && formPanel) {
    cancelBtn.addEventListener("click", () => {
      formPanel.style.display = "none";
    });
  }

  const submitBtn = document.getElementById("btn-submit-wish");
  if (submitBtn) {
    submitBtn.addEventListener("click", async () => {
      const prodName = document.getElementById("wish-product-name")?.value.trim();
      const origin = document.getElementById("wish-origin-country")?.value || "USA";
      const city = document.getElementById("wish-city")?.value || "National";
      const desc = document.getElementById("wish-description")?.value.trim() || "";

      if (!prodName) {
        showToast(currentLang === "es" ? "Por favor ingrese el nombre del producto." : "Please enter a product name.");
        return;
      }

      showToast(currentLang === "es" ? `Registrando deseo: '${prodName}'...` : `Submitting wishlist item '${prodName}'...`);
      try {
        const res = await fetch("/api/product-voids/submit", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            product_name: prodName,
            origin_country: origin,
            city: city,
            description: desc
          })
        });

        const data = await res.json();
        showToast(data.message || (currentLang === "es" ? "¡Vacío de producto registrado!" : "Product void logged successfully!"));
        
        const inputElem = document.getElementById("wish-product-name");
        if (inputElem) inputElem.value = "";
        const descElem = document.getElementById("wish-description");
        if (descElem) descElem.value = "";
        if (formPanel) formPanel.style.display = "none";

        loadProductVoids();
        loadMetrics();
        loadProblems();
      } catch (err) {
        showToast("Error: " + err.message);
      }
    });
  }
}

async function loadProductVoids() {
  try {
    const res = await fetch("/api/product-voids");
    allProductVoids = await res.json();
    
    const counterBadge = document.getElementById("voids-counter-badge");
    if (counterBadge) {
      counterBadge.textContent = `${allProductVoids.length} ${currentLang === "es" ? "Vacíos Verificados" : "Verified Voids"}`;
    }

    filterAndRenderProductVoids();
  } catch (err) {
    console.error("Failed to load product voids:", err);
  }
}

function filterAndRenderProductVoids() {
  const searchInput = document.getElementById("void-search-input");
  const query = (searchInput ? searchInput.value : "").toLowerCase().trim();

  let filtered = allProductVoids;

  if (currentVoidOrigin !== "All") {
    filtered = filtered.filter(v => {
      const txt = `${v.title} ${v.content} ${v.venture_concept || ''}`.toLowerCase();
      if (currentVoidOrigin === "USA") return txt.includes("usa") || txt.includes("estados unidos") || txt.includes("trader") || txt.includes("target") || txt.includes("costco") || txt.includes("gabacho");
      if (currentVoidOrigin === "China") return txt.includes("china") || txt.includes("aliexpress") || txt.includes("taobao") || txt.includes("sonoff") || txt.includes("roborock");
      if (currentVoidOrigin === "Japan") return txt.includes("japón") || txt.includes("japan") || txt.includes("corea") || txt.includes("korea") || txt.includes("biore") || txt.includes("deshumidificadores");
      if (currentVoidOrigin === "Europe") return txt.includes("europa") || txt.includes("europe") || txt.includes("alemania") || txt.includes("wera") || txt.includes("progreso");
      return true;
    });
  }

  if (query) {
    filtered = filtered.filter(v => {
      const txt = `${v.title} ${v.content} ${v.problem_summary || ''} ${v.venture_concept || ''}`.toLowerCase();
      return txt.includes(query);
    });
  }

  renderProductVoids(filtered);
}

function renderProductVoids(voids) {
  const grid = document.getElementById("product-voids-grid");
  if (!grid) return;

  if (!voids.length) {
    grid.innerHTML = `
      <div class="empty-state glass-panel" style="grid-column: 1 / -1; padding: 32px; text-align: center;">
        <span style="font-size: 32px;">🔍</span>
        <h3 style="margin-top: 8px;">${currentLang === "es" ? "No hay vacíos de producto para este filtro" : "No product voids matching current filters"}</h3>
        <p style="color: var(--text-muted); font-size: 13px;">${currentLang === "es" ? "Cambie el país de origen o agregue uno nuevo con '+ Enviar Producto Deseado'." : "Try switching origin countries or click '+ Submit Wishlist Item' to add one."}</p>
      </div>
    `;
    return;
  }

  grid.innerHTML = voids.map(v => {
    const txt = `${v.title} ${v.content}`.toLowerCase();
    let originBadge = currentLang === "es" ? "🌍 Internacional" : "🌍 International";
    let originClass = "badge-info";
    if (txt.includes("trader") || txt.includes("melatonina") || txt.includes("creami") || txt.includes("areneros") || txt.includes("costco") || txt.includes("usa") || txt.includes("gabacho")) {
      originBadge = currentLang === "es" ? "🇺🇸 Disponible en EE.UU." : "🇺🇸 Available in USA Retail";
      originClass = "badge-success";
    } else if (txt.includes("china") || txt.includes("zigbee") || txt.includes("aspiradoras") || txt.includes("molinos") || txt.includes("aliexpress")) {
      originBadge = currentLang === "es" ? "🇨🇳 Directo de China" : "🇨🇳 Direct from China";
      originClass = "badge-accent";
    } else if (txt.includes("japón") || txt.includes("japan") || txt.includes("corea") || txt.includes("korea") || txt.includes("biore") || txt.includes("deshumidificadores")) {
      originBadge = currentLang === "es" ? "🇯🇵 Especialidad Japón y Corea" : "🇯🇵 Japan & Korea Specialty";
      originClass = "badge-purple";
    } else if (txt.includes("europa") || txt.includes("europe") || txt.includes("progreso") || txt.includes("alemana")) {
      originBadge = currentLang === "es" ? "🇪🇺 Directo de Europa" : "🇪🇺 European Direct";
      originClass = "badge-info";
    }

    const urgencyStars = "🔴".repeat(v.urgency || 3);

    return `
      <div class="problem-card glass-panel" style="border-top: 3px solid var(--accent-cyan); display: flex; flex-direction: column; justify-content: space-between;">
        <div>
          <div class="problem-card-header">
            <span class="badge ${originClass}">${originBadge}</span>
            <span class="problem-urgency">${urgencyStars} ${currentLang === "es" ? "Urgencia" : "Void Severity"}</span>
          </div>

          <h4 class="problem-title" style="color: #fff; font-size: 15px; margin: 10px 0 6px;">${escapeHtml(v.title)}</h4>
          
          <div style="background: rgba(0,0,0,0.25); border-left: 2px solid var(--accent-orange); padding: 8px 12px; border-radius: 4px; margin: 8px 0; font-size: 12px; color: var(--text-main);">
            <strong style="color: var(--accent-orange);">⚠️ ${currentLang === "es" ? "Causa Raíz / Barrera" : "Root Cause / Barrier"}:</strong> ${escapeHtml(v.problem_summary || v.content.slice(0, 140))}
          </div>

          <p class="problem-content" style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">${escapeHtml(v.content ? v.content.slice(0, 180) + "..." : "")}</p>

          <div style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.1); border-radius: 4px; padding: 8px 12px; margin: 10px 0; font-size: 11px;">
            <div style="color: var(--text-dim); font-weight: 700;">${currentLang === "es" ? "SOLUCIÓN ACTUAL DEL CONSUMIDOR" : "CONSUMER WORKAROUND"}:</div>
            <div style="color: var(--text-main); margin-top: 2px;">${escapeHtml(v.solution_found || "Fayuca o casilleros postales pagando sobreprecio.")}</div>
          </div>

          <div class="problem-meta-row">
            <span class="meta-pill">📍 ${escapeHtml(v.city)}</span>
            <span class="meta-pill">🔗 ${escapeHtml(v.source_platform)}</span>
          </div>
        </div>

        ${v.venture_concept ? `
          <div class="problem-opp-box" style="margin-top: 12px; border-color: rgba(0, 191, 255, 0.3);">
            <div class="problem-opp-title" style="color: var(--accent-cyan);">💡 ${currentLang === "es" ? "Oportunidad de Arbitraje / Emprendimiento" : "Import Arbitrage & Venture Concept"}</div>
            <div style="font-size: 12px;"><strong>${escapeHtml(v.venture_concept)}</strong>: ${escapeHtml(v.solution_summary || "")}</div>
          </div>
        ` : ''}
      </div>
    `;
  }).join("");
}

// 11. Trigger Single Agent (Globally Available)
window.triggerSingleAgent = function(agentName) {
  showToast(currentLang === "es" ? `Iniciando agente ${agentName}...` : `Starting ${agentName} agent in background...`);
  fetch(`/api/agents/run/${agentName}`, { method: "POST" })
    .then(r => r.json())
    .then(() => {
      showToast(currentLang === "es" ? `Agente '${agentName}' ejecutado con éxito.` : `Agent '${agentName}' triggered successfully.`);
      setTimeout(() => {
        loadMetrics();
        loadLatestReport(currentRegion, currentLang);
        loadProblems();
        loadMercadoLibreProducts();
      }, 3500);
    })
    .catch(e => showToast("Error: " + e.message));
};

// 12. Markdown Parser & HTML Escaping
function parseMarkdownToHtml(md) {
  if (!md) return "";
  let html = md;

  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  html = html.replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>');
  html = html.replace(/\|(.+)\|/g, function(match) {
    if (match.includes("---")) return "";
    const cells = match.split("|").filter((_, i, arr) => i > 0 && i < arr.length - 1);
    const renderedCells = cells.map(c => `<td>${formatMarkdownText(c.trim())}</td>`).join("");
    return `<tr>${renderedCells}</tr>`;
  });
  html = html.replace(/(<tr>.+<\/tr>\s*)+/g, '<div class="table-responsive"><table class="data-table">$&</table></div>');
  html = html.replace(/^\s*\-\s+(.*$)/gim, '<li>$1</li>');
  html = html.replace(/(<li>.+<\/li>\s*)+/g, '<ul>$&</ul>');
  html = formatMarkdownText(html);
  html = html.replace(/\n\n/g, '<br><br>');
  return html;
}

function formatMarkdownText(txt) {
  if (!txt) return "";
  return txt
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\`([^`]+)\`/g, '<code>$1</code>');
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// -------------------------------------------------------------
// 12. Google Gemini Copilot & Conversational Research Assistant
// -------------------------------------------------------------
let geminiChatHistory = [];

function sendGeminiPrompt(text) {
  const input = document.getElementById("gemini-input");
  if (input) {
    input.value = text;
    handleGeminiSend();
  }
}

function clearGeminiChat() {
  geminiChatHistory = [];
  const feed = document.getElementById("gemini-chat-feed");
  if (feed) {
    feed.innerHTML = `
      <div class="chat-msg chat-assistant" style="display: flex; gap: 12px; align-items: flex-start;">
        <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #00e699, #00b4d8); display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">
          ✨
        </div>
        <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius-md); padding: 14px 18px; max-width: 85%; font-size: 14px; line-height: 1.6; color: var(--text-main);">
          <strong>¡Chat reiniciado!</strong><br>
          ¿Qué tema de consumo mexicano o producto de Mercado Libre te gustaría investigar ahora?
        </div>
      </div>
    `;
  }
}

async function handleGeminiSend() {
  const input = document.getElementById("gemini-input");
  const feed = document.getElementById("gemini-chat-feed");
  const btn = document.getElementById("btn-send-gemini");
  if (!input || !feed) return;

  const msg = input.value.trim();
  if (!msg) return;

  // Append user message
  const userMsgId = "msg-" + Date.now();
  feed.innerHTML += `
    <div class="chat-msg chat-user" id="${userMsgId}" style="display: flex; gap: 12px; justify-content: flex-end; align-items: flex-start;">
      <div style="background: rgba(0, 230, 153, 0.15); border: 1px solid rgba(0, 230, 153, 0.4); border-radius: var(--radius-md); padding: 12px 18px; max-width: 80%; font-size: 14px; line-height: 1.5; color: #fff;">
        ${escapeHtml(msg).replace(/\n/g, '<br>')}
      </div>
      <div style="width: 36px; height: 36px; border-radius: 50%; background: rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0;">
        👤
      </div>
    </div>
  `;

  input.value = "";
  feed.scrollTop = feed.scrollHeight;

  // Append loading indicator
  const loadingId = "loading-" + Date.now();
  feed.innerHTML += `
    <div class="chat-msg chat-assistant" id="${loadingId}" style="display: flex; gap: 12px; align-items: flex-start;">
      <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #00e699, #00b4d8); display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">
        ✨
      </div>
      <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius-md); padding: 14px 18px; font-size: 13px; color: var(--text-muted); display: flex; align-items: center; gap: 8px;">
        <div class="spinner" style="width: 14px; height: 14px; border-width: 2px;"></div>
        <span>Consultando a Google Gemini con datos en tiempo real de México...</span>
      </div>
    </div>
  `;
  feed.scrollTop = feed.scrollHeight;

  if (btn) btn.disabled = true;

  try {
    const res = await fetch("/api/gemini/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: msg,
        history: geminiChatHistory
      })
    });

    const data = await res.json();
    const loadingElem = document.getElementById(loadingId);
    if (loadingElem) loadingElem.remove();

    const reply = data.reply || "No response received.";
    const formattedReply = parseMarkdownToHtml(reply);

    feed.innerHTML += `
      <div class="chat-msg chat-assistant" style="display: flex; gap: 12px; align-items: flex-start;">
        <div style="width: 36px; height: 36px; border-radius: 50%; background: linear-gradient(135deg, #00e699, #00b4d8); display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">
          ✨
        </div>
        <div style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: var(--radius-md); padding: 16px 20px; max-width: 85%; font-size: 14px; line-height: 1.6; color: var(--text-main);">
          ${formattedReply}
          ${data.model_used ? `<div style="margin-top: 10px; font-size: 11px; color: var(--accent-cyan); font-family: var(--font-mono);">⚡ ${data.model_used}</div>` : ''}
        </div>
      </div>
    `;

    geminiChatHistory.push({ role: "user", parts: [msg] });
    geminiChatHistory.push({ role: "model", parts: [reply] });

  } catch (err) {
    console.error("Gemini request error:", err);
    const loadingElem = document.getElementById(loadingId);
    if (loadingElem) loadingElem.remove();

    feed.innerHTML += `
      <div class="chat-msg chat-assistant" style="display: flex; gap: 12px; align-items: flex-start;">
        <div style="width: 36px; height: 36px; border-radius: 50%; background: #ff4d6d; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0;">
          ⚠️
        </div>
        <div style="background: rgba(255, 77, 109, 0.1); border: 1px solid rgba(255, 77, 109, 0.3); border-radius: var(--radius-md); padding: 14px 18px; color: #ffb3c1; font-size: 13px;">
          Error al conectar con el servidor: ${err.message}
        </div>
      </div>
    `;
  } finally {
    if (btn) btn.disabled = false;
    feed.scrollTop = feed.scrollHeight;
  }
}

// Enter key submit on Gemini textarea
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("gemini-input");
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleGeminiSend();
      }
    });
  }
});

