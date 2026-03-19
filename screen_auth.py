import streamlit as st
import streamlit.components.v1 as components
from session_manager import navegar
from database import login_grupo, registrar_grupo, guardar_estudiante
import re

MIN_EST = 3
MAX_EST = 5
REGEX_NOMBRE = r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+"

# ── CSS compartido ────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&family=Courier+Prime:wght@400;700&display=swap');

#MainMenu, footer, header,
[data-testid="stToolbar"],
.stDeployButton { display: none !important; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main, .block-container {
    background: #07001a !important;
    padding: 0 !important; margin: 0 auto !important;
    max-width: 100% !important; min-height: 100vh !important;
}
.block-container {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 100vh !important;
    padding: 24px 16px !important;
    max-width: min(500px, 96vw) !important;
}

/* Inputs */
.stTextInput label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .76rem !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 2px !important;
    color: rgba(167,139,250,.65) !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(123,47,255,.28) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Courier Prime', monospace !important;
    font-size: .90rem !important; padding: 10px 14px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(167,139,250,.65) !important;
    box-shadow: 0 0 0 3px rgba(123,47,255,.13) !important;
}

/* Form submit */
.stFormSubmitButton button {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .93rem !important; font-weight: 700 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: 12px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,.40) !important;
    transition: all .22s ease !important; width: 100% !important;
}
.stFormSubmitButton button:hover {
    background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
    box-shadow: 0 6px 32px rgba(124,58,237,.58) !important;
    transform: translateY(-2px) !important;
}

/* Botón primario */
.auth-primary .stButton button {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .90rem !important; font-weight: 700 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    color: #fff !important; border: none !important;
    border-radius: 12px !important; padding: 11px !important;
    box-shadow: 0 4px 18px rgba(124,58,237,.38) !important;
    transition: all .22s ease !important; width: 100% !important;
}
.auth-primary .stButton button:hover {
    background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
    box-shadow: 0 6px 28px rgba(124,58,237,.55) !important;
    transform: translateY(-2px) !important;
}

