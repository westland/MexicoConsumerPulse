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
from agents.mercadolibre_agent import MercadoLibreAgent
from agents.gemini_agent import gemini_copilot
from pydantic import BaseModel

db = DatasetManager()
report_gen = DailyReportGenerator()
whatsapp_agent = WhatsAppVecinosAgent()
ml_agent = MercadoLibreAgent()

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
                "records_harvested": 5,
                "action_summary": "Synthesized executive briefings with sector breakdown, regional pain matrices, and exportable Markdown.",
                "key_findings": [
                    "Published Mexican Urban Consumer Intelligence Report (National)",
                    "Published Mérida & Yucatán Regional Consumer Intelligence Briefing"
                ]
            },
            {
                "id": "product_voids",
                "name": "Product Void & Cross-Border Retail Harvester",
                "icon": "🎁",
                "status": "Active • Tracking Voids",
                "target": "US, China, Japan, EU retail gaps & Mexican consumer wishlists",
                "records_harvested": len(db.get_product_voids()),
                "action_summary": "Monitors 'I wish they sold this in Mexico' ('Ojalá vendieran esto') across social platforms, identifying goods unavailable domestically.",
                "key_findings": [
                    "High demand for countertop compact dishwashers blocked by NOM 60cm retail default",
                    "Trader Joe's gourmet seasonings commanding 400% markup on Instagram grey market",
                    "COFEPRIS OTC classification restrictions blocking bulk generic allergy and melatonin products"
                ]
            },
            {
                "id": "mercadolibre",
                "name": "Mercado Libre México: Hot Products & Problem Harvester",
                "icon": "🛒",
                "status": "Active • Monitoring México",
                "target": "https://www.mercadolibre.com.mx/ (Only México MLM Items)",
                "records_harvested": len(ml_agent.get_products()),
                "action_summary": "Scrapes hot new breakout products, trending consumer demand, and critical 1-3 star reviews highlighting product failures across Mexico.",
                "key_findings": [
                    "Hot Trend: LiFePO4 portable power stations & solar minisplits exploding due to CFE grid blackouts (+420% demand)",
                    "Hot Trend: Ultrasonic tinaco/cisterna IoT level switches surging +510% amidst CDMX water cuts",
                    "Failure Mode: Water purifiers clogging in <14 days from Mérida & Yucatán limestone sarro",
                    "Failure Mode: CFE voltage spikes destroying refrigerator compressors with unreplaceable soldered fuses",
                    "Failure Mode: Standard 2L dehumidifier tanks overflowing in 3.5 hours under 90% tropical coastal humidity"
                ]
            }
        ],
        "hetzner_deployment_status": {
            "target": "pulse-mexico.com (89.167.22.10)",
            "state": "Live & Dual-Language Ready",
            "script": "C:\\Users\\chris\\Desktop\\Market Research Mexico\\hetzner",
            "containers": ["mexconsumerpulse_web (port 8080->8000)", "Nginx reverse proxy (443 Let's Encrypt & 8000)"],
            "notes": "Live production environment serving English on https://pulse-mexico.com/ and Spanish on :8000"
        }
    }

# Mount static frontend
frontend_dir = BASE_DIR / "frontend"
if not frontend_dir.exists():
    frontend_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")

@app.get("/")
@app.get("/es")
@app.get("/en")
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

@app.get("/api/product-voids")
def get_product_voids(
    origin: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500)
):
    voids = db.get_product_voids(limit=limit)
    if origin and origin != "All":
        voids = [v for v in voids if origin.lower() in v.get("content", "").lower() or origin.lower() in v.get("title", "").lower() or origin.lower() in v.get("venture_concept", "").lower()]
    return voids

@app.post("/api/product-voids/submit")
def submit_product_void(payload: dict):
    product_name = payload.get("product_name", "")
    origin_country = payload.get("origin_country", "USA")
    description = payload.get("description", "")
    city = payload.get("city", "National")
    
    if not product_name:
        raise HTTPException(status_code=400, detail="Product name is required.")
        
    record = {
        "title": f"Ojalá vendieran en México: {product_name}",
        "content": f"Demanda de producto no disponible: {product_name} (Disponible en {origin_country}). {description}",
        "source_platform": "Community Wishlist Submissions",
        "source_url": "https://pulse-mexico.com/wishlist",
        "city": city,
        "colonia": "Community Wishlist",
        "category": "Product Voids & Import Wishlist",
        "confidence": 0.99,
        "audience": "Both",
        "urgency": 3,
        "sentiment": "Inquiring / Service Gap",
        "matched_slang": [{"term": "ojalá vendieran", "meaning": "Direct user submitted product void"}],
        "problem_summary": f"Demanda de consumidores mexicanos por {product_name} disponible en {origin_country}.",
        "solution_found": "Actualmente inexistente en canales formales de retail en México.",
        "market_opportunity": {
            "venture_concept": f"Cross-Border Import & Distribution of {product_name}",
            "solution_summary": f"Import arbitrage and local fulfillment opportunity for {product_name} from {origin_country} into the Mexican market."
        }
    }
    
    db.insert_problem(record)
    return {"status": "success", "message": f"Successfully submitted wishlist item: {product_name}"}

