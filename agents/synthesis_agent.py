"""
Synthesis & NLP Agent for Mexican Consumer Research.
Understands Mexican modismos, classifies consumer problems into taxonomy,
assesses urgency/sentiment, identifies geographic nuance (colonias/cities),
distinguishes locals vs. expats, and generates entrepreneurial market opportunities.
"""

import re
from typing import Dict, Any, List
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import PROBLEM_KEYWORDS, MEXICAN_SLANG_MAP, TARGET_CITIES

class MexicanSynthesisAgent:
    """
    Intelligent problem classifier and market opportunity synthesis engine.
    """

    def __init__(self):
        self.categories = PROBLEM_KEYWORDS
        self.slang_map = MEXICAN_SLANG_MAP
        self.cities = TARGET_CITIES

    def analyze_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a scraped post and produce structured intelligence.
        """
        title = post.get("title", "")
        content = post.get("content", "")
        combined_text = f"{title} {content}".lower()

        # 1. Detect City and Colonia
        detected_city, detected_colonia = self._detect_location(post, combined_text)

        # 2. Detect Slang / Modismos and Severity adjustments
        matched_slang = []
        base_urgency = 2

        for slang_term, meta in self.slang_map.items():
            terms = [t.strip() for t in slang_term.split("/")]
            for t in terms:
                if t in combined_text:
                    matched_slang.append({"term": t, "meaning": meta["meaning"]})
                    base_urgency = max(base_urgency, meta.get("severity", 2))
                    break

        # 3. Categorize Problem
        category, confidence = self._categorize_text(combined_text)

        # 4. Audience Detection (Local vs Expat vs Both)
        audience = self._detect_audience(post, combined_text)

        # 5. Urgency Calculation
        urgency = self._calculate_urgency(combined_text, base_urgency)

        # 6. Sentiment Detection
        sentiment = self._detect_sentiment(combined_text)

        # 7. Extract Core Problem & Workaround / Solution
        problem_summary = self._extract_problem_summary(title, content)
        solution_found = self._extract_solution(combined_text)

        # 8. Generate Market Opportunity / Business Hypothesis
        market_opportunity = self._generate_market_opportunity(category, problem_summary, audience, detected_city)

        return {
            "title": post.get("title", ""),
            "content": post.get("content", ""),
            "source_platform": post.get("source_platform", "Unknown"),
            "source_url": post.get("source_url", ""),
            "city": detected_city,
            "colonia": detected_colonia,
            "category": category,
            "confidence": confidence,
            "audience": audience,
            "urgency": urgency,
            "sentiment": sentiment,
            "matched_slang": matched_slang,
            "problem_summary": problem_summary,
            "solution_found": solution_found,
            "market_opportunity": market_opportunity,
            "timestamp": post.get("timestamp", "")
        }

    def _detect_location(self, post: Dict[str, Any], text: str):
        # First check post metadata
        meta_city = post.get("city", "")
        if meta_city and meta_city != "National":
            # Still scan for colonia
            for city_name, colonias in self.cities.items():
                if city_name.lower().startswith(meta_city.lower()[:5]):
                    for col in colonias:
                        if col.lower() in text:
                            return city_name, col
            return meta_city, "General / Undefined"

        # Search for colonia mentions
        for city_name, colonias in self.cities.items():
            for col in colonias:
                if col.lower() in text:
                    return city_name, col

        # Search for city mentions
        if "mérida" in text or "merida" in text or "yucatán" in text or "yucatan" in text or "japay" in text or "progreso" in text:
            return "Mérida & Yucatán", "General"
        if "cdmx" in text or "ciudad de méxico" in text or "df" in text or "distrito federal" in text:
            return "Mexico City (CDMX)", "General"
        if "guadalajara" in text or "gdl" in text or "zapopan" in text:
            return "Guadalajara (GDL)", "General"
        if "monterrey" in text or "mty" in text or "san pedro" in text:
            return "Monterrey (MTY)", "General"
        if "querétaro" in text or "queretaro" in text:
            return "Querétaro", "General"
        if "puebla" in text:
            return "Puebla", "General"

        return meta_city if meta_city else "Mexico City (CDMX)", "General"

    def _categorize_text(self, text: str):
        scores = {cat: 0 for cat in self.categories}
        
        # Check specific keywords
        for cat, keywords in self.categories.items():
            for kw in keywords:
                if kw.lower() in text:
                    # Boost exact phrase matches
                    scores[cat] += len(kw.split())

        # Additional domain heuristics
        if any(w in text for w in ["plomero", "albañil", "electricista", "gotera", "boiler", "maestro"]):
            scores["Home Maintenance & Trades"] += 4
        if any(w in text for w in ["sat", "rfc", "e.firma", "imss", "visa", "inm", "licencia", "trámite"]):
            scores["Bureaucracy & GovTech"] += 4
        if any(w in text for w in ["casero", "depósito", "renta", "póliza jurídica", "fiador", "inmobiliaria", "arrendamiento"]):
            scores["Housing & Real Estate"] += 4
        if any(w in text for w in ["estafa", "spei", "fraude", "bazar", "transa", "mercado libre", "lady multitask"]):
            scores["Marketplaces & Consumer Scams"] += 4
        if any(w in text for w in ["expat", "foreigner", "temporary resident", "without rfc", "gringo", "nomad"]):
            scores["Expat & Relocation Friction"] += 4
        if any(w in text for w in ["luz", "agua", "cfe", "sacmex", "apagón", "tandeo", "pipa", "bache", "alumbrado"]):
            scores["Infrastructure & Utilities"] += 4

        top_cat = max(scores, key=scores.get)
        if scores[top_cat] == 0:
            return "Infrastructure & Utilities", 0.5
        
        confidence = min(0.98, 0.6 + (scores[top_cat] * 0.08))
        return top_cat, round(confidence, 2)

    def _detect_audience(self, post: Dict[str, Any], text: str) -> str:
        # Check source metadata first
        meta_aud = post.get("audience", "")
        if meta_aud in ["Expat", "Local"]:
            return meta_aud

        # Check language and expat-specific indicators
        english_words = ["landlord", "expat", "foreigner", "residency", "deposit", "visa", "sat", "temporary resident", "inm"]
        eng_count = sum(1 for w in english_words if w in text)
        
        if eng_count >= 2 or "expat" in text or "gringo" in text or "foreigner" in text:
            return "Expat"
        if "vecinos" in text or "colonia" in text or "albañil" in text or "tandeo" in text or "profeco" in text:
            return "Local"
        return "Both"

    def _calculate_urgency(self, text: str, base_urgency: int) -> int:
        urgency = base_urgency
        high_urgency_words = ["urgente", "emergencia", "estafa", "sin agua", "sin luz", "días sin", "peligro", "inundación", "fraude", "asaltaron", "desesperado"]
        for w in high_urgency_words:
            if w in text:
                urgency = max(urgency, 4)
                break
        if "llevamos 3 días" in text or "llevamos una semana" in text or "estafa de miles" in text:
            urgency = 5
        return min(5, urgency)

    def _detect_sentiment(self, text: str) -> str:
        if any(w in text for w in ["estafa", "rateros", "transas", "hijos de", "porquería", "coraje", "pésimo"]):
            return "Angry / Outraged"
        if any(w in text for w in ["desesperado", "urgente", "ayuda por favor", "ya no sé qué hacer", "alguien que me diga"]):
            return "Frustrated / Seeking Help"
        if any(w in text for w in ["ojo vecinos", "tengan cuidado", "alerta", "aviso"]):
            return "Alerting Community"
        if any(w in text for w in ["busco recomendación", "alguien conoce", "recomienden"]):
            return "Inquiring / Service Gap"
        return "Informative / Seeking Workaround"

    def _extract_problem_summary(self, title: str, content: str) -> str:
        if title and len(title) > 15:
            return title.strip()
        # Fallback to first sentence of content
        sentences = re.split(r'[.!?\n]', content)
        for s in sentences:
            if len(s.strip()) > 20:
                return s.strip()[:140]
        return "Reported consumer friction in Mexican metropolitan zone."

    def _extract_solution(self, text: str) -> str:
        solution_triggers = ["lo resolví", "la solución fue", "me funcionó", "el truco es", "recomiendo ir a", "vayan temprano", "pueden usar"]
        for t in solution_triggers:
            idx = text.find(t)
            if idx != -1:
                snippet = text[idx:idx+150]
                return snippet.strip().capitalize()
        return "No confirmed workaround mentioned yet; community searching for solution."

    def _generate_market_opportunity(self, category: str, problem: str, audience: str, city: str) -> Dict[str, str]:
        """
        Synthesize problem into a direct business / tech solution hypothesis.
        """
        hypotheses = {
            "Infrastructure & Utilities": {
                "venture_concept": "Hyperlocal Water & Power Tracking with On-Demand Tanker Dispatch",
                "solution_summary": f"A mobile platform mapping real-time CFE/Sacmex outages by colonia in {city}, offering group orders for verified water trucks (pipas) with transparent standardized pricing."
            },
            "Bureaucracy & GovTech": {
                "venture_concept": "GovTech Concierge & Automated Appointment Hunter (SAT/IMSS/INM)",
                "solution_summary": "An automated bot and legal-tech service that tracks SAT e.firma and INM visa appointment cancellations 24/7, booking legal slots with pre-filled document validation."
            },
            "Home Maintenance & Trades": {
                "venture_concept": "Guaranteed Home-Services Escrow Network (Vetted Maestros)",
                "solution_summary": f"An 'Angi/TaskRabbit for Mexico' holding client payments in escrow until plumbing/electrical jobs pass photographic proof, eliminating contractor abandonments."
            },
            "Housing & Real Estate": {
                "venture_concept": "Póliza Jurídica & Fiador Replacement Protocol",
                "solution_summary": "A fintech guarantor service backed by underwriting that replaces the archaic Mexican 'fiador con bien raíz' deed requirement for foreigners and younger locals."
            },
            "Marketplaces & Consumer Scams": {
                "venture_concept": "Escrow P2P Marketplace Verification (Safe SPEI Protocol)",
                "solution_summary": "A peer-to-peer transaction protection layer for Facebook Bazar and local marketplace groups, freezing SPEI funds until in-person buyer inspection."
            },
            "Expat & Relocation Friction": {
                "venture_concept": "Bilingual Soft-Landing & Financial Onboarding Engine",
                "solution_summary": f"All-in-one expat relocation stack managing Mexican bank accounts without RFC, local SIMs, legal lease reviews, and verified bilingual contractors in {city}."
            }
        }
        
        # Check for Merida & Yucatan specific opportunities
        if "mérida" in city.lower() or "yucatán" in city.lower() or "yucatan" in city.lower():
            yucatan_hypotheses = {
                "Infrastructure & Utilities": {
                    "venture_concept": "Yucatán Limestone Water Descaling & CFE Summer Cooling Optimizer",
                    "solution_summary": "Household ionization water softener hardware and automated CFE tariff monitor mitigating severe JAPAY calcification (sarro) and summer AC bill shocks in Mérida."
                },
                "Housing & Real Estate": {
                    "venture_concept": "Yucatán Ejido Title Due Diligence & Anti-Terrenos de Inversión Scanner",
                    "solution_summary": "A proptech title search and aerial verification registry exposing fraudulent jungle subdivisions (terrenos de inversión sin servicios) for local and expat buyers."
                },
                "Bureaucracy & GovTech": {
                    "venture_concept": "INAH Colonial Heritage Permit Concierge for Mérida Centro",
                    "solution_summary": "Specialized legal-tech platform streamlining historic façade and interior architectural approvals with INAH Yucatán, reducing renovation shutdowns from 18 months to weeks."
                },
                "Home Maintenance & Trades": {
                    "venture_concept": "Anti-Salitre Tropical Barrier & Certified Minisplit Network",
                    "solution_summary": "Vetted network providing chemical barrier injections against Yucatán saltpeter wall decay and guaranteed 24/7 HVAC air conditioning maintenance during heatwaves."
                },
                "Expat & Relocation Friction": {
                    "venture_concept": "Yucatán Coastal Fideicomiso & Bilingual Soft-Landing Stack",
                    "solution_summary": "Turnkey legal bank trust (fideicomiso) structuring for foreign buyers in Progreso and Mérida, bilingual escrow, and utility onboarding."
                }
            }
            if category in yucatan_hypotheses:
                return yucatan_hypotheses[category]

        return hypotheses.get(category, {
            "venture_concept": "Localized Consumer Resolution Platform",
            "solution_summary": f"A digital marketplace addressing unmet consumer service demand in {city}."
        })
