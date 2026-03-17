MISIONES = {
    # ── Misiones de preguntas ────────────────────────────────────
    "m_3_correctas":    {"nombre":"Trío Perfecto",         "icon":"🎯","desc":"Responde 3 preguntas correctas en una partida",     "req":"correctas>=3",   "estrellas":5},
    "m_5_correctas":    {"nombre":"Experto",               "icon":"🧠","desc":"Responde 5 preguntas correctas en una partida",     "req":"correctas>=5",   "estrellas":10},
    "m_0_incorrectas":  {"nombre":"Sin Errores",           "icon":"💯","desc":"Completa la partida sin respuestas incorrectas",    "req":"incorrectas==0", "estrellas":20},
    "m_combo3":         {"nombre":"Combo x3",              "icon":"🔥","desc":"3 respuestas correctas consecutivas",              "req":"combo_max>=3",   "estrellas":8},
    "m_combo5":         {"nombre":"Combo x5",              "icon":"💥","desc":"5 respuestas correctas consecutivas",              "req":"combo_max>=5",   "estrellas":15},
    "m_rapido":         {"nombre":"Veloz",                 "icon":"⚡","desc":"Responde 3 preguntas en menos de 10 segundos",     "req":"rapidas>=3",     "estrellas":12},
    # ── Misiones de indicadores ──────────────────────────────────
    "m_eco_70":         {"nombre":"Economía Sólida",       "icon":"💰","desc":"Economía por encima de 70 al final",               "req":"eco>70",         "estrellas":8},
    "m_amb_70":         {"nombre":"Planeta Verde",         "icon":"🌿","desc":"Medio Ambiente por encima de 70 al final",         "req":"amb>70",         "estrellas":8},
    "m_ene_70":         {"nombre":"Energía Limpia",        "icon":"🔋","desc":"Energía por encima de 70 al final",                "req":"ene>70",         "estrellas":8},
    "m_bie_70":         {"nombre":"Bienestar Alto",        "icon":"🏥","desc":"Bienestar Social por encima de 70 al final",       "req":"bie>70",         "estrellas":8},
    "m_prom_70":        {"nombre":"Ciudad Equilibrada",    "icon":"⚖️","desc":"Promedio de todos los indicadores ≥ 70",           "req":"prom>=70",       "estrellas":15},
    "m_todos_60":       {"nombre":"Gestión Integral",      "icon":"🏆","desc":"Todos los indicadores por encima de 60 al final",  "req":"todos_60",       "estrellas":18},
    # ── Misiones de dificultad ───────────────────────────────────
    "m_ganar_facil":    {"nombre":"Primera Victoria",      "icon":"🌱","desc":"Gana una partida en nivel Fácil",                  "req":"victoria_facil", "estrellas":5},
    "m_ganar_medio":    {"nombre":"Desafío Medio",         "icon":"⭐","desc":"Gana una partida en nivel Medio",                  "req":"victoria_medio", "estrellas":12},
    "m_ganar_dificil":  {"nombre":"Élite",                 "icon":"💀","desc":"Gana una partida en nivel Difícil",               "req":"victoria_dificil","estrellas":25},
    # ── Misiones de estrategia ───────────────────────────────────
    "m_sin_estrellas":  {"nombre":"Juego Puro",            "icon":"🎭","desc":"Gana sin usar ningún atributo de estrellas",       "req":"sin_estrellas",  "estrellas":20},
    "m_superviviente":  {"nombre":"Superviviente",         "icon":"🛡️","desc":"10 rondas sin ningún indicador crítico",          "req":"ninguno_critico","estrellas":15},
    "m_sin_neg":        {"nombre":"Cielos Despejados",     "icon":"☀️","desc":"0 eventos negativos en la partida",               "req":"eventos_neg==0", "estrellas":10},
    "m_5_pos":          {"nombre":"Suertudo",              "icon":"🍀","desc":"5 o más eventos positivos en la partida",          "req":"eventos_pos>=5", "estrellas":8},
}


def evaluar_misiones(stats, ind):
    """Retorna lista de claves de misiones cumplidas en esta partida."""
    correctas   = stats.get("correctas", 0)
    incorrectas = stats.get("incorrectas", 0)
    combo_max   = stats.get("combo_max", 0)
    rapidas     = stats.get("rapidas", 0)
    eventos_neg = stats.get("eventos_negativos", 0)
    eventos_pos = stats.get("eventos_positivos", 0)
    sin_estr    = stats.get("estrellas_usadas", 0) == 0
    n_critico   = stats.get("ninguno_critico", True)
    resultado   = stats.get("resultado", "")
    dificultad  = stats.get("dificultad", "Medio")

    eco  = ind.get("economia", 0)
    amb  = ind.get("medio_ambiente", 0)
    ene  = ind.get("energia", 0)
    bie  = ind.get("bienestar_social", 0)
    prom = (eco + amb + ene + bie) / 4

    cumplidas = []
    if correctas >= 3:                           cumplidas.append("m_3_correctas")
    if correctas >= 5:                           cumplidas.append("m_5_correctas")
    if incorrectas == 0:                         cumplidas.append("m_0_incorrectas")
    if combo_max >= 3:                           cumplidas.append("m_combo3")
    if combo_max >= 5:                           cumplidas.append("m_combo5")
    if rapidas >= 3:                             cumplidas.append("m_rapido")
    if eco > 70:                                 cumplidas.append("m_eco_70")
    if amb > 70:                                 cumplidas.append("m_amb_70")
    if ene > 70:                                 cumplidas.append("m_ene_70")
    if bie > 70:                                 cumplidas.append("m_bie_70")
    if prom >= 70:                               cumplidas.append("m_prom_70")
    if all(v > 60 for v in [eco,amb,ene,bie]):   cumplidas.append("m_todos_60")
    if resultado == "victoria" and dificultad == "Fácil":   cumplidas.append("m_ganar_facil")
    if resultado == "victoria" and dificultad == "Medio":   cumplidas.append("m_ganar_medio")
    if resultado == "victoria" and dificultad == "Difícil": cumplidas.append("m_ganar_dificil")
    if sin_estr and resultado == "victoria":     cumplidas.append("m_sin_estrellas")
    if n_critico:                                cumplidas.append("m_superviviente")
    if eventos_neg == 0:                         cumplidas.append("m_sin_neg")
    if eventos_pos >= 5:                         cumplidas.append("m_5_pos")

    return cumplidas
