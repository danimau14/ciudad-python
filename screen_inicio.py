import streamlit as st
from navigation import navegar
from config import TOTAL_RONDAS, DIFICULTADES
from achievements import LOGROS


# ─── VENTANA PRINCIPAL (login/registro) ──────────────────────────
def pantalla_inicio():
    st.markdown(
        "<div style='text-align:center;padding:40px 0 20px;'>"
        "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
        "font-size:clamp(2.5rem,8vw,4rem);line-height:1;margin-bottom:12px;'>🏙️</div>"
        "<div style='font-family:Orbitron,sans-serif;"
        "font-size:clamp(1.4rem,5vw,2.8rem);font-weight:900;"
        "background:linear-gradient(90deg,#00d4ff,#8b5cf6,#22c55e,#00d4ff);"
        "background-size:300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "background-clip:text;animation:shimmer 4s linear infinite;"
        "letter-spacing:4px;margin-bottom:6px;'>CIUDAD EN EQUILIBRIO</div>"
        "<div style='font-family:Rajdhani,sans-serif;font-size:.8rem;"
        "color:rgba(255,255,255,0.3);letter-spacing:4px;'>SIMULADOR DE PENSAMIENTO SISTÉMICO</div>"
        "</div>",
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown(
            "<div style='text-align:center;font-family:Orbitron,sans-serif;font-size:0.62rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:3px;margin-bottom:16px;'>"
            "ACCESO AL SISTEMA</div>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🔐  INICIAR SESIÓN", use_container_width=True, key="btn_login"):
                navegar("login")
        with b2:
            if st.button("📝  REGISTRAR GRUPO", use_container_width=True, key="btn_reg"):
                navegar("registro")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏆  VER RANKING", use_container_width=True, key="btn_rank_inicio"):
            navegar("ranking")


# ─── LOBBY (después de login) ────────────────────────────────────
def pantalla_lobby():
    nombre_grp = st.session_state.get("grupo_nombre", "Equipo")
    gid        = st.session_state.get("grupo_id")
    logros_gp  = st.session_state.get("logros_obtenidos", [])

    # Título
    st.markdown(
        "<div style='text-align:center;padding:20px 0 10px;'>"
        "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
        "font-size:clamp(2rem,6vw,3rem);line-height:1;margin-bottom:10px;'>🏙️</div>"
        "<div style='font-family:Orbitron,sans-serif;font-size:clamp(1rem,3vw,1.8rem);"
        "font-weight:900;color:#00d4ff;letter-spacing:3px;'>"
        + nombre_grp.upper() +
        "</div>"
        "<div style='font-size:.7rem;color:rgba(255,255,255,.3);letter-spacing:2px;"
        "font-family:Rajdhani,sans-serif;margin-top:4px;'>PANEL DE COMANDO</div>"
        "</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        # ── Selector de dificultad ──────────────────────────────
        st.markdown(
            "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:3px;margin-bottom:10px;'>"
            "SELECCIONA NIVEL DE DIFICULTAD</div>", unsafe_allow_html=True)

        dif_actual = st.session_state.get("dificultad", "Medio")
        d1, d2, d3 = st.columns(3)
        for col_d, (dif_key, dif_val) in zip([d1, d2, d3], DIFICULTADES.items()):
            with col_d:
                selected = dif_actual == dif_key
                border = "rgba(0,212,255,0.8)" if selected else "rgba(255,255,255,0.1)"
                bg     = "rgba(0,212,255,0.12)" if selected else "rgba(5,10,20,0.8)"
                glow   = "0 0 20px rgba(0,212,255,0.3)" if selected else "none"
                col_txt= "#00d4ff" if selected else "#64748b"
                st.markdown(
                    "<div style='background:" + bg + ";border:1.5px solid " + border + ";"
                    "border-radius:12px;padding:12px 8px;text-align:center;"
                    "box-shadow:" + glow + ";transition:all .3s;'>"
                    "<div style='font-size:1.5rem;margin-bottom:6px;'>" + dif_val["icon"] + "</div>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:0.68rem;"
                    "color:" + col_txt + ";font-weight:700;margin-bottom:4px;'>"
                    + dif_key.upper() + "</div>"
                    "<div style='font-size:0.6rem;color:rgba(255,255,255,.3);line-height:1.4;'>"
                    + dif_val["desc"] + "</div></div>", unsafe_allow_html=True)
                if st.button(
                    ("✅ " if selected else "") + "Seleccionar",
                    key="dif_lobby_" + dif_key,
                    use_container_width=True
                ):
                    st.session_state["dificultad"] = dif_key
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Botones de acción ───────────────────────────────────
        col_j, col_i, col_r = st.columns(3)
        with col_j:
            if st.button("🚀  JUGAR", use_container_width=True, key="btn_jugar_lobby"):
                navegar("login_jugar")
        with col_i:
            if st.button("📖  INSTRUCCIONES", use_container_width=True, key="btn_inst_lobby"):
                navegar("instrucciones")
        with col_r:
            if st.button("🏆  RANKING", use_container_width=True, key="btn_rank_lobby"):
                navegar("ranking")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪  CERRAR SESIÓN", use_container_width=True, key="btn_logout"):
            st.session_state["grupo_id"]     = None
            st.session_state["grupo_nombre"] = ""
            navegar("inicio")

    with right:
        # ── Panel de logros ─────────────────────────────────────
        st.markdown(
            "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
            "color:rgba(245,158,11,0.6);letter-spacing:3px;margin-bottom:10px;'>"
            "🏅 LOGROS</div>", unsafe_allow_html=True)

        # Colores de borde según "rareza" del logro
        LOGRO_COLOR = {
            "admin_eficiente":   "#f59e0b",   # dorado
            "ciudad_verde":      "#22c55e",   # verde
            "energia_sost":      "#facc15",   # amarillo
            "economia_boom":     "#3b82f6",   # azul
            "ciudad_feliz":      "#ec4899",   # rosa
            "superviviente":     "#8b5cf6",   # morado
            "maestro_preguntas": "#06b6d4",   # cyan
            "equilibrio_total":  "#f97316",   # naranja
        }

        cols_l = st.columns(2)
        for i, (lkey, ldata) in enumerate(LOGROS.items()):
            obtenido = lkey in logros_gp
            color    = LOGRO_COLOR.get(lkey, "#94a3b8")
            if obtenido:
                bg     = f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.1)"
                border = color
                glow   = f"0 0 14px {color}88, 0 0 28px {color}33"
                icon_op= "1"
                txt_col= color
            else:
                bg     = "rgba(5,10,20,0.7)"
                border = "rgba(255,255,255,0.07)"
                glow   = "none"
                icon_op= "0.25"
                txt_col= "rgba(255,255,255,0.2)"

            with cols_l[i % 2]:
                st.markdown(
                    f"<div style='background:{bg};border:1.5px solid {border};"
                    f"border-radius:10px;padding:10px;text-align:center;"
                    f"box-shadow:{glow};margin-bottom:8px;transition:all .3s;'>"
                    f"<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                    f"font-size:1.6rem;opacity:{icon_op};'>{ldata['icon']}</div>"
                    f"<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;"
                    f"color:{txt_col};font-weight:700;margin:5px 0 3px;line-height:1.3;'>"
                    f"{ldata['nombre']}</div>"
                    f"<div style='font-size:0.55rem;color:rgba(255,255,255,.2);line-height:1.3;'>"
                    f"{ldata['desc']}</div>"
                    f"</div>", unsafe_allow_html=True)


# ─── INSTRUCCIONES ───────────────────────────────────────────────
def pantalla_instrucciones():
    st.markdown(
        "<div style='text-align:center;'>"
        "<span class='emoji-title' style='font-size:2rem;'>📖</span></div>"
        "<div class='game-title' style='font-size:1.8rem;'>Instrucciones</div>",
        unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='card'>
<h3 style='color:#a78bfa;margin-top:0;'>🎯 Objetivo</h3>
<p>Administrar la ciudad durante <b>10 rondas</b>. El juego siempre completa las 10 rondas.</p>
<h3 style='color:#60a5fa;'>📊 Indicadores (inician en 50)</h3>
<p>💰 Economia &nbsp;|&nbsp; 🌿 Medio Ambiente<br>⚡ Energia &nbsp;|&nbsp; 🏥 Bienestar Social</p>
<h3 style='color:#f59e0b;'>⏱️ Temporizador</h3>
<p>Cada pregunta tiene <b>30 segundos</b>. Si se acaba el tiempo, se cuenta como incorrecta.</p>
<h3 style='color:#f87171;'>🔒 Cooldown</h3>
<p>Cada decisión tiene <b>cooldown de 3 rondas</b>. Si la usas en ronda 2, vuelve en ronda 5 (correcta o incorrecta).</p>
</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='card-glow'>
<h3 style='color:#34d399;margin-top:0;'>🔄 Mecánica de Rondas</h3>
<ol style='padding-left:18px;'>
<li>Se selecciona el <b>estudiante en turno</b></li>
<li>El grupo <b>elige una decisión estratégica</b></li>
<li>El estudiante responde una <b>pregunta de opción múltiple</b></li>
<li>✅ Acierta → se aplican los efectos de la decisión</li>
<li>❌ Falla → la decisión no tiene efecto (pero cooldown igual aplica)</li>
<li>Ocurre un <b>evento aleatorio</b></li>
</ol>
</div>
<div class='card-danger'>
<h3 style='color:#f87171;margin-top:0;'>🎯 Dificultad de Preguntas</h3>
<p>🟢 <b>Fácil:</b> preguntas básicas de Python y PSeInt.<br>
🟡 <b>Medio:</b> incluye Cálculo, Física y Matrices.<br>
🔴 <b>Difícil:</b> preguntas avanzadas de todas las materias.</p>
</div>""", unsafe_allow_html=True)
    if st.button("⬅️  Volver", use_container_width=True):
        navegar("lobby")
