import streamlit as st
from session_manager import navegar
from database import (obtener_misiones_canjeadas, obtener_estrellas,
                      obtener_misiones_pendientes, guardar_mision,
                      guardar_estrellas, eliminar_mision_pendiente)
from config import MISIONES

DIF_COLOR = {"Facil": "#10b981", "Normal": "#f59e0b", "Dificil": "#ef4444", "todas": "#a78bfa"}
DIF_LABEL = {"Facil": "FÁCIL",   "Normal": "NORMAL",  "Dificil": "DIFÍCIL", "todas": "TODAS"}


def _dif_key(dif):
    return {"Fácil": "Facil", "Difícil": "Dificil"}.get(dif, dif)


def _badge_estrellas(total):
    return (
        "<span style='display:inline-flex;align-items:center;gap:5px;"
        "background:rgba(251,191,36,.12);color:#fbbf24;"
        "border:1px solid rgba(251,191,36,.35);border-radius:20px;"
        "padding:4px 14px;font-family:Courier Prime,monospace;"
        "font-size:.82rem;font-weight:800;"
        "box-shadow:0 0 10px rgba(251,191,36,.18)'>⭐ " + str(total) + " estrellas acumuladas</span>"
    )


def pantalla_misiones():
    gid = st.session_state.get("grupo_id")

    # Leer todo desde database.db
    canjeadas   = set(obtener_misiones_canjeadas(gid)) if gid else set()
    pendientes  = obtener_misiones_pendientes(gid) if gid else []   # misiones completadas no canjeadas
    estrellas   = obtener_estrellas(gid) if gid else 0
    completadas = len(canjeadas)
    total       = len(MISIONES)
    pct         = int(completadas / total * 100) if total else 0

    # Mapa rápido id→misión completa
    mision_map = {m["id"]: m for m in MISIONES}
    # IDs pendientes de canjear
    pendientes_ids = {p["id"] for p in pendientes}

    # ── HEADER con estrellas visibles ─────────────────────────────────────────
    st.markdown(
        "<div style='display:flex;align-items:center;justify-content:space-between;"
        "flex-wrap:wrap;gap:10px;margin-bottom:12px'>"
        "<div>"
        "<div style='font-family:Press Start 2P,monospace;"
        "font-size:clamp(.8rem,2.5vw,1.3rem);"
        "background:linear-gradient(90deg,#a78bfa,#34d399);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>📋 MISIONES</div>"
        "<div style='color:rgba(255,255,255,.3);font-size:.72rem;"
        "font-family:Courier Prime,monospace'>"
        + str(completadas) + "/" + str(total) + " canjeadas</div></div>"
        + _badge_estrellas(estrellas) +
        "</div>",
        unsafe_allow_html=True)

    # Barra de progreso
    st.markdown(
        "<div style='background:rgba(255,255,255,.05);border-radius:8px;"
        "height:10px;margin-bottom:4px;overflow:hidden'>"
        "<div style='width:" + str(pct) + "%;height:10px;border-radius:8px;"
        "background:linear-gradient(90deg,#7c3aed,#34d399);transition:width .6s ease'></div></div>"
        "<div style='text-align:right;font-size:.66rem;color:rgba(255,255,255,.22);"
        "font-family:Courier Prime,monospace;margin-bottom:16px'>"
        + str(completadas) + "/" + str(total) + " · " + str(pct) + "%</div>",
        unsafe_allow_html=True)

    # Estadísticas
    total_canjeadas = sum(m["recompensa"] for m in MISIONES if m["id"] in canjeadas)
    total_pendiente = sum(p["recompensa"] for p in pendientes)
    s1, s2, s3 = st.columns(3)
    for col, label, val, color, emoji in [
        (s1, "Canjeadas",  completadas,                    "#34d399", "✅"),
        (s2, "Pendientes", len(pendientes),                "#fbbf24", "⏳"),
        (s3, "Acumuladas", str(estrellas) + " ⭐",         "#fbbf24", "⭐"),
    ]:
        with col:
            st.markdown(
                "<div style='background:rgba(255,255,255,.03);border:1px solid " + color + "22;"
                "border-radius:12px;padding:12px;text-align:center;margin-bottom:16px'>"
                "<div style='font-size:1.3rem'>" + emoji + "</div>"
                "<div style='font-size:1.1rem;font-weight:700;color:" + color + "'>" + str(val) + "</div>"
                "<div style='font-size:.65rem;color:rgba(255,255,255,.3);"
                "font-family:Courier Prime,monospace'>" + label + "</div></div>",
                unsafe_allow_html=True)

    # Aviso de pendientes
    if pendientes:
        st.markdown(
            "<div style='background:rgba(251,191,36,.06);"
            "border:1px solid rgba(251,191,36,.22);"
            "border-radius:10px;padding:10px 14px;margin-bottom:14px;"
            "font-family:Courier Prime,monospace;font-size:.70rem;"
            "color:#fbbf24;text-align:center'>"
            "⭐ Tienes <b>" + str(total_pendiente) + " estrellas</b> de misiones pendientes por canjear</div>",
            unsafe_allow_html=True)

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(167,139,250,.2);margin:0 0 14px'>",
        unsafe_allow_html=True)

    # ── LISTA DE MISIONES ─────────────────────────────────────────────────────
    for m in MISIONES:
        mid      = m["id"]
        canjeada = mid in canjeadas
        pendiente = mid in pendientes_ids

        dif_raw   = _dif_key(m.get("dif", "todas"))
        dif_color = DIF_COLOR.get(dif_raw, "#a78bfa")
        dif_label = DIF_LABEL.get(dif_raw, "TODAS")

        if canjeada:
            bg    = "rgba(52,211,153,.06)"
            borde = "rgba(52,211,153,.28)"
        elif pendiente:
            bg    = "rgba(251,191,36,.07)"
            borde = "rgba(251,191,36,.32)"
        else:
            bg    = "rgba(15,15,25,.6)"
            borde = "rgba(167,139,250,.10)"

        badge_dif = ""
        if dif_raw != "todas":
            badge_dif = (
                "<span style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
                "letter-spacing:1px;color:" + dif_color + ";background:" + dif_color + "18;"
                "border:1px solid " + dif_color + "44;border-radius:20px;padding:2px 9px;"
                "font-family:Courier Prime,monospace'>" + dif_label + "</span>")

        if canjeada:
            badge_estado = (
                "<span style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
                "color:#34d399;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.3);"
                "border-radius:20px;padding:2px 9px;letter-spacing:1px;"
                "font-family:Courier Prime,monospace'>✅ CANJEADA</span>")
        elif pendiente:
            badge_estado = (
                "<span style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
                "color:#fbbf24;background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.3);"
                "border-radius:20px;padding:2px 9px;letter-spacing:1px;"
                "font-family:Courier Prime,monospace'>⏳ PENDIENTE</span>")
        else:
            badge_estado = ""

        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(
                "<div style='background:" + bg + ";border:1px solid " + borde + ";"
                "border-radius:14px;padding:14px 18px;margin-bottom:8px'>"
                "<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px'>"
                "<span style='font-weight:700;color:#f1f5f9;"
                "font-family:Courier Prime,monospace;font-size:.9rem'>" + m["nombre"] + "</span>"
                + badge_dif + badge_estado +
                "</div>"
                "<div style='display:flex;justify-content:space-between;align-items:center'>"
                "<div style='font-size:.78rem;color:rgba(255,255,255,.4);"
                "font-family:Courier Prime,monospace;line-height:1.5'>" + m["desc"] + "</div>"
                "<span style='color:#fbbf24;font-weight:700;font-size:.82rem;"
                "font-family:Courier Prime,monospace;margin-left:12px;flex-shrink:0'>+"
                + str(m["recompensa"]) + " ⭐</span>"
                "</div></div>",
                unsafe_allow_html=True)

        with c2:
            if canjeada:
                st.markdown(
                    "<div style='display:flex;align-items:center;justify-content:center;"
                    "height:80px'><span style='color:#34d399;font-size:1.4rem'>✅</span></div>",
                    unsafe_allow_html=True)
            elif pendiente:
                # Misión completada en partida anterior, pendiente de canjear → SE PUEDE CANJEAR AQUÍ
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
                if st.button(
                        "Canjear", key="lobby_canjear_" + mid,
                        use_container_width=True):
                    # 1. Marcar como canjeada en database.db
                    guardar_mision(gid, mid)
                    # 2. Sumar estrellas en database.db
                    guardar_estrellas(gid, m["recompensa"])
                    # 3. Eliminar de pendientes en database.db
                    eliminar_mision_pendiente(gid, mid)
                    st.rerun()
            else:
                # No completada aún
                st.markdown(
                    "<div style='display:flex;align-items:center;justify-content:center;"
                    "height:80px'>"
                    "<span style='color:#fbbf24;font-weight:700;font-size:.88rem;"
                    "font-family:Courier Prime,monospace'>+" + str(m["recompensa"]) + " ⭐</span>"
                    "</div>",
                    unsafe_allow_html=True)

    st.markdown(
        "<div style='background:rgba(96,165,250,.07);"
        "border:1px solid rgba(96,165,250,.2);"
        "border-radius:14px;padding:12px 18px;margin-top:14px;margin-bottom:6px;"
        "font-family:Courier Prime,monospace;font-size:.75rem;color:rgba(255,255,255,.45);"
        "line-height:1.6'>💡 Las misiones marcadas como "
        "<b style='color:#fbbf24'>⏳ PENDIENTE</b> fueron completadas en una partida "
        "pero no se canjearon en la pantalla final. "
        "Las estrellas se acumulan en tu cuenta en <b style='color:#60a5fa'>database.db</b>.</div>",
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
