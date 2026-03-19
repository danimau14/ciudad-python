import streamlit as st
from session_manager import navegar
from database import (obtener_misiones_canjeadas, obtener_estrellas,
                      guardar_mision, guardar_estrellas)
from config import MISIONES

DIF_COLOR = {"Facil": "#10b981", "Normal": "#f59e0b", "Dificil": "#ef4444", "todas": "#a78bfa"}
DIF_LABEL = {"Facil": "FÁCIL",   "Normal": "NORMAL",  "Dificil": "DIFÍCIL", "todas": "TODAS"}


def _dif_key(dif):
    return {"Fácil": "Facil", "Difícil": "Dificil"}.get(dif, dif)


def pantalla_misiones():
    gid         = st.session_state.get("grupo_id")
    canjeadas   = set(obtener_misiones_canjeadas(gid)) if gid else set()
    estrellas   = obtener_estrellas(gid) if gid else 0
    completadas = len(canjeadas)
    total       = len(MISIONES)
    pct         = int(completadas / total * 100) if total else 0

    # Misiones pendientes de canjear (completadas en partidas pero no canjeadas)
    # Se detectan comparando las misiones que están en _misiones_completadas_partida
    # con las ya canjeadas en BD
    pendientes_canje = [
        m for m in MISIONES
        if m["id"] not in canjeadas
        # Una misión está "pendiente" si fue completada en alguna partida
        # pero no fue canjeada. En el lobby no podemos re-evaluar la partida,
        # pero sí mostrar las que el usuario dejó pendientes desde screen_fin
    ]

    # ── HEADER ────────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='font-family:Press Start 2P,monospace;"
        "font-size:clamp(.8rem,2.5vw,1.3rem);"
        "background:linear-gradient(90deg,#a78bfa,#34d399);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>📋 MISIONES</div>"
        "<div style='color:rgba(255,255,255,.3);font-size:.75rem;"
        "font-family:Courier Prime,monospace;margin-bottom:14px'>"
        + str(completadas) + "/" + str(total) + " canjeadas · "
        + str(estrellas) + " ⭐ acumuladas</div>",
        unsafe_allow_html=True)

    # Barra de progreso
    st.markdown(
        "<div style='background:rgba(255,255,255,.05);border-radius:8px;"
        "height:10px;margin-bottom:4px;overflow:hidden'>"
        "<div style='width:" + str(pct) + "%;height:10px;border-radius:8px;"
        "background:linear-gradient(90deg,#7c3aed,#34d399);transition:width .6s ease'></div></div>"
        "<div style='text-align:right;font-size:.68rem;color:rgba(255,255,255,.25);"
        "font-family:Courier Prime,monospace;margin-bottom:18px'>"
        + str(completadas) + "/" + str(total) + " · " + str(pct) + "%</div>",
        unsafe_allow_html=True)

    # Estadísticas
    total_recompensas = sum(m["recompensa"] for m in MISIONES if m["id"] in canjeadas)
    pendientes_count  = total - completadas
    s1, s2, s3 = st.columns(3)
    for col, label, val, color, emoji in [
        (s1, "Canjeadas",  completadas,               "#34d399", "✅"),
        (s2, "Pendientes", pendientes_count,           "#64748b", "⏳"),
        (s3, "Acumuladas", str(estrellas) + " ⭐",    "#fbbf24", "⭐"),
    ]:
        with col:
            st.markdown(
                "<div style='background:rgba(255,255,255,.03);border:1px solid " + color + "22;"
                "border-radius:12px;padding:12px;text-align:center;margin-bottom:18px'>"
                "<div style='font-size:1.3rem'>" + emoji + "</div>"
                "<div style='font-size:1.1rem;font-weight:700;color:" + color + "'>" + str(val) + "</div>"
                "<div style='font-size:.65rem;color:rgba(255,255,255,.3);"
                "font-family:Courier Prime,monospace'>" + label + "</div></div>",
                unsafe_allow_html=True)

    st.markdown(
        "<hr style='border:none;border-top:1px solid rgba(167,139,250,.2);margin:0 0 18px'>",
        unsafe_allow_html=True)

    # ── LISTA DE MISIONES ─────────────────────────────────────────────────────
    for m in MISIONES:
        canjeada  = m["id"] in canjeadas
        dif_raw   = _dif_key(m.get("dif", "todas"))
        dif_color = DIF_COLOR.get(dif_raw, "#a78bfa")
        dif_label = DIF_LABEL.get(dif_raw, "TODAS")
        bg    = "rgba(52,211,153,.06)"    if canjeada else "rgba(15,15,25,.6)"
        borde = "rgba(52,211,153,.28)"    if canjeada else "rgba(167,139,250,.12)"

        badge_dif = ""
        if dif_raw != "todas":
            badge_dif = (
                "<span style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
                "letter-spacing:1px;color:" + dif_color + ";background:" + dif_color + "18;"
                "border:1px solid " + dif_color + "44;border-radius:20px;padding:2px 9px;"
                "font-family:Courier Prime,monospace'>" + dif_label + "</span>")

        badge_estado = (
            "<span style='font-size:.62rem;font-weight:700;text-transform:uppercase;"
            "color:#34d399;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.3);"
            "border-radius:20px;padding:2px 9px;letter-spacing:1px;"
            "font-family:Courier Prime,monospace'>✅ CANJEADA</span>"
        ) if canjeada else ""

        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(
                "<div style='background:" + bg + ";border:1px solid " + borde + ";"
                "border-radius:14px;padding:14px 18px;margin-bottom:8px'>"
                "<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px'>"
                "<span style='font-weight:700;color:#f1f5f9;font-family:Courier Prime,monospace;"
                "font-size:.9rem'>" + m["nombre"] + "</span>"
                + badge_dif + badge_estado +
                "</div>"
                "<div style='display:flex;justify-content:space-between;align-items:center'>"
                "<div style='font-size:.78rem;color:rgba(255,255,255,.4);"
                "font-family:Courier Prime,monospace;line-height:1.5'>" + m["desc"] + "</div>"
                "<div style='margin-left:12px;flex-shrink:0'>"
                "<span style='color:#fbbf24;font-weight:700;font-size:.82rem;"
                "font-family:Courier Prime,monospace'>+" + str(m["recompensa"]) + " ⭐</span>"
                "</div></div></div>",
                unsafe_allow_html=True)

        with c2:
            if canjeada:
                st.markdown(
                    "<div style='display:flex;align-items:center;justify-content:center;"
                    "height:80px'><span style='color:#34d399;font-size:1.4rem'>✅</span></div>",
                    unsafe_allow_html=True)
            else:
                # Botón para canjear estrellas de misión pendiente
                # Solo se puede canjear si la misión fue completada en una partida anterior
                # y quedó pendiente (registrada en session_state desde screen_fin)
                misiones_pendientes_fin = [
                    x["id"] for x in
                    st.session_state.get("_misiones_completadas_partida", [])]
                puede_canjear = m["id"] in misiones_pendientes_fin

                st.markdown(
                    "<div style='display:flex;align-items:center;justify-content:center;"
                    "height:80px'>",
                    unsafe_allow_html=True)
                if puede_canjear:
                    if st.button(
                            "Canjear", key="lobby_canjear_" + m["id"],
                            use_container_width=True):
                        guardar_mision(gid, m["id"])
                        guardar_estrellas(gid, m["recompensa"])
                        # Actualizar session_state
                        pendientes = st.session_state.get("_misiones_completadas_partida", [])
                        st.session_state["_misiones_completadas_partida"] = [
                            x for x in pendientes if x["id"] != m["id"]]
                        st.rerun()
                else:
                    st.markdown(
                        "<span style='color:#fbbf24;font-weight:700;font-size:.85rem;"
                        "font-family:Courier Prime,monospace'>+" + str(m["recompensa"]) + " ⭐</span>",
                        unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ── INFO ──────────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:rgba(96,165,250,.07);border:1px solid rgba(96,165,250,.2);"
        "border-radius:14px;padding:14px 18px;margin-top:18px;margin-bottom:6px;"
        "font-family:Courier Prime,monospace;font-size:.78rem;color:rgba(255,255,255,.5);"
        "line-height:1.6'>💡 Las misiones completadas se pueden "
        "<b style='color:#60a5fa'>canjear en la pantalla final</b> de cada partida "
        "o aquí si quedaron pendientes. Las estrellas se acumulan en tu cuenta.</div>",
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
