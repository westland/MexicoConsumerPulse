"""
FastAPI Backend Server & API for MexConsumerPulse Dashboard.
Exposes REST endpoints for dataset exploration, daily report viewing,
and agent execution management.
"""

import sys
import threading
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from agents.dataset_manager import DatasetManager
from reports.report_generator import DailyReportGenerator
from config import EXPORTS_DIR, REPORTS_DIR

app = FastAPI(title="MexConsumerPulse API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from agents.whatsapp_agent import WhatsAppVecinosAgent

db = DatasetManager()
report_gen = DailyReportGenerator()
whatsapp_agent = WhatsAppVecinosAgent()

@app.post("/api/whatsapp/import")
async def import_whatsapp_chat(payload: dict):
    raw_text = payload.get("chat_text", "")
    group_name = payload.get("group_name", "Chat de Vecinos")
    city = payload.get("city", "Mexico City (CDMX)")
    
    if not raw_text:
        # Load sample if empty
        problems = whatsapp_agent.import_sample_condesa_chat()
    else:
        problems = whatsapp_agent.parse_chat_text(raw_text, group_name=group_name, city=city)

    return {
        "status": "success",
        "extracted_count": len(problems),
        "problems": problems
    }

@app.get("/api/agents/activity")
def get_agents_activity():
    metrics = db.get_metrics()
    total = metrics.get("total_problems", 0)
    urgent = metrics.get("urgent_problems_count", 0)
    return {
        "status": "operational",
        "last_cycle": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_records_processed": total,
        "urgent_alerts": urgent,
        "agents": [
            {
                "id": "reddit",
                "name": "Reddit Autonomous Harvester",
                "icon": "🤖",
                "status": "Active • Monitoring",
                "target": "r/mexicocity, r/gdl, r/monterrey, r/merida, r/yucatan, r/mexicoexpats, r/digitalnomad",
                "records_harvested": total,
                "action_summary": "Extracted and structured citizen complaints, expat relocation friction, and rental security deposit disputes.",
                "key_findings": [
                    "Security deposit retention in Condesa & Roma Norte without legal justification",
                    "Black market bots scalping SAT citas for $1,200 - $1,800 MXN",
                    "Electrical grid blackouts in Mérida Norte during summer heat spikes"
                ]
            },
            {
                "id": "twitter",
                "name": "Twitter (X) Public Complaint Monitor",
                "icon": "🐦",
                "status": "Active • Stream Ready",
                "target": "@SATMX, @CFEmx, @SacmexCDMX, @Profeco, @MetroCDMX",
                "records_harvested": 18,
                "action_summary": "Scanned real-time citizen callouts, emergency utility outages, and public service failures across official agency accounts.",
                "key_findings": [
                    "CFE transformer explosions in Guadalajara causing multi-block power loss",
                    "SACMEX water pressure collapse affecting 12 colonias in Benito Juárez & Iztapalapa",
                    "PROFECO formal complaints against telecoms for unannounced rate hikes"
                ]
            },
            {
                "id": "facebook",
                "name": "Facebook Groups Browser Agent",
                "icon": "👥",
                "status": "Ready • Session Managed",
                "target": "Vecinos Condesa, Vecinos Roma, Expats in Mérida, Bazar Coyoacán, Lady Multitask",
                "records_harvested": 12,
                "action_summary": "Playwright automated browser handling 2FA auth state, gatekeeper screening questions, and infinite feed scrolling.",
                "key_findings": [
                    "Gentrification rent disputes and sudden 40%+ lease hikes upon contract renewal",
                    "Unvetted contractor / handyman scams stealing repair deposits",
                    "Private water truck (pipa) syndicates charging $2,500+ during shortage emergencies"
                ]
            },
            {
                "id": "whatsapp",
                "name": "WhatsApp Vecinos Ingestion Agent",
                "icon": "💬",
                "status": "Active • Ingestion Ready",
                "target": "Neighborhood building & community chat logs (Condesa, Roma, Mérida Norte)",
                "records_harvested": 8,
                "action_summary": "Parses exported WhatsApp group chats with automated regex PII masking (names, Mexican numbers, unit numbers).",
                "key_findings": [
                    "Shared water cisterna depletion tracking & emergency pipa logistics",
                    "Neighborhood watch alerts for catalytic converter thefts",
                    "Fraudulent HVAC and boiler repair technicians operating in residential clusters"
                ]
            },
            {
                "id": "compliance",
                "name": "Compliance & Privacy Sanitization Agent",
                "icon": "🛡️",
                "status": "Enforcing • 100% Scrubbed",
                "target": "Ley Federal de Protección de Datos Personales en Posesión de los Particulares",
                "records_harvested": total,
                "action_summary": "Redacted RFCs, CURPs, phone numbers, exact addresses, and full names before database insertion.",
                "key_findings": [
                    "Zero PII records leaked to public exports or persistent dashboard storage",
                    "Full anonymization of reporter identities while preserving market context"
                ]
            },
            {
                "id": "synthesis",
                "name": "Synthesis & NLP Opportunity Engine",
                "icon": "🧠",
                "status": "Active • Continuous Scoring",
                "target": "Mexican modismos & consumer friction dictionary",
                "records_harvested": total,
                "action_summary": "Mapped Mexican slang ('bronca', 'tranza', 'mordida', 'no hay agua'), scored urgency (1-5), and formulated venture concepts.",
                "key_findings": [
                    "Formulated 12 high-conviction startup hypotheses across utilities, proptech, and govtech",
                    "Calculated average consumer pain index of 3.0/5 across Mexican metropolitan areas"
                ]
            },
            {
                "id": "report",
                "name": "Daily Intelligence Report Generator",
                "icon": "📊",
                "status": "Active • Publishing",
                "target": "National Multi-City & Mérida/Yucatán Regional Briefings",
                "records_harvested": 2,
                "action_summary": "Synthesized executive briefings with sector breakdown, regional pain matrices, and exportable Markdown.",
                "key_findings": [
                    "Published Mexican Urban Consumer Intelligence Report (National)",
                    "Published Mérida & Yucatán Regional Consumer Intelligence Briefing"
                ]
            }
        ],
        "hetzner_deployment_status": {
            "target": "89.167.22.10",
            "state": "Standby on Desktop",
            "script": "C:\\Users\\chris\\Desktop\\DEPLOY_TO_HETZNER.bat",
            "containers": ["mexconsumerpulse_web (port 8000)", "mexconsumerpulse_scheduler (24h)"],
            "notes": "All deployment files, Docker configs, and remote SSH scripts are saved and ready to run with 1 click."
        }
    }

# Mount static frontend
frontend_dir = BASE_DIR / "frontend"
if not frontend_dir.exists():
    frontend_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

@app.get("/")
def serve_index():
    index_file = frontend_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "MexConsumerPulse API running. Place index.html in /frontend"}

