import streamlit as st
from database import obtener_ranking, obtener_estudiantes_ranking
from session_manager import navegar


def pantalla_ranking():
    st.markdown('<div class="game-title" style="font-size:1.8rem">🏆 Ranking</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌐 Global", "🟢 Fácil · 🟡 Normal", "🔴 Difícil"])

    def render_ranking(filas):
        if not filas:
            st.info("Aún no hay partidas registradas.")
            return
        for i, r in enumerate(filas, 1):
            medalla = ["🥇","🥈","🥉"][i-1] if i <= 3 else f"**#{i}**"
            dif     = r.get("dificultad","Normal")
            dif_col = {"Fácil":"#10b981","Normal":"#f59e0b","Difícil":"#ef4444"}.get(dif,"#a78bfa")
            logros_raw = r.get("logros","") or ""
            logros_list = [l.strip() for l in logros_raw.split(",") if l.strip()]
            logros_html = " ".join(
                f'<span style="background:rgba(167,139,250,0.15);color:#a78bfa;'
                f'border:1px solid rgba(167,139,250,0.3);border-radius:20px;'
                f'padding:2px 8px;font-size:0.72rem;margin:2px;display:inline-block">{l}</span>'
                for l in logros_list
            ) if logros_list else '<span style="color:rgba(255,255,255,0.25);font-size:0.75rem">Sin logros</span>'

            gid_r = r.get("grupo_id")
            estudiantes = obtener_estudiantes_ranking(gid_r) if gid_r else []
            est_html = " · ".join(
                f'<span style="color:#94a3b8">{e}</span>' for e in estudiantes
            ) if estudiantes else '<span style="color:rgba(255,255,255,0.2)">—</span>'

            correctas   = r.get("correctas", 0) or 0
            incorrectas = r.get("incorrectas", 0) or 0

            st.markdown(f'''
            <div class="card" style="margin-bottom:12px">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;
                    flex-wrap:wrap;gap:8px">
                    <div>
                        <div style="font-size:1.15rem;font-weight:800;color:#f1f5f9">
                            {medalla} {r["nombre_grupo"]}</div>
                        <div style="margin-top:4px;font-size:0.8rem">{est_html}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="color:#a78bfa;font-weight:900;font-size:1.3rem">
                            {r["puntaje"]} pts</div>
                        <div style="font-size:0.75rem;color:{dif_col};font-weight:600">
                            {dif}</div>
                    </div>
                </div>
                <div style="display:flex;gap:16px;margin:10px 0 6px;flex-wrap:wrap">
                    <span style="color:#34d399;font-size:0.8rem">✅ {correctas} correctas</span>
                    <span style="color:#f87171;font-size:0.8rem">❌ {incorrectas} incorrectas</span>
                </div>
                <div style="margin-top:6px">{logros_html}</div>
            </div>''', unsafe_allow_html=True)

    with tab1:
        render_ranking(obtener_ranking())
    with tab2:
        facil  = obtener_ranking("Fácil")
        normal = obtener_ranking("Normal")
        if facil:
            st.markdown("#### 🟢 Fácil")
            render_ranking(facil)
        if normal:
            st.markdown("#### 🟡 Normal")
            render_ranking(normal)
        if not facil and not normal:
            st.info("Sin partidas en estas dificultades.")
    with tab3:
        render_ranking(obtener_ranking("Difícil"))

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Lobby", use_container_width=True):
        navegar("lobby")
