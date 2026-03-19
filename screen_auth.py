import streamlit as st
from session_manager import navegar
import re

REGEX_NOMBRE = r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+"
MIN_EST = 3
MAX_EST = 5

# ── CSS compartido para login y registro ──────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&family=Courier+Prime:wght@400;700&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main, .block-container {
    background: #07001a !important;
    padding: 0 !important; margin: 0 auto !important;
    max-width: 100% !important; min-height: 100vh !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

/* Centrado vertical */
.block-container {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 100vh !important;
    padding: 24px 16px !important;
    max-width: min(520px, 96vw) !important;
}

/* ── Inputs ── */
.stTextInput label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 2px !important;
    color: rgba(167,139,250,.7) !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,.04) !important;
    border: 1px solid rgba(123,47,255,.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Courier Prime', monospace !important;
    font-size: .92rem !important;
    padding: 10px 14px !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(167,139,250,.7) !important;
    box-shadow: 0 0 0 3px rgba(123,47,255,.15) !important;
}

/* ── Botón primario ── */
.auth-primary .stButton button {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .95rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg,#7c3aed,#4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,.45) !important;
    transition: all .22s ease !important;
    width: 100% !important;
}
.auth-primary .stButton button:hover {
    background: linear-gradient(135deg,#8b5cf6,#6366f1) !important;
    box-shadow: 0 6px 32px rgba(124,58,237,.65) !important;
    transform: translateY(-2px) !important;
}

/* ── Botón secundario ── */
.auth-back .stButton button {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .82rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    background: transparent !important;
    color: rgba(148,163,184,.6) !important;
    border: 1px solid rgba(255,255,255,.08) !important;
    border-radius: 10px !important;
    padding: 8px !important;
    transition: all .2s !important;
    width: 100% !important;
}
.auth-back .stButton button:hover {
    color: #c4b5fd !important;
    border-color: rgba(167,139,250,.35) !important;
    background: rgba(167,139,250,.06) !important;
}

/* ── Form submit ── */
.stFormSubmitButton button {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: .95rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg,#7c3aed,#4f46e5) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,.4) !important;
    transition: all .22s ease !important;
    width: 100% !important;
}
.stFormSubmitButton button:hover {
    background: linear-gradient(135deg,#8b5cf6,#6366f1) !important;
    box-shadow: 0 6px 32px rgba(124,58,237,.60) !important;
    transform: translateY(-2px) !important;
}
</style>
"""


def _card_header(titulo, subtitulo, emoji):
    """Header del card con gradiente y animación."""
    return (
        "<div style='text-align:center;padding:28px 24px 20px'>"
        "<div style='font-size:3rem;margin-bottom:12px;"
        "filter:drop-shadow(0 0 20px rgba(123,47,255,.8))'>" + emoji + "</div>"
        "<div style='font-family:Press Start 2P,monospace;"
        "font-size:clamp(.65rem,2.5vw,.88rem);"
        "background:linear-gradient(90deg,#c4b5fd,#818cf8,#60a5fa);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "letter-spacing:2px;line-height:1.6;margin-bottom:6px'>"
        + titulo + "</div>"
        "<div style='font-family:Rajdhani,sans-serif;font-size:.72rem;"
        "color:rgba(167,139,250,.45);letter-spacing:3px;text-transform:uppercase'>"
        + subtitulo + "</div>"
        "</div>"
    )


def _sep():
    return "<div style='height:1px;background:linear-gradient(90deg,transparent,rgba(123,47,255,.4),rgba(99,102,241,.4),transparent);margin:0 20px'></div>"


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_login():
    st.markdown(_CSS, unsafe_allow_html=True)

    # Fondo animado con estrellas (iframe 0px)
    import streamlit.components.v1 as components
    components.html("""
    <style>body{margin:0;background:transparent;overflow:hidden}</style>
    <canvas id="c" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0"></canvas>
    <script>
    var c=document.getElementById('c'),cx=c.getContext('2d');
    function rs(){c.width=window.innerWidth;c.height=window.innerHeight}rs();
    var S=[];for(var i=0;i<120;i++)S.push({x:Math.random()*c.width,y:Math.random()*c.height,
    r:Math.random()*1.2+.2,a:Math.random()*.6+.1,da:(Math.random()*.008+.002)*(Math.random()<.5?1:-1),
    dx:(Math.random()-.5)*.15,dy:(Math.random()-.5)*.1,
    col:['#fff','#c4b5fd','#a78bfa','#818cf8'][Math.floor(Math.random()*4)]});
    function draw(){cx.clearRect(0,0,c.width,c.height);
    S.forEach(function(s){s.x+=s.dx;s.y+=s.dy;s.a+=s.da;
    if(s.a>.85||s.a<.05)s.da*=-1;
    if(s.x<0)s.x=c.width;if(s.x>c.width)s.x=0;
    if(s.y<0)s.y=c.height;if(s.y>c.height)s.y=0;
    cx.save();cx.globalAlpha=s.a;cx.beginPath();cx.arc(s.x,s.y,s.r,0,Math.PI*2);
    cx.fillStyle=s.col;cx.shadowColor=s.col;cx.shadowBlur=s.r*5;cx.fill();cx.restore();});
    requestAnimationFrame(draw);}draw();window.addEventListener('resize',rs);
    </script>
    """, height=0, scrolling=False)

    # Card principal
    st.markdown(
        # Nebulosa de fondo
        "<div style='position:fixed;inset:0;z-index:0;pointer-events:none;"
        "background:radial-gradient(ellipse 60% 50% at 20% 30%,rgba(123,47,255,.22) 0%,transparent 55%),"
        "radial-gradient(ellipse 50% 60% at 80% 70%,rgba(79,70,229,.18) 0%,transparent 55%)'></div>"

        # Card
        "<div style='position:relative;z-index:1;width:100%;"
        "background:rgba(12,4,36,.92);"
        "border:1px solid rgba(123,47,255,.4);"
        "border-top:2px solid rgba(167,139,250,.6);"
        "border-radius:20px;overflow:hidden;"
        "box-shadow:0 0 60px rgba(123,47,255,.18),0 24px 48px rgba(0,0,0,.5);"
        "animation:fadein .6s ease both'>"

        "<style>@keyframes fadein{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}</style>"

        # Línea de energía animada
        "<div style='position:absolute;top:0;left:0;right:0;height:2px;overflow:hidden'>"
        "<div style='height:2px;background:linear-gradient(90deg,transparent,#7b2fff,#a78bfa,#60a5fa,transparent);"
        "animation:eline 2.5s linear infinite'></div></div>"
        "<style>@keyframes eline{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}</style>"

        + _card_header("INICIAR SESIÓN", "Accede a tu ciudad", "🔐")
        + _sep() +

        "<div style='padding:20px 24px 24px'>",
        unsafe_allow_html=True)

    with st.form("form_login"):
        st.text_input("👥  Nombre del grupo", placeholder="Nombre de tu equipo", key="li_nombre")
        st.text_input("🔒  Contraseña", type="password", placeholder="••••••••", key="li_pw")
        sub = st.form_submit_button("🚀  ENTRAR AL JUEGO", use_container_width=True)

    if sub:
        from database import login_grupo
        nombre = st.session_state.get("li_nombre", "")
        pw     = st.session_state.get("li_pw", "")
        gid    = login_grupo(nombre, pw)
        if gid:
            st.session_state["grupo_id"]     = gid
            st.session_state["grupo_nombre"] = nombre
            navegar("lobby")
        else:
            st.markdown(
                "<div style='background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);"
                "border-radius:10px;padding:10px 14px;margin-top:8px;"
                "font-family:Rajdhani,sans-serif;font-size:.84rem;color:#fca5a5;text-align:center'>"
                "❌ Nombre o contraseña incorrectos</div>",
                unsafe_allow_html=True)

    # Separador con "o"
    st.markdown(
        "<div style='display:flex;align-items:center;gap:12px;margin:16px 0'>"
        "<div style='flex:1;height:1px;background:rgba(255,255,255,.06)'></div>"
        "<span style='font-family:Rajdhani,sans-serif;font-size:.72rem;"
        "color:rgba(255,255,255,.2);letter-spacing:2px'>¿No tienes cuenta?</span>"
        "<div style='flex:1;height:1px;background:rgba(255,255,255,.06)'></div>"
        "</div>",
        unsafe_allow_html=True)

    st.markdown('<div class="auth-back">', unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL INICIO", use_container_width=True):
        navegar("inicio")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA REGISTRO (función requerida por screen_auth.py)
#  La lógica real está en screen_registro.py — esta es la versión integrada
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_registro():
    from database import registrar_grupo, guardar_estudiante
    from config import MIN_EST, MAX_EST

    st.markdown(_CSS, unsafe_allow_html=True)

    import streamlit.components.v1 as components
    components.html("""
    <style>body{margin:0;background:transparent;overflow:hidden}</style>
    <canvas id="c" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:0"></canvas>
    <script>
    var c=document.getElementById('c'),cx=c.getContext('2d');
    function rs(){c.width=window.innerWidth;c.height=window.innerHeight}rs();
    var S=[];for(var i=0;i<120;i++)S.push({x:Math.random()*c.width,y:Math.random()*c.height,
    r:Math.random()*1.2+.2,a:Math.random()*.6+.1,da:(Math.random()*.008+.002)*(Math.random()<.5?1:-1),
    dx:(Math.random()-.5)*.15,dy:(Math.random()-.5)*.1,
    col:['#fff','#c4b5fd','#a78bfa','#34d399'][Math.floor(Math.random()*4)]});
    function draw(){cx.clearRect(0,0,c.width,c.height);
    S.forEach(function(s){s.x+=s.dx;s.y+=s.dy;s.a+=s.da;
    if(s.a>.85||s.a<.05)s.da*=-1;
    if(s.x<0)s.x=c.width;if(s.x>c.width)s.x=0;
    if(s.y<0)s.y=c.height;if(s.y>c.height)s.y=0;
    cx.save();cx.globalAlpha=s.a;cx.beginPath();cx.arc(s.x,s.y,s.r,0,Math.PI*2);
    cx.fillStyle=s.col;cx.shadowColor=s.col;cx.shadowBlur=s.r*5;cx.fill();cx.restore();});
    requestAnimationFrame(draw);}draw();window.addEventListener('resize',rs);
    </script>
    """, height=0, scrolling=False)

    gid_reg     = st.session_state.get("grupo_id_registro")
    estudiantes = st.session_state.get("estudiantes_temp", [])
    paso        = 2 if gid_reg else 1

    # Barra de pasos
    def _paso_bar(paso_actual):
        pasos = ["Datos del grupo", "Agregar estudiantes", "¡Listo!"]
        items = ""
        for i, p in enumerate(pasos):
            n      = i + 1
            active = (n == paso_actual)
            done   = (n < paso_actual)
            bg_c   = "#7c3aed" if done else ("#a78bfa" if active else "rgba(255,255,255,.08)")
            col_c  = "#fff"    if (done or active) else "rgba(255,255,255,.2)"
            brd_c  = "#7c3aed" if done else ("#a78bfa" if active else "rgba(255,255,255,.1)")
            txt_c  = "#c4b5fd" if active else ("#6ee7b7" if done else "rgba(255,255,255,.2)")
            symbol = "✓" if done else str(n)
            items += (
                "<div style='display:flex;flex-direction:column;align-items:center;flex:1'>"
                "<div style='width:28px;height:28px;border-radius:50%;"
                "background:" + bg_c + ";border:1.5px solid " + brd_c + ";"
                "display:flex;align-items:center;justify-content:center;"
                "font-size:.72rem;font-weight:700;color:" + col_c + ";margin-bottom:4px'>"
                + symbol + "</div>"
                "<div style='font-family:Rajdhani,sans-serif;font-size:.60rem;"
                "text-transform:uppercase;letter-spacing:1px;color:" + txt_c + ";text-align:center'>"
                + p + "</div></div>")
            if i < len(pasos) - 1:
                line_col = "#7c3aed" if n < paso_actual else "rgba(255,255,255,.08)"
                items += (
                    "<div style='flex:1;height:1.5px;background:" + line_col + ";"
                    "margin:14px 4px 0;align-self:flex-start'></div>")
        return (
            "<div style='display:flex;align-items:flex-start;gap:0;"
            "padding:16px 20px 14px'>" + items + "</div>")

    # Header card
    titulo    = "REGISTRAR GRUPO"
    subtitulo = "Crea tu equipo de control"
    emoji_h   = "📝" if paso == 1 else "👥"

    st.markdown(
        "<div style='position:fixed;inset:0;z-index:0;pointer-events:none;"
        "background:radial-gradient(ellipse 60% 50% at 20% 30%,rgba(52,211,153,.15) 0%,transparent 55%),"
        "radial-gradient(ellipse 50% 60% at 80% 70%,rgba(124,58,237,.18) 0%,transparent 55%)'></div>"

        "<div style='position:relative;z-index:1;width:100%;"
        "background:rgba(12,4,36,.92);"
        "border:1px solid rgba(123,47,255,.38);"
        "border-top:2px solid rgba(52,211,153,.5);"
        "border-radius:20px;overflow:hidden;"
        "box-shadow:0 0 60px rgba(52,211,153,.12),0 24px 48px rgba(0,0,0,.5);"
        "animation:fadein .6s ease both'>"
        "<style>@keyframes fadein{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}</style>"

        "<div style='position:absolute;top:0;left:0;right:0;height:2px;overflow:hidden'>"
        "<div style='height:2px;background:linear-gradient(90deg,transparent,#34d399,#a78bfa,transparent);"
        "animation:eline 2.5s linear infinite'></div></div>"
        "<style>@keyframes eline{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}</style>"

        + _card_header(titulo, subtitulo, emoji_h)
        + _sep()
        + _paso_bar(paso)
        + _sep() +

        "<div style='padding:16px 24px 22px'>",
        unsafe_allow_html=True)

    # ── PASO 1: Datos del grupo ───────────────────────────────────────────────
    if not gid_reg:
        # Info del proceso
        st.markdown(
            "<div style='background:rgba(52,211,153,.05);"
            "border:1px solid rgba(52,211,153,.18);"
            "border-radius:10px;padding:10px 14px;margin-bottom:14px'>"
            "<div style='font-family:Rajdhani,sans-serif;font-size:.78rem;"
            "color:rgba(52,211,153,.7);line-height:1.7'>"
            "1️⃣ Nombre y contraseña del grupo &nbsp;→&nbsp; "
            "2️⃣ Agrega <b style='color:#34d399'>" + str(MIN_EST) + "–" + str(MAX_EST) + "</b>"
            " estudiantes &nbsp;→&nbsp; 3️⃣ ¡A jugar!"
            "</div></div>",
            unsafe_allow_html=True)

        with st.form("form_registro"):
            nombre = st.text_input(
                "👥  Nombre del grupo",
                placeholder="Ej: Equipo Titán",
                value=st.session_state.get("reg_nombre_temp", ""))
            pw  = st.text_input("🔒  Contraseña", type="password", placeholder="Mínimo 4 caracteres")
            pw2 = st.text_input("🔒  Confirmar contraseña", type="password", placeholder="Repite la contraseña")
            sub = st.form_submit_button("SIGUIENTE → AGREGAR ESTUDIANTES", use_container_width=True)

        if sub:
            nombre = nombre.strip()
            if not nombre:
                st.markdown(
                    "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.25);"
                    "border-radius:9px;padding:9px 13px;font-family:Rajdhani,sans-serif;"
                    "font-size:.83rem;color:#fca5a5;margin-top:6px'>⚠️ El nombre del grupo es requerido.</div>",
                    unsafe_allow_html=True)
            elif len(pw) < 4:
                st.markdown(
                    "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.25);"
                    "border-radius:9px;padding:9px 13px;font-family:Rajdhani,sans-serif;"
                    "font-size:.83rem;color:#fca5a5;margin-top:6px'>⚠️ Mínimo 4 caracteres.</div>",
                    unsafe_allow_html=True)
            elif pw != pw2:
                st.markdown(
                    "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.25);"
                    "border-radius:9px;padding:9px 13px;font-family:Rajdhani,sans-serif;"
                    "font-size:.83rem;color:#fca5a5;margin-top:6px'>⚠️ Las contraseñas no coinciden.</div>",
                    unsafe_allow_html=True)
            else:
                ok, gid = registrar_grupo(nombre, pw)
                if ok:
                    st.session_state["grupo_id_registro"] = gid
                    st.session_state["grupo_nombre"]      = nombre
                    st.session_state["estudiantes_temp"]  = []
                    st.rerun()
                else:
                    st.markdown(
                        "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.25);"
                        "border-radius:9px;padding:9px 13px;font-family:Rajdhani,sans-serif;"
                        "font-size:.83rem;color:#fca5a5;margin-top:6px'>❌ Ese nombre ya existe.</div>",
                        unsafe_allow_html=True)

    # ── PASO 2: Agregar estudiantes ───────────────────────────────────────────
    else:
        nombre_grp = st.session_state.get("grupo_nombre", "")

        # Banner del grupo creado
        st.markdown(
            "<div style='background:rgba(52,211,153,.07);"
            "border:1px solid rgba(52,211,153,.25);"
            "border-radius:10px;padding:10px 14px;margin-bottom:14px;"
            "display:flex;align-items:center;gap:10px'>"
            "<span style='font-size:1.3rem'>🏙️</span>"
            "<div><div style='font-family:Rajdhani,sans-serif;font-weight:700;"
            "color:#34d399;font-size:.9rem'>" + nombre_grp + "</div>"
            "<div style='font-family:Courier Prime,monospace;font-size:.62rem;"
            "color:rgba(52,211,153,.5)'>Grupo creado correctamente ✓</div></div>"
            "</div>",
            unsafe_allow_html=True)

        # Progreso de estudiantes
        prog_pct = int(len(estudiantes) / MAX_EST * 100)
        prog_col = "#34d399" if len(estudiantes) >= MIN_EST else "#f59e0b"
        st.markdown(
            "<div style='background:rgba(255,255,255,.03);"
            "border:1px solid rgba(255,255,255,.07);"
            "border-radius:10px;padding:10px 14px;margin-bottom:12px'>"
            "<div style='display:flex;justify-content:space-between;"
            "margin-bottom:6px'>"
            "<span style='font-family:Rajdhani,sans-serif;font-size:.72rem;"
            "color:rgba(255,255,255,.4)'>👥 Equipo</span>"
            "<span style='font-family:Courier Prime,monospace;font-size:.72rem;"
            "color:" + prog_col + ";font-weight:700'>"
            + str(len(estudiantes)) + "/" + str(MAX_EST) + " estudiantes</span></div>"
            "<div style='background:rgba(255,255,255,.06);border-radius:4px;height:6px'>"
            "<div style='width:" + str(prog_pct) + "%;height:6px;border-radius:4px;"
            "background:" + prog_col + ";transition:width .4s ease'></div></div>"
            "</div>",
            unsafe_allow_html=True)

        # Lista de estudiantes
        if estudiantes:
            chips = "".join(
                "<div style='display:flex;align-items:center;gap:8px;"
                "background:rgba(167,139,250,.07);"
                "border:1px solid rgba(167,139,250,.18);"
                "border-radius:8px;padding:7px 12px;margin-bottom:5px'>"
                "<span style='color:#a78bfa;font-size:.85rem'>👤</span>"
                "<span style='font-family:Rajdhani,sans-serif;font-size:.86rem;"
                "color:#c4b5fd;font-weight:600'>" + e + "</span>"
                "<span style='margin-left:auto;color:#34d399;font-size:.75rem'>✓</span>"
                "</div>"
                for e in estudiantes)
            st.markdown(chips, unsafe_allow_html=True)

        # Formulario agregar estudiante
        if len(estudiantes) < MAX_EST:
            with st.form("form_estudiante"):
                est_nombre = st.text_input(
                    "👤  Estudiante #" + str(len(estudiantes) + 1),
                    placeholder="Nombre completo del estudiante")
                add = st.form_submit_button("➕  AGREGAR ESTUDIANTE", use_container_width=True)

            if add:
                est_nombre = est_nombre.strip()
                if not re.fullmatch(REGEX_NOMBRE, est_nombre):
                    st.markdown(
                        "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.25);"
                        "border-radius:9px;padding:9px 13px;font-family:Rajdhani,sans-serif;"
                        "font-size:.83rem;color:#fca5a5;margin-top:6px'>⚠️ Solo letras y espacios.</div>",
                        unsafe_allow_html=True)
                elif est_nombre in estudiantes:
                    st.markdown(
                        "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.25);"
                        "border-radius:9px;padding:9px 13px;font-family:Rajdhani,sans-serif;"
                        "font-size:.83rem;color:#fca5a5;margin-top:6px'>⚠️ Nombre ya agregado.</div>",
                        unsafe_allow_html=True)
                else:
                    guardar_estudiante(gid_reg, est_nombre)
                    st.session_state["estudiantes_temp"].append(est_nombre)
                    st.rerun()
        else:
            st.markdown(
                "<div style='background:rgba(52,211,153,.06);"
                "border:1px solid rgba(52,211,153,.2);"
                "border-radius:9px;padding:9px 13px;margin-bottom:8px;"
                "font-family:Rajdhani,sans-serif;font-size:.82rem;"
                "color:#6ee7b7;text-align:center'>✅ Equipo completo (" + str(MAX_EST) + "/" + str(MAX_EST) + ")</div>",
                unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if len(estudiantes) >= MIN_EST:
            st.markdown('<div class="auth-primary">', unsafe_allow_html=True)
            if st.button(
                    "🚀  IR AL LOBBY (" + str(len(estudiantes)) + " estudiantes)",
                    use_container_width=True):
                st.session_state["grupo_id"]          = gid_reg
                st.session_state["grupo_id_registro"] = None
                st.session_state["estudiantes_temp"]  = []
                navegar("lobby")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            faltantes = MIN_EST - len(estudiantes)
            st.markdown(
                "<div style='background:rgba(245,158,11,.06);"
                "border:1px solid rgba(245,158,11,.2);"
                "border-radius:9px;padding:9px 13px;margin-bottom:8px;"
                "font-family:Rajdhani,sans-serif;font-size:.82rem;"
                "color:#fbbf24;text-align:center'>"
                "📋 Agrega " + str(faltantes) + " estudiante(s) más (mínimo " + str(MIN_EST) + ")</div>",
                unsafe_allow_html=True)

    # Botón volver
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="auth-back">', unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL INICIO", use_container_width=True, key="btn_volver_reg"):
        st.session_state["grupo_id_registro"] = None
        st.session_state["estudiantes_temp"]  = []
        st.session_state.pop("reg_nombre_temp", None)
        navegar("inicio")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)