/* Botón volver */
.auth-back .stButton button {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .78rem !important; font-weight: 600 !important;
    background: transparent !important;
    color: rgba(148,163,184,.55) !important;
    border: 1px solid rgba(255,255,255,.07) !important;
    border-radius: 10px !important; padding: 8px !important;
    transition: all .2s !important; width: 100% !important;
}
.auth-back .stButton button:hover {
    color: #c4b5fd !important;
    border-color: rgba(167,139,250,.32) !important;
    background: rgba(167,139,250,.05) !important;
}
</style>
"""


def _estrellas_fondo(color_acento="#a78bfa"):
    """Canvas de estrellas animadas (iframe 0px altura)."""
    components.html(
        "<style>body{margin:0;background:transparent;overflow:hidden}</style>"
        "<canvas id='c' style='position:fixed;top:0;left:0;"
        "width:100vw;height:100vh;pointer-events:none;z-index:0'></canvas>"
        "<script>"
        "var c=document.getElementById('c'),cx=c.getContext('2d');"
        "function rs(){c.width=window.innerWidth;c.height=window.innerHeight}rs();"
        "var S=[],COL=['#fff','#c4b5fd','#a78bfa','" + color_acento + "'];"
        "for(var i=0;i<130;i++)S.push({x:Math.random()*c.width,"
        "y:Math.random()*c.height,r:Math.random()*1.3+.2,"
        "a:Math.random()*.55+.1,da:(Math.random()*.009+.002)*(Math.random()<.5?1:-1),"
        "dx:(Math.random()-.5)*.16,dy:(Math.random()-.5)*.1,"
        "col:COL[Math.floor(Math.random()*COL.length)]});"
        "function draw(){cx.clearRect(0,0,c.width,c.height);"
        "S.forEach(function(s){s.x+=s.dx;s.y+=s.dy;s.a+=s.da;"
        "if(s.a>.88||s.a<.06)s.da*=-1;"
        "if(s.x<0)s.x=c.width;if(s.x>c.width)s.x=0;"
        "if(s.y<0)s.y=c.height;if(s.y>c.height)s.y=0;"
        "cx.save();cx.globalAlpha=s.a;cx.beginPath();"
        "cx.arc(s.x,s.y,s.r,0,Math.PI*2);"
        "cx.fillStyle=s.col;cx.shadowColor=s.col;cx.shadowBlur=s.r*4;"
        "cx.fill();cx.restore();});"
        "requestAnimationFrame(draw);}draw();"
        "window.addEventListener('resize',rs);</script>",
        height=0, scrolling=False)


def _card_abierto(color_top, color_nebula):
    """Abre el card visual (nebulosa + borde + línea animada)."""
    st.markdown(
        "<div style='position:fixed;inset:0;z-index:0;pointer-events:none;"
        "background:radial-gradient(ellipse 65% 50% at 18% 28%,"
        + color_nebula + " 0%,transparent 55%),"
        "radial-gradient(ellipse 50% 58% at 82% 72%,"
        "rgba(79,70,229,.16) 0%,transparent 55%)'></div>"

        "<div style='position:relative;z-index:1;width:100%;"
        "background:rgba(10,3,30,.93);"
        "border:1px solid rgba(123,47,255,.38);"
        "border-top:2px solid " + color_top + ";"
        "border-radius:20px;overflow:hidden;"
        "box-shadow:0 0 60px rgba(123,47,255,.14),0 24px 48px rgba(0,0,0,.5);"
        "animation:fadein .6s ease both'>"
        "<style>@keyframes fadein{from{opacity:0;transform:translateY(18px)}"
        "to{opacity:1;transform:translateY(0)}}</style>"

        # Línea de energía
        "<div style='position:absolute;top:0;left:0;right:0;height:2px;overflow:hidden'>"
        "<div style='height:2px;background:linear-gradient(90deg,transparent,"
        + color_top + ",transparent);"
        "animation:sweep 2.5s linear infinite'></div></div>"
        "<style>@keyframes sweep{0%{transform:translateX(-100%)}"
        "100%{transform:translateX(200%)}}</style>"

        "<div style='padding:24px 24px 20px'>",
        unsafe_allow_html=True)


def _card_cerrado():
    st.markdown("</div></div>", unsafe_allow_html=True)


def _header_card(emoji, titulo, subtitulo):
    st.markdown(
        "<div style='text-align:center;margin-bottom:18px'>"
        "<div style='font-size:2.8rem;margin-bottom:10px;"
        "filter:drop-shadow(0 0 18px rgba(123,47,255,.75))'>" + emoji + "</div>"
        "<div style='font-family:Press Start 2P,monospace;"
        "font-size:clamp(.60rem,2.3vw,.84rem);"
        "background:linear-gradient(90deg,#c4b5fd,#818cf8,#60a5fa);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "letter-spacing:2px;line-height:1.6;margin-bottom:5px'>" + titulo + "</div>"
        "<div style='font-family:Rajdhani,sans-serif;font-size:.70rem;"
        "color:rgba(167,139,250,.42);letter-spacing:3px;text-transform:uppercase'>"
        + subtitulo + "</div></div>"
        "<div style='height:1px;background:linear-gradient(90deg,transparent,"
        "rgba(123,47,255,.4),rgba(99,102,241,.4),transparent);margin-bottom:18px'></div>",
        unsafe_allow_html=True)


def _error_card(msg):
    st.markdown(
        "<div style='background:rgba(239,68,68,.07);"
        "border:1px solid rgba(239,68,68,.28);"
        "border-radius:9px;padding:9px 13px;margin-top:8px;"
        "font-family:Rajdhani,sans-serif;font-size:.82rem;"
        "color:#fca5a5;text-align:center'>" + msg + "</div>",
        unsafe_allow_html=True)


def _exito_card(msg):
    st.markdown(
        "<div style='background:rgba(52,211,153,.07);"
        "border:1px solid rgba(52,211,153,.25);"
        "border-radius:9px;padding:9px 13px;margin-bottom:10px;"
        "font-family:Rajdhani,sans-serif;font-size:.82rem;"
        "color:#6ee7b7;text-align:center'>" + msg + "</div>",
        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA LOGIN
#  Flujo: pantalla_login() → login_grupo(nombre, pw) [database.py]
#         → grupo_id guardado en session_state → navegar("lobby")
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_login():
    st.markdown(_CSS, unsafe_allow_html=True)
    _estrellas_fondo("#818cf8")
    _card_abierto("rgba(167,139,250,.65)", "rgba(123,47,255,.20)")
    _header_card("🔐", "INICIAR SESIÓN", "Accede a tu ciudad")

    error_msg = st.session_state.pop("_login_error", None)
    if error_msg:
        _error_card(error_msg)

    with st.form("form_login", clear_on_submit=False):
        nombre = st.text_input("👥  Nombre del grupo",
                               placeholder="Nombre de tu equipo",
                               key="li_nombre")
        pw     = st.text_input("🔒  Contraseña",
                               type="password",
                               placeholder="••••••••",
                               key="li_pw")
        sub    = st.form_submit_button("🚀  ENTRAR AL JUEGO", use_container_width=True)

    if sub:
        nombre_v = st.session_state.get("li_nombre", "").strip()
        pw_v     = st.session_state.get("li_pw", "")

        if not nombre_v:
            st.session_state["_login_error"] = "⚠️ Ingresa el nombre del grupo."
            st.rerun()
        elif not pw_v:
            st.session_state["_login_error"] = "⚠️ Ingresa la contraseña."
            st.rerun()
        else:
            # ── Consulta a database.py → database.db ─────────────────────────
            gid = login_grupo(nombre_v, pw_v)
            if gid:
                # Login exitoso: guardar en session_state y navegar al lobby
                st.session_state["grupo_id"]     = gid
                st.session_state["grupo_nombre"] = nombre_v
                navegar("lobby")            # → router → pantalla_lobby()
            else:
                st.session_state["_login_error"] = "❌ Nombre o contraseña incorrectos."
                st.rerun()

    st.markdown(
        "<div style='height:1px;background:rgba(255,255,255,.05);margin:16px 0'></div>",
        unsafe_allow_html=True)

    st.markdown('<div class="auth-back">', unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL INICIO", use_container_width=True, key="btn_back_login"):
        navegar("inicio")
    st.markdown('</div>', unsafe_allow_html=True)

    _card_cerrado()


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA REGISTRO
#  Flujo:
#    Paso 1: registrar_grupo(nombre, pw) [database.py] → grupo_id
#    Paso 2: guardar_estudiante(gid, nombre) [database.py] × N
#    Final:  grupo_id guardado en session_state → navegar("lobby")
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_registro():
    st.markdown(_CSS, unsafe_allow_html=True)
    _estrellas_fondo("#34d399")

    gid_reg     = st.session_state.get("grupo_id_registro")
    estudiantes = st.session_state.get("estudiantes_temp", [])
    paso        = 2 if gid_reg else 1

    # ── Barra de pasos ────────────────────────────────────────────────────────
    pasos_info = [("1", "Datos", paso > 1), ("2", "Equipo", paso == 2), ("3", "¡Listo!", False)]
    items_html = ""
    for idx, (num, label, done) in enumerate(pasos_info):
        actual  = (int(num) == paso)
        bg_c    = "#7c3aed" if done else ("#a78bfa" if actual else "rgba(255,255,255,.07)")
        col_c   = "#fff"    if (done or actual) else "rgba(255,255,255,.2)"
        brd_c   = "#7c3aed" if done else ("#a78bfa" if actual else "rgba(255,255,255,.09)")
        txt_c   = "#c4b5fd" if actual else ("#6ee7b7" if done else "rgba(255,255,255,.2)")
        symbol  = "✓" if done else num
        items_html += (
            "<div style='display:flex;flex-direction:column;align-items:center;flex:1'>"
            "<div style='width:26px;height:26px;border-radius:50%;"
            "background:" + bg_c + ";border:1.5px solid " + brd_c + ";"
            "display:flex;align-items:center;justify-content:center;"
            "font-size:.68rem;font-weight:700;color:" + col_c + ";margin-bottom:4px'>"
            + symbol + "</div>"
            "<div style='font-family:Rajdhani,sans-serif;font-size:.58rem;"
            "text-transform:uppercase;letter-spacing:1px;color:" + txt_c + "'>"
            + label + "</div></div>")
        if idx < len(pasos_info) - 1:
            ln = "#7c3aed" if int(num) < paso else "rgba(255,255,255,.07)"
            items_html += (
                "<div style='flex:1;height:1.5px;background:" + ln + ";"
                "margin:13px 4px 0;align-self:flex-start'></div>")

    color_top = "rgba(52,211,153,.55)" if paso == 2 else "rgba(167,139,250,.60)"
    _card_abierto(color_top, "rgba(52,211,153,.14)")

    # Header con barra de pasos incluida
    emoji_h = "👥" if paso == 2 else "📝"
    _header_card(emoji_h, "REGISTRAR GRUPO", "Crea tu equipo de control")

    st.markdown(
        "<div style='display:flex;align-items:flex-start;gap:0;padding:0 4px 16px'>"
        + items_html + "</div>"
        "<div style='height:1px;background:rgba(255,255,255,.05);margin-bottom:16px'></div>",
        unsafe_allow_html=True)

    error_msg = st.session_state.pop("_reg_error", None)
    if error_msg:
        _error_card(error_msg)

    # ══ PASO 1: Crear grupo ═══════════════════════════════════════════════════
    if not gid_reg:
        st.markdown(
            "<div style='background:rgba(52,211,153,.05);"
            "border:1px solid rgba(52,211,153,.16);"
            "border-radius:9px;padding:9px 13px;margin-bottom:14px;"
            "font-family:Rajdhani,sans-serif;font-size:.76rem;"
            "color:rgba(52,211,153,.7);line-height:1.7'>"
            "1️⃣ Crea el grupo &nbsp;→&nbsp; "
            "2️⃣ Agrega <b style='color:#34d399'>" + str(MIN_EST) + "–" + str(MAX_EST) + "</b>"
            " estudiantes &nbsp;→&nbsp; 3️⃣ ¡A jugar!</div>",
            unsafe_allow_html=True)

        with st.form("form_registro", clear_on_submit=False):
            nombre = st.text_input("👥  Nombre del grupo",
                                   placeholder="Ej: Equipo Titán",
                                   key="reg_nombre")
            pw  = st.text_input("🔒  Contraseña", type="password",
                                placeholder="Mínimo 4 caracteres", key="reg_pw")
            pw2 = st.text_input("🔒  Confirmar contraseña", type="password",
                                placeholder="Repite la contraseña", key="reg_pw2")
            sub = st.form_submit_button("SIGUIENTE → AGREGAR ESTUDIANTES",
                                        use_container_width=True)

        if sub:
            nombre_v = st.session_state.get("reg_nombre", "").strip()
            pw_v     = st.session_state.get("reg_pw", "")
            pw2_v    = st.session_state.get("reg_pw2", "")

            if not nombre_v:
                st.session_state["_reg_error"] = "⚠️ El nombre es requerido."
                st.rerun()
            elif len(pw_v) < 4:
                st.session_state["_reg_error"] = "⚠️ Mínimo 4 caracteres."
                st.rerun()
            elif pw_v != pw2_v:
                st.session_state["_reg_error"] = "⚠️ Las contraseñas no coinciden."
                st.rerun()
            else:
                # ── Registrar grupo en database.py → database.db ──────────────
                ok, gid = registrar_grupo(nombre_v, pw_v)
                if ok:
                    st.session_state["grupo_id_registro"] = gid
                    st.session_state["grupo_nombre"]      = nombre_v
                    st.session_state["estudiantes_temp"]  = []
                    st.rerun()
                else:
                    st.session_state["_reg_error"] = "❌ Ese nombre ya existe. Elige otro."
                    st.rerun()

    # ══ PASO 2: Agregar estudiantes ═══════════════════════════════════════════
    else:
        nombre_grp = st.session_state.get("grupo_nombre", "")

        # Grupo creado
        _exito_card("✅ Grupo <b>" + nombre_grp + "</b> creado")

        # Barra de progreso del equipo
        prog_pct = int(len(estudiantes) / MAX_EST * 100)
        prog_col = "#34d399" if len(estudiantes) >= MIN_EST else "#f59e0b"
        st.markdown(
            "<div style='background:rgba(255,255,255,.03);"
            "border:1px solid rgba(255,255,255,.06);"
            "border-radius:9px;padding:9px 13px;margin-bottom:12px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
            "<span style='font-family:Rajdhani,sans-serif;font-size:.70rem;"
            "color:rgba(255,255,255,.35)'>👥 Equipo</span>"
            "<span style='font-family:Courier Prime,monospace;font-size:.70rem;"
            "color:" + prog_col + ";font-weight:700'>"
            + str(len(estudiantes)) + "/" + str(MAX_EST) + " estudiantes</span></div>"
            "<div style='background:rgba(255,255,255,.06);border-radius:3px;height:5px'>"
            "<div style='width:" + str(prog_pct) + "%;height:5px;border-radius:3px;"
            "background:" + prog_col + ";transition:width .4s ease'></div></div></div>",
            unsafe_allow_html=True)

        # Lista de estudiantes
        if estudiantes:
            lista_html = "".join(
                "<div style='display:flex;align-items:center;gap:8px;"
                "background:rgba(167,139,250,.06);"
                "border:1px solid rgba(167,139,250,.15);"
                "border-radius:8px;padding:6px 11px;margin-bottom:4px'>"
                "<span style='color:#a78bfa;font-size:.82rem'>👤</span>"
                "<span style='font-family:Rajdhani,sans-serif;font-size:.84rem;"
                "color:#c4b5fd;font-weight:600'>" + e + "</span>"
                "<span style='margin-left:auto;color:#34d399;font-size:.72rem'>✓</span>"
                "</div>"
                for e in estudiantes)
            st.markdown(lista_html, unsafe_allow_html=True)
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Formulario agregar estudiante
        if len(estudiantes) < MAX_EST:
            with st.form("form_est", clear_on_submit=True):
                est_nombre = st.text_input(
                    "👤  Estudiante #" + str(len(estudiantes) + 1),
                    placeholder="Nombre completo",
                    key="est_nombre_input")
                add = st.form_submit_button("➕  AGREGAR ESTUDIANTE",
                                            use_container_width=True)
            if add:
                est_v = st.session_state.get("est_nombre_input", "").strip()
                if not re.fullmatch(REGEX_NOMBRE, est_v):
                    st.session_state["_reg_error"] = "⚠️ Solo letras y espacios."
                    st.rerun()
                elif est_v in estudiantes:
                    st.session_state["_reg_error"] = "⚠️ Nombre ya agregado."
                    st.rerun()
                else:
                    # ── Guardar estudiante en database.py → database.db ───────
                    guardar_estudiante(gid_reg, est_v)
                    st.session_state["estudiantes_temp"].append(est_v)
                    st.rerun()
        else:
            st.markdown(
                "<div style='background:rgba(52,211,153,.06);"
                "border:1px solid rgba(52,211,153,.18);"
                "border-radius:9px;padding:8px 12px;margin-bottom:8px;"
                "font-family:Rajdhani,sans-serif;font-size:.80rem;"
                "color:#6ee7b7;text-align:center'>✅ Equipo completo ("
                + str(MAX_EST) + "/" + str(MAX_EST) + ")</div>",
                unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if len(estudiantes) >= MIN_EST:
            # ── Ir al lobby ───────────────────────────────────────────────────
            st.markdown('<div class="auth-primary">', unsafe_allow_html=True)
            if st.button("🚀  IR AL LOBBY (" + str(len(estudiantes)) + " estudiantes)",
                         use_container_width=True, key="btn_ir_lobby"):
                st.session_state["grupo_id"]          = gid_reg
                st.session_state["grupo_id_registro"] = None
                st.session_state["estudiantes_temp"]  = []
                navegar("lobby")            # → router → pantalla_lobby()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            faltantes = MIN_EST - len(estudiantes)
            st.markdown(
                "<div style='background:rgba(245,158,11,.06);"
                "border:1px solid rgba(245,158,11,.18);"
                "border-radius:9px;padding:8px 12px;margin-bottom:8px;"
                "font-family:Rajdhani,sans-serif;font-size:.80rem;"
                "color:#fbbf24;text-align:center'>📋 Agrega "
                + str(faltantes) + " más (mínimo " + str(MIN_EST) + ")</div>",
                unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="auth-back">', unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL INICIO", use_container_width=True, key="btn_back_reg"):
        st.session_state["grupo_id_registro"] = None
        st.session_state["estudiantes_temp"]  = []
        navegar("inicio")
    st.markdown('</div>', unsafe_allow_html=True)

    _card_cerrado()
