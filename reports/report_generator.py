"""
Daily Intelligence Report Generator for MexConsumerPulse.
Synthesizes collected data into clear, bullet-pointed executive market research reports.
Supports both National multi-city briefings and dedicated regional reports for:
- Mérida & The Yucatán Peninsula
- Mexico City (CDMX)
- Guadalajara (GDL)
- Monterrey (MTY)
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import REPORTS_DIR
from agents.dataset_manager import DatasetManager

class DailyReportGenerator:
    """
    Engine transforming raw consumer problem datasets into executive daily intelligence briefings.
    Supports National and Regional (Mérida & Yucatán, CDMX, GDL, MTY) deep-dives.
    """

    def __init__(self):
        self.db = DatasetManager()
        self.reports_dir = REPORTS_DIR

    def generate_report(self, date_str: str = None, region: str = "All", lang: str = "es") -> Dict[str, Any]:
        """
        Generate, save, and persist a daily bullet-pointed market research report.
        Can generate for 'All' (National) or specific regions like 'Mérida & Yucatán',
        in either Spanish ('es') or English ('en').
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        all_problems = self.db.get_all_problems(limit=300)
        
        # Filter by region if requested
        if region != "All":
            problems = [p for p in all_problems if region.lower() in p.get("city", "").lower() or (region == "Mérida & Yucatán" and ("mérida" in p.get("city", "").lower() or "yucatán" in p.get("city", "").lower()))]
        else:
            problems = all_problems

        # Segment by category and urgency
        urgent_problems = [p for p in problems if p.get("urgency", 0) >= 4]
        expat_problems = [p for p in problems if p.get("audience") in ["Expat", "Both"]]
        local_problems = [p for p in problems if p.get("audience") in ["Local", "Both"]]

        if region == "Mérida & Yucatán":
            report_title = f"Informe Regional de Inteligencia del Consumidor: Mérida y Yucatán - {date_str}" if lang == "es" else f"Mérida & Yucatán Regional Consumer Intelligence Briefing - {date_str}"
            report_key = f"{date_str}_merida_yucatan_{lang}"
            file_suffix = f"report_merida_yucatan_{date_str}_{lang}.md"
        else:
            report_title = f"Reporte de Inteligencia del Consumidor Urbano en México (Nacional) - {date_str}" if lang == "es" else f"Mexican Urban Consumer Intelligence Report (National) - {date_str}"
            report_key = f"{date_str}_{lang}"
            file_suffix = f"report_{date_str}_{lang}.md"

        # Compute dynamic stats for this report scope
        cat_counts = {}
        for p in problems:
            c = p.get("category", "General")
            cat_counts[c] = cat_counts.get(c, 0) + 1

        top_category = max(cat_counts, key=cat_counts.get) if cat_counts else "Infrastructure & Utilities"

        # Build Executive Bullet Summary
        if lang == "es":
            if region == "Mérida & Yucatán":
                exec_bullets = [
                    f"**Puntos de Fricción Verificados en Mérida y Yucatán**: {len(problems)} incidentes activos documentados en Centro Histórico, Altabrisa, Montebello, Conkal y Progreso.",
                    f"**Carga Crítica de Servicios Públicos**: Dureza extrema del agua por caliza (*sarro de JAPAY*) destruyendo calentadores y tuberías, sumado a picos tarifarios de CFE por aire acondicionado.",
                    f"**Alerta de Fraude Inmobiliario**: Proliferación de supuestos 'terrenos de inversión' en litigios ejidales sin luz ni agua en la carretera Mérida–Telchac.",
                    f"**Cuello de Botella de Patrimonio e INAH**: Clausuras y sellos del INAH frenando restauraciones de casonas coloniales en Mérida Centro de 8 a 18 meses.",
                    f"**Tensión entre Locales y Expats**: Alzas de rentas en barrios históricos (Santiago, Santa Ana) vs. falta de contratos transparentes y daños por salitre."
                ]
            else:
                exec_bullets = [
                    f"**Total de Problemas Verificados Monitoreados**: {len(problems)} casos registrados en zonas metropolitanas de México.",
                    f"**Alertas de Alta Urgencia (Severidad 4-5)**: {len(urgent_problems)} fallas críticas de infraestructura y disputas legales activas.",
                    f"**Vector Dominante de Fricción**: `{top_category}` representa la categoría de mayor frecuencia de quejas ciudadanas.",
                    f"**Cobertura Regional Especializada**: Monitoreo dedicado para Ciudad de México, Guadalajara, Monterrey y Mérida / Península de Yucatán.",
                    f"**Desglose Demográfico**: {len(local_problems)} reportes de Residentes Locales, {len(expat_problems)} de Extranjeros / Expats."
                ]
        else:
            if region == "Mérida & Yucatán":
                exec_bullets = [
                    f"**Mérida & Yucatán Verified Pain Points**: {len(problems)} active consumer friction issues documented across Centro Histórico, Altabrisa, Montebello, and Conkal.",
                    f"**Top Regional Utility Burden**: Severe limestone water hardness (*sarro de JAPAY*) destroying water heaters and pipe networks, coupled with CFE summer cooling bill spikes.",
                    f"**Critical Real Estate Alert**: Proliferation of speculative 'terrenos de inversión' ejidal fraud along the Mérida–Telchac corridor targeting uninformed buyers.",
                    f"**Heritage & Renovation Bottleneck**: Federal INAH work shutdowns halting colonial casona restorations in Mérida Centro for 8–18 months.",
                    f"**Expat vs. Local Tension**: Gentrification in historic barrios (Santiago, Santa Ana) vs. lack of bilingual contractor transparency and salitre damage."
                ]
            else:
                exec_bullets = [
                    f"**Total Verified Pain Points Tracked**: {len(problems)} across Mexican metropolitan centers.",
                    f"**High Urgency Alerts (Severity 4-5)**: {len(urgent_problems)} critical infrastructure and legal issues currently active.",
                    f"**Dominant Friction Vector**: `{top_category}` is currently the highest-frequency complaint category.",
                    f"**Key Regional Inclusions**: Dedicated coverage for Mexico City, Guadalajara, Monterrey, and Mérida & The Yucatán Peninsula.",
                    f"**Demographic Breakdown**: {len(local_problems)} Local-specific, {len(expat_problems)} Expat-specific concerns."
                ]

        exec_summary_text = "\n".join([f"- {b}" for b in exec_bullets])

        # Markdown Document Assembly
        md_lines = []
        md_lines.append(f"# {report_title}\n")
        if lang == "es":
            md_lines.append(f"> **Fecha de Generación**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | **Alcance Regional**: {region} | **Idioma**: Español 🇲🇽")
            md_lines.append("> **Privacidad**: 100% Anonimizado bajo la *Ley Federal de Protección de Datos Personales*\n")
            md_lines.append("## 1. Resumen Ejecutivo e Indicadores Clave")
        else:
            md_lines.append(f"> **Generated at**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | **Scope**: {region} | **Language**: English 🇺🇸")
            md_lines.append("> **Compliance**: 100% Anonymized under *Ley Federal de Protección de Datos Personales*\n")
            md_lines.append("## 1. Executive Briefing & Key Indicators")

        md_lines.append(exec_summary_text)
        md_lines.append("")

        if lang == "es":
            md_lines.append(f"## 2. Principales Puntos Críticos y Urgentes de Fricción ({region})")
        else:
            md_lines.append(f"## 2. Top Urgent Consumer Pain Points ({region})")

        top_urgent = urgent_problems[:6] if urgent_problems else problems[:6]
        if not top_urgent:
            md_lines.append("- *No hay problemas urgentes registrados para esta región.*" if lang == "es" else "- *No urgent problems currently logged for this specific region.*")
        else:
            for idx, p in enumerate(top_urgent, 1):
                md_lines.append(f"### {idx}. {p.get('title')}")
                md_lines.append(f"- **Ciudad / Colonia**: {p.get('city')} ({p.get('colonia', 'General')})")
                md_lines.append(f"- **Categoría**: `{p.get('category')}` | **Severidad**: {'🔴' * p.get('urgency', 3)} ({p.get('urgency')}/5) | **Población**: {p.get('audience')}")
                md_lines.append(f"- **Problema Identificado**: {p.get('problem_summary')}")
                md_lines.append(f"- **Solución / Alternativa Actual**: {p.get('solution_found')}")
                if p.get("venture_concept"):
                    md_lines.append(f"- **Oportunidad de Negocio**: *{p.get('venture_concept')}* — {p.get('solution_summary')}")
                md_lines.append("")

        if region == "Mérida & Yucatán":
            if lang == "es":
                md_lines.append("## 3. Desglose Específico de Fricción en Mérida y Yucatán")
                md_lines.append("| Vector de Problema | Causa Raíz | Frustración del Consumidor | Oportunidad de Mercado |")
                md_lines.append("| :--- | :--- | :--- | :--- |")
                md_lines.append("| **Agua con Caliza (Sarro)** | Acuífero kárstico; líneas de JAPAY con altísimo calcio | Calentadores arruinados, llaves atascadas, sarro en tinacos | Suavizadores de agua domésticos, mantenimiento por suscripción |")
                md_lines.append("| **Terrenos de Inversión** | Subdivisión ejidal no regulada sin luz ni agua | Pérdida de ahorros en predios inaccesibles en el monte | Verificación satelital de títulos de propiedad y depósitos en garantía |")
                md_lines.append("| **Tarifas de CFE en Verano** | Olas de calor de más de 40°C que exigen minisplits 24/7 | Recibos bimestrales que saltan de $800 a $8,000+ MXN | Termostatos inteligentes y paneles solares con interconexión rápida |")
                md_lines.append("| **Salitre y Humedad** | Capilaridad tropical que disuelve el mortero de cal | Pintura y yeso desprendiéndose a los pocos meses de aplicar | Inyecciones químicas contra salitre y pinturas transpirables |")
                md_lines.append("| **Permisos INAH en Casonas** | Normativas estrictas de preservación patrimonial | Obras clausuradas por 12+ meses con sellos federales | Gestoría digital de permisos de restauración pre-aprobados |")
            else:
                md_lines.append("## 3. Mérida & Yucatán Specific Friction Breakdown")
                md_lines.append("| Problem Vector | Root Cause | Consumer Frustration | Market Opportunity |")
                md_lines.append("| :--- | :--- | :--- | :--- |")
                md_lines.append("| **Limestone Water (Sarro)** | Karst aquifer geology; JAPAY municipal lines high in calcium | Ruined water heaters, clogged faucets, dry skin, mineral buildup | Home ionization water softeners, descaling subscription services |")
                md_lines.append("| **Terrenos de Inversión** | Unregulated ejido land subdivision with no electricity/water | Thousands of buyers lose savings on inaccessible jungle plots | Satellite/drone land registry title verification & escrow |")
                md_lines.append("| **CFE Summer AC Tariffs** | 40°C+ heatwaves with 85% humidity requiring 24/7 cooling | Electric bills jumping from $800 to $8,000+ MXN per cycle | Smart minisplit thermostats & accelerated solar interconnections |")
                md_lines.append("| **Salitre & Humidity** | Tropical moisture capillary action dissolving lime mortar | Wall plaster bubbling and falling off within months of painting | Specialized anti-salitre barrier injections & breathability paints |")
                md_lines.append("| **INAH Heritage Permits** | Historic preservation regulations for colonial casonas | Renovation work halted with federal seals for 12+ months | Architectural permit facilitation & pre-approved restoration designs |")
            md_lines.append("")
        else:
            if lang == "es":
                md_lines.append("## 3. Matriz Comparativa: Residentes Locales vs. Expats Extranjeros")
                md_lines.append("| Dimensión | Dolores de Residentes Locales | Dolores de Expats y Nómadas Digitales |")
                md_lines.append("| :--- | :--- | :--- |")
                md_lines.append("| **Vivienda y Rentas** | Aumentos abusivos de renta en Condesa/Roma/Mérida; caseros reteniendo depósitos sin causa | Imposibilidad de presentar *fiador con bien raíz*; cobro de costosas *pólizas jurídicas*; pérdida de depósitos |")
                md_lines.append("| **Burocracia y Gobierno** | Escasez de citas del SAT; reventa en mercado negro; filas virtuales para RFC y e.firma | Trabas para tramitar RFC sin cuenta bancaria mexicana; apostillas; barreras de idioma en INM |")
                md_lines.append("| **Oficios y Reparaciones** | Desconfianza en maestros albañiles que piden anticipo y dejan obras a medias | Dificultad para hallar contratistas bilingües; cobro inflado de 'impuesto al gringo' |")
                md_lines.append("| **Servicios y Red Eléctrica** | Tandeo y cortes de agua; pipas caras; sobrevoltajes de CFE quemando electrodomésticos | Obstrucción de tuberías por sarro de JAPAY; desconocimiento de horarios de tandeo |")
            else:
                md_lines.append("## 3. Locals vs. Expats Friction Comparison Matrix")
                md_lines.append("| Dimension | Local Residents Pain Points | Foreign Expats / Digital Nomads Pain Points |")
                md_lines.append("| :--- | :--- | :--- |")
                md_lines.append("| **Housing & Rents** | Outrage over rising rents in Condesa/Roma/Mérida; aggressive landlords charging for wear-and-tear | Inability to provide a Mexican *fiador con bien raíz*; exorbitant non-refundable *póliza jurídica* fees; lost deposits |")
                md_lines.append("| **Bureaucracy & Gov** | SAT cita scarcity; sold appointments in black market; waiting in virtual queues for RFC and e.firma | Conflicting requirements for RFC without Mexican bank account; apostille delays; language barriers at INM |")
                md_lines.append("| **Home Maintenance** | Distrust of unverified *maestros albañiles* who take advance payments and abandon jobs | Finding English-speaking or transparently-priced contractors; vulnerability to 'gringo tax' overcharging |")
                md_lines.append("| **Utilities & Grid** | Water rationing (*tandeo*); high pipa prices; CFE electrical surges frying household appliances | JAPAY limestone sarro clogging; lack of awareness about water delivery schedules |")
            md_lines.append("")

        if lang == "es":
            md_lines.append("## 4. Desglose por Categoría de Problema")
            for cat, cnt in cat_counts.items():
                pct = round((cnt / max(1, len(problems))) * 100, 1)
                md_lines.append(f"- **{cat}**: {cnt} reportes ({pct}%)")
            md_lines.append("")

            md_lines.append("## 5. Hipótesis Estratégicas de Emprendimiento y Brechas de Mercado")
        else:
            md_lines.append("## 4. Problem Category Breakdown")
            for cat, cnt in cat_counts.items():
                pct = round((cnt / max(1, len(problems))) * 100, 1)
                md_lines.append(f"- **{cat}**: {cnt} reports ({pct}%)")
            md_lines.append("")

            md_lines.append("## 5. Strategic Venture Hypotheses & Market Gaps")

        concepts_seen = set()
        for p in problems:
            concept = p.get("venture_concept")
            summary = p.get("solution_summary")
            if concept and concept not in concepts_seen:
                concepts_seen.add(concept)
                md_lines.append(f"### 💡 {concept}")
                if lang == "es":
                    md_lines.append(f"- **Cliente Objetivo**: {p.get('audience')} en {p.get('city')}")
                    md_lines.append(f"- **Brecha de Mercado**: {summary}")
                    md_lines.append(f"- **Señal en Plataformas**: Derivado de discusiones comunitarias en {p.get('source_platform')}")
                else:
                    md_lines.append(f"- **Target Customer**: {p.get('audience')} in {p.get('city')}")
                    md_lines.append(f"- **Market Gap**: {summary}")
                    md_lines.append(f"- **Platform Signal**: Derived from discussions on {p.get('source_platform')}")
                md_lines.append("")
                if len(concepts_seen) >= 6:
                    break

        # Product Voids & Cross-Border Retail Arbitrage Intelligence Section
        product_voids = [p for p in problems if p.get("category") == "Product Voids & Import Wishlist"]
        if not product_voids:
            product_voids = self.db.get_product_voids(limit=10)

        if product_voids:
            if lang == "es":
                md_lines.append("## 6. Vacíos de Producto Transfronterizo e Inteligencia 'Ojalá Vendieran Esto en México'")
                md_lines.append("Análisis de bienes de consumo extranjeros ampliamente disponibles en EE.UU., China, Japón o Europa que los consumidores mexicanos buscan activamente pero no pueden adquirir formalmente debido a trabas regulatorias, arancelarias o falta de distribución de marca.\n")
                md_lines.append("| Producto / Característica Faltante | País de Origen | Barrera Principal en México | Solución Actual del Consumidor | Oportunidad de Emprendimiento / Arbitraje |")
                md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
            else:
                md_lines.append("## 6. Cross-Border Product Voids & 'I Wish They Sold This in Mexico' Intelligence")
                md_lines.append("Analysis of foreign consumer goods widely available in the U.S., China, Japan, or Europe that Mexican consumers actively search for but cannot purchase domestically due to regulatory, tariff, or distribution barriers.\n")
                md_lines.append("| Missing Product / Feature | Origin Country | Key Barrier in Mexico | Current Consumer Workaround | Venture / Import Arbitrage |")
                md_lines.append("| :--- | :--- | :--- | :--- | :--- |")

            for pv in product_voids[:8]:
                title_short = pv.get('title', '').replace('Ojalá vendieran en México los ', '').replace('Ojalá vendieran ', '')[:45]
                origin = "🇺🇸 USA" if "trader" in title_short.lower() or "melatonina" in title_short.lower() or "creami" in title_short.lower() or "areneros" in title_short.lower() else ("🇨🇳 China" if "zigbee" in title_short.lower() or "aspiradoras" in title_short.lower() or "molinos" in title_short.lower() else ("🇯🇵 Japan / 🇰🇷 Korea" if "bloqueadores" in title_short.lower() or "deshumidificadores" in title_short.lower() else "🇺🇸 USA / 🇨🇳 China"))
                if "progreso" in title_short.lower() or "herramientas" in title_short.lower():
                    origin = "🇪🇺 Europe / 🇺🇸 USA"
                
                barrier = pv.get('problem_summary', '')[:85]
                workaround = pv.get('solution_found', '')[:75]
                opp = pv.get('venture_concept', '')[:65]
                md_lines.append(f"| **{title_short}** | {origin} | {barrier}... | {workaround}... | *{opp}* |")
            md_lines.append("")

        if lang == "es":
            md_lines.append("## 7. Citas Textuales Anónimas del Campo")
        else:
            md_lines.append("## 7. Verbatim Field Quotes (Anonymized)")

        for idx, p in enumerate(problems[:6], 1):
            md_lines.append(f"> *\"{p.get('content', '')[:160]}...\"*")
            if lang == "es":
                md_lines.append(f"> — **Fuente**: {p.get('source_platform')} | **Ciudad**: {p.get('city')}\n")
            else:
                md_lines.append(f"> — **Source**: {p.get('source_platform')} | **City**: {p.get('city')}\n")

        full_markdown = "\n".join(md_lines)

        # Save to file
        report_file = self.reports_dir / file_suffix
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(full_markdown)

        # Persist in SQLite
        self.db.save_daily_report(
            report_date=report_key,
            title=report_title,
            summary=exec_summary_text,
            markdown=full_markdown,
            metrics={"total_problems": len(problems), "category_counts": cat_counts, "region": region, "lang": lang}
        )

        print(f"[DailyReportGenerator] Successfully synthesized and saved report ({lang}): {report_file}")
        return {
            "report_key": report_key,
            "report_date": date_str,
            "report_file": str(report_file),
            "report_title": report_title,
            "region": region,
            "lang": lang,
            "total_problems_analyzed": len(problems),
            "markdown": full_markdown
        }

    def generate_all_reports(self, date_str: str = None) -> List[Dict[str, Any]]:
        """
        Generates both National and Regional reports in both Spanish ('es') and English ('en').
        """
        regions = ["All", "Mérida & Yucatán", "Mexico City (CDMX)", "Guadalajara (GDL)", "Monterrey (MTY)"]
        results = []
        for reg in regions:
            for l in ["es", "en"]:
                res = self.generate_report(date_str=date_str, region=reg, lang=l)
                results.append(res)
        return results

    def _get_top_item(self, counts_dict: Dict[str, int]) -> str:
        if not counts_dict:
            return "General Infrastructure"
        return max(counts_dict, key=counts_dict.get)

if __name__ == "__main__":
    gen = DailyReportGenerator()
    res = gen.generate_all_reports()
    print(f"Generated {len(res)} reports successfully.")
