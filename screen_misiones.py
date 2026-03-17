import streamlit as st
from session_manager import navegar

MISIONES = [
    {"id":"m1","icono":"🌱","nombre":"Primera Ronda",      "pts":50,
     "desc":"Completa tu primera ronda de juego."},
    {"id":"m2","icono":"🌳","nombre":"Decisión Ecológica", "pts":30,
     "desc":"Elige 'Crear parque natural' en una decisión."},
    {"id":"m3","icono":"⚡","nombre":"Respuesta Rápida",   "pts":40,
     "desc":"Responde correctamente en menos de 10 segundos."},
    {"id":"m4","icono":"🎯","nombre":"Sin Errores",        "pts":60,
     "desc":"Completa una ronda sin fallar ninguna pregunta."},
    {"id":"m5","icono":"🏙️","nombre":"Ciudad Equilibrada","pts":100,
     "desc":"Termina con todos los indicadores por encima de 50."},
]


def pantalla_misiones():
    logros = st.session_state.get("logros_obtenidos", [])
    completadas = sum(1 for m in MISIONES if m["id"] in logros)

    st.markdown('<div class="game-title" style="font-size:1.8rem">📋 Misiones</div>',
                unsafe_allow_html=True)
    st.markdown(f'''<div style="text-align:center;margin:8px 0 16px">
        <span style="color:rgba(255,255,255,0.5)">Completadas: </span>
        <span style="color:#34d399;font-weight:800;font-size:1.1rem">
            {completadas} / {len(MISIONES)}</span>
    </div>''', unsafe_allow_html=True)
    st.progress(completadas / len(MISIONES) if MISIONES else 0)
    st.markdown("<br>", unsafe_allow_html=True)

    for m in MISIONES:
        hecho  = m["id"] in logros
        color  = "#34d399" if hecho else "rgba(255,255,255,0.18)"
        bg     = "rgba(16,185,129,0.07)" if hecho else "rgba(255,255,255,0.02)"
        badge  = f'<span style="color:#34d399;font-size:0.8rem;font-weight:700">✅ Completada</span>' \
                 if hecho else '<span style="color:rgba(255,255,255,0.3);font-size:0.8rem">⏳ Pendiente</span>'
        st.markdown(f'''<div class="card" style="background:{bg};border-color:{color}55;
            display:flex;justify-content:space-between;align-items:center;
            padding:16px 20px;margin-bottom:10px">
            <div>
                <div style="font-size:1.05rem;font-weight:700;color:#f1f5f9">
                    {m["icono"]} {m["nombre"]}</div>
                <div style="font-size:0.82rem;color:rgba(255,255,255,0.42);margin-top:4px">
                    {m["desc"]}</div>
            </div>
            <div style="text-align:right;min-width:120px">
                {badge}
                <div style="color:#fbbf24;font-size:0.78rem;margin-top:4px">+{m["pts"]} pts</div>
            </div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Lobby", use_container_width=True):
        navegar("lobby")
