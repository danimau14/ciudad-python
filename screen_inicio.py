import streamlit as st
from navigation import navegar
from config import TOTAL_RONDAS, DIFICULTADES


def pantalla_inicio():
    # ── Núcleo holográfico animado + título ──
    st.markdown(
        "<div style='text-align:center;padding:40px 0 20px;'>"
        "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,Noto Color Emoji,sans-serif;"
        "font-size:clamp(2.5rem,8vw,4rem);line-height:1;margin-bottom:12px;'>🏙️</div>"
        "<div style='font-family:Orbitron,sans-serif;"
        "font-size:clamp(1.4rem,5vw,2.8rem);font-weight:900;"
        "background:linear-gradient(90deg,#00d4ff,#8b5cf6,#22c55e,#00d4ff);"
        "background-size:300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "background-clip:text;animation:shimmer 4s linear infinite;"
        "letter-spacing:4px;margin-bottom:6px;'>CIUDAD EN EQUILIBRIO</div>"
        "<div style='font-family:Rajdhani,sans-serif;font-size:.8rem;"
        "color:rgba(255,255,255,0.3);letter-spacing:4px;'>SIMULADOR DE PENSAMIENTO SISTÉMICO</div>"
        "</div>",
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Selector de dificultad ──
    st.markdown(
        "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
        "color:rgba(0,212,255,0.5);letter-spacing:3px;text-align:center;"
        "margin-bottom:8px;'>NIVEL DE DIFICULTAD</div>", unsafe_allow_html=True)
    d1,d2,d3 = st.columns(3)
    dif_actual = st.session_state.get("dificultad","Medio")
    for col_d, (dif_key, dif_val) in zip([d1,d2,d3], DIFICULTADES.items()):
        with col_d:
            selected = dif_actual == dif_key
            border   = "rgba(0,212,255,0.7)" if selected else "rgba(255,255,255,0.1)"
            bg       = "rgba(0,212,255,0.12)" if selected else "rgba(5,10,20,0.8)"
            glow     = "0 0 16px rgba(0,212,255,0.25)" if selected else "none"
            st.markdown(
                "<div style='background:"+bg+";border:1.5px solid "+border+";"
                "border-radius:10px;padding:10px;text-align:center;"
                "box-shadow:"+glow+";cursor:pointer;'>"
                "<div style='font-size:1.3rem;'>"+dif_val["icon"]+"</div>"
                "<div style='font-family:Orbitron,sans-serif;font-size:0.7rem;"
                "color:"+("#00d4ff" if selected else "#94a3b8")+";font-weight:700;"
                "margin:4px 0 2px;'>"+dif_key.upper()+"</div>"
                "<div style='font-size:0.65rem;color:rgba(255,255,255,0.3);'>"
                +dif_val["desc"]+"</div></div>", unsafe_allow_html=True)
            if st.button(("✅ " if selected else "")+"Seleccionar",
                         key="dif_"+dif_key, use_container_width=True):
                st.session_state["dificultad"] = dif_key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botones de menú ──
    b1,b2,b3,b4 = st.columns(4)
    with b1:
        if st.button("🔐  INICIAR SESIÓN", use_container_width=True): navegar("login")
    with b2:
        if st.button("📝  REGISTRAR GRUPO", use_container_width=True): navegar("registro")
    with b3:
        if st.button("📖  INSTRUCCIONES", use_container_width=True): navegar("instrucciones")
    with b4:
        if st.button("🏆  RANKING", use_container_width=True): navegar("ranking")


def pantalla_instrucciones():
    st.markdown("<div style='text-align:center;'><span class='emoji-title' style='font-size:2rem;'>📖</span></div><div class='game-title' style='font-size:1.8rem;'>Instrucciones</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='card'>
<h3 style='color:#a78bfa;margin-top:0;'>🎯 Objetivo</h3>
<p>Administrar la ciudad durante <b>10 rondas</b>. El juego siempre completa las 10 rondas.</p>
<h3 style='color:#60a5fa;'>📊 Indicadores (inician en 50)</h3>
<p>💰 Economia &nbsp;|&nbsp; 🌿 Medio Ambiente<br>⚡ Energia &nbsp;|&nbsp; 🏥 Bienestar Social</p>
<h3 style='color:#f59e0b;'>⏱️ Temporizador</h3>
<p>Cada pregunta tiene <b>30 segundos</b>. Si se acaba el tiempo, se cuenta como respuesta incorrecta automaticamente.</p>
</div>""",unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='card-glow'>
<h3 style='color:#34d399;margin-top:0;'>🔄 Mecanica de Rondas</h3>
<ol style='padding-left:18px;'>
<li>Se selecciona el <b>estudiante en turno</b></li>
<li>El grupo <b>elige una decision estrategica</b></li>
<li>El estudiante responde una <b>pregunta de opcion multiple</b></li>
<li>✅ Acierta → se aplican los puntos de la decision</li>
<li>❌ Falla → <b>todos pierden 10 pts</b> (20 en rondas pares)</li>
<li>Ocurre un <b>evento aleatorio</b></li>
</ol>
</div>
<div class='card-danger'>
<h3 style='color:#f87171;margin-top:0;'>⚠️ Dificultad</h3>
<p>Los eventos negativos son <b>mas frecuentes y severos</b>. Las decisiones tienen <b>mayor impacto</b> positivo y negativo. Mantener el equilibrio es un verdadero reto.</p>
</div>""",unsafe_allow_html=True)
    if st.button("⬅️  Volver al Inicio"): navegar("inicio")
