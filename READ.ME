# MexicoConsumerPulse 🇲🇽 (Release 0.8)
### Autonomous Consumer Problem Intelligence & Multi-Agent Market Research Swarm

[![Release](https://img.shields.io/badge/Release-v0.8-blue.svg)](https://github.com/westland/MexicoConsumerPulse/releases)
[![Production](https://img.shields.io/badge/Live_Portal-pulse--mexico.com-green.svg)](https://pulse-mexico.com/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

An end-to-end multi-agent market research platform built to discover, scrape, sanitize, synthesize, and report on major daily consumer problems and service voids across Mexican cities (**Mérida & Yucatán, CDMX, Guadalajara, Monterrey, Puebla, Querétaro**) for both **Mexican Locals** and **Foreign Expats / Digital Nomads**.

* 🌐 **Live Cloud Production Portal:** [**https://pulse-mexico.com/**](https://pulse-mexico.com/)
* 📚 **API Swagger Documentation:** [**https://pulse-mexico.com/docs**](https://pulse-mexico.com/docs)
* 🐙 **GitHub Repository:** [**https://github.com/westland/MexicoConsumerPulse**](https://github.com/westland/MexicoConsumerPulse)

---

## ⚡ 1-Click Installation (Release 0.8)

### Windows
Double-click [**`INSTALL_RELEASE_0.8.bat`**](INSTALL_RELEASE_0.8.bat) or run:
```cmd
INSTALL_RELEASE_0.8.bat
```
* Automatically configures Python virtual environment (`venv`).
* Installs all requirements and headless Playwright Chromium.
* Verifies database schema, initial seed complaints, and launches the web dashboard.

### Linux / macOS / Server
Run the installer script:
```bash
chmod +x install_release_0.8.sh
./install_release_0.8.sh
```

### Docker Deployment
```bash
docker compose up -d --build
```
Runs `mexconsumerpulse_web` (dashboard) and `mexconsumerpulse_scheduler` (autonomous 24h scraper pipeline).

---

## 🏗️ Architecture & Component Overview

```
c:\Users\chris\Desktop\Market Research Mexico\
├── config.py                 # City colonias, subreddits, keywords, and Mexican slang lexicon
├── run.py                    # Master CLI orchestrator to run individual or all agents
├── scheduler.py              # Automated 24-hour daily scheduler loop
├── app.py                    # FastAPI server & REST API powering the live dashboard
├── deploy_hetzner.sh         # One-click automated installer for Hetzner Cloud Linux servers
├── Dockerfile                # Production Docker image with headless Playwright Chromium
├── docker-compose.yml        # Docker Compose configuration (Web UI + Daily Scheduler)
├── HETZNER_DEPLOYMENT_GUIDE.md # Complete Hetzner VPS setup manual
├── hetzner/                  # Production systemd services and Nginx SSL configuration
├── requirements.txt          # Python dependencies
│
├── agents/                   # Autonomous Agent Swarm
│   ├── base_agent.py         # Base agent interfaces
│   ├── reddit_agent.py       # Scrapes r/MexicoCity, r/Guadalajara, r/Monterrey, r/mexicoexpats
│   ├── twitter_agent.py      # Monitors @SATMX, @CFEmx, @SacmexCDMX, @Profeco, @AtencionCDMX
│   ├── facebook_agent.py     # Playwright agent for Vecinos & Bazar groups (with session cookies & 2FA support)
│   ├── compliance_agent.py   # Ley Federal de Protección de Datos Personales (Strips PII, RFC, CURP, phone, address)
│   ├── synthesis_agent.py    # Mexican slang NLP, urgency classification, and venture opportunity generator
│   └── dataset_manager.py    # SQLite database manager & automated CSV/JSON exporter
│
├── data/
│   ├── mexico_consumer_insights.db  # SQLite database storing raw posts, cleaned problems, and metrics
│   ├── auth_state/                  # Preserved browser session tokens (facebook_state.json)
│   └── exports/                     # Automated daily exports (CSV & JSON)
│       ├── mexico_consumer_problems_latest.csv
│       └── mexico_consumer_problems_latest.json
│
├── reports/
│   ├── report_generator.py   # Compiles daily bullet-pointed executive briefings
│   └── daily_reports/        # Persisted markdown reports (e.g., report_YYYY-MM-DD.md)
│
└── frontend/                 # Modern Executive Web Dashboard
    ├── index.html            # Responsive UI with KPIs, Daily Report, Explorer, and Console
    ├── style.css             # Glassmorphism dark-mode design system
    └── app.js                # Live API data binding, search filters, and agent controls
```

---

## 🚀 Quickstart Guide

### 1. View the Live Web Dashboard
The web dashboard is running locally on port **8000**:
```bash
http://127.0.0.1:8000
```
To launch or restart the dashboard at any time:
```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

### 2. Run the Autonomous Agent Swarm via CLI
To trigger an immediate data gathering and synthesis cycle across all agents:
```powershell
python run.py --all
```

Individual agent options:
```powershell
python run.py --reddit     # Scrapes target Mexican subreddits
python run.py --twitter    # Scrapes utility & gov complaint feeds
python run.py --facebook   # Runs Facebook Vecinos & Bazar groups browser agent
python run.py --report     # Generates a fresh daily bullet-pointed report
python run.py --export     # Exports current database to CSV & JSON
```

### 3. Facebook Groups 2FA & Session Setup (Human-in-the-Loop)
Because Facebook groups have strict gatekeeper questions (*"¿En qué calle vives?"*) and 2FA, use the headed login launcher:
```powershell
python run.py --fb-login
```
* **Step 1:** A Chromium browser window opens.
* **Step 2:** Log in to Facebook and complete your 2FA.
* **Step 3:** Answer any screening questions for your target neighborhood groups (*Vecinos de la Condesa, Bazar Coyoacán*, etc.).
* **Step 4:** The agent automatically saves your session to `data/auth_state/facebook_state.json`. Future automated runs will reuse this state without asking for credentials again.

### 4. Continuous Daily Automation (Scheduler)
To run the swarm automatically every 24 hours:
```powershell
python scheduler.py --interval-hours 24
```
You can also hook `python run.py --all` into Windows Task Scheduler or cron.

---

## 🛡️ Legal & Privacy Compliance (*Ley Federal*)
Mexico's **Ley Federal de Protección de Datos Personales en Posesión de los Particulares** is enforced by [`MexicanComplianceAgent`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/agents/compliance_agent.py). Every post gathered is sanitized before database storage:
- **Phone Numbers**: Mexican mobile numbers (`+52`, 10-digit formats) are redacted.
- **Tax IDs**: RFC and CURP identifiers are scrubbed.
- **Bank / Cards**: CLABE (18 digits) and payment card numbers are removed.
- **Addresses**: Exact street names and interior numbers (*e.g., Calle Durango #142*) are stripped.
- **Usernames**: Real author names are replaced with deterministic privacy hashes.

---

## 🧠 Mexican Slang & Modismos Classification
The [`MexicanSynthesisAgent`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/agents/synthesis_agent.py) translates Mexican cultural expressions into structured taxonomy:
- *"Se me fue la luz / transformador echó chispas"* ➔ Infrastructure (CFE Outage) • Severity 4/5
- *"No cae agua / tandeo seco / pipa turbia"* ➔ Infrastructure (Sacmex Crisis) • Severity 4-5/5
- *"Maestro albañil dejó la obra tirada / plomero transa"* ➔ Home Maintenance & Trades • Severity 4/5
- *"Citas del SAT vendidas en fila virtual"* ➔ Bureaucracy & GovTech • Severity 5/5
- *"Póliza jurídica abusiva / casero no regresa depósito"* ➔ Housing & Real Estate • Severity 4/5
- *"Expat opening bank account without RFC / fiador barrier"* ➔ Expat Friction • Severity 4/5

---

## 📊 Dataset Exports
The system maintains up-to-date flat file exports in [`data/exports/`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/data/exports):
- **CSV Format**: [`mexico_consumer_problems_latest.csv`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/data/exports/mexico_consumer_problems_latest.csv)
- **JSON Format**: [`mexico_consumer_problems_latest.json`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/data/exports/mexico_consumer_problems_latest.json)
- **Daily Markdown Reports**: [`reports/daily_reports/`](file:///c:/Users/chris/Desktop/Market%20Research%20Mexico/reports/daily_reports/)
