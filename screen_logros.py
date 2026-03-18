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
    pct        = int(obtenidos / total * 100) if total else 0

    pixel_header("LOGROS", f"{obtenidos}/{total} desbloqueados", "🏅")

    col_pct = "#34d399" if pct >= 70 else "#f59e0b" if pct >= 30 else "#a78bfa"
    st.markdown(
        f"<div style='background:rgba(255,255,255,.05);border-radius:8px;"
        f"height:10px;margin-bottom:4px;overflow:hidden'>"
        f"<div style='width:{pct}%;height:10px;border-radius:8px;"
        f"background:linear-gradient(90deg,#7c3aed,{col_pct});"
        f"transition:width .6s ease;box-shadow:0 0 10px {col_pct}44'></div></div>"
        f"<div style='text-align:right;font-size:.7rem;color:rgba(255,255,255,.3);"
        f"font-family:Courier Prime,monospace;margin-bottom:18px'>"
        f"{obtenidos}/{total} logros · {pct}%</div>",
        unsafe_allow_html=True)

    total_stars = sum(l.get("estrellas",0) for l in LOGROS if l["id"] in logros_ids)
    html_stats = (
        stat_badge("Obtenidos",  obtenidos,       "#34d399", "✅") +
        stat_badge("Bloqueados", total-obtenidos, "#64748b", "🔒") +
        stat_badge("Estrellas",  total_stars,     "#fbbf24", "⭐")
    )
    st.markdown(f'<div style="text-align:center;margin-bottom:22px">{html_stats}</div>',
                unsafe_allow_html=True)

    pixel_divider("#a78bfa", "TODOS LOS LOGROS")

    cols = st.columns(4)
    for i, logro in enumerate(LOGROS):
        obtenido = logro["id"] in logros_ids
        color    = "#a78bfa" if obtenido else "rgba(255,255,255,.1)"
        bg       = "rgba(124,58,237,.08)" if obtenido else "rgba(15,15,25,.5)"
        borde    = "rgba(124,58,237,.4)"  if obtenido else "rgba(255,255,255,.06)"
        sombra   = "0 0 18px rgba(124,58,237,.2)" if obtenido else "none"
        emoji    = logro["emoji"] if obtenido else "🔒"
        nombre   = logro["nombre"] if obtenido else "BLOQUEADO"
        stars_h  = (
            f'<div style="font-size:.68rem;color:#fbbf24;margin-top:4px">'
            f'{"⭐"*min(logro.get("estrellas",0),5)}</div>'
        ) if obtenido and logro.get("estrellas",0) else ""

        badge_h = (
            '<div style="position:absolute;top:7px;right:7px;font-size:.55rem;' +
            'background:rgba(52,211,153,.12);color:#34d399;border:1px solid rgba(52,211,153,.28);' +
            'border-radius:20px;padding:2px 7px;font-family:Courier Prime,monospace">✅ OBTENIDO</div>'
        ) if obtenido else (
            '<div style="position:absolute;top:7px;right:7px;font-size:.55rem;' +
            'background:rgba(255,255,255,.04);color:rgba(255,255,255,.25);' +
            'border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:2px 7px;' +
            'font-family:Courier Prime,monospace">🔒 BLOQUEADO</div>'
        )

        with cols[i % 4]:
            card_html = (
                f'<div style="background:{bg};border:1px solid {borde};border-radius:14px;' +
                f'padding:14px 10px 10px;text-align:center;box-shadow:{sombra};' +
                f'position:relative;min-height:140px;margin-bottom:10px">' +
                badge_h +
                f'<div style="font-size:1.6rem;margin-bottom:6px;' +
                f'filter:{("none" if obtenido else "grayscale(1) opacity(.25)") }">' +
                f'{emoji}</div>' +
                f'<div style="font-size:.68rem;font-weight:700;color:{color};' +
                f'font-family:Courier Prime,monospace;line-height:1.3;margin-bottom:4px">' +
                f'{nombre}</div>'
            )
            if obtenido:
                card_html += (
                    f'<div style="font-size:.6rem;color:rgba(255,255,255,.35);' +
                    f'font-family:Courier Prime,monospace;line-height:1.4">' +
                    f'{logro["desc"]}</div>' + stars_h
                )
            card_html += "</div>"
            st.markdown(card_html, unsafe_allow_html=True)

            if not obtenido:
                with st.expander("¿Cómo obtenerlo?"):
                    st.markdown(
                        f'<div style="font-family:Courier Prime,monospace;font-size:.78rem;' +
                        f'color:#c4b5fd;line-height:1.6">{logro["como"]}</div>',
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
