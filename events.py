import random
from config import DIFICULTADES

# ════════════════════════════════════════════════════════════════════════════════
# EVENTOS CLASIFICADOS POR DIFICULTAD
# 70% mantener equilibrio ciudad (eventos positivos/balanceados)
# 30% que la ciudad colapse (eventos negativos)
# ════════════════════════════════════════════════════════════════════════════════

EVENTOS_FACIL = {
    "negativos": [  # 30% - Eventos que causan colapso (leves)
        {"nombre":"🌧️ Lluvia intensa local",    "efectos":{"medio_ambiente":-6}},
        {"nombre":"🔌 Corte eléctrico parcial", "efectos":{"energia":-7}},
        {"nombre":"📉 Baja de recaudo",         "efectos":{"economia":-6}},
        {"nombre":"🚗 Congestión urbana",       "efectos":{"bienestar_social":-6}},
    ],
    "positivos": [  # 70% - Eventos para mantener equilibrio (leves)
        {"nombre":"🎉 Feria barrial",           "efectos":{"bienestar_social":6}},
        {"nombre":"💰 Ahorro municipal",        "efectos":{"economia":6}},
        {"nombre":"⚡ Mantenimiento energético","efectos":{"energia":6}},
        {"nombre":"🌿 Jornada ecológica",       "efectos":{"medio_ambiente":6}},
    ],
}

EVENTOS_NORMAL = {
    "negativos": [  # 30% - Eventos que causan colapso (moderados)
        {"nombre":"🌩️ Tormenta devastadora",    "efectos":{"medio_ambiente":-14}},
        {"nombre":"🤒 Pandemia regional",        "efectos":{"bienestar_social":-16,"economia":-8}},
        {"nombre":"🔌 Apagón masivo",            "efectos":{"energia":-14,"economia":-6}},
        {"nombre":"📉 Recesión económica",       "efectos":{"economia":-14,"bienestar_social":-6}},
        {"nombre":"🌊 Inundación urbana",        "efectos":{"bienestar_social":-13,"energia":-8}},
    ],
    "positivos": [  # 70% - Eventos para mantener equilibrio (moderados)
        {"nombre":"💰 Boom económico",           "efectos":{"economia":10,"bienestar_social":5}},
        {"nombre":"⚡ Ahorro energético",        "efectos":{"energia":9}},
        {"nombre":"🌽 Gran cosecha",             "efectos":{"medio_ambiente":8,"bienestar_social":6}},
        {"nombre":"🎉 Festival cultural",        "efectos":{"bienestar_social":10,"economia":4}},
        {"nombre":"🌍 Inversión extranjera",     "efectos":{"economia":12,"bienestar_social":4}},
    ],
}

EVENTOS_DIFICIL = {
    "negativos": [  # 30% - Eventos que causan colapso (severos)
        {"nombre":"🏜️ Megasequía prolongada",   "efectos":{"medio_ambiente":-20,"energia":-8}},
        {"nombre":"⚡ Colapso de red eléctrica", "efectos":{"energia":-22,"economia":-10}},
        {"nombre":"💸 Crisis fiscal severa",    "efectos":{"economia":-21,"bienestar_social":-12}},
        {"nombre":"😷 Emergencia sanitaria",    "efectos":{"bienestar_social":-22,"economia":-15}},
        {"nombre":"🔥 Incendio forestal masivo", "efectos":{"medio_ambiente":-24,"bienestar_social":-8}},
    ],
    "positivos": [  # 70% - Eventos para mantener equilibrio (severos/épicos)
        {"nombre":"🚀 Plan de rescate nacional", "efectos":{"economia":14,"bienestar_social":8}},
        {"nombre":"⚡ Innovación energética",    "efectos":{"energia":14,"medio_ambiente":6}},
        {"nombre":"🌲 Reforestación récord",    "efectos":{"medio_ambiente":13,"bienestar_social":5}},
        {"nombre":"🤝 Pacto social ciudadano",  "efectos":{"bienestar_social":14,"economia":6}},
        {"nombre":"💻 Inversión tecnológica",   "efectos":{"economia":15,"energia":7}},
    ],
}

# Mapeo de dificultad a eventos
EVENTOS_POR_DIFICULTAD_DICT = {
    "facil": EVENTOS_FACIL,
    "normal": EVENTOS_NORMAL,
    "dificil": EVENTOS_DIFICIL,
}


def generar_evento(ronda, dificultad):
    """
    Genera un evento basado en la dificultad.
    70% de probabilidad de evento positivo (mantener equilibrio)
    30% de probabilidad de evento negativo (causar colapso)
    """
    # Obtener eventos según dificultad
    eventos_dict = EVENTOS_POR_DIFICULTAD_DICT.get(dificultad, EVENTOS_POR_DIFICULTAD_DICT["normal"])
    
    # 70% positivos, 30% negativos
    es_positivo = random.random() < 0.70
    
    pool = eventos_dict["positivos"] if es_positivo else eventos_dict["negativos"]
    
    if not pool:
        pool = eventos_dict["positivos"] + eventos_dict["negativos"]
    
    evento_base = random.choice(pool).copy()
    
    return evento_base
