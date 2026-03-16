import streamlit as st


def inyectar_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Exo+2:wght@300;400;600;700;800&family=Rajdhani:wght@400;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; }

/* ══ FONDO: grid digital + partículas ══ */
.stApp {
    background-color: #050a14;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px),
        radial-gradient(ellipse at 15% 40%, rgba(59,130,246,0.08) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 20%, rgba(139,92,246,0.09) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 90%, rgba(6,182,212,0.06) 0%, transparent 50%);
    background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%, 100% 100%;
    min-height: 100vh;
}

#MainMenu, header, footer { visibility: hidden; }
.block-container {
    padding-top: 1rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    max-width: 1500px !important;
}

/* ══ TARJETAS ══ */
.card {
    background: rgba(5,10,20,0.9);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
    transition: border-color .3s, box-shadow .3s;
}
.card::before {
    content:''; position:absolute; inset:0; border-radius:12px;
    background: linear-gradient(135deg, rgba(0,212,255,0.04), transparent 60%);
    pointer-events:none;
}
.card:hover {
    border-color: rgba(0,212,255,0.45);
    box-shadow: 0 0 28px rgba(0,212,255,0.1), inset 0 1px 0 rgba(0,212,255,0.08);
}

.card-glow {
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.12));
    border: 1px solid rgba(139,92,246,0.5);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    box-shadow: 0 0 30px rgba(139,92,246,0.15), inset 0 1px 0 rgba(255,255,255,0.04);
    animation: fadeInUp .4s ease;
    position: relative; overflow: hidden;
}

.card-danger {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    box-shadow: 0 0 20px rgba(239,68,68,0.08);
}
.card-success {
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    box-shadow: 0 0 20px rgba(34,197,94,0.08);
}

/* ══ TÍTULO PRINCIPAL ══ */
.game-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.5rem, 5vw, 3rem);
    font-weight: 900;
    background: linear-gradient(90deg, #00d4ff, #8b5cf6, #22c55e, #00d4ff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    line-height: 1.15;
    animation: shimmer 4s linear infinite;
    filter: drop-shadow(0 0 20px rgba(0,212,255,0.4));
    letter-spacing: 2px;
}
.game-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(0.65rem, 1.8vw, 0.88rem);
    color: rgba(0,212,255,0.5);
    text-align: center;
    letter-spacing: clamp(3px, 0.8vw, 6px);
    text-transform: uppercase;
    margin-bottom: 2rem;
}
@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 300% center; }
}

/* ══ BOTONES NEÓN ══ */
div.stButton > button {
    font-family: 'Exo 2', sans-serif !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: clamp(0.8rem, 2vw, 0.92rem) !important;
    padding: clamp(0.5rem,1.5vw,0.7rem) clamp(0.8rem,2vw,1.4rem) !important;
    transition: all 0.22s ease !important;
    border: 1px solid rgba(0,212,255,0.35) !important;
    background: rgba(5,10,20,0.95) !important;
    color: #94d8e8 !important;
    width: 100% !important;
    white-space: normal !important;
    position: relative !important;
    overflow: hidden !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}
div.stButton > button::after {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.15), transparent);
    transition: left 0.5s ease;
}
div.stButton > button:hover:not(:disabled)::after { left: 150%; }
div.stButton > button:hover:not(:disabled) {
    background: rgba(0,212,255,0.1) !important;
    border-color: #00d4ff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 24px rgba(0,212,255,0.3), 0 0 8px rgba(0,212,255,0.2) inset !important;
    color: #fff !important;
}
div.stButton > button:active:not(:disabled) {
    transform: translateY(0px) scale(0.97) !important;
    box-shadow: 0 0 40px rgba(0,212,255,0.4) !important;
}
div.stButton > button:disabled {
    opacity: 0.2 !important;
    cursor: not-allowed !important;
}

/* ══ INPUTS ══ */
div[data-baseweb="base-input"] > input,
div[data-baseweb="input"] > div {
    background: rgba(5,10,20,0.95) !important;
    border-color: rgba(0,212,255,0.25) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Exo 2', sans-serif !important;
}
div[data-baseweb="base-input"] > input:focus {
    border-color: rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1), 0 0 16px rgba(0,212,255,0.15) !important;
}

/* ══ RADIO BUTTONS ══ */
div[data-testid="stRadio"] > div { gap: 6px !important; }
div[data-testid="stRadio"] label {
    background: rgba(5,10,20,0.9);
    border: 1.5px solid rgba(0,212,255,0.18);
    border-radius: 8px;
    padding: clamp(10px,2vw,13px) clamp(12px,3vw,16px);
    margin: 0 !important;
    display: flex !important;
    cursor: pointer;
    transition: all 0.18s;
    color: #94d8e8;
    font-size: clamp(0.85rem, 2vw, 0.95rem);
    align-items: center; gap: 10px;
    font-family: 'Exo 2', sans-serif;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(0,212,255,0.08);
    border-color: rgba(0,212,255,0.5);
    transform: translateX(4px);
    box-shadow: 0 0 16px rgba(0,212,255,0.15), -3px 0 0 #00d4ff;
    color: #fff;
}

