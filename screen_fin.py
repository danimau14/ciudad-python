import streamlit as st
from session_manager import navegar
from database import (obtener_progreso, reiniciar_progreso, obtener_estrellas,
                      guardar_estrellas, guardar_logro, guardar_mision,
                      guardar_ranking, obtener_misiones_canjeadas, obtener_logros_grupo)
from config import (IND_COLOR, IND_LABEL, DIFICULTADES, LOGROS, MISIONES)
from ui_styles import pixel_header, pixel_divider, stat_badge


def _clamp(v): return max(0, min(100, v))


def _evaluar_misiones(gid, ind_fin, correctas, rondas, dif):
    ya_canjeadas = set(obtener_misiones_canjeadas(gid))
    nuevas = []
    for m in MISIONES:
        if m["id"] in ya_canjeadas:
            continue
        tipo = m.get("tipo", "")
        meta = m.get("meta", 1)
        ok   = False
        if tipo == "partidas"           : ok = rondas >= 10
        elif tipo == "racha"            : ok = st.session_state.get("mejor_racha", 0) >= meta
        elif tipo == "indicador"        : ok = ind_fin.get(m.get("ind", ""), 0) >= meta
        elif tipo == "sin_rojo"         : ok = all(v >= 30 for v in ind_fin.values())
        elif tipo == "victoria"         : ok = (rondas >= 10 and
                                                (m.get("dif","todas") == "todas" or m.get("dif") == dif))
        elif tipo == "correctas"        : ok = correctas >= meta
        elif tipo == "todos_sobre"      : ok = all(v >= meta for v in ind_fin.values())
        elif tipo == "decisiones_usadas": ok = len(st.session_state.get("decisiones_usadas_partida", set())) >= meta
        if ok:
            guardar_mision(gid, m["id"])
            nuevas.append(m)
    return nuevas


def _evaluar_logros(gid, ind_fin, correctas, rondas, dif):
    ya    = set(obtener_logros_grupo(gid))
    nuevos = []
    for l in LOGROS:
        if l["id"] in ya:
            continue
        tipo = l.get("tipo", "")
        meta = l.get("meta", 1)
        ok   = False
        if tipo == "partidas"            : ok = rondas >= 10
        elif tipo == "correctas_partida" : ok = correctas >= meta
        elif tipo == "victoria"          : ok = (rondas >= 10 and
                                                 (l.get("dif","todas") == "todas" or l.get("dif") == dif))
        elif tipo == "indicador_fin"     : ok = ind_fin.get(l.get("ind",""),0) >= meta
        elif tipo == "todos_sobre"       : ok = all(v >= meta for v in ind_fin.values())
        elif tipo == "racha"             : ok = st.session_state.get("mejor_racha",0) >= meta
        elif tipo == "correctas_total"   : ok = st.session_state.get("correctas_total_acum",0) >= meta
        elif tipo == "decisiones_todas"  : ok = len(st.session_state.get("decisiones_usadas_partida",set())) >= meta
        elif tipo == "tam_grupo"         :
            from database import obtener_estudiantes
            ok = len(obtener_estudiantes(gid)) >= meta
        if ok:
            guardar_logro(gid, l["id"])
            nuevos.append(l)
    return nuevos


