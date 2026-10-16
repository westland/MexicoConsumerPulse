# 🇲🇽 MexConsumerPulse — Complete User Manual & Feature Guide

> **Platform URL (Production):** [https://pulse-mexico.com/](https://pulse-mexico.com/)  
> **Local Dashboard:** `http://localhost:8000/` (or run [`START_LOCAL_WEBSITE.bat`](START_LOCAL_WEBSITE.bat))  
> **REST API Documentation:** [https://pulse-mexico.com/docs](https://pulse-mexico.com/docs)  
> **Repository:** [https://github.com/westland/MexicoConsumerPulse](https://github.com/westland/MexicoConsumerPulse)  
> **Language Support:** Full Dual-Language Engine (🇲🇽 Mexican Spanish & 🇺🇸 English)

---

## Table of Contents
1. [Platform Overview & Architecture](#1-platform-overview--architecture)
2. [Header Controls & Non-Obvious Global Actions](#2-header-controls--non-obvious-global-actions)
   - [Bilingual Toggle (`[🇲🇽 ES | 🇺🇸 EN]`) & URL Routing](#bilingual-toggle-es--en--url-routing)
   - [Live CSV / JSON Data Export](#live-csv--json-data-export)
   - [Facebook Session & 2FA Setup (`Sesión FB`)](#facebook-session--2fa-setup-sesión-fb)
   - [Trigger Full Swarm (`Ejecutar Enjambre`)](#trigger-full-swarm-ejecutar-enjambre)
3. [WhatsApp Vecinos Community Ingestion (Step-by-Step)](#3-whatsapp-vecinos-community-ingestion-step-by-step)
   - [Why This Sensor Matters](#why-this-sensor-matters)
   - [Supported Export Formats (iOS & Android)](#supported-export-formats-ios--android)
   - [How to Export from WhatsApp](#how-to-export-from-whatsapp)
   - [Automated PII Scrubbing & Keyword Triggers](#automated-pii-scrubbing--keyword-triggers)
   - [Using the Ingestion Tool](#using-the-ingestion-tool)
4. [🎁 "I Wish They Sold This in Mexico" (Product Voids & Import Wishlist)](#4--i-wish-they-sold-this-in-mexico-product-voids--import-wishlist)
   - [Understanding Product Voids & Retail Arbitrage](#understanding-product-voids--retail-arbitrage)
   - [Origin Country Filters](#origin-country-filters)
   - [Submitting a New Wishlist Item](#submitting-a-new-wishlist-item)
5. [🛒 Mercado Libre México (MLM) Intelligence Tab](#5--mercado-libre-méxico-mlm-intelligence-tab)
   - [Real-Time Review Scraping & Mexican Failure Modes](#real-time-review-scraping--mexican-failure-modes)
   - [Interpreting Product Cards & Defect Warnings](#interpreting-product-cards--defect-warnings)
6. [Executive Daily Intelligence Reports Tab](#6-executive-daily-intelligence-reports-tab)
   - [Scope Selector: National vs. Mérida / Yucatán vs. Capital Cities](#scope-selector-national-vs-mérida--yucatán-vs-capital-cities)
   - [Downloading Raw Markdown Reports](#downloading-raw-markdown-reports)
7. [Problem Explorer & Dataset Search](#7-problem-explorer--dataset-search)
   - [Multi-Filter Hierarchy](#multi-filter-hierarchy)
   - [Mexican Slang & Modismos Search](#mexican-slang--modismos-search)
8. [Venture Opportunity Matrix](#8-venture-opportunity-matrix)
9. [🤖 Agent Operations & Swarm Audit](#9--agent-operations--swarm-audit)
   - [Individual Agent Re-execution](#individual-agent-re-execution)
   - [Checking Ingestion Pipeline Health](#checking-ingestion-pipeline-health)
10. [CLI & Server Automation Cheat Sheet](#10-cli--server-automation-cheat-sheet)

---

## 1. Platform Overview & Architecture

MexConsumerPulse is an autonomous multi-agent intelligence platform that continuously harvests, anonymizes, categorizes, and synthesizes Mexican consumer friction, municipal infrastructure gaps, and cross-border retail omissions across **Mexico City (CDMX)**, **Mérida & Yucatán**, **Guadalajara (GDL)**, and **Monterrey (MTY)**.

The platform runs on an 8-agent swarm:
* **Ingestion:** Reddit, Twitter/X, Facebook Groups, WhatsApp Vecinos, and Mercado Libre México.
* **Governance:** Compliance Agent enforcing the *Ley Federal de Protección de Datos Personales*.
* **Intelligence:** Synthesis & NLP Opportunity Engine mapping Mexican modismos and calculating urgency.
* **Delivery:** Executive Report Generator and FastAPI REST engine.

---

## 2. Header Controls & Non-Obvious Global Actions

Located in the top header bar across all tabs:

### Bilingual Toggle (`[🇲🇽 ES | 🇺🇸 EN]`) & URL Routing
* **How it works:** Toggles all interface text, metric labels, tab headers, filter options, cards, and daily briefing contents between Mexican Spanish (`es-MX`) and English (`en-US`).
* **Non-obvious behavior:**
  * Your preference is saved to browser `localStorage` under `mex_pulse_lang`.
  * The server also listens to URL paths: navigating to `/es` or `/?lang=es` loads Spanish by default; `/en` or `/?lang=en` loads English.
  * When you switch language on the **Daily Intelligence Report** tab, the platform actively queries the backend for the pre-compiled Spanish (`*_es.md`) or English (`*_en.md`) briefing version without refreshing the page.

### Live CSV / JSON Data Export
* **Button:** `Exportar CSV` / `Export CSV`
* **Direct Endpoints:**
  * CSV: `GET /api/exports/csv`
  * JSON: `GET /api/exports/json`
* **Non-obvious behavior:** The download is generated on-the-fly from the persistent SQLite database (`data/mexico_consumer_insights.db`), but **guarantees zero PII leakage**. Names, Mexican phone numbers, RFC tax identifiers, CURP strings, and exact apartment unit numbers are stripped *before* the export is packaged.

### Facebook Session & 2FA Setup (`Sesión FB`)
* **Button:** `Sesión FB` / `FB Session` in the header or in the **Facebook Groups Browser Agent** card.
* **Why it is needed:** Mexican neighborhood groups (*"Vecinos Condesa"*, *"Vecinos Roma Norte"*, *"Expats in Mérida"*, *"Lady Multitask"*) are closed or private, protected by anti-bot verification and gatekeeper screening questions (e.g., *"¿En qué calle o colonia vives?"*). Headless scrapers get blocked.
* **How to use it:**
  1. Click **`Sesión FB`**. A modal dialog appears.
  2. Click **`Launch Headed Login Browser`** (or execute `python run.py --fb-login` in terminal).
  3. An automated Google Chrome / Chromium window will pop open on your desktop via Playwright.
  4. Manually type your Facebook username, password, and approve your 2FA authentication prompt (SMS or authenticator app).
  5. Navigate to your target private groups and answer any gatekeeper screening questions if prompted.
  6. **You do not need to save anything manually.** The agent watches the browser URL; as soon as it detects the Facebook feed (`/home` or `/groups`), it extracts your encrypted session cookies and writes them to:
     ```text
     data/auth_state/facebook_state.json
     ```
  7. Subsequent automated runs will now browse Facebook in headless mode using this session state without triggering bot verification.

### Trigger Full Swarm (`Ejecutar Enjambre`)
* **Button:** Green `Ejecutar Enjambre` / `Run Agent Swarm` button.
* **What happens:** Dispatches an asynchronous `POST /api/agents/run/all` background task on the server. The multi-agent swarm runs the entire collection loop:
  1. Harvests subreddits (r/mexicocity, r/gdl, r/monterrey, r/merida, r/yucatan, r/mexicoexpats).
  2. Queries agency Twitter handles (`@CFEmx`, `@SacmexCDMX`, `@SATMX`, `@Profeco`).
  3. Checks Mercado Libre México prices and failure reviews.
  4. Cleans and scores new records.
  5. Re-compiles all 10 national and regional markdown daily briefings.
  6. The frontend automatically updates KPIs and lists after 4 seconds.

---

## 3. WhatsApp Vecinos Community Ingestion (Step-by-Step)

Located in Tab 5: **`💬 Ingesta de WhatsApp Vecinos`** (`tab-whatsapp`).

### Why This Sensor Matters
In Mexico, residential building and neighborhood WhatsApp groups are the single fastest early warning sensor for civic problems. When a CFE transformer blows up, a SACMEX water pipeline is shut down for *tandeo*, or an unauthorized contractor scams a building resident, it appears on the neighborhood WhatsApp group hours before any public agency acknowledges it.

### Supported Export Formats (iOS & Android)
The ingestion parser is equipped with a regex header matcher (`msg_header_pattern`) that handles both standard WhatsApp timestamp conventions:
1. **iOS Export Format:**
   ```text
   [14/10/26, 08:15:30] +52 55 9876 5432: Buenos días vecinos, no cae agua en el edificio 42...
   ```
2. **Android Export Format:**
   ```text
   14/10/26, 8:15 AM - Vecino Depto 301: Hola, aquí en el 48 tampoco cae agua de Sacmex...
   ```
3. **Multi-line Messages:** If a neighbor writes a lengthy complaint across multiple paragraphs, the parser automatically concatenates them until the next message timestamp appears.

### How to Export from WhatsApp
1. Open the target WhatsApp group on your phone (e.g., your building chat or neighborhood watch group).
2. Tap the group name at the top to open **Group Info**.
3. Scroll down and tap **Export Chat** (or *Exportar chat*).
4. **Crucial:** Select **"Without Media"** (*Sin archivos*). This produces a clean `.txt` file.
5. AirDrop, email, or copy the `.txt` content to your clipboard.

### Automated PII Scrubbing & Keyword Triggers
Before any message is allowed into the intelligence database, two automated layers run:
1. **System & Noise Elimination:** System notices like `<Media omitted>`, *Archivo omitido*, *cambió el código de seguridad*, *creó el grupo*, and *los mensajes están cifrados* are filtered out.
2. **Friction Keyword Filtering:** The agent only processes messages containing actionable consumer friction triggers:
   * *Water & Utilities:* `"sin agua"`, `"no cae agua"`, `"tandeo"`, `"pipa"`, `"sacmex"`, `"se fue la luz"`, `"sin luz"`, `"cfe"`, `"fuga"`, `"gas"`, `"tanque"`, `"boiler"`
   * *Trades & Fraud:* `"recomiendan"`, `"plomero"`, `"albañil"`, `"electricista"`, `"estafaron"`, `"no vino"`, `"anticipo"`
   * *Property & Security:* `"gotera"`, `"impermeabilizar"`, `"ruido"`, `"bache"`, `"cerradura"`, `"seguridad"`
3. **Mexican PII Redaction:**
   * Phone numbers (`+52 55...`, `+52 999...`, `55-XXXX-XXXX`) are masked.
   * Mexican taxpayer identification (`RFC`) and population registry keys (`CURP`) are redacted.
   * Specific interior apartment units (e.g. *Depto 301*) and personal names are replaced with anonymous neighborhood placeholders.

### Using the Ingestion Tool
1. In the **Group Name** field (`wa-group-name`), enter the community name (e.g., `Vecinos Ámsterdam Condesa` or `Vecinos Montes de Amé Mérida`).
2. In the **City** field (`wa-city`), select or enter the municipality (e.g., `Mexico City (CDMX)` or `Mérida & Yucatán`).
3. If you want to test the workflow first, click **`Cargar Chat de Ejemplo`** (**Load Sample Chat**). This populates realistic Mexican neighbor conversations about SACMEX water cutoffs, emergency *pipa* prices ($2,200 MXN per 5,000L), boiler repair scams, and CFE transformer failures.
4. Paste your exported text into the large box.
5. Click **`Anonimizar e Ingerir Chat`** (**Scrub PII & Ingest Chat**).
6. **Result:** An alert notifies you of the exact number of extracted problems. A card appears under **`✦ Problemas Comunitarios Extraídos`** showing:
   * Categorization (e.g., *Infrastructure & Utilities*, *Home Maintenance & Trades*)
   * Urgency score (1 to 5)
   * The scrubbed text
   * The automatically generated **Venture Hypothesis** (e.g., *PipaExpress: On-demand transparent water truck dispatch* or *Vetted HVAC escrow repair network*).
   * Global metrics and Problem Explorer update immediately.

---

## 4. 🎁 "I Wish They Sold This in Mexico" (Product Voids & Import Wishlist)

Located in Tab 3: **`🎁 "Ojalá Vendieran Esto" (Vacíos e Importaciones)`** (`tab-product-voids`).

### Understanding Product Voids & Retail Arbitrage
A "product void" is a product that has high consumer demand in Mexico and is easily purchased in the United States, China, Japan, Korea, or Europe, but is **unavailable through formal Mexican retail channels**. The causes usually include:
* **Regulatory blocks:** COFEPRIS classifying generic bulk supplements (like 365-count melatonin or allergy medicine) under stricter OTC rules; or NOM standards assuming residential dishwashers must be 60cm standard width.
* **Electrical incompatibilities:** Smart home switches requiring a "neutral wire" which 85% of Mexican residential conduits lack.
* **Retail neglect:** Big-box retailers (Walmart México, Liverpool, Home Depot) failing to stock compact countertop appliances suited for small urban apartments in Condesa, Roma, or Providencia.

### Origin Country Filters
Use the pill filter buttons to quickly isolate cross-border opportunities:
* **`🌍 Todos los Orígenes` (`All`):** Displays all verified product voids.
* **`🇺🇸 Comercio EE. UU.` (`USA`):** Filters for items bought across the border or commanding 300–400% markups on grey-market Instagram/Mercado Libre channels (e.g., *Trader Joe's Everything Bagel Seasoning*, *Ninja Creami*, *Bulk Generic OTC meds*).
* **`🇨🇳 Directo de China` (`China`):** Filters for electronics requiring adaptation to Mexican infrastructure (e.g., *Matter/Zigbee No-Neutral Smart Relays*, *Flagship Robot Vacuums with hot water mop washing*).
* **`🇯🇵 Japón y Corea` (`Japan`):** Filters for tropical climate skin and home solutions (e.g., *Ultralight UV sunscreens with next-gen filters*, *Continuous drain tropical dehumidifiers*).
* **`🇪🇺 Europa` (`Europe`):** Highlights specialized tools and maritime logistics gaps (e.g., *Wera/Knipex precision hand tools*, *Miami-to-Progreso direct container consolidation*).

### Submitting a New Wishlist Item
Users and market researchers can directly expand the product void database from the website:
1. Click **`+ Sugerir Producto Deseado`** (**`+ Submit Wishlist Item`**) on the right of the filter bar.
2. A collapsible glassmorphism panel slides open.
3. Fill in the fields:
   * **Nombre del Producto y Marca (Product Name & Brand):** e.g., *Trader Joe's Cookie Butter* or *Countertop compact water softener*.
   * **Disponible en (Origin Country):** Select `USA`, `China`, `Japan`, `Korea`, or `Europe`.
   * **Tu Ciudad / Región (City):** Select `CDMX`, `Mérida`, `GDL`, `MTY`, or `National`.
   * **¿Por qué no se vende / Cómo lo consigues actualmente? (Why is it missing?):** Describe customs issues, lack of domestic warranty, or how much you pay to have relatives bring it (*"traer del gabacho"*).
4. Click **`Enviar al Enjambre de Investigación`** (**Submit to Research Swarm**).
5. **Behind the scenes:**
   * Handled by `POST /api/product-voids/submit`.
   * The item is saved with 0.99 confidence and automatically routed to the Synthesis Engine.
   * The Synthesis Engine creates a venture hypothesis explaining how an entrepreneur could import and distribute this item legally in Mexico.
   * The new card appears in the grid immediately with a cyan border.

---

## 5. 🛒 Mercado Libre México (MLM) Intelligence Tab

Located in Tab 6: **`🛒 Mercado Libre México`** (`tab-mercadolibre`).

### Where to Find Mercado Libre Sales, Products & Sentiment in the App
The platform tracks real-time consumer sales trends, product velocity, and user sentiment across multiple core areas of the application:
1. **The Interactive MLM Dashboard (Tab 6):** The primary visual interface featuring live statistics, category filtering, sales velocity indicators, and sentiment cards.
2. **The Executive Daily Intelligence Report (Tab 1, Section 7):** Formatted executive summaries broken down into *Section 7.1 (Sales Velocity & Breakout Trends)* and *Section 7.2 (Critical Flaws & 1–3 Star Complaints)*.
3. **The REST API (`/api/mercadolibre/*`):** Structured JSON endpoints providing real-time sales growth metrics, buyer quotes, and failure modes for programmatic consumption.
4. **The Swarm Harvester CLI (`python run.py --ml-*`):** Autonomous background crawling updating the sales and review database on demand.

---

### Consumer Sales Velocity & What People Like (🔥 Hot New Products)

To see what products are currently experiencing explosive sales in Mexico and **what consumers love about them**:
1. Click the **`🔥 Hot New Products & Tendencias`** filter pill at the top of Tab 6.
2. Review the product cards (`ml-card-hot`), accented in amber and gold.
3. **Consumer Sales & Demand Indicators:**
   * **Sales Badges:** Track badges like `🔥 MÁS VENDIDO #1`, `⚡ TENDENCIA VIRAL`, and `📈 VENTAS EN ALZA`.
   * **Demand Growth Metrics:** Look for green percentage spikes detailing sales catalysts (e.g., `+420% búsquedas durante apagones CFE` or `+510% durante cortes Cutzamala`).
   * **Pricing in MXN:** Real-time pricing indicating consumer willingness-to-pay (e.g., `$13,499 MXN` for portable power stations, `$1,890 MXN` for cistern sensors).
   * **Estimated Sales Volume:** Signals monthly retail velocity on `mercadolibre.com.mx`.
4. **What People Like (Adoption Drivers & Strengths):**
   * **High Star Ratings:** Displays customer satisfaction levels (typically 4.7 ⭐ to 4.9 ⭐).
   * **`¿Por qué gusta a los mexicanos?` (Adoption Catalyst):** Highlights exact buyer praise explaining why the product is succeeding (e.g., *Keeps home Wi-Fi and CPAP running silently for 14 hours during heatwave blackouts with zero gasoline fumes*; *Direct DC solar connection bypasses expensive CFE DAC tariff brackets without requiring grid tie-in permits*; *Fits into tight Condesa/Roma rental kitchens with no rough-in plumbing alterations required*).
   * **Oportunidad de Escalamiento / Venture Hypothesis:** Strategic business model recommendations for founders and e-commerce operators to import, bundle, or localize these products.

---

### Critical Flaws, Failure Modes & What People DON'T Like (⚠️ 1–3 ⭐ Defect Audits)

To see which products are failing in the Mexican market, experiencing high return rates, or **what buyers dislike and complain about**:
1. Click the **`⚠️ Fallas en Productos Existentes (1–3 ⭐)`** filter pill at the top of Tab 6.
2. Review the problem cards (`ml-card-problem`), accented in alert crimson.
3. **Negative Review & Defect Metrics:**
   * **Depressed Star Ratings:** Pinpoints poorly reviewed listings averaging 1.8 ⭐ to 2.6 ⭐.
   * **Failure Mode Header:** Clearly identifies the root engineering or structural failure (e.g., `Falla: Obstrucción por carbonato de calcio kárstico en <14 días`, `Falla: Fusible térmico interno soldado no reemplazable`, `Falla: Desbordamiento por humedad relativa >90% en costa`).
4. **What People DON'T Like (Verbatim Mexican Buyer Quotes):**
   * **Verbatim Reviews:** Every problem card displays authentic 1–3 star customer complaints extracted from Mexican buyers on Mercado Libre, highlighting recurring frustrations:
     > *"En Mérida el agua tiene tanto sarro que la membrana de cerámica se tapó por completo a los 12 días; la lavé con vinagre como dice el manual y no sirvió para nada."*
     > *"Con el primer apagón de CFE en Monterrey tronó el regulador. Al abrirlo vi que el fusible viene soldado a la placa y no hay refacción en México."*
     > *"Vivo en Progreso y el tanque de 2 litros se llena en 3 horas y media. Si sales a trabajar se desborda y además calienta la recámara 3 grados."*
   * **Hypothesis for Product Redesign:** Provides actionable engineering fixes (e.g., swapping standard membranes for ion-exchange resin pre-filters, introducing external replaceable slow-blow fuses, or designing continuous gravity-drain hoses with thermoelectric Peltier cooling).

---

### Filter Controls & View Modes in the App
* **`Todos los Artículos` (`All Products`):** Consolidated view comparing hot winners alongside flawed products side-by-side.
* **`🔥 Hot New Products & Tendencias`:** Isolates breakout sales leaders.
* **`⚠️ Fallas en Productos Existentes (1–3 ⭐)`:** Isolates negative review defect audits.
* **Categoría (Category Selector):** Drill down into:
  - *⚡ Energía y Red CFE* (Power stations, regulators, inverters)
  - *💧 Agua y Sarro* (Purifiers, softeners, water pumps)
  - *🌴 Clima y Humedad Tropical* (Dehumidifiers, solar mini-splits)
  - *🍳 Electrodomésticos y Departamentos* (Countertop dishwashers, ice makers)
  - *📱 Smart Home y Automatización* (Cistern level sensors, smart relays)
  - *🔧 Plomería e Hidráulica* (Solar heaters, booster pump flow switches)
* **Direct MLM Verification Link:** Click **`Ver Artículo en Mercado Libre ↗`** on any card to navigate directly to the product on `mercadolibre.com.mx`.

---

### Mercado Libre Data in the Executive Report (Tab 1)
When navigating to the **Informe Diario de Inteligencia** (Tab 1), scroll to **Sección 7: Inteligencia Minorista de Mercado Libre México**:
* **Sección 7.1 (Hot Products & Ventas):** Provides executive bullet points on sales velocity surges, top trending ASINs/categories, and key consumer satisfaction drivers.
* **Sección 7.2 (Fallas Críticas y Reseñas Negativas):** Synthesizes negative review patterns, regional failure breakdowns (Yucatán limestone, Northern grid fluctuations), and specific buyer quotes for investor-grade diligence.

---

## 6. Executive Daily Intelligence Reports Tab

Located in Tab 1: **`Informe Diario de Inteligencia`** (`tab-report`).

### Scope Selector: National vs. Mérida / Yucatán vs. Capital Cities
At the top right of the report card, use the **`Alcance del Informe:`** dropdown:
* **🇲🇽 Reporte Nacional Multiciudad:** A holistic macro analysis covering nationwide utility trends, federal agencies (`SAT`, `PROFECO`, `CFE`), and general consumer sentiment.
* **🌴 Reporte Mérida y Península de Yucatán:** A deep-dive briefing covering limestone water scale (*sarro kárstico*), summer electrical blackouts, rapid gentrification in northern Mérida (Temozón Norte, Montes de Amé), and expat relocation friction.
* **🏙️ Ciudad de México (CDMX):** Focuses on SACMEX water rationing, gentrification rent disputes in Cuauhtémoc/Benito Juárez, and public transit issues.
* **🌮 Guadalajara (GDL) & ⛰️ Monterrey (MTY):** Focuses on manufacturing boomtown housing pressure, industrial water shortages, and localized utility strain.

### Downloading Raw Markdown Reports
* Click **`Descargar Markdown`** (**Download Markdown**).
* This immediately generates and downloads an offline `.md` file titled `mexico_consumer_report_<DATE>_<LANG>.md` containing executive bullet points, data tables, and formatted failure matrices for distribution to investors or team members.

---

## 7. Problem Explorer & Dataset Search

Located in Tab 2: **`Explorador de Problemas y Datos`** (`tab-explorer`).

### Multi-Filter Hierarchy
You can combine all four filter controls simultaneously:
1. **Ciudad / Región:** Filter to problems originating from a specific city.
2. **Categoría:** Narrow to:
   * *Product Voids & Import Wishlist*
   * *Infrastructure & Utilities*
   * *Bureaucracy & GovTech*
   * *Home Maintenance & Trades*
   * *Housing & Real Estate*
   * *Marketplaces & Consumer Scams*
   * *Expat & Relocation Friction*
3. **Población Objetivo (Audience):**
   * `🇲🇽 Residentes Locales` (Local citizens)
   * `🇺🇸 Expats / Extranjeros` (Foreign residents, digital nomads)
   * `👥 Compartido` (Shared urban friction)

### Mexican Slang & Modismos Search
The search input box (`#search-input`) is linked to a Mexican slang lexicon. You can search directly using colloquial terms:
* Search `"tandeo"` or `"pipa"` to find water rationing issues.
* Search `"tranza"` or `"estafa"` to surface contractor or marketplace fraud.
* Search `"mordida"` or `"citas SAT"` to surface bureaucratic bottlenecks.
* Search `"sarro"` to find plumbing and appliance calcification records.
* Search `"casero"` or `"depósito"` to review rental lease and security deposit disputes.

---

## 8. Venture Opportunity Matrix

Located in Tab 4: **`Matriz de Oportunidades de Negocio`** (`tab-ventures`).

* **How it works:** Whenever the autonomous agents ingest a consumer complaint scoring an urgency of **3 or higher**, the **Synthesis & NLP Opportunity Engine** translates the problem into an actionable commercial startup concept.
* **What each card displays:**
  * **Venture Name:** (e.g., *PipaExpress*, *DepósitoSeguro MX*, *MéridaGrid IoT*, *SarroShield MX*).
  * **Core Value Proposition:** A concise statement explaining how the business solves the consumer pain point.
  * **Target Demographics & Geography:** Identifies whether the customer base is local, expat, or both, and the primary initial launch city.

---

## 9. 🤖 Agent Operations & Swarm Audit

Located in Tab 7: **`🤖 Operaciones y Reporte de Agentes`** (`tab-agents`).

### Individual Agent Re-execution
If you only want to scrape a specific data source without waiting for the full pipeline, scroll to the agent's dossier card and click its execution button:
* **Reddit Agent:** Click `Re-run Reddit Agent` (`triggerSingleAgent('reddit')`).
* **Twitter / X Monitor:** Click `Re-run Twitter Agent` (`triggerSingleAgent('twitter')`).
* **Facebook Agent:** Click `Run FB Agent` (`triggerSingleAgent('facebook')`).
* **Mercado Libre Scraper:** Click `Ejecutar Agente Mercado Libre` (`triggerSingleAgent('mercadolibre')`).
* **Report Synthesizer:** Click `Re-synthesize Intelligence` (`triggerSingleAgent('report')`).

### Checking Ingestion Pipeline Health
* **Auditoría Ejecutiva (Scorecard):** Confirms that all agents are online and displays total verified records harvested.
* **Ley Federal Sanitization Badge:** Confirms **100% PII Scrubbing** status.
* **Server Status Box:** Displays production deployment details for Hetzner Cloud VPS (`pulse-mexico.com` at `89.167.22.10`), including active Docker containers, reverse proxy routing, and SSL status.

---

## 10. CLI & Server Automation Cheat Sheet

For users managing or automating the platform outside the browser:

```powershell
# 1. Start Web Dashboard Locally
python run.py --web
# (Opens http://localhost:8000/)

# 2. Run Full Collection & Report Cycle
python run.py --all

# 3. Interactive Facebook Headed Browser Setup
python run.py --fb-login

# 4. Ingest WhatsApp Vecinos Sample via CLI
python run.py --whatsapp

# 5. Scrape Mercado Libre México via CLI
python run.py --mercadolibre

# 6. Export Database to Clean CSV & JSON
python run.py --export
# Stored in: data/exports/mexico_consumer_problems_latest.csv
```
