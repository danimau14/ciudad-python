import streamlit as st

def init_session():
    defaults = {
        "pantalla": "inicio",
        "grupo_id": None,
        "grupo_nombre": "",
        "dificultad": "Medio",
        "fase_ronda": "decision",
        "pregunta_actual": None,
        "respuesta_correcta": False,
        "decision_elegida": None,
        "decision_efectos": None,
        "evento_ronda": None,
        "timer_inicio": None,
        "tiempo_agotado": False,
        "correctas": 0,
        "incorrectas": 0,
        "ninguno_critico": True,
        "logros_obtenidos": [],
        "logros_ganados": [],
        "preguntas_usadas": [],
        "energia_rondas_altas": 0,
        "ranking_guardado": False,
        "progreso_cargado": {},
        "resultado": "victoria",
        "indicadores_finales": {},
        "rondas_completadas": 0,
        "atributo_activo": None,
        "estrellas_usadas": 0,
        "combo_actual": 0,
        "combo_max": 0,
        "rapidas": 0,
        "sin_timeout": True,
        "eventos_negativos": 0,
        "eventos_positivos": 0,
        "misiones_cumplidas": [],
        "misiones_canjeadas": False,
        "estrellas_ganadas_partida": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

