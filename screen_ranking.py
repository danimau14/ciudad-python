import streamlit as st
from session_manager import navegar
from database import obtener_ranking, obtener_estudiantes_ranking

MEDAL   = ["🥇","🥈","🥉"]
D_COLOR = {"Fácil":"#10b981","Normal":"#f59e0b","Difícil":"#ef4444"}
D_ICO   = {"Fácil":"🟢","Normal":"🟡","Difícil":"🔴"}


def _card(i, r):
    pos   = MEDAL[i-1] if i <= 3 else f"#{i}"
    dif   = r.get("dificultad","Normal") or "Normal"
    color = D_COLOR.get(dif,"#a78bfa")
    ico   = D_ICO.get(dif,"⚪")

    logros_list = [l.strip() for l in (r.get("logros") or "").split(",") if l.strip()]
    logros_html = " ".join(
        f'<span style="background:rgba(167,139,250,.1);color:#a78bfa;'
        f'border:1px solid rgba(167,139,250,.25);border-radius:20px;'
        f'padding:2px 8px;font-size:.68rem;margin:2px">🏅 {l}</span>'
        for l in logros_list
    ) if logros_list else '<span style="color:rgba(255,255,255,.2);font-size:.72rem">—</span>'

    ests = obtener_estudiantes_ranking(r.get("grupo_id")) if r.get("grupo_id") else []
    ests_html = " · ".join(f'<span style="color:#94a3b8;font-size:.8rem">{e}</span>' for e in ests) if ests else '<span style="color:rgba(255,255,255,.18);font-size:.8rem">—</span>'

    correctas   = r.get("correctas",0)   or 0
    incorrectas = r.get("incorrectas",0) or 0
    puntaje     = r.get("puntaje",0)     or 0
    fecha       = (r.get("fecha","") or "")[:10]

    st.markdown(f'''<div class="card" style="border-left:4px solid {color}88;margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;
            flex-wrap:wrap;gap:10px">
            <div style="flex:1;min-width:160px">
                <div style="font-size:1.1rem;font-weight:800;color:#f1f5f9;margin-bottom:4px">
                    {pos} {r["nombre_grupo"]}</div>
                <div style="margin-bottom:6px">{ests_html}</div>
                <div style="display:flex;gap:14px;flex-wrap:wrap">
                    <span style="color:#34d399;font-size:.8rem;font-weight:700">✅ {correctas} correctas</span>
                    <span style="color:#f87171;font-size:.8rem;font-weight:700">❌ {incorrectas} incorrectas</span>
                    <span style="color:{color};font-size:.78rem;font-weight:600">{ico} {dif}</span>
                    <span style="color:rgba(255,255,255,.25);font-size:.72rem">{fecha}</span>
                </div>
            </div>
            <div style="text-align:right;min-width:90px">
                <div style="color:#a78bfa;font-weight:900;font-size:1.6rem;
                    font-variant-numeric:tabular-nums">{puntaje}</div>
                <div style="color:rgba(255,255,255,.3);font-size:.7rem">puntos</div>
            </div>
        </div>
        <div style="margin-top:10px;padding-top:10px;
            border-top:1px solid rgba(255,255,255,.06)">
            <div style="font-size:.7rem;color:rgba(255,255,255,.3);
                text-transform:uppercase;letter-spacing:1px;margin-bottom:5px">Logros obtenidos</div>
            {logros_html}
        </div>
    </div>''', unsafe_allow_html=True)


def _lista(filas):
    if not filas:
        st.info("Aún no hay partidas registradas aquí.")
        return
    for i, r in enumerate(filas, 1):
        _card(i, r)


def pantalla_ranking():
    st.markdown('<div class="game-title" style="font-size:clamp(1.6rem,5vw,2.2rem)">🏆 Ranking</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    tf, tn, td, tg = st.tabs(["🟢 Fácil","🟡 Normal","🔴 Difícil","🌐 Global"])
    with tf: _lista(obtener_ranking("Fácil"))
    with tn: _lista(obtener_ranking("Normal"))
    with td: _lista(obtener_ranking("Difícil"))
    with tg: _lista(obtener_ranking())

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Volver al Lobby", use_container_width=True):
        navegar("lobby")
