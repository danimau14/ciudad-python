import streamlit as st
from session_manager import navegar
from database import (obtener_estrellas, reiniciar_progreso, obtener_progreso,
                      partida_en_curso, obtener_logros_grupo)
from config import LOGROS, LOGROS_LOBBY, TOTAL_RONDAS, ATRIBUTOS


def pantalla_lobby():
    gid          = st.session_state.get("grupo_id")
    nombre_grupo = st.session_state.get("grupo_nombre", "")
    dif_sel      = st.session_state.get("dificultad_sel", "Normal")
    if not gid:
        navegar("inicio"); return

    estrellas   = obtener_estrellas(gid)
    logros_ids  = obtener_logros_grupo(gid)

    # ── Cabecera ──────────────────────────────────────────────────────────────
    st.markdown(f'''<div style="text-align:center;margin-bottom:14px">
        <div class="game-title" style="font-size:clamp(1.8rem,5vw,2.6rem)">{nombre_grupo}</div>
        <div style="margin-top:10px">
            <span style="color:#fbbf24;font-size:1.2rem;letter-spacing:2px">
                {"⭐"*min(estrellas,15)}</span>
            <br>
            <span style="color:rgba(255,255,255,.3);font-size:.82rem;font-weight:500">
                {estrellas} estrella{"s" if estrellas!=1 else ""} acumulada{"s" if estrellas!=1 else ""}
            </span>
        </div>
    </div>''', unsafe_allow_html=True)
    st.markdown("---")

    # ── Selector de dificultad ────────────────────────────────────────────────
    st.markdown('<div style="font-size:1.1rem;font-weight:700;color:#f1f5f9;margin-bottom:12px">🎮 Selecciona la dificultad</div>', unsafe_allow_html=True)
    dif_info = {
        "Fácil":   ("🟢","#10b981","Penalización ×10 pt · Eventos suaves"),
        "Normal":  ("🟡","#f59e0b","Penalización ×15 pt · Eventos normales"),
        "Difícil": ("🔴","#ef4444","Penalización ×20 pt · Eventos intensos"),
    }
    cols_dif = st.columns(3)
    for col, (dif,(ico,color,desc)) in zip(cols_dif, dif_info.items()):
        with col:
            sel = dif_sel == dif
            en_curso = partida_en_curso(gid, dif)
            borde = color if sel else "rgba(255,255,255,.07)"
            bg    = f"{color}18" if sel else "rgba(255,255,255,.025)"
            badge = ('<div style="margin-top:5px"><span style="background:rgba(251,191,36,.12);'
                     'color:#fbbf24;border:1px solid rgba(251,191,36,.28);border-radius:20px;'
                     'padding:2px 9px;font-size:.7rem">▶ En curso</span></div>') if en_curso else ""
            st.markdown(f'''<div style="background:{bg};border:2px solid {borde};
                border-radius:20px;padding:18px 14px;text-align:center;
                margin-bottom:8px;transition:all .2s">
                <div style="font-size:1.9rem">{ico}</div>
                <div style="font-weight:800;color:#f1f5f9;font-size:1rem;margin-top:5px">{dif}</div>
                <div style="font-size:.72rem;color:rgba(255,255,255,.35);margin-top:3px">{desc}</div>
                {badge}
            </div>''', unsafe_allow_html=True)
            label = f"✅ {dif}" if sel else f"Elegir {dif}"
            if st.button(label, key=f"dif_{dif}", use_container_width=True):
                st.session_state["dificultad_sel"] = dif
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botón JUGAR ───────────────────────────────────────────────────────────
    en_curso_sel = partida_en_curso(gid, dif_sel)
    j1, j2 = st.columns([2, 1])
    with j1:
        lbl = "▶ Continuar Partida" if en_curso_sel else "🚀 Nueva Partida"
        if st.button(lbl, use_container_width=True):
            if not en_curso_sel:
                reiniciar_progreso(gid, dif_sel)
                obtener_progreso(gid, dif_sel)
            _reset_estado_juego()
            navegar("juego")
    with j2:
        if en_curso_sel:
            if st.button("🔄 Reiniciar", use_container_width=True):
                reiniciar_progreso(gid, dif_sel)
                st.rerun()

    # Barra de progreso si hay partida en curso
    if en_curso_sel:
        prog = obtener_progreso(gid, dif_sel)
        ronda_actual = prog.get("ronda_actual", 1)
        pct = int((ronda_actual - 1) / TOTAL_RONDAS * 100)
        st.markdown(f'''<div class="card" style="padding:14px 20px;margin-top:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <span style="color:rgba(255,255,255,.4);font-size:.75rem;text-transform:uppercase;
                    letter-spacing:1px">Partida en curso — {dif_sel}</span>
                <span style="color:#fbbf24;font-size:.82rem;font-weight:700">
                    Ronda {ronda_actual}/{TOTAL_RONDAS}</span>
            </div>
            <div style="background:rgba(255,255,255,.07);border-radius:8px;height:7px">
                <div style="width:{pct}%;background:linear-gradient(90deg,#7c3aed,#a78bfa);
                    height:7px;border-radius:8px"></div>
            </div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Menú secundario ───────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if st.button("🏆 Ranking",   use_container_width=True): navegar("ranking")
    with m2:
        if st.button("📋 Misiones",  use_container_width=True): navegar("misiones")
    with m3:
        if st.button("🏅 Logros",    use_container_width=True): navegar("logros")
    with m4:
        if st.button("📖 Instrucciones", use_container_width=True): navegar("instrucciones")

    # ── 8 logros destacados ───────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:1rem;font-weight:700;color:#f1f5f9;margin-bottom:10px">🏅 Logros Destacados</div>', unsafe_allow_html=True)
    logros_map = {l["id"]: l for l in LOGROS}
    lgrid = st.columns(4)
    for ci, lid in enumerate(LOGROS_LOBBY):
        logro = logros_map.get(lid)
        if not logro: continue
        obtenido = lid in logros_ids
        with lgrid[ci % 4]:
            bg    = "rgba(167,139,250,.12)" if obtenido else "rgba(255,255,255,.025)"
            borde = "rgba(167,139,250,.45)" if obtenido else "rgba(255,255,255,.07)"
            txt   = "#f1f5f9" if obtenido else "rgba(255,255,255,.4)"
            badge = '<span style="color:#a78bfa;font-size:.68rem">✅ OBTENIDO</span>' if obtenido else '<span style="color:rgba(255,255,255,.25);font-size:.68rem">🔒</span>'
            st.markdown(f'''<div style="background:{bg};border:1px solid {borde};
                border-radius:14px;padding:12px;text-align:center;margin-bottom:8px">
                <div style="font-size:1.4rem">{logro["emoji"]}</div>
                <div style="font-size:.78rem;font-weight:700;color:{txt};
                    margin:4px 0 2px">{logro["nombre"]}</div>
                {badge}
            </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Atributos disponibles ─────────────────────────────────────────────────
    with st.expander("⭐ Atributos disponibles con estrellas"):
        st.markdown('<div style="color:rgba(255,255,255,.45);font-size:.82rem;margin-bottom:8px">Activa atributos al inicio de cada ronda durante el juego.</div>', unsafe_allow_html=True)
        acols = st.columns(4)
        for ci, (aid, atr) in enumerate(ATRIBUTOS.items()):
            with acols[ci % 4]:
                puede = estrellas >= atr["costo"]
                color = "#a78bfa" if puede else "rgba(255,255,255,.2)"
                st.markdown(f'''<div style="background:rgba(255,255,255,.03);border:1px solid {color}55;
                    border-radius:12px;padding:10px;text-align:center;margin-bottom:6px">
                    <div style="font-size:1.3rem">{atr["emoji"]}</div>
                    <div style="font-size:.75rem;font-weight:700;color:{color};margin:3px 0">
                        {atr["nombre"]}</div>
                    <div style="font-size:.68rem;color:rgba(255,255,255,.3)">{atr["costo"]} ⭐</div>
                </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.update({
            "grupo_id": None, "grupo_nombre": "",
            "dificultad_sel": "Normal", "logros_obtenidos": []})
        navegar("inicio")


def _reset_estado_juego():
    st.session_state.update({
        "pregunta_actual":   None, "respuesta_correcta": False,
        "decision_elegida":  None, "decision_efectos":   None,
        "evento_ronda":      None, "fase_ronda":         "decision",
        "preguntas_usadas":  [],   "timer_inicio":       None,
        "tiempo_agotado":    False,"correctas":          0,
        "incorrectas":       0,    "logros_partida":     [],
        "racha_actual":      0,    "racha_max":          0,
        "decisiones_usadas_set": set(),
        "correctas_por_est": {},
        "atributos_activos": {},
        "_ranking_guardado": False,
        "_logro_velocidad":  False,
        "_logro_casi_tiempo":False,
        "_min_global_ok":    True,
        "_logro_recuperacion":False,
        "_correctas_dificil":0,
        "_inicio_partida":   __import__("time").time(),
    })
