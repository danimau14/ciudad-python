import streamlit as st
from session_manager import navegar
from database import (obtener_progreso, obtener_estudiantes, nombregrupoporid,
                      reiniciar_progreso, obtener_estrellas, obtener_logros_grupo)
from config import IND_COLOR, IND_LABEL, LOGROS, LOGROS_LOBBY

DIF_CFG = {
    "Fácil":   {"color": "#10b981", "bg": "rgba(16,185,129,.08)",  "borde": "rgba(16,185,129,.35)",  "emoji": "🟢", "desc": "Preguntas fáciles · Penalización baja"},
    "Normal":  {"color": "#f59e0b", "bg": "rgba(245,158,11,.08)",  "borde": "rgba(245,158,11,.35)",  "emoji": "🟡", "desc": "Preguntas mixtas · Penalización media"},
    "Difícil": {"color": "#ef4444", "bg": "rgba(239,68,68,.08)",   "borde": "rgba(239,68,68,.35)",   "emoji": "🔴", "desc": "Preguntas difíciles · Penalización alta"},
}


def _ind_mini(label, valor, color, emoji):
    v     = max(0, min(100, valor))
    badge = "Estable"   if v >= 60 else "Precaución" if v >= 30 else "Crítico"
    b_col = "#10b981"   if v >= 60 else "#f59e0b"    if v >= 30 else "#ef4444"
    return (
        f"<div style='background:rgba(255,255,255,.03);border:1px solid {color}22;"
        f"border-radius:12px;padding:10px 14px'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px'>"
        f"<span style='color:#94a3b8;font-size:.72rem'>{emoji} {label}</span>"
        f"<span style='color:{b_col};font-size:.6rem;border:1px solid {b_col}44;"
        f"border-radius:20px;padding:1px 7px'>{badge}</span></div>"
        f"<div style='background:rgba(255,255,255,.07);border-radius:4px;height:6px'>"
        f"<div style='width:{v}%;background:{color};height:6px;border-radius:4px'></div></div>"
        f"<div style='text-align:right;color:{color};font-size:.75rem;font-weight:700;margin-top:3px'>{v}</div>"
        f"</div>"
    )


