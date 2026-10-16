"""
Gemini Intelligence Agent for MexicoConsumerPulse.
Provides conversational AI Q&A, deep venture synthesis, and grounded market research
using Google's Gemini Flash / Flash-Lite models.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Load .env if present
env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.exists():
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

try:
    import google.genai as genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiCopilotAgent:
    """
    Autonomous conversational agent grounded in Mexican consumer and retail data.
    """

    CANDIDATE_MODELS = [
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-2.0-flash"
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.preferred_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite").strip()
        self.client = None
        self._init_client()

    def _init_client(self):
        if self.api_key and GENAI_AVAILABLE:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[GeminiAgent] Client initialization error: {e}")
                self.client = None

    def is_configured(self) -> bool:
        return bool(self.client and self.api_key)

    def _call_gemini_with_fallback(self, prompt: str, system_instruction: str = "") -> Dict[str, Any]:
        """
        Attempts execution across candidate flash-lite models with graceful fallback.
        """
        if not self.client:
            return {
                "success": False,
                "error": "Gemini API key is not configured or google-genai library missing.",
                "reply": "⚠️ La clave de API de Gemini no está configurada o no es válida."
            }

        # Try configured model first, then fallback models
        models_to_try = [self.preferred_model] + [m for m in self.CANDIDATE_MODELS if m != self.preferred_model]

        last_error = ""
        for model_name in models_to_try:
            try:
                config_kwargs = {}
                if system_instruction:
                    config_kwargs["system_instruction"] = system_instruction

                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(**config_kwargs) if config_kwargs else None
                )
                if response and response.text:
                    return {
                        "success": True,
                        "model_used": model_name,
                        "reply": response.text.strip()
                    }
            except Exception as e:
                err_str = str(e)
                last_error = err_str
                # If permission denied (API not enabled), break early with instructions
                if "PERMISSION_DENIED" in err_str or "has not been used in project" in err_str:
                    return {
                        "success": False,
                        "error": err_str,
                        "needs_activation": True,
                        "reply": (
                            "⚠️ **Google Gemini API Requiere Activación en tu Proyecto de Google Cloud**\n\n"
                            "Tu API Key fue reconocida exitosamente, pero la **Generative Language API** debe ser habilitada en tu consola de Google Cloud:\n\n"
                            "👉 [**Haz clic aquí para habilitar la API de Gemini en tu proyecto**](https://console.developers.google.com/apis/api/generativelanguage.googleapis.com/overview?project=807787924803)\n\n"
                            "*(O si prefieres, puedes generar una API Key directa con la API ya activada en [Google AI Studio](https://aistudio.google.com/app/apikey)).*"
                        )
                    }
                continue

        return {
            "success": False,
            "error": last_error,
            "reply": f"Lo sentimos, hubo un error al contactar a Gemini: {last_error}"
        }

    def chat_with_copilot(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        context_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Grounded conversational research session.
        """
        system_instruction = (
            "Eres el Asistente de Inteligencia de Mercado y Estrategia de MexConsumerPulse. "
            "Eres un analista senior de investigación de mercado y capital de riesgo especializado en México "
            "(CDMX, Mérida y Yucatán, Monterrey, Guadalajara, Querétaro, Puebla). "
            "Tienes profundo conocimiento de:\n"
            "- Fricciones de infraestructura mexicana (apagones y tarifas DAC de CFE, sarro kárstico de JAPAY, cortes del Cutzamala de SACMEX, humedad costera).\n"
            "- Modismos y expresiones culturales mexicanas (broncas, transas, jineteo, pipas, tandas, fayuca).\n"
            "- Vacíos de productos y arbitraje comercial transfronterizo (NOMs, COFEPRIS, retención aduanal, 'traer del gabacho').\n"
            "- Mercado Libre México (tendencias de ventas 'Hot Products' y reseñas negativas de 1 a 3 estrellas por fallas locales).\n"
            "Responde de forma ejecutiva, concisa, profesional y con mentalidad de negocio e inversión. "
            "Si el usuario pregunta en español, responde en español; si pregunta en inglés, responde en inglés."
        )

        # Build context prompt
        context_text = ""
        if context_data:
            hot_prods = context_data.get("hot_products", [])[:4]
            problem_prods = context_data.get("problem_products", [])[:4]
            voids = context_data.get("product_voids", [])[:4]

            context_text = "\n\n### CONTEXTO EN TIEMPO REAL DE LA BASE DE DATOS DE MÉXICO:\n"
            if hot_prods:
                context_text += "🔥 Top Productos en Mercado Libre (Ventas en Alza):\n"
                for p in hot_prods:
                    context_text += f"- {p.get('product_name')} (${p.get('price_mxn', 0):,} MXN) | {p.get('demand_growth', '')} | Éxito: {p.get('adoption_driver', '')}\n"

            if problem_prods:
                context_text += "\n⚠️ Productos con Fallas Críticas (1-3 Estrellas):\n"
                for p in problem_prods:
                    context_text += f"- {p.get('product_name')} | Falla: {p.get('failure_mode', '')} | Cita de comprador: \"{p.get('sample_buyer_review', '')}\"\n"

            if voids:
                context_text += "\n🎁 Vacíos Comerciales / 'Ojalá Vendieran Esto en México':\n"
                for v in voids:
                    context_text += f"- {v.get('product_name')} (Origen: {v.get('origin_country')}) | Causa: {v.get('why_missing', '')}\n"

        prompt = f"{context_text}\n\nPregunta del usuario:\n{message}"
        return self._call_gemini_with_fallback(prompt, system_instruction)

    def deep_venture_synthesis(
        self,
        problem_title: str,
        problem_content: str,
        city: str,
        category: str
    ) -> Dict[str, Any]:
        """
        Generates an investor-grade venture thesis and unit economics.
        """
        system_instruction = (
            "Eres un inversionista de Venture Capital y fundador serial en México. "
            "Tu tarea es transformar una queja o problema de consumo mexicano en una hipótesis de negocio escalable."
        )

        prompt = (
            f"Analiza la siguiente fricción del consumidor mexicano:\n"
            f"- Título: {problem_title}\n"
            f"- Detalle: {problem_content}\n"
            f"- Ciudad/Región: {city}\n"
            f"- Categoría: {category}\n\n"
            f"Genera un reporte breve estructurado con:\n"
            f"1. Nombre Propuesto del Startup / Producto\n"
            f"2. Solución Diferenciada (Adaptada a México)\n"
            f"3. Modelo de Monetización y Precio sugerido en MXN\n"
            f"4. Barrera Regulatoria o Logística a superar (NOM, COFEPRIS, CFE o Aduana)\n"
            f"5. Estrategia de Adquisición (Go-To-Market en {city})"
        )

        return self._call_gemini_with_fallback(prompt, system_instruction)


# Global singleton instance
gemini_copilot = GeminiCopilotAgent()