/* ══ MÉTRICAS ══ */
div[data-testid="metric-container"] {
    background: rgba(5,10,20,0.92);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 10px;
    padding: clamp(10px,2vw,14px) clamp(12px,2.5vw,18px);
    text-align: center;
    box-shadow: 0 0 20px rgba(0,212,255,0.06);
}
div[data-testid="metric-container"] label {
    color: rgba(0,212,255,0.6) !important;
    font-size: clamp(0.55rem,1.3vw,0.68rem) !important;
    text-transform: uppercase; letter-spacing: 2px;
    font-family: 'Orbitron', sans-serif !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-size: clamp(0.9rem,2.5vw,1.3rem) !important;
    font-weight: 800 !important;
    font-family: 'Orbitron', sans-serif !important;
}

/* ══ PROGRESS BAR ══ */
div[data-testid="stProgressBar"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 4px !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #00d4ff, #8b5cf6) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.5) !important;
    transition: width .6s ease !important;
}

/* ══ ALERTS ══ */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Exo 2', sans-serif !important;
    border-left-width: 3px !important;
}

/* ══ EXPANDER ══ */
details {
    background: rgba(5,10,20,0.9) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 8px !important;
}
details summary { color: #94d8e8 !important; font-family: 'Exo 2', sans-serif !important; }

/* ══ TEXTO ══ */
hr { border-color: rgba(0,212,255,0.1) !important; margin: 1rem 0 !important; }
p, li, .stMarkdown p {
    color: #94a3b8 !important;
    font-size: clamp(0.85rem,2vw,0.95rem) !important;
    font-family: 'Exo 2', sans-serif !important;
}
h1, h2, h3 { color: #e2e8f0 !important; font-family: 'Exo 2', sans-serif !important; }
h3 { font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important; }

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(5,10,20,0.5); }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.4); border-radius: 2px; }

/* ══ ANIMACIONES ══ */
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
@keyframes pulse-neon {
    0%,100% { box-shadow: 0 0 4px rgba(0,212,255,0.4); }
    50%      { box-shadow: 0 0 16px rgba(0,212,255,0.8), 0 0 30px rgba(0,212,255,0.3); }
}
.pulse { animation: pulse-neon 2s infinite; }

/* ══ EMOJI FIX ══ */
.emoji-title {
    font-family: 'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif !important;
    -webkit-text-fill-color: initial !important;
    filter: none !important;
    display: inline-block;
}

/* ══════════════════════════════════
   RESPONSIVE — MULTI-DISPOSITIVO
   ══════════════════════════════════ */

/* ── Tablet (≤ 900px) ── */
@media (max-width: 900px) {
    .block-container {
        padding-left: .8rem !important;
        padding-right: .8rem !important;
    }
    /* Botones más grandes para touch */
    div.stButton > button {
        padding: .65rem 1rem !important;
        font-size: .9rem !important;
    }
    /* Texto base más legible */
    p, li, .stMarkdown p {
        font-size: .95rem !important;
        line-height: 1.6 !important;
    }
    /* Métricas más compactas */
    div[data-testid="metric-container"] {
        padding: 10px 12px !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }
    /* Game title más pequeño */
    .game-title { font-size: clamp(1.1rem,4vw,2rem) !important; }
}

/* ── Móvil (≤ 640px) ── */
@media (max-width: 640px) {
    .block-container {
        padding-left: .4rem !important;
        padding-right: .4rem !important;
        padding-top: .6rem !important;
    }

    /* Forzar columnas Streamlit a stack vertical */
    div[data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
    }

    /* Botones grandes para dedo */
    div.stButton > button {
        padding: .8rem 1rem !important;
        font-size: .88rem !important;
        min-height: 48px !important;
        touch-action: manipulation !important;
    }

    /* Inputs más altos para touch */
    div[data-baseweb="base-input"] > input {
        min-height: 48px !important;
        font-size: 1rem !important;
        padding: .6rem .9rem !important;
    }

    /* Radio options más grandes */
    div[data-testid="stRadio"] label {
        padding: 14px 14px !important;
        font-size: .9rem !important;
        min-height: 50px !important;
    }

    /* Cards con menos padding */
    .card, .card-glow, .card-danger, .card-success {
        padding: 12px !important;
        border-radius: 10px !important;
    }

    /* Título */
    .game-title {
        font-size: clamp(1rem,7vw,1.6rem) !important;
        letter-spacing: 1px !important;
    }
    .game-sub {
        font-size: .65rem !important;
        letter-spacing: 2px !important;
    }

    /* Texto legible */
    p, li, .stMarkdown p {
        font-size: .9rem !important;
        line-height: 1.65 !important;
    }
    h3 { font-size: .95rem !important; }

    /* Métricas compactas */
    div[data-testid="metric-container"] {
        padding: 8px 10px !important;
    }
    div[data-testid="metric-container"] label {
        font-size: .5rem !important;
        letter-spacing: 1px !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: .9rem !important;
    }

    /* Expander más cómodo */
    details summary { padding: 10px !important; font-size: .88rem !important; }

    /* Separadores */
    hr { margin: .6rem 0 !important; }
}

/* ── Pantalla grande (≥ 1280px) ── */
@media (min-width: 1280px) {
    .block-container { max-width: 1500px !important; }
    .game-title { font-size: 2.8rem !important; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
}
</style>
""", unsafe_allow_html=True)
