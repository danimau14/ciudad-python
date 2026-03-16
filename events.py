import random
from config import DIFICULTADES

EVENTOS = [
    {"nombre":"🌩️ Tormenta devastadora",    "efectos":{"medio_ambiente":-14}},
    {"nombre":"🤒 Pandemia regional",        "efectos":{"bienestar_social":-16,"economia":-8}},
    {"nombre":"🔌 Apagón masivo",            "efectos":{"energia":-14,"economia":-6}},
    {"nombre":"📉 Recesión económica",       "efectos":{"economia":-14,"bienestar_social":-6}},
    {"nombre":"🔥 Incendio forestal grave",  "efectos":{"medio_ambiente":-18,"bienestar_social":-5}},
    {"nombre":"💧 Sequía prolongada",        "efectos":{"medio_ambiente":-12,"energia":-8}},
    {"nombre":"💣 Crisis industrial",        "efectos":{"economia":-12,"medio_ambiente":-10}},
    {"nombre":"🌊 Inundación urbana",        "efectos":{"bienestar_social":-13,"energia":-8}},
    {"nombre":"⚡ Fallo de infraestructura", "efectos":{"energia":-16,"economia":-5}},
    {"nombre":"😷 Brote de enfermedad",      "efectos":{"bienestar_social":-12,"economia":-6}},
    {"nombre":"💰 Boom económico",           "efectos":{"economia":10,"bienestar_social":5}},
    {"nombre":"⚡ Ahorro energético",        "efectos":{"energia":9}},
    {"nombre":"🌽 Gran cosecha",             "efectos":{"medio_ambiente":8,"bienestar_social":6}},
    {"nombre":"🎉 Festival cultural",        "efectos":{"bienestar_social":10,"economia":4}},
    {"nombre":"🌍 Inversión extranjera",     "efectos":{"economia":12,"bienestar_social":4}},
    {"nombre":"🎓 Beca educativa masiva",    "efectos":{"bienestar_social":9,"economia":-4}},
    {"nombre":"🌬️ Energía renovable bonus", "efectos":{"energia":8,"medio_ambiente":5}},
    {"nombre":"🏗️ Protestas sociales",      "efectos":{"bienestar_social":-13,"economia":-8}},
    {"nombre":"🌱 Programa ambiental",       "efectos":{"medio_ambiente":15,"bienestar_social":4}},
]

EVENTOS_EPICOS = [
    {"nombre":"🚀 REVOLUCIÓN TECNOLÓGICA", "efectos":{"economia":20,"energia":18,"bienestar_social":10}},
    {"nombre":"💎 MEGA INVERSIÓN INTERNACIONAL","efectos":{"economia":25,"bienestar_social":12}},
    {"nombre":"🔋 DESCUBRIMIENTO ENERGÍA LIMPIA","efectos":{"energia":25,"medio_ambiente":18}},
    {"nombre":"🌍 CUMBRE AMBIENTAL MUNDIAL","efectos":{"medio_ambiente":22,"bienestar_social":14}},
    {"nombre":"☄️ CRISIS CLIMÁTICA GLOBAL","efectos":{"medio_ambiente":-25,"energia":-15,"bienestar_social":-12}},
    {"nombre":"💸 COLAPSO FINANCIERO MUNDIAL","efectos":{"economia":-25,"bienestar_social":-15}},
]


def generar_evento(ronda, dificultad):
    mult_neg = DIFICULTADES[dificultad]['mult_neg']
    mult_pos = DIFICULTADES[dificultad]['mult_pos']
    prob_neg = DIFICULTADES[dificultad]['evento_neg_prob']
    if ronda >= 7 and random.random() < 0.35:
        base_ev = random.choice(EVENTOS_EPICOS).copy()
        es_epico = True
    else:
        neg_pool = [e for e in EVENTOS if any(v < 0 for v in e['efectos'].values())]
        pos_pool = [e for e in EVENTOS if all(v >= 0 for v in e['efectos'].values())]
        base_ev = random.choice(neg_pool if random.random() < prob_neg else pos_pool).copy()
        es_epico = False
    base_ev['efectos'] = {k: int(v * (mult_neg if v < 0 else mult_pos))
                          for k, v in base_ev['efectos'].items()}
    base_ev['epico'] = es_epico
    return base_ev
