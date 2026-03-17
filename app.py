import streamlit as st
from ui_styles import inyectar_css
from session_manager import init_session
from database import inicializar_db
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
    inicializar_db()
    router()


if __name__ == "__main__":
    main()
