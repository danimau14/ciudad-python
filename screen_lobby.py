import streamlit as st
from session_manager import navegar
from database import obtener_estrellas, reiniciar_progreso, obtener_progreso


def pantalla_lobby():
    gid          = st.session_state.get("grupo_id")
    nombre_grupo = st.session_state.get("grupo_nombre", "")
    dif_sel      = st.session_state.get("dificultad_sel", "Normal")

    if not gid:
        navegar("inicio")
        return

    estrellas = obtener_estrellas(gid)

    # ── Cabecera ──────────────────────────────────────────────────────────────
    st.markdown(f'''<div style="text-align:center;margin-bottom:8px">
        <div class="game-title" style="font-size:2.2rem">🏙️ {nombre_grupo}</div>
        <div style="color:#fbbf24;font-size:1.1rem;margin-top:6px">
            {"⭐" * min(estrellas, 10)}
            <span style="color:rgba(255,255,255,0.35);font-size:0.82rem;margin-left:8px">
                {estrellas} estrellas acumuladas</span>
        </div>
    </div>''', unsafe_allow_html=True)
    st.markdown("---")

    # ── Selector dificultad ───────────────────────────────────────────────────
    st.markdown('### 🎮 Selecciona la dificultad')
    dif_info = {
        "Fácil":   ("🟢", "#10b981", "Penalización ×0.7 · Eventos suaves"),
        "Normal":  ("🟡", "#f59e0b", "Penalización ×1.0 · Eventos estándar"),
        "Difícil": ("🔴", "#ef4444", "Penalización ×1.3 · Eventos intensos"),
    }
    d1, d2, d3 = st.columns(3)
    for col, (dif, (ico, color, desc)) in zip([d1, d2, d3], dif_info.items()):
        with col:
            selec = dif_sel == dif
            st.markdown(f'''<div style="background:{"rgba(255,255,255,0.08)" if selec else "rgba(255,255,255,0.02)"};
                border:2px solid {color if selec else "rgba(255,255,255,0.08)"};
                border-radius:14px;padding:14px;text-align:center;margin-bottom:8px">
                <div style="font-size:1.6rem">{ico}</div>
                <div style="font-weight:700;color:#f1f5f9;font-size:0.95rem">{dif}</div>
                <div style="font-size:0.72rem;color:rgba(255,255,255,0.4);margin-top:4px">{desc}</div>
            </div>''', unsafe_allow_html=True)
            label = f"✅ {dif}" if selec else f"Elegir {dif}"
            if st.button(label, key=f"dif_{dif}", use_container_width=True):
                st.session_state["dificultad_sel"] = dif
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── JUGAR ─────────────────────────────────────────────────────────────────
    j1, j2 = st.columns([2, 1])
    with j1:
        if st.button("🚀 JUGAR", use_container_width=True):
            reiniciar_progreso(gid)
            obtener_progreso(gid)
            st.session_state.update({
                "pregunta_actual":   None, "respuesta_correcta": False,
                "decision_elegida":  None, "decision_efectos":   None,
                "evento_ronda":      None, "fase_ronda":         "decision",
                "preguntas_usadas":  [],   "timer_inicio":       None,
                "tiempo_agotado":    False,"correctas":          0,
                "incorrectas":       0,    "logros_partida":     [],
                "_ranking_guardado": False,
            })
            navegar("juego")
    with j2:
        if st.button("📖 Instrucciones", use_container_width=True):
            navegar("instrucciones")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Menú secundario ───────────────────────────────────────────────────────
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🏆 Ranking",    use_container_width=True): navegar("ranking")
    with b2:
        if st.button("📋 Misiones",   use_container_width=True): navegar("misiones")
    with b3:
        if st.button("🏅 Ver Logros", use_container_width=True): navegar("logros")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.update({
            "grupo_id": None, "grupo_nombre": "",
            "dificultad_sel": "Normal", "logros_obtenidos": [],
        })
        navegar("inicio")
