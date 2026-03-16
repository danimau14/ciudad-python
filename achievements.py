LOGROS = {
    "admin_eficiente":   {"icon":"🏆","nombre":"Administrador Eficiente","desc":"Todos los indicadores sobre 60"},
    "ciudad_verde":      {"icon":"🌿","nombre":"Ciudad Verde",           "desc":"Medio ambiente sobre 80"},
    "energia_sost":      {"icon":"⚡","nombre":"Energía Sostenible",      "desc":"Energía alta 3 rondas seguidas"},
    "economia_boom":     {"icon":"💰","nombre":"Economía en Auge",        "desc":"Economía sobre 75"},
    "ciudad_feliz":      {"icon":"😊","nombre":"Ciudad Feliz",           "desc":"Bienestar Social sobre 80"},
    "superviviente":     {"icon":"🛡️","nombre":"Superviviente",          "desc":"10 rondas sin indicador crítico"},
    "maestro_preguntas": {"icon":"🧠","nombre":"Maestro de Preguntas",   "desc":"8 o más respuestas correctas"},
    "equilibrio_total":  {"icon":"⚖️","nombre":"Equilibrio Total",        "desc":"Promedio ≥ 70 al final"},
}


def calcular_logros(ind, stats):
    ganados = []
    vals = [ind.get("economia",0), ind.get("medio_ambiente",0),
            ind.get("energia",0),  ind.get("bienestar_social",0)]
    prom = sum(vals) / 4 if vals else 0
    if all(v >= 60 for v in vals):          ganados.append("admin_eficiente")
    if ind.get("medio_ambiente",0) >= 80:   ganados.append("ciudad_verde")
    if ind.get("energia",0) >= 60:          ganados.append("energia_sost")
    if ind.get("economia",0) >= 75:         ganados.append("economia_boom")
    if ind.get("bienestar_social",0) >= 80: ganados.append("ciudad_feliz")
    if stats.get("ninguno_critico", True):  ganados.append("superviviente")
    if stats.get("correctas", 0) >= 8:      ganados.append("maestro_preguntas")
    if prom >= 70:                          ganados.append("equilibrio_total")
    return ganados


def calcular_puntaje(ind, correctas, incorrectas, logros, dificultad):
    from config import DIFICULTADES
    vals = [ind.get("economia",0), ind.get("medio_ambiente",0),
            ind.get("energia",0),  ind.get("bienestar_social",0)]
    prom = sum(vals) / 4 if vals else 0
    mult = {"Fácil": 0.8, "Medio": 1.0, "Difícil": 1.3}.get(dificultad, 1.0)
    base = int(prom * mult)
    return max(0, base + correctas * 5 - incorrectas * 3 + len(logros) * 10)
