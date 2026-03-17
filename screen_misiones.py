import streamlit as st
from navigation import navegar
from missions import MISIONES


def pantalla_misiones():
    logros_gp   = st.session_state.get("misiones_cumplidas", [])
    canjeadas   = st.session_state.get("misiones_canjeadas", False)
    est_ganadas = st.session_state.get("estrellas_ganadas_partida", 0)

    _, col, _ = st.columns([0.3, 3, 0.3])
    with col:
        st.markdown(
            "<div style='text-align:center;padding:18px 0 8px;'>"
            "<div style='font-size:2rem;'>📋</div>"
            "<div style='font-family:Orbitron,sans-serif;font-size:1.3rem;font-weight:900;"
            "color:#fbbf24;letter-spacing:3px;margin:6px 0 3px;'>MISIONES</div>"
            "<div style='font-size:.7rem;color:rgba(255,255,255,.3);letter-spacing:2px;'>"
            "Completa misiones para ganar ⭐ estrellas</div></div>",
            unsafe_allow_html=True)

        if canjeadas:
            st.markdown(
                "<div style='background:rgba(34,197,94,0.07);border:1px solid rgba(34,197,94,0.3);"
                "border-radius:12px;padding:14px;text-align:center;margin:10px 0;'>"
                "<span style='color:#22c55e;font-size:.85rem;font-weight:700;'>"
                "✅ Estrellas de esta partida ya canjeadas.<br>"
                "<span style='font-size:.72rem;color:rgba(255,255,255,.4);'>"
                "Juega una nueva partida para obtener más.</span>"
                "</span></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (mkey, mdata) in enumerate(MISIONES.items()):
            cumplida = mkey in logros_gp
            color = "#fbbf24" if cumplida else "rgba(255,255,255,0.07)"
            bg    = "rgba(251,191,36,0.08)" if cumplida else "rgba(5,10,20,0.85)"
            glow  = "0 0 16px rgba(251,191,36,0.25)" if cumplida else "none"
            op    = "1" if cumplida else "0.45"
            badge = (
                "<div style='font-family:Orbitron,sans-serif;font-size:.5rem;"
                "color:#fbbf24;margin-top:5px;'>✅ COMPLETADA</div>"
                if cumplida else
                "<div style='font-family:Orbitron,sans-serif;font-size:.5rem;"
                "color:rgba(255,255,255,.2);margin-top:5px;'>🔒 PENDIENTE</div>"
            )
            with cols[i % 3]:
                icon = mdata["icon"]
                nom  = mdata["nombre"]
                desc = mdata["desc"]
                ests = mdata["estrellas"]
                st.markdown(
                    f"<div style='background:{bg};border:1.5px solid {color};"
                    f"border-radius:14px;padding:14px 10px;text-align:center;"
                    f"box-shadow:{glow};margin-bottom:10px;opacity:{op};'>"
                    f"<div style='font-size:1.7rem;margin-bottom:4px;'>{icon}</div>"
                    f"<div style='font-family:Orbitron,sans-serif;font-size:.58rem;"
                    f"color:#fbbf24;font-weight:700;margin-bottom:4px;'>{nom}</div>"
                    f"<div style='font-size:.55rem;color:rgba(255,255,255,.3);"
                    f"line-height:1.4;'>{desc}</div>"
                    f"<div style='font-size:.65rem;color:#facc15;font-weight:700;"
                    f"margin-top:6px;'>⭐ {ests} estrellas</div>"
                    f"{badge}</div>",
                    unsafe_allow_html=True)

        if not canjeadas and est_ganadas > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            c1, _ = st.columns([2, 3])
            with c1:
                st.markdown(
                    f"<div style='background:rgba(251,191,36,0.08);"
                    f"border:2px solid rgba(251,191,36,0.4);border-radius:14px;"
                    f"padding:16px;text-align:center;'>"
                    f"<div style='font-family:Orbitron,sans-serif;font-size:.65rem;"
                    f"color:#fbbf24;'>PENDIENTE DE CANJEAR</div>"
                    f"<div style='font-size:2rem;font-weight:900;color:#fbbf24;'>"
                    f"⭐ {est_ganadas}</div>"
                    f"<div style='font-size:.6rem;color:rgba(255,255,255,.3);'>"
                    f"Canjea al final de la partida</div></div>",
                    unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️  VOLVER AL LOBBY", use_container_width=True):
            navegar("lobby")
