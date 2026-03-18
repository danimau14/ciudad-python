import streamlit as st
import streamlit.components.v1 as components
from session_manager import navegar


def pantalla_inicio():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap');

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none !important; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0025 !important;
        overflow-x: hidden;
    }

    /* Nebulosa de fondo */
    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed; inset: 0;
        background:
            radial-gradient(ellipse 75% 55% at 12% 22%, rgba(123,47,255,0.30) 0%, transparent 62%),
            radial-gradient(ellipse 60% 70% at 88% 78%, rgba(99,102,241,0.24) 0%, transparent 62%),
            radial-gradient(ellipse 50% 38% at 50% 98%, rgba(167,139,250,0.18) 0%, transparent 62%);
        pointer-events: none; z-index: 0;
        animation: nebula 14s ease-in-out infinite alternate;
    }
    @keyframes nebula {
        0%   { opacity: 0.7; transform: scale(1);    }
        100% { opacity: 1.0; transform: scale(1.05); }
    }

    /* Silueta ciudad */
    .city-bg {
        position: fixed; bottom: 0; left: 0;
        width: 100%; height: 260px;
        z-index: 0; pointer-events: none;
        animation: cityglow 4s ease-in-out infinite alternate;
    }
    @keyframes cityglow {
        0%   { opacity: 0.14; filter: drop-shadow(0 -8px 35px rgba(123,47,255,0.35)); }
        100% { opacity: 0.28; filter: drop-shadow(0 -10px 65px rgba(123,47,255,0.72))
                                      drop-shadow(0 -2px 28px rgba(255,215,0,0.25)); }
    }

    /* Keyframes generales */
    @keyframes float {
        0%, 100% { transform: translateY(0);    }
        50%       { transform: translateY(-11px); }
    }
    @keyframes pglow {
        0%, 100% { box-shadow: 0 0 20px #7b2fff44, 0 0 50px #7b2fff18; }
        50%       { box-shadow: 0 0 42px #7b2fff99, 0 0 90px #7b2fff50; }
    }
    @keyframes fadein {
        from { opacity: 0; transform: translateY(28px); }
        to   { opacity: 1; transform: translateY(0);    }
    }
    @keyframes eline {
        0%   { left: -100%; width: 55%; }
        100% { left: 110%;  width: 75%; }
    }
    @keyframes shine {
        0%   { left: -80%; }
        100% { left: 130%; }
    }
    @keyframes tbounce {
        0%, 100% { transform: translateY(0);    }
        40%       { transform: translateY(-8px); }
        60%       { transform: translateY(-4px); }
    }
    @keyframes tglitch {
        0%,87%,100% { transform:skewX(0);   color:#fff;
                      text-shadow:0 0 16px #7b2fff99,0 0 30px #7b2fff55; }
        88%          { transform:skewX(-7deg); color:#ff4d6d;
                      text-shadow:-3px 0 #00ffff,3px 0 #ff4d6d; }
        90%          { transform:skewX(7deg);  color:#00ffff;
                      text-shadow:3px 0 #ff4d6d,-3px 0 #00ffff; }
        92%          { transform:skewX(0);   color:#fff;
                      text-shadow:0 0 16px #7b2fff99,0 0 30px #7b2fff55; }
    }

    /* Layout centrado */
    .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        padding: 1.5rem 1rem !important;
        max-width: 440px !important;
        margin: 0 auto !important;
        position: relative; z-index: 1;
    }

    /* === PANEL SUPERIOR === */
    .ip {
        background: rgba(18,4,52,0.93);
        border: 1.5px solid rgba(123,47,255,0.52);
        border-bottom: none;
        border-radius: 24px 24px 0 0;
        padding: 34px 26px 24px;
        text-align: center;
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        width: 100%;
        animation: pglow 4s ease-in-out infinite, fadein 0.7s ease;
        position: relative; overflow: hidden; z-index: 2;
    }
    /* Línea de energía */
    .ip::before {
        content: ''; position: absolute; top: 0; height: 2px;
        background: linear-gradient(90deg,
            transparent,#7b2fff,#FFD700,#00ffff,transparent);
        animation: eline 2.8s linear infinite;
    }

    /* Ícono */
    .cicon {
        font-size: 3.4rem; display: block; margin-bottom: 11px;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 20px #7b2fffcc)
                drop-shadow(0 0 45px #7b2fff88)
                drop-shadow(0 0 8px #FFD70055);
    }

    /* Badge */
    .ibadge {
        display: inline-block;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.67rem; font-weight: 600;
        letter-spacing: 2px; text-transform: uppercase;
        color: #a78bfa;
        background: rgba(123,47,255,0.14);
        border: 1px solid rgba(123,47,255,0.38);
        border-radius: 20px; padding: 4px 13px; margin-bottom: 18px;
    }

    /* === TÍTULO ===
       - Texto completo por línea (sin spans individuales)
       - font-size 15px: "CIUDAD EN" ≈ 130px, "EQUILIBRIO" ≈ 145px
         → ambos caben en el panel de ~388px de contenido
       - white-space: nowrap garantiza que nunca se parta
    */
    .ititle {
        font-family: 'Press Start 2P', monospace;
        font-size: 15px;
        color: #fff;
        margin: 0 0 6px;
        text-align: center;
        line-height: 1;
    }
    .tl1 {
        display: block; white-space: nowrap; margin-bottom: 13px;
        text-shadow: 0 0 14px #7b2fff99, 0 0 28px #7b2fff55;
        animation: tbounce 2s ease-in-out infinite,
                   tglitch 7s step-end  infinite;
    }
    .tl2 {
        display: block; white-space: nowrap;
        text-shadow: 0 0 14px #7b2fff99, 0 0 28px #7b2fff55;
        animation: tbounce 2s ease-in-out infinite,
                   tglitch 7s step-end  infinite;
        animation-delay: 0.12s, 0.35s;
    }

    /* Subtítulo */
    .isub {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.78rem; color: #ccccff;
        font-weight: 300; letter-spacing: 3px;
        text-transform: uppercase; margin: 16px 0 14px;
    }

    /* Separador */
    .isep {
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%,#7b2fff 30%,#FFD700 50%,#7b2fff 70%,transparent 100%);
        border-radius: 2px; margin: 0 auto;
        width: 78%; opacity: 0.9;
    }

    /* === ZONA BOTONES + FOOTER === */
    .bzone {
        background: rgba(18,4,52,0.93);
        border: 1.5px solid rgba(123,47,255,0.52);
        border-top: none;
        border-radius: 0 0 24px 24px;
        padding: 18px 26px 26px;
        width: 100%;
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        animation: pglow 4s ease-in-out infinite;
        position: relative; z-index: 2;
    }

    /* Helper */
    .ihelper {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.68rem;
        color: rgba(167,139,250,0.38);
        letter-spacing: 1.5px; text-transform: uppercase;
        text-align: center; margin: 0 0 14px;
    }

    /* Botón primario dorado */
    .bprimary .stButton button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important; font-weight: 700 !important;
        letter-spacing: 2px !important; text-transform: uppercase !important;
        border-radius: 12px !important; padding: 0.70rem 2rem !important;
        width: 100% !important;
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #12003e !important; border: none !important;
        box-shadow: 0 4px 24px rgba(255,215,0,0.42) !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important; position: relative !important;
        overflow: hidden !important;
    }
    .bprimary .stButton button::after {
        content: ''; position: absolute; top: 0; left: -80%;
        width: 50%; height: 100%;
        background: linear-gradient(90deg,
            transparent,rgba(255,255,255,0.40),transparent);
        transform: skewX(-20deg);
        animation: shine 2.4s ease-in-out infinite;
    }
    .bprimary .stButton button:hover {
        background: linear-gradient(135deg, #FFE44D, #FFB733) !important;
        box-shadow: 0 6px 38px rgba(255,215,0,0.68) !important;
        transform: translateY(-3px) !important;
    }

    /* Botón secundario púrpura */
    .bsecondary .stButton button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important; font-weight: 700 !important;
        letter-spacing: 2px !important; text-transform: uppercase !important;
        border-radius: 12px !important; padding: 0.70rem 2rem !important;
        width: 100% !important;
        background: transparent !important; color: #c4b5fd !important;
        border: 1.5px solid #7b2fff !important;
        box-shadow: 0 0 14px rgba(123,47,255,0.26) !important;
        transition: all 0.25s ease !important; cursor: pointer !important;
    }
    .bsecondary .stButton button:hover {
        background: linear-gradient(135deg,
            rgba(123,47,255,0.24),rgba(99,102,241,0.20)) !important;
        border-color: #a78bfa !important; color: #ffffff !important;
        box-shadow: 0 0 34px rgba(123,47,255,0.62),
                    0 0 65px rgba(123,47,255,0.30) !important;
        transform: translateY(-3px) !important;
    }

    /* Footer */
    .ifooter {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.63rem; color: rgba(167,139,250,0.28);
        letter-spacing: 1.5px; text-transform: uppercase;
        text-align: center; margin-top: 18px; margin-bottom: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Canvas estrellas ──────────────────────────────────────────────────────
    components.html("""
    <style>
        body{margin:0;padding:0;background:transparent;}
        #sf{position:fixed;top:0;left:0;width:100vw;height:100vh;
            z-index:-1;pointer-events:none;}
    </style>
    <canvas id="sf"></canvas>
    <script>
    (function(){
        const c=document.getElementById('sf'),ctx=c.getContext('2d');
        c.width=window.innerWidth;c.height=window.innerHeight;
        const COL=['#ffffff','#c4b5fd','#a78bfa','#818cf8','#e0d7ff'];
        const S=Array.from({length:200},()=>({
            x:Math.random()*c.width,y:Math.random()*c.height,
            r:Math.random()*1.7+0.2,a:Math.random()*0.6+0.2,
            da:(Math.random()*0.013+0.004)*(Math.random()<.5?1:-1),
            dx:(Math.random()-.5)*.2,dy:(Math.random()-.5)*.14,
            col:COL[Math.floor(Math.random()*COL.length)]
        }));
        function draw(){
            ctx.clearRect(0,0,c.width,c.height);
            S.forEach(s=>{
                s.x+=s.dx;s.y+=s.dy;s.a+=s.da;
                if(s.a>.95||s.a<.1)s.da*=-1;
                if(s.x<0)s.x=c.width;if(s.x>c.width)s.x=0;
                if(s.y<0)s.y=c.height;if(s.y>c.height)s.y=0;
                ctx.save();ctx.globalAlpha=s.a;
                ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
                ctx.fillStyle=s.col;ctx.shadowColor=s.col;
                ctx.shadowBlur=s.r*5;ctx.fill();ctx.restore();
            });
            requestAnimationFrame(draw);
        }
        draw();
        window.addEventListener('resize',()=>{
            c.width=window.innerWidth;c.height=window.innerHeight;
        });
    })();
    </script>
    """, height=0, scrolling=False)

    # ── Silueta skyline ───────────────────────────────────────────────────────
    st.markdown("""
    <svg class="city-bg" viewBox="0 0 1440 260"
         xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax slice">
      <defs>
        <linearGradient id="cg" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"   stop-color="#7b2fff" stop-opacity="1"/>
          <stop offset="100%" stop-color="#3b0080" stop-opacity="0.3"/>
        </linearGradient>
      </defs>
      <path fill="url(#cg)" d="
        M0,260 L0,190 L40,190 L40,150 L60,150 L60,120 L75,120 L75,90
        L85,90 L85,70 L92,70 L92,50 L98,50 L98,70 L105,70 L105,90
        L120,90 L120,120 L145,120 L145,95 L158,95 L158,70 L165,70
        L165,45 L170,45 L170,25 L175,25 L175,45 L180,45 L180,70
        L188,70 L188,95 L205,95 L205,70 L215,70 L215,48 L222,48
        L222,28 L228,28 L228,48 L235,48 L235,70 L250,70 L250,95
        L270,95 L270,65 L280,65 L280,45 L290,45 L290,65 L305,65
        L305,90 L325,90 L325,58 L335,58 L335,38 L342,38 L342,18
        L348,18 L348,38 L355,38 L355,58 L370,58 L370,85 L390,85
        L390,58 L400,58 L400,38 L408,38 L408,58 L420,58 L420,85
        L440,85 L440,60 L452,60 L452,40 L460,40 L460,20 L466,20
        L466,5  L472,5  L472,20 L478,20 L478,40 L486,40 L486,60
        L500,60 L500,85 L520,85 L520,60 L530,60 L530,40 L538,40
        L538,60 L550,60 L550,85 L570,85 L570,58 L580,58 L580,38
        L588,38 L588,58 L600,58 L600,82 L620,82 L620,55 L630,55
        L630,35 L637,35 L637,18 L643,18 L643,35 L650,35 L650,55
        L665,55 L665,80 L685,80 L685,55 L695,55 L695,35 L703,35
        L703,55 L715,55 L715,80 L735,80 L735,55 L745,55 L745,35
        L752,35 L752,55 L764,55 L764,80 L784,80 L784,55 L794,55
        L794,35 L801,35 L801,18 L808,18 L808,35 L815,35 L815,55
        L830,55 L830,80 L850,80 L850,55 L860,55 L860,35 L868,35
        L868,55 L880,55 L880,80 L900,80 L900,55 L910,55 L910,35
        L917,35 L917,55 L929,55 L929,80 L949,80 L949,55 L959,55
        L959,35 L967,35 L967,18 L973,18 L973,35 L980,35 L980,55
        L995,55 L995,80 L1015,80 L1015,55 L1025,55 L1025,35
        L1032,35 L1032,55 L1044,55 L1044,80 L1064,80 L1064,55
        L1074,55 L1074,35 L1082,35 L1082,55 L1094,55 L1094,80
        L1114,80 L1114,55 L1124,55 L1124,35 L1131,35 L1131,18
        L1138,18 L1138,35 L1145,35 L1145,55 L1160,55 L1160,80
        L1180,80 L1180,55 L1190,55 L1190,35 L1198,35 L1198,55
        L1210,55 L1210,80 L1230,80 L1230,55 L1240,55 L1240,35
        L1248,35 L1248,55 L1260,55 L1260,80 L1280,80 L1280,55
        L1290,55 L1290,35 L1297,35 L1297,55 L1309,55 L1309,80
        L1329,80 L1329,55 L1339,55 L1339,35 L1347,35 L1347,18
        L1353,18 L1353,35 L1360,35 L1360,55 L1375,55 L1375,80
        L1395,80 L1395,55 L1410,55 L1410,80 L1440,80 L1440,260 Z"/>
      <g fill="#FFD700" opacity="0.55">
        <rect x="170" y="28"  width="3" height="4"/>
        <rect x="342" y="22"  width="3" height="4"/>
        <rect x="466" y="9"   width="3" height="4"/>
        <rect x="637" y="22"  width="3" height="4"/>
        <rect x="801" y="22"  width="3" height="4"/>
        <rect x="967" y="22"  width="3" height="4"/>
        <rect x="1131" y="22" width="3" height="4"/>
        <rect x="1347" y="22" width="3" height="4"/>
      </g>
    </svg>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PANEL SUPERIOR — ícono + badge + título + subtítulo + separador
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="ip">
        <span class="cicon">🏙️</span>
        <div class="ibadge">🌐 Pensamiento Sistémico 🌐</div>
        <h1 class="ititle">
            <span class="tl1">CIUDAD EN</span>
            <span class="tl2">EQUILIBRIO</span>
        </h1>
        <p class="isub">Gestiona tu ciudad · Salva el futuro</p>
        <div class="isep"></div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ZONA INFERIOR — helper + botones + footer (continúa el panel)
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown('<div class="bzone">', unsafe_allow_html=True)

    st.markdown(
        '<p class="ihelper">⬇ Selecciona una opción para continuar ⬇</p>',
        unsafe_allow_html=True)

    st.markdown('<div class="bprimary">', unsafe_allow_html=True)
    if st.button("🔐  INICIAR SESIÓN", key="btn_login", use_container_width=True):
        navegar("login")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="bsecondary">', unsafe_allow_html=True)
    if st.button("📝  REGISTRAR GRUPO", key="btn_registro", use_container_width=True):
        navegar("registro")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        "<p class='ifooter'>⚡ Ciudad en Equilibrio · v2.0 · 2026 ⚡</p>",
        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # cierra .bzone


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA INSTRUCCIONES  (requerida por router.py)
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_instrucciones():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap');
    #MainMenu, footer, header { visibility: hidden; }
    html, body, [data-testid="stAppViewContainer"] { background: #0d0025 !important; }
    .inst-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(0.62rem, 2vw, 0.88rem);
        color: #fff; text-shadow: 0 0 20px #7b2fff99;
        text-align: center; margin-bottom: 26px; line-height: 1.9;
    }
    .inst-card {
        background: rgba(18,4,52,0.88);
        border: 1px solid rgba(123,47,255,0.36);
        border-radius: 16px; padding: 16px 20px;
        margin-bottom: 11px; backdrop-filter: blur(16px);
    }
    .inst-card-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.93rem; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: #FFD700; margin: 0 0 9px;
    }
    .inst-item {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.84rem; color: #c4b5fd;
        line-height: 1.72; margin: 3px 0; padding-left: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 3, 1])
    with col:
        st.markdown('<h1 class="inst-title">📖 INSTRUCCIONES</h1>',
                    unsafe_allow_html=True)
        secciones = [
            ("🏙️ Objetivo",
             ["Administra la ciudad durante <b>10 rondas</b> manteniendo los 4 indicadores en equilibrio.",
              "Si cualquier indicador llega a <b>0</b>, la ciudad colapsa.",
              "Gana completando las 10 rondas sin colapso."]),
            ("📊 Los 4 Indicadores",
             ["💰 <b>Economía</b> — Finanzas y desarrollo",
              "🌿 <b>Medio Ambiente</b> — Salud ecológica",
              "⚡ <b>Energía</b> — Suministro energético",
              "❤️ <b>Bienestar Social</b> — Calidad de vida"]),
            ("🔄 Flujo de cada Ronda",
             ["1️⃣ Elige una <b>decisión de ciudad</b>",
              "2️⃣ Responde una <b>pregunta académica</b> en 30 s",
              "✅ Acierto → efectos de la decisión aplicados",
              "❌ Fallo → penalización según dificultad",
              "3️⃣ Ocurre un <b>evento aleatorio</b>"]),
            ("⚙️ Dificultades",
             ["🟢 <b>Fácil</b> — Penalización baja",
              "🟡 <b>Normal</b> — Balance equilibrado",
              "🔴 <b>Difícil</b> — Penalización alta"]),
            ("💡 Consejos",
             ["Mantén todos los indicadores &gt; 30 para evitar colapso.",
              "Verde (&gt; 60) = estable · Amarillo (30–60) = vigilar.",
              "Coordina las decisiones del grupo."]),
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
        if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
            navegar("lobby")