def pantalla_lobby():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    dif         = st.session_state.get("dificultad_sel", "Normal")
    nombre_grp  = nombregrupoporid(gid)
    estudiantes = obtener_estudiantes(gid)
    progreso    = obtener_progreso(gid, dif)
    estrellas   = obtener_estrellas(gid)
    logros_ids  = set(obtener_logros_grupo(gid))
    ronda       = progreso.get("rondaactual", 1)
    idx_turno   = (ronda - 1) % len(estudiantes) if estudiantes else 0
    dcfg        = DIF_CFG.get(dif, DIF_CFG["Normal"])

    # ══════════════════════════════════════════════════════════════════════════
    # ENCABEZADO
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown(
        f"<div style='background:linear-gradient(135deg,rgba(15,15,30,.97),rgba(20,20,42,.93));"
        f"border:1px solid {dcfg['borde']};border-radius:20px;"
        f"padding:clamp(16px,3vw,24px) clamp(16px,3vw,28px);margin-bottom:20px;"
        f"box-shadow:0 0 40px {dcfg['color']}14'>"

        # Fila 1: nombre + dificultad + estrellas + turno
        f"<div style='display:flex;justify-content:space-between;"
        f"align-items:flex-start;flex-wrap:wrap;gap:10px;margin-bottom:8px'>"
        f"<div>"
        f"<div style='font-family:Press Start 2P,monospace;"
        f"font-size:clamp(.75rem,2.5vw,1.1rem);"
        f"background:linear-gradient(90deg,#a78bfa,#60a5fa);"
        f"-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        f"margin-bottom:8px'>🏙️ {nombre_grp}</div>"
        f"<div style='display:flex;gap:8px;flex-wrap:wrap;align-items:center'>"
        f"<span style='background:{dcfg[\"bg\"]};color:{dcfg[\"color\"]};"
        f"border:1px solid {dcfg[\"borde\"]};border-radius:20px;"
        f"padding:3px 14px;font-size:.75rem;font-weight:700'>"
        f"{dcfg['emoji']} {dif}</span>"
        f"<span style='color:#fbbf24;font-size:.85rem;font-weight:700'>⭐ {estrellas}</span>"
        f"<span style='color:rgba(255,255,255,.3);font-size:.72rem;"
        f"font-family:Courier Prime,monospace'>Ronda {min(ronda-1,10)}/10</span>"
        f"</div></div>"
        f"<div style='text-align:right'>"
        f"<div style='font-size:.60rem;color:rgba(255,255,255,.3);"
        f"font-family:Courier Prime,monospace;margin-bottom:3px'>TURNO ACTUAL</div>"
        f"<div style='font-size:.95rem;font-weight:700;color:#c4b5fd'>"
        f"{estudiantes[idx_turno] if estudiantes else '—'}</div>"
        f"</div></div>"
        f"</div>",
        unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # DOS COLUMNAS: Izquierda (dificultad + JUGAR + estado) | Derecha (equipo + logros)
    # ══════════════════════════════════════════════════════════════════════════
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        # ── Botonera secundaria ANTES de la dificultad ───────────────────────
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🏆  RANKING", use_container_width=True):
                navegar("ranking")
        with b2:
            if st.button("📋  MISIONES", use_container_width=True):
                navegar("misiones")
        with b3:
            if st.button("🏅  VER LOGROS", use_container_width=True):
                navegar("logros")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📖  INSTRUCCIONES", use_container_width=True):
                navegar("instrucciones")
        with c2:
            if st.button("🔄  REINICIAR PARTIDA", use_container_width=True):
                reiniciar_progreso(gid, dif)
                st.session_state.update(
                    fase_ronda="decision", pregunta_actual=None,
                    respuesta_correcta=False, decision_elegida=None,
                    decision_efectos=None, evento_ronda=None,
                    preguntas_usadas=[], timer_inicio=None,
                    tiempo_agotado=False, correctas=0, incorrectas=0,
                    _ranking_guardado=False,
                    decisiones_usadas_partida=set(),
                    mejor_racha=0, racha_actual=0,
                    atributos_activos=set(),
                )
                st.success(f"✅ Partida reiniciada para {dif}")
                st.rerun()
        with c3:
            if st.button("🚪  CERRAR SESIÓN", use_container_width=True):
                st.session_state.clear()
                navegar("inicio")

        st.markdown(
            f"<hr style='border:none;border-top:1px solid {dcfg['color']}22;"
            f"margin:14px 0 12px'>",
            unsafe_allow_html=True)

        # ── Selector de dificultad ────────────────────────────────────────────
        st.markdown(
            "<div style='font-family:Courier Prime,monospace;font-size:.65rem;"
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.3);"
            "margin-bottom:8px'>⚙️ Selecciona Dificultad</div>",
            unsafe_allow_html=True)

        for d in ["Fácil", "Normal", "Difícil"]:
            cfg    = DIF_CFG[d]
            activa = (d == dif)
            bg_btn  = cfg["bg"]    if activa else "rgba(255,255,255,.02)"
            brd_btn = cfg["borde"] if activa else "rgba(255,255,255,.07)"
            col_txt = cfg["color"] if activa else "#64748b"
            glow    = f"box-shadow:0 0 18px {cfg['color']}28;" if activa else ""
            check   = f"<span style='color:{cfg['color']};font-size:1rem'>✓</span>" if activa else ""
            st.markdown(
                f"<div style='background:{bg_btn};border:1px solid {brd_btn};"
                f"border-radius:12px;padding:10px 14px;margin-bottom:5px;{glow}'>"
                f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                f"<div><span style='color:{col_txt};font-weight:700;font-size:.86rem'>"
                f"{cfg['emoji']} {d}</span>"
                f"<div style='color:rgba(255,255,255,.28);font-size:.66rem;margin-top:2px'>"
                f"{cfg['desc']}</div></div>{check}</div></div>",
                unsafe_allow_html=True)
            if st.button(f"Seleccionar {d}", key=f"dif_{d}",
                         use_container_width=True,
                         type="primary" if activa else "secondary"):
                st.session_state["dificultad_sel"] = d
                st.rerun()

        # ── Botón JUGAR — justo después de los niveles ────────────────────────
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='height:2px;background:linear-gradient(90deg,"
            f"transparent,{dcfg['color']}66,transparent);"
            f"margin-bottom:12px;border-radius:2px'></div>",
            unsafe_allow_html=True)
        if st.button("▶️  JUGAR", use_container_width=True, type="primary"):
            navegar("juego")

        # ── Estado de la ciudad ───────────────────────────────────────────────
        st.markdown(
            "<div style='font-family:Courier Prime,monospace;font-size:.65rem;"
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.3);"
            "margin:18px 0 8px'>📊 Estado de la Ciudad</div>",
            unsafe_allow_html=True)
        vals = {
            "economia":         progreso.get("economia", 50),
            "medio_ambiente":   progreso.get("medioambiente", 50),
            "energia":          progreso.get("energia", 50),
            "bienestar_social": progreso.get("bienestarsocial", 50),
        }
        ind_html = "".join(
            _ind_mini(IND_LABEL[k], vals[k], IND_COLOR[k][0], IND_COLOR[k][1])
            for k in vals)
        st.markdown(
            f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>"
            f"{ind_html}</div>",
            unsafe_allow_html=True)

    with col_der:
        # ── Equipo ────────────────────────────────────────────────────────────
        st.markdown(
            "<div style='font-family:Courier Prime,monospace;font-size:.65rem;"
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.3);"
            "margin-bottom:8px'>👥 Equipo</div>",
            unsafe_allow_html=True)
        for i, est in enumerate(estudiantes):
            es_turno  = (i == idx_turno)
            bg_e  = "rgba(167,139,250,.12)" if es_turno else "rgba(255,255,255,.02)"
            brd_e = "rgba(167,139,250,.4)"  if es_turno else "rgba(255,255,255,.06)"
            turno_badge = (
                "<div style='color:#a78bfa;font-size:.60rem;margin-top:2px'>✦ Turno actual</div>"
                if es_turno else "")
            st.markdown(
                f"<div style='background:{bg_e};border:1px solid {brd_e};"
                f"border-radius:12px;padding:9px 13px;margin-bottom:5px;"
                f"display:flex;align-items:center;gap:9px'>"
                f"<span style='font-size:1.1rem'>{'✏️' if es_turno else '👤'}</span>"
                f"<div><div style='color:{'#c4b5fd' if es_turno else '#64748b'};"
                f"font-weight:{'700' if es_turno else '400'};font-size:.83rem'>{est}</div>"
                f"{turno_badge}</div></div>",
                unsafe_allow_html=True)

        # ── Logros destacados ─────────────────────────────────────────────────
        st.markdown(
            "<div style='font-family:Courier Prime,monospace;font-size:.65rem;"
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.3);"
            "margin:14px 0 8px'>🏅 Logros</div>",
            unsafe_allow_html=True)
        logros_dest = [l for l in LOGROS if l["id"] in LOGROS_LOBBY]
        chips = ""
        for logro in logros_dest:
            ob    = logro["id"] in logros_ids
            emoji = logro["emoji"] if ob else "🔒"
            color = "#a78bfa"              if ob else "rgba(255,255,255,.15)"
            bg_l  = "rgba(124,58,237,.12)" if ob else "rgba(255,255,255,.02)"
            brd_l = "rgba(124,58,237,.35)" if ob else "rgba(255,255,255,.06)"
            nom   = logro["nombre"]        if ob else "???"
            filt  = "none"                 if ob else "grayscale(1) opacity(.3)"
            chips += (
                f"<div style='background:{bg_l};border:1px solid {brd_l};"
                f"border-radius:10px;padding:7px;text-align:center'>"
                f"<div style='font-size:1.1rem;filter:{filt}'>{emoji}</div>"
                f"<div style='font-size:.50rem;color:{color};"
                f"font-family:Courier Prime,monospace;margin-top:2px;line-height:1.2'>"
                f"{nom}</div></div>")
        st.markdown(
            f"<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:5px'>"
            f"{chips}</div>",
            unsafe_allow_html=True)


