import streamlit as st


def navegar(p):
    st.session_state["pantalla"] = p
    st.rerun()


def init_session():
    defaults = {
        "pantalla":             "inicio",
        "grupo_id":             None,
        "grupo_nombre":         "",
        "grupo_id_registro":    None,
        "dificultad_reg":       "Normal",
        "dificultad_sel":       "Normal",
        "estudiantes_temp":     [],
        "msg_est":              "",
        "pregunta_actual":      None,
        "respuesta_correcta":   False,
        "decision_elegida":     None,
        "decision_efectos":     None,
        "evento_ronda":         None,
        "fase_ronda":           "decision",
        "preguntas_usadas":     [],
        "resultado":            None,
        "indicadores_finales":  {},
        "rondas_completadas":   0,
        "timer_inicio":         None,
        "tiempo_agotado":       False,
        "correctas":            0,
        "incorrectas":          0,
        "logros_partida":       [],
        "logros_obtenidos":     [],
        "_ranking_guardado":    False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
