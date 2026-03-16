import streamlit as st
from navigation import navegar
from database import login_grupo, obtener_progreso
from config import TOTAL_RONDAS


def pantalla_login():
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown("<div style='text-align:center;'><span class='emoji-title' style='font-size:1.8rem;'>🔐</span></div><div class='game-title' style='font-size:1.6rem;'>Iniciar Sesion</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        with st.form("form_login"):
            nombre = st.text_input("👥 Nombre del grupo")
            pw     = st.text_input("🔒 Contrasena", type="password")
            sub    = st.form_submit_button("Entrar 🚀", use_container_width=True)
        if sub:
            resultado = login_grupo(nombre, pw)
            if resultado:
                gid, dificultad = resultado
                progreso = obtener_progreso(gid)
                st.session_state["grupo_id"]       = gid
                st.session_state["grupo_nombre"]   = nombre.strip()
                st.session_state["dificultad"]     = dificultad
                st.session_state["fase_ronda"]     = "decision"
                st.session_state["ranking_guardado"] = False
                # Si la partida ya terminó, mandar a fin para que elija JUGAR DE NUEVO
                if progreso.get("partida_terminada", 0) == 1:
                    st.session_state["resultado"]           = "victoria"
                    st.session_state["indicadores_finales"] = {
                        k: progreso[k] for k in ["economia","medio_ambiente","energia","bienestar_social"]
                    }
                    st.session_state["rondas_completadas"]  = TOTAL_RONDAS
                    st.session_state["ranking_guardado"]    = True  # ya se guardó antes
                    navegar("fin")
                else:
                    navegar("juego")
            else:
                st.error("Credenciales incorrectas.")
        if st.button("⬅️ Volver", use_container_width=True):
            navegar("inicio")
