import streamlit as st
from session_manager import navegar

LOGROS_DEF = [
    {"id":"primera_ronda",    "nombre":"Primera Ronda",         "icono":"🌱",
     "desc":"Completa tu primera ronda.",
     "como":"Llega al final de la Ronda 1 sin abandonar la partida."},
    {"id":"ecologista",       "nombre":"Ecologista",            "icono":"🌳",
     "desc":"Elige 'Crear parque natural' en una partida.",
     "como":"En la fase de decisión, selecciona 'Crear parque natural'."},
    {"id":"respuesta_rapida", "nombre":"Respuesta Rápida",      "icono":"⚡",
     "desc":"Responde correctamente en menos de 10 segundos.",
     "como":"Confirma tu respuesta antes de que el temporizador baje de 20."},
    {"id":"sin_errores",      "nombre":"Sin Errores",           "icono":"🎯",
     "desc":"Completa una ronda sin fallar ninguna pregunta.",
     "como":"Responde todas las preguntas de la ronda correctamente."},
    {"id":"ciudad_equilibrada","nombre":"Ciudad Equilibrada",   "icono":"🏙️",
     "desc":"Mantén todos los indicadores por encima de 50 al final.",
     "como":"Termina las 10 rondas con los 4 indicadores ≥ 50."},
    {"id":"superviviente",    "nombre":"Superviviente",         "icono":"🛡️",
     "desc":"Completa la partida con al menos un indicador en estado crítico.",
     "como":"Termina con algún indicador < 30 pero sin llegar a 0."},
    {"id":"maestro_python",   "nombre":"Maestro Python",        "icono":"🐍",
     "desc":"Responde correctamente 5 preguntas de Python seguidas.",
     "como":"Acierta 5 preguntas de la categoría Python sin fallar."},
    {"id":"matematico",       "nombre":"Matemático",            "icono":"📐",
     "desc":"Responde correctamente preguntas de Cálculo, Derivadas y Matrices.",
     "como":"Acierta al menos 1 pregunta de cada una de esas 3 categorías."},
    {"id":"estratega",        "nombre":"Estratega",             "icono":"♟️",
     "desc":"Usa cada decisión al menos una vez en una partida.",
     "como":"Selecciona las 8 decisiones disponibles a lo largo de la partida."},
    {"id":"perfecto",         "nombre":"Partida Perfecta",      "icono":"💎",
     "desc":"Termina con todos los indicadores ≥ 70.",
     "como":"Lleva los 4 indicadores a 70 o más al completar las 10 rondas."},
]


def pantalla_logros():
    gid = st.session_state.get("grupo_id")
    logros_obtenidos = st.session_state.get("logros_obtenidos", [])

    st.markdown('<div class="game-title" style="font-size:1.8rem">🏅 Logros</div>',
                unsafe_allow_html=True)

    total    = len(LOGROS_DEF)
    obtenidos = len([l for l in LOGROS_DEF if l["id"] in logros_obtenidos])
    st.markdown(f'''<div style="text-align:center;margin-bottom:16px">
        <span style="color:rgba(255,255,255,0.5);font-size:0.9rem">
        Obtenidos: </span>
        <span style="color:#a78bfa;font-weight:800;font-size:1rem">
        {obtenidos}/{total}</span>
    </div>''', unsafe_allow_html=True)

    st.progress(obtenidos / total)
    st.markdown("<br>", unsafe_allow_html=True)

    for logro in LOGROS_DEF:
        obtenido = logro["id"] in logros_obtenidos
        if obtenido:
            color = "#a78bfa"
            borde = "#a78bfa"
            bg    = "rgba(167,139,250,0.08)"
            badge = '<span style="color:#a78bfa;font-weight:700;font-size:0.8rem">✅ OBTENIDO</span>'
            glow  = "box-shadow:0 0 18px rgba(167,139,250,0.25);"
        else:
            color = "rgba(255,255,255,0.25)"
            borde = "rgba(255,255,255,0.08)"
            bg    = "rgba(255,255,255,0.02)"
            badge = '<span style="color:rgba(255,255,255,0.3);font-size:0.8rem">🔒 BLOQUEADO</span>'
            glow  = ""

        with st.expander(f"{logro['icono']}  {logro['nombre']}  —  {logro['desc']}"):
            st.markdown(f'''<div style="background:{bg};border:1.5px solid {borde};
                border-radius:14px;padding:16px 20px;{glow}">
                <div style="display:flex;justify-content:space-between;align-items:center;
                    margin-bottom:10px">
                    <span style="font-size:1.8rem">{logro['icono']}</span>
                    {badge}
                </div>
                <p style="color:#f1f5f9;font-weight:600;margin:0 0 6px">{logro['desc']}</p>
                <div style="background:rgba(255,255,255,0.05);border-radius:8px;
                    padding:8px 12px;margin-top:8px">
                    <span style="color:rgba(255,255,255,0.4);font-size:0.75rem;
                        text-transform:uppercase;letter-spacing:1px">
                        ¿Cómo obtenerlo?</span><br>
                    <span style="color:#cbd5e1;font-size:0.88rem">{logro['como']}</span>
                </div>
            </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Lobby", use_container_width=True):
        navegar("lobby")
