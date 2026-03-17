import streamlit as st
from database import obtener_ranking
from session_manager import navegar


def pantalla_ranking():
    st.markdown('<div class="game-title" style="font-size:1.8rem">🏆 Ranking</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    filas = obtener_ranking()
    if not filas:
        st.info("Aún no hay partidas registradas.")
    else:
        for i, r in enumerate(filas, 1):
            medalla = ["🥇","🥈","🥉"][i-1] if i <= 3 else f"{i}."
            st.markdown(f'''<div class="card" style="display:flex;justify-content:space-between;align-items:center">
                <span style="font-size:1.2rem">{medalla} <b style="color:#f1f5f9">{r["nombre_grupo"]}</b></span>
                <span style="color:#a78bfa;font-weight:800;font-size:1.1rem">{r["puntaje"]} pts</span>
            </div>''', unsafe_allow_html=True)

    if st.button("← Volver al Inicio", use_container_width=True):
        navegar("inicio")
