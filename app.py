import streamlit as st
import os
from session_manager import init_session
from ui_styles import inyectar_css
from database import inicializar_db, DB_PATH
from router import router

st.set_page_config(
    page_title="Ciudad en Equilibrio",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    init_session()
    inyectar_css()
    for ext in ["-wal", "-shm", "-journal"]:
        f_lock = DB_PATH + ext
        try:
            if os.path.exists(f_lock):
                os.remove(f_lock)
        except Exception:
            pass
    inicializar_db()
    router()


if __name__ == "__main__":
    main()
