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
    "Fácil":   {"facil": 0.90, "normal": 0.09, "dificil": 0.01},
    "Normal":  {"facil": 0.20, "normal": 0.60, "dificil": 0.20},
    "Difícil": {"facil": 0.05, "normal": 0.35, "dificil": 0.60},
}

# ── Penalizaciones  ──────────────────────────────────────────────────────────
# -5 pts por respuesta incorrecta (ronda impar)
# -10 pts por respuesta incorrecta (ronda par = doble)
# Eventos: 70% positivos (mantener equilibrio) / 30% negativos (colapso)
DIFICULTADES = {
    "Fácil":   {"penalizacion": 5, "mult_par": 2, "estrellas": 1,
                "eventos_peso": {"positivos": 0.70, "negativos": 0.30}},
    "Normal":  {"penalizacion": 5, "mult_par": 2, "estrellas": 2,
                "eventos_peso": {"positivos": 0.70, "negativos": 0.30}},
    "Difícil": {"penalizacion": 5, "mult_par": 2, "estrellas": 3,
                "eventos_peso": {"positivos": 0.70, "negativos": 0.30}},
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
# Impactos reducidos para pensamiento sistémico (+1 a +10, -1 a -10)
DECISIONES = {
    # ── FÁCIL (efectos claros y bajos) ─────────────────────────────────────
    "Crear parque natural":     {"emoji":"🌳","dif":"facil","economia":-2,"medio_ambiente":5,"energia":-1,"bienestar_social":3},
    "Agricultura urbana":       {"emoji":"🌱","dif":"facil","economia":2,"medio_ambiente":3,"energia":1,"bienestar_social":2},
    "Construir escuelas":       {"emoji":"🏫","dif":"facil","economia":-3,"medio_ambiente":1,"energia":-1,"bienestar_social":6},
    
    # ── NORMAL (trade-offs moderados) ──────────────────────────────────────
    "Construir fábrica":        {"emoji":"🏭","dif":"normal","economia":5,"medio_ambiente":-4,"energia":-2,"bienestar_social":-1},
    "Instalar paneles solares": {"emoji":"☀️","dif":"normal","economia":-3,"medio_ambiente":3,"energia":6,"bienestar_social":0},
    "Ampliar autopistas":       {"emoji":"🛣️","dif":"normal","economia":3,"medio_ambiente":-5,"energia":-3,"bienestar_social":-2},
    "Mejorar hospitales":       {"emoji":"🏥","dif":"normal","economia":-5,"medio_ambiente":0,"energia":-2,"bienestar_social":7},
    
    # ── DIFÍCIL (trade-offs complejos) ────────────────────────────────────
    "Planta de carbón":         {"emoji":"⚫","dif":"dificil","economia":6,"medio_ambiente":-7,"energia":8,"bienestar_social":-3},
}

# ── Eventos por dificultad ────────────────────────────────────────────────────
# 70% eventos positivos (mantener equilibrio) / 30% eventos negativos (colapso)
# Impactos reducidos para pensamiento sistémico (+1 a +10, -1 a -10)
EVENTOS_POR_DIFICULTAD = {
    "Fácil": {
        "negativos": [  # 30% - causan colapso
            {"nombre":"🌧️ Lluvia intensa local",    "indicador":"medio_ambiente",  "valor":-2},
            {"nombre":"🔌 Corte eléctrico parcial", "indicador":"energia",         "valor":-2},
            {"nombre":"📉 Baja de recaudo",         "indicador":"economia",        "valor":-2},
            {"nombre":"🚗 Congestión urbana",       "indicador":"bienestar_social","valor":-2},
        ],
        "positivos": [  # 70% - mantienen equilibrio
            {"nombre":"🎉 Feria barrial",           "indicador":"bienestar_social","valor":2},
            {"nombre":"💰 Ahorro municipal",        "indicador":"economia",        "valor":2},
            {"nombre":"⚡ Mantenimiento energético","indicador":"energia",         "valor":2},
            {"nombre":"🌿 Jornada ecológica",       "indicador":"medio_ambiente",  "valor":2},
            {"nombre":"🏘️ Mejora en comunidades",  "indicador":"bienestar_social","valor":1},
        ],
    },
    "Normal": {
        "negativos": [  # 30% - causan colapso
            {"nombre":"🌩️ Tormenta devastadora",    "indicador":"medio_ambiente",  "valor":-4},
            {"nombre":"🤒 Pandemia regional",       "indicador":"bienestar_social","valor":-5},
            {"nombre":"🔌 Apagón masivo",           "indicador":"energia",         "valor":-4},
            {"nombre":"📉 Recesión económica",      "indicador":"economia",        "valor":-4},
            {"nombre":"🌊 Inundación urbana",       "indicador":"bienestar_social","valor":-3},
        ],
        "positivos": [  # 70% - mantienen equilibrio
            {"nombre":"💰 Boom económico",          "indicador":"economia",        "valor":3},
            {"nombre":"⚡ Ahorro energético",       "indicador":"energia",         "valor":3},
            {"nombre":"🌽 Gran cosecha",            "indicador":"medio_ambiente",  "valor":2},
            {"nombre":"🎉 Festival cultural",       "indicador":"bienestar_social","valor":3},
            {"nombre":"🌍 Inversión extranjera",    "indicador":"economia",        "valor":4},
            {"nombre":"🎓 Programa educativo",      "indicador":"bienestar_social","valor":2},
        ],
    },
    "Difícil": {
        "negativos": [  # 30% - causan colapso
            {"nombre":"🏜️ Megasequía prolongada",   "indicador":"medio_ambiente",  "valor":-6},
            {"nombre":"⚡ Colapso de red eléctrica","indicador":"energia",         "valor":-7},
            {"nombre":"💸 Crisis fiscal severa",    "indicador":"economia",        "valor":-6},
            {"nombre":"😷 Emergencia sanitaria",    "indicador":"bienestar_social","valor":-7},
            {"nombre":"🔥 Incendio forestal masivo","indicador":"medio_ambiente",  "valor":-7},
        ],
        "positivos": [  # 70% - mantienen equilibrio (épicos/severos)
            {"nombre":"🚀 Plan de rescate nacional","indicador":"economia",        "valor":4},
            {"nombre":"⚡ Innovación energética",   "indicador":"energia",         "valor":4},
            {"nombre":"🌲 Reforestación récord",    "indicador":"medio_ambiente",  "valor":4},
            {"nombre":"🤝 Pacto social ciudadano",  "indicador":"bienestar_social","valor":4},
            {"nombre":"💻 Inversión tecnológica",   "indicador":"economia",        "valor":5},
            {"nombre":"🌍 Cumbre ambiental mundial","indicador":"medio_ambiente",  "valor":3},
        ],
    },
}

# ── Estados de la ciudad (basados en puntuación total 0-100) ─────────────────
# Puntuación total = promedio de 4 indicadores (0-100)
ESTADOS_CIUDAD = {
    "colapso": {
        "nombre": "🔴 CIUDAD EN COLAPSO",
        "rango": (0, 25),
        "color": "#ef4444",
        "descripcion": "Los sistemas de la ciudad se han desestabilizado. Múltiples indicadores en crisis.",
        "emoji": "🔴"
    },
    "critica": {
        "nombre": "🟠 CIUDAD EN CRISIS",
        "rango": (25, 50),
        "color": "#f59e0b",
        "descripcion": "La ciudad enfrenta desafíos significativos. Se requieren cambios urgentes.",
        "emoji": "🟠"
    },
    "inestable": {
        "nombre": "🟡 CIUDAD INESTABLE",
        "rango": (50, 75),
        "color": "#eab308",
        "descripcion": "La ciudad tiene sistemas balanceados pero frágiles. Necesita refuerzos.",
        "emoji": "🟡"
    },
    "estable": {
        "nombre": "🟢 CIUDAD EQUILIBRADA",
        "rango": (75, 100),
        "color": "#10b981",
        "descripcion": "¡Excelente! Los sistemas de la ciudad están en equilibrio sostenible.",
        "emoji": "🟢"
    },
}

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
# Generar misiones adicionales hasta tener 100 misiones totales.
for i in range(13, 101):
    MISIONES.append({
        "id": f"m{i:02d}",
        "nombre": f"Misión {i}",
        "desc": f"Logra un objetivo especial #{i} en tu gestión urbana.",
        "recompensa": 2 + (i % 5),
        "dif": "todas" if i % 3 else "Normal" if i % 5 else "Difícil",
        "tipo": "partidas" if i % 4 == 0 else "racha" if i % 4 == 1 else "correctas" if i % 4 == 2 else "indicador",
        "meta": (i % 10 + 1) * (2 if i % 4 == 2 else 1)
    })

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
    {"id":"l09","emoji":"🛠️","nombre":"Ingeniero",                "tipo":"indicador_fin",    "dif":"todas", "ind":"energia","meta":80},
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

# ── Preguntas — banco principal ────────────────────────────────────────────────
from questions_bank import PREGUNTAS
