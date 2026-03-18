import streamlit as st
import time
from database import (reiniciar_progreso, guardar_ranking, sumar_estrellas,
                      obtener_estrellas, actualizar_stats, obtener_stats)
from session_manager import navegar
from config import TOTAL_RONDAS, DIFICULTADES, UMBRAL_ROJO, LOGROS
from utils import evaluar_logros, evaluar_misiones_partida, calcular_puntaje, hay_colapso
from database import canjear_mision


def _barra(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    color = "#10b981" if valor >= 60 else "#f59e0b" if valor >= UMBRAL_ROJO else "#ef4444"
    badge = "Estable" if valor >= 60 else "Precaución" if valor >= UMBRAL_ROJO else "Crítico"
    st.markdown(f'''<div style="background:rgba(255,255,255,.04);border:1px solid {color}44;
        border-radius:16px;padding:14px 18px;margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;margin-bottom:7px">
            <span style="font-weight:700;color:#f1f5f9;font-family:Outfit,sans-serif">
                {emoji} {nombre}</span>
            <span style="font-size:.72rem;color:{color};font-weight:700;
                background:{color}22;border-radius:20px;padding:2px 8px">{badge}</span>
        </div>
        <div style="background:rgba(255,255,255,.08);border-radius:6px;height:9px">
            <div style="width:{valor}%;background:{color};height:9px;border-radius:6px;
                transition:width .4s ease"></div>
        </div>
        <div style="text-align:right;margin-top:5px;font-size:.82rem;
            font-weight:700;color:{color}">{valor}/100</div>
    </div>''', unsafe_allow_html=True)


def pantalla_fin():
    resultado    = st.session_state.get("resultado", "desconocido")
    ind_fin      = st.session_state.get("indicadores_finales", {})
    rondas_comp  = st.session_state.get("rondas_completadas", 0)
    correctas    = st.session_state.get("correctas", 0)
    incorrectas  = st.session_state.get("incorrectas", 0)
    gid          = st.session_state.get("grupo_id")
    nombre_grupo = st.session_state.get("grupo_nombre", "")
    dificultad   = st.session_state.get("dificultad_sel", "Normal")
    racha_max    = st.session_state.get("racha_max", 0)
    decisiones_usadas_set = st.session_state.get("decisiones_usadas_set", set())
    correctas_por_est     = st.session_state.get("correctas_por_est", {})
    estudiantes           = st.session_state.get("estudiantes_juego", [])
    tiempo_seg            = int(time.time() - st.session_state.get("_inicio_partida", time.time()))
    victoria              = resultado == "victoria"

    # ── Evaluar logros + guardar ranking (una sola vez) ───────────────────────
    if not st.session_state.get("_ranking_guardado"):
        # Logros nuevos
        nuevos_logros = evaluar_logros(
            gid, ind_fin, correctas, incorrectas, dificultad,
            racha_max, decisiones_usadas_set, tiempo_seg,
            estudiantes, correctas_por_est)
        st.session_state["logros_partida"] = nuevos_logros

        # Estrellas por victoria
        estrellas_ganadas = 0
        if victoria:
            cfg_dif = DIFICULTADES.get(dificultad, DIFICULTADES["Normal"])
            estrellas_ganadas = cfg_dif["estrellas"]
            sumar_estrellas(gid, estrellas_ganadas)
        st.session_state["_estrellas_ganadas"] = estrellas_ganadas

        # Puntaje
        puntaje = calcular_puntaje(ind_fin, correctas, incorrectas)
        logros_nombres = [l["nombre"] for l in LOGROS if l["id"] in nuevos_logros]
        try:
            guardar_ranking(gid, nombre_grupo, puntaje, correctas,
                            incorrectas, dificultad, logros_nombres)
        except Exception:
            pass

        # Actualizar stats globales
        stats = obtener_stats(gid)
        d_key = {"Fácil":"victorias_facil","Normal":"victorias_normal","Difícil":"victorias_dificil"}
        actualizar_stats(gid,
            partidas_total   = stats.get("partidas_total",0) + 1,
            correctas_total  = stats.get("correctas_total",0) + correctas,
            racha_max        = max(stats.get("racha_max",0), racha_max),
            **({d_key[dificultad]: stats.get(d_key[dificultad],0)+1} if victoria else {}),
        )

        st.session_state["_ranking_guardado"] = True
        st.session_state["_puntaje_fin"]      = puntaje
        st.session_state["_misiones_pendientes"] = evaluar_misiones_partida(
            gid, ind_fin, correctas, dificultad, racha_max, victoria)

    logros_part       = st.session_state.get("logros_partida", [])
    estrellas_ganadas = st.session_state.get("_estrellas_ganadas", 0)
    puntaje           = st.session_state.get("_puntaje_fin", 0)
    misiones_pend     = st.session_state.get("_misiones_pendientes", [])

    # ── Banner resultado ──────────────────────────────────────────────────────
    if victoria:
        st.balloons()
        col_r  = "#10b981"
        bg_r   = "rgba(16,185,129,.12)"
        ico, tit = "🏆", "¡Ciudad Equilibrada!"
        sub    = f"El grupo administró la ciudad durante las {TOTAL_RONDAS} rondas exitosamente."
    else:
        col_r  = "#ef4444"
        bg_r   = "rgba(239,68,68,.12)"
        ico, tit = "💥", "La Ciudad Colapsó"
        sub    = "Un indicador llegó al límite crítico o el promedio fue insuficiente."

    cfg_dif   = DIFICULTADES.get(dificultad, DIFICULTADES["Normal"])
    dif_color = {"Fácil":"#10b981","Normal":"#f59e0b","Difícil":"#ef4444"}.get(dificultad,"#a78bfa")
    dif_ico   = {"Fácil":"🟢","Normal":"🟡","Difícil":"🔴"}.get(dificultad,"⚪")

    st.markdown(f'''<div style="background:{bg_r};border:2px solid {col_r}44;
        border-radius:22px;padding:36px;text-align:center;margin-bottom:22px">
        <div style="font-size:3.5rem">{ico}</div>
        <h1 style="color:{col_r};margin:10px 0 6px;font-size:clamp(1.4rem,5vw,2rem);
            font-family:Outfit,sans-serif">{tit}</h1>
        <p style="color:rgba(255,255,255,.5);margin-bottom:16px">{sub}</p>
        <div style="display:flex;justify-content:center;gap:22px;flex-wrap:wrap;margin-bottom:12px">
            <span style="color:#34d399;font-weight:700">✅ {correctas} correctas</span>
            <span style="color:#f87171;font-weight:700">❌ {incorrectas} incorrectas</span>
            <span style="color:#60a5fa;font-weight:700">🔄 {rondas_comp}/{TOTAL_RONDAS} rondas</span>
            <span style="color:#a78bfa;font-weight:700">🎯 {puntaje} pts</span>
        </div>
        <div style="display:flex;justify-content:center;gap:14px;flex-wrap:wrap">
            <span style="background:{dif_color}22;color:{dif_color};border:1px solid {dif_color}44;
                border-radius:20px;padding:3px 14px;font-size:.82rem;font-weight:700">
                {dif_ico} {dificultad}</span>
            {f'<span style="background:rgba(251,191,36,.15);color:#fbbf24;border:1px solid rgba(251,191,36,.35);border-radius:20px;padding:3px 14px;font-size:.82rem;font-weight:700">+{estrellas_ganadas} ⭐ ganadas</span>' if estrellas_ganadas else ""}
        </div>
    </div>''', unsafe_allow_html=True)

    # ── Logros desbloqueados ──────────────────────────────────────────────────
    if logros_part:
        logros_map = {l["id"]: l for l in LOGROS}
        badges = " ".join(
            f'<span style="display:inline-block;background:rgba(167,139,250,.15);color:#a78bfa;'
            f'border:1px solid rgba(167,139,250,.4);border-radius:20px;padding:4px 14px;'
            f'font-size:.85rem;margin:3px;font-family:Outfit,sans-serif">'
            f'🏅 {logros_map[lid]["nombre"] if lid in logros_map else lid}</span>'
            for lid in logros_part)
        st.markdown(f'''<div class="card-glow" style="text-align:center;padding:18px;margin-bottom:18px">
            <div style="color:rgba(255,255,255,.4);font-size:.75rem;text-transform:uppercase;
                letter-spacing:1.5px;margin-bottom:10px">🏅 Nuevos Logros Desbloqueados</div>
            {badges}</div>''', unsafe_allow_html=True)

    # ── Misiones cumplidas para canjear ───────────────────────────────────────
    if misiones_pend:
        st.markdown('<div style="font-size:1rem;font-weight:700;color:#f1f5f9;'
                    'font-family:Outfit,sans-serif;margin-bottom:10px">'
                    '📋 Misiones completadas — Canjea tus estrellas</div>',
                    unsafe_allow_html=True)
        for m in misiones_pend:
            col_m1, col_m2 = st.columns([3, 1])
            with col_m1:
                st.markdown(f'''<div style="background:rgba(16,185,129,.07);
                    border:1px solid rgba(16,185,129,.25);border-radius:14px;
                    padding:12px 16px;margin-bottom:6px">
                    <div style="font-weight:700;color:#f1f5f9;font-family:Outfit,sans-serif">
                        {m["nombre"]}</div>
                    <div style="color:rgba(255,255,255,.4);font-size:.82rem">{m["desc"]}</div>
                </div>''', unsafe_allow_html=True)
            with col_m2:
                if st.button(f"⭐ +{m['recompensa']}", key=f"canje_{m['id']}",
                             use_container_width=True):
                    if canjear_mision(gid, m["id"], m["recompensa"]):
                        st.success(f"+{m['recompensa']} ⭐ canjeadas")
                        # Eliminar de pendientes para no mostrar de nuevo
                        st.session_state["_misiones_pendientes"] = [
                            x for x in misiones_pend if x["id"] != m["id"]]
                        st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Indicadores finales ───────────────────────────────────────────────────
    st.markdown('<div style="font-size:1rem;font-weight:700;color:#f1f5f9;'
                'font-family:Outfit,sans-serif;margin-bottom:10px">📊 Indicadores Finales</div>',
                unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    with f1: _barra("Economía",       ind_fin.get("economia",0),         "💰")
    with f2: _barra("Medio Ambiente", ind_fin.get("medio_ambiente",0),   "🌿")
    with f3: _barra("Energía",        ind_fin.get("energia",0),          "⚡")
    with f4: _barra("Bienestar",      ind_fin.get("bienestar_social",0), "❤️")

    # ── Estrellas actuales ────────────────────────────────────────────────────
    estrellas_actuales = obtener_estrellas(gid)
    st.markdown(f'''<div style="text-align:center;margin:18px 0 10px">
        <span style="color:#fbbf24;font-size:1.1rem">⭐</span>
        <span style="color:rgba(255,255,255,.5);font-size:.85rem;margin-left:6px">
            Total de estrellas: </span>
        <span style="color:#fbbf24;font-weight:800;font-size:1rem">{estrellas_actuales}</span>
    </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botones de navegación ─────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 Jugar de Nuevo", use_container_width=True):
            if gid: reiniciar_progreso(gid, dificultad)
            st.session_state.update({
                "pregunta_actual":    None,  "respuesta_correcta": False,
                "decision_elegida":   None,  "decision_efectos":   None,
                "evento_ronda":       None,  "fase_ronda":         "decision",
                "preguntas_usadas":   [],    "timer_inicio":       None,
                "tiempo_agotado":     False, "correctas":          0,
                "incorrectas":        0,     "logros_partida":     [],
                "_ranking_guardado":  False, "racha_actual":       0,
                "racha_max":          0,     "decisiones_usadas_set": set(),
                "correctas_por_est":  {},    "atributos_activos":  {},
                "_estrellas_ganadas": 0,     "_puntaje_fin":       0,
                "_misiones_pendientes": [],  "_inicio_partida":    __import__("time").time(),
            })
            navegar("lobby")
    with c2:
        if st.button("🏆 Ver Ranking", use_container_width=True):
            navegar("ranking")
    with c3:
        if st.button("🏠 Volver al Lobby", use_container_width=True):
            navegar("lobby")
