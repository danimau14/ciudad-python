import streamlit as st
from session_manager import navegar
from database import obtener_misiones_canjeadas, canjear_mision, obtener_estrellas
from config import MISIONES


def pantalla_misiones():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio"); return

    canjeadas = obtener_misiones_canjeadas(gid)
    estrellas = obtener_estrellas(gid)

    st.markdown('<div class="game-title" style="font-size:clamp(1.6rem,5vw,2.2rem)">📋 Misiones</div>', unsafe_allow_html=True)
    st.markdown(f'''<div style="text-align:center;color:rgba(255,255,255,.35);
        font-size:.85rem;margin-bottom:16px">
        {len(canjeadas)}/{len(MISIONES)} completadas · ⭐ {estrellas} estrellas</div>''',
        unsafe_allow_html=True)
    st.markdown("---")

    for m in MISIONES:
        canjeada = m["id"] in canjeadas
        bg    = "rgba(16,185,129,.07)"  if canjeada else "rgba(255,255,255,.03)"
        borde = "rgba(16,185,129,.3)"   if canjeada else "rgba(255,255,255,.08)"
        badge = '<span style="color:#34d399;background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.3);border-radius:20px;padding:2px 9px;font-size:.72rem;font-weight:700">✅ CANJEADA</span>' if canjeada else f'<span style="color:#fbbf24;font-size:.8rem;font-weight:700">+{m["recompensa"]} ⭐</span>'
        dif_tag = "" if m["dif"]=="todas" else f'<span style="color:#a78bfa;background:rgba(167,139,250,.12);border-radius:12px;padding:1px 7px;font-size:.68rem;margin-left:6px">{m["dif"]}</span>'
        st.markdown(f'''<div style="background:{bg};border:1px solid {borde};
            border-radius:16px;padding:14px 18px;margin-bottom:10px;
            display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">
            <div style="flex:1;min-width:180px">
                <div style="font-weight:700;color:#f1f5f9;font-size:.92rem;margin-bottom:3px">
                    {m["nombre"]}{dif_tag}</div>
                <div style="color:rgba(255,255,255,.45);font-size:.82rem">{m["desc"]}</div>
            </div>
            <div style="text-align:right">{badge}</div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Las estrellas de misiones se canjean al **finalizar una partida** desde la pantalla de resultados.")

    if st.button("⬅️ Volver al Lobby", use_container_width=True):
        navegar("lobby")
