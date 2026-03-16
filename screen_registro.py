import streamlit as st
from navigation import navegar
from database import registrar_grupo
from config import DIFICULTADES, MIN_EST, MAX_EST


def pantalla_registro():
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown(
            "<div style='text-align:center;padding:6px 0 2px;'>"
            "<span class='emoji-title' style='font-size:2.2rem;'>📝</span></div>"
            "<div class='game-title' style='font-size:1.5rem;letter-spacing:3px;'>REGISTRAR GRUPO</div>"
            "<div class='game-sub' style='font-size:.7rem;'>NUEVO EQUIPO DE CONTROL</div>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Info: el grupo se registra al finalizar con estudiantes
        st.markdown(
            "<div style='background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.18);"
            "border-radius:8px;padding:10px 14px;margin-bottom:14px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:2px;margin-bottom:4px;'>PROCESO</div>"
            "<div style='color:#94a3b8;font-size:0.82rem;line-height:1.6;'>"
            "1️⃣ Define el nombre y contraseña del grupo<br>"
            "2️⃣ Agrega entre <b style='color:#00d4ff;'>"+str(MIN_EST)+"</b> y "
            "<b style='color:#00d4ff;'>"+str(MAX_EST)+"</b> operadores<br>"
            "3️⃣ El grupo se crea solo al finalizar con el mínimo requerido"
            "</div></div>", unsafe_allow_html=True)

        with st.form("form_reg"):
            nombre = st.text_input("👥 Nombre del grupo", placeholder="Ej: Equipo Titan",
                                   value=st.session_state.get("reg_nombre_temp",""))
            pw     = st.text_input("🔒 Contraseña", type="password")
            pw2    = st.text_input("🔒 Confirmar contraseña", type="password")
            sub    = st.form_submit_button("SIGUIENTE → AGREGAR OPERADORES",
                                           use_container_width=True)
        if sub:
            nombre = nombre.strip()
            if not nombre:
                st.error("⚠️ El nombre del grupo es requerido.")
            elif len(pw) < 4:
                st.error("⚠️ La contraseña debe tener mínimo 4 caracteres.")
            elif pw != pw2:
                st.error("⚠️ Las contraseñas no coinciden.")
            else:
                # Solo guardar en session_state — NO escribir en DB todavía
                st.session_state["reg_nombre_temp"]   = nombre
                st.session_state["reg_pw_temp"]       = pw
                st.session_state["grupo_id_registro"] = None  # aún no existe en DB
                st.session_state["estudiantes_temp"]  = []
                navegar("agregar_estudiantes")

        if st.button("⬅️ VOLVER", use_container_width=True, key="btn_volver_reg"):
            navegar("inicio")
