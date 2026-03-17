import streamlit as st
from navigation import navegar
from missions import MISIONES

def pantalla_misiones():
    logros_gp = st.session_state.get("misiones_cumplidas", [])
    canjeadas = st.session_state.get("misiones_canjeadas", False)

    _, col, _ = st.columns([0.5, 3, 0.5])
    with col:
        st.markdown(
            "<div style='text-align:center;padding:14px 0 6px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:1.3rem;font-weight:900;"
            "color:#fbbf24;letter-spacing:3px;margin-bottom:4px;'>📋 MISIONES</div>"
            "<div style='font-size:.68rem;color:rgba(255,255,255,.3);letter-spacing:2px;"
            "font-family:Space Grotesk,sans-serif;'>Completa misiones para ganar estrellas ⭐</div>"
            "</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if canjeadas:
            st.markdown(
                "<div style='background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);"
                "border-radius:10px;padding:12px;text-align:center;margin-bottom:16px;'>"
                "<span style='color:#22c55e;font-family:Syne,sans-serif;font-size:.85rem;"
                "font-weight:700;'>✅ Las estrellas de esta partida ya fueron canjeadas en la pantalla final."
                "<br>Juega una nueva partida para obtener más misiones.</span></div>",
                unsafe_allow_html=True)

        cols = st.columns(3)
        for i, (mkey, mdata) in enumerate(MISIONES.items()):
            cumplida = mkey in logros_gp
            color    = "#fbbf24" if cumplida else "rgba(255,255,255,0.06)"
            bg       = "rgba(251,191,36,0.08)" if cumplida else "rgba(5,10,20,0.85)"
            glow     = "0 0 14px rgba(251,191,36,0.3)" if cumplida else "none"
            op       = "1" if cumplida else "0.5"
            estado   = (
                f"<div style='font-size:.52rem;color:#fbbf24;font-weight:700;"
                f"font-family:Orbitron,sans-serif;margin-top:4px;'>✅ COMPLETADA</div>"
                if cumplida else
                "<div style='font-size:.52rem;color:rgba(255,255,255,.2);"
                "font-family:Orbitron,sans-serif;margin-top:4px;'>🔒 PENDIENTE</div>"
            )
            with cols[i % 3]:
                st.markdown(
                    f"<div style='background:{bg};border:1.5px solid {color};"
                    f"border-radius:12px;padding:12px;text-align:center;"
                    f"box-shadow:{glow};margin-bottom:10px;opacity:{op};transition:all .3s;'>"
                    f"<div style='font-size:1.6rem;margin-bottom:4px;'>{mdata['icon']}</div>"
                    f"<div style='font-family:Syne,sans-serif;font-size:.62rem;"
                    f"color:#fbbf24;font-weight:700;margin-bottom:3px;'>{mdata['nombre']}</div>"
                    f"<div style='font-size:.55rem;color:rgba(255,255,255,.3);line-height:1.4;'>"
                    f"{mdata['desc']}</div>"
                    f"<div style='font-size:.62rem;color:#facc15;font-weight:700;margin-top:5px;'>"
                    f"⭐ {mdata['estrellas']} estrellas</div>"
                    f"{estado}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ VOLVER AL LOBBY", use_container_width=True):
            navegar("lobby")
