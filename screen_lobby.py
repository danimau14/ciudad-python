import streamlit as st
from session_manager import navegar
from database import obtener_estrellas


def pantalla_lobby():
    gid          = st.session_state.get("grupo_id")
    nombre_grupo = st.session_state.get("grupo_nombre", "")
    dificultad   = st.session_state.get("dificultad_sel", "Normal")

    if not gid:
        navegar("inicio")
        return

    estrellas = obtener_estrellas(gid)

    # ── Cabecera ──────────────────────────────────────────────
    st.markdown(f'''
    <div style="text-align:center;margin-bottom:8px">
        <div class="game-title" style="font-size:2rem">🏙️ {nombre_grupo}</div>
        <div style="color:#fbbf24;font-size:1.1rem;margin-top:4px">
            {"⭐" * min(estrellas,10)} &nbsp;
            <span style="color:rgba(255,255,255,0.4);font-size:0.85rem">{estrellas} estrellas</span>
        </div>
    </div>''', unsafe_allow_html=True)
    st.markdown("---")

    # ── Selector de dificultad ────────────────────────────────
    st.markdown("### 🎮 Selecciona la dificultad")
    d1, d2, d3 = st.columns(3)
    dif_info = {
        "Fácil":   ("🟢","Penalización ×0.7 · Eventos suaves",  "#10b981"),
        "Normal":  ("🟡","Penalización ×1.0 · Eventos estándar","#f59e0b"),
        "Difícil": ("🔴","Penalización ×1.3 · Eventos intensos", "#ef4444"),
    }
    for col, (dif, (ico, desc, color)) in zip([d1,d2,d3], dif_info.items()):
        with col:
            selec = dificultad == dif
            borde = color if selec else "rgba(255,255,255,0.1)"
            bg    = f"rgba(255,255,255,0.08)" if selec else "rgba(255,255,255,0.03)"
            st.markdown(f'''<div style="background:{bg};border:2px solid {borde};
                border-radius:14px;padding:14px;text-align:center;margin-bottom:8px">
                <div style="font-size:1.5rem">{ico}</div>
                <div style="font-weight:700;color:#f1f5f9">{dif}</div>
                <div style="font-size:0.75rem;color:rgba(255,255,255,0.45);margin-top:4px">{desc}</div>
            </div>''', unsafe_allow_html=True)
            if st.button(f"{'✅ ' if selec else ''}Elegir {dif}", key=f"dif_{dif}",
                         use_container_width=True):
                st.session_state["dificultad_sel"] = dif
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botones principales ───────────────────────────────────
    j1, j2 = st.columns([2, 1])
    with j1:
        if st.button("🚀 JUGAR", use_container_width=True):
            from database import reiniciar_progreso, obtener_progreso
            reiniciar_progreso(gid)
            obtener_progreso(gid)
            st.session_state.update({
                "pregunta_actual": None, "respuesta_correcta": False,
                "decision_elegida": None, "decision_efectos": None,
                "evento_ronda": None, "fase_ronda": "decision",
                "preguntas_usadas": [], "timer_inicio": None,
                "tiempo_agotado": False, "correctas": 0, "incorrectas": 0,
                "logros_partida": [],
            })
            navegar("juego")
    with j2:
        if st.button("📖 Instrucciones", use_container_width=True): navegar("instrucciones")

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🏆 Ranking",   use_container_width=True): navegar("ranking")
    with b2:
        if st.button("📋 Misiones",  use_container_width=True): navegar("misiones")
    with b3:
        if st.button("🏅 Ver Logros",use_container_width=True): navegar("logros")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        for k in ["grupo_id","grupo_nombre","dificultad_sel","dificultad_reg",
                  "estudiantes_temp","logros_partida"]:
            st.session_state[k] = None if k in ["grupo_id"] else ""
        st.session_state["estudiantes_temp"] = []
        st.session_state["logros_partida"]   = []
        navegar("inicio")
