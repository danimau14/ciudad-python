import streamlit as st
from session_manager import navegar
from database import obtener_misiones_canjeadas, obtener_estrellas
from config import MISIONES

DIF_COLOR = {"Facil":"#10b981","Normal":"#f59e0b","Dificil":"#ef4444","todas":"#a78bfa"}
DIF_LABEL = {"Facil":"FÁCIL","Normal":"NORMAL","Dificil":"DIFÍCIL","todas":"TODAS"}


def _dif_key(dif):
    return {"Fácil":"Facil","Difícil":"Dificil"}.get(dif, dif)


def pantalla_misiones():
    gid         = st.session_state.get("grupo_id")
    canjeadas   = set(obtener_misiones_canjeadas(gid)) if gid else set()
    estrellas   = obtener_estrellas(gid) if gid else 0
    completadas = len(canjeadas)
    total       = len(MISIONES)
    pct         = int(completadas / total * 100) if total else 0

    st.markdown(
        "<div style='font-family:Press Start 2P,monospace;font-size:1.3rem;"
        "background:linear-gradient(90deg,#a78bfa,#34d399);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>📋 MISIONES</div>"
        f"<div style='color:rgba(255,255,255,.3);font-size:.75rem;"
        f"font-family:Courier Prime,monospace;margin-bottom:14px'>"
        f"{completadas}/{total} completadas · {estrellas} ⭐</div>",
        unsafe_allow_html=True)

    st.markdown(
        f"<div style='background:rgba(255,255,255,.05);border-radius:8px;"
        f"height:10px;margin-bottom:4px;overflow:hidden'>"
        f"<div style='width:{pct}%;height:10px;border-radius:8px;"
        f"background:linear-gradient(90deg,#7c3aed,#34d399);transition:width .6s ease'></div></div>"
        f"<div style='text-align:right;font-size:.68rem;color:rgba(255,255,255,.25);"
        f"font-family:Courier Prime,monospace;margin-bottom:18px'>"
        f"{completadas}/{total} · {pct}%</div>",
        unsafe_allow_html=True)

    total_recompensas = sum(m["recompensa"] for m in MISIONES if m["id"] in canjeadas)
    s1, s2, s3 = st.columns(3)
    for col, label, val, color, emoji in [
        (s1, "Canjeadas",  completadas,          "#34d399", "✅"),
        (s2, "Pendientes", total - completadas,  "#64748b", "⏳"),
        (s3, "Ganadas",    f"{total_recompensas} ⭐", "#fbbf24", "⭐"),
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

    for m in MISIONES:
        canjeada  = m["id"] in canjeadas
        dif_raw   = _dif_key(m.get("dif", "todas"))
        dif_color = DIF_COLOR.get(dif_raw, "#a78bfa")
        dif_label = DIF_LABEL.get(dif_raw, "TODAS")
        bg    = "rgba(52,211,153,.06)"   if canjeada else "rgba(15,15,25,.6)"
        borde = "rgba(52,211,153,.3)"    if canjeada else "rgba(167,139,250,.12)"

        badge_dif = ""
        if dif_raw not in ("todas",):
            badge_dif = (
                f"<span style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
                f"letter-spacing:1px;color:{dif_color};background:{dif_color}18;"
                f"border:1px solid {dif_color}44;border-radius:20px;padding:2px 9px;"
                f"font-family:Courier Prime,monospace'>{dif_label}</span>")

        badge_estado = (
            "<span style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
            "color:#34d399;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.3);"
            "border-radius:20px;padding:2px 9px;letter-spacing:1px;"
            "font-family:Courier Prime,monospace'>✅ COMPLETADA</span>"
        ) if canjeada else ""

        icono_der = (
            "<span style='color:#34d399;font-size:1.3rem'>✅</span>"
            if canjeada else
            f"<span style='color:#fbbf24;font-weight:700;font-size:.9rem;"
            f"font-family:Courier Prime,monospace'>+{m['recompensa']} ⭐</span>"
        )

        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(
                f"<div style='background:{bg};border:1px solid {borde};"
                f"border-radius:14px;padding:14px 18px;margin-bottom:8px'>"
                f"<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px'>"
                f"<span style='font-weight:700;color:#f1f5f9;font-family:Courier Prime,monospace;"
                f"font-size:.9rem'>{m['nombre']}</span>"
                + badge_dif + badge_estado +
                f"</div>"
                f"<div style='font-size:.78rem;color:rgba(255,255,255,.4);"
                f"font-family:Courier Prime,monospace;line-height:1.5'>{m['desc']}</div>"
                f"</div>",
                unsafe_allow_html=True)
        with c2:
            st.markdown(
                f"<div style='display:flex;align-items:center;justify-content:center;"
                f"height:72px'>{icono_der}</div>",
                unsafe_allow_html=True)

    st.markdown(
        "<div style='background:rgba(96,165,250,.07);border:1px solid rgba(96,165,250,.2);"
        "border-radius:14px;padding:14px 18px;margin-top:18px;margin-bottom:6px;"
        "font-family:Courier Prime,monospace;font-size:.8rem;color:rgba(255,255,255,.5);"
        "line-height:1.6'>💡 Las misiones se <b style='color:#60a5fa'>canjean automáticamente</b> "
        "al finalizar una partida desde la pantalla de resultados.</div>",
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
