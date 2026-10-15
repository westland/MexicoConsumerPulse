# 🇲🇽 MexConsumerPulse & Nuveen Grant - Master Project Memory & Operation Manual

> **Archival Date:** October 15, 2026  
> **Status:** Release 1.00 Production Live on [**https://pulse-mexico.com/**](https://pulse-mexico.com/) • Local Dashboard on `http://localhost:8000/` • GitHub Repo & Release 1.00 at [**https://github.com/westland/MexicoConsumerPulse**](https://github.com/westland/MexicoConsumerPulse)

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
| `Nuveen_Grants_..._filled.pdf` | Completed UIC Nuveen grant budget application form |
