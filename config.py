"""
Configuration file for MexConsumerPulse Market Research & Autonomous Agent Pipeline.
Defines cities, colonias, search keywords, categories, and target platforms.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
AUTH_DIR = DATA_DIR / "auth_state"
EXPORTS_DIR = DATA_DIR / "exports"
REPORTS_DIR = BASE_DIR / "reports" / "daily_reports"
DB_PATH = DATA_DIR / "mexico_consumer_insights.db"

for p in [DATA_DIR, AUTH_DIR, EXPORTS_DIR, REPORTS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Target Cities and Key Colonias / Neighborhoods
TARGET_CITIES = {
    "Mexico City (CDMX)": [
        "Condesa", "Roma Norte", "Roma Sur", "Polanco", "Juárez", "Cuauhtémoc",
        "Coyoacán", "Del Valle", "Narvarte", "San Pedro de los Pinos", "Santa Fe",
        "Satélite", "Lindavista", "Tlalpan", "Xochimilco", "Escandón", "San Rafael"
    ],
    "Guadalajara (GDL)": [
        "Americana", "Chapultepec", "Providencia", "Ladrón de Guevara", 
        "Zapopan Centro", "Puerta de Hierro", "Tlaquepaque", "Ciudad Granja"
    ],
    "Monterrey (MTY)": [
        "San Pedro Garza García", "Valle Oriente", "Cumbres", "Tecnológico",
        "Mitras", "Contry", "San Jerónimo", "Santa Catarina", "Apodaca"
    ],
    "Querétaro": [
        "Juriquilla", "Centro Histórico", "El Campanario", "Milenio III", "Zibatá"
    ],
    "Puebla": [
        "Angelópolis", "La Paz", "Centro", "Cholula", "Lomas de Angelópolis"
    ],
    "Mérida & Yucatán": [
        "Centro Histórico (Santiago, Santa Ana, Santa Lucía)", "García Ginerés", "Itzimná",
        "Montebello", "Altabrisa", "Temozón Norte", "Montes de Amé", "Chuburná",
        "Campestre", "Las Américas Mérida", "Caucel", "Progreso", "Cholul", "Conkal"
    ],
    "Puerto Vallarta / Riviera Nayarit": [
        "Zona Romántica", "Marina Vallarta", "Fluvial", "Bucerías", "Sayulita"
    ],
    "Playa del Carmen / Tulum / Cancún": [
        "Playacar", "Centro Playa", "La Veleta", "Aldea Zama", "Zona Hotelera Cancún"
    ]
}

# Subreddits for Local & Expat Consumer Discussions
TARGET_SUBREDDITS = [
    # Mexican Local Subreddits
    {"name": "MexicoCity", "city": "Mexico City (CDMX)", "audience": "Both"},
    {"name": "Guadalajara", "city": "Guadalajara (GDL)", "audience": "Both"},
    {"name": "Monterrey", "city": "Monterrey (MTY)", "audience": "Both"},
    {"name": "merida", "city": "Mérida & Yucatán", "audience": "Both"},
    {"name": "Yucatan", "city": "Mérida & Yucatán", "audience": "Both"},
    {"name": "mexico", "city": "National", "audience": "Local"},
    {"name": "AskMexico", "city": "National", "audience": "Both"},
    # Expat / Foreigner Subreddits
    {"name": "mexicoexpats", "city": "National", "audience": "Expat"},
    {"name": "expats", "city": "National", "audience": "Expat", "filter_keyword": "Mexico"},
    {"name": "digitalnomad", "city": "National", "audience": "Expat", "filter_keyword": "Mexico"}
]

# Targeted Facebook Groups (Curated list with search queries & identifiers)
FACEBOOK_TARGET_GROUPS = [
    # Neighborhood / Vecinos groups
    {"name": "Vecinos de la Condesa", "city": "Mexico City (CDMX)", "type": "vecinos", "url": "https://www.facebook.com/groups/vecinosdelacondesa"},
    {"name": "Vecinos Roma Norte y Sur", "city": "Mexico City (CDMX)", "type": "vecinos", "url": "https://www.facebook.com/groups/vecinosromanorte"},
    {"name": "Vecinos de Satélite", "city": "Mexico City (CDMX)", "type": "vecinos", "url": "https://www.facebook.com/groups/vecinosdesatelite"},
    {"name": "Vecinos Providencia GDL", "city": "Guadalajara (GDL)", "type": "vecinos", "url": "https://www.facebook.com/groups/vecinosprovidenciagdl"},
    {"name": "Vecinos San Pedro Garza García", "city": "Monterrey (MTY)", "type": "vecinos", "url": "https://www.facebook.com/groups/vecinosspgg"},
    {"name": "Vecinos Mérida Centro y Norte", "city": "Mérida & Yucatán", "type": "vecinos", "url": "https://www.facebook.com/groups/vecinosmerida"},
    {"name": "Quejas y Servicios Mérida / Yucatán", "city": "Mérida & Yucatán", "type": "vecinos", "url": "https://www.facebook.com/groups/quejasmerida"},
    # Bazar / Marketplace
    {"name": "Bazar Coyoacán", "city": "Mexico City (CDMX)", "type": "bazar", "url": "https://www.facebook.com/groups/bazarcoyoacan"},
    {"name": "Bazar Polanco", "city": "Mexico City (CDMX)", "type": "bazar", "url": "https://www.facebook.com/groups/bazarpolanco"},
    {"name": "Bazar Mérida Norte y Altabrisa", "city": "Mérida & Yucatán", "type": "bazar", "url": "https://www.facebook.com/groups/bazarmeridanorte"},
    # Expat Communities
    {"name": "Foreigners & Expats in Mexico City (CDMX)", "city": "Mexico City (CDMX)", "type": "expat", "url": "https://www.facebook.com/groups/expatscdmx"},
    {"name": "Expats in Guadalajara", "city": "Guadalajara (GDL)", "type": "expat", "url": "https://www.facebook.com/groups/expatsgdl"},
    {"name": "Mérida Expats & Foreigners Community", "city": "Mérida & Yucatán", "type": "expat", "url": "https://www.facebook.com/groups/meridaexpats"}
]

# X (Twitter) Accounts and Hashtags Monitored
TWITTER_MONITORS = {
    "official_handles": [
        "@SATMX", "@CFEmx", "@CFE_Contigo", "@SacmexCDMX", "@MetroCDMX",
        "@AtencionCDMX", "@Profeco", "@GobCDMX", "@AytoGDL", "@mtygob",
        "@AyuntaMerida", "@JAPAYOficial", "@GobYucatan"
    ],
    "complaint_queries": [
        "SAT no funciona",
        "CFE sin luz",
        "Sacmex sin agua",
        "JAPAY sin agua Mérida",
        "CFE Mérida apagón",
        "salitre Mérida humedad",
        "terrenos de inversión estafa Yucatán",
        "fuga de agua CDMX",
        "estafa inmobiliaria",
        "poliza juridica fraude",
        "corte de agua Guadalajara",
        "corte de luz Monterrey"
    ],
    "hashtags": [
        "#CDMX", "#AtencionCiudadana", "#CFE", "#SAT", "#FugaDeAgua", "#GDL", "#Monterrey", "#Merida", "#Yucatan", "#JAPAY"
    ]
}

# Categorized Problem Keywords
PROBLEM_KEYWORDS = {
    "Infrastructure & Utilities": [
        "sin luz", "se fue la luz", "CFE", "apagón", "recibo de luz alto", "tarifa cfe yucatán",
        "sin agua", "no cae agua", "tandeo", "pipa", "Sacmex", "JAPAY", "fuga de agua",
        "sarro", "sarro en tuberías", "bomba de agua quemada", "fuga de gas", "tanque estacionario",
        "sin internet", "falla totalplay", "telmex no sirve", "baches", "alumbrado público"
    ],
    "Bureaucracy & GovTech": [
        "citas SAT", "SAT no funciona", "RFC", "e.firma", "portal del SAT caído",
        "cita IMSS", "clínica IMSS", "INM", "residencia temporal", "residencia permanente",
        "trámite de visa", "licencia digital", "verificación vehicular", "predial",
        "pago de tenencia", "apostilla", "acta de nacimiento", "permiso INAH mérida", "inah clausura"
    ],
    "Home Maintenance & Trades": [
        "recomienden plomero", "maestro albañil", "electricista de confianza",
        "reparación de boiler", "humedad", "gotera", "impermeabilizante", "salitre",
        "salitre en paredes", "anti salitre", "suavizador de agua", "clima no enfría",
        "mantenimiento minisplit", "cerrajero urgente", "fumigación chinches", "albañil me estafó",
        "obra inconclusa", "carpintero"
    ],
    "Housing & Real Estate": [
        "casero no regresa depósito", "póliza jurídica abusiva", "piden fiador con bienes raíces",
        "aval en cdmx", "subieron la renta", "gentrificación", "contrato de arrendamiento",
        "inmobiliaria fraude", "terrenos de inversión", "estafa ejidal yucatán", "ruido vecinos",
        "fiestas en el edificio", "estafa renta"
    ],
    "Marketplaces & Consumer Scams": [
        "estafa marketplace", "fraude transferencia spei", "paquete no llegó",
        "cobro indebido", "profeco queja", "producto pirata", "Lady Multitask queja",
        "técnico cobró y no vino", "terrenos fantasmas mérida"
    ],
    "Expat & Relocation Friction": [
        "open bank account without rfc", "intercam", "bbva foreigner",
        "fiador alternative", "temporary resident renewal", "english speaking doctor",
        "apostilled documents", "tax residency sat", "mexico rent deposit refund",
        "safety condesa roma", "scam foreigner rental", "merida expat trust fideicomiso",
        "inah permits expat renovation"
    ]
}

# Mexican Slang & Modismos Lexicon for NLP Classification
MEXICAN_SLANG_MAP = {
    "se me fue la luz": {"meaning": "Power outage / Electrical failure", "severity": 4, "category": "Infrastructure & Utilities"},
    "no hay agua / no cae agua / estamos secos": {"meaning": "Water shortage / Cutoff", "severity": 4, "category": "Infrastructure & Utilities"},
    "tandeo": {"meaning": "Rationed water schedule", "severity": 3, "category": "Infrastructure & Utilities"},
    "sarro / sarro de japay": {"meaning": "Severe calcium / limestone water hardness clogging pipes and boilers in Yucatan", "severity": 4, "category": "Infrastructure & Utilities"},
    "salitre / salitre en la pared": {"meaning": "Saltpeter & tropical efflorescence destroying concrete walls in Merida", "severity": 3, "category": "Home Maintenance & Trades"},
    "bochorno insoportable": {"meaning": "Oppressive tropical heat causing health and power strain in Yucatan", "severity": 3, "category": "Infrastructure & Utilities"},
    "terrenos de inversión / ejidal": {"meaning": "Real estate speculative land subdivision scam in Yucatan jungle", "severity": 5, "category": "Housing & Real Estate"},
    "clausura del inah": {"meaning": "Federal historical institute halting colonial home renovation in Merida Centro", "severity": 4, "category": "Bureaucracy & GovTech"},
    "maestro": {"meaning": "Independent contractor / Handyman / Builder", "severity": 2, "category": "Home Maintenance & Trades"},
    "transa / me transaron": {"meaning": "Scammed / Swindled / Defrauded", "severity": 5, "category": "Marketplaces & Consumer Scams"},
    "me hicieron de chivo los tamales": {"meaning": "Cheated or deceived in transaction", "severity": 4, "category": "Marketplaces & Consumer Scams"},
    "trámite engorroso": {"meaning": "Tedious bureaucracy barrier", "severity": 3, "category": "Bureaucracy & GovTech"},
    "vendiendo citas del SAT": {"meaning": "Corruption / Black market for tax authority appointments", "severity": 5, "category": "Bureaucracy & GovTech"},
    "sin luz otra vez CFE": {"meaning": "Chronic electrical grid instability", "severity": 4, "category": "Infrastructure & Utilities"},
    "póliza jurídica": {"meaning": "Rental insurance legal policy requirement (major barrier for expats and young locals)", "severity": 3, "category": "Housing & Real Estate"},
    "fiador con bien raíz": {"meaning": "Requirement of real estate deed guarantor in same city to rent an apartment", "severity": 4, "category": "Housing & Real Estate"},
    "pipa de agua": {"meaning": "Emergency water tanker truck necessitated by dry pipes", "severity": 4, "category": "Infrastructure & Utilities"},
    "bachezote": {"meaning": "Severe street pothole causing vehicle damage", "severity": 3, "category": "Infrastructure & Utilities"},
    "cobro fantasma": {"meaning": "Phantom / fraudulent utility billing spike", "severity": 4, "category": "Infrastructure & Utilities"}
}
