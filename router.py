import streamlit as st
from session_manager import init_session
from ui_styles import inyectar_css
from screen_inicio import pantalla_inicio, pantalla_instrucciones
from screen_auth import pantalla_login, pantalla_registro   # ambas en screen_auth.py
from screen_lobby import pantalla_lobby
from screen_juego import pantalla_juego
from screen_fin import pantalla_fin
from screen_ranking import pantalla_ranking
from screen_misiones import pantalla_misiones
from screen_logros import pantalla_logros


def router():
    init_session()
    inyectar_css()
    pantallas = {
        "inicio":        pantalla_inicio,
        "login":         pantalla_login,       # screen_auth → pantalla_login()   → lobby
        "registro":      pantalla_registro,    # screen_auth → pantalla_registro() → lobby
        "lobby":         pantalla_lobby,
        "juego":         pantalla_juego,
        "fin":           pantalla_fin,
        "ranking":       pantalla_ranking,
        "misiones":      pantalla_misiones,
        "logros":        pantalla_logros,
        "instrucciones": pantalla_instrucciones,
    }
    pantallas.get(st.session_state.get("pantalla", "inicio"), pantalla_inicio)()
