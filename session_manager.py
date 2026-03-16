import streamlit as st


def init_session():
    d = {
        "pantalla": "inicio", "grupo_id": None, "grupo_nombre": "",
        "grupo_id_registro": None, "estudiantes_temp": [], "msg_est": "",
        "pregunta_actual": None, "respuesta_correcta": False,
        "decision_elegida": None, "decision_efectos": None,
        "evento_ronda": None, "fase_ronda": "decision",
        "preguntas_usadas": [], "resultado": None,
        "indicadores_finales": {}, "rondas_completadas": 0,
        "timer_inicio": None, "tiempo_agotado": False,
        "correctas": 0, "incorrectas": 0,
        "ninguno_critico": True, "dificultad": "Medio",
        "ranking_guardado": False,
    }
    for k, v in d.items():
        if k not in st.session_state:
            st.session_state[k] = v
