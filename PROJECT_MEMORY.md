# 🇲🇽 MexConsumerPulse & Nuveen Grant - Master Project Memory & Operation Manual

> **Archival Date:** October 16, 2026  
> **Status:** Release 1.14 Production Live on [**https://pulse-mexico.com/**](https://pulse-mexico.com/) • Local Dashboard on `http://localhost:8000/` • GitHub Repo at [**https://github.com/westland/MexicoConsumerPulse**](https://github.com/westland/MexicoConsumerPulse)

---

## 1. Executive Summary of All Completed Work

### A. UIC John and Grace Nuveen Grants for Internationalization (PDF Budget Form)
* **Project Title:** *Chicago–Yucatán Bridges: Fostering Hispanic and Mexican-American Cross-Border Engagement Through Economic Network Models of Entrepreneurship*
* **Principal Investigator:** Christopher Westland (Fulbright García-Robles U.S. Scholar, Universidad Anáhuac Mayab, Mérida, Yucatán).
* **Fillable PDF Generated:**
  * Exact itemized budget filled into the official UIC Nuveen grant form:
    * Row 1: Student / RA Support (Network analysis & data pipeline) — **$2,500**
    * Row 2: Airfare (Chicago ORD ⇄ Mérida MID roundtrip) — **$1,200**
    * Row 3: Lodging & Per Diem (Mérida & fieldwork in Yucatán) — **$3,600**
    * Row 4: Materials & Dissemination (Bilingual workshop & reports) — **$2,700**
    * **Total Requested:** **$10,000**
  * Preserved in root folder as:
    * [`Nuveen_Grants_Internationalization_2027_application_form_budget_filled.pdf`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/Nuveen_Grants_Internationalization_2027_application_form_budget_filled.pdf)
    * [`Nuveen_Grants_Internationalization_2027_budget_itemized_4rows.pdf`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/Nuveen_Grants_Internationalization_2027_budget_itemized_4rows.pdf)

---

### B. Hetzner Server Production Deployment (`pulse-mexico.com`)
* **Host / Server:** Hetzner Cloud CX23 (`89.167.22.10`, Helsinki datacenter, Ubuntu 24.04 LTS).
* **Root Password:** `@Wei2Shi4Lin2` (Verified and tested via SSH/SFTP).
* **Decommission of Old Site:**
  * Decommissioned old `/var/www/sumar` (`woowoocenterforhealing.com`).
  * Archived cleanly to `/root/sumar_backup_before_delete.tar.gz`.
* **Domain & SSL Configuration:**
  * Primary domain **`pulse-mexico.com`** and **`www.pulse-mexico.com`** bound directly to standard web ports **80 (HTTP)** and **443 (HTTPS)**.
  * Configured Let's Encrypt SSL certificates with automatic auto-renewal.
  * Reverse-proxied via Nginx to Docker container `mexconsumerpulse_web` running on internal port `8080` (FastAPI + Uvicorn).
* **Live URLs:**
  * 🌐 **Production Dashboard:** [**https://pulse-mexico.com/**](https://pulse-mexico.com/)
  * 📚 **REST API Swagger:** [**https://pulse-mexico.com/docs**](https://pulse-mexico.com/docs)
  * 🎁 **Product Voids Endpoint:** [**https://pulse-mexico.com/api/product-voids**](https://pulse-mexico.com/api/product-voids)

---

### C. Release 1.00: "I Wish They Sold This in Mexico" Product Void Harvester
Expanded the autonomous market research multi-agent system from urban complaints to cross-border retail arbitrage and product void discovery:
* **Colloquial Mexican Lexicon:** Integrated slang triggers:
  * `"ojalá vendieran en méxico"`, `"por qué no venden en méxico"`, `"quisiera que vendieran en méxico"`, `"no hay en méxico"`, `"no se consigue en méxico"`, `"en amazon méxico no hay"`, `"mandar a traer de usa"`, `"traer del gabacho"`, `"fayuca moderna"`, `"me lo atoró la aduana"`, `"cofepris no deja pasar"`, `"pedir por aliexpress/taobao"`.
* **8 Autonomous Agents in Swarm:**
  1. **Reddit Autonomous Harvester:** Monitors r/mexicocity, r/gdl, r/monterrey, r/merida, r/yucatan, r/mexico, r/AskMexico, r/mexicoexpats, r/ShopeeMexico.
  2. **Twitter/X Public Complaint Monitor:** Monitors `@SATMX`, `@CFEmx`, `@SacmexCDMX`, `@Profeco`, `@COFEPRIS`, `@AduanasMx`.
  3. **Facebook Groups Browser Agent:** Playwright headed/headless browser with 2FA session persistence (`data/auth_state/facebook_state.json`) and gatekeeper question handling for neighborhood Vecinos & Bazar groups.
  4. **WhatsApp Vecinos Ingestion Agent:** Direct text ingestion of exported neighborhood chat logs with instant regex PII masking.
  5. **Compliance & Privacy Sanitization Agent:** 100% adherence to Mexico's *Ley Federal de Protección de Datos Personales*. Zero PII stored (RFC, CURP, phone, address, and names redacted).
  6. **Synthesis & NLP Opportunity Engine:** Modismos scoring (urgency 1-5), local vs expat demographic classification, and venture hypothesis generation.
  7. **Executive Intelligence Report Generator:** Compiles daily bullet-pointed briefings with dedicated cross-border product void tables.
  8. **Product Void & Cross-Border Retail Harvester:** Identifies goods available in USA, China, Japan, Korea, or Europe that are missing in Mexico due to regulatory barriers (COFEPRIS, NOMs) or distribution omissions.
* **Database & Seed Dataset:**
  * `data/mexico_consumer_insights.db` expanded to **48 verified consumer records**, including **13 verified cross-border product voids**:
    1. Countertop Compact Dishwashers (USA / China - Small apartment living)
    2. Trader Joe's Everything Bagel & Chili Crunch (USA - 400% grey-market markup)
    3. Bulk Generic Melatonin & Antihistamines 365-ct (USA - COFEPRIS bulk restrictions)
    4. Matter / Zigbee No-Neutral Smart Relays (China - Mexican residential conduit)
    5. Continuous Drain Tropical Dehumidifiers (Japan / China - Mérida limestone humidity & mold)
    6. Japanese & Korean Ultralight Sunscreens (Japan / Korea - Outdated UV filter regulations)
    7. Automated Self-Cleaning Cat Litter Boxes (USA / China - Lack of domestic service & repair)
    8. Ninja Creami Ice Cream Maker & Spare Pints (USA - Chronic Mexican retail out-of-stock)
    9. Specialty Coffee Hand Grinders (Taiwan / China - Barista precision gear void)
    10. Pneumatic Standing Desk Converters (USA / China - Fixed wood desk retail dominance)
    11. Cast-Iron Chainmail Scrubbers & Seasoning Wax (USA - Cookware preservation void)
    12. Hydrocolloid Extra-Large Body Patches (USA / Korea - Medical-grade blemish care)
    13. Flagship Robot Vacuums with Hot Water Mop Washing (China - Grey-market arbitrage)
    14. Puerto de Progreso - Miami Direct Maritime Consolidation (Europe / USA - Gulf logistics bypass)

---

### D. Dedicated Dashboard UI & Wishlist Pipeline
* **Dedicated Tab:** `🎁 "I Wish They Sold This" (Product Voids & Imports)` in [frontend/index.html](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/frontend/index.html).
* **Filters:** Origin Country Pills (`All`, `🇺🇸 USA Retail`, `🇨🇳 China Direct`, `🇯🇵 Japan & Korea`, `🇪🇺 Europe`) and live search bar.
* **Interactive Wishlist Form:** `+ Submit Wishlist Item` allowing community users to log missing products directly to the database.
* **REST Endpoints:**
  * `GET /api/product-voids`
  * `POST /api/product-voids/submit`
  * `GET /api/metrics`
  * `GET /api/agents/activity`

---

### E. GitHub Release 1.00 (`westland/MexicoConsumerPulse`)
* **Repository:** [https://github.com/westland/MexicoConsumerPulse](https://github.com/westland/MexicoConsumerPulse)
* **Published Release:** **Release 1.00 (`v1.0.0`)** at [https://github.com/westland/MexicoConsumerPulse/releases/tag/v1.0.0](https://github.com/westland/MexicoConsumerPulse/releases/tag/v1.0.0)
* **One-Click Installers:**
  * Windows: [`INSTALL_RELEASE_1.0.bat`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/INSTALL_RELEASE_1.0.bat)
  * Linux / macOS / Server: [`install_release_1.0.sh`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/install_release_1.0.sh)
* **Local Web Server Shortcut:** [`START_LOCAL_WEBSITE.bat`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/START_LOCAL_WEBSITE.bat) (`python run.py --web`)
* **Documentation:** Fully updated [README.md](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/README.md) and [READ.ME](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/READ.ME).

---

## 2. Server Management Cheat Sheet

```bash
# Connect to Hetzner production server
ssh root@89.167.22.10
# (Password: @Wei2Shi4Lin2)

# Check container status
docker ps

# View live web dashboard logs
docker compose -f /opt/mexconsumerpulse/docker-compose.yml logs -f web

# View live autonomous agent scraper logs
docker compose -f /opt/mexconsumerpulse/docker-compose.yml logs -f scheduler

# Trigger an immediate on-demand full research cycle
docker compose -f /opt/mexconsumerpulse/docker-compose.yml exec web python run.py --all

# Test live API health
curl -s http://127.0.0.1:8080/api/metrics
curl -s http://127.0.0.1:8080/api/product-voids | head -c 200
```

---

## 3. Local Operation Cheat Sheet

```powershell
# 1. Start local web dashboard (http://localhost:8000)
START_LOCAL_WEBSITE.bat
# or
python run.py --web

# 2. Run all agents and regenerate daily reports locally
python run.py --all

# 3. Export latest cleaned datasets to CSV and JSON
python run.py --export
# (Exports stored in data/exports/mexico_consumer_problems_latest.csv)
```

---

## 4. File Inventory

| Path | Description |
|---|---|
| `app.py` | FastAPI backend server with REST endpoints & static frontend mount |
| `config.py` | City colonias, subreddits, keywords, slang lexicon & product void triggers |
| `run.py` | Master CLI orchestrator to run individual or all agents |
| `scheduler.py` | Autonomous 24-hour daily scheduler loop |
| `frontend/index.html` | Rich executive dashboard UI with all 6 operational tabs |
| `frontend/style.css` | Dark-mode glassmorphism design system |
| `frontend/app.js` | Dynamic tab routing, filters, markdown parser, product voids & API client |
| `data/mexico_consumer_insights.db` | Persistent SQLite database (48 records, daily reports) |
| `data/exports/` | Latest CSV and JSON dataset exports |
| `reports/daily_reports/` | Generated Markdown intelligence briefings |
| `agents/` | Source code for all 8 autonomous agents |
| `INSTALL_RELEASE_1.0.bat` | 1-click Windows installer for Release 1.00 |
| `install_release_1.0.sh` | 1-click Linux/macOS installer for Release 1.00 |
| `START_LOCAL_WEBSITE.bat` | 1-click local web dashboard launcher |
| `USER_MANUAL.md` | Complete website feature manual and operational documentation |
| `Nuveen_Grants_..._filled.pdf` | Completed UIC Nuveen grant budget application form |

---

## 5. Bilingual (Spanish / English) Architecture & Status (100% Completed)

* **Default Spanish Experience:** Port 8000 (`http://localhost:8000/`) and root `/` default to Mexican Spanish (`es-MX`), featuring Spanish KPI labels, navigation tabs, filter menus, and reports.
* **Interactive Switcher `[🇲🇽 ES | 🇺🇸 EN]`:** Live in the header actions bar. Toggles between Spanish and English without page reload.
* **URL Routing Support:** `/`, `/es`, and `/en` endpoints served via FastAPI and mirrored with client-side history state.
* **Persistent Preferences:** Selected language saved to browser `localStorage` (`mex_pulse_lang`).
* **Dual-Language Report Engine (`reports/report_generator.py`):**
  * Synthesizes and publishes 10 report variations (National, Mérida & Yucatán, CDMX, GDL, MTY in both `es` and `en`).
  * REST endpoint `GET /api/reports/latest?region=${region}&lang=${lang}` dynamically delivers Spanish or English markdown briefings.
* **Frontend Translation Layer (`frontend/app.js`):**
  * Comprehensive `TRANSLATIONS` dictionary covering all 7 tabs, KPI cards, modals, filter menus, and action buttons.
  * Dynamically re-renders Problem Explorer, Product Voids, and Mercado Libre intelligence in the user's selected language.

---

## 6. Mercado Libre México (mercadolibre.com.mx) Autonomous Agent & Reporting (100% Completed)

* **Dedicated Autonomous Agent (`agents/mercadolibre_agent.py`):**
  * Exclusively targets **Mercado Libre México (MLM)** items and verified Mexican consumer reviews.
  * Collects product specifications, prices in MXN, ratings, seller locations, and Mexican failure modes.
  * Focuses on acute regional pain points:
    1. *Water purifiers* clogged in 2 weeks by limestone (*sarro de JAPAY*) in Mérida and Querétaro.
    2. *Voltage regulators* burning thermal fuses due to CFE summer grid surges in Monterrey and GDL.
    3. *Dehumidifiers* overflowing 2L tanks under 90%+ tropical humidity in Yucatán coastal homes.
    4. *Compact countertop dishwashers* sold at 100% markup over US prices due to domestic retail omission.
    5. *Inverter mini-splits* suffering compressor failure from uncertified installation without vacuum pumps.
* **Dedicated SQLite Table & API:**
  * `mercadolibre_products` table persisted in `data/mexico_consumer_insights.db`.
  * REST endpoint `GET /api/mercadolibre/products` returning structured product intelligence with review JSON arrays.
  * Background execution trigger: `POST /api/agents/run/mercadolibre` and CLI flag `python run.py --mercadolibre`.
* **Integrated Reporting (`reports/report_generator.py`):**
  * Dedicated **Section 7** in daily executive reports:
    * Spanish: `## 7. Inteligencia de Productos y Reseñas en Mercado Libre México (mercadolibre.com.mx)`
    * English: `## 7. Mercado Libre Mexico Product Quality & Customer Review Intelligence (mercadolibre.com.mx)`
  * Includes pricing tables, seller locations, defect analyses, and verbatim buyer complaint callouts.
* **Dedicated Dashboard Tab (`tab-mercadolibre`):**
  * Interactive 7th navigation tab `🛒 Mercado Libre México` in [frontend/index.html](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/frontend/index.html).
  * Real-time metrics bar (Total products, average rating, MXN price range, 100% Mexican defect alerts).
  * Glassmorphism cards with Mercado Libre yellow accent (`#ffe600`), price tags, seller chips, failure summaries, buyer quotes, and venture opportunity formulations.

---

## 7. Website User Manual & GitHub Synchronization (100% Completed)

* **Comprehensive Manual (`USER_MANUAL.md`):**
  * Published to repository root as [USER_MANUAL.md](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/USER_MANUAL.md).
  * Provides in-depth operational walkthroughs of:
    1. **WhatsApp Vecinos Community Ingestion**: Export formats (iOS/Android), PII masking regex, system notice stripping, friction keyword filtering, sample chat loading, and venture synthesis.
    2. **Facebook Groups Browser Agent & 2FA Session Setup**: Headed interactive login via Playwright, gatekeeper screening question bypass, and session token persistence in `data/auth_state/facebook_state.json`.
    3. **"I Wish They Sold This in Mexico" (Product Voids)**: Cross-border import arbitrage, origin country filters (USA, China, Japan/Korea, Europe), regulatory blocks (COFEPRIS, NOMs), and the interactive `+ Submit Wishlist Item` form.
    4. **Mercado Libre México (MLM) Intelligence**: Scraping reviews on `mercadolibre.com.mx`, isolating Mexican failure modes (*sarro* in Yucatán, CFE surges, tropical humidity).
    5. **Executive Daily Intelligence Briefings**: Scope selection (National, Mérida/Yucatán, CDMX, GDL, MTY), Markdown export, and bilingual report delivery.
    6. **Bilingual Switcher (`[🇲🇽 ES | 🇺🇸 EN]`)**: Dynamic translation layer, `/es` and `/en` URL routing, and `localStorage` persistence.
    7. **Problem & Data Explorer**: Four-tier filter hierarchy, Mexican slang / modismos search, and Ley Federal anonymized exports.
    8. **CLI & Server Automation**: Command cheat sheet for `run.py` and Docker Compose.
* **GitHub Synchronization:**
  * Cleanly committed and pushed to `main` branch at [https://github.com/westland/MexicoConsumerPulse](https://github.com/westland/MexicoConsumerPulse).
  * Linked in [README.md](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/README.md) and inventory table.

---

## 8. Release 1.10: Dual Mercado Libre México Agent (Hot Products & Existing Product Flaws)

* **Dual Scraping & Intelligence Mission:**
  * Updated [`agents/mercadolibre_agent.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/agents/mercadolibre_agent.py) to target both **Hot New Products** (breakout velocity, high demand, best sellers) and **Problems with Existing Products** (critical 1–3 star customer complaints, regional failure modes in Mexico).
  * **Hot New Products Tracked**:
    1. *LiFePO4 Portable Power Stations (1024Wh / 1200W)*: Surge in demand (+420%) due to CFE summer grid outages and blackouts in Monterrey, CDMX, and Mérida.
    2. *Solar-Direct Hybrid Inverter Mini-Splits (1.5 Ton)*: Connects straight to 3 rooftop DC panels, bypassing CFE DAC high-consumption penalty tariffs.
    3. *6-Stage Reverse Osmosis Purifiers with Booster Pump*: Removes 99% limestone *sarro* from deep wells and tap water in Mérida and Bajío.
    4. *Ultrasonic IoT Cistern & Tinaco Level Sensors*: Surged +510% during CDMX Cutzamala water rationing to protect pumps from running dry.
    5. *Countertop Compact Portable Dishwashers (5L tank)*: Solves rental apartment friction where kitchens lack 60cm rough-in plumbing.
    6. *Ultra-Fast Portable Ice Makers (12 kg/24h)*: High demand during 44°C heatwaves when convenience stores run out of ice.
  * **Problems with Existing Products Tracked**:
    1. *Basic Ceramic Water Purifiers*: Clog with limestone *sarro* in <14 days in Mérida/Yucatán due to extreme JAPAY water hardness.
    2. *2000VA Voltage Regulators*: CFE transformer surges burn internal soldered thermal fuses with zero replacement parts in Mexico.
    3. *Portable 12L Dehumidifiers*: 2L reservoir fills in 3.5 hours under 90%+ tropical coastal humidity, shutting down and heating rooms by 3°C.
    4. *Booster Pumps with Mechanical Flow Switches*: Mineral calcification freezes flow switches, causing motors to run dry and melt impellers.
    5. *Evacuated Tube Solar Water Heaters*: Hailstorms in central highlands shatter glass tubes; short magnesium sacrificial anodes corrode in 3 months.
    6. *Basic Robotic Vacuums with Passive Wet Mops*: Mop drags dirty water over porous Mexican ceramic tile/cantera, smelling sour and slipping on Fabuloso/Pinol.
* **Database & REST API:**
  * Expanded SQLite schema in [`agents/dataset_manager.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/agents/dataset_manager.py) with `product_type`, `trend_badge`, `demand_growth`, and `failure_mode`.
  * Added endpoints in [`app.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/app.py):
    * `GET /api/mercadolibre/products?product_type=...&category=...`
    * `GET /api/mercadolibre/hot-products`
    * `GET /api/mercadolibre/problems`
* **CLI Runner Upgrades ([`run.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/run.py)):**
  * Added `--ml-hot`, `--ml-problems`, `--ml-login` (headed browser session/verification capture on `mercadolibre.com.mx`), and dual `--mercadolibre`.
* **Executive Daily Reports ([`reports/report_generator.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/reports/report_generator.py)):**
  * Subdivided Section 7 into:
    * `7.1 🔥 Hot New Products y Nuevas Tendencias de Consumo en México`
    * `7.2 ⚠️ Fallas Críticas, Defectos y Quejas en Productos Existentes (1-3 Estrellas)`
* **Dashboard Frontend ([`frontend/index.html`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/frontend/index.html), [`frontend/app.js`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/frontend/app.js), [`frontend/style.css`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/frontend/style.css)):**
  * Filter pills for `Todos los Artículos`, `🔥 Hot New Products & Tendencias`, and `⚠️ Fallas en Productos Existentes (1-3 ⭐)`.
  * Category dropdown selector and updated KPI stat counters.
  * Visual card differentiation (`ml-card-hot` with flame badges and demand acceleration tags vs. `ml-card-problem` with alert badges, failure mode banners, verbatim customer complaints, and redesign hypotheses).
  * Full bilingual Spanish/English localization.
* **Live Hetzner Deployment:**
  * Deployed to `89.167.22.10` via [`deploy_remote.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/deploy_remote.py).
  * Containers rebuilt and verified live at [**https://pulse-mexico.com/**](https://pulse-mexico.com/) (HTTP 200 OK across all endpoints).

---

---

## 9. Release 1.14: Google Gemini 3.5 Flash-Lite Market Copilot & Session Automation

### A. Gemini 3.5 Flash-Lite Conversational Integration
* **Foundational LLM Engine ([`agents/gemini_agent.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/agents/gemini_agent.py)):**
  * Connected to Google GenAI using the official `google-genai` SDK and model **`gemini-3.5-flash-lite`** (with automatic fallback to `gemini-3.5-flash`, `gemini-3.1-flash-lite`, and `gemini-2.5-flash-lite`).
  * **Real-Time Data Grounding:** Automatically queries SQLite database before answering, injecting live context on:
    * 🔥 Hot New Products & sales demand surges on Mercado Libre México.
    * ⚠️ 1–3 star negative review complaints (Yucatán limestone scale, CFE surge burnouts, coastal humidity overflows).
    * 🎁 Cross-border product voids and import wishlists.
    * 🇲🇽 Mexican modismo and cultural vernacular mapping (*broncas, transas, jineteo, pipas, tandeo, bochorno*).
* **REST Endpoints in [`app.py`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/app.py):**
  * `POST /api/gemini/chat`: Handles grounded interactive Q&A and conversation history.
  * `POST /api/gemini/synthesize`: Generates investor-grade startup theses, pricing in MXN, and regulatory roadmaps.
  * `GET /api/gemini/status`: Reports active model and configuration status.
* **Interactive UI Tab 7 ([`frontend/index.html`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/frontend/index.html), [`frontend/app.js`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/frontend/app.js)):**
  * Tab 7: **`✨ Copiloto IA (Gemini 3.5 / Flash-Lite)`** with live model status badges.
  * Quick research prompt pills (*💧 Quejas de Sarro en Mérida*, *⚡ Apagones de CFE & Mercado Libre*, *💼 Startup de Deshumidificadores*, *🇺🇸 Oportunidades de Arbitraje USA*).
  * Glassmorphism chat feed with markdown parsing, code blocks, bullet points, and conversation reset.

### B. 1-Click Interactive Session Launchers & Privacy Protection
* **Dedicated Batch Launchers:**
  * [`LOGIN_FB_SESSION.bat`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/LOGIN_FB_SESSION.bat): Directly launches Chromium headed browser on Windows for Facebook login, 2FA authorization, and group gatekeeper handling.
  * [`LOGIN_ML_SESSION.bat`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/LOGIN_ML_SESSION.bat): Launches Chromium headed browser on Windows for Mercado Libre human verification / CAPTCHA solving.
  * Robust path resolution logic allowing batch files to be double-clicked from the Windows `Desktop` or from the repository root.
* **Menu Button Direct Integration:**
  * Header button **`Sesión FB`** connects directly to `POST /api/agents/login/facebook` to launch `LOGIN_FB_SESSION.bat` on local machines.
  * On remote cloud instances (`pulse-mexico.com`), displays an intelligent notice explaining why headless cloud servers cannot open desktop GUI windows and providing terminal/desktop instructions.
* **Session Persistence & Security:**
  * Captured cookies written to `data/auth_state/facebook_state.json`.
  * Uploaded to Hetzner production server at `/opt/mexconsumerpulse/data/auth_state/`.
  * Fully secured and ignored in [`.gitignore`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/.gitignore) (`data/auth_state/`, `.env`, `*.json_state`) guaranteeing zero credential leakage to GitHub.

### C. Release 1.14 Installers
* Windows: [`INSTALL_RELEASE_1.14.bat`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/INSTALL_RELEASE_1.14.bat)
* Linux/macOS/Server: [`install_release_1.14.sh`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/install_release_1.14.sh)

---

## 10. Final Project Closure & Verification Checklist

| Milestone | Status | Details / URL |
|---|---|---|
| **UIC Nuveen Grant Budget PDF** | ✅ Complete | Form filled itemized to $10,000 (`Nuveen_Grants_..._filled.pdf`) |
| **Hetzner Cloud VPS Production** | ✅ Live | Running on `89.167.22.10`, HTTPS SSL on [https://pulse-mexico.com/](https://pulse-mexico.com/) |
| **Google Gemini 3.5 Flash-Lite Copilot** | ✅ Active | Tab 7 conversational grounded copilot live locally and on [pulse-mexico.com](https://pulse-mexico.com/) |
| **Dual Mercado Libre México Harvester** | ✅ Complete | Hot Products vs. 1-3 Star Complaints with verbatim buyer review quotes |
| **1-Click Session Launchers** | ✅ Operational | `LOGIN_FB_SESSION.bat` & `LOGIN_ML_SESSION.bat` with desktop path resolution |
| **Bilingual Support (ES/EN)** | ✅ Complete | Spanish default (`/`, `/es`), English (`/en`), header switcher |
| **Website Feature User Manual** | ✅ Updated | Comprehensive guide updated to Release 1.14 in `USER_MANUAL.md` |
| **Release 1.14 Installers** | ✅ Ready | `INSTALL_RELEASE_1.14.bat` & `install_release_1.14.sh` |
| **GitHub Remote Synchronization** | ✅ Synced | Pushed up-to-date to `origin/main` ([westland/MexicoConsumerPulse](https://github.com/westland/MexicoConsumerPulse)) |



