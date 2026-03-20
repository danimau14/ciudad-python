import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import hashlib
import re
from session_manager import navegar
from db import get_connection

def _cx():
    return get_connection()

def _hp(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

MIN_EST = 3
MAX_EST = 5
REGEX_NOMBRE = r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&family=Courier+Prime:wght@400;700&display=swap');
#MainMenu,footer,header,[data-testid="stToolbar"],.stDeployButton{display:none!important}
html,body,[data-testid="stAppViewContainer"],[data-testid="stAppViewBlockContainer"],.main,.block-container{background:#07001a!important;padding:0!important;margin:0 auto!important;max-width:100%!important;min-height:100vh!important}
.block-container{display:flex!important;flex-direction:column!important;align-items:center!important;justify-content:center!important;min-height:100vh!important;padding:24px 16px!important;max-width:min(500px,96vw)!important}
.stTextInput label{font-family:'Rajdhani',sans-serif!important;font-size:.76rem!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:2px!important;color:rgba(167,139,250,.65)!important}
.stTextInput>div>div>input{background:rgba(255,255,255,.04)!important;border:1px solid rgba(123,47,255,.28)!important;border-radius:10px!important;color:#e2e8f0!important;font-family:'Courier Prime',monospace!important;font-size:.90rem!important;padding:10px 14px!important}
.stFormSubmitButton button{font-family:'Rajdhani',sans-serif!important;font-size:.93rem!important;font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;color:#fff!important;border:none!important;border-radius:12px!important;padding:12px!important;box-shadow:0 4px 20px rgba(124,58,237,.40)!important;width:100%!important}
.auth-back .stButton button{font-family:'Rajdhani',sans-serif!important;font-size:.78rem!important;background:transparent!important;color:rgba(148,163,184,.55)!important;border:1px solid rgba(255,255,255,.07)!important;border-radius:10px!important;padding:8px!important;width:100%!important}
.auth-primary .stButton button{font-family:'Rajdhani',sans-serif!important;font-size:.90rem!important;font-weight:700!important;background:linear-gradient(135deg,#7c3aed,#4f46e5)!important;color:#fff!important;border:none!important;border-radius:12px!important;padding:11px!important;box-shadow:0 4px 18px rgba(124,58,237,.38)!important;width:100%!important}
</style>
"""

def _card_open(color_top, nebula_col):
    st.markdown(
        "<div style='position:fixed;inset:0;z-index:0;pointer-events:none;"
        "background:radial-gradient(ellipse 65% 50% at 18% 28%," + nebula_col + " 0%,transparent 55%),"
        "radial-gradient(ellipse 50% 58% at 82% 72%,rgba(79,70,229,.16) 0%,transparent 55%)'></div>"
        "<div style='position:relative;z-index:1;width:100%;background:rgba(10,3,30,.93);"
        "border:1px solid rgba(123,47,255,.38);border-top:2px solid " + color_top + ";"
        "border-radius:20px;overflow:hidden;"
        "box-shadow:0 0 60px rgba(123,47,255,.14),0 24px 48px rgba(0,0,0,.5);"
        "animation:fadein .6s ease both'>"
        "<style>@keyframes fadein{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}</style>"
        "<div style='position:absolute;top:0;left:0;right:0;height:2px;overflow:hidden'>"
        "<div style='height:2px;background:linear-gradient(90deg,transparent," + color_top + ",transparent);"
        "animation:sweep 2.5s linear infinite'></div></div>"
        "<style>@keyframes sweep{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}</style>"
        "<div style='padding:24px 24px 20px'>",
        unsafe_allow_html=True)

def _header_card(emoji, titulo, subtitulo):
    st.markdown(
        "<div style='text-align:center;margin-bottom:18px'>"
        "<div style='font-size:2.8rem;margin-bottom:10px;"
        "filter:drop-shadow(0 0 18px rgba(123,47,255,.75))'>" + emoji + "</div>"
        "<div style='font-family:Press Start 2P,monospace;font-size:clamp(.60rem,2.3vw,.84rem);"
        "background:linear-gradient(90deg,#c4b5fd,#818cf8,#60a5fa);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "letter-spacing:2px;line-height:1.6;margin-bottom:5px'>" + titulo + "</div>"
        "<div style='font-family:Rajdhani,sans-serif;font-size:.70rem;"
        "color:rgba(167,139,250,.42);letter-spacing:3px;text-transform:uppercase'>"
        + subtitulo + "</div></div>"
        "<div style='height:1px;background:linear-gradient(90deg,transparent,"
        "rgba(123,47,255,.4),rgba(99,102,241,.4),transparent);margin-bottom:18px'></div>",
        unsafe_allow_html=True)

def _err(msg):
    st.markdown(
        "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.28);"
        "border-radius:9px;padding:9px 13px;margin-top:8px;"
        "font-family:Rajdhani,sans-serif;font-size:.82rem;color:#fca5a5;text-align:center'>"
        + msg + "</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_login():
    st.markdown(_CSS, unsafe_allow_html=True)
    _card_open("rgba(167,139,250,.65)", "rgba(123,47,255,.20)")
    _header_card("🔐", "INICIAR SESIÓN", "Accede a tu ciudad")

    err = st.session_state.pop("_login_err", None)
    if err:
        _err(err)

    with st.form("form_login", clear_on_submit=False):
        st.text_input("👥  Nombre del grupo", placeholder="Nombre de tu equipo", key="li_nombre")
        st.text_input("🔒  Contraseña", type="password", placeholder="••••••••", key="li_pw")
        sub = st.form_submit_button("🚀  ENTRAR AL JUEGO", use_container_width=True)

    if sub:
        nombre = st.session_state.get("li_nombre", "").strip()
        pw     = st.session_state.get("li_pw", "")
        if not nombre:
            st.session_state["_login_err"] = "⚠️ Ingresa el nombre del grupo."
            st.rerun()
        elif not pw:
            st.session_state["_login_err"] = "⚠️ Ingresa la contraseña."
            st.rerun()
        else:
            # Consulta directa a database.db
            c = _cx(); cur = c.cursor()
            cur.execute("SELECT id FROM grupos WHERE nombregrupo=? AND password=?",
                        (nombre, _hp(pw)))
            row = cur.fetchone(); c.close()
            if row:
                st.session_state["grupo_id"]     = row["id"]
                st.session_state["grupo_nombre"] = nombre
                navegar("lobby")
            else:
                st.session_state["_login_err"] = "❌ Nombre o contraseña incorrectos."
                st.rerun()

    st.markdown("<div style='height:1px;background:rgba(255,255,255,.05);margin:14px 0'></div>",
                unsafe_allow_html=True)
    st.markdown('<div class="auth-back">', unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL INICIO", use_container_width=True, key="btn_back_login"):
        navegar("inicio")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  REGISTRO
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_registro():
    st.markdown(_CSS, unsafe_allow_html=True)
    gid_reg     = st.session_state.get("grupo_id_registro")
    estudiantes = st.session_state.get("estudiantes_temp", [])
    paso        = 2 if gid_reg else 1

    color_top = "rgba(52,211,153,.55)" if paso == 2 else "rgba(167,139,250,.60)"
    _card_open(color_top, "rgba(52,211,153,.14)")

    emoji_h = "👥" if paso == 2 else "📝"
    _header_card(emoji_h, "REGISTRAR GRUPO", "Crea tu equipo de control")

    err = st.session_state.pop("_reg_err", None)
    if err:
        _err(err)

    # ── PASO 1: Crear grupo ───────────────────────────────────────────────────
    if not gid_reg:
        with st.form("form_reg", clear_on_submit=False):
            st.text_input("👥  Nombre del grupo", placeholder="Ej: Equipo Titán", key="reg_nombre")
            st.text_input("🔒  Contraseña", type="password", placeholder="Mínimo 4 caracteres", key="reg_pw")
            st.text_input("🔒  Confirmar contraseña", type="password", key="reg_pw2")
            sub = st.form_submit_button("SIGUIENTE → AGREGAR ESTUDIANTES", use_container_width=True)

        if sub:
            nombre = st.session_state.get("reg_nombre", "").strip()
            pw     = st.session_state.get("reg_pw", "")
            pw2    = st.session_state.get("reg_pw2", "")
            if not nombre:
                st.session_state["_reg_err"] = "⚠️ El nombre es requerido."
                st.rerun()
            elif len(pw) < 4:
                st.session_state["_reg_err"] = "⚠️ Mínimo 4 caracteres."
                st.rerun()
            elif pw != pw2:
                st.session_state["_reg_err"] = "⚠️ Las contraseñas no coinciden."
                st.rerun()
            else:
                # Insertar grupo en database.db
                c = _cx(); cur = c.cursor()
                try:
                    cur.execute("INSERT INTO grupos(nombregrupo,password) VALUES(?,?)",
                                (nombre, _hp(pw)))
                    c.commit(); gid = cur.lastrowid; c.close()
                    st.session_state["grupo_id_registro"] = gid
                    st.session_state["grupo_nombre"]      = nombre
                    st.session_state["estudiantes_temp"]  = []
                    st.rerun()
                except sqlite3.IntegrityError:
                    c.close()
                    st.session_state["_reg_err"] = "❌ Ese nombre ya existe."
                    st.rerun()

    # ── PASO 2: Agregar estudiantes ───────────────────────────────────────────
    else:
        nombre_grp = st.session_state.get("grupo_nombre", "")
        prog_pct   = int(len(estudiantes) / MAX_EST * 100)
        prog_col   = "#34d399" if len(estudiantes) >= MIN_EST else "#f59e0b"

        st.markdown(
            "<div style='background:rgba(52,211,153,.07);border:1px solid rgba(52,211,153,.25);"
            "border-radius:9px;padding:9px 13px;margin-bottom:10px;"
            "font-family:Rajdhani,sans-serif;font-size:.82rem;color:#6ee7b7;text-align:center'>"
            "✅ Grupo <b>" + nombre_grp + "</b> creado correctamente</div>",
            unsafe_allow_html=True)

        st.markdown(
            "<div style='background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);"
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

        if estudiantes:
            lista = "".join(
                "<div style='display:flex;align-items:center;gap:8px;"
                "background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.15);"
                "border-radius:8px;padding:6px 11px;margin-bottom:4px'>"
                "<span style='color:#a78bfa'>👤</span>"
                "<span style='font-family:Rajdhani,sans-serif;font-size:.84rem;"
                "color:#c4b5fd;font-weight:600'>" + e + "</span>"
                "<span style='margin-left:auto;color:#34d399;font-size:.72rem'>✓</span></div>"
                for e in estudiantes)
            st.markdown(lista, unsafe_allow_html=True)

        if len(estudiantes) < MAX_EST:
            with st.form("form_est", clear_on_submit=True):
                st.text_input("👤  Estudiante #" + str(len(estudiantes) + 1),
                              placeholder="Nombre completo", key="est_input")
                add = st.form_submit_button("➕  AGREGAR ESTUDIANTE", use_container_width=True)
            if add:
                ev = st.session_state.get("est_input", "").strip()
                if not re.fullmatch(REGEX_NOMBRE, ev):
                    st.session_state["_reg_err"] = "⚠️ Solo letras y espacios."
                    st.rerun()
                elif ev in estudiantes:
                    st.session_state["_reg_err"] = "⚠️ Nombre ya agregado."
                    st.rerun()
                else:
                    # Guardar estudiante en database.db
                    c = _cx()
                    c.execute("INSERT INTO estudiantes(grupoid,nombreestudiante) VALUES(?,?)",
                              (gid_reg, ev))
                    c.commit(); c.close()
                    st.session_state["estudiantes_temp"].append(ev)
                    st.rerun()

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if len(estudiantes) >= MIN_EST:
            st.markdown('<div class="auth-primary">', unsafe_allow_html=True)
            if st.button("🚀  IR AL LOBBY (" + str(len(estudiantes)) + " estudiantes)",
                         use_container_width=True, key="btn_lobby"):
                st.session_state["grupo_id"]          = gid_reg
                st.session_state["grupo_id_registro"] = None
                st.session_state["estudiantes_temp"]  = []
                navegar("lobby")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.18);"
                "border-radius:9px;padding:8px 12px;margin-bottom:8px;"
                "font-family:Rajdhani,sans-serif;font-size:.80rem;color:#fbbf24;text-align:center'>"
                "📋 Agrega " + str(MIN_EST - len(estudiantes)) + " más (mínimo " + str(MIN_EST) + ")</div>",
                unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="auth-back">', unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL INICIO", use_container_width=True, key="btn_back_reg"):
        st.session_state["grupo_id_registro"] = None
        st.session_state["estudiantes_temp"]  = []
        navegar("inicio")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
