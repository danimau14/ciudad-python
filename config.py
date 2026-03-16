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
