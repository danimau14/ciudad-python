import streamlit as st
from session_manager import navegar


def pantalla_inicio():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600;700&display=swap');

    #MainMenu, footer, header { visibility: hidden; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #12003e !important;
        overflow-x: hidden;
    }

    /* ── Estrellas capa 1 (pequeñas, rápidas) ── */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(1px 1px at  5% 12%, #ffffff 0%, transparent 100%),
            radial-gradient(1px 1px at 18% 40%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 30% 72%, #ffffff 0%, transparent 100%),
            radial-gradient(1px 1px at 42%  8%, #a78bfa 0%, transparent 100%),
            radial-gradient(1px 1px at 58% 55%, #ffffff 0%, transparent 100%),
            radial-gradient(1px 1px at 67% 25%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 78% 80%, #ffffff 0%, transparent 100%),
            radial-gradient(1px 1px at 88% 47%, #a78bfa 0%, transparent 100%),
            radial-gradient(1px 1px at 95% 90%, #ffffff 0%, transparent 100%),
            radial-gradient(1px 1px at 12% 95%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 50% 33%, #ffffff 0%, transparent 100%),
            radial-gradient(1px 1px at 23% 58%, #a78bfa 0%, transparent 100%),
            radial-gradient(1px 1px at 71%  5%, #ffffff 0%, transparent 100%),
            radial-gradient(1px 1px at 85% 18%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 37% 85%, #ffffff 0%, transparent 100%);
        animation: twinkle1 5s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Estrellas capa 2 (grandes, lentas) + nebulosa ── */
    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(2px 2px at 15% 28%, #ffffff 0%, transparent 100%),
            radial-gradient(2px 2px at 44% 62%, #e9d5ff 0%, transparent 100%),
            radial-gradient(2px 2px at 72% 38%, #ffffff 0%, transparent 100%),
            radial-gradient(2px 2px at 90% 72%, #c4b5fd 0%, transparent 100%),
            radial-gradient(2px 2px at 33% 15%, #ffffff 0%, transparent 100%),
            radial-gradient(2px 2px at 60% 88%, #e9d5ff 0%, transparent 100%),
            radial-gradient(2px 2px at  8% 65%, #ffffff 0%, transparent 100%),
            /* nebulosa */
            radial-gradient(ellipse 55% 35% at 20% 25%, rgba(123,47,255,0.20) 0%, transparent 70%),
            radial-gradient(ellipse 45% 55% at 80% 70%, rgba(99,102,241,0.15) 0%, transparent 70%),
            radial-gradient(ellipse 35% 25% at 55% 95%, rgba(167,139,250,0.12) 0%, transparent 70%);
        animation: twinkle2 8s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    @keyframes twinkle1 {
        0%   { opacity: 0.35; transform: scale(1); }
        100% { opacity: 1;    transform: scale(1.03); }
    }
    @keyframes twinkle2 {
        0%   { opacity: 0.5; }
        100% { opacity: 1; }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) scale(1); }
        50%       { transform: translateY(-14px) scale(1.06); }
    }

    @keyframes glow-pulse {
        0%, 100% {
            text-shadow:
                0 0 10px rgba(123,47,255,0.6),
                0 0 25px rgba(123,47,255,0.3),
                3px 3px 0 #2d006e;
        }
        50% {
            text-shadow:
                0 0 22px rgba(123,47,255,0.9),
                0 0 55px rgba(167,139,250,0.5),
                0 0 90px rgba(123,47,255,0.2),
                3px 3px 0 #2d006e;
        }
    }

    @keyframes border-glow {
        0%, 100% { box-shadow: 0 0 18px rgba(123,47,255,0.35), 0 0 50px rgba(123,47,255,0.15), inset 0 0 30px rgba(123,47,255,0.04); }
        50%       { box-shadow: 0 0 35px rgba(123,47,255,0.6),  0 0 80px rgba(123,47,255,0.25), inset 0 0 40px rgba(123,47,255,0.07); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(28px); }
        to   { opacity: 1; transform: translateY(0px); }
    }

    @keyframes sep-shimmer {
        0%   { background-position: -200% center; }
        100% { background-position:  200% center; }
    }

    /* ── Layout centrado ── */
    .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        padding: 1rem !important;
        max-width: 500px !important;
        margin: 0 auto !important;
        position: relative;
        z-index: 1;
    }

    /* ── Panel ── */
    .inicio-panel {
        background: rgba(30, 10, 74, 0.88);
        border: 1px solid rgba(123, 47, 255, 0.45);
        border-radius: 28px;
        padding: 50px 44px 44px;
        text-align: center;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        animation: border-glow 4s ease-in-out infinite, fadeInUp 0.65s ease both;
        width: 100%;
        position: relative;
        z-index: 2;
    }

    /* ── Emoji ciudad ── */
    .city-icon {
        font-size: 4rem;
        display: block;
        margin-bottom: 20px;
        animation: float 5s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(123,47,255,0.7));
        line-height: 1;
    }

    /* ── Badge ── */
    .inicio-badge {
        display: inline-block;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #a78bfa;
        background: rgba(123, 47, 255, 0.14);
        border: 1px solid rgba(167, 139, 250, 0.35);
        border-radius: 20px;
        padding: 5px 18px;
        margin-bottom: 22px;
    }

    /* ── Título Press Start 2P ── */
    .inicio-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(0.78rem, 2.8vw, 1.05rem);
        font-weight: 400;
        color: #ffffff;
        margin: 0 0 14px;
        line-height: 2;
        letter-spacing: 1px;
        animation: glow-pulse 3.5s ease-in-out infinite;
    }

    /* ── Subtítulo ── */
    .inicio-sub {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(0.82rem, 2.2vw, 0.98rem);
        color: #ccccff;
        font-weight: 300;
        letter-spacing: 3.5px;
        text-transform: uppercase;
        margin-bottom: 28px;
        opacity: 0.85;
    }

    /* ── Separador animado ── */
    .inicio-sep {
        height: 2px;
        background: linear-gradient(
            90deg,
            transparent    0%,
            #7b2fff       20%,
            #a78bfa       40%,
            #FFD700       50%,
            #a78bfa       60%,
            #7b2fff       80%,
            transparent  100%
        );
        background-size: 200% auto;
        border-radius: 2px;
        margin: 0 auto 34px;
        width: 85%;
        animation: sep-shimmer 3s linear infinite;
    }

    /* ── Botones ── */
    div.stButton button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 2.5px !important;
        text-transform: uppercase !important;
        border-radius: 14px !important;
        padding: 0.72rem 2rem !important;
        width: 100% !important;
        transition: all 0.22s ease !important;
    }

    /* Primario — dorado */
    div.stButton:nth-of-type(1) button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%) !important;
        color: #12003e !important;
        border: none !important;
        box-shadow: 0 4px 22px rgba(255,215,0,0.32) !important;
    }
    div.stButton:nth-of-type(1) button:hover:not(:disabled) {
        background: linear-gradient(135deg, #FFE44D 0%, #FFB733 100%) !important;
        box-shadow: 0 6px 32px rgba(255,215,0,0.62) !important;
        transform: translateY(-3px) scale(1.01) !important;
    }

    /* Secundario — contorno púrpura */
    div.stButton:nth-of-type(2) button {
        background: transparent !important;
        color: #c4b5fd !important;
        border: 1.5px solid #7b2fff !important;
        box-shadow: 0 0 14px rgba(123,47,255,0.22) !important;
    }
    div.stButton:nth-of-type(2) button:hover:not(:disabled) {
        background: rgba(123,47,255,0.2) !important;
        border-color: #c4b5fd !important;
        color: #ffffff !important;
        box-shadow: 0 0 28px rgba(123,47,255,0.55), 0 0 60px rgba(123,47,255,0.2) !important;
        transform: translateY(-3px) scale(1.01) !important;
    }

    /* ── Pie ── */
    .inicio-footer {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.68rem;
        color: rgba(167, 139, 250, 0.38);
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 30px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Panel HTML ─────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="inicio-panel">
        <span class="city-icon">🏙️</span>
        <div class="inicio-badge">✦ Ingeniería Edition ✦</div>
        <h1 class="inicio-title">Ciudad en<br>Equilibrio</h1>
        <p class="inicio-sub">Gestiona tu ciudad. Salva el futuro.</p>
        <div class="inicio-sep"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Botones (lógica intacta) ───────────────────────────────────────────────
    if st.button("🔐  INICIAR SESIÓN", use_container_width=True):
        navegar("login")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if st.button("📝  REGISTRAR GRUPO", use_container_width=True):
        navegar("registro")

    st.markdown('<p class="inicio-footer">⚡ Pensamiento Sistémico · v2.0 ⚡</p>',
                unsafe_allow_html=True)
