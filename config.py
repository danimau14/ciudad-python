import random
import re

# ─── CONSTANTES GLOBALES ─────────────────────────────────────────
VALOR_INICIAL    = 50
VALOR_MINIMO     = 0
TOTAL_RONDAS     = 10
TIEMPO_PREGUNTA  = 30
COOLDOWN         = 3
MIN_EST          = 3
MAX_EST          = 5
REGEX_NOMBRE     = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"

DIFICULTADES = {
    "Fácil":   {"mult_neg": 0.5,  "mult_pos": 1.2, "evento_neg_prob": 0.25, "icon": "🟢", "desc": "Penalizaciones reducidas al 50%"},
    "Medio":   {"mult_neg": 1.0,  "mult_pos": 1.0, "evento_neg_prob": 0.45, "icon": "🟡", "desc": "Reglas estándar del juego"},
    "Difícil": {"mult_neg": 1.6,  "mult_pos": 0.8, "evento_neg_prob": 0.65, "icon": "🔴", "desc": "Errores y eventos más devastadores"},
}

IND_COLOR = {
    "economia":        ("#3b82f6","💰"),
    "medio_ambiente":  ("#22c55e","🌿"),
    "energia":         ("#f59e0b","⚡"),
    "bienestar_social":("#ec4899","🏥"),
}

IND_LABEL = {
    "economia":        "Economía",
    "medio_ambiente":  "Medio Ambiente",
    "energia":         "Energía",
    "bienestar_social":"Bienestar Social",
}

CAT_COLOR = {
    "Python":      "#6366f1",
    "PSeInt":      "#06b6d4",
    "Calculo":     "#f97316",
    "Derivadas":   "#a855f7",
    "Fisica MRU":  "#10b981",
    "Fisica MRUA": "#14b8a6",
    "Matrices":    "#f43f5e",
}

# ─── ATRIBUTOS DE ESTRELLAS ──────────────────────────────────────
ATRIBUTOS = {
    "escudo_ciudad":   {"nombre":"Escudo de Ciudad",      "icon":"🏰","costo":30,"desc":"Protege todos los indicadores de eventos negativos esta ronda","efecto":"escudo_total"},
    "escudo_economia": {"nombre":"Escudo Económico",      "icon":"💰","costo":10,"desc":"Protege Economía de efectos negativos esta ronda",            "efecto":"escudo_economia"},
    "escudo_ambiente": {"nombre":"Escudo Ambiental",      "icon":"🌿","costo":15,"desc":"Protege Medio Ambiente de efectos negativos esta ronda",      "efecto":"escudo_ambiente"},
    "escudo_energia":  {"nombre":"Escudo Energético",     "icon":"⚡","costo":12,"desc":"Protege Energía de efectos negativos esta ronda",             "efecto":"escudo_energia"},
    "escudo_social":   {"nombre":"Escudo Social",         "icon":"🏥","costo":12,"desc":"Protege Bienestar Social de efectos negativos esta ronda",    "efecto":"escudo_social"},
    "impulso_doble":   {"nombre":"Impulso Doble",         "icon":"🚀","costo":20,"desc":"Duplica el efecto positivo de la decisión esta ronda",        "efecto":"impulso_doble"},
    "tiempo_extra":    {"nombre":"Tiempo Extra",          "icon":"⏱️","costo":8, "desc":"Agrega 15 segundos extra al temporizador esta ronda",         "efecto":"tiempo_extra"},
    "segunda_oportunidad":{"nombre":"Segunda Oportunidad","icon":"🔄","costo":25,"desc":"Si fallas la pregunta no se aplica la penalización",          "efecto":"segunda_oportunidad"},
    "robar_pregunta":  {"nombre":"Cambiar Pregunta",      "icon":"🎲","costo":15,"desc":"Descarta la pregunta actual y obtén una nueva",               "efecto":"robar_pregunta"},
    "bonus_estrellas": {"nombre":"Lluvia de Estrellas",   "icon":"🌟","costo":5, "desc":"Gana 10 estrellas extra inmediatamente",                      "efecto":"bonus_estrellas"},
    "cooldown_reset":  {"nombre":"Reset de Cooldown",     "icon":"🔃","costo":20,"desc":"Elimina el cooldown de todas las decisiones esta ronda",      "efecto":"cooldown_reset"},
    "vision":          {"nombre":"Visión Estratégica",    "icon":"🔭","costo":18,"desc":"Muestra los efectos exactos del evento antes de decidir",     "efecto":"vision"},
}

# Cuántas estrellas gana el grupo al terminar una partida
ESTRELLAS_POR_RESULTADO = {
    "victoria_facil":   15,
    "victoria_medio":   25,
    "victoria_dificil": 40,
    "derrota_facil":     5,
    "derrota_medio":    10,
    "derrota_dificil":  18,
    "logro_bonus":       3,   # por cada logro obtenido
}
