import streamlit as st
from session_manager import navegar
from database import (obtener_estrellas, reiniciar_progreso,
                      obtener_progreso, partida_en_curso)


def pantalla_lobby():
    gid          = st.session_state.get("grupo_id")
    nombre_grupo = st.session_state.get("grupo_nombre", "")
    dif_sel      = st.session_state.get("dificultad_sel", "Normal")

    if not gid:
        navegar("inicio"); return

    estrellas = obtener_estrellas(gid)
    estrellas_display = min(estrellas, 20)

    # ── Cabecera ──────────────────────────────────────────────────────────────
    st.markdown(f'''<div style="text-align:center;margin-bottom:10px">
        <div class="game-title" style="font-size:2.2rem">🏙️ {nombre_grupo}</div>
        <div style="margin-top:8px">
            <span style="color:#fbbf24;font-size:1.15rem;letter-spacing:1px">
                {"⭐" * estrellas_display}
            </span>
            <br>
            <span style="color:rgba(255,255,255,.35);font-size:.82rem">
                {estrellas} estrella{"s" if estrellas != 1 else ""} acumulada{"s" if estrellas != 1 else ""}
            </span>
        </div>
    </div>''', unsafe_allow_html=True)
    st.markdown("---")

    # ── Selector dificultad ───────────────────────────────────────────────────
    st.markdown("### 🎮 Selecciona la dificultad")
    dif_info = {
        "Fácil":   ("🟢", "#10b981", "Penalización ×0.7 · Eventos suaves"),
        "Normal":  ("🟡", "#f59e0b", "Penalización ×1.0 · Eventos estándar"),
        "Difícil": ("🔴", "#ef4444", "Penalización ×1.3 · Eventos intensos"),
    }
    d1, d2, d3 = st.columns(3)
    for col, (dif, (ico, color, desc)) in zip([d1,d2,d3], dif_info.items()):
        with col:
            selec   = dif_sel == dif
            en_curso = partida_en_curso(gid, dif)
            borde   = color if selec else "rgba(255,255,255,.07)"
            bg      = f"rgba(255,255,255,.07)" if selec else "rgba(255,255,255,.02)"
            badge   = ('<span style="display:inline-block;background:rgba(251,191,36,.15);'
                       'color:#fbbf24;border:1px solid rgba(251,191,36,.3);border-radius:20px;'
                       'padding:1px 8px;font-size:.7rem;margin-top:4px">▶ En curso</span>') if en_curso else ""
            st.markdown(f'''<div style="background:{bg};border:2px solid {borde};
                border-radius:18px;padding:16px 12px;text-align:center;margin-bottom:8px;
                transition:all .2s">
                <div style="font-size:1.7rem">{ico}</div>
                <div style="font-weight:700;color:#f1f5f9;font-size:.95rem;margin-top:4px">{dif}</div>
                <div style="font-size:.72rem;color:rgba(255,255,255,.38);margin-top:3px">{desc}</div>
                <div style="margin-top:5px">{badge}</div>
            </div>''', unsafe_allow_html=True)
            label = f"✅ {dif}" if selec else f"Elegir {dif}"
            if st.button(label, key=f"dif_{dif}", use_container_width=True):
                st.session_state["dificultad_sel"] = dif
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── JUGAR ─────────────────────────────────────────────────────────────────
    en_curso_sel = partida_en_curso(gid, dif_sel)
    j1, j2 = st.columns([2, 1])
    with j1:
        lbl_jugar = "▶ Continuar Partida" if en_curso_sel else "🚀 Nueva Partida"
        if st.button(lbl_jugar, use_container_width=True):
            if not en_curso_sel:
                reiniciar_progreso(gid, dif_sel)
                obtener_progreso(gid, dif_sel)
            st.session_state.update({
                "pregunta_actual":   None, "respuesta_correcta": False,
                "decision_elegida":  None, "decision_efectos":   None,
                "evento_ronda":      None, "fase_ronda":         "decision",
                "preguntas_usadas":  [],   "timer_inicio":       None,
                "tiempo_agotado":    False,"correctas":          0,
                "incorrectas":       0,    "logros_partida":     [],
                "_ranking_guardado": False,
            })
            navegar("juego")
    with j2:
        if en_curso_sel:
            if st.button("🔄 Nueva partida", use_container_width=True):
                reiniciar_progreso(gid, dif_sel)
                st.rerun()
        else:
            if st.button("📖 Instrucciones", use_container_width=True):
                navegar("instrucciones")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Menú secundario ───────────────────────────────────────────────────────
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🏆 Ranking",    use_container_width=True): navegar("ranking")
    with b2:
        if st.button("📋 Misiones",   use_container_width=True): navegar("misiones")
    with b3:
        if st.button("🏅 Ver Logros", use_container_width=True): navegar("logros")

    if en_curso_sel:
        prog = obtener_progreso(gid, dif_sel)
        ronda_actual = prog.get("ronda_actual", 1)
        from config import TOTAL_RONDAS
        pct = int((ronda_actual - 1) / TOTAL_RONDAS * 100)
        st.markdown(f'''<div class="card" style="margin-top:8px;padding:14px 20px">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <span style="color:rgba(255,255,255,.45);font-size:.78rem;text-transform:uppercase;letter-spacing:1px">
                    Partida en curso — {dif_sel}</span>
                <span style="color:#fbbf24;font-size:.82rem;font-weight:600">
                    Ronda {ronda_actual}/{TOTAL_RONDAS}</span>
            </div>
            <div style="background:rgba(255,255,255,.07);border-radius:8px;height:7px">
                <div style="width:{pct}%;background:linear-gradient(90deg,#7c3aed,#a78bfa);
                    height:7px;border-radius:8px"></div>
            </div>
        </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.update({
            "grupo_id": None, "grupo_nombre": "",
            "dificultad_sel": "Normal", "logros_obtenidos": [],
        })
        navegar("inicio")
