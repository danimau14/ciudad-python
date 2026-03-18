import streamlit as st
from session_manager import navegar
from database import obtener_logros_grupo
from config import LOGROS
from ui_styles import pixel_header, pixel_divider, stat_badge


def pantalla_logros():
    gid        = st.session_state.get("grupo_id")
    logros_ids = set(obtener_logros_grupo(gid)) if gid else set()
    total      = len(LOGROS)
    obtenidos  = len(logros_ids)
    pct        = int(obtenidos / total * 100)

    pixel_header("LOGROS", f"{obtenidos}/{total} desbloqueados", "🏅")

    # ── Barra de progreso global ─────────────────────────────────────────────
    col_pct = "#34d399" if pct >= 70 else "#f59e0b" if pct >= 30 else "#a78bfa"
    st.markdown(f"""
    <div style="background:rgba(255,255,255,.05);border-radius:8px;
        height:10px;margin-bottom:4px;overflow:hidden">
        <div style="width:{pct}%;height:10px;border-radius:8px;
            background:linear-gradient(90deg,#7c3aed,{col_pct});
            transition:width .6s ease;box-shadow:0 0 10px {col_pct}44"></div>
    </div>
    <div style="text-align:right;font-size:.7rem;color:rgba(255,255,255,.3);
        font-family:Courier Prime,monospace;margin-bottom:18px">
        {obtenidos}/{total} logros · {pct}%
    </div>""", unsafe_allow_html=True)

    # ── Stats rápidas ────────────────────────────────────────────────────────
    total_stars = sum(l.get("estrellas",0) for l in LOGROS if l["id"] in logros_ids)
    html_stats = (
        stat_badge("Obtenidos",  obtenidos,       "#34d399", "✅") +
        stat_badge("Bloqueados", total-obtenidos, "#64748b", "🔒") +
        stat_badge("Estrellas",  total_stars,     "#fbbf24", "⭐")
    )
    st.markdown(f'<div style="text-align:center;margin-bottom:22px">{html_stats}</div>',
                unsafe_allow_html=True)

    pixel_divider("#a78bfa", "TODOS LOS LOGROS")

    # ── Grid de logros — SOLO HTML, sin st.expander ──────────────────────────
    cols = st.columns(4)
    for i, logro in enumerate(LOGROS):
        obtenido = logro["id"] in logros_ids
        color    = "#a78bfa" if obtenido else "rgba(255,255,255,.1)"
        bg       = "rgba(124,58,237,.08)" if obtenido else "rgba(15,15,25,.5)"
        borde    = "rgba(124,58,237,.4)"  if obtenido else "rgba(255,255,255,.05)"
        sombra   = "0 0 18px rgba(124,58,237,.15)" if obtenido else "none"
        emoji    = logro["emoji"] if obtenido else "&#10067;"
        nombre   = logro["nombre"] if obtenido else "???"
        desc     = logro["desc"]   if obtenido else logro["como"]
        stars_h  = (
            f'<div style="font-size:.68rem;color:#fbbf24;margin-top:5px">'
            f'{"⭐"*min(logro.get("estrellas",0),5)} {logro.get("estrellas",0)}&#9733;</div>'
        ) if obtenido and logro.get("estrellas",0) else ""
        badge_h  = (
            '<div style="position:absolute;top:8px;right:8px;font-size:.58rem;'
            'background:rgba(52,211,153,.12);color:#34d399;border:1px solid rgba(52,211,153,.28);'
            'border-radius:20px;padding:2px 7px;font-family:Courier Prime,monospace">OK</div>'
        ) if obtenido else (
            '<div style="position:absolute;top:8px;right:8px;font-size:.58rem;'
            'background:rgba(255,255,255,.04);color:rgba(255,255,255,.2);'
            'border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:2px 7px;'
            'font-family:Courier Prime,monospace">&#128274;</div>'
        )

        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {borde};border-radius:14px;
                padding:14px 10px;text-align:center;box-shadow:{sombra};
                position:relative;min-height:140px;margin-bottom:10px">
                {badge_h}
                <div style="font-size:1.6rem;margin-bottom:6px;
                    filter:{'none' if obtenido else 'grayscale(1) opacity(.25)'}">
                    {emoji}</div>
                <div style="font-size:.68rem;font-weight:700;color:{color};
                    font-family:Courier Prime,monospace;line-height:1.3;margin-bottom:4px">
                    {nombre}</div>
                <div style="font-size:.6rem;color:rgba(255,255,255,.28);
                    font-family:Courier Prime,monospace;line-height:1.4">
                    {desc}</div>
                {stars_h}
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
