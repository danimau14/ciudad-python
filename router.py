import streamlit as st
from database import inicializar_db
from ui_styles import inyectar_css


def router():
    # Inicializar ANTES de importar cualquier pantalla
    inicializar_db()
    inyectar_css()

    # Imports diferidos — se ejecutan DESPUÉS de que las tablas existen
    from screen_inicio import pantalla_inicio, pantalla_instrucciones
    from screen_auth import pantalla_login, pantalla_registro, pantalla_agregar_estudiantes
    from screen_lobby import pantalla_lobby
    from screen_juego import pantalla_juego
    from screen_fin import pantalla_fin
    from screen_ranking import pantalla_ranking
    from screen_misiones import pantalla_misiones
    from screen_logros import pantalla_logros

    pantallas = {
        "inicio":              pantalla_inicio,
        "instrucciones":       pantalla_instrucciones,
        "login":               pantalla_login,
        "registro":            pantalla_registro,
        "agregar_estudiantes": pantalla_agregar_estudiantes,
        "lobby":               pantalla_lobby,
        "juego":               pantalla_juego,
        "fin":                 pantalla_fin,
        "ranking":             pantalla_ranking,
        "misiones":            pantalla_misiones,
        "logros":              pantalla_logros,
    }
    pantallas.get(st.session_state.get("pantalla", "inicio"), pantalla_inicio)()
