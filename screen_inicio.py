import streamlit as st
from navigation import navegar
from config import DIFICULTADES, TOTAL_RONDAS
from achievements import LOGROS
from database import obtener_progreso, reiniciar_progreso, get_conn

LOGRO_COLOR = {
    "admin_eficiente":   "#f59e0b",
    "ciudad_verde":      "#22c55e",
    "energia_sost":      "#facc15",
    "economia_boom":     "#3b82f6",
    "ciudad_feliz":      "#ec4899",
    "superviviente":     "#8b5cf6",
    "maestro_preguntas": "#06b6d4",
    "equilibrio_total":  "#f97316",
}


# ─── VENTANA PRINCIPAL ───────────────────────────────────────────
def pantalla_inicio():
    st.markdown(
        "<style>@keyframes shimmer{0%{background-position:0%}100%{background-position:200%}}</style>"
        "<div style='text-align:center;padding:50px 0 30px;'>"
        "<div style='font-size:clamp(3rem,10vw,5rem);line-height:1;margin-bottom:16px;'>🏙️</div>"
        "<div style='font-family:Orbitron,sans-serif;font-size:clamp(1.4rem,5vw,2.8rem);"
        "font-weight:900;background:linear-gradient(90deg,#00d4ff,#8b5cf6,#22c55e,#00d4ff);"
        "background-size:300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "background-clip:text;animation:shimmer 4s linear infinite;letter-spacing:4px;"
        "margin-bottom:8px;'>CIUDAD EN EQUILIBRIO</div>"
        "<div style='font-family:Rajdhani,sans-serif;font-size:.85rem;"
        "color:rgba(255,255,255,0.3);letter-spacing:5px;'>SIMULADOR DE PENSAMIENTO SISTÉMICO</div>"
        "</div>", unsafe_allow_html=True)

    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown(
            "<div style='font-family:Orbitron,sans-serif;font-size:0.6rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:3px;text-align:center;"
            "margin-bottom:16px;'>ACCESO AL SISTEMA</div>", unsafe_allow_html=True)
        if st.button("🔐  INICIAR SESIÓN", use_container_width=True, key="btn_login"):
            navegar("login")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("📝  REGISTRAR GRUPO", use_container_width=True, key="btn_reg"):
            navegar("registro")


