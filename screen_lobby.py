import streamlit as st
from session_manager import navegar
from database import (obtener_progreso, obtener_estudiantes, nombregrupoporid,
                      reiniciar_progreso, obtener_estrellas, obtener_logros_grupo)
from config import IND_COLOR, IND_LABEL, LOGROS, LOGROS_LOBBY
from ui_styles import pixel_header, pixel_divider, stat_badge


def pantalla_lobby():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    nombre_grp  = nombregrupoporid(gid)
    estudiantes = obtener_estudiantes(gid)
    progreso    = obtener_progreso(gid)
    estrellas   = obtener_estrellas(gid)
    logros_ids  = set(obtener_logros_grupo(gid))
    ronda       = progreso.get("rondaactual", 1)
    dif         = st.session_state.get("dificultad_sel", "Normal")

    pixel_header(nombre_grp, f"Lobby · {dif} · {estrellas} ⭐", "🏙️")

    # ── Indicadores rápidos ────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    vals = {
        "economia":         progreso.get("economia", 50),
        "medio_ambiente":   progreso.get("medioambiente", 50),
        "energia":          progreso.get("energia", 50),
        "bienestar_social": progreso.get("bienestarsocial", 50),
    }
    for col, key in zip([m1,m2,m3,m4], vals):
        color, emoji = IND_COLOR[key]
        with col:
            st.metric(f"{emoji} {IND_LABEL[key]}", vals[key])

    pixel_divider("#a78bfa")

    # ── Estudiantes ────────────────────────────────────────────────────────────
    st.markdown("### 👥 Integrantes del Equipo")
    idx_turno = (ronda - 1) % len(estudiantes) if estudiantes else 0
    cols = st.columns(len(estudiantes)) if estudiantes else []
    for i, (col, est) in enumerate(zip(cols, estudiantes)):
        es_turno = (i == idx_turno)
        with col:
            st.markdown(
                f"<div style='background:{'rgba(167,139,250,0.15)' if es_turno else 'rgba(255,255,255,0.04)'};"
                f"border:1px solid {'rgba(167,139,250,0.5)' if es_turno else 'rgba(255,255,255,0.08)'};"
                f"border-radius:12px;padding:14px;text-align:center;margin-bottom:8px'>"
                f"<div style='font-size:1.5rem'>{'✏️' if es_turno else '👤'}</div>"
                f"<div style='color:{'#c4b5fd' if es_turno else '#94a3b8'};"
                f"font-weight:{'700' if es_turno else '400'};font-size:.85rem;"
                f"margin-top:6px'>{est}</div>"
                f"{'<div style=chr(39)color:#a78bfa;font-size:.7rem;margin-top:4px chr(39)>Turno actual</div>' if es_turno else ''}"
                f"</div>",
                unsafe_allow_html=True)

    pixel_divider("#60a5fa")

    # ── Dificultad ─────────────────────────────────────────────────────────────
    st.markdown("### ⚙️ Dificultad de Partida")
    dif_opts = ["Fácil", "Normal", "Difícil"]
    dif_actual = st.session_state.get("dificultad_sel", "Normal")
    nueva_dif = st.radio("", dif_opts,
                         index=dif_opts.index(dif_actual),
                         horizontal=True, key="dif_radio_lobby")
    st.session_state["dificultad_sel"] = nueva_dif

    pixel_divider("#34d399")

    # ── Logros destacados ──────────────────────────────────────────────────────
    st.markdown("### 🏅 Logros Destacados")
    logros_dest = [l for l in LOGROS if l["id"] in LOGROS_LOBBY]
    cols2 = st.columns(len(logros_dest))
    for col, logro in zip(cols2, logros_dest):
        obtenido = logro["id"] in logros_ids
        color    = "#a78bfa" if obtenido else "rgba(255,255,255,.12)"
        bg       = "rgba(124,58,237,.1)" if obtenido else "rgba(15,15,25,.5)"
        borde    = "rgba(124,58,237,.4)" if obtenido else "rgba(255,255,255,.05)"
        emoji    = logro["emoji"] if obtenido else "🔒"
        with col:
            st.markdown(
                f"<div style='background:{bg};border:1px solid {borde};"
                f"border-radius:12px;padding:10px;text-align:center;min-height:90px'>"
                f"<div style='font-size:1.4rem;filter:{'none' if obtenido else 'grayscale(1) opacity(.3)'}'>"
                f"{emoji}</div>"
                f"<div style='font-size:.58rem;color:{color};"
                f"font-family:Courier Prime,monospace;line-height:1.3;margin-top:5px'>"
                f"{logro['nombre'] if obtenido else '???'}</div></div>",
                unsafe_allow_html=True)

    pixel_divider("#a78bfa")

    # ── Navegación ─────────────────────────────────────────────────────────────
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        if st.button("▶️  JUGAR", use_container_width=True, type="primary"):
            navegar("juego")
    with b2:
        if st.button("🏆  RANKING", use_container_width=True):
            navegar("ranking")
    with b3:
        if st.button("📋  MISIONES", use_container_width=True):
            navegar("misiones")
    with b4:
        if st.button("🏅  LOGROS", use_container_width=True):
            navegar("logros")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📖  INSTRUCCIONES", use_container_width=True):
            navegar("instrucciones")
    with c2:
        if st.button("🔄  REINICIAR PARTIDA", use_container_width=True):
            reiniciar_progreso(gid)
            st.session_state.update(
                fase_ronda="decision", pregunta_actual=None,
                respuesta_correcta=False, decision_elegida=None,
                decision_efectos=None, evento_ronda=None,
                preguntas_usadas=[], timer_inicio=None,
                tiempo_agotado=False, correctas=0, incorrectas=0,
                _ranking_guardado=False,
            )
            st.success("Partida reiniciada. ¡Lista para empezar!")
            st.rerun()
