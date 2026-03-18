import streamlit as st
from session_manager import navegar
from database import obtener_logros_grupo, obtener_stats
from config import LOGROS
from ui_styles import pixel_header, pixel_divider, stat_badge


TIPO_GRUPOS = {
    "🏆 Rendimiento":  ["correctas_total","correctas_partida","racha","velocidad","casi_tiempo",
                        "correctas_partida_dif","correctas_dif_partida"],
    "🏙️ Ciudad":       ["victoria","victoria_3","victoria_dif_count","partidas","todos_sobre",
                        "todos_aciertan","indicador_fin","doble_indicador","exacto","rango",
                        "min_global","recuperacion","recuperacion_total","sin_rojo"],
    "🎯 Estrategia":   ["decisiones_todas","decision_count","sin_decision","tam_grupo",
                        "eventos_neg_seguidos","segunda_ok","atributo_count"],
    "⭐ Colección":    ["estrellas","misiones_count","partidas","dias_jugados",
                        "ranking_top","tiempo_partida","rondas"],
}


def _logro_card(logro, obtenido):
    lid    = logro["id"]
    color  = "#a78bfa" if obtenido else "rgba(255,255,255,.12)"
    bg     = "rgba(124,58,237,.08)" if obtenido else "rgba(15,15,25,.5)"
    borde  = "rgba(124,58,237,.4)"  if obtenido else "rgba(255,255,255,.06)"
    sombra = "0 0 20px rgba(124,58,237,.15)" if obtenido else "none"
    emoji  = logro["emoji"] if obtenido else "❓"
    nombre = logro["nombre"] if obtenido else "???"
    desc   = logro["desc"]   if obtenido else "Logro bloqueado"
    estrellas_html = ""
    if obtenido and logro.get("estrellas", 0) > 0:
        estrellas_html = (
            f'<div style="font-size:.7rem;color:#fbbf24;margin-top:5px;'
            f'font-family:Courier Prime,monospace">'
            f'{"⭐" * min(logro["estrellas"],5)} {logro["estrellas"]}★</div>'
        )
    como_html = ""
    if not obtenido:
        como_html = (
            f'<div style="font-size:.68rem;color:rgba(255,255,255,.2);'
            f'margin-top:6px;font-style:italic;font-family:Courier Prime,monospace;'
            f'line-height:1.4">📌 {logro["como"]}</div>'
        )
    estado_badge = (
        '<div style="position:absolute;top:10px;right:10px;font-size:.65rem;'
        'background:rgba(52,211,153,.15);color:#34d399;border:1px solid rgba(52,211,153,.3);'
        'border-radius:20px;padding:2px 8px;font-family:Courier Prime,monospace">LOGRO</div>'
    ) if obtenido else ""

    return f'''<div style="background:{bg};border:1px solid {borde};border-radius:16px;
        padding:16px 14px;text-align:center;transition:all .25s;box-shadow:{sombra};
        position:relative;height:100%;min-height:140px">
        {estado_badge}
        <div style="font-size:1.8rem;margin-bottom:6px;
            filter:{'none' if obtenido else 'grayscale(1) opacity(.3)'}">
            {emoji}</div>
        <div style="font-size:.72rem;font-weight:700;color:{color};
            font-family:Courier Prime,monospace;line-height:1.3;margin-bottom:4px">
            {nombre}</div>
        <div style="font-size:.65rem;color:rgba(255,255,255,.3);
            font-family:Courier Prime,monospace;line-height:1.4">
            {desc}</div>
        {estrellas_html}
        {como_html}
    </div>'''


def pantalla_logros():
    gid        = st.session_state.get("grupo_id")
    logros_ids = set(obtener_logros_grupo(gid)) if gid else set()
    total      = len(LOGROS)
    obtenidos  = len(logros_ids)
    pct        = int(obtenidos / total * 100)

    pixel_header("LOGROS", f"{obtenidos}/{total} desbloqueados · {pct}%", "🏅")

    # Barra de progreso global
    col_pct = "#34d399" if pct >= 70 else "#f59e0b" if pct >= 30 else "#a78bfa"
    st.markdown(f'''<div style="background:rgba(255,255,255,.05);border-radius:8px;
        height:12px;margin-bottom:6px;overflow:hidden">
        <div style="width:{pct}%;height:12px;border-radius:8px;
            background:linear-gradient(90deg,#7c3aed,{col_pct});
            transition:width .6s ease;box-shadow:0 0 10px {col_pct}44"></div>
    </div>
    <div style="text-align:right;font-size:.7rem;color:rgba(255,255,255,.3);
        font-family:Courier Prime,monospace;margin-bottom:20px">
        {obtenidos}/{total} logros · {pct}% completado</div>
    ''', unsafe_allow_html=True)

    # Stats rápidas
    stats_html = (
        stat_badge("Completados", obtenidos, "#34d399",  "✅") +
        stat_badge("Bloqueados",  total-obtenidos, "#64748b", "🔒") +
        stat_badge("Progreso",    f"{pct}%",  "#a78bfa", "📊")
    )
    st.markdown(f'<div style="text-align:center;margin-bottom:20px">{stats_html}</div>',
                unsafe_allow_html=True)

    # Tabs por categoría
    logros_map = {l["id"]: l for l in LOGROS}
    tabs_labels = list(TIPO_GRUPOS.keys()) + ["🌐 Todos"]
    tabs = st.tabs(tabs_labels)

    def _render_grupo(ids_tipo):
        grupo_logros = [l for l in LOGROS
                        if l["tipo"] in ids_tipo or
                        (l.get("dif") and l["tipo"] in ids_tipo)]
        if not grupo_logros:
            grupo_logros = [l for l in LOGROS if l["tipo"] in ids_tipo]
        if not grupo_logros:
            st.markdown('<div style="color:rgba(255,255,255,.2);text-align:center;'
                        'font-family:Courier Prime,monospace;padding:20px">Sin logros aquí</div>',
                        unsafe_allow_html=True)
            return
        cols = st.columns(4)
        for i, logro in enumerate(grupo_logros):
            with cols[i % 4]:
                obtenido = logro["id"] in logros_ids
                st.markdown(_logro_card(logro, obtenido), unsafe_allow_html=True)
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for tab, (categoria, tipos) in zip(tabs[:-1], TIPO_GRUPOS.items()):
        with tab:
            _render_grupo(tipos)

    with tabs[-1]:
        cols = st.columns(4)
        for i, logro in enumerate(LOGROS):
            with cols[i % 4]:
                obtenido = logro["id"] in logros_ids
                st.markdown(_logro_card(logro, obtenido), unsafe_allow_html=True)
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
