"""
WhatsApp 'Chat de Vecinos' Ingestion & Community Parser Agent.
Handles raw chat exports (.txt / .json) from Mexican neighborhood WhatsApp groups,
cleans phone numbers and user headers, and routes messages into the compliance and synthesis pipeline.
"""

import sys
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import PROBLEM_KEYWORDS
from agents.compliance_agent import MexicanComplianceAgent
from agents.synthesis_agent import MexicanSynthesisAgent
from agents.dataset_manager import DatasetManager

class WhatsAppVecinosAgent:
    """
    Autonomous parser for WhatsApp 'Chat de Vecinos' exports.
    Extracts hyper-local infrastructure outages, handyman recommendations,
    and building maintenance issues while guaranteeing 100% PII stripping.
    """

    def __init__(self):
        self.compliance_agent = MexicanComplianceAgent()
        self.synthesis_agent = MexicanSynthesisAgent()
        self.db = DatasetManager()

        # Regex for WhatsApp export lines:
        # [14/10/26, 18:04:12] +52 55 1234 5678: Text
        # or 10/14/26, 6:04 PM - John Doe: Text
        self.msg_header_pattern = re.compile(
            r'^(?:\[?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s+[AP]M)?)\]?\s*[-:]?\s*)([^:]+):\s*(.*)$',
            re.IGNORECASE
        )

    def parse_chat_text(self, raw_text: str, group_name: str = "Chat de Vecinos", city: str = "Mexico City (CDMX)") -> List[Dict[str, Any]]:
        """
        Parses raw WhatsApp chat export text and extracts actionable consumer problems.
        """
        lines = raw_text.splitlines()
        messages = []
        current_msg = None

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            match = self.msg_header_pattern.match(line_str)
            if match:
                if current_msg:
                    messages.append(current_msg)
                
                raw_time, sender, text = match.groups()
                # Skip media omitted or system notices
                if any(sys_notice in text.lower() for sys_notice in [
                    "<media omitted>", "archivo omitido", "cambió el código de seguridad",
                    "creó el grupo", "añadió a", "salió del grupo", "los mensajes y las llamadas están cifrados"
                ]):
                    current_msg = None
                    continue

                current_msg = {
                    "raw_time": raw_time,
                    "sender": sender,
                    "text": text,
                    "group_name": group_name,
                    "city": city
                }
            else:
                # Continuation of multi-line message
                if current_msg:
                    current_msg["text"] += " " + line_str

        if current_msg:
            messages.append(current_msg)

        # Filter messages that express consumer friction or service requests
        problem_candidates = []
        for msg in messages:
            txt = msg["text"]
            # Look for consumer problem keywords or recommendation requests
            if self._is_relevant_community_issue(txt):
                problem_candidates.append(msg)

        # Process through compliance and synthesis
        processed_problems = []
        for cand in problem_candidates:
            # 1. Compliance Scrubbing
            raw_record = {
                "title": f"WhatsApp Vecinos: {cand['text'][:90]}...",
                "content": cand["text"],
                "author": cand["sender"],
                "source_platform": f"WhatsApp ({cand['group_name']})",
                "source_url": "whatsapp://chat/vecinos",
                "city": cand["city"],
                "audience": "Local",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            sanitized = self.compliance_agent.sanitize_record(raw_record)
            analyzed = self.synthesis_agent.analyze_post(sanitized)

            is_new = self.db.insert_problem(analyzed)
            processed_problems.append(analyzed)

        self.db.log_agent_run(
            agent_name="WhatsAppVecinosAgent",
            status="SUCCESS",
            collected=len(messages),
            inserted=len(processed_problems),
            details=f"Parsed '{group_name}' ({len(messages)} messages, {len(processed_problems)} problems extracted)."
        )

        return processed_problems

    def _is_relevant_community_issue(self, text: str) -> bool:
        t_lower = text.lower()
        if len(t_lower) < 20:
            return False

        triggers = [
            "alguien conoce", "recomiendan", "plomero", "albañil", "electricista",
            "sin agua", "no cae agua", "tandeo", "pipa", "se fue la luz", "sin luz",
            "cfe", "sacmex", "fuga", "gas", "tanque", "ruido", "seguridad", "bache",
            "estafaron", "no vino", "gotera", "impermeabilizar", "boiler", "cerradura"
        ]
        return any(trig in t_lower for trig in triggers)

    def import_sample_condesa_chat(self) -> List[Dict[str, Any]]:
        """
        Loads a sample high-fidelity WhatsApp Vecinos chat export to demonstrate the workflow.
        """
        sample_chat = """
[14/10/26, 08:15:30] +52 55 9876 5432: Buenos días vecinos de Calle Ámsterdam. ¿A ustedes les está saliendo agua en los grifos? En el edificio 42 no cae ni una gota desde anoche.
[14/10/26, 08:17:10] Vecino Juan Depto 301: Hola, aquí en el 48 tampoco cae agua de Sacmex. Hablamos a la alcaldía y dicen que hay fuga principal en Insurgentes y van a tandeo todo el fin de semana.
[14/10/26, 08:22:45] Mariana Condesa: ¿Alguien tiene el contacto de una pipa de agua particular confiable? Los del teléfono de siempre quieren cobrar $2,200 pesos por 5,000 litros y dicen que tardan 8 horas en llegar.
[14/10/26, 09:30:12] +52 55 4321 8765: Oigan vecinos, aviso urgente: no contraten a un señor que se hace llamar 'Maestro Carlos' para reparar calentadores. Nos cobró $1,500 de anticipo de refacciones y nos dejó el boiler desarmado y ya no contesta las llamadas ni WhatsApp.
[14/10/26, 11:05:00] Alberto R: ¿Alguien sabe si CFE avisó de corte de luz para hoy? En la esquina de Parras se escuchó un tronido fuerte en el transformador y varios departamentos nos quedamos a oscuras.
"""
        return self.parse_chat_text(sample_chat, group_name="Vecinos Ámsterdam Condesa", city="Mexico City (CDMX)")

if __name__ == "__main__":
    agent = WhatsAppVecinosAgent()
    problems = agent.import_sample_condesa_chat()
    print(f"Extracted {len(problems)} hyper-local consumer problems from WhatsApp Chat de Vecinos.")