def pantalla_fin():
    gid         = st.session_state.get("grupo_id")
    resultado   = st.session_state.get("resultado", "desconocido")
    ind_fin     = st.session_state.get("indicadores_finales", {})
    rondas_comp = st.session_state.get("rondas_completadas", 0)
    correctas   = st.session_state.get("correctas", 0)
    incorrectas = st.session_state.get("incorrectas", 0)
    dif         = st.session_state.get("dificultad_sel", "Normal")
    dif_cfg     = DIFICULTADES.get(dif, DIFICULTADES["Normal"])
    estrellas_ganadas = dif_cfg.get("estrellas", 2) if resultado == "victoria" else 0

    if gid and not st.session_state.get("_ranking_guardado"):
        if estrellas_ganadas > 0:
            guardar_estrellas(gid, estrellas_ganadas)
        puntaje = int(sum(ind_fin.values()) / 4) if ind_fin else 0
        guardar_ranking(gid, puntaje, dif)
        _evaluar_misiones(gid, ind_fin, correctas, rondas_comp, dif)
        _evaluar_logros(gid, ind_fin, correctas, rondas_comp, dif)
        st.session_state["_ranking_guardado"] = True

    if resultado == "victoria":
        st.balloons()
        col_r = "#10b981"; bg_r = "rgba(16,185,129,.12)"; ico = "🏆"
        tit   = "¡Ciudad Equilibrada!"; sub = "El grupo administró la ciudad durante las 10 rondas."
    else:
        col_r = "#ef4444"; bg_r = "rgba(239,68,68,.12)"; ico = "💥"
        tit   = "La Ciudad Colapsó"; sub = "Un indicador llegó al límite crítico."

    DIF_COLOR = {"Fácil":"#10b981","Normal":"#f59e0b","Difícil":"#ef4444"}
    dif_badge = (f"<span style='background:{DIF_COLOR.get(dif,'#a78bfa')}22;"
                 f"color:{DIF_COLOR.get(dif,'#a78bfa')};border:1px solid "
                 f"{DIF_COLOR.get(dif,'#a78bfa')}55;border-radius:20px;padding:3px 14px;"
                 f"font-size:.78rem;font-weight:700;margin-left:8px'>{dif}</span>")

    st.markdown(
        f"<div style='background:{bg_r};border:2px solid {col_r}44;"
        f"border-radius:20px;padding:40px;text-align:center;margin-bottom:24px'>"
        f"<div style='font-size:4rem'>{ico}</div>"
        f"<h1 style='color:{col_r};margin:12px 0 8px;font-size:1.9rem'>{tit}{dif_badge}</h1>"
        f"<p style='color:rgba(255,255,255,.55)'>{sub}</p>"
        f"<p style='color:{col_r};font-size:1.1rem;font-weight:600'>Rondas {rondas_comp}/10</p>"
        f"{'<p style=\"color:#fbbf24;font-size:1rem\">+' + str(estrellas_ganadas) + ' ⭐ ganadas</p>' if estrellas_ganadas else ''}"
        f"</div>",
        unsafe_allow_html=True)

    total_est = obtener_estrellas(gid) if gid else 0
    html_stats = (
        stat_badge("Correctas",   correctas,   "#34d399", "✅") +
        stat_badge("Incorrectas", incorrectas, "#ef4444", "❌") +
        stat_badge("Dificultad",  dif,         DIF_COLOR.get(dif,"#a78bfa"), "⚙️") +
        stat_badge("Estrellas",   f"{total_est} ⭐", "#fbbf24", "⭐")
    )
    st.markdown(f"<div style='text-align:center;margin-bottom:22px'>{html_stats}</div>",
                unsafe_allow_html=True)

    pixel_divider("#a78bfa", "INDICADORES FINALES")
    f1, f2, f3, f4 = st.columns(4)
    for col, key in zip([f1, f2, f3, f4],
                        ["economia","medio_ambiente","energia","bienestar_social"]):
        color, emoji = IND_COLOR[key]
        val   = _clamp(ind_fin.get(key, 0))
        badge = "Estable" if val >= 60 else "Precaución" if val >= 30 else "Crítico"
        b_col = "#10b981" if val >= 60 else "#f59e0b" if val >= 30 else "#ef4444"
        with col:
            st.markdown(
                f"<div style='background:rgba(255,255,255,.04);border:1px solid {color}33;"
                f"border-radius:14px;padding:12px 16px;margin-bottom:8px'>"
                f"<div style='display:flex;justify-content:space-between;margin-bottom:6px'>"
                f"<span style='font-weight:700;color:#f1f5f9;font-size:.82rem'>{emoji} {IND_LABEL[key]}</span>"
                f"<span style='color:{b_col};font-size:.68rem;border:1px solid {b_col}44;"
                f"border-radius:20px;padding:1px 8px'>{badge}</span></div>"
                f"<div style='background:rgba(255,255,255,.08);border-radius:6px;height:8px'>"
                f"<div style='width:{val}%;background:{color};height:8px;border-radius:6px'></div></div>"
                f"<div style='text-align:right;margin-top:4px;color:{color};"
                f"font-weight:700;font-size:.8rem'>{val}/100</div></div>",
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("🔄  REINICIAR", use_container_width=True):
            if gid:
                reiniciar_progreso(gid, dif)
            st.session_state.update(
                fase_ronda="decision", pregunta_actual=None,
                respuesta_correcta=False, decision_elegida=None,
                decision_efectos=None, evento_ronda=None,
                preguntas_usadas=[], timer_inicio=None,
                tiempo_agotado=False, correctas=0, incorrectas=0,
                logros_partida=[], _ranking_guardado=False,
                decisiones_usadas_partida=set(), mejor_racha=0, racha_actual=0,
            )
            navegar("juego")
    with c2:
        if st.button("🏆  RANKING", use_container_width=True):
            navegar("ranking")
    with c3:
        if st.button("🏠  LOBBY", use_container_width=True):
            navegar("lobby")
    with c4:
        if st.button("🚪  INICIO", use_container_width=True):
            navegar("inicio")
