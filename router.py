import streamlit as st
from screen_inicio import pantalla_inicio, pantalla_lobby, pantalla_instrucciones, pantalla_logros
from screen_registro import pantalla_registro
from screen_agregar_estudiantes import pantalla_agregar_estudiantes
from screen_login import pantalla_login
from screen_juego import pantalla_juego
from screen_fin import pantalla_fin
from screen_ranking import pantalla_ranking
from screen_misiones import pantalla_misiones


def router():
    pantallas = {
        "inicio":              pantalla_inicio,
        "lobby":               pantalla_lobby,
        "instrucciones":       pantalla_instrucciones,
        "logros":              pantalla_logros,
        "misiones":            pantalla_misiones,
        "registro":            pantalla_registro,
        "agregar_estudiantes": pantalla_agregar_estudiantes,
        "login":               pantalla_login,
        "juego":               pantalla_juego,
        "fin":                 pantalla_fin,
        "ranking":             pantalla_ranking,
    }
    pantallas.get(st.session_state["pantalla"], pantalla_inicio)()
