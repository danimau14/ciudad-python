import streamlit as st
from session_manager import navegar

LOGROS_DEF = [
    {"id":"primera_ronda",     "nombre":"Primera Ronda",       "icono":"🌱",
     "desc":"Completa tu primera ronda.",
     "como":"Llega al final de la Ronda 1 sin abandonar la partida."},
    {"id":"ecologista",        "nombre":"Ecologista",          "icono":"🌳",
     "desc":"Elige 'Crear parque natural' en una partida.",
     "como":"En la fase de decisión selecciona 'Crear parque natural'."},
    {"id":"respuesta_rapida",  "nombre":"Respuesta Rápida",    "icono":"⚡",
     "desc":"Responde correctamente en menos de 10 segundos.",
     "como":"Confirma tu respuesta antes de que el temporizador baje de 20."},
    {"id":"sin_errores",       "nombre":"Sin Errores",         "icono":"🎯",
     "desc":"Completa una ronda sin fallar ninguna pregunta.",
     "como":"Responde todas las preguntas de la ronda correctamente."},
    {"id":"ciudad_equilibrada","nombre":"Ciudad Equilibrada",  "icono":"🏙️",
     "desc":"Termina con todos los indicadores ≥ 50.",
     "como":"Completa las 10 rondas con los 4 indicadores en 50 o más."},
    {"id":"superviviente",     "nombre":"Superviviente",       "icono":"🛡️",
     "desc":"Termina con al menos un indicador en estado crítico.",
     "como":"Completa la partida con algún indicador entre 1 y 29."},
    {"id":"maestro_python",    "nombre":"Maestro Python",      "icono":"🐍",
     "desc":"Responde correctamente 5 preguntas de Python seguidas.",
     "como":"Acierta 5 preguntas consecutivas de la categoría Python."},
    {"id":"matematico",        "nombre":"Matemático",          "icono":"📐",
     "desc":"Acierta preguntas de Cálculo, Derivadas y Matrices en una partida.",
     "como":"Responde correctamente al menos 1 pregunta de cada una de esas 3 categorías."},
    {"id":"estratega",         "nombre":"Estratega",           "icono":"♟️",
     "desc":"Usa cada decisión al menos una vez en una partida.",
     "como":"Selecciona las 8 decisiones disponibles a lo largo de la partida."},
    {"id":"perfecto",          "nombre":"Partida Perfecta",    "icono":"💎",
     "desc":"Termina con todos los indicadores ≥ 70.",
     "como":"Lleva los 4 indicadores a 70 o más al completar las 10 rondas."},
]


def pantalla_logros():
    logros_obtenidos = st.session_state.get("logros_obtenidos", [])
    obtenidos_n = len([l for l in LOGROS_DEF if l["id"] in logros_obtenidos])
    total_n     = len(LOGROS_DEF)

    st.markdown('<div class="game-title" style="font-size:1.8rem">🏅 Logros</div>',
                unsafe_allow_html=True)
    st.markdown(f'''<div style="text-align:center;margin:8px 0 16px">
        <span style="color:rgba(255,255,255,0.5)">Obtenidos: </span>
        <span style="color:#a78bfa;font-weight:800;font-size:1.1rem">
            {obtenidos_n} / {total_n}</span>
    </div>''', unsafe_allow_html=True)
    st.progress(obtenidos_n / total_n if total_n else 0)
    st.markdown("<br>", unsafe_allow_html=True)

    for logro in LOGROS_DEF:
        obtenido = logro["id"] in logros_obtenidos
        if obtenido:
            borde = "#a78bfa"
            bg    = "rgba(167,139,250,0.09)"
            glow  = "box-shadow:0 0 20px rgba(167,139,250,0.2);"
            badge = '<span style="background:rgba(167,139,250,0.2);color:#a78bfa;border:1px solid rgba(167,139,250,0.5);border-radius:20px;padding:2px 10px;font-size:0.78rem;font-weight:700">✅ OBTENIDO</span>'
            ico_color = "#f1f5f9"
        else:
            borde = "rgba(255,255,255,0.07)"
            bg    = "rgba(255,255,255,0.02)"
            glow  = "filter:grayscale(0.6);"
            badge = '<span style="background:rgba(255,255,255,0.06);color:rgba(255,255,255,0.3);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2px 10px;font-size:0.78rem">🔒 BLOQUEADO</span>'
            ico_color = "rgba(255,255,255,0.3)"

        with st.expander(f"{logro['icono']}  {logro['nombre']}"):
            st.markdown(f'''<div style="background:{bg};border:1.5px solid {borde};
                border-radius:14px;padding:18px 22px;{glow}">
                <div style="display:flex;justify-content:space-between;
                    align-items:center;margin-bottom:12px">
                    <span style="font-size:2rem;{glow}">{logro['icono']}</span>
                    {badge}
                </div>
                <p style="color:#f1f5f9;font-weight:600;margin:0 0 10px;font-size:0.95rem">
                    {logro['desc']}</p>
                <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                    border-radius:10px;padding:10px 14px">
                    <span style="color:rgba(255,255,255,0.35);font-size:0.72rem;
                        text-transform:uppercase;letter-spacing:1px">
                        ¿Cómo obtenerlo?</span><br>
                    <span style="color:#cbd5e1;font-size:0.88rem">{logro['como']}</span>
                </div>
            </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Lobby", use_container_width=True):
        navegar("lobby")
