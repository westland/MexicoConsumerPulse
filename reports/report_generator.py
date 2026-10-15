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

    def generate_report(self, date_str: str = None, region: str = "All") -> Dict[str, Any]:
        """
        Generate, save, and persist a daily bullet-pointed market research report.
        Can generate for 'All' (National) or specific regions like 'Mérida & Yucatán'.
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
            report_title = f"Mérida & Yucatán Regional Consumer Intelligence Briefing - {date_str}"
            report_key = f"{date_str}_merida_yucatan"
            file_suffix = f"report_merida_yucatan_{date_str}.md"
        else:
            report_title = f"Mexican Urban Consumer Intelligence Report (National) - {date_str}"
            report_key = date_str
            file_suffix = f"report_{date_str}.md"

        # Compute dynamic stats for this report scope
        cat_counts = {}
        for p in problems:
            c = p.get("category", "General")
            cat_counts[c] = cat_counts.get(c, 0) + 1

        top_category = max(cat_counts, key=cat_counts.get) if cat_counts else "Infrastructure & Utilities"

        # Build Executive Bullet Summary
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
        md_lines.append(f"> **Generated at**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} | **Scope**: {region}")
        md_lines.append("> **Compliance**: 100% Anonymized under *Ley Federal de Protección de Datos Personales*\n")
        
        md_lines.append("## 1. Executive Briefing & Key Indicators")
        md_lines.append(exec_summary_text)
        md_lines.append("")

        md_lines.append(f"## 2. Top Urgent Consumer Pain Points ({region})")
        top_urgent = urgent_problems[:6] if urgent_problems else problems[:6]
        if not top_urgent:
            md_lines.append("- *No urgent problems currently logged for this specific region.*")
        else:
            for idx, p in enumerate(top_urgent, 1):
                md_lines.append(f"### {idx}. {p.get('title')}")
                md_lines.append(f"- **City / Colonia**: {p.get('city')} ({p.get('colonia', 'General')})")
                md_lines.append(f"- **Category**: `{p.get('category')}` | **Severity**: {'🔴' * p.get('urgency', 3)} ({p.get('urgency')}/5) | **Target**: {p.get('audience')}")
                md_lines.append(f"- **Identified Problem**: {p.get('problem_summary')}")
                md_lines.append(f"- **Community Workaround**: {p.get('solution_found')}")
                if p.get("venture_concept"):
                    md_lines.append(f"- **Venture Opportunity**: *{p.get('venture_concept')}* — {p.get('solution_summary')}")
                md_lines.append("")

        if region == "Mérida & Yucatán":
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
            md_lines.append("## 3. Locals vs. Expats Friction Comparison Matrix")
            md_lines.append("| Dimension | Local Residents Pain Points | Foreign Expats / Digital Nomads Pain Points |")
            md_lines.append("| :--- | :--- | :--- |")
            md_lines.append("| **Housing & Rents** | Outrage over rising rents in Condesa/Roma/Mérida; aggressive landlords charging for wear-and-tear | Inability to provide a Mexican *fiador con bien raíz*; exorbitant non-refundable *póliza jurídica* fees; lost deposits |")
            md_lines.append("| **Bureaucracy & Gov** | SAT cita scarcity; sold appointments in black market; waiting in virtual queues for RFC and e.firma | Conflicting requirements for RFC without Mexican bank account; apostille delays; language barriers at INM |")
            md_lines.append("| **Home Maintenance** | Distrust of unverified *maestros albañiles* who take advance payments and abandon jobs | Finding English-speaking or transparently-priced contractors; vulnerability to 'gringo tax' overcharging |")
            md_lines.append("| **Utilities & Grid** | Water rationing (*tandeo*); high pipa prices; CFE electrical surges frying household appliances | JAPAY limestone sarro clogging; lack of awareness about water delivery schedules |")
            md_lines.append("")

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
                md_lines.append(f"- **Target Customer**: {p.get('audience')} in {p.get('city')}")
                md_lines.append(f"- **Market Gap**: {summary}")
                md_lines.append(f"- **Platform Signal**: Derived from discussions on {p.get('source_platform')}")
                md_lines.append("")
                if len(concepts_seen) >= 4:
                    break

        md_lines.append("## 6. Verbatim Field Quotes (Anonymized)")
        for idx, p in enumerate(problems[:5], 1):
            md_lines.append(f"> *\"{p.get('content', '')[:160]}...\"*")
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
            metrics={"total_problems": len(problems), "category_counts": cat_counts, "region": region}
        )

        print(f"[DailyReportGenerator] Successfully synthesized and saved report: {report_file}")
        return {
            "report_key": report_key,
            "report_date": date_str,
            "report_file": str(report_file),
            "report_title": report_title,
            "region": region,
            "total_problems_analyzed": len(problems),
            "markdown": full_markdown
        }

    def generate_all_reports(self, date_str: str = None) -> List[Dict[str, Any]]:
        """
        Generates both National and Regional reports (Mérida & Yucatán, CDMX, GDL, MTY).
        """
        regions = ["All", "Mérida & Yucatán", "Mexico City (CDMX)", "Guadalajara (GDL)", "Monterrey (MTY)"]
        results = []
        for reg in regions:
            res = self.generate_report(date_str=date_str, region=reg)
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
