import streamlit as st
from database import obtener_ranking, obtener_estudiantes_ranking
from session_manager import navegar


def _render(filas):
    if not filas:
        st.info("Aún no hay partidas registradas.")
        return
    for i, r in enumerate(filas, 1):
        med     = ["🥇","🥈","🥉"][i-1] if i <= 3 else f"#{i}"
        dif     = r.get("dificultad","Normal") or "Normal"
        dif_col = {"Fácil":"#10b981","Normal":"#f59e0b","Difícil":"#ef4444"}.get(dif,"#a78bfa")
        logros_raw  = r.get("logros","") or ""
        logros_list = [l.strip() for l in logros_raw.split(",") if l.strip()]
        logros_html = " ".join(
            f'<span style="display:inline-block;background:rgba(167,139,250,0.12);'
            f'color:#a78bfa;border:1px solid rgba(167,139,250,0.3);border-radius:20px;'
            f'padding:2px 9px;font-size:0.72rem;margin:2px">🏅 {l}</span>'
            for l in logros_list
        ) if logros_list else '<span style="color:rgba(255,255,255,0.2);font-size:0.75rem">Sin logros</span>'

        gid_r = r.get("grupo_id")
        ests  = obtener_estudiantes_ranking(gid_r) if gid_r else []
        ests_html = " &middot; ".join(
            f'<span style="color:#94a3b8;font-size:0.82rem">{e}</span>' for e in ests
        ) if ests else '<span style="color:rgba(255,255,255,0.2);font-size:0.8rem">—</span>'

        correctas   = r.get("correctas",   0) or 0
        incorrectas = r.get("incorrectas", 0) or 0
        fecha       = (r.get("fecha","") or "")[:10]

        st.markdown(f'''<div class="card" style="margin-bottom:14px">
            <div style="display:flex;justify-content:space-between;
                align-items:flex-start;flex-wrap:wrap;gap:8px">
                <div>
                    <div style="font-size:1.2rem;font-weight:800;color:#f1f5f9;line-height:1.2">
                        {med} {r["nombre_grupo"]}</div>
                    <div style="margin-top:5px">{ests_html}</div>
                </div>
                <div style="text-align:right">
                    <div style="color:#a78bfa;font-weight:900;font-size:1.4rem">
                        {r["puntaje"]} pts</div>
                    <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:3px;flex-wrap:wrap">
                        <span style="color:{dif_col};font-size:0.75rem;font-weight:600">{dif}</span>
                        <span style="color:rgba(255,255,255,0.25);font-size:0.75rem">{fecha}</span>
                    </div>
                </div>
            </div>
            <div style="display:flex;gap:20px;margin:10px 0 8px;flex-wrap:wrap">
                <span style="color:#34d399;font-size:0.82rem">✅ {correctas} correctas</span>
                <span style="color:#f87171;font-size:0.82rem">❌ {incorrectas} incorrectas</span>
            </div>
            <div>{logros_html}</div>
        </div>''', unsafe_allow_html=True)


def pantalla_ranking():
    st.markdown('<div class="game-title" style="font-size:1.8rem">🏆 Ranking</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌐 Global", "🟡 Normal & 🟢 Fácil", "🔴 Difícil"])
    with tab1: _render(obtener_ranking())
    with tab2:
        n = obtener_ranking("Normal")
        f = obtener_ranking("Fácil")
        if n:
            st.markdown("#### 🟡 Normal"); _render(n)
        if f:
            st.markdown("#### 🟢 Fácil");  _render(f)
        if not n and not f:
            st.info("Sin partidas en estas dificultades.")
    with tab3: _render(obtener_ranking("Difícil"))

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Lobby", use_container_width=True):
        navegar("lobby")
