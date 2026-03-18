import streamlit as st
from session_manager import navegar


def pantalla_inicio():

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Rajdhani:wght@300;400;600&display=swap');

    #MainMenu, footer, header { visibility: hidden; }

    html, body, [data-testid="stAppViewContainer"] {
        background: #12003e !important;
        overflow-x: hidden;
    }

    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            radial-gradient(1px 1px at 10% 15%, #fff 0%, transparent 100%),
            radial-gradient(1px 1px at 25% 60%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1.5px 1.5px at 40% 30%, #fff 0%, transparent 100%),
            radial-gradient(1px 1px at 55% 75%, #a78bfa 0%, transparent 100%),
            radial-gradient(1px 1px at 70% 20%, #fff 0%, transparent 100%),
            radial-gradient(2px 2px at 80% 55%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 90% 40%, #fff 0%, transparent 100%),
            radial-gradient(1px 1px at 15% 85%, #a78bfa 0%, transparent 100%),
            radial-gradient(1.5px 1.5px at 60% 10%, #fff 0%, transparent 100%),
            radial-gradient(1px 1px at 35% 90%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 5%  50%, #fff 0%, transparent 100%),
            radial-gradient(1px 1px at 75% 80%, #a78bfa 0%, transparent 100%),
            radial-gradient(2px 2px at 48% 48%, #fff 0%, transparent 100%),
            radial-gradient(1px 1px at 92% 12%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 20% 35%, #fff 0%, transparent 100%),
            radial-gradient(1.5px 1.5px at 65% 65%, #a78bfa 0%, transparent 100%),
            radial-gradient(1px 1px at 85% 90%, #fff 0%, transparent 100%),
            radial-gradient(1px 1px at 30% 70%, #c4b5fd 0%, transparent 100%),
            radial-gradient(1px 1px at 50% 25%, #fff 0%, transparent 100%),
            radial-gradient(2px 2px at 8%  78%, #a78bfa 0%, transparent 100%);
        animation: twinkle 6s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }

    [data-testid="stAppViewContainer"]::after {
        content: '';
        position: fixed;
        inset: 0;
        background:
            radial-gradient(ellipse 60% 40% at 20% 30%, rgba(123,47,255,0.18) 0%, transparent 70%),
            radial-gradient(ellipse 50% 60% at 80% 70%, rgba(99,102,241,0.14) 0%, transparent 70%),
            radial-gradient(ellipse 40% 30% at 50% 90%, rgba(167,139,250,0.10) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }

    @keyframes twinkle {
        0%   { opacity: 0.4; transform: scale(1); }
        50%  { opacity: 0.9; }
        100% { opacity: 0.5; transform: scale(1.02); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-12px); }
    }

    @keyframes glow-pulse {
        0%, 100% { text-shadow: 0 0 10px #7b2fff88, 0 0 25px #7b2fff44, 2px 2px 0 #3b0082; }
        50%       { text-shadow: 0 0 20px #7b2fffcc, 0 0 50px #7b2fff66, 2px 2px 0 #3b0082, 0 0 80px #a78bfa33; }
    }

    @keyframes shimmer-border {
        0%   { box-shadow: 0 0 15px #7b2fff44, 0 0 40px #7b2fff22; }
        50%  { box-shadow: 0 0 30px #7b2fff88, 0 0 60px #7b2fff44; }
        100% { box-shadow: 0 0 15px #7b2fff44, 0 0 40px #7b2fff22; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        padding: 0 1rem !important;
        max-width: 520px !important;
        margin: 0 auto !important;
        position: relative;
        z-index: 1;
    }

    .inicio-panel {
        background: rgba(30, 10, 74, 0.85);
        border: 1px solid rgba(123, 47, 255, 0.4);
        border-radius: 24px;
        padding: 48px 40px 40px;
        text-align: center;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        animation: shimmer-border 4s ease-in-out infinite, fadeInUp 0.7s ease;
        width: 100%;
        max-width: 480px;
        position: relative;
        z-index: 2;
    }

    .city-icon {
        font-size: 3.8rem;
        display: block;
        margin-bottom: 18px;
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 0 18px #7b2fff99);
    }

    /* ── TÍTULO con Press Start 2P ── */
    .inicio-title {
        font-family: 'Press Start 2P', monospace;
        font-size: clamp(0.85rem, 3vw, 1.15rem);
        font-weight: 400;
        color: #ffffff;
        margin: 0 0 10px;
        line-height: 1.8;
        letter-spacing: 1px;
        animation: glow-pulse 3s ease-in-out infinite;
    }

    .inicio-sub {
        font-family: 'Rajdhani', sans-serif;
        font-size: clamp(0.85rem, 2.5vw, 1rem);
        color: #ccccff;
        font-weight: 300;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 28px;
    }

    .inicio-sep {
        height: 2px;
        background: linear-gradient(90deg,
            transparent 0%, #7b2fff 30%, #FFD700 50%, #7b2fff 70%, transparent 100%);
        border-radius: 2px;
        margin: 0 auto 32px;
        width: 80%;
        opacity: 0.8;
    }

    .inicio-badge {
        display: inline-block;
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #a78bfa;
        background: rgba(123, 47, 255, 0.15);
        border: 1px solid rgba(123, 47, 255, 0.35);
        border-radius: 20px;
        padding: 4px 16px;
        margin-bottom: 22px;
    }

    div.stButton button {
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        width: 100% !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }

    div.stButton:nth-of-type(1) button {
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #12003e !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.35) !important;
    }
    div.stButton:nth-of-type(1) button:hover {
        background: linear-gradient(135deg, #FFE44D, #FFB733) !important;
        box-shadow: 0 6px 30px rgba(255, 215, 0, 0.6) !important;
        transform: translateY(-3px) !important;
    }

    div.stButton:nth-of-type(2) button {
        background: transparent !important;
        color: #c4b5fd !important;
        border: 1.5px solid #7b2fff !important;
        box-shadow: 0 0 12px rgba(123, 47, 255, 0.25) !important;
    }
    div.stButton:nth-of-type(2) button:hover {
        background: rgba(123, 47, 255, 0.18) !important;
        border-color: #a78bfa !important;
        color: #ffffff !important;
        box-shadow: 0 0 24px rgba(123, 47, 255, 0.5) !important;
        transform: translateY(-3px) !important;
    }

    .inicio-footer {
        font-family: 'Rajdhani', sans-serif;
        font-size: 0.7rem;
        color: rgba(167, 139, 250, 0.4);
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="inicio-panel">
        <span class="city-icon">🏙️</span>
        <div class="inicio-badge">✦ Ingeniería Edition ✦</div>
        <h1 class="inicio-title">Ciudad en<br>Equilibrio</h1>
        <p class="inicio-sub">Gestiona tu ciudad. Salva el futuro.</p>
        <div class="inicio-sep"></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔐  INICIAR SESIÓN", use_container_width=True):
        navegar("login")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    if st.button("📝  REGISTRAR GRUPO", use_container_width=True):
        navegar("registro")

    st.markdown("""
    <p class="inicio-footer">⚡ Pensamiento Sistémico · v2.0 ⚡</p>
    """, unsafe_allow_html=True)
