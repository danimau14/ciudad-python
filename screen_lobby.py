import streamlit as st


def pantalla_lobby():
    from database import (obtenerprogreso, obtenerestudiantes,
                          nombregrupoporid, reiniciarprogreso)
    from session_manager import navegar

    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    nombre_grp  = nombregrupoporid(gid)
    estudiantes = obtenerestudiantes(gid)
    progreso    = obtenerprogreso(gid)

    st.markdown(
        "<h1 style='background:linear-gradient(90deg,#a78bfa,#60a5fa);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "font-size:2rem;margin-bottom:4px'>🏙️ Lobby del Grupo</h1>",
        unsafe_allow_html=True
    )

    # ── Info del grupo ────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Grupo", nombre_grp)
    with c2:
        st.metric("Estudiantes", len(estudiantes))
    with c3:
        ronda = progreso.get("ronda_actual", 1)
        st.metric("Ronda guardada", f"{ronda}/10")

    st.markdown("---")

    # ── Lista de estudiantes ──────────────────────────────────────────────────
    st.markdown("### 👥 Integrantes")
    for i, est in enumerate(estudiantes):
        turno_actual = (ronda - 1) % len(estudiantes)
        es_turno = (i == turno_actual)
        color = "#c4b5fd" if es_turno else "#94a3b8"
        prefijo = "✏️ " if es_turno else ""
        st.markdown(
            f"<div style='background:rgba(255,255,255,0.05);border:1px solid "
            f"{'rgba(167,139,250,0.4)' if es_turno else 'rgba(255,255,255,0.08)'};"
            f"border-radius:10px;padding:10px 16px;margin-bottom:6px;"
            f"color:{color};font-weight:{'700' if es_turno else '400'}'>"
            f"{prefijo}{est}{'  ← turno actual' if es_turno else ''}</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Indicadores actuales ──────────────────────────────────────────────────
    st.markdown("### 📊 Estado actual de la ciudad")
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("💰 Economía",      progreso.get("economia", 50))
    with m2: st.metric("🌿 Medio Ambiente", progreso.get("medioambiente", 50))
    with m3: st.metric("⚡ Energía",         progreso.get("energia", 50))
    with m4: st.metric("❤️ Bienestar",       progreso.get("bienestarsocial", 50))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Acciones ──────────────────────────────────────────────────────────────
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("▶️  CONTINUAR JUEGO", use_container_width=True, type="primary"):
            navegar("juego")
    with b2:
        if st.button("🔄  REINICIAR PARTIDA", use_container_width=True):
            reiniciarprogreso(gid)
            st.session_state.update(
                fase_ronda="decision",
                pregunta_actual=None,
                respuesta_correcta=False,
                decision_elegida=None,
                decision_efectos=None,
                evento_ronda=None,
                preguntas_usadas=[],
                timer_inicio=None,
                tiempo_agotado=False,
            )
            st.success("Partida reiniciada. ¡Lista para empezar!")
            st.rerun()
    with b3:
        if st.button("🏠  VOLVER AL INICIO", use_container_width=True):
            navegar("inicio")
