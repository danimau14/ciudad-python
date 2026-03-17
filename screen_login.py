import streamlit as st
from database import login_grupo
from session_manager import navegar


def pantalla_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="game-title" style="font-size:1.6rem">Iniciar Sesión</div>',
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("form_login"):
            nombre = st.text_input("Nombre del grupo")
            pw     = st.text_input("Contraseña", type="password")
            sub    = st.form_submit_button("Entrar 🚀", use_container_width=True)

        if sub:
            gid = login_grupo(nombre, pw)
            if gid:
                st.session_state["grupo_id"]     = gid
                st.session_state["grupo_nombre"] = nombre.strip()
                st.session_state["fase_ronda"]   = "decision"
                navegar("juego")
            else:
                st.error("Credenciales incorrectas.")

        if st.button("← Volver", use_container_width=True):
            navegar("inicio")
