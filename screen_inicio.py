import streamlit as st
from session_manager import navegar


def pantalla_inicio():
    st.markdown('<div class="game-title">Ciudad en Equilibrio</div>', unsafe_allow_html=True)
    st.markdown('<div class="game-sub">Ingeniería Edition · Pensamiento Sistémico</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    stats = [("🏙️","10 Rondas","Por partida"),("📚","63 Preguntas","7 categorías"),
             ("⏱️","30 Segundos","Por pregunta"),("🔥","Alta dificultad","Mayor riesgo")]
    for col, (em, v, d) in zip([c1,c2,c3,c4], stats):
        with col:
            st.markdown(f'''<div class="card" style="text-align:center">
                <div style="font-size:1.8rem">{em}</div>
                <div style="font-size:1rem;font-weight:700;color:#f1f5f9">{v}</div>
                <div style="font-size:0.78rem;color:rgba(255,255,255,0.4)">{d}</div></div>''',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🔐 Iniciar Sesión", use_container_width=True): navegar("login")
    with b2:
        if st.button("📝 Registrar Grupo", use_container_width=True): navegar("registro")
    with b3:
        if st.button("📖 Instrucciones", use_container_width=True): navegar("instrucciones")


def pantalla_instrucciones():
    st.markdown('<div class="game-title" style="font-size:1.8rem">Instrucciones</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('''<div class="card">
            <h3 style="color:#a78bfa;margin-top:0">🎯 Objetivo</h3>
            <p>Administrar la ciudad durante <b>10 rondas</b>. El juego siempre completa las 10 rondas.</p>
            <h3 style="color:#60a5fa">📊 Indicadores inician en 50</h3>
            <p>Economía &nbsp;&nbsp; Medio Ambiente<br>Energía &nbsp;&nbsp; Bienestar Social</p>
            <h3 style="color:#f59e0b">⏱️ Temporizador</h3>
            <p>Cada pregunta tiene <b>30 segundos</b>. Si se acaba el tiempo, cuenta como incorrecta.</p>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown('''<div class="card-glow">
            <h3 style="color:#34d399;margin-top:0">⚙️ Mecánica de Rondas</h3>
            <ol style="padding-left:18px">
            <li>Se selecciona el <b>estudiante en turno</b></li>
            <li>El grupo <b>elige una decisión estratégica</b></li>
            <li>El estudiante responde una <b>pregunta de opción múltiple</b></li>
            <li>Acierta → se aplican los puntos de la decisión</li>
            <li>Falla → <b>todos pierden 10 pts</b> (20 en rondas pares)</li>
            <li>Ocurre un <b>evento aleatorio</b></li>
            </ol></div>
            <div class="card-danger">
            <h3 style="color:#f87171;margin-top:0">⚠️ Dificultad</h3>
            <p>Los eventos negativos son <b>más frecuentes y severos</b>. Las decisiones tienen <b>mayor impacto</b>. Mantener el equilibrio es un verdadero reto.</p>
        </div>''', unsafe_allow_html=True)
    if st.button("← Volver al Inicio"): navegar("inicio")


def pantalla_lobby():
    st.markdown('<div class="game-title">Lobby</div>', unsafe_allow_html=True)
    if st.button("← Volver"): navegar("inicio")


def pantalla_logros():
    st.markdown('<div class="game-title">Logros</div>', unsafe_allow_html=True)
    st.info("Sistema de logros próximamente.")
    if st.button("← Volver"): navegar("inicio")
