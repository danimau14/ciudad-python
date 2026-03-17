import streamlit as st
from navigation import navegar
from database import login_grupo, obtener_progreso


def pantalla_login():
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown(
            "<div style='text-align:center;'>"
            "<span class='emoji-title' style='font-size:1.8rem;'>🔐</span></div>"
            "<div class='game-title' style='font-size:1.6rem;'>Iniciar Sesión</div>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("form_login"):
            nombre = st.text_input("👥 Nombre del grupo")
            pw     = st.text_input("🔒 Contraseña", type="password")
            sub    = st.form_submit_button("Entrar 🚀", use_container_width=True)
        if sub:
            resultado = login_grupo(nombre, pw)
            if resultado:
                gid, dificultad_guardada = resultado
                progreso = obtener_progreso(gid)
                st.session_state["grupo_id"]         = gid
                st.session_state["grupo_nombre"]     = nombre.strip()
                st.session_state["dificultad"]       = dificultad_guardada
                st.session_state["fase_ronda"]       = "decision"
                st.session_state["ranking_guardado"] = False
                st.session_state["progreso_cargado"] = dict(progreso)
                # Siempre ir al lobby — el lobby decide si jugar o mostrar fin
                navegar("lobby")
            else:
                st.error("Credenciales incorrectas.")
        if st.button("⬅️ Volver", use_container_width=True):
            navegar("inicio")
