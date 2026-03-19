import streamlit as st
from session_manager import navegar
from database import (obtener_progreso, reiniciar_progreso, obtener_estrellas,
                      guardar_estrellas, guardar_logro, guardar_mision,
                      guardar_mision_pendiente, obtener_misiones_canjeadas,
                      obtener_misiones_pendientes, eliminar_mision_pendiente,
                      guardar_ranking, obtener_logros_grupo)
from config import IND_COLOR, IND_LABEL, DIFICULTADES, LOGROS, MISIONES


def _clamp(v): return max(0, min(100, v))


def _badge_estrellas(gid):
    """Badge de estrellas reutilizable para mostrar en pantallas."""
    total = obtener_estrellas(gid) if gid else 0
    return (
        "<span style='display:inline-flex;align-items:center;gap:5px;"
        "background:rgba(251,191,36,.12);color:#fbbf24;"
        "border:1px solid rgba(251,191,36,.35);border-radius:20px;"
        "padding:4px 14px;font-family:Courier Prime,monospace;"
        "font-size:.80rem;font-weight:800;"
        "box-shadow:0 0 10px rgba(251,191,36,.18)'>⭐ " + str(total) + " estrellas</span>"
    )


def _evaluar_misiones_partida(gid, ind_fin, correctas, rondas, dif):
    """
    Detecta misiones completadas esta partida que NO han sido canjeadas aún.
    Las guarda en misiones_pendientes (database.db) para que estén disponibles
    en la pantalla de misiones si no se canjean aquí.
    """
    ya_canjeadas  = set(obtener_misiones_canjeadas(gid))
    ya_pendientes = {p["id"] for p in obtener_misiones_pendientes(gid)}
    nuevas = []

    for m in MISIONES:
        mid = m["id"]
        if mid in ya_canjeadas or mid in ya_pendientes:
            continue
        tipo = m.get("tipo", ""); meta = m.get("meta", 1); ok = False
        if   tipo == "partidas"          : ok = rondas >= 10
        elif tipo == "racha"             : ok = st.session_state.get("mejor_racha", 0) >= meta
        elif tipo == "indicador"         : ok = ind_fin.get(m.get("ind", ""), 0) >= meta
        elif tipo == "sin_rojo"          : ok = all(v >= 30 for v in ind_fin.values())
        elif tipo == "victoria"          : ok = rondas >= 10 and m.get("dif","todas") in ("todas", dif)
        elif tipo == "correctas"         : ok = correctas >= meta
        elif tipo == "todos_sobre"       : ok = all(v >= meta for v in ind_fin.values())
        elif tipo == "decisiones_usadas" : ok = len(st.session_state.get("decisiones_usadas_partida", set())) >= meta
        if ok:
            # Guardar como pendiente en database.db
            guardar_mision_pendiente(gid, mid, m["recompensa"])
            nuevas.append(m)
    return nuevas


