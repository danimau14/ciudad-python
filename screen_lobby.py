import streamlit as st
from session_manager import navegar
from database import (obtener_estrellas, reiniciar_progreso,
                      obtener_progreso, partida_en_curso, obtener_logros_grupo)
from config import LOGROS, LOGROS_LOBBY, TOTAL_RONDAS, ATRIBUTOS
import time


def pantalla_lobby():
    gid          = st.session_state.get("grupo_id")
    nombre_grupo = st.session_state.get("grupo_nombre", "")
    dif_sel      = st.session_state.get("dificultad_sel", "Normal")
    if not gid:
        navegar("inicio"); return

    estrellas  = obtener_estrellas(gid)
    logros_ids = obtener_logros_grupo(gid)

    # ── Cabecera ──────────────────────────────────────────────────────────────
    st.markdown(f'''
    <div style="text-align:center;padding:10px 0 20px">
        <div style="font-family:Outfit,sans-serif;font-size:clamp(2rem,6vw,3rem);
            font-weight:900;background:linear-gradient(90deg,#a78bfa,#60a5fa,#34d399);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;line-height:1.1;margin-bottom:10px">{nombre_grupo}</div>
        <div style="display:inline-flex;align-items:center;gap:10px;
            background:rgba(251,191,36,.1);border:1px solid rgba(251,191,36,.3);
            border-radius:30px;padding:8px 22px">
            <span style="font-size:1.3rem">⭐</span>
            <span style="color:#fbbf24;font-weight:800;font-size:1.1rem">{estrellas}</span>
            <span style="color:rgba(255,255,255,.35);font-size:.82rem">estrellas acumuladas</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # ── Selector de dificultad ────────────────────────────────────────────────
    st.markdown('''<div style="font-size:.75rem;font-weight:700;color:rgba(255,255,255,.35);
        text-transform:uppercase;letter-spacing:2.5px;margin-bottom:14px;
        font-family:Outfit,sans-serif">🎮 Selecciona la dificultad</div>''',
        unsafe_allow_html=True)

    dif_info = {
        "Fácil":   ("🟢","#10b981","Penalización ×1  · Eventos suaves    · +1 ⭐ por victoria"),
        "Normal":  ("🟡","#f59e0b","Penalización ×1.5· Eventos estándar  · +2 ⭐ por victoria"),
        "Difícil": ("🔴","#ef4444","Penalización ×2  · Eventos intensos  · +4 ⭐ por victoria"),
    }

    cols_dif = st.columns(3)
    for col, (dif, (ico, color, desc)) in zip(cols_dif, dif_info.items()):
        with col:
            sel      = dif_sel == dif
            en_curso = partida_en_curso(gid, dif)
            borde    = color      if sel else "rgba(255,255,255,.06)"
            bg       = f"{color}15" if sel else "rgba(255,255,255,.02)"
            shadow   = f"0 0 28px {color}30" if sel else "none"
            badge_html = (
                '<div style="margin-top:8px">'
                '<span style="background:rgba(251,191,36,.12);color:#fbbf24;'
                'border:1px solid rgba(251,191,36,.3);border-radius:20px;'
                'padding:3px 11px;font-size:.7rem;font-weight:700">▶ En curso</span></div>'
            ) if en_curso else ""

            st.markdown(f'''<div style="background:{bg};border:2px solid {borde};
                border-radius:20px;padding:22px 16px;text-align:center;
                box-shadow:{shadow};transition:all .25s;min-height:130px">
                <div style="font-size:2.2rem;margin-bottom:6px">{ico}</div>
                <div style="font-weight:800;color:#f1f5f9;font-size:1.05rem;
                    font-family:Outfit,sans-serif">{dif}</div>
                <div style="font-size:.68rem;color:rgba(255,255,255,.3);
                    margin-top:5px;line-height:1.5">{desc}</div>
                {badge_html}
            </div>''', unsafe_allow_html=True)

            label = f"✅ {dif}" if sel else f"Elegir {dif}"
            if st.button(label, key=f"dif_{dif}", use_container_width=True):
                st.session_state["dificultad_sel"] = dif
                st.rerun()

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # ── Botón JUGAR / CONTINUAR ───────────────────────────────────────────────
    en_curso_sel = partida_en_curso(gid, dif_sel)

    if en_curso_sel:
        prog         = obtener_progreso(gid, dif_sel)
        ronda_actual = prog.get("ronda_actual", 1)
        pct          = int((ronda_actual - 1) / TOTAL_RONDAS * 100)
        st.markdown(f'''<div style="background:rgba(255,255,255,.03);border:1px solid
            rgba(251,191,36,.2);border-radius:16px;padding:14px 20px;margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;margin-bottom:7px">
                <span style="color:#fbbf24;font-size:.8rem;font-weight:700">
                    ▶ Partida en curso — {dif_sel}</span>
                <span style="color:rgba(255,255,255,.4);font-size:.78rem">
                    Ronda {ronda_actual}/{TOTAL_RONDAS}</span>
            </div>
            <div style="background:rgba(255,255,255,.07);border-radius:8px;height:7px">
                <div style="width:{pct}%;background:linear-gradient(90deg,#7c3aed,#a78bfa);
                    height:7px;border-radius:8px"></div>
            </div>
        </div>''', unsafe_allow_html=True)

    j1, j2 = st.columns([3, 1])
    with j1:
        lbl = "▶  Continuar Partida" if en_curso_sel else "🚀  Nueva Partida"
        if st.button(lbl, use_container_width=True):
            if not en_curso_sel:
                reiniciar_progreso(gid, dif_sel)
            _reset_estado_juego()
            navegar("juego")
    with j2:
        if en_curso_sel:
            if st.button("↺", use_container_width=True, help="Reiniciar partida"):
                reiniciar_progreso(gid, dif_sel)
                st.rerun()

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Menú secundario ───────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if st.button("🏆 Ranking",        use_container_width=True): navegar("ranking")
    with m2:
        if st.button("📋 Misiones",       use_container_width=True): navegar("misiones")
    with m3:
        if st.button("🏅 Logros",         use_container_width=True): navegar("logros")
    with m4:
        if st.button("📖 Instrucciones",  use_container_width=True): navegar("instrucciones")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<hr style="border-color:rgba(255,255,255,.06);margin:0 0 18px">',
                unsafe_allow_html=True)

    # ── 8 logros destacados ───────────────────────────────────────────────────
    st.markdown('''<div style="font-size:.75rem;font-weight:700;color:rgba(255,255,255,.35);
        text-transform:uppercase;letter-spacing:2.5px;margin-bottom:12px;
        font-family:Outfit,sans-serif">🏅 Logros Destacados</div>''',
        unsafe_allow_html=True)

    logros_map = {l["id"]: l for l in LOGROS}
    lgrid = st.columns(4)
    for ci, lid in enumerate(LOGROS_LOBBY):
        logro = logros_map.get(lid)
        if not logro: continue
        obtenido = lid in logros_ids
        with lgrid[ci % 4]:
            bg    = "rgba(167,139,250,.1)"     if obtenido else "rgba(255,255,255,.02)"
            borde = "rgba(167,139,250,.4)"     if obtenido else "rgba(255,255,255,.06)"
            txt   = "#e2e8f0"                  if obtenido else "rgba(255,255,255,.3)"
            badge = ('<span style="color:#a78bfa;font-size:.65rem;font-weight:700">✅</span>'
                     if obtenido else
                     '<span style="color:rgba(255,255,255,.2);font-size:.65rem">🔒</span>')
            st.markdown(f'''<div style="background:{bg};border:1px solid {borde};
                border-radius:16px;padding:14px 10px;text-align:center;margin-bottom:8px;
                transition:all .2s">
                <div style="font-size:1.5rem;margin-bottom:4px">
                    {logro["emoji"] if obtenido else "❓"}</div>
                <div style="font-size:.72rem;font-weight:700;color:{txt};
                    margin-bottom:4px;font-family:Outfit,sans-serif;line-height:1.3">
                    {logro["nombre"] if obtenido else "???"}
                </div>
                {badge}
            </div>''', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Atributos ─────────────────────────────────────────────────────────────
    with st.expander("⭐ Atributos disponibles con estrellas"):
        st.markdown(f'''<div style="color:rgba(255,255,255,.35);font-size:.82rem;
            margin-bottom:12px">Tienes <b style="color:#fbbf24">{estrellas} ⭐</b>.
            Actívalos durante el juego antes de elegir tu decisión.</div>''',
            unsafe_allow_html=True)
        acols = st.columns(4)
        for ci, (aid, atr) in enumerate(ATRIBUTOS.items()):
            with acols[ci % 4]:
                puede = estrellas >= atr["costo"]
                color = "#a78bfa" if puede else "rgba(255,255,255,.2)"
                st.markdown(f'''<div style="background:rgba(255,255,255,.025);
                    border:1px solid {color}44;border-radius:14px;
                    padding:12px 8px;text-align:center;margin-bottom:8px">
                    <div style="font-size:1.3rem">{atr["emoji"]}</div>
                    <div style="font-size:.72rem;font-weight:700;color:{color};
                        margin:4px 0;font-family:Outfit,sans-serif">{atr["nombre"]}</div>
                    <div style="font-size:.65rem;color:rgba(255,255,255,.25);
                        margin-bottom:4px;line-height:1.4">{atr["desc"]}</div>
                    <div style="font-size:.7rem;color:#fbbf24;font-weight:700">
                        {atr["costo"]} ⭐</div>
                </div>''', unsafe_allow_html=True)

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # ── Cerrar sesión ─────────────────────────────────────────────────────────
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.update({
            "grupo_id": None, "grupo_nombre": "",
            "dificultad_sel": "Normal", "logros_obtenidos": []})
        navegar("inicio")


# ── Reset estado de juego (SIN llamar a DB) ───────────────────────────────────
def _reset_estado_juego():
    """Limpia el estado de la sesión para una nueva partida.
       NO hace consultas a la DB — eso lo hace pantalla_juego al arrancar."""
    st.session_state.update({
        "pregunta_actual":      None,
        "respuesta_correcta":   False,
        "decision_elegida":     None,
        "decision_efectos":     None,
        "evento_ronda":         None,
        "fase_ronda":           "decision",
        "preguntas_usadas":     [],
        "timer_inicio":         None,
        "tiempo_agotado":       False,
        "correctas":            0,
        "incorrectas":          0,
        "logros_partida":       [],
        "racha_actual":         0,
        "racha_max":            0,
        "decisiones_usadas_set": set(),
        "correctas_por_est":    {},
        "atributos_activos":    {},
        "_ranking_guardado":    False,
        "_logro_velocidad":     False,
        "_logro_casi_tiempo":   False,
        "_min_global_ok":       True,
        "_logro_recuperacion":  False,
        "_correctas_dificil":   0,
        "_segunda_usada":       False,
        "_estrellas_ganadas":   0,
        "_puntaje_fin":         0,
        "_misiones_pendientes": [],
        "_inicio_partida":      time.time(),
    })
