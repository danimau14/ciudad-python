import re
import streamlit as st
from navigation import navegar
from config import MIN_EST, MAX_EST, REGEX_NOMBRE
from database import guardar_estudiante, obtener_estudiantes, registrar_grupo, obtener_progreso


def pantalla_agregar_estudiantes():
    # El grupo aún no está en DB — verificar que se pasó por pantalla_registro
    if not st.session_state.get("reg_nombre_temp"):
        navegar("inicio"); return
    gid = None  # se asignará al finalizar

    # Nombre del grupo viene de session_state (aún no está en DB)
    nombre_grupo = st.session_state.get("reg_nombre_temp", "Nuevo Grupo")
    _,col,_ = st.columns([0.5,3,0.5])
    with col:
        # Título
        st.markdown(
            "<div style='text-align:center;padding:6px 0 2px;'>"
            "<span class='emoji-title' style='font-size:2.2rem;'>👨‍🎓</span></div>"
            "<div class='game-title' style='font-size:1.5rem;letter-spacing:3px;'>AGREGAR OPERADORES</div>"
            "<div class='game-sub' style='font-size:.7rem;'>EQUIPO DE INGENIERÍA</div>",
            unsafe_allow_html=True)

        # Info del grupo
        st.markdown(
            "<div style='background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);"
            "border-radius:8px;padding:8px 14px;text-align:center;margin-bottom:14px;'>"
            "<span style='color:rgba(0,212,255,0.5);font-size:0.72rem;font-family:Orbitron,sans-serif;"
            "letter-spacing:2px;'>GRUPO: </span>"
            "<span style='color:#00d4ff;font-weight:700;font-family:Orbitron,sans-serif;'>"
            +nombre_grupo+"</span></div>", unsafe_allow_html=True)

        estudiantes = st.session_state.get("estudiantes_temp", [])
        n = len(estudiantes)

        # Barra de progreso
        pct_est = int(n / MAX_EST * 100)
        st.markdown(
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;margin-bottom:6px;'>"
            "<span style='font-family:Orbitron,sans-serif;font-size:0.6rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:2px;'>OPERADORES</span>"
            "<span style='font-family:Orbitron,sans-serif;font-size:0.75rem;"
            "color:#00d4ff;font-weight:700;'>"+str(n)+" / "+str(MAX_EST)+"</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,0.06);border-radius:3px;"
            "height:6px;overflow:hidden;margin-bottom:14px;'>"
            "<div style='width:"+str(pct_est)+"%;height:6px;border-radius:3px;"
            "background:linear-gradient(90deg,#00d4ff,#8b5cf6);"
            "box-shadow:0 0 8px rgba(0,212,255,0.5);transition:width .4s;'></div>"
            "</div>", unsafe_allow_html=True)

        # Input + botón (sin st.form para evitar bugs de estado)
        if n < MAX_EST:
            nombre_est = st.text_input(
                "👤 Nombre completo del operador",
                placeholder="Ej: Ana López",
                key="input_est_nombre")

            if st.button("➕ AGREGAR OPERADOR", use_container_width=True, key="btn_agregar"):
                nombre_est = nombre_est.strip()
                if not nombre_est:
                    st.error("⚠️ El nombre no puede estar vacío.")
                elif not re.match(REGEX_NOMBRE, nombre_est):
                    st.error("⚠️ Solo se permiten letras y espacios.")
                elif nombre_est.lower() in [e.lower() for e in estudiantes]:
                    st.error("⚠️ Ya existe un operador con ese nombre.")
                else:
                    st.session_state["estudiantes_temp"].append(nombre_est)
                    st.session_state["msg_est"] = "✅ " + nombre_est + " agregado al equipo."
                    st.rerun()
        else:
            st.markdown(
                "<div style='background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);"
                "border-radius:8px;padding:10px;text-align:center;margin-bottom:10px;'>"
                "<span style='color:#22c55e;font-family:Orbitron,sans-serif;font-size:0.75rem;'>"
                "✅ EQUIPO COMPLETO ("+str(MAX_EST)+" operadores)</span></div>",
                unsafe_allow_html=True)

        # Mensaje de éxito
        if st.session_state.get("msg_est"):
            st.success(st.session_state["msg_est"])
            st.session_state["msg_est"] = ""

        # Lista de estudiantes agregados
        if estudiantes:
            st.markdown(
                "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
                "color:rgba(0,212,255,0.5);letter-spacing:2px;margin:10px 0 8px;'>"
                "EQUIPO ACTUAL</div>", unsafe_allow_html=True)
            for idx_e, est in enumerate(list(estudiantes)):
                cn, cb = st.columns([5, 1])
                with cn:
                    st.markdown(
                        "<div style='background:rgba(0,212,255,0.05);"
                        "border:1px solid rgba(0,212,255,0.18);border-radius:8px;"
                        "padding:8px 14px;margin-bottom:4px;display:flex;align-items:center;gap:8px;'>"
                        "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>👤</span>"
                        "<span style='color:#e2e8f0;font-size:0.9rem;'>"+est+"</span>"
                        "<span style='margin-left:auto;font-family:Orbitron,sans-serif;"
                        "font-size:0.6rem;color:rgba(0,212,255,0.4);'>#"+str(idx_e+1)+"</span>"
                        "</div>", unsafe_allow_html=True)
                with cb:
                    if st.button("✕", key="del_"+str(idx_e)+"_"+est,
                                 use_container_width=True):
                        st.session_state["estudiantes_temp"].remove(est)
                        st.rerun()

        # Requisito mínimo
        st.markdown("<br>", unsafe_allow_html=True)
        puede = n >= MIN_EST

        if not puede:
            faltantes = MIN_EST - n
            st.markdown(
                "<div style='background:rgba(245,158,11,0.08);"
                "border:1px solid rgba(245,158,11,0.3);border-radius:8px;"
                "padding:10px 14px;text-align:center;margin-bottom:10px;'>"
                "<span style='font-family:Orbitron,sans-serif;font-size:0.7rem;"
                "color:#f59e0b;'>⚠️ FALTAN "+str(faltantes)+" OPERADOR"
                +("ES" if faltantes>1 else "")+" MÍNIMO</span></div>",
                unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            if st.button("⬅️ CANCELAR", use_container_width=True, key="btn_cancel_est"):
                st.session_state["estudiantes_temp"] = []
                navegar("inicio")
        with cb:
            if st.button(
                "🚀 INICIAR MISIÓN" if puede else "🔒 MÍNIMO "+str(MIN_EST)+" OPERADORES",
                disabled=not puede,
                use_container_width=True,
                key="btn_finalizar_est"
            ):
                # Registrar el grupo en DB solo ahora que tiene los estudiantes mínimos
                nombre_reg = st.session_state.get("reg_nombre_temp","")
                pw_reg     = st.session_state.get("reg_pw_temp","")
                dif_reg = st.session_state.get("dificultad", "Medio")
                new_gid = registrar_grupo(nombre_reg, pw_reg, dif_reg)
                if new_gid is None:
                    st.error("⚠️ Ya existe un grupo con ese nombre. Vuelve y elige otro.")
                else:
                    for est in estudiantes:
                        guardar_estudiante(new_gid, est)
                    obtener_progreso(new_gid)
                    st.session_state["grupo_id"]          = new_gid
                    st.session_state["grupo_nombre"]      = nombre_reg
                    st.session_state["dificultad"]        = dif_reg
                    st.session_state["grupo_id_registro"] = None
                    st.session_state["estudiantes_temp"]  = []
                    st.session_state["reg_nombre_temp"]   = ""
                    st.session_state["reg_pw_temp"]       = ""
                    st.session_state["fase_ronda"]        = "decision"
                    navegar("juego")
