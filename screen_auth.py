import streamlit as st
from session_manager import navegar
import re

REGEX_NOMBRE = r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+"
MIN_EST = 3
MAX_EST = 5


def pantalla_login():
    st.markdown('<div class="game-title" style="font-size:1.6rem">🔐 Iniciar Sesión</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("form_login"):
        nombre = st.text_input("Nombre del grupo")
        pw     = st.text_input("Contraseña", type="password")
        sub    = st.form_submit_button("Entrar", use_container_width=True)

    if sub:
        from database import login_grupo, obtener_progreso
        gid = login_grupo(nombre, pw)
        if gid:
            st.session_state["grupo_id"]     = gid
            st.session_state["grupo_nombre"] = nombre
            navegar("lobby")
        else:
            st.error("Nombre o contraseña incorrectos.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  Volver al Inicio", use_container_width=True):
        navegar("inicio")


def pantalla_registro():
    st.markdown('<div class="game-title" style="font-size:1.6rem">📝 Registrar Grupo</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if "grupo_id_registro" not in st.session_state:
        st.session_state["grupo_id_registro"] = None
    if "estudiantes_temp" not in st.session_state:
        st.session_state["estudiantes_temp"] = []

    gid_reg = st.session_state.get("grupo_id_registro")

    if not gid_reg:
        with st.form("form_registro"):
            nombre = st.text_input("Nombre del grupo")
            pw     = st.text_input("Contraseña", type="password")
            pw2    = st.text_input("Confirmar contraseña", type="password")
            sub    = st.form_submit_button("Crear Grupo", use_container_width=True)

        if sub:
            from database import registrar_grupo
            if not nombre.strip():
                st.error("El nombre no puede estar vacío.")
            elif pw != pw2:
                st.error("Las contraseñas no coinciden.")
            elif len(pw) < 4:
                st.error("La contraseña debe tener al menos 4 caracteres.")
            else:
                ok, gid = registrar_grupo(nombre, pw)
                if ok:
                    st.session_state["grupo_id_registro"] = gid
                    st.session_state["grupo_nombre"]      = nombre
                    st.session_state["estudiantes_temp"]  = []
                    st.rerun()
                else:
                    st.error("Ese nombre de grupo ya existe.")
    else:
        from database import guardar_estudiante, obtener_estudiantes
        nombre_grp  = st.session_state.get("grupo_nombre", "")
        estudiantes = st.session_state.get("estudiantes_temp", [])

        st.success(f"Grupo **{nombre_grp}** creado. Ahora agrega de {MIN_EST} a {MAX_EST} estudiantes.")

        if len(estudiantes) < MAX_EST:
            with st.form("form_est"):
                est_nombre = st.text_input(f"Estudiante #{len(estudiantes)+1}")
                add        = st.form_submit_button("Agregar", use_container_width=True)
            if add:
                if not re.fullmatch(REGEX_NOMBRE, est_nombre.strip()):
                    st.error("Solo letras y espacios.")
                elif est_nombre.strip() in estudiantes:
                    st.error("Ese nombre ya fue agregado.")
                else:
                    guardar_estudiante(gid_reg, est_nombre.strip())
                    st.session_state["estudiantes_temp"].append(est_nombre.strip())
                    st.rerun()

        if estudiantes:
            st.markdown("**Estudiantes agregados:**")
            for e in estudiantes:
                st.markdown(f"- {e}")

        if len(estudiantes) >= MIN_EST:
            if st.button("✅  Ir al Lobby", use_container_width=True, type="primary"):
                st.session_state["grupo_id"]            = gid_reg
                st.session_state["grupo_id_registro"]   = None
                st.session_state["estudiantes_temp"]    = []
                navegar("lobby")
        else:
            st.info(f"Agrega al menos {MIN_EST - len(estudiantes)} estudiante(s) más.")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  Volver al Inicio", use_container_width=True):
        navegar("inicio")