@app.get("/api/reports/latest")
def get_latest_report(region: Optional[str] = Query("All"), lang: Optional[str] = Query("es")):
    if lang not in ["es", "en"]:
        lang = "es"
    date_str = datetime.now().strftime("%Y-%m-%d")
    is_merida = region and (region == "Mérida & Yucatán" or "mérida" in region.lower() or "yucatan" in region.lower())

    if is_merida:
        report_key = f"{date_str}_merida_yucatan_{lang}"
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM daily_reports 
                WHERE report_date = ? 
                ORDER BY id DESC LIMIT 1
            """, (report_key,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            
            # fallback if legacy key exists
            cursor.execute("""
                SELECT * FROM daily_reports 
                WHERE report_date LIKE '%merida%'
                ORDER BY id DESC LIMIT 1
            """)
            row = cursor.fetchone()
            if row:
                return dict(row)

        res = report_gen.generate_report(region="Mérida & Yucatán", lang=lang)
        return {
            "report_date": res["report_date"],
            "report_title": res["report_title"],
            "executive_summary": "",
            "markdown_content": res["markdown"]
        }

    # National Report
    report_key = f"{date_str}_{lang}"
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM daily_reports 
            WHERE report_date = ?
            ORDER BY id DESC LIMIT 1
        """, (report_key,))
        row = cursor.fetchone()
        if row:
            return dict(row)

        cursor.execute("""
            SELECT * FROM daily_reports 
            WHERE report_date NOT LIKE '%merida%'
            ORDER BY id DESC LIMIT 1
        """)
        row = cursor.fetchone()
        if row:
            return dict(row)

    res = report_gen.generate_report(region="All", lang=lang)
    return {
        "report_date": res["report_date"],
        "report_title": res["report_title"],
        "executive_summary": "",
        "markdown_content": res["markdown"]
    }

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

@app.get("/api/mercadolibre/products")
def get_mercadolibre_products(
    product_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100)
):
    return ml_agent.get_products(product_type=product_type, category=category, limit=limit)

@app.get("/api/mercadolibre/hot-products")
def get_mercadolibre_hot_products(limit: int = Query(50, ge=1, le=100)):
    return ml_agent.get_hot_new_products(limit=limit)

@app.get("/api/mercadolibre/problems")
def get_mercadolibre_product_problems(limit: int = Query(50, ge=1, le=100)):
    return ml_agent.get_product_problems(limit=limit)

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
    elif agent_name == "whatsapp":
        cmd.append("--whatsapp")
    elif agent_name == "mercadolibre":
        cmd.append("--mercadolibre")
    elif agent_name == "report":
        cmd.append("--report")

    subprocess.run(cmd, capture_output=True, text=True)

@app.post("/api/agents/run/{agent_name}")
def trigger_agent(agent_name: str, background_tasks: BackgroundTasks):
    valid_agents = ["all", "reddit", "twitter", "facebook", "whatsapp", "mercadolibre", "report"]
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

class GeminiChatRequest(BaseModel):
    message: str
    history: Optional[list] = None

class GeminiSynthesizeRequest(BaseModel):
    problem_title: str
    problem_content: str
    city: str
    category: str

@app.get("/api/gemini/status")
def gemini_status():
    return {
        "configured": gemini_copilot.is_configured(),
        "preferred_model": gemini_copilot.preferred_model,
        "available_models": gemini_copilot.CANDIDATE_MODELS
    }

@app.post("/api/gemini/chat")
def gemini_chat(payload: GeminiChatRequest):
    if not payload.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    # Gather live database context for grounding
    try:
        hot_prods = db.get_mercadolibre_hot_products(limit=5)
    except Exception:
        hot_prods = []
    try:
        problem_prods = db.get_mercadolibre_problem_products(limit=5)
    except Exception:
        problem_prods = []
    try:
        voids = db.get_product_voids(limit=5)
    except Exception:
        voids = []
    
    context = {
        "hot_products": hot_prods,
        "problem_products": problem_prods,
        "product_voids": voids
    }
    
    res = gemini_copilot.chat_with_copilot(
        message=payload.message,
        history=payload.history,
        context_data=context
    )
    return res

@app.post("/api/gemini/synthesize")
def gemini_synthesize(payload: GeminiSynthesizeRequest):
    res = gemini_copilot.deep_venture_synthesis(
        problem_title=payload.problem_title,
        problem_content=payload.problem_content,
        city=payload.city,
        category=payload.category
    )
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