def _evaluar_logros(gid, ind_fin, correctas, rondas, dif):
    ya = set(obtener_logros_grupo(gid))
    for l in LOGROS:
        if l["id"] in ya: continue
        tipo = l.get("tipo",""); meta = l.get("meta",1); ok = False
        if   tipo == "partidas"         : ok = rondas >= 10
        elif tipo == "correctas_partida": ok = correctas >= meta
        elif tipo == "victoria"         : ok = rondas >= 10 and l.get("dif","todas") in ("todas", dif)
        elif tipo == "indicador_fin"    : ok = ind_fin.get(l.get("ind",""), 0) >= meta
        elif tipo == "todos_sobre"      : ok = all(v >= meta for v in ind_fin.values())
        elif tipo == "racha"            : ok = st.session_state.get("mejor_racha", 0) >= meta
        elif tipo == "decisiones_todas" : ok = len(st.session_state.get("decisiones_usadas_partida", set())) >= meta
        elif tipo == "tam_grupo":
            from database import obtener_estudiantes
            ok = len(obtener_estudiantes(gid)) >= meta
        if ok: guardar_logro(gid, l["id"])


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA FINAL
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_fin():
    gid         = st.session_state.get("grupo_id")
    resultado   = st.session_state.get("resultado", "desconocido")
    ind_fin     = st.session_state.get("indicadores_finales", {})
    rondas_comp = st.session_state.get("rondas_completadas", 0)
    correctas   = st.session_state.get("correctas", 0)
    incorrectas = st.session_state.get("incorrectas", 0)
    dif         = st.session_state.get("dificultad_sel", "Normal")
    dif_cfg     = DIFICULTADES.get(dif, DIFICULTADES["Normal"])
    DIF_COL     = {"Fácil": "#10b981", "Normal": "#f59e0b", "Difícil": "#ef4444"}
    col_dif     = DIF_COL.get(dif, "#a78bfa")
    est_victoria = dif_cfg.get("estrellas", 2) if resultado == "victoria" else 0

    # ── Guardar resultados UNA sola vez ───────────────────────────────────────
    if gid and not st.session_state.get("_ranking_guardado"):
        if est_victoria > 0:
            guardar_estrellas(gid, est_victoria)   # → database.db
        puntaje = int(sum(ind_fin.values()) / 4) if ind_fin else 0
        guardar_ranking(gid, puntaje, dif)          # → database.db
        _evaluar_logros(gid, ind_fin, correctas, rondas_comp, dif)
        # Misiones: evaluar y guardar pendientes en database.db
        _evaluar_misiones_partida(gid, ind_fin, correctas, rondas_comp, dif)
        st.session_state["_ranking_guardado"] = True

    # Leer estrellas actuales desde database.db
    total_est = obtener_estrellas(gid) if gid else 0
    # Leer misiones pendientes desde database.db (incluye las de esta partida)
    pendientes_db = obtener_misiones_pendientes(gid) if gid else []
    # Dict rápido id→misión completa
    mision_map = {m["id"]: m for m in MISIONES}

    # ══ BANNER RESULTADO (mismo diseño visual) ═══════════════════════════════
    if resultado == "victoria":
        st.balloons()
        col_r = "#10b981"; bg_r = "rgba(16,185,129,.1)"; ico = "🏆"
        tit   = "¡Ciudad Equilibrada!"
        sub   = "El grupo administró la ciudad durante las 10 rondas."
    else:
        col_r = "#ef4444"; bg_r = "rgba(239,68,68,.1)"; ico = "💥"
        tit   = "La Ciudad Colapsó"
        sub   = "Un indicador llegó al límite crítico."

    # Estrellas acumuladas visibles en el banner
    st.markdown(
        "<div style='display:flex;justify-content:flex-end;margin-bottom:8px'>"
        + _badge_estrellas(gid) + "</div>",
        unsafe_allow_html=True)

    st.markdown(
        "<div style='background:" + bg_r + ";border:2px solid " + col_r + "33;"
        "border-radius:20px;padding:36px;text-align:center;margin-bottom:22px'>"
        "<div style='font-size:3.5rem'>" + ico + "</div>"
        "<h1 style='color:" + col_r + ";margin:10px 0 6px;font-size:1.7rem'>" + tit +
        "<span style='font-size:.75rem;margin-left:10px;color:" + col_dif + ";"
        "border:1px solid " + col_dif + "44;border-radius:20px;padding:3px 12px'>" + dif + "</span>"
        "</h1>"
        "<p style='color:rgba(255,255,255,.45);margin-bottom:6px'>" + sub + "</p>"
        "<p style='color:" + col_r + ";font-weight:700'>Rondas " + str(rondas_comp) + "/10</p>"
        + ("<p style='color:#fbbf24;font-weight:700;margin-top:4px'>+"
           + str(est_victoria) + " ⭐ ganadas por victoria</p>" if est_victoria else "") +
        "</div>",
        unsafe_allow_html=True)

    # ══ ESTADÍSTICAS (mismo diseño visual) ═══════════════════════════════════
    s1, s2, s3, s4 = st.columns(4)
    for col, label, val, color, emoji in [
        (s1, "Correctas",   correctas,              "#34d399", "✅"),
        (s2, "Incorrectas", incorrectas,            "#ef4444", "❌"),
        (s3, "Dificultad",  dif,                    col_dif,   "⚙️"),
        (s4, "Estrellas",   str(total_est) + " ⭐", "#fbbf24", "⭐"),
    ]:
        with col:
            st.markdown(
                "<div style='background:rgba(255,255,255,.04);"
                "border:1px solid " + color + "22;"
                "border-radius:12px;padding:12px;text-align:center;margin-bottom:16px'>"
                "<div style='font-size:1.3rem'>" + emoji + "</div>"
                "<div style='font-size:1.05rem;font-weight:700;color:" + color + "'>"
                + str(val) + "</div>"
                "<div style='font-size:.62rem;color:rgba(255,255,255,.3);"
                "font-family:Courier Prime,monospace'>" + label + "</div></div>",
                unsafe_allow_html=True)

    # ══ MISIONES COMPLETADAS (con canjeo manual) ══════════════════════════════
    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(167,139,250,.2);margin:0 0 16px'>",
        unsafe_allow_html=True)

    if pendientes_db:
        total_pend = sum(p["recompensa"] for p in pendientes_db)
        st.markdown(
            "<div style='font-family:Courier Prime,monospace;font-size:.68rem;"
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.3);"
            "margin-bottom:10px'>🎯 MISIONES COMPLETADAS — Clic para canjear estrellas</div>",
            unsafe_allow_html=True)

        st.markdown(
            "<div style='background:rgba(251,191,36,.06);"
            "border:1px solid rgba(251,191,36,.22);"
            "border-radius:10px;padding:9px 14px;margin-bottom:14px;"
            "font-family:Courier Prime,monospace;font-size:.72rem;"
            "color:#fbbf24;text-align:center'>"
            "⭐ Tienes <b>" + str(total_pend) + " estrellas</b> disponibles para canjear. "
            "Las no canjeadas aquí estarán en <b>Lobby → Misiones</b>.</div>",
            unsafe_allow_html=True)

        n = min(len(pendientes_db), 4)
        cols_m = st.columns(n)
        for i, p in enumerate(pendientes_db):
            mid       = p["id"]
            mision    = mision_map.get(mid, {"nombre": mid, "desc": "", "recompensa": p["recompensa"]})
            col       = cols_m[i % n]
            with col:
                st.markdown(
                    "<div style='background:rgba(251,191,36,.05);"
                    "border:1px solid rgba(251,191,36,.22);"
                    "border-radius:14px;padding:14px 10px;text-align:center;margin-bottom:8px'>"
                    "<div style='font-size:1.5rem;margin-bottom:5px'>🎯</div>"
                    "<div style='font-family:Courier Prime,monospace;font-size:.70rem;"
                    "font-weight:700;color:#f1f5f9;margin-bottom:4px'>"
                    + mision.get("nombre", mid) + "</div>"
                    "<div style='font-size:.60rem;color:rgba(255,255,255,.30);"
                    "line-height:1.4;margin-bottom:7px'>"
                    + mision.get("desc", "") + "</div>"
                    "<div style='color:#fbbf24;font-size:.85rem;font-weight:700'>"
                    "+" + str(p["recompensa"]) + " ⭐</div>"
                    "</div>",
                    unsafe_allow_html=True)

                if st.button(
                        "Canjear +" + str(p["recompensa"]) + "⭐",
                        key="canjear_fin_" + mid,
                        use_container_width=True):
                    # 1. Marcar como canjeada en database.db
                    guardar_mision(gid, mid)
                    # 2. Sumar estrellas en database.db
                    guardar_estrellas(gid, p["recompensa"])
                    # 3. Eliminar de pendientes en database.db
                    eliminar_mision_pendiente(gid, mid)
                    st.rerun()
    else:
        st.markdown(
            "<div style='background:rgba(255,255,255,.03);"
            "border:1px solid rgba(255,255,255,.07);"
            "border-radius:9px;padding:9px 14px;margin-bottom:12px;"
            "font-family:Courier Prime,monospace;font-size:.68rem;"
            "color:rgba(255,255,255,.28);text-align:center'>"
            "📋 No hay misiones nuevas para canjear en esta partida.</div>",
            unsafe_allow_html=True)

    # ══ INDICADORES FINALES (mismo diseño visual) ═════════════════════════════
    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(167,139,250,.2);margin:0 0 16px'>",
        unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Courier Prime,monospace;font-size:.68rem;"
        "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.3);"
        "margin-bottom:12px'>📊 INDICADORES FINALES</div>",
        unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    for col, key in zip([f1, f2, f3, f4],
                        ["economia", "medio_ambiente", "energia", "bienestar_social"]):
        color, emoji = IND_COLOR[key]
        val   = _clamp(ind_fin.get(key, 0))
        badge = "Estable" if val >= 60 else "Precaución" if val >= 30 else "Crítico"
        b_col = "#10b981" if val >= 60 else "#f59e0b" if val >= 30 else "#ef4444"
        with col:
            st.markdown(
                "<div style='background:rgba(255,255,255,.04);"
                "border:1px solid " + color + "28;"
                "border-radius:14px;padding:14px'>"
                "<div style='display:flex;justify-content:space-between;margin-bottom:6px'>"
                "<span style='color:#f1f5f9;font-size:.8rem'>"
                + emoji + " " + IND_LABEL[key] + "</span>"
                "<span style='color:" + b_col + ";font-size:.62rem;"
                "border:1px solid " + b_col + "44;border-radius:20px;padding:1px 7px'>"
                + badge + "</span></div>"
                "<div style='background:rgba(255,255,255,.07);border-radius:4px;height:8px'>"
                "<div style='width:" + str(val) + "%;background:" + color + ";"
                "height:8px;border-radius:4px'></div></div>"
                "<div style='text-align:right;color:" + color + ";font-weight:700;"
                "font-size:.82rem;margin-top:4px'>" + str(val) + "/100</div></div>",
                unsafe_allow_html=True)

    # ══ BOTONES (mismo diseño visual) ════════════════════════════════════════
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔄  REINICIAR", use_container_width=True):
            if gid: reiniciar_progreso(gid, dif)
            st.session_state.update(
                fase_ronda="decision", pregunta_actual=None,
                respuesta_correcta=False, decision_elegida=None,
                decision_efectos=None, evento_ronda=None,
                preguntas_usadas=[], timer_inicio=None,
                tiempo_agotado=False, correctas=0, incorrectas=0,
                logros_partida=[], _ranking_guardado=False,
                decisiones_usadas_partida=set(), mejor_racha=0, racha_actual=0,
                atributos_activos=set(), estrellas_usadas_partida=0,
                resultado_ts=None, evento_ts=None,
            )
            navegar("juego")
    with c2:
        if st.button("🏆  RANKING",  use_container_width=True): navegar("ranking")
    with c3:
        if st.button("🏠  LOBBY",    use_container_width=True): navegar("lobby")
    with c4:
        if st.button("🚪  INICIO",   use_container_width=True): navegar("inicio")
