import streamlit as st
import streamlit.components.v1 as components
from session_manager import navegar


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA DE INICIO
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_inicio():

    # ── CSS global ────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap');

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none !important; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #0d0025 !important;
        overflow-x: hidden;
    }

    /* ── Nebulosa ── */
    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 75% 55% at 12% 22%, rgba(123,47,255,0.32) 0%, transparent 62%),
            radial-gradient(ellipse 60% 70% at 88% 78%, rgba(99,102,241,0.26) 0%, transparent 62%),
            radial-gradient(ellipse 50% 38% at 50% 98%, rgba(167,139,250,0.20) 0%, transparent 62%),
            radial-gradient(ellipse 85% 32% at 50% 115%, rgba(123,47,255,0.38) 0%, transparent 58%);
        pointer-events: none;
        z-index: 0;
        animation: nebula-shift 14s ease-in-out infinite alternate;
    }
    @keyframes nebula-shift {
        0%   { opacity: 0.65; transform: scale(1);    }
        100% { opacity: 1.0;  transform: scale(1.06); }
    }

    /* ── Silueta ciudad ── */
    .city-skyline-bg {
        position: fixed;
        bottom: 0; left: 0;
        width: 100%; height: 280px;
        z-index: 0;
        pointer-events: none;
        animation: city-glow 4s ease-in-out infinite alternate;
    }
    @keyframes city-glow {
        0%   { opacity: 0.16;
               filter: drop-shadow(0 -8px 40px rgba(123,47,255,0.38))
                       drop-shadow(0 -2px 15px rgba(255,215,0,0.08)); }
        100% { opacity: 0.32;
               filter: drop-shadow(0 -10px 70px rgba(123,47,255,0.78))
                       drop-shadow(0 -2px 30px rgba(255,215,0,0.30)); }
    }

    /* ── Animaciones ── */
    @keyframes float {
        0%, 100% { transform: translateY(0px) scale(1);      }
        50%       { transform: translateY(-12px) scale(1.06); }
    }
    @keyframes shimmer-border {
        0%, 100% { box-shadow: 0 0 22px #7b2fff44, 0 0 55px #7b2fff20,
                               inset 0 0 22px rgba(123,47,255,0.04); }
        50%       { box-shadow: 0 0 45px #7b2fff99, 0 0 95px #7b2fff55,
                               inset 0 0 40px rgba(123,47,255,0.10); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(34px); }
        to   { opacity: 1; transform: translateY(0);    }
    }
    @keyframes energy-line {
        0%   { left: -100%; width: 60%; }
        100% { left: 110%;  width: 80%; }
    }
    @keyframes btn-shine {
        0%   { left: -80%; }
        100% { left: 130%; }
    }

    /* ── Bounce + Glitch por letra ── */
    @keyframes bounce-letter {
        0%, 100% { transform: translateY(0) scaleY(1);        }
        35%       { transform: translateY(-10px) scaleY(1.12); }
        55%       { transform: translateY(-4px)  scaleY(1.03); }
        70%       { transform: translateY(-7px)  scaleY(1.07); }
    }
    @keyframes glitch-fx {
        0%,  87%, 100% {
            transform: translateX(0) skewX(0deg);
            color: #ffffff;
            text-shadow: 0 0 16px #7b2fff99, 0 0 32px #7b2fff55;
        }
        89% { transform: translateX(-4px) skewX(-9deg);  color: #ff4d6d;
              text-shadow: -3px 0 #00ffff, 3px 0 #ff4d6d; }
        91% { transform: translateX(4px)  skewX(9deg);   color: #00ffff;
              text-shadow: 3px 0 #ff4d6d, -3px 0 #00ffff; }
        93% { transform: translateX(-2px) skewX(-4deg);  color: #ffffff;
              text-shadow: 2px 0 #7b2fff, -2px 0 #FFD700; }
        95% { transform: translateX(0)    skewX(0deg);   color: #ffffff;
              text-shadow: 0 0 16px #7b2fff99, 0 0 32px #7b2fff55; }
    }

    /* ── Layout: centra el panel en pantalla ── */
    .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        padding: 1.5rem 1rem !important;
        max-width: 520px !important;
        margin: 0 auto !important;
        position: relative;
        z-index: 1;
    }

    /* ══════════════════════════════════════════════
       PANEL ÚNICO — contiene TODO: título + botones
       ══════════════════════════════════════════════ */
    .inicio-panel {
        background: rgba(18, 4, 52, 0.92);
        border: 1px solid rgba(123, 47, 255, 0.52);
        border-radius: 24px;           /* redondo en los 4 bordes */
        padding: 40px 32px 32px;
        text-align: center;
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        width: 100%;
        animation: shimmer-border 4s ease-in-out infinite, fadeInUp 0.7s ease;
        position: relative;
        overflow: hidden;
        z-index: 2;
    }
    /* Línea de energía en borde superior */
    .inicio-panel::before {
        content: '';
        position: absolute;
        top: 0; height: 2px;
        background: linear-gradient(90deg,
            transparent, #7b2fff, #FFD700, #00ffff, transparent);
        border-radius: 2px;
        animation: energy-line 2.8s linear infinite;
    }

    /* ── Ícono ciudad ── */
    .city-icon {
        font-size: 3.8rem;
        display: block;
        margin-bottom: 12px;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 24px #7b2fffcc)
                drop-shadow(0 0 52px #7b2fff88)
                drop-shadow(0 0 10px #FFD70066);
    }

    /* ── Badge ── */
    .inicio-badge {
        display: inline-block;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.70rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #a78bfa;
        background: rgba(123,47,255,0.15);
        border: 1px solid rgba(123,47,255,0.42);
        border-radius: 20px;
        padding: 5px 16px;
        margin-bottom: 18px;
    }

    /* ── Título pixel animado ── */
    .inicio-title {
        font-family: 'Press Start 2P', monospace;
        /* Tamaño que cabe en el panel sin romperse */
        font-size: clamp(0.7rem, 3.5vw, 1.05rem);
        font-weight: 400;
        color: #ffffff;
        margin: 0 0 6px;
        line-height: 1.9;
        /* Cada palabra en su línea, sin cortes arbitrarios */
        white-space: pre-line;
        word-break: keep-all;
        overflow-wrap: normal;
    }
    /* Línea 1: CIUDAD EN  — línea 2: EQUILIBRIO */
    .titulo-l1, .titulo-l2 {
        display: block;
        white-space: nowrap;
    }
    .inicio-title span {
        display: inline-block;
        animation:
            bounce-letter 2s    ease-in-out infinite,
            glitch-fx     6.5s  step-end    infinite;
        animation-delay:
            calc(var(--i) * 0.07s),
            calc(var(--i) * 0.05s + 1.8s);
        text-shadow: 0 0 16px #7b2fff99, 0 0 32px #7b2fff55;
    }

    /* ── Subtítulo ── */
    .inicio-sub {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(0.74rem, 2vw, 0.90rem);
        color: #ccccff;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin: 6px 0 18px;
    }

    /* ── Separador ── */
    .inicio-sep {
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%, #7b2fff 30%, #FFD700 50%, #7b2fff 70%, transparent 100%);
        border-radius: 2px;
        margin: 0 auto 16px;
        width: 80%;
        opacity: 0.9;
    }

    /* ── Helper text ── */
    .inicio-helper {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.72rem;
        color: rgba(167,139,250,0.42);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 14px;
    }

    /* ── Botón primario (dorado + shimmer) ── */
    .btn-primary .stButton button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        padding: 0.72rem 2rem !important;
        width: 100% !important;
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #12003e !important;
        border: none !important;
        box-shadow: 0 4px 26px rgba(255,215,0,0.42) !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    .btn-primary .stButton button::after {
        content: '';
        position: absolute;
        top: 0; left: -80%;
        width: 50%; height: 100%;
        background: linear-gradient(90deg,
            transparent, rgba(255,255,255,0.40), transparent);
        transform: skewX(-20deg);
        animation: btn-shine 2.4s ease-in-out infinite;
    }
    .btn-primary .stButton button:hover {
        background: linear-gradient(135deg, #FFE44D, #FFB733) !important;
        box-shadow: 0 6px 40px rgba(255,215,0,0.70) !important;
        transform: translateY(-3px) !important;
    }

    /* ── Botón secundario (púrpura) ── */
    .btn-secondary .stButton button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        padding: 0.72rem 2rem !important;
        width: 100% !important;
        background: transparent !important;
        color: #c4b5fd !important;
        border: 1.5px solid #7b2fff !important;
        box-shadow: 0 0 16px rgba(123,47,255,0.28) !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }
    .btn-secondary .stButton button:hover {
        background: linear-gradient(135deg,
            rgba(123,47,255,0.26), rgba(99,102,241,0.22)) !important;
        border-color: #a78bfa !important;
        color: #ffffff !important;
        box-shadow: 0 0 36px rgba(123,47,255,0.66),
                    0 0 68px rgba(123,47,255,0.32) !important;
        transform: translateY(-3px) !important;
    }

    /* ── Footer dentro del panel ── */
    .inicio-footer {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.66rem;
        color: rgba(167,139,250,0.34);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Canvas: estrellas animadas ────────────────────────────────────────────
    components.html("""
    <style>
        body { margin:0; padding:0; background:transparent; }
        #starfield {
            position: fixed; top:0; left:0;
            width:100vw; height:100vh;
            z-index: -1; pointer-events: none;
        }
    </style>
    <canvas id="starfield"></canvas>
    <script>
    (function(){
        const c = document.getElementById('starfield');
        const ctx = c.getContext('2d');
        c.width = window.innerWidth; c.height = window.innerHeight;
        const COLORS = ['#ffffff','#c4b5fd','#a78bfa','#818cf8','#e0d7ff','#FFD70033'];
        const stars = Array.from({length:210}, () => ({
            x: Math.random()*c.width, y: Math.random()*c.height,
            r: Math.random()*1.8+0.22, alpha: Math.random()*0.65+0.2,
            da: (Math.random()*0.014+0.004)*(Math.random()<0.5?1:-1),
            dx: (Math.random()-0.5)*0.22, dy: (Math.random()-0.5)*0.15,
            color: COLORS[Math.floor(Math.random()*COLORS.length)]
        }));
        function frame(){
            ctx.clearRect(0,0,c.width,c.height);
            stars.forEach(s=>{
                s.x+=s.dx; s.y+=s.dy; s.alpha+=s.da;
                if(s.alpha>0.95||s.alpha<0.1) s.da*=-1;
                if(s.x<0) s.x=c.width; if(s.x>c.width) s.x=0;
                if(s.y<0) s.y=c.height; if(s.y>c.height) s.y=0;
                ctx.save(); ctx.globalAlpha=s.alpha;
                ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
                ctx.fillStyle=s.color; ctx.shadowColor=s.color;
                ctx.shadowBlur=s.r*5; ctx.fill(); ctx.restore();
            });
            requestAnimationFrame(frame);
        }
        frame();
        window.addEventListener('resize',()=>{c.width=window.innerWidth;c.height=window.innerHeight;});
    })();
    </script>
    """, height=0, scrolling=False)

    # ── Silueta SVG skyline ───────────────────────────────────────────────────
    st.markdown("""
    <svg class="city-skyline-bg" viewBox="0 0 1440 280"
         xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMax slice">
      <defs>
        <linearGradient id="cg" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"   stop-color="#7b2fff" stop-opacity="1"/>
          <stop offset="100%" stop-color="#3b0080" stop-opacity="0.3"/>
        </linearGradient>
      </defs>
      <path fill="url(#cg)" d="
        M0,280 L0,200 L30,200 L30,160 L50,160 L50,140 L70,140 L70,100
        L80,100 L80,80 L90,80 L90,60 L95,60 L95,80 L100,80 L100,100
        L110,100 L110,130 L130,130 L130,110 L145,110 L145,90 L155,90
        L155,70 L160,70 L160,50 L165,50 L165,30 L170,30 L170,50
        L175,50 L175,70 L180,70 L180,90 L195,90 L195,110 L210,110
        L210,80 L220,80 L220,60 L230,60 L230,40 L235,40 L235,20
        L240,20 L240,40 L245,40 L245,60 L255,60 L255,80 L270,80
        L270,100 L290,100 L290,70 L300,70 L300,50 L310,50 L310,70
        L320,70 L320,90 L340,90 L340,60 L350,60 L350,40 L360,40
        L360,55 L370,55 L370,75 L390,75 L390,95 L410,95 L410,65
        L420,65 L420,45 L430,45 L430,25 L435,25 L435,10 L440,10
        L440,25 L445,25 L445,45 L455,45 L455,65 L470,65 L470,90
        L490,90 L490,110 L510,110 L510,80 L520,80 L520,55 L530,55
        L530,35 L535,35 L535,55 L545,55 L545,75 L560,75 L560,100
        L580,100 L580,70 L590,70 L590,50 L600,50 L600,70 L610,70
        L610,90 L630,90 L630,60 L640,60 L640,40 L650,40 L650,20
        L655,20 L655,5 L660,5 L660,20 L665,20 L665,40 L675,40
        L675,60 L690,60 L690,85 L710,85 L710,105 L730,105 L730,75
        L740,75 L740,55 L750,55 L750,75 L760,75 L760,95 L780,95
        L780,65 L790,65 L790,45 L800,45 L800,65 L815,65 L815,85
        L835,85 L835,55 L845,55 L845,35 L855,35 L855,55 L865,55
        L865,75 L885,75 L885,95 L905,95 L905,65 L915,65 L915,45
        L925,45 L925,65 L935,65 L935,85 L955,85 L955,110 L975,110
        L975,80 L985,80 L985,55 L995,55 L995,35 L1000,35 L1000,20
        L1005,20 L1005,35 L1010,35 L1010,55 L1020,55 L1020,80
        L1040,80 L1040,100 L1060,100 L1060,70 L1070,70 L1070,50
        L1080,50 L1080,70 L1090,70 L1090,90 L1110,90 L1110,60
        L1120,60 L1120,40 L1130,40 L1130,60 L1145,60 L1145,80
        L1165,80 L1165,100 L1185,100 L1185,70 L1195,70 L1195,50
        L1205,50 L1205,70 L1220,70 L1220,90 L1240,90 L1240,60
        L1250,60 L1250,40 L1260,40 L1260,20 L1265,20 L1265,40
        L1275,40 L1275,60 L1290,60 L1290,85 L1310,85 L1310,105
        L1330,105 L1330,75 L1340,75 L1340,55 L1355,55 L1355,75
        L1370,75 L1370,95 L1390,95 L1390,65 L1410,65 L1410,85
        L1440,85 L1440,280 Z"/>
      <g fill="#FFD700" opacity="0.65">
        <rect x="165" y="34" width="3" height="4"/>
        <rect x="237" y="24" width="3" height="4"/>
        <rect x="432" y="14" width="3" height="4"/>
        <rect x="657" y="9"  width="3" height="4"/>
        <rect x="1002" y="24" width="3" height="4"/>
        <rect x="1262" y="24" width="3" height="4"/>
      </g>
    </svg>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # PANEL ÚNICO: título + separador + helper + botones + footer
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="inicio-panel">

        <!-- Ícono -->
        <span class="city-icon">🏙️</span>

        <!-- Badge -->
        <div class="inicio-badge">🌐 Pensamiento Sistémico 🌐</div>

        <!-- Título animado: CIUDAD EN / EQUILIBRIO en dos líneas limpias -->
        <h1 class="inicio-title">
            <span class="titulo-l1">
                <span style="--i:0">C</span><span style="--i:1">I</span><span style="--i:2">U</span><span style="--i:3">D</span><span style="--i:4">A</span><span style="--i:5">D</span>&nbsp;<span style="--i:6">E</span><span style="--i:7">N</span>
            </span>
            <span class="titulo-l2">
                <span style="--i:8">E</span><span style="--i:9">Q</span><span style="--i:10">U</span><span style="--i:11">I</span><span style="--i:12">L</span><span style="--i:13">I</span><span style="--i:14">B</span><span style="--i:15">R</span><span style="--i:16">I</span><span style="--i:17">O</span>
            </span>
        </h1>

        <!-- Subtítulo -->
        <p class="inicio-sub">Gestiona tu ciudad · Salva el futuro</p>

        <!-- Separador -->
        <div class="inicio-sep"></div>

        <!-- Helper -->
        <p class="inicio-helper">⬇ Selecciona una opción para continuar ⬇</p>

    </div>
    """, unsafe_allow_html=True)

    # ── Botones dentro del panel (Streamlit los renderiza fuera del HTML,
    #    pero los envolvemos en divs que continúan visualmente el panel) ───────
    st.markdown("""
    <style>
    /* Zona botones: continúa el panel sin borde superior */
    .btn-zone {
        background: rgba(18, 4, 52, 0.92);
        border: 1px solid rgba(123,47,255,0.52);
        border-top: none;
        border-radius: 0 0 24px 24px;
        padding: 6px 32px 28px;
        width: 100%;
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        position: relative;
        z-index: 2;
    }
    </style>
    <div class="btn-zone" id="btn-zone-start"></div>
    """, unsafe_allow_html=True)

    # Contenedor visual del panel inferior
    st.markdown('<div class="btn-zone">', unsafe_allow_html=True)

    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("🔐  INICIAR SESIÓN", key="btn_login", use_container_width=True):
        navegar("login")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("📝  REGISTRAR GRUPO", key="btn_registro", use_container_width=True):
        navegar("registro")
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer dentro del panel
    st.markdown(
        "<p class='inicio-footer' id='footer-año'>⚡ Ciudad en Equilibrio · v2.0 ⚡</p>",
        unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # cierra .btn-zone

    # Año dinámico vía JS
    components.html("""
    <script>
    (function(){
        // Espera a que el DOM de Streamlit esté listo e inyecta el año
        function setYear(){
            const el = window.parent.document.getElementById('footer-año');
            if(el){
                el.textContent = '⚡ Ciudad en Equilibrio · v2.0 · '
                                 + new Date().getFullYear() + ' ⚡';
            }
        }
        setTimeout(setYear, 600);
    })();
    </script>
    """, height=0, scrolling=False)


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA DE INSTRUCCIONES
#  Requerida por router.py — se accede desde el Lobby, NO desde el inicio.
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_instrucciones():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap');
    #MainMenu, footer, header { visibility: hidden; }
    html, body, [data-testid="stAppViewContainer"] { background: #0d0025 !important; }
    .inst-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(0.65rem, 2vw, 0.9rem);
        color: #ffffff;
        text-shadow: 0 0 20px #7b2fff99;
        text-align: center;
        margin-bottom: 28px; line-height: 1.9;
    }
    .inst-card {
        background: rgba(18,4,52,0.88);
        border: 1px solid rgba(123,47,255,0.38);
        border-radius: 16px; padding: 18px 22px;
        margin-bottom: 12px; backdrop-filter: blur(16px);
    }
    .inst-card-title {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.95rem; font-weight: 700;
        letter-spacing: 2px; text-transform: uppercase;
        color: #FFD700; margin: 0 0 10px;
    }
    .inst-item {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.86rem; color: #c4b5fd;
        line-height: 1.75; margin: 3px 0; padding-left: 8px;
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
              "Si cualquier indicador llega a <b>0</b>, la ciudad colapsa y pierdes.",
              "Gana completando las 10 rondas sin colapso."]),
            ("📊 Los 4 Indicadores",
             ["💰 <b>Economía</b> — Finanzas y desarrollo económico",
              "🌿 <b>Medio Ambiente</b> — Salud ecológica de la ciudad",
              "⚡ <b>Energía</b> — Suministro y sostenibilidad energética",
              "❤️ <b>Bienestar Social</b> — Calidad de vida de los ciudadanos"]),
            ("🔄 Flujo de cada Ronda",
             ["1️⃣ El estudiante en turno elige una <b>decisión de ciudad</b>",
              "2️⃣ Responde una <b>pregunta académica</b> en 30 segundos",
              "✅ Acierto: se aplican los efectos de la decisión",
              "❌ Fallo: penalización según la dificultad seleccionada",
              "3️⃣ Ocurre un <b>evento aleatorio</b> que afecta los indicadores"]),
            ("⚙️ Dificultades",
             ["🟢 <b>Fácil</b> — Penalización baja · eventos más favorables",
              "🟡 <b>Normal</b> — Balance equilibrado de retos",
              "🔴 <b>Difícil</b> — Penalización alta · más eventos negativos"]),
            ("⭐ Estrellas y Logros",
             ["Gana estrellas al completar partidas y misiones.",
              "Úsalas para activar atributos especiales durante el juego.",
              "Desbloquea logros cumpliendo objetivos específicos."]),
            ("💡 Consejos",
             ["Mantén todos los indicadores por encima de <b>30</b> para evitar colapso.",
              "Indicadores verdes (&gt; 60) = estables · amarillos (30–60) = vigilar.",
              "Coordina las decisiones del grupo para mantener el equilibrio."]),
        ]

        for titulo, items in secciones:
            items_html = "".join(
                f"<div class='inst-item'>• {i}</div>" for i in items)
            st.markdown(
                f"<div class='inst-card'>"
                f"<div class='inst-card-title'>{titulo}</div>"
                f"{items_html}"
                f"</div>",
                unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
            navegar("lobby")
