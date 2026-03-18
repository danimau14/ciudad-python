import streamlit as st
from session_manager import navegar
from database import obtener_logros_grupo
from config import LOGROS


def pantalla_logros():
    gid        = st.session_state.get("grupo_id")
    logros_ids = set(obtener_logros_grupo(gid)) if gid else set()
    total      = len(LOGROS)
    obtenidos  = len(logros_ids)
    pct        = int(obtenidos / total * 100) if total else 0

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='font-family:Press Start 2P,monospace;font-size:1.3rem;"
        "background:linear-gradient(90deg,#a78bfa,#60a5fa);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>🏅 LOGROS</div>"
        f"<div style='color:rgba(255,255,255,.3);font-size:.75rem;"
        f"font-family:Courier Prime,monospace;margin-bottom:14px'>"
        f"{obtenidos}/{total} desbloqueados</div>",
        unsafe_allow_html=True)

    col_pct = "#34d399" if pct >= 70 else "#f59e0b" if pct >= 30 else "#a78bfa"
    st.markdown(
        f"<div style='background:rgba(255,255,255,.05);border-radius:8px;"
        f"height:10px;margin-bottom:4px;overflow:hidden'>"
        f"<div style='width:{pct}%;height:10px;border-radius:8px;"
        f"background:linear-gradient(90deg,#7c3aed,{col_pct});"
        f"box-shadow:0 0 10px {col_pct}44'></div></div>"
        f"<div style='text-align:right;font-size:.68rem;color:rgba(255,255,255,.25);"
        f"font-family:Courier Prime,monospace;margin-bottom:22px'>"
        f"{obtenidos}/{total} · {pct}%</div>",
        unsafe_allow_html=True)

    # ── Estadísticas rápidas ──────────────────────────────────────────────────
    total_stars = sum(l.get("estrellas", 0) for l in LOGROS if l["id"] in logros_ids)
    s1, s2, s3 = st.columns(3)
    for col, label, val, color, emoji in [
        (s1, "Obtenidos",  obtenidos,       "#34d399", "✅"),
        (s2, "Bloqueados", total-obtenidos, "#64748b", "🔒"),
        (s3, "Estrellas",  f"{total_stars} ⭐", "#fbbf24", "⭐"),
    ]:
        with col:
            st.markdown(
                f"<div style='background:rgba(255,255,255,.03);border:1px solid {color}22;"
                f"border-radius:12px;padding:12px;text-align:center;margin-bottom:18px'>"
                f"<div style='font-size:1.3rem'>{emoji}</div>"
                f"<div style='font-size:1.1rem;font-weight:700;color:{color}'>{val}</div>"
                f"<div style='font-size:.65rem;color:rgba(255,255,255,.3);"
                f"font-family:Courier Prime,monospace'>{label}</div></div>",
                unsafe_allow_html=True)

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(167,139,250,.2);margin:0 0 18px'>",
        unsafe_allow_html=True)

    # ── Grid de logros ────────────────────────────────────────────────────────
    cols = st.columns(4)
    for i, logro in enumerate(LOGROS):
        obtenido = logro["id"] in logros_ids
        color = "#a78bfa"              if obtenido else "rgba(255,255,255,.18)"
        bg    = "rgba(124,58,237,.08)" if obtenido else "rgba(15,15,25,.5)"
        borde = "rgba(124,58,237,.45)" if obtenido else "rgba(255,255,255,.07)"
        sombra = "0 0 22px rgba(124,58,237,.22)" if obtenido else "none"
        emoji = logro["emoji"] if obtenido else "🔒"
        filt  = "none" if obtenido else "grayscale(1) opacity(.2)"
        stars = "⭐" * min(logro.get("estrellas", 0), 5)

        badge = (
            "<div style='position:absolute;top:7px;right:7px;font-size:.52rem;"
            "background:rgba(52,211,153,.12);color:#34d399;"
            "border:1px solid rgba(52,211,153,.3);border-radius:20px;"
            "padding:2px 7px;font-family:Courier Prime,monospace'>"
            "✅ OBTENIDO</div>"
        ) if obtenido else (
            "<div style='position:absolute;top:7px;right:7px;font-size:.52rem;"
            "background:rgba(255,255,255,.04);color:rgba(255,255,255,.25);"
            "border:1px solid rgba(255,255,255,.09);border-radius:20px;"
            "padding:2px 7px;font-family:Courier Prime,monospace'>"
            "🔒 BLOQUEADO</div>"
        )

        card = (
            f"<div style='background:{bg};border:1px solid {borde};"
            f"border-radius:14px;padding:14px 10px 12px;text-align:center;"
            f"box-shadow:{sombra};position:relative;min-height:148px;margin-bottom:4px'>"
            + badge +
            f"<div style='font-size:1.7rem;margin-bottom:6px;margin-top:8px;"
            f"filter:{filt}'>{emoji}</div>"
            f"<div style='font-size:.67rem;font-weight:700;color:{color};"
            f"font-family:Courier Prime,monospace;line-height:1.3;margin-bottom:4px'>"
            f"{'BLOQUEADO' if not obtenido else logro['nombre']}</div>"
        )
        if obtenido:
            card += (
                f"<div style='font-size:.6rem;color:rgba(255,255,255,.3);"
                f"font-family:Courier Prime,monospace;line-height:1.4;margin-bottom:4px'>"
                f"{logro['desc']}</div>"
                f"<div style='font-size:.65rem;color:#fbbf24'>{stars}</div>"
            )
        card += "</div>"

        with cols[i % 4]:
            st.markdown(card, unsafe_allow_html=True)
            if not obtenido:
                with st.expander("¿Cómo obtenerlo?"):
                    st.markdown(
                        f"<div style='font-family:Courier Prime,monospace;font-size:.8rem;"
                        f"color:#c4b5fd;line-height:1.7;padding:4px 0'>{logro['como']}</div>",
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
