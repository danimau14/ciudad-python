import streamlit as st
import streamlit.components.v1 as components
import datetime
import sqlite3
import os
from session_manager import navegar

_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def _ensure_db_file():
    """Crea database.db si aun no existe."""
    conn = sqlite3.connect(_DB, check_same_thread=False)
    conn.close()


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA DE INICIO
#  Flujo:
#    🔐 INICIAR SESIÓN  → navegar("login")    → pantalla_login()   → navegar("lobby")
#    📝 REGISTRAR GRUPO → navegar("registro") → pantalla_registro() → navegar("lobby")
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_inicio():
    _ensure_db_file()

    # ── CSS: ocultar Streamlit + fondo + panel + botones ─────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap');

    /* Ocultar UI de Streamlit */
    #MainMenu, footer, header,
    [data-testid="stToolbar"],
    .stDeployButton { display: none !important; }

    /* Fondo oscuro */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewBlockContainer"],
    .main, .block-container {
        background: #0d0025 !important;
        padding: 0 !important;
        margin: 0 auto !important;
        max-width: 100% !important;
        min-height: 100vh !important;
    }

    /* Centrar todo verticalmente */
    .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        padding: 20px 12px !important;
        max-width: min(440px, 96vw) !important;
    }

    /* Nebulosa */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed; inset: 0; z-index: 0; pointer-events: none;
        background:
            radial-gradient(ellipse 65% 50% at 15% 25%, rgba(123,47,255,.26) 0%, transparent 58%),
            radial-gradient(ellipse 50% 60% at 85% 75%, rgba(99,102,241,.20) 0%, transparent 58%),
            radial-gradient(ellipse 75% 30% at 50% 105%, rgba(123,47,255,.28) 0%, transparent 52%);
    }

    /* ══ PANEL SUPERIOR (HTML) ══ */
    .ip {
        position: relative; z-index: 1;
        background: rgba(18,4,52,.93);
        border: 1.5px solid rgba(123,47,255,.50);
        border-bottom: none;
        border-radius: 22px 22px 0 0;
        width: 100%;
        text-align: center;
        padding: clamp(22px,5vw,32px) clamp(18px,5vw,28px) clamp(14px,3vw,20px);
        overflow: hidden;
        animation: pglow 4s ease-in-out infinite, fadein .7s ease both;
    }
    @keyframes pglow {
        0%,100% { box-shadow: 0 0 20px #7b2fff44, 0 0 50px #7b2fff18; }
        50%     { box-shadow: 0 0 42px #7b2fff99, 0 0 88px #7b2fff50; }
    }
    @keyframes fadein {
        from { opacity: 0; transform: translateY(22px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    /* Línea de energía */
    .ip::before {
        content: ''; position: absolute; top: 0; left: -100%;
        height: 2px; width: 55%; z-index: 3;
        background: linear-gradient(90deg, transparent, #7b2fff, #FFD700, #00ffff, transparent);
        animation: eline 2.8s linear infinite;
    }
    @keyframes eline { 0% { left:-100%; width:55%; } 100% { left:110%; width:75%; } }

    /* Separador */
    .isep {
        position: relative; z-index: 1;
        height: 2px; width: 100%; margin: 0;
        background: linear-gradient(90deg, transparent 0%, #7b2fff 30%, #FFD700 50%, #7b2fff 70%, transparent 100%);
        opacity: .9;
    }

    /* ══ ZONA DE BOTONES ══ */
    .bzone {
        position: relative; z-index: 1;
        background: rgba(18,4,52,.93);
        border: 1.5px solid rgba(123,47,255,.50);
        border-top: none;
        border-radius: 0 0 22px 22px;
        width: 100%;
        padding: clamp(14px,4vw,20px) clamp(18px,5vw,28px) clamp(18px,5vw,26px);
        animation: pglow 4s ease-in-out infinite;
    }

    /* Helper */
    .ihelper {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.58rem,2vw,.66rem);
        color: rgba(167,139,250,.36);
        letter-spacing: 1.5px; text-transform: uppercase;
        text-align: center; margin-bottom: clamp(10px,3vw,14px);
    }

    /* ── Botón dorado (Iniciar Sesión) ── */
    .btn-login > div > button,
    .btn-login .stButton > button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: clamp(.85rem,3vw,1rem) !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        padding: clamp(10px,2.5vw,13px) 16px !important;
        width: 100% !important;
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #12003e !important;
        border: none !important;
        box-shadow: 0 4px 22px rgba(255,215,0,.42) !important;
        transition: all .22s ease !important;
        margin-bottom: 10px !important;
    }
    .btn-login > div > button:hover,
    .btn-login .stButton > button:hover {
        background: linear-gradient(135deg, #FFE44D, #FFB733) !important;
        box-shadow: 0 6px 36px rgba(255,215,0,.70) !important;
        transform: translateY(-3px) !important;
    }

    /* ── Botón púrpura (Registrar Grupo) ── */
    .btn-registro > div > button,
    .btn-registro .stButton > button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: clamp(.85rem,3vw,1rem) !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        padding: clamp(10px,2.5vw,13px) 16px !important;
        width: 100% !important;
        background: transparent !important;
        color: #c4b5fd !important;
        border: 1.5px solid #7b2fff !important;
        box-shadow: 0 0 13px rgba(123,47,255,.26) !important;
        transition: all .22s ease !important;
    }
    .btn-registro > div > button:hover,
    .btn-registro .stButton > button:hover {
        background: linear-gradient(135deg, rgba(123,47,255,.26), rgba(99,102,241,.20)) !important;
        border-color: #a78bfa !important;
        color: #fff !important;
        box-shadow: 0 0 32px rgba(123,47,255,.62), 0 0 60px rgba(123,47,255,.28) !important;
        transform: translateY(-3px) !important;
    }

    /* Footer */
    .ifooter {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.50rem,1.8vw,.58rem);
        color: rgba(167,139,250,.24);
        letter-spacing: 1.5px; text-transform: uppercase;
        text-align: center; margin-top: clamp(12px,3vw,18px);
    }

    /* Ícono flotante */
    .cicon {
        font-size: clamp(2.2rem,8vw,3rem);
        display: block; margin-bottom: clamp(8px,2vw,12px);
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 18px #7b2fffcc)
                drop-shadow(0 0 40px #7b2fff88)
                drop-shadow(0 0  8px #FFD70055);
    }
    @keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-10px); } }

    /* Badge */
    .ibadge {
        display: inline-block;
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.55rem,1.8vw,.64rem);
        font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
        color: #a78bfa;
        background: rgba(123,47,255,.14);
        border: 1px solid rgba(123,47,255,.36);
        border-radius: 20px; padding: 4px clamp(8px,3vw,14px);
        margin-bottom: clamp(10px,3vw,16px);
    }

    /* Título pixel */
    .ititulo {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(9px,3.1vw,14px);
        color: #fff; text-align: center; line-height: 1; margin: 0;
    }
    .tl1, .tl2 {
        display: block; white-space: nowrap;
        text-shadow: 0 0 14px #7b2fff99, 0 0 28px #7b2fff55;
    }
    .tl1 {
        margin-bottom: clamp(10px,3vw,16px);
        animation: tbounce 1.9s ease-in-out infinite, tglitch 7s step-end infinite;
    }
    .tl2 {
        animation: tbounce 1.9s ease-in-out infinite, tglitch 7s step-end infinite;
        animation-delay: 0.18s, 0.6s;
    }
    @keyframes tbounce {
        0%,100% { transform: translateY(0)     scaleY(1);    }
        35%     { transform: translateY(-10px) scaleY(1.10); }
        55%     { transform: translateY(-4px)  scaleY(1.03); }
        70%     { transform: translateY(-7px)  scaleY(1.06); }
    }
    @keyframes tglitch {
        0%,85%,100% { transform:skewX(0) translateX(0); color:#fff;
                      text-shadow:0 0 14px #7b2fff99,0 0 28px #7b2fff55; }
        86% { transform:translateX(-5px) skewX(-9deg); color:#ff4d6d;
              text-shadow:-3px 0 #00ffff, 3px 0 #ff4d6d; }
        88% { transform:translateX(5px)  skewX(9deg);  color:#00ffff;
              text-shadow: 3px 0 #ff4d6d,-3px 0 #00ffff; }
        90% { transform:translateX(-2px) skewX(-3deg); color:#fff;
              text-shadow:2px 0 #7b2fff,-2px 0 #FFD700; }
        92% { transform:translateX(0)   skewX(0);      color:#fff;
              text-shadow:0 0 14px #7b2fff99,0 0 28px #7b2fff55; }
    }
    /* Subtítulo */
    .isub {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.68rem,2.5vw,.78rem); color: #ccccff;
        font-weight: 300; letter-spacing: clamp(1px,1vw,3px);
        text-transform: uppercase; margin-top: clamp(10px,3vw,16px);
    }

    /* Skyline */
    .skyline-bg {
        position: fixed; bottom: 0; left: 0;
        width: 100%; height: 200px;
        pointer-events: none; z-index: 0;
        opacity: .18;
        filter: drop-shadow(0 -6px 30px rgba(123,47,255,.5));
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Estrellas (iframe 0px) ────────────────────────────────────────────────
    components.html("""
    <style>body{margin:0;background:transparent;overflow:hidden}</style>
    <canvas id="c" style="position:fixed;top:0;left:0;width:100vw;height:100vh;
        pointer-events:none;z-index:0"></canvas>
    <script>
    var c=document.getElementById('c'),cx=c.getContext('2d');
    function rs(){c.width=window.innerWidth;c.height=window.innerHeight}rs();
    var S=[],COL=['#fff','#c4b5fd','#a78bfa','#818cf8','#e0d7ff'];
    for(var i=0;i<160;i++)S.push({
        x:Math.random()*c.width, y:Math.random()*c.height,
        r:Math.random()*1.5+0.2, a:Math.random()*.55+0.15,
        da:(Math.random()*.011+.003)*(Math.random()<.5?1:-1),
        dx:(Math.random()-.5)*.18, dy:(Math.random()-.5)*.12,
        col:COL[Math.floor(Math.random()*5)]
    });
    function draw(){
        cx.clearRect(0,0,c.width,c.height);
        S.forEach(function(s){
            s.x+=s.dx;s.y+=s.dy;s.a+=s.da;
            if(s.a>.92||s.a<.08)s.da*=-1;
            if(s.x<0)s.x=c.width;if(s.x>c.width)s.x=0;
            if(s.y<0)s.y=c.height;if(s.y>c.height)s.y=0;
            cx.save();cx.globalAlpha=s.a;
            cx.beginPath();cx.arc(s.x,s.y,s.r,0,Math.PI*2);
            cx.fillStyle=s.col;cx.shadowColor=s.col;cx.shadowBlur=s.r*4;
            cx.fill();cx.restore();
        });
        requestAnimationFrame(draw);
    }
    draw();window.addEventListener('resize',rs);
    </script>
    """, height=0, scrolling=False)

    # ── Skyline SVG ───────────────────────────────────────────────────────────
    st.markdown("""
    <svg class="skyline-bg" viewBox="0 0 1440 200"
         xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax slice">
      <defs>
        <linearGradient id="cg" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"   stop-color="#7b2fff" stop-opacity="1"/>
          <stop offset="100%" stop-color="#3b0080" stop-opacity="0.3"/>
        </linearGradient>
      </defs>
      <path fill="url(#cg)" d="
        M0,200 L0,155 L40,155 L40,125 L58,125 L58,95 L70,95 L70,70
        L80,70 L80,50 L88,50 L88,30 L94,30 L94,10 L100,10 L100,30
        L106,30 L106,50 L116,50 L116,70 L132,70 L132,95 L152,95
        L152,70 L164,70 L164,46 L172,46 L172,24 L178,24 L178,46
        L186,46 L186,70 L202,70 L202,50 L212,50 L212,28 L220,28
        L220,10 L226,10 L226,28 L234,28 L234,50 L250,50 L250,75
        L270,75 L270,50 L280,50 L280,30 L288,30 L288,50 L302,50
        L302,75 L322,75 L322,46 L332,46 L332,26 L340,26 L340,8
        L346,8 L346,26 L354,26 L354,46 L370,46 L370,70 L392,70
        L392,46 L402,46 L402,26 L410,26 L410,46 L422,46 L422,70
        L442,70 L442,46 L452,46 L452,26 L460,26 L460,8 L466,8
        L466,2 L472,2 L472,8 L478,8 L478,26 L486,26 L486,46
        L502,46 L502,70 L522,70 L522,46 L532,46 L532,26 L540,26
        L540,46 L552,46 L552,70 L572,70 L572,46 L582,46 L582,26
        L590,26 L590,46 L602,46 L602,70 L622,70 L622,44 L632,44
        L632,24 L640,24 L640,8 L646,8 L646,24 L654,24 L654,44
        L670,44 L670,70 L690,70 L690,44 L700,44 L700,24 L708,24
        L708,44 L720,44 L720,70 L740,70 L740,44 L750,44 L750,24
        L758,24 L758,44 L770,44 L770,70 L790,70 L790,44 L800,44
        L800,24 L808,24 L808,8 L814,8 L814,24 L822,24 L822,44
        L838,44 L838,70 L858,70 L858,44 L868,44 L868,24 L876,24
        L876,44 L888,44 L888,70 L908,70 L908,44 L918,44 L918,24
        L926,24 L926,44 L938,44 L938,70 L958,70 L958,44 L968,44
        L968,24 L976,24 L976,8 L982,8 L982,24 L990,24 L990,44
        L1006,44 L1006,70 L1026,70 L1026,44 L1036,44 L1036,24
        L1044,24 L1044,44 L1056,44 L1056,70 L1076,70 L1076,44
        L1086,44 L1086,24 L1094,24 L1094,44 L1106,44 L1106,70
        L1126,70 L1126,44 L1136,44 L1136,24 L1144,24 L1144,8
        L1150,8 L1150,24 L1158,24 L1158,44 L1174,44 L1174,70
        L1194,70 L1194,44 L1204,44 L1204,24 L1212,24 L1212,44
        L1224,44 L1224,70 L1244,70 L1254,44 L1254,24 L1262,24
        L1262,44 L1274,44 L1274,70 L1294,70 L1304,44 L1304,24
        L1312,24 L1312,8 L1318,8 L1318,24 L1326,24 L1326,44
        L1342,44 L1342,70 L1362,70 L1378,44 L1378,70 L1412,70
        L1432,44 L1432,70 L1440,70 L1440,200 Z"/>
      <g fill="#FFD700" opacity="0.5">
        <rect x="94"   y="14" width="3" height="4"/>
        <rect x="340"  y="12" width="3" height="4"/>
        <rect x="466"  y="6"  width="3" height="4"/>
        <rect x="640"  y="12" width="3" height="4"/>
        <rect x="808"  y="12" width="3" height="4"/>
        <rect x="976"  y="12" width="3" height="4"/>
        <rect x="1144" y="12" width="3" height="4"/>
        <rect x="1312" y="12" width="3" height="4"/>
      </g>
    </svg>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PANEL SUPERIOR — HTML puro (ícono + badge + título + subtítulo)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="ip">
        <span class="cicon">🏙️</span>
        <div class="ibadge">🌐 Pensamiento Sistémico 🌐</div>
        <p class="ititulo">
            <span class="tl1">CIUDAD EN</span>
            <span class="tl2">EQUILIBRIO</span>
        </p>
        <p class="isub">Gestiona tu ciudad · Salva el futuro</p>
    </div>
    <div class="isep"></div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA DE BOTONES — st.button() REALES de Streamlit
    # Siempre funcionan: no dependen de JavaScript ni iframes
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="bzone">', unsafe_allow_html=True)

    st.markdown('<p class="ihelper">⬇ Selecciona una opción para continuar ⬇</p>',
                unsafe_allow_html=True)

    # ── Botón 1: INICIAR SESIÓN ───────────────────────────────────────────────
    # Acción: navegar("login") → session_state["pantalla"] = "login" → st.rerun()
    # Router: "login" → pantalla_login() en screen_auth.py
    # pantalla_login: login_grupo(nombre,pw) en database.py → navegar("lobby")
    st.markdown('<div class="btn-login">', unsafe_allow_html=True)
    if st.button("🔐  INICIAR SESIÓN", key="btn_login", use_container_width=True):
        navegar("login")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Botón 2: REGISTRAR GRUPO ──────────────────────────────────────────────
    # Acción: navegar("registro") → session_state["pantalla"] = "registro" → st.rerun()
    # Router: "registro" → pantalla_registro() en screen_auth.py
    # pantalla_registro: registrar_grupo() + guardar_estudiante() en database.py → navegar("lobby")
    st.markdown('<div class="btn-registro">', unsafe_allow_html=True)
    if st.button("📝  REGISTRAR GRUPO", key="btn_registro", use_container_width=True):
        navegar("registro")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    anio = datetime.datetime.now().year
    st.markdown(
        "<p class='ifooter'>⚡ Ciudad en Equilibrio · v2.0 · " + str(anio) + " ⚡</p>",
        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)   # cierra .bzone


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA INSTRUCCIONES — requerida por router.py
#  Acceso: Lobby → INSTRUCCIONES  (botón "⬅ Volver al Lobby")
#          Juego → ⚙️ → Instrucciones (botón "⬅ Volver al Juego" o "🏠 Lobby")
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_instrucciones():
    from_juego = st.session_state.get("_from_juego", False)

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap');
    #MainMenu, footer, header { visibility: hidden; }
    html, body, [data-testid="stAppViewContainer"] { background: #0d0025 !important; }
    .inst-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(0.55rem,1.8vw,0.82rem);
        color: #fff; text-shadow: 0 0 18px #7b2fff99;
        text-align: center; margin-bottom: 24px; line-height: 1.9;
    }
    .inst-card {
        background: rgba(18,4,52,.88);
        border: 1px solid rgba(123,47,255,.32);
        border-radius: 14px; padding: 14px 18px;
        margin-bottom: 9px;
    }
    .inst-card-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.78rem,2vw,.90rem); font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: #FFD700; margin: 0 0 7px;
    }
    .inst-item {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.74rem,2vw,.82rem); color: #c4b5fd;
        line-height: 1.72; margin: 3px 0; padding-left: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown('<h1 class="inst-title">📖 INSTRUCCIONES</h1>',
                    unsafe_allow_html=True)

        secciones = [
            ("🏙️ Objetivo", [
                "Administra la ciudad durante <b>10 rondas</b> sin que los indicadores colapsen.",
                "Si cualquier indicador llega a <b>0</b>, la ciudad colapsa.",
                "Completa las 10 rondas para ganar.",
            ]),
            ("📊 Los 4 Indicadores", [
                "💰 <b>Economía</b> — Finanzas y desarrollo",
                "🌿 <b>Medio Ambiente</b> — Salud ecológica",
                "⚡ <b>Energía</b> — Suministro energético",
                "❤️ <b>Bienestar Social</b> — Calidad de vida",
            ]),
            ("🔄 Flujo de Ronda", [
                "1️⃣ Elige una <b>decisión de ciudad</b>",
                "2️⃣ Responde una <b>pregunta académica</b> en 30s",
                "✅ Acierto → efectos positivos aplicados",
                "❌ Fallo → penalización según dificultad",
                "3️⃣ Ocurre un <b>evento aleatorio</b>",
            ]),
            ("⚙️ Dificultades", [
                "🟢 <b>Fácil</b> — Penalización baja",
                "🟡 <b>Normal</b> — Balance equilibrado",
                "🔴 <b>Difícil</b> — Penalización alta",
            ]),
            ("⭐ Atributos", [
                "Gana estrellas completando partidas y misiones.",
                "Canjéalas en el juego para activar atributos por ronda.",
            ]),
            ("💡 Consejos", [
                "Mantén indicadores &gt; 30 para evitar colapso.",
                "Verde (&gt;60) = estable · Amarillo (30–60) = vigilar.",
                "Coordina las decisiones del equipo.",
            ]),
        ]

        for titulo, items in secciones:
            items_html = "".join(
                "<div class='inst-item'>• " + i + "</div>" for i in items)
            st.markdown(
                "<div class='inst-card'>"
                "<div class='inst-card-title'>" + titulo + "</div>"
                + items_html + "</div>",
                unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if from_juego:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("⬅️  VOLVER AL JUEGO", use_container_width=True, type="primary"):
                    st.session_state["_from_juego"] = False
                    navegar("juego")
            with c2:
                if st.button("🏠  VOLVER AL LOBBY", use_container_width=True):
                    st.session_state["_from_juego"] = False
                    navegar("lobby")
        else:
            if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
                navegar("lobby")
