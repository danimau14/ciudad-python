# ── Constantes generales ─────────────────────────────────────────────────────
TOTAL_RONDAS    = 10
COOLDOWN        = 3
MIN_EST         = 3
MAX_EST         = 5
REGEX_NOMBRE    = r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+"
TIEMPO_PREGUNTA = 30
UMBRAL_COLAPSO  = 60
UMBRAL_ROJO     = 30

# ── Mix de preguntas por dificultad ──────────────────────────────────────────
MEZCLA_PREGUNTAS = {
    "Fácil":   {"facil": 0.60, "normal": 0.35, "dificil": 0.05},
    "Normal":  {"facil": 0.20, "normal": 0.55, "dificil": 0.25},
    "Difícil": {"facil": 0.05, "normal": 0.35, "dificil": 0.60},
}

# ── Penalizaciones  ──────────────────────────────────────────────────────────
# -5 pts por respuesta incorrecta (ronda impar)
# -10 pts por respuesta incorrecta (ronda par = doble)
DIFICULTADES = {
    "Fácil":   {"penalizacion": 5, "mult_par": 2, "estrellas": 1,
                "eventos_peso": {"positivos": 0.55, "negativos": 0.45}},
    "Normal":  {"penalizacion": 5, "mult_par": 2, "estrellas": 2,
                "eventos_peso": {"positivos": 0.40, "negativos": 0.60}},
    "Difícil": {"penalizacion": 5, "mult_par": 2, "estrellas": 3,
                "eventos_peso": {"positivos": 0.25, "negativos": 0.75}},
}

# ── Colores e iconos de indicadores ──────────────────────────────────────────
IND_COLOR = {
    "economia":        ("#fbbf24", "💰"),
    "medio_ambiente":  ("#34d399", "🌿"),
    "energia":         ("#60a5fa", "⚡"),
    "bienestar_social":("#f472b6", "❤️"),
}
IND_LABEL = {
    "economia":        "Economía",
    "medio_ambiente":  "Medio Amb.",
    "energia":         "Energía",
    "bienestar_social":"Bienestar",
}
CAT_COLOR = {
    "Python":      "#6366f1", "PSeInt":    "#8b5cf6",
    "Calculo":     "#06b6d4", "Derivadas": "#10b981",
    "Fisica MRU":  "#f59e0b", "Fisica MRUA":"#ef4444",
    "Matrices":    "#ec4899", "Logica":    "#f97316",
    "Algebra":     "#84cc16", "Estadistica":"#a78bfa",
    "Sistemas":    "#34d399",
}

# ── Decisiones ────────────────────────────────────────────────────────────────
DECISIONES = {
    "Construir fábrica":       {"emoji":"🏭","economia":18,"medio_ambiente":-15,"energia":-8, "bienestar_social":-3},
    "Crear parque natural":    {"emoji":"🌳","economia":-8,"medio_ambiente":18, "energia":-3, "bienestar_social":12},
    "Instalar paneles solares":{"emoji":"☀️","economia":-12,"medio_ambiente":12,"energia":22, "bienestar_social":-2},
    "Construir escuelas":      {"emoji":"🏫","economia":-12,"medio_ambiente":-2,"energia":-6, "bienestar_social":22},
    "Ampliar autopistas":      {"emoji":"🛣️","economia":12, "medio_ambiente":-18,"energia":-12,"bienestar_social":-5},
    "Agricultura urbana":      {"emoji":"🌱","economia":6,  "medio_ambiente":12, "energia":4,  "bienestar_social":10},
    "Mejorar hospitales":      {"emoji":"🏥","economia":-18,"medio_ambiente":-2, "energia":-6, "bienestar_social":28},
    "Planta de carbón":        {"emoji":"⚫","economia":22, "medio_ambiente":-25,"energia":28, "bienestar_social":-10},
}