# ─── LOBBY # ─── LOBBY ───────────────────────────────────────────────────────
def pantalla_lobby():
    nombre_grp = st.session_state.get("grupo_nombre", "Equipo")
    gid        = st.session_state.get("grupo_id")
    logros_gp  = st.session_state.get("logros_obtenidos", [])
    dif_actual = st.session_state.get("dificultad", "Medio")

    # Encabezado
    st.markdown(
        "<div style='text-align:center;padding:20px 0 6px;'>"
        "<div style='font-size:clamp(2rem,6vw,3rem);line-height:1;margin-bottom:8px;'>🏙️</div>"
        "<div style='font-family:Orbitron,sans-serif;font-size:clamp(1rem,3vw,1.6rem);"
        "font-weight:900;color:#00d4ff;letter-spacing:3px;'>" + nombre_grp.upper() + "</div>"
        "<div style='font-size:.65rem;color:rgba(255,255,255,.3);letter-spacing:3px;"
        "font-family:Rajdhani,sans-serif;margin-top:3px;'>PANEL DE COMANDO</div>"
        "</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])

    with left:
        # Selector de dificultad
        st.markdown(
            "<div style='font-family:Orbitron,sans-serif;font-size:0.6rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:3px;margin-bottom:12px;'>"
            "NIVEL DE DIFICULTAD</div>", unsafe_allow_html=True)

        d1, d2, d3 = st.columns(3)
        for col_d, (dif_key, dif_val) in zip([d1, d2, d3], DIFICULTADES.items()):
            with col_d:
                sel    = dif_actual == dif_key
                border = "rgba(0,212,255,0.8)" if sel else "rgba(255,255,255,0.08)"
                bg     = "rgba(0,212,255,0.10)" if sel else "rgba(5,10,20,0.85)"
                glow   = "0 0 18px rgba(0,212,255,0.25)" if sel else "none"
                ctxt   = "#00d4ff" if sel else "#4b5563"
                st.markdown(
                    f"<div style='background:{bg};border:1.5px solid {border};"
                    f"border-radius:12px;padding:12px 6px;text-align:center;"
                    f"box-shadow:{glow};transition:all .3s;'>"
                    f"<div style='font-size:1.4rem;margin-bottom:5px;'>{dif_val['icon']}</div>"
                    f"<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
                    f"color:{ctxt};font-weight:700;margin-bottom:3px;'>{dif_key.upper()}</div>"
                    f"<div style='font-size:0.56rem;color:rgba(255,255,255,.25);line-height:1.4;'>"
                    f"{dif_val['desc']}</div></div>", unsafe_allow_html=True)
                if st.button(
                    ("✅ " if sel else "") + "Seleccionar",
                    key=f"dif_lobby_{dif_key}", use_container_width=True
                ):
                    st.session_state["dificultad"] = dif_key
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Botones de acción
        bj, bi, br = st.columns(3)
        with bj:
            if st.button("🚀  JUGAR", use_container_width=True, key="btn_jugar"):
                _iniciar_juego(gid)
        with bi:
            if st.button("📖  INSTRUCCIONES", use_container_width=True, key="btn_inst"):
                navegar("instrucciones")
        with br:
            if st.button("🏆  RANKING", use_container_width=True, key="btn_rank"):
                navegar("ranking")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏅  VER LOGROS", use_container_width=True, key="btn_logros"):
            navegar("logros")
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("🚪  CERRAR SESIÓN", use_container_width=True, key="btn_logout"):
            for k in ["grupo_id","grupo_nombre","logros_obtenidos","progreso_cargado"]:
                st.session_state.pop(k, None)
            navegar("inicio")

    with right:
        # Panel de logros compacto (preview)
        st.markdown(
            "<div style='font-family:Orbitron,sans-serif;font-size:0.6rem;"
            "color:rgba(245,158,11,0.6);letter-spacing:3px;margin-bottom:10px;'>"
            "🏅 LOGROS</div>", unsafe_allow_html=True)

        cols_l = st.columns(2)
        for i, (lkey, ldata) in enumerate(LOGROS.items()):
            obtenido = lkey in logros_gp
            color    = LOGRO_COLOR.get(lkey, "#94a3b8")
            if obtenido:
                r,g,b  = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
                bg     = f"rgba({r},{g},{b},0.1)"
                border = color
                glow   = f"0 0 12px {color}99, 0 0 24px {color}33"
                op, tc = "1", color
            else:
                bg,border,glow = "rgba(5,10,20,0.8)","rgba(255,255,255,0.06)","none"
                op, tc = "0.2","rgba(255,255,255,0.18)"
            with cols_l[i % 2]:
                st.markdown(
                    f"<div style='background:{bg};border:1.5px solid {border};"
                    f"border-radius:10px;padding:9px 6px;text-align:center;"
                    f"box-shadow:{glow};margin-bottom:7px;transition:all .3s;'>"
                    f"<div style='font-size:1.4rem;opacity:{op};'>{ldata['icon']}</div>"
                    f"<div style='font-family:Orbitron,sans-serif;font-size:0.52rem;"
                    f"color:{tc};font-weight:700;margin:4px 0 2px;line-height:1.3;'>"
                    f"{ldata['nombre']}</div>"
                    f"<div style='font-size:0.5rem;color:rgba(255,255,255,.15);line-height:1.3;'>"
                    f"{ldata['desc']}</div></div>", unsafe_allow_html=True)


def _iniciar_juego(gid):
    """Lógica de inicio de juego desde el lobby."""
    from config import TOTAL_RONDAS
    dif_sel     = st.session_state.get("dificultad", "Medio")
    progreso    = st.session_state.get("progreso_cargado", {})
    partida_fin = progreso.get("partida_terminada", 0) == 1
    dif_guardada= st.session_state.get("dificultad", "Medio")

    if partida_fin and dif_sel == dif_guardada:
        # Misma dificultad ya terminada → pantalla de fin
        st.session_state["resultado"]           = "victoria"
        st.session_state["indicadores_finales"] = {
            k: progreso.get(k, 50) for k in ["economia","medio_ambiente","energia","bienestar_social"]
        }
        st.session_state["rondas_completadas"]  = TOTAL_RONDAS
        st.session_state["ranking_guardado"]    = True
        navegar("fin")
    elif dif_sel != dif_guardada:
        # Nivel diferente → reiniciar progreso y jugar
        reiniciar_progreso(gid)
        conn = get_conn()
        conn.execute("UPDATE grupos SET dificultad=? WHERE id=?", (dif_sel, gid))
        conn.commit(); conn.close()
        _reset_juego()
        navegar("juego")
    else:
        # Misma dificultad en curso → continuar
        navegar("juego")


def _reset_juego():
    st.session_state.update({
        "pregunta_actual": None, "respuesta_correcta": False,
        "decision_elegida": None, "decision_efectos": None,
        "evento_ronda": None, "correctas": 0, "incorrectas": 0,
        "ninguno_critico": True, "preguntas_usadas": [],
        "timer_inicio": None, "tiempo_agotado": False,
        "ranking_guardado": False,
    })


# ─── LOGROS (ventana dedicada) ───────────────────────────────────
def pantalla_logros():
    logros_gp = st.session_state.get("logros_obtenidos", [])
    _,col,_ = st.columns([0.5,3,0.5])
    with col:
        st.markdown(
            "<div style='text-align:center;padding:14px 0 6px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:1.3rem;font-weight:900;"
            "color:#f59e0b;text-shadow:0 0 20px rgba(245,158,11,.5);"
            "letter-spacing:3px;margin-bottom:4px;'>🏅 LOGROS</div>"
            f"<div style='font-size:.68rem;color:rgba(255,255,255,.3);letter-spacing:2px;'>"
            f"{len(logros_gp)} / {len(LOGROS)} OBTENIDOS</div></div>", unsafe_allow_html=True)

        st.markdown(
            "<div style='font-size:.62rem;color:rgba(255,255,255,.25);text-align:center;"
            "margin-bottom:16px;font-family:Rajdhani,sans-serif;letter-spacing:1px;'>"
            "Haz clic en un logro para ver cómo obtenerlo</div>", unsafe_allow_html=True)

        cols = st.columns(4)
        for i, (lkey, ldata) in enumerate(LOGROS.items()):
            obtenido = lkey in logros_gp
            color    = LOGRO_COLOR.get(lkey, "#94a3b8")
            if obtenido:
                r,g,b  = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
                bg     = f"rgba({r},{g},{b},0.1)"
                border = color
                glow   = f"0 0 16px {color}aa, 0 0 32px {color}44"
                op,tc  = "1", color
                estado = f"<div style='font-size:0.5rem;color:{color};font-weight:700;font-family:Orbitron,sans-serif;letter-spacing:1px;margin-top:5px;'>✅ OBTENIDO</div>"
            else:
                bg,border,glow = "rgba(5,10,20,0.85)","rgba(255,255,255,0.06)","none"
                op,tc  = "0.2","rgba(255,255,255,0.2)"
                estado = "<div style='font-size:0.5rem;color:rgba(255,255,255,.15);font-family:Orbitron,sans-serif;letter-spacing:1px;margin-top:5px;'>🔒 BLOQUEADO</div>"

            with cols[i % 4]:
                st.markdown(
                    f"<div style='background:{bg};border:2px solid {border};"
                    f"border-radius:14px;padding:14px 8px;text-align:center;"
                    f"box-shadow:{glow};margin-bottom:4px;transition:all .3s;'>"
                    f"<div style='font-size:1.8rem;opacity:{op};margin-bottom:6px;'>{ldata['icon']}</div>"
                    f"<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;"
                    f"color:{tc};font-weight:700;margin-bottom:3px;line-height:1.3;'>{ldata['nombre']}</div>"
                    f"<div style='font-size:0.52rem;color:rgba(255,255,255,.2);line-height:1.4;'>{ldata['desc']}</div>"
                    f"{estado}</div>", unsafe_allow_html=True)
                # Expander "cómo obtenerlo"
                with st.expander("¿Cómo obtenerlo?"):
                    como = ldata.get("como", ldata["desc"])
                    if obtenido:
                        st.success(f"✅ Ya lo tienes: {como}")
                    else:
                        st.info(f"🎯 {como}")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ VOLVER AL LOBBY", use_container_width=True):
            navegar("lobby")


# ─── INSTRUCCIONES ───────────────────────────────────────────────
def pantalla_instrucciones():
    st.markdown(
        "<div style='text-align:center;'>"
        "<span style='font-size:2rem;'>📖</span></div>"
        "<div class='game-title' style='font-size:1.8rem;'>Instrucciones</div>",
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='card'>
<h3 style='color:#a78bfa;margin-top:0;'>🎯 Objetivo</h3>
<p>Administrar la ciudad durante <b>10 rondas</b>. El juego siempre completa las 10 rondas.</p>
<h3 style='color:#60a5fa;'>📊 Indicadores (inician en 50)</h3>
<p>💰 Economía &nbsp;|&nbsp; 🌿 Medio Ambiente<br>⚡ Energía &nbsp;|&nbsp; 🏥 Bienestar Social</p>
<h3 style='color:#f59e0b;'>⏱️ Temporizador</h3>
<p>Cada pregunta tiene <b>30 segundos</b>. Si se acaba el tiempo, se cuenta como incorrecta.</p>
<h3 style='color:#f87171;'>🔒 Cooldown de Decisiones</h3>
<p>Cada decisión tiene <b>cooldown de 3 rondas</b>.<br>
Si la usas en ronda 2, vuelve disponible en ronda 5.<br>
El cooldown aplica <b>aciertes o falles</b> la pregunta.</p>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='card-glow'>
<h3 style='color:#34d399;margin-top:0;'>🔄 Mecánica de Rondas</h3>
<ol style='padding-left:18px;'>
<li>Se selecciona el <b>estudiante en turno</b></li>
<li>El grupo <b>elige una decisión estratégica</b></li>
<li>El estudiante responde una <b>pregunta de opción múltiple</b></li>
<li>✅ Acierta → se aplican los efectos de la decisión</li>
<li>❌ Falla → sin efecto (cooldown igual aplica)</li>
<li>Ocurre un <b>evento aleatorio</b></li>
</ol>
</div>
<div class='card-danger'>
<h3 style='color:#f87171;margin-top:0;'>🎯 Dificultad de Preguntas</h3>
<p>🟢 <b>Fácil:</b> Python y PSeInt básico.<br>
🟡 <b>Medio:</b> + Cálculo, Física y Matrices.<br>
🔴 <b>Difícil:</b> preguntas avanzadas de todo.</p>
</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️  Volver al Lobby", use_container_width=True):
        navegar("lobby")
