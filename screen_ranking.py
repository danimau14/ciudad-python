import streamlit as st
from database import obtener_ranking, obtener_estudiantes_ranking
from session_manager import navegar

MEDAL = ["🥇", "🥈", "🥉"]
DIF_COLOR = {"Fácil": "#10b981", "Normal": "#f59e0b", "Difícil": "#ef4444"}
DIF_ICO   = {"Fácil": "🟢",      "Normal": "🟡",      "Difícil": "🔴"}


def _card(i, r):
    med   = MEDAL[i-1] if i <= 3 else f"#{i}"
    dif   = r.get("dificultad", "Normal") or "Normal"
    color = DIF_COLOR.get(dif, "#a78bfa")
    ico   = DIF_ICO.get(dif, "⚪")

    logros_list = [l.strip() for l in (r.get("logros") or "").split(",") if l.strip()]
    logros_html = " ".join(
        f'<span style="display:inline-block;background:rgba(167,139,250,.12);color:#a78bfa;'
        f'border:1px solid rgba(167,139,250,.28);border-radius:20px;'
        f'padding:2px 9px;font-size:.7rem;margin:2px">🏅 {l}</span>'
        for l in logros_list
    ) if logros_list else '<span style="color:rgba(255,255,255,.2);font-size:.75rem">Sin logros</span>'

    ests = obtener_estudiantes_ranking(r.get("grupo_id")) if r.get("grupo_id") else []
    ests_html = " · ".join(
        f'<span style="color:#94a3b8;font-size:.8rem">{e}</span>' for e in ests
    ) if ests else '<span style="color:rgba(255,255,255,.18);font-size:.8rem">—</span>'

    correctas   = r.get("correctas", 0) or 0
    incorrectas = r.get("incorrectas", 0) or 0
    fecha       = (r.get("fecha", "") or "")[:10]
    puntaje     = r.get("puntaje", 0) or 0

    st.markdown(f'''<div class="card" style="margin-bottom:12px;
        border-left:4px solid {color}88">
        <div style="display:flex;justify-content:space-between;
            align-items:flex-start;flex-wrap:wrap;gap:8px">
            <div style="flex:1;min-width:160px">
                <div style="font-size:1.15rem;font-weight:700;color:#f1f5f9;
                    line-height:1.2;margin-bottom:4px">
                    {med} {r["nombre_grupo"]}</div>
                <div>{ests_html}</div>
            </div>
            <div style="text-align:right;min-width:100px">
                <div style="color:#a78bfa;font-weight:800;font-size:1.4rem;
                    font-variant-numeric:tabular-nums">{puntaje}</div>
                <div style="color:rgba(255,255,255,.3);font-size:.72rem">puntos</div>
                <div style="margin-top:3px">
                    <span style="color:{color};font-size:.72rem;font-weight:600">
                        {ico} {dif}</span>
                    <span style="color:rgba(255,255,255,.2);font-size:.68rem;margin-left:6px">
                        {fecha}</span>
                </div>
            </div>
        </div>
        <div style="display:flex;gap:18px;margin:10px 0 8px;flex-wrap:wrap">
            <span style="color:#34d399;font-size:.8rem;font-weight:600">
                ✅ {correctas} correctas</span>
            <span style="color:#f87171;font-size:.8rem;font-weight:600">
                ❌ {incorrectas} incorrectas</span>
        </div>
        <div>{logros_html}</div>
    </div>''', unsafe_allow_html=True)


def _render_lista(filas):
    if not filas:
        st.info("Aún no hay partidas registradas en esta dificultad.")
        return
    for i, r in enumerate(filas, 1):
        _card(i, r)


def pantalla_ranking():
    st.markdown('<div class="game-title" style="font-size:1.9rem">🏆 Ranking</div>',
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tab_f, tab_n, tab_d, tab_g = st.tabs([
        "🟢 Fácil", "🟡 Normal", "🔴 Difícil", "🌐 Global"
    ])
    with tab_f: _render_lista(obtener_ranking("Fácil"))
    with tab_n: _render_lista(obtener_ranking("Normal"))
    with tab_d: _render_lista(obtener_ranking("Difícil"))
    with tab_g: _render_lista(obtener_ranking())

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Volver al Lobby", use_container_width=True):
        navegar("lobby")
