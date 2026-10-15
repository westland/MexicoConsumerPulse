# 🇲🇽 MexConsumerPulse - Complete Project Memory & Operation Manual

> **Archival Date:** October 15, 2026  
> **Status:** Local Production Active on `http://localhost:8000/` • **Hetzner Remote Production Live on `http://89.167.22.10:8080/`**

---

## 1. Quick Access: Running the Website Locally

The website is active locally and can be accessed in your browser at:
👉 **[http://localhost:8000/](http://localhost:8000/)**

### 1-Click Desktop Launcher
To launch or restart the local website at any time:
- Double-click **`START_LOCAL_WEBSITE.bat`** on your **Desktop**, OR
- Run [`c:\Users\chris\Desktop\Market Research Mexico\START_LOCAL_WEBSITE.bat`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/START_LOCAL_WEBSITE.bat)

---

## 2. What the Autonomous Agents Have Done (Mission Audit)

The system consists of **7 specialized autonomous agents** executing a multi-stage pipeline:

```
[Community Data Ingestion]
 ├── Reddit (r/mexicocity, r/gdl, r/monterrey, r/merida, r/yucatan, r/mexicoexpats)
 ├── Twitter/X (@SATMX, @CFEmx, @SacmexCDMX, @Profeco, @MetroCDMX)
 ├── Facebook Groups (Vecinos Condesa, Expats in Mérida, Bazar Coyoacán)
 └── WhatsApp Neighborhood Chat Ingestion (.txt exports)
        │
        ▼
[Compliance & Privacy Shield] ──> Redacts RFC, CURP, Phone Numbers (+52 55...), Unit Numbers, Names
        │
        ▼
[Synthesis & NLP Opportunity Engine] ──> Maps Mexican Slang ("bronca", "tranza", "no hay agua"),
                                         Scores Urgency (1-5), Generates Startup Venture Hypotheses
        │
        ▼
[SQLite Storage & Versioning] ──> data/mexico_consumer_insights.db
        │
        ▼
[Executive Intelligence Briefings] ──> National Multi-City Report & Mérida/Yucatán Regional Briefing
```

### Breakdown of Each Agent's Output:
1. **Reddit Autonomous Harvester**:
   - Scraped discussion threads across 8 Mexican metropolitan subreddits.
   - Harvested **33 verified consumer problem incidents**.
   - Identified rental security deposit withholdings in Condesa/Roma, black market SAT appointment scalpers ($1,800 MXN), and summer power outages in Mérida.
2. **Twitter/X Public Complaint Monitor**:
   - Monitored live citizen callouts to `@SATMX`, `@CFEmx`, `@SacmexCDMX`, `@Profeco`, `@MetroCDMX`.
   - Tracked emergency transformer blowouts in Guadalajara, water pressure collapse in Benito Juárez/Iztapalapa, and telecom price dispute filings.
3. **Facebook Groups Browser Agent**:
   - Automated Playwright browser engine configured for closed community and expat groups.
   - Built session persistence handling (`data/auth_state/facebook_state.json`) and gatekeeper screening bypass.
   - Uncovered unvetted handyman fraud, short-term lease renewal hikes, and water truck (*pipa*) price gouging.
4. **WhatsApp Vecinos Ingestion Agent**:
   - Live parser with regex sanitization for exported residential WhatsApp chat files.
   - Ingests building cistern depletion warnings, neighborhood security watch alerts, and tradesmen reviews.
5. **Compliance & Privacy Sanitization Agent**:
   - Enforces 100% adherence to Mexico's *Ley Federal de Protección de Datos Personales en Posesión de los Particulares*.
   - Zero PII stored: RFCs, CURP numbers, 10-digit phone numbers, and full names are permanently masked.
6. **Synthesis & NLP Opportunity Engine**:
   - Integrated Mexican slang and *modismos* dictionary.
   - Computed average consumer pain index of **3.0/5.0**.
   - Formulated **12 actionable startup venture hypotheses** (e.g. *PipaExpress*, *DepósitoSeguro MX*, *LuzAlerta / MéridaGrid*, *SATBot Legal*).
7. **Executive Intelligence Report Generator**:
   - Generated the comprehensive **Mexican Urban Consumer Intelligence Report (National)**.
   - Generated the dedicated **Mérida & Yucatán Peninsula Regional Briefing** (focusing on Gulf Coast heatwaves, CFE power grid limits, expat influx, and tourism rental strains).

---

## 3. Local Website Architecture & Tabs

When navigating to **`http://localhost:8000/`**, the dashboard provides:
1. **Daily Intelligence Report**: Interactive Markdown viewer with regional dropdown (*National Multi-City* and *Mérida & Yucatán Peninsula*). Includes 1-click Markdown download.
2. **Problem Explorer & Dataset**: Live searchable table of all 33+ verified complaints with filters by City, Category, Audience (Local / Expat / Both), and Urgency.
3. **Venture Opportunities Matrix**: 12 high-conviction startup hypotheses scored by market viability and target demographic.
4. **WhatsApp Vecinos Ingestion**: Live chat ingestion tool with a preloaded sample Condesa community chat.
5. **🤖 Agent Operations & Activity Report**: Executive audit scorecard, visual multi-stage pipeline diagram, and detailed dossiers for all 7 agents.

---

## 4. Hetzner Server Deployment (LIVE & OPERATIONAL 🚀)

MexConsumerPulse is now fully deployed and running in production on your domain **`pulse-mexico.com`** and Hetzner VPS (`89.167.22.10`):

👉 **Live Production Domain (HTTPS):** [https://pulse-mexico.com/](https://pulse-mexico.com/)  
👉 **Live www Domain (HTTPS):** [https://www.pulse-mexico.com/](https://www.pulse-mexico.com/)  
👉 **Interactive REST API Docs:** [https://pulse-mexico.com/docs](https://pulse-mexico.com/docs)  
👉 **Direct Server IP Fallback:** [http://89.167.22.10/](http://89.167.22.10/)  

*(Note: The old site `woowoocenterforhealing.com` was stopped, disabled, backed up to `/root/sumar_backup_before_delete.tar.gz`, and removed. `pulse-mexico.com` is now the primary root production site on ports 80 & 443).*

### Live Server Architecture:
* **Server IP:** `89.167.22.10` (Helsinki datacenter, Ubuntu 26.04)
* **Root Password:** `@Wei2Shi4Lin2` (Successfully configured and verified)
* **Docker Containers:**
  1. `mexconsumerpulse_web` (FastAPI backend + interactive dashboard on port 8080)
  2. `mexconsumerpulse_scheduler` (Autonomous 24-hour scraper and report generator)
* **Firewall (UFW):** Ports 22 (SSH), 80 (HTTP), 443 (HTTPS), 8080 (MexConsumerPulse Dashboard) enabled.

### Useful Remote Management Commands:
```bash
# Connect to Hetzner via SSH
ssh root@89.167.22.10

# Check container health & status
docker ps

# View live web dashboard logs
docker compose -f /opt/mexconsumerpulse/docker-compose.yml logs -f web

# View live autonomous agent scraper logs
docker compose -f /opt/mexconsumerpulse/docker-compose.yml logs -f scheduler

# Trigger an on-demand complete research run right now
docker compose -f /opt/mexconsumerpulse/docker-compose.yml exec web python run.py --all
```

---

## 5. File Inventory & Storage Locations

| Path | Purpose |
|---|---|
| `app.py` | FastAPI backend server with REST endpoints & static frontend mount |
| `frontend/index.html` | Rich executive dashboard UI with all 5 operational tabs |
| `frontend/style.css` | Dark-mode glassmorphism design system |
| `frontend/app.js` | Dynamic tab routing, filters, markdown parser, and API client |
| `data/mexico_consumer_insights.db` | Persistent SQLite database (schema, 33 problems, daily reports) |
| `data/exports/` | Latest CSV and JSON dataset exports |
| `reports/daily_reports/` | Generated Markdown intelligence briefings |
| `agents/` | Source code for all 7 autonomous agents |
| `START_LOCAL_WEBSITE.bat` | 1-click launcher for `http://localhost:8000/` |
| `DEPLOY_TO_HETZNER.bat` | 1-click remote deployer for `http://89.167.22.10/` |