# ── Eventos ───────────────────────────────────────────────────────────────────
EVENTOS_NEGATIVOS = [
    {"nombre":"Tormenta devastadora",    "indicador":"medio_ambiente",  "valor":-14},
    {"nombre":"Pandemia regional",       "indicador":"bienestar_social","valor":-16},
    {"nombre":"Apagón masivo",           "indicador":"energia",         "valor":-14},
    {"nombre":"Recesión económica",      "indicador":"economia",        "valor":-14},
    {"nombre":"Incendio forestal",       "indicador":"medio_ambiente",  "valor":-18},
    {"nombre":"Sequía prolongada",       "indicador":"medio_ambiente",  "valor":-12},
    {"nombre":"Crisis industrial",       "indicador":"economia",        "valor":-12},
    {"nombre":"Inundación urbana",       "indicador":"bienestar_social","valor":-13},
    {"nombre":"Fallo de infraestructura","indicador":"energia",         "valor":-16},
    {"nombre":"Brote de enfermedad",     "indicador":"bienestar_social","valor":-12},
]
EVENTOS_POSITIVOS = [
    {"nombre":"Boom económico",         "indicador":"economia",        "valor":10},
    {"nombre":"Ahorro energético",      "indicador":"energia",         "valor": 9},
    {"nombre":"Gran cosecha",           "indicador":"medio_ambiente",  "valor": 8},
    {"nombre":"Festival cultural",      "indicador":"bienestar_social","valor":10},
    {"nombre":"Inversión extranjera",   "indicador":"economia",        "valor":12},
    {"nombre":"Beca educativa masiva",  "indicador":"bienestar_social","valor": 9},
    {"nombre":"Energía renovable bonus","indicador":"energia",         "valor": 8},
]
EVENTOS = EVENTOS_NEGATIVOS + EVENTOS_POSITIVOS

# ── Atributos comprables con estrellas ────────────────────────────────────────
ATRIBUTOS = {
    "escudo_ciudad":      {"emoji":"🛡️","nombre":"Escudo de Ciudad",
                           "desc":"Reduce 50% impacto de eventos negativos esta ronda.",
                           "costo":30,"tipo":"ronda"},
    "prot_economia":      {"emoji":"💰","nombre":"Prot. Economía",
                           "desc":"Ignora la penalización en Economía esta ronda.",
                           "costo":10,"tipo":"ronda"},
    "prot_ambiente":      {"emoji":"🌿","nombre":"Prot. Ambiente",
                           "desc":"Ignora la penalización en Medio Ambiente esta ronda.",
                           "costo":15,"tipo":"ronda"},
    "prot_energia":       {"emoji":"⚡","nombre":"Prot. Energía",
                           "desc":"Ignora la penalización en Energía esta ronda.",
                           "costo":15,"tipo":"ronda"},
    "prot_bienestar":     {"emoji":"❤️","nombre":"Prot. Bienestar",
                           "desc":"Ignora la penalización en Bienestar esta ronda.",
                           "costo":15,"tipo":"ronda"},
    "segunda_oportunidad":{"emoji":"🔄","nombre":"2ª Oportunidad",
                           "desc":"Permite responder de nuevo si fallas esta pregunta.",
                           "costo":20,"tipo":"pregunta"},
    "tiempo_extra":       {"emoji":"⏱️","nombre":"Tiempo Extra",
                           "desc":"Añade +15 segundos al cronómetro de la pregunta.",
                           "costo":12,"tipo":"pregunta"},
    "doble_efecto":       {"emoji":"✨","nombre":"Doble Efecto",
                           "desc":"Duplica los efectos positivos de la decisión elegida.",
                           "costo":25,"tipo":"ronda"},
}

