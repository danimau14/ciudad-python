import streamlit as st
from session_manager import navegar

MISIONES = [
    {"id":"m1","nombre":"Primera Ronda",      "icono":"🌱","pts":50,
     "desc":"Completa tu primera ronda de juego."},
    {"id":"m2","nombre":"Decisión Ecológica", "icono":"🌳","pts":30,
     "desc":"Elige 'Crear parque natural' en una decisión."},
    {"id":"m3","nombre":"Respuesta Rápida",   "icono":"⚡","pts":40,
     "desc":"Responde correctamente en menos de 10 segundos."},
    {"id":"m4","nombre":"Sin Errores",        "icono":"🎯","pts":60,
     "desc":"Completa una ronda sin fallar ninguna pregunta."},
    {"id":"m5","nombre":"Ciudad Equilibrada", "icono":"🏙️","pts":100,
     "desc":"Mantén todos los indicadores por encima de 50 al final."},
]


def pantalla_misiones():
    st.markdown('<div class="game-title" style="font-size:1.8rem">📋 Misiones</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    logros = st.session_state.get("logros_obtenidos", [])
    completadas = sum(1 for m in MISIONES if m["id"] in logros)

    st.markdown(f'''<div class="card" style="text-align:center;padding:12px">
        <span style="color:rgba(255,255,255,0.5)">Completadas: </span>
        <span style="color:#34d399;font-weight:800">{completadas}/{len(MISIONES)}</span>
    </div>''', unsafe_allow_html=True)
    st.progress(completadas / len(MISIONES) if MISIONES else 0)
    st.markdown("<br>", unsafe_allow_html=True)

    for m in MISIONES:
        hecho = m["id"] in logros
        color = "#34d399" if hecho else "rgba(255,255,255,0.2)"
        bg    = "rgba(16,185,129,0.07)" if hecho else "rgba(255,255,255,0.03)"
        badge = "✅ Completada" if hecho else "⏳ Pendiente"
        st.markdown(f'''<div class="card" style="background:{bg};border-color:{color}55;
            display:flex;justify-content:space-between;align-items:center;padding:16px 20px">
            <div>
                <div style="font-size:1.1rem;font-weight:700;color:#f1f5f9">
                    {m["icono"]} {m["nombre"]}</div>
                <div style="font-size:0.82rem;color:rgba(255,255,255,0.45);margin-top:3px">
                    {m["desc"]}</div>
            </div>
            <div style="text-align:right;min-width:110px">
                <div style="color:{color};font-size:0.82rem;font-weight:600">{badge}</div>
                <div style="color:#fbbf24;font-size:0.78rem;margin-top:3px">+{m["pts"]} pts</div>
            </div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Lobby", use_container_width=True):
        navegar("lobby")
