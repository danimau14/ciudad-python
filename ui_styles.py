import streamlit as st


def inyectar_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Courier+Prime:wght@400;700&display=swap');

    /* ══════════════════════════════════════════════
       BASE
       ══════════════════════════════════════════════ */
    html, body, [class*="css"] {
        font-family: 'Courier Prime', 'Courier New', Courier, monospace !important;
        background-color: #0a0a0f !important;
        color: #e2e8f0 !important;
    }
    .stApp {
        background-color: #0a0a0f !important;
        background-image:
            linear-gradient(rgba(167,139,250,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(167,139,250,0.03) 1px, transparent 1px);
        background-size: 32px 32px;
    }
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Layout principal responsivo ── */
    .block-container {
        padding: clamp(0.6rem, 2vw, 1.4rem) clamp(0.75rem, 3vw, 2rem) 3rem !important;
        max-width: min(1200px, 100%) !important;
        min-height: 100vh !important;
        margin: 0 auto !important;
        width: 100% !important;
        background: rgba(10, 12, 26, 0.82) !important;
        box-shadow: 0 16px 40px rgba(0,0,0,0.30) !important;
        backdrop-filter: blur(11px) !important;
        border: 1px solid rgba(167,139,250,0.16) !important;
        border-radius: 20px !important;
        overflow-x: hidden !important;
    }

    /* ══════════════════════════════════════════════
       TIPOGRAFÍA
       ══════════════════════════════════════════════ */
    h1, h2, h3, h4 {
        font-family: 'Press Start 2P', 'Courier New', monospace !important;
        letter-spacing: 1px;
    }

    /* ══════════════════════════════════════════════
       EXPANDERS
       ══════════════════════════════════════════════ */
    .streamlit-expanderHeader svg { display: none !important; }
    .streamlit-expanderHeader::before {
        content: '+ ';
        font-family: 'Courier Prime', monospace;
        font-weight: 700;
        color: #a78bfa;
        margin-right: 6px;
    }
    [aria-expanded="true"].streamlit-expanderHeader::before { content: '- '; }

    .streamlit-expanderHeader {
        font-family: 'Courier Prime', 'Courier New', monospace !important;
        font-size: clamp(0.72rem, 2vw, 0.82rem) !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: #94a3b8 !important;
        background: rgba(15,15,25,0.7) !important;
        border: 1px solid rgba(167,139,250,0.15) !important;
        border-radius: 10px !important;
        padding: clamp(8px,2vw,10px) clamp(10px,2vw,16px) !important;
    }
    .streamlit-expanderHeader:hover {
        color: #c4b5fd !important;
        border-color: rgba(167,139,250,0.4) !important;
    }
    .streamlit-expanderContent {
        background: rgba(10,10,20,0.6) !important;
        border: 1px solid rgba(167,139,250,0.1) !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        padding: clamp(10px,2vw,16px) !important;
    }

    /* ══════════════════════════════════════════════
       CARDS
       ══════════════════════════════════════════════ */
    .card {
        background: rgba(15,15,25,0.85);
        border: 1px solid rgba(167,139,250,0.18);
        border-radius: 16px;
        padding: clamp(14px,3vw,20px) clamp(14px,3vw,22px);
        margin-bottom: 12px;
        transition: border-color .25s, box-shadow .25s;
        position: relative;
        overflow: hidden;
    }
    .card:hover {
        border-color: rgba(167,139,250,0.45);
        box-shadow: 0 0 24px rgba(167,139,250,0.12);
    }
    .card-glow {
        background: rgba(15,15,25,0.9);
        border: 1px solid rgba(96,165,250,0.25);
        border-radius: 18px;
        padding: clamp(14px,3vw,22px) clamp(14px,3vw,24px);
        margin-bottom: 14px;
        box-shadow: 0 0 30px rgba(96,165,250,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
    }

    /* ══════════════════════════════════════════════
       BOTONES
       ══════════════════════════════════════════════ */
    .stButton > button {
        font-family: 'Courier Prime', 'Courier New', monospace !important;
        font-weight: 700 !important;
        font-size: clamp(0.72rem, 2vw, 0.82rem) !important;
        letter-spacing: 0.5px !important;
        background: rgba(30,30,50,0.9) !important;
        color: #c4b5fd !important;
        border: 1px solid rgba(167,139,250,0.35) !important;
        border-radius: 10px !important;
        padding: clamp(8px,2vw,10px) clamp(12px,3vw,20px) !important;
        transition: all .2s ease !important;
        text-transform: uppercase !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: rgba(124,58,237,0.25) !important;
        border-color: rgba(167,139,250,0.7) !important;
        color: #ede9fe !important;
        box-shadow: 0 0 18px rgba(167,139,250,0.25) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:disabled { opacity: 0.35 !important; transform: none !important; }

    /* ══════════════════════════════════════════════
       RADIO
       ══════════════════════════════════════════════ */
    .stRadio > div {
        background: rgba(15,15,25,0.6) !important;
        border: 1px solid rgba(167,139,250,0.15) !important;
        border-radius: 14px !important;
        padding: clamp(10px,2vw,14px) clamp(12px,3vw,18px) !important;
    }
    .stRadio label {
        font-family: 'Courier Prime', monospace !important;
        color: #cbd5e1 !important;
        font-size: clamp(0.72rem, 2vw, 0.85rem) !important;
    }

    /* ══════════════════════════════════════════════
       INPUTS
       ══════════════════════════════════════════════ */
    .stTextInput > div > div > input {
        font-family: 'Courier Prime', 'Courier New', monospace !important;
        background: rgba(15,15,30,0.8) !important;
        border: 1px solid rgba(167,139,250,0.25) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-size: clamp(0.78rem, 2vw, 0.9rem) !important;
        padding: clamp(8px,2vw,12px) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(167,139,250,0.6) !important;
        box-shadow: 0 0 14px rgba(167,139,250,0.15) !important;
    }
    .stTextInput label {
        font-family: 'Courier Prime', monospace !important;
        color: #94a3b8 !important;
        font-size: clamp(0.68rem, 1.8vw, 0.82rem) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ══════════════════════════════════════════════
       TABS
       ══════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15,15,25,0.7) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        border: 1px solid rgba(167,139,250,0.12) !important;
        flex-wrap: wrap !important;
        gap: 2px !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Courier Prime', monospace !important;
        font-size: clamp(0.62rem, 1.8vw, 0.78rem) !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        color: #64748b !important;
        border-radius: 8px !important;
        padding: clamp(6px,1.5vw,8px) clamp(8px,2vw,16px) !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #c4b5fd !important;
        background: rgba(124,58,237,0.2) !important;
    }

    /* ══════════════════════════════════════════════
       MÉTRICAS
       ══════════════════════════════════════════════ */
    [data-testid="metric-container"] {
        background: rgba(15,15,25,0.7) !important;
        border: 1px solid rgba(167,139,250,0.15) !important;
        border-radius: 12px !important;
        padding: clamp(8px,2vw,12px) clamp(10px,2vw,16px) !important;
    }
    [data-testid="metric-container"] label {
        font-family: 'Courier Prime', monospace !important;
        font-size: clamp(0.58rem, 1.6vw, 0.7rem) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        color: #64748b !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Press Start 2P', monospace !important;
        font-size: clamp(0.65rem, 2vw, 0.9rem) !important;
        color: #c4b5fd !important;
    }

    /* ══════════════════════════════════════════════
       MISC
       ══════════════════════════════════════════════ */
    hr {
        border: none !important;
        border-top: 1px solid rgba(167,139,250,0.1) !important;
        margin: 18px 0 !important;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15,15,25,0.5); }
    ::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.3); border-radius: 4px; }

    /* ══════════════════════════════════════════════
       ANIMACIONES GLOBALES
       ══════════════════════════════════════════════ */
    @keyframes fadeIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
    @keyframes pulse  { 0%,100% { opacity:1; } 50% { opacity:0.5; } }
    @keyframes float  { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-6px); } }
    @keyframes blink  { 0%,100% { opacity:1; } 50% { opacity:0; } }
    @keyframes glow   { 0%,100% { box-shadow:0 0 8px rgba(167,139,250,0.2); } 50% { box-shadow:0 0 24px rgba(167,139,250,0.5); } }

    .anim-fade  { animation: fadeIn .4s ease; }
    .anim-pulse { animation: pulse 2s infinite; }
    .anim-float { animation: float 3s ease-in-out infinite; }

    /* ══════════════════════════════════════════════
       GAME TITLE
       ══════════════════════════════════════════════ */
    .game-title {
        font-family: 'Press Start 2P', monospace !important;
        font-size: clamp(0.9rem, 3.5vw, 2rem);
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        line-height: 1.5;
        filter: drop-shadow(0 0 20px rgba(167,139,250,0.4));
        margin-bottom: 6px;
    }

    /* Efecto scanlines sutil */
    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background: repeating-linear-gradient(0deg, transparent, transparent 2px,
            rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px);
        pointer-events: none;
        z-index: 9999;
    }

    /* ══════════════════════════════════════════════
       RESPONSIVE — MÓVIL (≤ 480px)
       ══════════════════════════════════════════════ */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.5rem 0.5rem 2rem !important;
        }
        .game-title {
            font-size: 0.75rem !important;
            line-height: 1.7 !important;
        }
        /* Columnas apiladas en móvil */
        [data-testid="column"] {
            min-width: 100% !important;
        }
        /* Métricas más compactas */
        [data-testid="metric-container"] {
            padding: 8px 10px !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 0.65rem !important;
        }
        /* Tabs más compactos */
        .stTabs [data-baseweb="tab"] {
            padding: 5px 8px !important;
            font-size: 0.60rem !important;
        }
    }

    /* ══════════════════════════════════════════════
       RESPONSIVE — TABLET (481px – 768px)
       ══════════════════════════════════════════════ */
    @media (min-width: 481px) and (max-width: 768px) {
        .block-container {
            padding: 0.75rem 1rem 2.5rem !important;
        }
        .game-title {
            font-size: 1rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 0.72rem !important;
        }
    }

    /* ══════════════════════════════════════════════
       RESPONSIVE — LAPTOP (769px – 1024px)
       ══════════════════════════════════════════════ */
    @media (min-width: 769px) and (max-width: 1024px) {
        .block-container {
            padding: 1rem 1.5rem 3rem !important;
        }
        .game-title {
            font-size: 1.3rem !important;
        }
    }

    /* ══════════════════════════════════════════════
       RESPONSIVE — DESKTOP GRANDE (> 1400px)
       ══════════════════════════════════════════════ */
    @media (min-width: 1400px) {
        .block-container {
            max-width: 1200px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def pixel_header(titulo, subtitulo="", emoji=""):
    sub_html = (
        f'<div style="font-family:Courier Prime,monospace;'
        f'font-size:clamp(.65rem,2vw,.75rem);'
        f'color:rgba(255,255,255,.3);margin-top:8px;letter-spacing:2px;'
        f'text-transform:uppercase">{subtitulo}</div>'
    ) if subtitulo else ""
    st.markdown(
        f'''<div class="anim-fade" style="text-align:center;padding:10px 0 20px">
            <div style="font-size:clamp(1.5rem,5vw,2rem);margin-bottom:8px;
                animation:float 3s ease-in-out infinite">{emoji}</div>
            <div class="game-title">{titulo}</div>
            {sub_html}
        </div>''', unsafe_allow_html=True)


def pixel_divider(color="#a78bfa", label=""):
    label_html = (
        f'<span style="background:#0a0a0f;padding:0 12px;'
        f'font-family:Courier Prime,monospace;font-size:.68rem;'
        f'color:{color};text-transform:uppercase;letter-spacing:2px">{label}</span>'
    ) if label else ""
    st.markdown(
        f'<div style="text-align:center;margin:18px 0;position:relative">'
        f'<div style="border-top:1px solid {color}33;width:100%;'
        f'position:absolute;top:50%"></div>'
        f'<div style="position:relative;display:inline-block">{label_html}</div>'
        f'</div>', unsafe_allow_html=True)


def stat_badge(label, valor, color="#a78bfa", emoji=""):
    return (
        f'<div style="display:inline-flex;align-items:center;gap:6px;'
        f'background:rgba(15,15,25,.8);border:1px solid {color}44;'
        f'border-radius:8px;padding:5px 12px;margin:3px;'
        f'font-family:Courier Prime,monospace">'
        f'<span style="font-size:.9rem">{emoji}</span>'
        f'<span style="color:{color}88;font-size:.68rem;text-transform:uppercase;'
        f'letter-spacing:1px">{label}</span>'
        f'<span style="color:{color};font-weight:700;font-size:.9rem">{valor}</span>'
        f'</div>'
    )