# ── Misiones ─────────────────────────────────────────────────────────────────
MISIONES = [
    {"id":"m01","nombre":"Primera Partida", "desc":"Completa tu primera partida.",
     "recompensa":2,"dif":"todas","tipo":"partidas","meta":1},
    {"id":"m02","nombre":"Racha de 3",      "desc":"Responde 3 preguntas seguidas correctamente.",
     "recompensa":3,"dif":"todas","tipo":"racha","meta":3},
    {"id":"m03","nombre":"Racha de 5",      "desc":"Responde 5 preguntas seguidas correctamente.",
     "recompensa":5,"dif":"todas","tipo":"racha","meta":5},
    {"id":"m04","nombre":"Ciudad Verde",    "desc":"Termina con Medio Ambiente > 70.",
     "recompensa":4,"dif":"todas","tipo":"indicador","ind":"medio_ambiente","meta":70},
    {"id":"m05","nombre":"Economía Próspera","desc":"Termina con Economía > 75.",
     "recompensa":4,"dif":"todas","tipo":"indicador","ind":"economia","meta":75},
    {"id":"m06","nombre":"Sin Colapso",     "desc":"Completa 10 rondas sin que ningún indicador llegue a rojo.",
     "recompensa":6,"dif":"todas","tipo":"sin_rojo","meta":1},
    {"id":"m07","nombre":"Victoria Fácil",  "desc":"Gana una partida en dificultad Fácil.",
     "recompensa":3,"dif":"Fácil","tipo":"victoria","meta":1},
    {"id":"m08","nombre":"Victoria Normal", "desc":"Gana una partida en dificultad Normal.",
     "recompensa":5,"dif":"Normal","tipo":"victoria","meta":1},
    {"id":"m09","nombre":"Victoria Difícil","desc":"Gana una partida en dificultad Difícil.",
     "recompensa":8,"dif":"Difícil","tipo":"victoria","meta":1},
    {"id":"m10","nombre":"Experto",         "desc":"Responde 8 preguntas correctas en una partida.",
     "recompensa":5,"dif":"todas","tipo":"correctas","meta":8},
    {"id":"m11","nombre":"Ciudad Perfecta", "desc":"Todos los indicadores > 60 al final.",
     "recompensa":10,"dif":"todas","tipo":"todos_sobre","meta":60},
    {"id":"m12","nombre":"Decisivo",        "desc":"Usa todas las decisiones disponibles en una partida.",
     "recompensa":6,"dif":"todas","tipo":"decisiones_usadas","meta":8},
]

# ── Logros ─────────────────────────────────────────────────────────────────
LOGROS = [
    {"id":"l01","emoji":"🏆","nombre":"Primera Victoria",         "tipo":"victoria",         "dif":"todas", "meta":1},
    {"id":"l02","emoji":"⚡","nombre":"Maestro del Normal",       "tipo":"victoria",         "dif":"Normal","meta":1},
    {"id":"l03","emoji":"🔥","nombre":"Leyenda Difícil",          "tipo":"victoria",         "dif":"Difícil","meta":1},
    {"id":"l04","emoji":"✅","nombre":"Académico",                "tipo":"correctas_partida","dif":"todas", "meta":8},
    {"id":"l05","emoji":"💯","nombre":"Perfeccionista",           "tipo":"correctas_partida","dif":"todas", "meta":10},
    {"id":"l06","emoji":"🌱","nombre":"Ecologista",               "tipo":"indicador_fin",    "dif":"todas", "ind":"medio_ambiente","meta":80},
    {"id":"l07","emoji":"💰","nombre":"Capitalista",              "tipo":"indicador_fin",    "dif":"todas", "ind":"economia","meta":80},
    {"id":"l08","emoji":"❤️","nombre":"Humanista",               "tipo":"indicador_fin",    "dif":"todas", "ind":"bienestar_social","meta":80},
    {"id":"l09","emoji":"⚡","nombre":"Ingeniero",                "tipo":"indicador_fin",    "dif":"todas", "ind":"energia","meta":80},
    {"id":"l10","emoji":"🌟","nombre":"Ciudad Equilibrada",       "tipo":"todos_sobre",      "dif":"todas", "meta":70},
    {"id":"l11","emoji":"🔗","nombre":"Racha x3",                 "tipo":"racha",            "dif":"todas", "meta":3},
    {"id":"l12","emoji":"⛓️","nombre":"Racha x5",                "tipo":"racha",            "dif":"todas", "meta":5},
    {"id":"l13","emoji":"🎯","nombre":"Decisivo",                 "tipo":"decisiones_todas", "dif":"todas", "meta":8},
    {"id":"l14","emoji":"👥","nombre":"Equipo Grande",            "tipo":"tam_grupo",        "dif":"todas", "meta":5},
    {"id":"l15","emoji":"🏙️","nombre":"Urbanista",               "tipo":"partidas",         "dif":"todas", "meta":1},
    {"id":"l20","emoji":"👑","nombre":"Rey de la Ciudad",         "tipo":"todos_sobre",      "dif":"todas", "meta":80},
    {"id":"l25","emoji":"🎓","nombre":"Maestro Académico",        "tipo":"correctas_partida","dif":"todas", "meta":9},
    {"id":"l28","emoji":"🌍","nombre":"Guardián del Planeta",     "tipo":"indicador_fin",    "dif":"todas", "ind":"medio_ambiente","meta":90},
]
LOGROS_LOBBY = ["l04","l06","l11","l12","l13","l20","l25","l28"]

# ── Preguntas — importadas desde questions.py ─────────────────────────────────
from questions import PREGUNTAS
