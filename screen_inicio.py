import streamlit as st
import streamlit.components.v1 as components
from session_manager import navegar


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA DE INICIO
#  Flujo: Inicio → Login → Lobby
#         Inicio → Registro → Lobby
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_inicio():

    # ── Detectar navegación desde los botones HTML ────────────────────────────
    accion = st.query_params.get("action", "")
    if accion == "login":
        st.query_params.clear()
        navegar("login")       # screen_auth.pantalla_login → navega a "lobby"
        return
    if accion == "registro":
        st.query_params.clear()
        navegar("registro")    # screen_auth.pantalla_registro → navega a "lobby"
        return

    # ── CSS base: ocultar Streamlit y fondo oscuro ───────────────────────────
    st.markdown("""
    <style>
    #MainMenu, footer, header,
    [data-testid="stToolbar"],
    .stDeployButton { display: none !important; }
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
    </style>
    """, unsafe_allow_html=True)

    # ── Panel completo en HTML ────────────────────────────────────────────────
    # Todo el visual vive aquí. Botones HTML nativos = siempre dentro del panel.
    # Navegación: clic → ?action=login/registro → Streamlit recarga → navegar()
    # ─────────────────────────────────────────────────────────────────────────
    components.html("""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background: #0d0025;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Rajdhani', sans-serif;
    overflow-x: hidden;
    padding: 20px 12px;
}

/* Estrellas */
#sf {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0;
}

/* Nebulosa */
.neb {
    position: fixed; inset: 0;
    z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 70% 50% at 15% 25%, rgba(123,47,255,.28) 0%, transparent 60%),
        radial-gradient(ellipse 55% 65% at 85% 75%, rgba(99,102,241,.22) 0%, transparent 60%),
        radial-gradient(ellipse 80% 30% at 50% 110%, rgba(123,47,255,.30) 0%, transparent 55%);
    animation: neb 12s ease-in-out infinite alternate;
}
@keyframes neb {
    0%   { opacity: .7;  transform: scale(1);    }
    100% { opacity: 1.0; transform: scale(1.05); }
}

/* Skyline */
.sky {
    position: fixed; bottom: 0; left: 0;
    width: 100%; height: 200px;
    pointer-events: none; z-index: 0;
    animation: skyglow 4s ease-in-out infinite alternate;
}
@keyframes skyglow {
    0%   { opacity: .12; filter: drop-shadow(0 -6px 28px rgba(123,47,255,.32)); }
    100% { opacity: .26; filter: drop-shadow(0 -8px 55px rgba(123,47,255,.70))
                                  drop-shadow(0 -2px 22px rgba(255,215,0,.22)); }
}

/* ══════════════════════════════════════════════
   PANEL ÚNICO — responsivo con clamp()
   ══════════════════════════════════════════════ */
.panel {
    position: relative; z-index: 1;
    width: 100%;
    max-width: min(420px, 95vw);
    background: rgba(18, 4, 52, .93);
    border: 1.5px solid rgba(123, 47, 255, .52);
    border-radius: 22px;
    overflow: hidden;
    animation: pglow 4s ease-in-out infinite, fadein .7s ease both;
}
@keyframes pglow {
    0%,100% { box-shadow: 0 0 20px #7b2fff44, 0 0 50px #7b2fff18; }
    50%     { box-shadow: 0 0 42px #7b2fff99, 0 0 88px #7b2fff50; }
}
@keyframes fadein {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0);    }
}

/* Línea de energía */
.eline {
    position: absolute; top: 0; left: -100%;
    height: 2px; width: 55%; z-index: 3;
    background: linear-gradient(90deg,
        transparent, #7b2fff, #FFD700, #00ffff, transparent);
    animation: eline 2.8s linear infinite;
}
@keyframes eline {
    0%   { left: -100%; width: 55%; }
    100% { left:  110%; width: 75%; }
}

/* Secciones */
.ptop {
    padding: clamp(20px, 5vw, 32px) clamp(18px, 5vw, 28px) clamp(14px, 3vw, 20px);
    text-align: center;
    border-bottom: 1px solid rgba(123, 47, 255, .22);
}
.pbot {
    padding: clamp(14px, 4vw, 20px) clamp(18px, 5vw, 28px) clamp(18px, 5vw, 26px);
    text-align: center;
}

/* Ícono */
.icon {
    font-size: clamp(2.2rem, 8vw, 3rem);
    display: block;
    margin-bottom: clamp(8px, 2vw, 12px);
    animation: float 4s ease-in-out infinite;
    filter: drop-shadow(0 0 18px #7b2fffcc)
            drop-shadow(0 0 40px #7b2fff88)
            drop-shadow(0 0  8px #FFD70055);
}
@keyframes float {
    0%,100% { transform: translateY(0);     }
    50%     { transform: translateY(-10px); }
}

/* Badge */
.badge {
    display: inline-block;
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(.56rem, 1.8vw, .65rem);
    font-weight: 600; letter-spacing: 2px; text-transform: uppercase;
    color: #a78bfa;
    background: rgba(123, 47, 255, .14);
    border: 1px solid rgba(123, 47, 255, .36);
    border-radius: 20px;
    padding: 4px clamp(8px, 3vw, 14px);
    margin-bottom: clamp(10px, 3vw, 16px);
}

/* Título */
.title {
    font-family: 'Press Start 2P', monospace;
    font-size: clamp(9px, 3.1vw, 14px);
    color: #fff;
    text-align: center;
    line-height: 1;
    margin: 0;
}
.tl1, .tl2 {
    display: block;
    white-space: nowrap;
    text-shadow: 0 0 14px #7b2fff99, 0 0 28px #7b2fff55;
}
.tl1 {
    margin-bottom: clamp(10px, 3vw, 16px);
    animation: tbounce 1.9s ease-in-out infinite,
               tglitch 7s   step-end    infinite;
}
.tl2 {
    animation: tbounce 1.9s ease-in-out infinite,
               tglitch 7s   step-end    infinite;
    animation-delay: 0.18s, 0.6s;
}
@keyframes tbounce {
    0%,100% { transform: translateY(0)     scaleY(1);    }
    35%     { transform: translateY(-10px) scaleY(1.10); }
    55%     { transform: translateY(-4px)  scaleY(1.03); }
    70%     { transform: translateY(-7px)  scaleY(1.06); }
}
@keyframes tglitch {
    0%,85%,100% {
        transform: skewX(0) translateX(0); color: #fff;
        text-shadow: 0 0 14px #7b2fff99, 0 0 28px #7b2fff55;
    }
    86% { transform: translateX(-5px) skewX(-9deg); color: #ff4d6d;
          text-shadow: -3px 0 #00ffff, 3px 0 #ff4d6d; }
    88% { transform: translateX( 5px) skewX( 9deg); color: #00ffff;
          text-shadow:  3px 0 #ff4d6d,-3px 0 #00ffff; }
    90% { transform: translateX(-2px) skewX(-3deg); color: #fff;
          text-shadow: 2px 0 #7b2fff,-2px 0 #FFD700; }
    92% { transform: translateX(0)    skewX(0);     color: #fff;
          text-shadow: 0 0 14px #7b2fff99, 0 0 28px #7b2fff55; }
}

/* Subtítulo */
.sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(.68rem, 2.5vw, .78rem);
    color: #ccccff; font-weight: 300;
    letter-spacing: clamp(1px, 1vw, 3px);
    text-transform: uppercase;
    margin-top: clamp(10px, 3vw, 16px);
}

/* Separador */
.sep {
    height: 2px;
    background: linear-gradient(90deg,
        transparent 0%, #7b2fff 30%, #FFD700 50%, #7b2fff 70%, transparent 100%);
    opacity: .9;
}

/* Helper */
.helper {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(.58rem, 2vw, .67rem);
    color: rgba(167, 139, 250, .36);
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-bottom: clamp(10px, 3vw, 14px);
}

/* Botón dorado */
.btn-g {
    display: block; width: 100%;
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(.82rem, 3vw, 1rem);
    font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
    padding: clamp(10px, 3vw, 13px) 16px;
    margin-bottom: clamp(8px, 2vw, 10px);
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #12003e; border: none; border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 4px 22px rgba(255,215,0,.40);
    transition: all .22s ease;
    position: relative; overflow: hidden;
}
.btn-g::after {
    content: ''; position: absolute; top: 0; left: -80%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg,
        transparent, rgba(255,255,255,.38), transparent);
    transform: skewX(-20deg);
    animation: shine 2.4s ease-in-out infinite;
}
@keyframes shine { 0% { left: -80%; } 100% { left: 130%; } }
.btn-g:hover {
    background: linear-gradient(135deg, #FFE44D, #FFB733);
    box-shadow: 0 6px 36px rgba(255,215,0,.68);
    transform: translateY(-3px);
}

/* Botón púrpura */
.btn-p {
    display: block; width: 100%;
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(.82rem, 3vw, 1rem);
    font-weight: 700; letter-spacing: 2px; text-transform: uppercase;
    padding: clamp(10px, 3vw, 13px) 16px;
    background: transparent; color: #c4b5fd;
    border: 1.5px solid #7b2fff; border-radius: 12px;
    cursor: pointer;
    box-shadow: 0 0 13px rgba(123,47,255,.24);
    transition: all .22s ease;
}
.btn-p:hover {
    background: linear-gradient(135deg,
        rgba(123,47,255,.24), rgba(99,102,241,.18));
    border-color: #a78bfa; color: #fff;
    box-shadow: 0 0 32px rgba(123,47,255,.60),
                0 0 60px rgba(123,47,255,.28);
    transform: translateY(-3px);
}

/* Footer */
.footer {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(.52rem, 1.8vw, .60rem);
    color: rgba(167, 139, 250, .26);
    letter-spacing: 1.5px; text-transform: uppercase;
    margin-top: clamp(12px, 3vw, 18px);
}
</style>
</head>
<body>

<canvas id="sf"></canvas>
<div class="neb"></div>

<svg class="sky" viewBox="0 0 1440 200" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax slice">
  <defs>
    <linearGradient id="cg" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%"   stop-color="#7b2fff" stop-opacity="1"/>
      <stop offset="100%" stop-color="#3b0080" stop-opacity="0.3"/>
    </linearGradient>
  </defs>
  <path fill="url(#cg)" d="
    M0,200 L0,155 L38,155 L38,125 L55,125 L55,95 L68,95 L68,70
    L78,70 L78,50 L86,50 L86,30 L92,30 L92,10 L98,10 L98,30
    L104,30 L104,50 L114,50 L114,70 L130,70 L130,95 L150,95
    L150,70 L162,70 L162,46 L170,46 L170,24 L176,24 L176,46
    L184,46 L184,70 L200,70 L200,50 L210,50 L210,28 L218,28
    L218,10 L224,10 L224,28 L232,28 L232,50 L248,50 L248,75
    L268,75 L268,50 L278,50 L278,30 L286,30 L286,50 L300,50
    L300,75 L320,75 L320,46 L330,46 L330,26 L338,26 L338,8
    L344,8 L344,26 L352,26 L352,46 L368,46 L368,70 L390,70
    L390,46 L400,46 L400,26 L408,26 L408,46 L420,46 L420,70
    L440,70 L440,46 L450,46 L450,26 L458,26 L458,8 L464,8
    L464,2 L470,2 L470,8 L476,8 L476,26 L484,26 L484,46
    L500,46 L500,70 L520,70 L520,46 L530,46 L530,26 L538,26
    L538,46 L550,46 L550,70 L570,70 L570,46 L580,46 L580,26
    L588,26 L588,46 L600,46 L600,70 L620,70 L620,44 L630,44
    L630,24 L638,24 L638,8 L644,8 L644,24 L652,24 L652,44
    L668,44 L668,70 L688,70 L688,44 L698,44 L698,24 L706,24
    L706,44 L718,44 L718,70 L738,70 L738,44 L748,44 L748,24
    L756,24 L756,44 L768,44 L768,70 L788,70 L788,44 L798,44
    L798,24 L806,24 L806,8 L812,8 L812,24 L820,24 L820,44
    L836,44 L836,70 L856,70 L856,44 L866,44 L866,24 L874,24
    L874,44 L886,44 L886,70 L906,70 L906,44 L916,44 L916,24
    L924,24 L924,44 L936,44 L936,70 L956,70 L956,44 L966,44
    L966,24 L974,24 L974,8 L980,8 L980,24 L988,24 L988,44
    L1004,44 L1004,70 L1024,70 L1024,44 L1034,44 L1034,24
    L1042,24 L1042,44 L1054,44 L1054,70 L1074,70 L1074,44
    L1084,44 L1084,24 L1092,24 L1092,44 L1104,44 L1104,70
    L1124,70 L1124,44 L1134,44 L1134,24 L1142,24 L1142,8
    L1148,8 L1148,24 L1156,24 L1156,44 L1172,44 L1172,70
    L1192,70 L1192,44 L1202,44 L1202,24 L1210,24 L1210,44
    L1222,44 L1222,70 L1242,70 L1252,44 L1252,24 L1260,24
    L1260,44 L1272,44 L1272,70 L1292,70 L1302,44 L1302,24
    L1310,24 L1310,8 L1316,8 L1316,24 L1324,24 L1324,44
    L1340,44 L1340,70 L1360,70 L1375,44 L1375,70 L1410,70
    L1430,44 L1430,70 L1440,70 L1440,200 Z"/>
  <g fill="#FFD700" opacity="0.45">
    <rect x="92"   y="14" width="3" height="3"/>
    <rect x="338"  y="12" width="3" height="3"/>
    <rect x="464"  y="6"  width="3" height="3"/>
    <rect x="638"  y="12" width="3" height="3"/>
    <rect x="806"  y="12" width="3" height="3"/>
    <rect x="974"  y="12" width="3" height="3"/>
    <rect x="1142" y="12" width="3" height="3"/>
  </g>
</svg>

<div class="panel">
  <div class="eline"></div>
  <div class="ptop">
    <span class="icon">&#127961;&#65039;</span>
    <div class="badge">&#127760; Pensamiento Sistémico &#127760;</div>
    <p class="title">
      <span class="tl1">CIUDAD EN</span>
      <span class="tl2">EQUILIBRIO</span>
    </p>
    <p class="sub">Gestiona tu ciudad · Salva el futuro</p>
  </div>
  <div class="sep"></div>
  <div class="pbot">
    <p class="helper">&#11015; Selecciona una opción para continuar &#11015;</p>
    <button class="btn-g" onclick="ir('login')">
      &#128272;&nbsp; INICIAR SESIÓN
    </button>
    <button class="btn-p" onclick="ir('registro')">
      &#128196;&nbsp; REGISTRAR GRUPO
    </button>
    <p class="footer" id="yr">&#9889; Ciudad en Equilibrio · v2.0 · 2026 &#9889;</p>
  </div>
</div>

<script>
(function () {
    var c = document.getElementById('sf');
    var cx = c.getContext('2d');
    function rs() { c.width = window.innerWidth; c.height = window.innerHeight; }
    rs();
    var COL = ['#ffffff', '#c4b5fd', '#a78bfa', '#818cf8', '#e0d7ff'];
    var S = [];
    for (var i = 0; i < 160; i++) {
        S.push({
            x: Math.random() * c.width, y: Math.random() * c.height,
            r: Math.random() * 1.5 + 0.2, a: Math.random() * 0.55 + 0.2,
            da: (Math.random() * 0.011 + 0.003) * (Math.random() < .5 ? 1 : -1),
            dx: (Math.random() - .5) * .18, dy: (Math.random() - .5) * .12,
            col: COL[Math.floor(Math.random() * COL.length)]
        });
    }
    function draw() {
        cx.clearRect(0, 0, c.width, c.height);
        for (var i = 0; i < S.length; i++) {
            var s = S[i];
            s.x += s.dx; s.y += s.dy; s.a += s.da;
            if (s.a > .92 || s.a < .1) s.da *= -1;
            if (s.x < 0) s.x = c.width; if (s.x > c.width) s.x = 0;
            if (s.y < 0) s.y = c.height; if (s.y > c.height) s.y = 0;
            cx.save(); cx.globalAlpha = s.a;
            cx.beginPath(); cx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            cx.fillStyle = s.col; cx.shadowColor = s.col;
            cx.shadowBlur = s.r * 4; cx.fill(); cx.restore();
        }
        requestAnimationFrame(draw);
    }
    draw();
    window.addEventListener('resize', rs);
})();

document.getElementById('yr').textContent =
    '\u26A1 Ciudad en Equilibrio \u00B7 v2.0 \u00B7 ' +
    new Date().getFullYear() + ' \u26A1';

function ir(dest) {
    try {
        var base = window.parent.location.href.split('?')[0];
        window.parent.location.href = base + '?action=' + dest;
    } catch (e) {
        window.location.href = window.location.href.split('?')[0] + '?action=' + dest;
    }
}
</script>
</body>
</html>""",
        height=700,
        scrolling=False,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA DE INSTRUCCIONES
#  Requerida por router.py.
#  Se accede desde DOS lugares:
#    1. Lobby  → botón INSTRUCCIONES → volver al Lobby
#    2. Juego  → ⚙️ Configuración → Instrucciones → volver al Juego
#  El session_state["_from_juego"] = True indica que viene del juego.
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
        font-size: clamp(0.55rem, 1.8vw, 0.85rem);
        color: #fff; text-shadow: 0 0 18px #7b2fff99;
        text-align: center; margin-bottom: 24px; line-height: 1.9;
    }
    .inst-card {
        background: rgba(18,4,52,.88);
        border: 1px solid rgba(123,47,255,.34);
        border-radius: 16px; padding: 15px 19px;
        margin-bottom: 10px; backdrop-filter: blur(16px);
    }
    .inst-card-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.80rem, 2vw, .92rem); font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: #FFD700; margin: 0 0 8px;
    }
    .inst-item {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(.76rem, 2vw, .84rem); color: #c4b5fd;
        line-height: 1.72; margin: 3px 0; padding-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown('<h1 class="inst-title">📖 INSTRUCCIONES</h1>',
                    unsafe_allow_html=True)

        secciones = [
            ("🏙️ Objetivo", [
                "Administra la ciudad durante <b>10 rondas</b> manteniendo los 4 indicadores en equilibrio.",
                "Si cualquier indicador llega a <b>0</b>, la ciudad colapsa.",
                "Gana completando las 10 rondas sin colapso.",
            ]),
            ("📊 Los 4 Indicadores", [
                "💰 <b>Economía</b> — Finanzas y desarrollo económico",
                "🌿 <b>Medio Ambiente</b> — Salud ecológica de la ciudad",
                "⚡ <b>Energía</b> — Suministro y sostenibilidad energética",
                "❤️ <b>Bienestar Social</b> — Calidad de vida de los ciudadanos",
            ]),
            ("🔄 Flujo de cada Ronda", [
                "1️⃣ El estudiante en turno elige una <b>decisión de ciudad</b>",
                "2️⃣ Responde una <b>pregunta académica</b> en 30 segundos",
                "✅ Acierto → se aplican los efectos positivos de la decisión",
                "❌ Fallo → penalización en todos los indicadores según dificultad",
                "3️⃣ Ocurre un <b>evento aleatorio</b> que afecta los indicadores",
            ]),
            ("⚙️ Dificultades", [
                "🟢 <b>Fácil</b> — Penalización baja · eventos más favorables",
                "🟡 <b>Normal</b> — Balance equilibrado de retos",
                "🔴 <b>Difícil</b> — Penalización alta · más eventos negativos",
            ]),
            ("⭐ Estrellas y Logros", [
                "Gana estrellas al completar partidas y misiones.",
                "Úsalas para activar atributos especiales durante el juego.",
                "Desbloquea logros cumpliendo objetivos específicos.",
            ]),
            ("💡 Consejos", [
                "Mantén todos los indicadores &gt; 30 para evitar colapso.",
                "Verde (&gt; 60) = estable · Amarillo (30–60) = vigilar.",
                "Coordina las decisiones del grupo para equilibrar todos los indicadores.",
            ]),
        ]

        for titulo, items in secciones:
            items_html = "".join(
                f"<div class='inst-item'>• {i}</div>" for i in items)
            st.markdown(
                f"<div class='inst-card'>"
                f"<div class='inst-card-title'>{titulo}</div>"
                f"{items_html}</div>",
                unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Botones de navegación según origen ───────────────────────────────
        if from_juego:
            # Viene del juego → mostrar ambos botones
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
            # Viene del lobby → solo volver al lobby
            if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
                navegar("lobby")
