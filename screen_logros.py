import streamlit as st
from session_manager import navegar
from database import obtener_logros_grupo
from config import LOGROS


def pantalla_logros():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio"); return

    logros_ids = obtener_logros_grupo(gid)
    total  = len(LOGROS)
    obt    = len([l for l in LOGROS if l["id"] in logros_ids])

    st.markdown('<div class="game-title" style="font-size:clamp(1.6rem,5vw,2.2rem)">🏅 Logros</div>', unsafe_allow_html=True)
    st.markdown(f'''<div style="text-align:center;color:rgba(255,255,255,.35);
        font-size:.85rem;margin-bottom:16px">{obt} / {total} desbloqueados</div>''',
        unsafe_allow_html=True)

    # Barra de progreso global
    st.progress(obt / total if total else 0, text=f"{obt}/{total} logros")
    st.markdown("<br>", unsafe_allow_html=True)

    # Agrupar por tipo para mejor lectura
    grupos = {}
    for l in LOGROS:
        t = l.get("tipo","otros")
        grupos.setdefault(t, []).append(l)

    etiquetas = {
        "rondas":"🎮 Primeras Veces","partidas":"📅 Partidas",
        "correctas_total":"📚 Preguntas","correctas_partida":"🎯 Partida Perfecta",
        "correctas_partida_dif":"💫 Sin Fallos","racha":"🔥 Rachas",
        "velocidad":"⚡ Velocidad","victoria":"🏆 Victorias",
        "victoria_3":"👑 Leyenda","victoria_dif_count":"💎 Élite",
        "indicador_fin":"📊 Indicadores","todos_sobre":"🌈 Ciudad Perfecta",
        "min_global":"🛡️ Resistencia","recuperacion":"🚑 Recuperación",
        "decision_count":"🔬 Decisiones","decisiones_todas":"🗺️ Explorador",
        "sin_decision":"♻️ Eco","estrellas":"⭐ Estrellas",
        "atributo_count":"🛡️ Atributos","segunda_ok":"🔄 Segunda Vida",
        "misiones_count":"📋 Misiones","exacto":"🎲 Especiales",
        "eventos_neg_seguidos":"🌪️ Supervivencia","doble_indicador":"🚀 Futuro",
        "rango":"🧩 Equilibrio","tiempo_partida":"🏃 Velocidad Total",
        "recuperacion_total":"😤 Nunca Me Rindo","todos_aciertan":"🤝 Equipo",
        "tam_grupo":"🗣️ Social","dias_jugados":"🎮 Dedicación",
        "ranking_top":"🥇 Ranking","casi_tiempo":"🕐 Tiempo",
    }

    for tipo, logros_grupo in grupos.items():
        label = etiquetas.get(tipo, f"🏅 {tipo.replace('_',' ').title()}")
        with st.expander(label, expanded=False):
            cols = st.columns(2)
            for ci, logro in enumerate(logros_grupo):
                obtenido = logro["id"] in logros_ids
                with cols[ci % 2]:
                    if obtenido:
                        st.markdown(f'''<div style="background:rgba(167,139,250,.1);
                            border:2px solid rgba(167,139,250,.5);border-radius:18px;
                            padding:14px 16px;margin-bottom:10px;
                            box-shadow:0 0 20px rgba(167,139,250,.1)">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                                <span style="font-size:1.5rem">{logro["emoji"]}</span>
                                <div>
                                    <div style="font-weight:800;color:#a78bfa;font-size:.9rem">
                                        {logro["nombre"]}</div>
                                    <span style="background:rgba(167,139,250,.2);color:#a78bfa;
                                        border-radius:20px;padding:2px 8px;font-size:.68rem;
                                        font-weight:700">✅ OBTENIDO</span>
                                </div>
                            </div>
                            <div style="color:#94a3b8;font-size:.8rem">{logro["desc"]}</div>
                            {f'<div style="color:#fbbf24;font-size:.75rem;margin-top:5px">+{logro["estrellas"]} ⭐</div>' if logro.get("estrellas") else ""}
                        </div>''', unsafe_allow_html=True)
                    else:
                        with st.container():
                            st.markdown(f'''<div style="background:rgba(255,255,255,.022);
                                border:1px solid rgba(255,255,255,.07);border-radius:18px;
                                padding:14px 16px;margin-bottom:10px">
                                <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
                                    <span style="font-size:1.5rem;filter:grayscale(1) opacity(.4)">
                                        {logro["emoji"]}</span>
                                    <div>
                                        <div style="font-weight:700;color:rgba(255,255,255,.35);
                                            font-size:.9rem">{logro["nombre"]}</div>
                                        <span style="color:rgba(255,255,255,.2);font-size:.68rem">
                                            🔒 BLOQUEADO</span>
                                    </div>
                                </div>
                                <div style="color:rgba(255,255,255,.2);font-size:.8rem">{logro["desc"]}</div>
                            </div>''', unsafe_allow_html=True)
                            with st.expander("💡 ¿Cómo obtenerlo?"):
                                st.markdown(f'''<div style="color:#a78bfa;font-size:.85rem;
                                    padding:4px 0">{logro["como"]}</div>''', unsafe_allow_html=True)
                                if logro.get("estrellas"):
                                    st.markdown(f'''<div style="color:#fbbf24;font-size:.78rem;
                                        margin-top:4px">Recompensa: {logro["estrellas"]} ⭐</div>''',
                                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Volver al Lobby", use_container_width=True):
        navegar("lobby")