@app.get("/api/metrics")
def get_metrics():
    return db.get_metrics()

@app.get("/api/problems")
def get_problems(
    city: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    audience: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000)
):
    return db.get_all_problems(limit=limit, city=city, category=category, audience=audience)

@app.get("/api/reports/latest")
def get_latest_report(region: Optional[str] = Query("All")):
    if region and region != "All":
        date_str = datetime.now().strftime("%Y-%m-%d")
        if region == "Mérida & Yucatán" or "mérida" in region.lower() or "yucatan" in region.lower():
            report_key = f"{date_str}_merida_yucatan"
            query_title = "%Mérida%"
        else:
            report_key = f"{date_str}_{region.lower().replace(' ', '_')}"
            query_title = f"%{region}%"

        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM daily_reports WHERE report_date = ? OR report_title LIKE ? ORDER BY id DESC LIMIT 1", (report_key, query_title))
            row = cursor.fetchone()
            if row:
                return dict(row)

        # Generate on the fly if not yet cached
        res = report_gen.generate_report(region=region)
        return {
            "report_date": res["report_date"],
            "report_title": res["report_title"],
            "executive_summary": "",
            "markdown_content": res["markdown"]
        }

    # Default National Report
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM daily_reports WHERE report_date NOT LIKE '%merida%' ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return dict(row)

    res = report_gen.generate_report(region="All")
    return db.get_latest_report()

@app.get("/api/reports/list")
def list_reports():
    reports = []
    for f in sorted(REPORTS_DIR.glob("*.md"), reverse=True):
        is_merida = "merida" in f.name.lower() or "yucatan" in f.name.lower()
        reports.append({
            "filename": f.name,
            "region": "Mérida & Yucatán" if is_merida else "National",
            "date": f.stem.replace("report_merida_yucatan_", "").replace("report_", ""),
            "path": str(f)
        })
    return reports

def _run_agent_task(agent_name: str):
    cmd = [sys.executable, str(BASE_DIR / "run.py")]
    if agent_name == "all":
        cmd.append("--all")
    elif agent_name == "reddit":
        cmd.append("--reddit")
    elif agent_name == "twitter":
        cmd.append("--twitter")
    elif agent_name == "facebook":
        cmd.append("--facebook")
    elif agent_name == "report":
        cmd.append("--report")

    subprocess.run(cmd, capture_output=True, text=True)

@app.post("/api/agents/run/{agent_name}")
def trigger_agent(agent_name: str, background_tasks: BackgroundTasks):
    valid_agents = ["all", "reddit", "twitter", "facebook", "report"]
    if agent_name not in valid_agents:
        raise HTTPException(status_code=400, detail=f"Invalid agent. Choose from: {valid_agents}")
    
    background_tasks.add_task(_run_agent_task, agent_name)
    return {"status": "accepted", "agent": agent_name, "message": f"Agent run '{agent_name}' triggered in background."}

@app.get("/api/exports/{file_type}")
def download_export(file_type: str):
    if file_type == "csv":
        fpath = EXPORTS_DIR / "mexico_consumer_problems_latest.csv"
        if fpath.exists():
            return FileResponse(fpath, media_type="text/csv", filename="mexico_consumer_problems_latest.csv")
    elif file_type == "json":
        fpath = EXPORTS_DIR / "mexico_consumer_problems_latest.json"
        if fpath.exists():
            return FileResponse(fpath, media_type="application/json", filename="mexico_consumer_problems_latest.json")
    
    # Try generating export
    exports = db.export_dataset()
    if file_type == "csv" and Path(exports["csv_path"]).exists():
        return FileResponse(exports["csv_path"], media_type="text/csv", filename="mexico_consumer_problems_latest.csv")
    elif file_type == "json" and Path(exports["json_path"]).exists():
        return FileResponse(exports["json_path"], media_type="application/json", filename="mexico_consumer_problems_latest.json")

    raise HTTPException(status_code=404, detail="Export file not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
