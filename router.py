import streamlit as st
from screen_inicio import pantalla_inicio, pantalla_instrucciones
from screen_agregar_estudiantes import pantalla_registro, pantalla_agregar_estudiantes
from screen_login import pantalla_login
from screen_lobby import pantalla_lobby
from screen_juego import pantalla_juego
from screen_fin import pantalla_fin
from screen_ranking import pantalla_ranking
from screen_misiones import pantalla_misiones
from screen_logros import pantalla_logros


def router():
    pantallas = {
        "inicio":              pantalla_inicio,
        "instrucciones":       pantalla_instrucciones,
        "registro":            pantalla_registro,
        "agregar_estudiantes": pantalla_agregar_estudiantes,
        "login":               pantalla_login,
        "lobby":               pantalla_lobby,
        "juego":               pantalla_juego,
        "fin":                 pantalla_fin,
        "ranking":             pantalla_ranking,
        "misiones":            pantalla_misiones,
        "logros":              pantalla_logros,
    }
    pantallas.get(st.session_state.get("pantalla", "inicio"), pantalla_inicio)()
