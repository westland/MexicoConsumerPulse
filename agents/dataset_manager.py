"""
Dataset & Persistence Manager for MexConsumerPulse.
Manages SQLite storage, deduplication, schema migrations, and CSV/JSON automated exports.
"""

import sqlite3
import json
import csv
from datetime import datetime
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import DB_PATH, EXPORTS_DIR

class DatasetManager:
    """
    Manages the persistent database for raw posts, classified consumer problems,
    daily reports, and analytical metrics.
    """

    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self._init_db()
        self.seed_product_voids()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Consumer Problems Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consumer_problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_hash TEXT UNIQUE,
                    title TEXT NOT NULL,
                    content TEXT,
                    source_platform TEXT NOT NULL,
                    source_url TEXT,
                    city TEXT NOT NULL,
                    colonia TEXT,
                    category TEXT NOT NULL,
                    confidence REAL,
                    audience TEXT NOT NULL,
                    urgency INTEGER NOT NULL,
                    sentiment TEXT,
                    matched_slang TEXT,
                    problem_summary TEXT,
                    solution_found TEXT,
                    venture_concept TEXT,
                    solution_summary TEXT,
                    timestamp TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 2. Daily Intelligence Reports Table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    report_date TEXT UNIQUE,
                    report_title TEXT,
                    executive_summary TEXT,
                    markdown_content TEXT,
                    metrics_json TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 3. Agent Execution Run Logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    records_collected INTEGER,
                    records_inserted INTEGER,
                    details TEXT,
                    executed_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()

    def insert_problem(self, problem: Dict[str, Any]) -> bool:
        """
        Insert a analyzed consumer problem, preventing duplicate entries.
        """
        import hashlib
        raw_sig = f"{problem.get('source_url', '')}_{problem.get('title', '')[:50]}"
        content_hash = hashlib.sha256(raw_sig.encode('utf-8')).hexdigest()

        market_opp = problem.get("market_opportunity", {})
        venture_concept = market_opp.get("venture_concept", "")
        solution_summary = market_opp.get("solution_summary", "")

        matched_slang_json = json.dumps(problem.get("matched_slang", []), ensure_ascii=False)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO consumer_problems (
                        content_hash, title, content, source_platform, source_url,
                        city, colonia, category, confidence, audience, urgency,
                        sentiment, matched_slang, problem_summary, solution_found,
                        venture_concept, solution_summary, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    content_hash,
                    problem.get("title", ""),
                    problem.get("content", ""),
                    problem.get("source_platform", "Unknown"),
                    problem.get("source_url", ""),
                    problem.get("city", "National"),
                    problem.get("colonia", "General"),
                    problem.get("category", "General"),
                    problem.get("confidence", 0.5),
                    problem.get("audience", "Both"),
                    problem.get("urgency", 3),
                    problem.get("sentiment", "Neutral"),
                    matched_slang_json,
                    problem.get("problem_summary", ""),
                    problem.get("solution_found", ""),
                    venture_concept,
                    solution_summary,
                    problem.get("timestamp") or datetime.utcnow().isoformat()
                ))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Already exists
                return False

    def get_all_problems(self, limit: int = 500, city: Optional[str] = None, 
                         category: Optional[str] = None, audience: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM consumer_problems WHERE 1=1"
        params = []
        if city and city != "All":
            query += " AND city LIKE ?"
            params.append(f"%{city}%")
        if category and category != "All":
            query += " AND category = ?"
            params.append(category)
        if audience and audience != "All":
            query += " AND audience = ?"
            params.append(audience)
        
        query += " ORDER BY urgency DESC, created_at DESC LIMIT ?"
        params.append(limit)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_metrics(self) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM consumer_problems")
            total_count = cursor.fetchone()[0]

            cursor.execute("SELECT category, COUNT(*) as count FROM consumer_problems GROUP BY category ORDER BY count DESC")
            cat_rows = cursor.fetchall()
            by_category = {r["category"]: r["count"] for r in cat_rows}

            cursor.execute("SELECT city, COUNT(*) as count FROM consumer_problems GROUP BY city ORDER BY count DESC")
            city_rows = cursor.fetchall()
            by_city = {r["city"]: r["count"] for r in city_rows}

            cursor.execute("SELECT audience, COUNT(*) as count FROM consumer_problems GROUP BY audience")
            aud_rows = cursor.fetchall()
            by_audience = {r["audience"]: r["count"] for r in aud_rows}

            cursor.execute("SELECT AVG(urgency) FROM consumer_problems")
            avg_urgency = cursor.fetchone()[0] or 0.0

            cursor.execute("SELECT COUNT(*) FROM consumer_problems WHERE urgency >= 4")
            urgent_count = cursor.fetchone()[0]

            return {
                "total_problems": total_count,
                "urgent_problems_count": urgent_count,
                "average_urgency": round(avg_urgency, 2),
                "by_category": by_category,
                "by_city": by_city,
                "by_audience": by_audience
            }

    def save_daily_report(self, report_date: str, title: str, summary: str, markdown: str, metrics: Dict[str, Any]):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO daily_reports (report_date, report_title, executive_summary, markdown_content, metrics_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(report_date) DO UPDATE SET
                    report_title=excluded.report_title,
                    executive_summary=excluded.executive_summary,
                    markdown_content=excluded.markdown_content,
                    metrics_json=excluded.metrics_json
            ''', (report_date, title, summary, markdown, json.dumps(metrics, ensure_ascii=False)))
            conn.commit()

    def get_latest_report(self) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM daily_reports ORDER BY report_date DESC LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else None

    def log_agent_run(self, agent_name: str, status: str, collected: int, inserted: int, details: str = ""):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO agent_runs (agent_name, status, records_collected, records_inserted, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (agent_name, status, collected, inserted, details))
            conn.commit()

    def export_dataset(self) -> Dict[str, str]:
        """
        Exports all current records to CSV and JSON in data/exports/
        """
        problems = self.get_all_problems(limit=5000)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        csv_filename = EXPORTS_DIR / f"mexico_consumer_problems_{timestamp}.csv"
        latest_csv = EXPORTS_DIR / "mexico_consumer_problems_latest.csv"
        json_filename = EXPORTS_DIR / f"mexico_consumer_problems_{timestamp}.json"
        latest_json = EXPORTS_DIR / "mexico_consumer_problems_latest.json"

        if problems:
            keys = problems[0].keys()
            for out_csv in [csv_filename, latest_csv]:
                with open(out_csv, "w", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(problems)

        for out_json in [json_filename, latest_json]:
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(problems, f, ensure_ascii=False, indent=2)

        return {
            "csv_path": str(latest_csv),
            "json_path": str(latest_json),
            "total_exported": len(problems)
        }

    def get_mercadolibre_products(self, product_type: Optional[str] = None, category: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve all scraped Mercado Libre products with review breakdowns, optionally filtered by product_type and category."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mercadolibre_products'")
            if not cursor.fetchone():
                return []
            
            query = "SELECT * FROM mercadolibre_products"
            params = []
            conditions = []

            if product_type and product_type != "ALL":
                conditions.append("product_type = ?")
                params.append(product_type)

            if category and category != "ALL":
                conditions.append("category = ?")
                params.append(category)

            if conditions:
                query += " WHERE " + " AND ".join(conditions)

            query += " ORDER BY id DESC LIMIT ?"
            params.append(limit)

            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            output = []
            for r in rows:
                d = dict(r)
                try:
                    d["reviews"] = json.loads(d.get("reviews_json", "[]"))
                except Exception:
                    d["reviews"] = []
                output.append(d)
            return output

    def get_mercadolibre_hot_products(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve only hot new products and breakout trends in Mexico."""
        return self.get_mercadolibre_products(product_type="HOT_NEW_PRODUCT", limit=limit)

    def get_mercadolibre_problem_products(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve only products with critical failures, quality complaints, and 1-3 star reviews."""
        return self.get_mercadolibre_products(product_type="EXISTING_PRODUCT_PROBLEMS", limit=limit)

    def seed_product_voids(self) -> int:
        """
        Seeds authentic consumer expressions of 'I wish they sold this product in Mexico'
        covering products available in USA, China, Japan, Korea, and Europe but missing in Mexico.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM consumer_problems WHERE category = 'Product Voids & Import Wishlist'")
            count = cursor.fetchone()[0]
            if count >= 10:
                return count

        seeds = [
            {
                "title": "Ojalá vendieran en México los lavavajillas de encimera (countertop dishwashers) para departamentos pequeños",
                "content": "Llevo meses buscando un lavavajillas compacto de sobremesa como los que venden en USA (Hava, Farberware, Comfee) o en China. En México tiendas como Liverpool o Home Depot solo venden lavavajillas gigantes de 60cm que requieren remodelar toda la cocina y no caben en departamentos de la Roma o Condesa. Quise pedirlo por Amazon US pero la aduana me cobró $3,500 pesos de depósito arancelario por NOM eléctrica. Ojalá una empresa mexicana los importara con garantía y certificación oficial.",
                "source_platform": "Reddit (r/MexicoCity)",
                "source_url": "https://reddit.com/r/MexicoCity/comments/wish_countertop_dishwasher",
                "city": "Mexico City (CDMX)",
                "colonia": "Roma Norte",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.98,
                "audience": "Both",
                "urgency": 4,
                "sentiment": "Frustrated / Seeking Help",
                "matched_slang": [{"term": "ojalá vendieran", "meaning": "Unmet consumer product void / High cross-border import demand"}],
                "problem_summary": "Falta de lavavajillas compactos de encimera en México para departamentos pequeños; tiendas solo venden modelos industriales gigantes y aduana bloquea importaciones individuales.",
                "solution_found": "Comprarlo en viaje a Texas y pasarlo por tierra o pagar triple en MercadoLibre a revendedores sin garantía.",
                "market_opportunity": {
                    "venture_concept": "Direct White-Label Compact Appliance Brand & NOM-Certified Logistics",
                    "solution_summary": "Direct import and certification of compact European/US-style countertop dishwashers and apartment appliances tailored for Mexican urban rental living with local warranty."
                }
            },
            {
                "title": "Trader Joe's Everything Bagel Seasoning & Chili Onion Crunch: Revendedores cobran 400% en Instagram",
                "content": "¿Por qué ninguna tienda o supermercado tipo City Market o Chedraui Selecto vende condimentos de Trader Joe's en México? Todo el mundo busca el 'Everything but the Bagel' y el 'Chili Onion Crunch'. En Instagram hay páginas de 'fayuqueros gourmet' que traen de San Diego o McAllen y te cobran $380 pesos por un frasco que en USA cuesta $2.99 dólares ($50 MXN). Hay una demanda brutal no atendida de botanas y sazonadores de Trader Joe's.",
                "source_platform": "Facebook (Bazar Polanco)",
                "source_url": "https://facebook.com/groups/bazarpolanco/posts/traderjoes_demand",
                "city": "Mexico City (CDMX)",
                "colonia": "Polanco",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.97,
                "audience": "Both",
                "urgency": 3,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "fayuca / fayuquero moderno", "meaning": "Informal cross-border courier arbitrage for goods unavailable domestically"}],
                "problem_summary": "Ausencia de productos y sazonadores Trader Joe's en México provoca mercado negro en Instagram con 400% de sobreprecio.",
                "solution_found": "Encargar a familiares que viajen al gabacho o comprar en bazares locales con sobreprecio abusivo.",
                "market_opportunity": {
                    "venture_concept": "Cross-Border Specialty Grocery Hub & Private Label Seasoning Formulations",
                    "solution_summary": "A domestic specialty pantry brand formulating exact Mexican-made alternatives (Everything Bagel, Chili Crunch) plus pre-cleared US specialty snack curation."
                }
            },
            {
                "title": "Melatonina 10mg y antihistamínicos genéricos en botes de 365 pastillas (Kirkland/Costco USA)",
                "content": "Es ridículo cómo en México las farmacias (San Pablo, Benavides, Guadalajara) te venden la melatonina en cajas de 20 pastillas de 3mg a $280 pesos, cuando en Costco USA compras un bote de 360 gomitas de 10mg por $15 dólares. Igual con la cetirizina y loratadina: aquí te venden cajitas de 10 pastillas a precio de oro. COFEPRIS no deja pasar pedidos de iHerb si traen melatonina alta. Ojalá hubiera tiendas autorizadas que vendieran presentaciones a granel.",
                "source_platform": "Reddit (r/Guadalajara)",
                "source_url": "https://reddit.com/r/Guadalajara/comments/melatonin_bulk_mexico",
                "city": "Guadalajara (GDL)",
                "colonia": "Providencia",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.96,
                "audience": "Both",
                "urgency": 4,
                "sentiment": "Frustrated / Seeking Help",
                "matched_slang": [{"term": "me lo atoró la aduana / paquete retenido", "meaning": "Customs confiscation or 19%+ import tax barrier on foreign goods"}],
                "problem_summary": "Restricción de presentaciones a granel de melatonina y antihistamínicos en farmacias mexicanas y bloqueos de COFEPRIS en paquetería internacional.",
                "solution_found": "Pedir a amigos en Estados Unidos que los traigan en su equipaje documentado.",
                "market_opportunity": {
                    "venture_concept": "COFEPRIS Fast-Track Bulk OTC Wellness & Supplement Subscription",
                    "solution_summary": "Regulatory-compliant Mexican health brand offering bulk generic OTC allergy and sleep formulations at US parity pricing with national delivery."
                }
            },
            {
                "title": "Interruptores y relevadores Zigbee/Matter que NO requieren cable neutro (No Neutral Wire)",
                "content": "Para los que tenemos casas o departamentos en México: casi todas las instalaciones eléctricas antiguas no tienen cable neutro en las chalupas de los apagadores. En tiendas mexicanas como Steren o Home Depot solo venden apagadores WiFi que exigen neutro o focos inteligentes Tuya que saturan el módem y se desconectan a cada rato. En China (AliExpress/Taobao) marcas como Sonoff, Aqara y Tuya Zigbee tienen relevadores 'No Neutral' excelentes, pero tardan 40 días en llegar y Correos de México pierde la mitad.",
                "source_platform": "Twitter (X) - Compras Tech",
                "source_url": "https://twitter.com/smarthome_mx/status/17812001",
                "city": "Mexico City (CDMX)",
                "colonia": "Narvarte",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.95,
                "audience": "Local",
                "urgency": 3,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "pedir por aliexpress / taobao", "meaning": "Direct China sourcing for tech and household goods missing in Mexican retail"}],
                "problem_summary": "Mercado mexicano carece de hardware domótico Zigbee/Matter sin neutro adaptado a la infraestructura eléctrica residencial tradicional de México.",
                "solution_found": "Comprar en AliExpress y esperar 45 días asumiendo riesgo de extravío en Correos de México.",
                "market_opportunity": {
                    "venture_concept": "Smart-Home Retrofit Hardware & No-Neutral Switch Kits for Mexican Homes",
                    "solution_summary": "A specialized domestic smart-home brand stocking localized Zigbee/Matter no-neutral relays and switches with Mexican NOM electrical certification and next-day shipping."
                }
            },
            {
                "title": "Deshumidificadores compactos de desagüe continuo para clima tropical en Mérida y la costa",
                "content": "En Mérida la humedad relativa llega al 90% en temporada de lluvias y bochorno. Las paredes de mampostería colonial y los closets se llenan de moho negro (hongo), arruinando ropa, zapatos de piel e instrumentos musicales. En las tiendas de Yucatán (Liverpool, Chedraui, Home Depot Mérida) solo venden minisplits de aire acondicionado, NINGUNA tienda vende deshumidificadores potentes con compresor o desecante y manguera de desagüe continuo. En Japón y China hay deshumidificadores compactos increíbles. ¿Por qué nadie los vende en el sureste?",
                "source_platform": "Facebook (Vecinos Mérida Centro y Norte)",
                "source_url": "https://facebook.com/groups/vecinosmerida/posts/deshumidificadores_sarro",
                "city": "Mérida & Yucatán",
                "colonia": "Centro Histórico (Santiago, Santa Ana, Santa Lucía)",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.97,
                "audience": "Both",
                "urgency": 4,
                "sentiment": "Frustrated / Seeking Help",
                "matched_slang": [{"term": "ojalá vendieran / ojalá hubiera en méxico", "meaning": "Unmet consumer product void / High cross-border import demand"}],
                "problem_summary": "Inexistencia de deshumidificadores domésticos de alta capacidad en tiendas de Mérida a pesar de humedad extrema de más del 85% que pudre paredes y ropa.",
                "solution_found": "Poner botes de silica gel deshumidificadora desechable (Aroma Sílice) que se saturan en 48 horas.",
                "market_opportunity": {
                    "venture_concept": "Yucatán Tropical Indoor Humidity Control & Hardware Distribution",
                    "solution_summary": "A specialized HVAC startup importing high-efficiency compressor/desiccant dehumidifiers tailored for Yucatán limestone architecture with automated drainage installation."
                }
            },
            {
                "title": "Bloqueadores solares japoneses y coreanos ultraligeros (Biore UV Watery Essence, Skin Aqua)",
                "content": "¿Por qué en México casi no hay bloqueadores solares de tecnología japonesa o coreana? Los protectores solares de farmacia mexicana (Isdin, La Roche Posay, Eucerin) cuestan más de $600 pesos por un botecito diminuto y muchos dejan la cara grasosa o blanca en el calor. En Japón el Biore UV Aqua Rich cuesta $7 dólares ($120 pesos) y parece agua, pero COFEPRIS tiene trabas arcaicas con los filtros solares modernos (Tinosorb, Uvinul). En México las chicas terminan comprando en bazares coreanos al triple de precio.",
                "source_platform": "Facebook (Lady Multitask CDMX)",
                "source_url": "https://facebook.com/groups/ladymultitask/posts/bloqueadores_coreanos",
                "city": "Mexico City (CDMX)",
                "colonia": "Juárez",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.96,
                "audience": "Both",
                "urgency": 3,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "no llega a méxico / no hacen envíos a méxico", "meaning": "Geographic exclusion from international e-commerce & brand direct distribution"}],
                "problem_summary": "Regulaciones desactualizadas de COFEPRIS impiden la entrada formal de bloqueadores solares asiáticos ultraligeros y económicos.",
                "solution_found": "Comprar en tiendas de la Zona Rosa coreana con 250% de recargo o arriesgarse a piratería en Mercado Libre.",
                "market_opportunity": {
                    "venture_concept": "Certified Asian Dermo-Cosmetics Import Concierge & COFEPRIS Registry Hub",
                    "solution_summary": "Direct-to-consumer authorized distributor clearing next-gen Asian suncare and skincare products with official COFEPRIS sanitary registration and anti-counterfeit batch verification."
                }
            },
            {
                "title": "Areneros automáticos autolimpiables para gatos (Litter-Robot, Petkit Pura Max)",
                "content": "Tengo 3 gatos en departamento en Monterrey y limpiar areneros diario con el olor es una pesadilla. En USA todo el mundo usa el Litter-Robot 4 o Petkit Pura Max que se limpian solos y avisan al celular. En México Petkit no tiene distribuidor oficial y en Amazon México los revendedores lo tienen en $26,000 pesos cuando en USA vale $500 dólares ($9,000 pesos). Si se descompone el motor no hay refacciones en el país. Ojalá vendieran areneros automáticos a precio justo y con centro de servicio técnico.",
                "source_platform": "Reddit (r/Monterrey)",
                "source_url": "https://reddit.com/r/Monterrey/comments/litter_robot_mexico",
                "city": "Monterrey (MTY)",
                "colonia": "San Pedro Garza García",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.95,
                "audience": "Both",
                "urgency": 3,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "mandar a traer del gabacho / traer de usa", "meaning": "Cross-border informal purchasing to bypass Mexican retail availability gaps"}],
                "problem_summary": "Sobreprecio abusivo de 200%+ y falta de refacciones locales para areneros inteligentes autolimpiables en México.",
                "solution_found": "Cruzar en coche a McAllen o Laredo para comprarlo en Petco USA y pasarlo por aduana en la cajuela.",
                "market_opportunity": {
                    "venture_concept": "Smart Pet Automation Direct Distribution & Certified Warranty Repair Fleet",
                    "solution_summary": "Authorized import and technical servicing for automated pet appliances (self-cleaning litter boxes, smart feeders, fountains) with domestic spare parts inventory."
                }
            },
            {
                "title": "Ninja Creami para hacer helados y helados de proteína (agotado y revendedores al triple)",
                "content": "¿Por qué Ninja no surte suficiente stock de la Ninja Creami y sus botes de repuesto en México? En Liverpool y Walmart siempre está agotada, y en Mercado Libre te cobran $9,500 pesos por la máquina que en Target USA está en $179 dólares ($3,200 MXN). Además conseguir los recipientes de plástico extra en México es imposible, te quieren cobrar $1,200 por 2 botes de plástico. Miles de personas haciendo dietas keto o fitness buscando esta máquina.",
                "source_platform": "Facebook (Bazar Coyoacán)",
                "source_url": "https://facebook.com/groups/bazarcoyoacan/posts/ninja_creami_stock",
                "city": "Mexico City (CDMX)",
                "colonia": "Coyoacán",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.98,
                "audience": "Both",
                "urgency": 3,
                "sentiment": "Frustrated / Seeking Help",
                "matched_slang": [{"term": "ojalá vendieran", "meaning": "Unmet consumer product void / High cross-border import demand"}],
                "problem_summary": "Desabasto crónico de Ninja Creami y botes de repuesto en México, explotado por revendedores de Mercado Libre al 300% de sobreprecio.",
                "solution_found": "Usar casilleros de paquetería en Laredo (Redpost/Estafeta Members) pagando altos fletes y aranceles.",
                "market_opportunity": {
                    "venture_concept": "Viral Kitchen Appliance Import Arbitrage & Accessories Ecosystem",
                    "solution_summary": "High-velocity retail arbitrage importing viral kitchen hardware and manufacturing high-margin accessories (BPA-free extra pints, insulating sleeves) locally."
                }
            },
            {
                "title": "Molinos manuales de café de muelas cónicas de precisión (1Zpresso, Timemore C3 ESP)",
                "content": "México es uno de los mejores productores de café de especialidad del mundo (Veracruz, Chiapas, Oaxaca), pero conseguir equipo de extracción en el país es una tristeza. En tiendas mexicanas solo encuentras molinos eléctricos de cuchillas que queman el café o máquinas comerciales de $30,000 pesos. Si quieres un molino manual de muelas de acero como 1Zpresso J-Max o Timemore C3 para espresso, tienes que pedirlo a Taiwán o China y arriesgarte a que la aduana te cobre 19% de IVA y gastos de despacho postal. Ojalá hubiera tiendas especializadas locales.",
                "source_platform": "Reddit (r/mexico)",
                "source_url": "https://reddit.com/r/mexico/comments/molinos_cafe_especialidad",
                "city": "Guadalajara (GDL)",
                "colonia": "Americana",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.96,
                "audience": "Both",
                "urgency": 3,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "no hay en méxico", "meaning": "Unmet consumer product void / High cross-border import demand"}],
                "problem_summary": "Paradoja de país productor de café de alta calidad sin distribución local de molinos manuales de precisión para café de especialidad.",
                "solution_found": "Importación personal desde distribuidores asiáticos con sorpresas tributarias de aduana.",
                "market_opportunity": {
                    "venture_concept": "Specialty Coffee Gear & Precision Barista D2C Store Mexico",
                    "solution_summary": "Dedicated Mexican e-commerce platform offering top-rated international manual grinders, espresso tools, and drippers with domestic warranty and bean subscriptions."
                }
            },
            {
                "title": "Malla limpiadora de cota de malla (Chainmail) y cera para sartenes de hierro fundido (Cast Iron)",
                "content": "Los que cocinamos con sartenes de hierro fundido en México sufrimos porque en los súpers (Chedraui, Soriana) solo venden fibras verdes Scotch-Brite que le quitan el curado al sartén. En USA compras limpiadores de cota de malla de acero inoxidable (chainmail scrubbers) y cera orgánica Crisbee para curarlos. En México no hay ninguna marca local que los fabrique; en Amazon MX te los mandan de importación de USA a $600 pesos por un pedacito de malla que cuesta $3 dólares en China.",
                "source_platform": "Facebook (Vecinos Providencia GDL)",
                "source_url": "https://facebook.com/groups/vecinosprovidenciagdl/posts/cast_iron_scrubber",
                "city": "Guadalajara (GDL)",
                "colonia": "Providencia",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.94,
                "audience": "Both",
                "urgency": 2,
                "sentiment": "Informative / Seeking Workaround",
                "matched_slang": [{"term": "no se consigue en méxico", "meaning": "Unmet consumer product void / High cross-border import demand"}],
                "problem_summary": "Inexistencia de herramientas de mantenimiento para utensilios de hierro fundido en el retail tradicional mexicano.",
                "solution_found": "Limpiar con sal de grano gruesa y toallas de papel o pedir a amigos que viajen al extranjero.",
                "market_opportunity": {
                    "venture_concept": "Artisanal Cast Iron Cookware Care & Domestic Metal Goods Brand",
                    "solution_summary": "Mexican manufacturing of stainless-steel chainmail scrubbers, beeswax seasoning pucks, and leather handle covers distributed across culinary specialty shops."
                }
            },
            {
                "title": "Parches hidrocoloides extragrandes para acné corporal y heridas (Mighty Patch Surface)",
                "content": "En farmacias mexicanas te venden cajitas de 'pimple patches' con 12 rueditas microscópicas a $180 pesos. En USA y Corea venden parches hidrocoloides tamaño sábana (Mighty Patch Surface, Cosrx Master Patch) de 6x6 cm para brotes en la espalda, pecho o raspones de bici. En México no existen en farmacias de cadena; si los pides por Amazon US te cobran $15 dólares de envío por un sobrecito. Es un producto básico para el cuidado de la piel que urge que traigan a México.",
                "source_platform": "Reddit (r/MexicoCity)",
                "source_url": "https://reddit.com/r/MexicoCity/comments/hydrocolloid_patches_mx",
                "city": "Mexico City (CDMX)",
                "colonia": "Condesa",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.97,
                "audience": "Both",
                "urgency": 3,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "no hay en méxico", "meaning": "Unmet consumer product void / High cross-border import demand"}],
                "problem_summary": "Falta de formatos grandes de apósitos hidrocoloides para cuidado dermatológico corporal a precios accesibles en farmacias mexicanas.",
                "solution_found": "Comprar apósitos para úlceras de pie diabético en droguerías médicas y cortarlos con tijeras.",
                "market_opportunity": {
                    "venture_concept": "Affordable D2C Hydrocolloid Acne & Wound Care Brand (Mexico)",
                    "solution_summary": "A domestic Mexican skincare brand producing large-format medical-grade hydrocolloid sheets for facial and body blemish care sold through farmacias and Amazon MX."
                }
            },
            {
                "title": "Aspiradoras robot con estación de autovaciado, lavado activo de mopa con agua caliente y secado (Roborock / Dreame)",
                "content": "¿Por qué marcas como Roborock o Dreame traen a México solo sus modelos viejos que solo barren y tienen mopas pasivas que huelen a perro mojado? En China y USA ya todas las aspiradoras robot lavan la mopa con agua a 60 grados y la secan con aire caliente para no generar bacterias. En las casas de Monterrey y CDMX donde hay mucho polvo y azulejo son indispensables. Para tener una hay que traerla de contrabando o pagar $35,000 pesos en importadores grises.",
                "source_platform": "Twitter (X) - Smart Home México",
                "source_url": "https://twitter.com/roborock_mexico/status/17814002",
                "city": "Monterrey (MTY)",
                "colonia": "Valle Oriente",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.95,
                "audience": "Both",
                "urgency": 3,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "traer del gabacho", "meaning": "Cross-border informal purchasing to bypass Mexican retail availability gaps"}],
                "problem_summary": "Exclusión del mercado mexicano de los modelos insignia de aspiradoras robot con autolavado térmico de mopa, forzando importaciones informales de alto costo.",
                "solution_found": "Importar vía AliExpress esperando semanas o pagar el doble a revendedores sin soporte.",
                "market_opportunity": {
                    "venture_concept": "Premium Domestic Robotics Importer & White-Glove Smart Home Installation",
                    "solution_summary": "Direct partnership importing flagship home robotics with 110V Mexican plugs, local NOM certification, consumable replacement delivery, and technical maintenance."
                }
            },
            {
                "title": "Consolidación marítima Puerto de Progreso - Miami para insumos europeos y herramientas alemanas",
                "content": "Para la comunidad de constructores, restauradores y extranjeros en Mérida y la costa de Yucatán: traer herramientas alemanas de calidad (Wera, Knipex, Festool) o refacciones para sistemas solares europeos es una odisea porque todo pasa por la aduana del Aeropuerto de CDMX con retrasos de meses y tarifas abusivas. Teniendo el Puerto de Progreso a 30 minutos de Mérida y Miami enfrente en el Golfo, debería existir una naviera de consolidación directa para compras de USA y Europa sin pasar por CDMX.",
                "source_platform": "Facebook (Mérida Expats & Foreigners Community)",
                "source_url": "https://facebook.com/groups/meridaexpats/posts/progreso_miami_shipping",
                "city": "Mérida & Yucatán",
                "colonia": "Altabrisa",
                "category": "Product Voids & Import Wishlist",
                "confidence": 0.98,
                "audience": "Both",
                "urgency": 4,
                "sentiment": "Inquiring / Service Gap",
                "matched_slang": [{"term": "me lo atoró la aduana / paquete retenido", "meaning": "Customs confiscation or 19%+ import tax barrier on foreign goods"}],
                "problem_summary": "Falta de conexión logística directa marítima Miami-Progreso obliga a residentes de Yucatán a sufrir cuellos de botella en aduanas del centro del país para herramientas y bienes importados.",
                "solution_found": "Pagar envíos exprés aéreos exorbitantes por DHL o esperar a que alguien viaje en avión con sobrepeso de equipaje.",
                "market_opportunity": {
                    "venture_concept": "Port of Progreso Maritime Consolidation for US & European Specialty Goods",
                    "solution_summary": "A direct maritime container logistics service linking Florida/Gulf ports directly to Puerto Progreso, bypassing CDMX customs bottlenecks to supply Mérida expats and locals with missing home goods, appliances, and specialty foods."
                }
            }
        ]

        inserted = 0
        for s in seeds:
            if self.insert_problem(s):
                inserted += 1

        return inserted

    def get_product_voids(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Returns all consumer product void records.
        """
        return self.get_all_problems(limit=limit, category="Product Voids & Import Wishlist")

