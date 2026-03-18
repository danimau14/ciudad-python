import streamlit as st
import re
from session_manager import navegar
from config import MIN_EST, MAX_EST, REGEX_NOMBRE


def pantalla_login():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="game-title" style="font-size:1.6rem">🔐 Iniciar Sesión</div>',
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("form_login"):
            nombre = st.text_input("Nombre del grupo")
            pw     = st.text_input("Contraseña", type="password")
            sub    = st.form_submit_button("Entrar 🚀", use_container_width=True)
        if sub:
            from database import login_grupo
            gid = login_grupo(nombre, pw)
            if gid:
                st.session_state["grupo_id"]     = gid
                st.session_state["grupo_nombre"] = nombre.strip()
                st.session_state["fase_ronda"]   = "decision"
                navegar("lobby")
            else:
                st.error("Credenciales incorrectas.")
        if st.button("← Volver al Inicio", use_container_width=True):
            navegar("inicio")


def pantalla_registro():
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown('<div class="game-title" style="font-size:1.6rem">📝 Registrar Grupo</div>',
                    unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("form_reg"):
            nombre  = st.text_input("Nombre del grupo", placeholder="Ej: Equipo Titán")
            pw      = st.text_input("Contraseña", type="password")
            pw2     = st.text_input("Confirmar contraseña", type="password")
            sub     = st.form_submit_button("Crear Grupo 🚀", use_container_width=True)
        if sub:
            if not nombre.strip():
                st.error("Nombre requerido.")
            elif len(pw) < 4:
                st.error("Mínimo 4 caracteres.")
            elif pw != pw2:
                st.error("Las contraseñas no coinciden.")
            else:
                from database import registrar_grupo
                ok, gid = registrar_grupo(nombre, pw)
                if ok:
                    st.session_state["grupo_id_registro"] = gid
                    st.session_state["estudiantes_temp"]  = []
                    navegar("agregar_estudiantes")
                else:
                    st.error("Ya existe un grupo con ese nombre.")
        if st.button("← Volver al Inicio", use_container_width=True):
            navegar("inicio")


def pantalla_agregar_estudiantes():
    gid = st.session_state.get("grupo_id_registro")
    if not gid:
        navegar("inicio")
        return

    from database import nombre_grupo_por_id, guardar_estudiante, obtener_progreso
    nombre_grupo = nombre_grupo_por_id(gid)

    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.markdown('<div class="game-title" style="font-size:1.6rem">👥 Agregar Estudiantes</div>',
                    unsafe_allow_html=True)
        st.markdown(f'''<div style="text-align:center;color:rgba(255,255,255,0.5);margin-bottom:12px">
            Grupo <b style="color:#a78bfa">{nombre_grupo}</b></div>''',
                    unsafe_allow_html=True)

        estudiantes = st.session_state["estudiantes_temp"]
        st.progress(len(estudiantes) / MAX_EST,
                    text=f"{len(estudiantes)} / {MAX_EST} estudiantes")

        with st.form("form_est", clear_on_submit=True):
            nombre_est = st.text_input("Nombre completo", placeholder="Ej: Ana López")
            agregar    = st.form_submit_button("➕ Agregar", use_container_width=True)

        if agregar:
            nombre_est = nombre_est.strip()
            if not nombre_est:
                st.error("Nombre vacío.")
            elif not re.match(REGEX_NOMBRE, nombre_est):
                st.error("Solo letras y espacios.")
            elif nombre_est.lower() in [e.lower() for e in estudiantes]:
                st.error("Nombre repetido.")
            elif len(estudiantes) >= MAX_EST:
                st.error(f"Máximo {MAX_EST} estudiantes.")
            else:
                st.session_state["estudiantes_temp"].append(nombre_est)
                st.session_state["msg_est"] = f"✅ {nombre_est} agregado."
                st.rerun()

        if st.session_state.get("msg_est"):
            st.success(st.session_state["msg_est"])
            st.session_state["msg_est"] = ""

        if estudiantes:
            st.markdown("**Estudiantes registrados:**")
            for est in list(estudiantes):
                cn, cb = st.columns([5, 1])
                with cn:
                    st.markdown(
                        f'<span style="color:#e2e8f0;background:rgba(255,255,255,0.05);'
                        f'border:1px solid rgba(255,255,255,0.08);border-radius:8px;'
                        f'padding:5px 12px;display:inline-block;width:100%">{est}</span>',
                        unsafe_allow_html=True)
                with cb:
                    if st.button("✕", key=f"del_{est}"):
                        st.session_state["estudiantes_temp"].remove(est)
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        puede = len(estudiantes) >= MIN_EST
        if not puede:
            st.info(f"Faltan {MIN_EST - len(estudiantes)} estudiante(s) mínimo.")

        ca, cb = st.columns(2)
        with ca:
            if st.button("Cancelar", use_container_width=True):
                navegar("inicio")
        with cb:
            if st.button("✅ Finalizar Registro", disabled=not puede,
                         use_container_width=True):
                for est in estudiantes:
                    guardar_estudiante(gid, est)
                obtener_progreso(gid)
                st.session_state.update({
                    "grupo_id":          gid,
                    "grupo_nombre":      nombre_grupo,
                    "grupo_id_registro": None,
                    "estudiantes_temp":  [],
                    "fase_ronda":        "decision",
                })
                navegar("lobby")
