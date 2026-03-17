import streamlit as st
from session_manager import navegar


MISIONES = [
    {"id": "m1", "nombre": "Primera Ronda",     "desc": "Completa tu primera ronda.",          "icono": "🌱"},
    {"id": "m2", "nombre": "Decisión Ecológica","desc": "Elige 'Crear parque natural'.",        "icono": "🌳"},
    {"id": "m3", "nombre": "Respuesta Rápida",  "desc": "Responde en menos de 10 segundos.",   "icono": "⚡"},
    {"id": "m4", "nombre": "Sin Errores",        "desc": "Completa una ronda sin fallar.",      "icono": "🎯"},
    {"id": "m5", "nombre": "Ciudad Equilibrada","desc": "Mantén todos los indicadores > 50.",  "icono": "🏙️"},
]


def pantalla_misiones():
    st.markdown('<div class="game-title" style="font-size:1.8rem">🎯 Misiones</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    logros = st.session_state.get("logros_obtenidos", [])
    for m in MISIONES:
        hecho = m["id"] in logros
        color = "#34d399" if hecho else "rgba(255,255,255,0.3)"
        bg    = "rgba(16,185,129,0.08)" if hecho else "rgba(255,255,255,0.03)"
        badge = "✅ Completada" if hecho else "⏳ Pendiente"
        st.markdown(f'''<div class="card" style="background:{bg};border-color:{color}44">
            <div style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:1.3rem">{m["icono"]} <b style="color:#f1f5f9">{m["nombre"]}</b></span>
                <span style="color:{color};font-size:0.8rem;font-weight:600">{badge}</span>
            </div>
            <p style="margin:6px 0 0;color:rgba(255,255,255,0.5);font-size:0.85rem">{m["desc"]}</p>
        </div>''', unsafe_allow_html=True)

    if st.button("← Volver al Inicio", use_container_width=True):
        navegar("inicio")
