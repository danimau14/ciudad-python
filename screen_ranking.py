import streamlit as st
from navigation import navegar
from database import obtener_ranking
from achievements import LOGROS
from config import DIFICULTADES


def _render_tabla(filas):
    if not filas:
        st.markdown(
            "<div style='text-align:center;padding:30px;color:rgba(255,255,255,.3);'>"
            "No hay partidas registradas en este nivel.</div>", unsafe_allow_html=True)
        return
    medallas = ["🥇","🥈","🥉"] + ["🏅"]*(len(filas)-3)
    for pos,(med,fila) in enumerate(zip(medallas,filas), 1):
        col_pos = "#f59e0b" if pos==1 else "#94a3b8" if pos==2 else "#cd7f32" if pos==3 else "#64748b"
        logros_str = " ".join([LOGROS[k]["icon"] for k in fila["logros"].split(",") if k in LOGROS]) if fila["logros"] else ""
        dif_icon = DIFICULTADES.get(fila["dificultad"],{}).get("icon","")
        st.markdown(
            "<div style='background:rgba(5,10,20,.85);border:1px solid "+col_pos+"44;"
            "border-radius:12px;padding:14px 18px;margin-bottom:8px;"
            "display:flex;align-items:center;gap:14px;"
            "box-shadow:0 0 16px "+col_pos+"18;'>"
            "<div style='font-size:1.6rem;min-width:36px;text-align:center;"
            "font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>"+med+"</div>"
            "<div style='flex:1;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:.85rem;"
            "color:#f1f5f9;font-weight:700;'>"+fila["nombre_grupo"]+"</div>"
            "<div style='font-size:.7rem;color:rgba(255,255,255,.35);margin-top:2px;'>"
            +dif_icon+" "+fila["dificultad"]+" · ✅"+str(fila["correctas"])+" · "+logros_str+"</div>"
            "</div>"
            "<div style='font-family:Orbitron,sans-serif;font-size:1.3rem;"
            "font-weight:900;color:"+col_pos+";text-shadow:0 0 12px "+col_pos+"66;'>"
            +str(fila["puntaje"])+"</div>"
            "</div>", unsafe_allow_html=True)


def pantalla_ranking():
    _,col,_ = st.columns([0.5,3,0.5])
    with col:
        st.markdown(
            "<div style='text-align:center;padding:10px 0 6px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:1.4rem;font-weight:900;"
            "color:#f59e0b;text-shadow:0 0 20px rgba(245,158,11,.5);"
            "letter-spacing:3px;margin-bottom:4px;'>🏆 RANKING</div>"
            "<div style='font-size:.7rem;color:rgba(255,255,255,.3);letter-spacing:2px;'>"
            "MEJOR PUNTAJE POR GRUPO Y DIFICULTAD</div></div>", unsafe_allow_html=True)

        tab_facil, tab_medio, tab_dificil, tab_global = st.tabs([
            "🟢 Fácil", "🟡 Medio", "🔴 Difícil", "🌐 Global"
        ])
        with tab_facil:
            _render_tabla(obtener_ranking("Fácil"))
        with tab_medio:
            _render_tabla(obtener_ranking("Medio"))
        with tab_dificil:
            _render_tabla(obtener_ranking("Difícil"))
        with tab_global:
            _render_tabla(obtener_ranking())

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ VOLVER AL MENÚ", use_container_width=True):
            navegar("inicio")
