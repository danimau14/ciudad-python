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
        "<div style='background:rgba(255,255,255,.03);border:1px solid " + color + "22;"
        "border-radius:12px;padding:10px 14px'>"
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px'>"
        "<span style='color:#94a3b8;font-size:.72rem'>" + emoji + " " + label + "</span>"
        "<span style='color:" + b_col + ";font-size:.6rem;border:1px solid " + b_col + "44;"
        "border-radius:20px;padding:1px 7px'>" + badge + "</span></div>"
        "<div style='background:rgba(255,255,255,.07);border-radius:4px;height:6px'>"
        "<div style='width:" + str(v) + "%;background:" + color + ";height:6px;border-radius:4px'></div></div>"
        "<div style='text-align:right;color:" + color + ";font-size:.75rem;font-weight:700;margin-top:3px'>" + str(v) + "</div>"
        "</div>"
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

    # ── ENCABEZADO ────────────────────────────────────────────────────────────
    turno_actual = estudiantes[idx_turno] if estudiantes else "—"
    st.markdown(
        "<div style='background:linear-gradient(135deg,rgba(15,15,30,.97),rgba(20,20,42,.93));"
        "border:1px solid " + dcfg['borde'] + ";border-radius:20px;"
        "padding:20px 24px;margin-bottom:20px;"
        "box-shadow:0 0 40px " + dcfg['color'] + "14'>"
        "<div style='display:flex;justify-content:space-between;"
        "align-items:flex-start;flex-wrap:wrap;gap:10px;margin-bottom:8px'>"
        "<div>"
        "<div style='font-family:Press Start 2P,monospace;"
        "font-size:clamp(.75rem,2.5vw,1.1rem);"
        "background:linear-gradient(90deg,#a78bfa,#60a5fa);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:8px'>🏙️ " + nombre_grp + "</div>"
        "<div style='display:flex;gap:8px;flex-wrap:wrap;align-items:center'>"
        "<span style='background:" + dcfg['bg'] + ";color:" + dcfg['color'] + ";"
        "border:1px solid " + dcfg['borde'] + ";border-radius:20px;"
        "padding:3px 14px;font-size:.75rem;font-weight:700'>"
        + dcfg['emoji'] + " " + dif + "</span>"
        "<span style='color:#fbbf24;font-size:.85rem;font-weight:700'>⭐ " + str(estrellas) + "</span>"
        "<span style='color:rgba(255,255,255,.3);font-size:.72rem;"
        "font-family:Courier Prime,monospace'>Ronda " + str(min(ronda-1, 10)) + "/10</span>"
        "</div></div>"
        "<div style='text-align:right'>"
        "<div style='font-size:.60rem;color:rgba(255,255,255,.3);"
        "font-family:Courier Prime,monospace;margin-bottom:3px'>TURNO ACTUAL</div>"
        "<div style='font-size:.95rem;font-weight:700;color:#c4b5fd'>"
        + turno_actual + "</div>"
        "</div></div></div>",
        unsafe_allow_html=True)

    # ── DOS COLUMNAS ──────────────────────────────────────────────────────────
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        # ── 1) Botones secundarios PRIMERO ───────────────────────────────────
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🏆  RANKING", use_container_width=True):
                navegar("ranking")
        with b2:
            if st.button("📋  MISIONES", use_container_width=True):
                navegar("misiones")
        with b3:
            if st.button("🏅  LOGROS", use_container_width=True):
                navegar("logros")

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📖  INSTRUCCIONES", use_container_width=True):
                navegar("instrucciones")
        with c2:
            if st.button("🔄  REINICIAR", use_container_width=True):
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
                st.success("✅ Partida reiniciada para " + dif)
                st.rerun()
        with c3:
            if st.button("🚪  CERRAR SESIÓN", use_container_width=True):
                st.session_state.clear()
                navegar("inicio")

        st.markdown(
            "<hr style='border:none;border-top:1px solid " + dcfg['color'] + "22;margin:14px 0 12px'>",
            unsafe_allow_html=True)

        # ── 2) Selector de dificultad ─────────────────────────────────────────
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
            glow    = "box-shadow:0 0 18px " + cfg["color"] + "28;" if activa else ""
            check   = "<span style='color:" + cfg["color"] + ";font-size:1rem'>✓</span>" if activa else ""
            st.markdown(
                "<div style='background:" + bg_btn + ";border:1px solid " + brd_btn + ";"
                "border-radius:12px;padding:10px 14px;margin-bottom:5px;" + glow + "'>"
                "<div style='display:flex;justify-content:space-between;align-items:center'>"
                "<div><span style='color:" + col_txt + ";font-weight:700;font-size:.86rem'>"
                + cfg["emoji"] + " " + d + "</span>"
                "<div style='color:rgba(255,255,255,.28);font-size:.66rem;margin-top:2px'>"
                + cfg["desc"] + "</div></div>" + check + "</div></div>",
                unsafe_allow_html=True)
            if st.button("Seleccionar " + d, key="dif_" + d,
                         use_container_width=True,
                         type="primary" if activa else "secondary"):
                st.session_state["dificultad_sel"] = d
                st.rerun()

        # ── 3) Botón JUGAR justo después de dificultad ───────────────────────
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='height:2px;background:linear-gradient(90deg,"
            "transparent," + dcfg['color'] + "66,transparent);"
            "margin-bottom:12px;border-radius:2px'></div>",
            unsafe_allow_html=True)
        if st.button("▶️  JUGAR", use_container_width=True, type="primary"):
            navegar("juego")

        # ── 4) Estado de la ciudad ────────────────────────────────────────────
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
            "<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>"
            + ind_html + "</div>",
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
            icon  = "✏️" if es_turno else "👤"
            col_n = "#c4b5fd" if es_turno else "#64748b"
            fw    = "700"     if es_turno else "400"
            turno_b = "<div style='color:#a78bfa;font-size:.60rem;margin-top:2px'>✦ Turno actual</div>" if es_turno else ""
            st.markdown(
                "<div style='background:" + bg_e + ";border:1px solid " + brd_e + ";"
                "border-radius:12px;padding:9px 13px;margin-bottom:5px;"
                "display:flex;align-items:center;gap:9px'>"
                "<span style='font-size:1.1rem'>" + icon + "</span>"
                "<div><div style='color:" + col_n + ";font-weight:" + fw + ";font-size:.83rem'>"
                + est + "</div>" + turno_b + "</div></div>",
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
                "<div style='background:" + bg_l + ";border:1px solid " + brd_l + ";"
                "border-radius:10px;padding:7px;text-align:center'>"
                "<div style='font-size:1.1rem;filter:" + filt + "'>" + emoji + "</div>"
                "<div style='font-size:.50rem;color:" + color + ";"
                "font-family:Courier Prime,monospace;margin-top:2px;line-height:1.2'>"
                + nom + "</div></div>")
        st.markdown(
            "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:5px'>"
            + chips + "</div>",
            unsafe_allow_html=True)
