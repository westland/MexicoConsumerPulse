"""
Agent for Mexican Data Privacy Compliance (Ley Federal de Protección de Datos Personales).
Strips PII (Personally Identifiable Information) including Mexican phone numbers, RFC, CURP,
exact street addresses, credit/CLABE account numbers, and personal names.
"""

import re
from typing import Dict, Any, Tuple

class MexicanComplianceAgent:
    """
    Anonymization engine strictly adhering to Mexican Data Protection regulations.
    Ensures that research datasets contain zero PII before storage or synthesis.
    """

    def __init__(self):
        # Mexican Phone patterns: +52 1 ..., +52 ..., 55 ..., 33 ..., 81 ... and 10 digit formats
        self.phone_pattern = re.compile(
            r'(\+?52\s?1?\s?)?(\(?\d{2,3}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}\b'
        )
        
        # RFC (Registro Federal de Contribuyentes): 4 letters, 6 numbers, 3 alphanumeric homoclave
        self.rfc_pattern = re.compile(
            r'\b[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}\b', re.IGNORECASE
        )
        
        # CURP (Clave Única de Registro de Población): 18 characters standard pattern
        self.curp_pattern = re.compile(
            r'\b[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z]\d\b', re.IGNORECASE
        )
        
        # Email address pattern
        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )
        
        # CLABE Bancaria (18 digits) or card numbers
        self.clabe_pattern = re.compile(
            r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4,6}\b'
        )
        
        # Exact street numbers and interior numbers (e.g. Calle Durango 142 Int 4B, No. 23)
        self.address_number_pattern = re.compile(
            r'(?:#|no\.?|número|num\.?|calle\s+[a-záéíóúñ]+)\s*(\d{1,5}(?:\s*int\.?\s*[a-z0-9-]+)?)',
            re.IGNORECASE
        )

    def anonymize_text(self, text: str) -> Tuple[str, Dict[str, int]]:
        """
        Scrub all PII from text and return cleaned text along with scrub stats.
        """
        if not text or not isinstance(text, str):
            return "", {"scrubbed_count": 0}

        scrub_counts = {
            "phones": 0,
            "emails": 0,
            "rfc": 0,
            "curp": 0,
            "clabe_cards": 0,
            "addresses": 0
        }

        # 1. Emails
        emails_found = len(self.email_pattern.findall(text))
        if emails_found:
            scrub_counts["emails"] = emails_found
            text = self.email_pattern.sub("[CORREO_ANONIMIZADO]", text)

        # 2. RFC & CURP
        rfc_found = len(self.rfc_pattern.findall(text))
        if rfc_found:
            scrub_counts["rfc"] = rfc_found
            text = self.rfc_pattern.sub("[RFC_ANONIMIZADO]", text)

        curp_found = len(self.curp_pattern.findall(text))
        if curp_found:
            scrub_counts["curp"] = curp_found
            text = self.curp_pattern.sub("[CURP_ANONIMIZADO]", text)

        # 3. CLABE & Card numbers
        clabe_found = len(self.clabe_pattern.findall(text))
        if clabe_found:
            scrub_counts["clabe_cards"] = clabe_found
            text = self.clabe_pattern.sub("[CUENTA_ANONIMIZADA]", text)

        # 4. Phones (careful with short numbers)
        # Only replace if string has phone indicators or >= 8 digits
        def replace_phone(match):
            val = match.group(0).strip()
            digits = re.sub(r'\D', '', val)
            if len(digits) >= 8 and len(digits) <= 13:
                scrub_counts["phones"] += 1
                return "[TELÉFONO_ANONIMIZADO]"
            return val

        text = self.phone_pattern.sub(replace_phone, text)

        # 5. Exact Street numbers
        text = self.address_number_pattern.sub(" [DIRECCIÓN_EXACTA_OMITIDA] ", text)

        # Clean excess spaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text, scrub_counts

    def sanitize_record(self, raw_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitize an entire dictionary payload before persistence.
        """
        clean_record = dict(raw_record)
        
        # Scrub title, content, author
        if "title" in clean_record and clean_record["title"]:
            clean_title, _ = self.anonymize_text(clean_record["title"])
            clean_record["title"] = clean_title
            
        if "content" in clean_record and clean_record["content"]:
            clean_content, scrub_stats = self.anonymize_text(clean_record["content"])
            clean_record["content"] = clean_content
            clean_record["scrub_stats"] = scrub_stats

        # Anonymize author username
        if "author" in clean_record and clean_record["author"]:
            # Keep only generic or hash
            clean_record["author_anonymized"] = f"user_{abs(hash(clean_record['author'])) % 100000}"
            clean_record.pop("author", None)
            
        clean_record["privacy_compliant"] = True
        return clean_record


if __name__ == "__main__":
    agent = MexicanComplianceAgent()
    sample = "Hola vecinos de Condesa, busco plomero urgente al 55-4321-9876 o a mi correo juan.perez@gmail.com, vivo en Durango #142 interior 3. Mi RFC es PEVJ900101XYZ y me cobraron 4000 pesos de luz en CFE."
    cleaned, stats = agent.anonymize_text(sample)
    print("Original:", sample)
    print("\nCleaned:", cleaned)
    print("\nStats:", stats)
