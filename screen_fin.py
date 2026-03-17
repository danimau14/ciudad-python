import streamlit as st
from database import reiniciar_progreso
from session_manager import navegar
from config import TOTAL_RONDAS


def barra_indicador(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    if valor >= 60:   color, badge = "#10b981", "Estable"
    elif valor >= 30: color, badge = "#f59e0b", "Precaución"
    else:             color, badge = "#ef4444", "Crítico"
    st.markdown(f'''<div style="background:rgba(255,255,255,0.05);border:1px solid {color}44;
        border-radius:14px;padding:14px 18px;margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="font-weight:700;color:#f1f5f9">{emoji} {nombre}</span>
            <span style="font-size:0.72rem;color:{color};font-weight:600">{badge}</span>
        </div>
        <div style="background:rgba(255,255,255,0.1);border-radius:6px;height:8px">
            <div style="width:{valor}%;background:{color};height:8px;border-radius:6px"></div>
        </div>
        <div style="text-align:right;margin-top:5px;font-size:0.82rem;font-weight:700;color:{color}">{valor}/100</div>
    </div>''', unsafe_allow_html=True)


def pantalla_fin():
    resultado   = st.session_state.get("resultado", "desconocido")
    ind_fin     = st.session_state.get("indicadores_finales", {})
    rondas_comp = st.session_state.get("rondas_completadas", 0)

    if resultado == "victoria":
        st.balloons()
        col_r, bg_r = "#10b981", "rgba(16,185,129,0.12)"
        ico, tit = "🏆", "¡Ciudad Equilibrada!"
        sub = f"El grupo administró la ciudad durante todas las {TOTAL_RONDAS} rondas exitosamente."
    else:
        col_r, bg_r = "#ef4444", "rgba(239,68,68,0.12)"
        ico, tit = "💥", "La Ciudad Colapsó"
        sub = "Un indicador llegó al límite crítico."

    st.markdown(f'''<div style="background:{bg_r};border:2px solid {col_r}44;
        border-radius:20px;padding:40px;text-align:center;margin-bottom:24px">
        <div style="font-size:4rem">{ico}</div>
        <h1 style="color:{col_r};margin:12px 0 8px;font-size:1.9rem">{tit}</h1>
        <p style="color:rgba(255,255,255,0.55)">{sub}</p>
        <p style="color:{col_r};font-size:1.1rem;font-weight:600">
            Rondas {rondas_comp}/{TOTAL_RONDAS}</p>
    </div>''', unsafe_allow_html=True)

    st.markdown("### Indicadores Finales")
    f1, f2, f3, f4 = st.columns(4)
    with f1: barra_indicador("Economía",      ind_fin.get("economia",0),       "💰")
    with f2: barra_indicador("Medio Ambiente",ind_fin.get("medio_ambiente",0), "🌿")
    with f3: barra_indicador("Energía",       ind_fin.get("energia",0),        "⚡")
    with f4: barra_indicador("Bienestar",     ind_fin.get("bienestar_social",0),"❤️")

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 Reiniciar Juego", use_container_width=True):
            gid = st.session_state.get("grupo_id")
            if gid:
                reiniciar_progreso(gid)
            st.session_state.update({
                "pregunta_actual":None,"respuesta_correcta":False,
                "decision_elegida":None,"decision_efectos":None,
                "evento_ronda":None,"fase_ronda":"decision",
                "preguntas_usadas":[],"timer_inicio":None,
                "tiempo_agotado":False,"correctas":0,"incorrectas":0,
            })
            navegar("juego")
    with c2:
        if st.button("🏆 Ver Ranking", use_container_width=True):
            navegar("ranking")
    with c3:
        if st.button("🏠 Volver al Inicio", use_container_width=True):
            navegar("inicio")
