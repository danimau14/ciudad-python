import streamlit as st


def inyectar_css():
    st.markdown("""
    <style>
    /* ═══════════════════════════════════════════════════════════════
       FUENTES & RESET
    ═══════════════════════════════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Courier+Prime:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Courier Prime', 'Courier New', Courier, monospace !important;
        background-color: #0a0a0f !important;
        color: #e2e8f0 !important;
    }

    /* Fondo principal con grid pixelado sutil */
    .stApp {
        background-color: #0a0a0f !important;
        background-image:
            linear-gradient(rgba(167,139,250,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(167,139,250,0.03) 1px, transparent 1px);
        background-size: 32px 32px;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container {
        padding: 1.5rem 2rem 3rem !important;
        max-width: 1100px !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       TIPOGRAFÍA
    ═══════════════════════════════════════════════════════════════ */
    h1, h2, h3, h4 {
        font-family: 'Press Start 2P', 'Courier New', monospace !important;
        letter-spacing: 1px;
    }

    /* ═══════════════════════════════════════════════════════════════
       CARDS
    ═══════════════════════════════════════════════════════════════ */
    .card {
        background: rgba(15,15,25,0.85);
        border: 1px solid rgba(167,139,250,0.18);
        border-radius: 16px;
        padding: 20px 22px;
        margin-bottom: 12px;
        transition: border-color .25s, box-shadow .25s;
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(167,139,250,0.04) 0%, transparent 60%);
        pointer-events: none;
    }
    .card:hover {
        border-color: rgba(167,139,250,0.45);
        box-shadow: 0 0 24px rgba(167,139,250,0.12);
    }

    .card-glow {
        background: rgba(15,15,25,0.9);
        border: 1px solid rgba(96,165,250,0.25);
        border-radius: 18px;
        padding: 22px 24px;
        margin-bottom: 14px;
        box-shadow: 0 0 30px rgba(96,165,250,0.08), inset 0 1px 0 rgba(255,255,255,0.04);
    }

    /* ═══════════════════════════════════════════════════════════════
       BOTONES
    ═══════════════════════════════════════════════════════════════ */
    .stButton > button {
        font-family: 'Courier Prime', 'Courier New', monospace !important;
        font-weight: 700;
        font-size: 0.82rem;
        letter-spacing: 0.5px;
        background: rgba(30,30,50,0.9) !important;
        color: #c4b5fd !important;
        border: 1px solid rgba(167,139,250,0.35) !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        transition: all .2s ease !important;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    .stButton > button::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(135deg, rgba(167,139,250,0.08) 0%, transparent 70%);
        pointer-events: none;
    }
    .stButton > button:hover {
        background: rgba(124,58,237,0.25) !important;
        border-color: rgba(167,139,250,0.7) !important;
        color: #ede9fe !important;
        box-shadow: 0 0 18px rgba(167,139,250,0.25) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: none !important;
    }
    .stButton > button:disabled {
        opacity: 0.35 !important;
        cursor: not-allowed !important;
        transform: none !important;
    }

    /* Botón primario (primer botón de una fila) */
    div[data-testid="column"]:first-child .stButton > button,
    .btn-primary > button {
        background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(99,102,241,0.3)) !important;
        border-color: rgba(167,139,250,0.6) !important;
        box-shadow: 0 0 20px rgba(124,58,237,0.2) !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       RADIO BUTTONS
    ═══════════════════════════════════════════════════════════════ */
    .stRadio > div {
        background: rgba(15,15,25,0.6) !important;
        border: 1px solid rgba(167,139,250,0.15) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        gap: 10px !important;
    }
    .stRadio label {
        font-family: 'Courier Prime', monospace !important;
        color: #cbd5e1 !important;
        font-size: 0.9rem !important;
        cursor: pointer;
        transition: color .15s;
    }
    .stRadio label:hover { color: #c4b5fd !important; }

    /* ═══════════════════════════════════════════════════════════════
       INPUTS & TEXT AREAS
    ═══════════════════════════════════════════════════════════════ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        font-family: 'Courier Prime', 'Courier New', monospace !important;
        background: rgba(15,15,30,0.8) !important;
        border: 1px solid rgba(167,139,250,0.25) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        padding: 10px 14px !important;
        transition: border-color .2s, box-shadow .2s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(167,139,250,0.6) !important;
        box-shadow: 0 0 14px rgba(167,139,250,0.15) !important;
        outline: none !important;
    }
    .stTextInput label, .stTextArea label {
        font-family: 'Courier Prime', monospace !important;
        color: #94a3b8 !important;
        font-size: 0.82rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ═══════════════════════════════════════════════════════════════
       SELECTBOX
    ═══════════════════════════════════════════════════════════════ */
    .stSelectbox > div > div {
        background: rgba(15,15,30,0.8) !important;
        border: 1px solid rgba(167,139,250,0.25) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        font-family: 'Courier Prime', monospace !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       EXPANDERS
    ═══════════════════════════════════════════════════════════════ */
    .streamlit-expanderHeader {
        font-family: 'Courier Prime', 'Courier New', monospace !important;
        font-size: 0.82rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        color: #94a3b8 !important;
        background: rgba(15,15,25,0.7) !important;
        border: 1px solid rgba(167,139,250,0.15) !important;
        border-radius: 10px !important;
        padding: 10px 16px !important;
        transition: color .2s, border-color .2s !important;
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
        padding: 16px !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       TABS
    ═══════════════════════════════════════════════════════════════ */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15,15,25,0.7) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid rgba(167,139,250,0.12) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Courier Prime', monospace !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #64748b !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        transition: all .2s !important;
        border: none !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #c4b5fd !important;
        background: rgba(124,58,237,0.2) !important;
        box-shadow: 0 0 12px rgba(124,58,237,0.15) !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        padding: 16px 0 0 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       MÉTRICAS
    ═══════════════════════════════════════════════════════════════ */
    [data-testid="metric-container"] {
        background: rgba(15,15,25,0.7) !important;
        border: 1px solid rgba(167,139,250,0.15) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        transition: border-color .2s !important;
    }
    [data-testid="metric-container"]:hover {
        border-color: rgba(167,139,250,0.35) !important;
    }
    [data-testid="metric-container"] label {
        font-family: 'Courier Prime', monospace !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        color: #64748b !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-family: 'Press Start 2P', monospace !important;
        font-size: 0.9rem !important;
        color: #c4b5fd !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       DIVIDERS
    ═══════════════════════════════════════════════════════════════ */
    hr {
        border: none !important;
        border-top: 1px solid rgba(167,139,250,0.1) !important;
        margin: 18px 0 !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       ALERTS / INFO / WARNING
    ═══════════════════════════════════════════════════════════════ */
    .stAlert {
        font-family: 'Courier Prime', monospace !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 0.85rem !important;
    }
    [data-baseweb="notification"] {
        background: rgba(15,15,25,0.9) !important;
        border-radius: 12px !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       SCROLLBAR
    ═══════════════════════════════════════════════════════════════ */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15,15,25,0.5); }
    ::-webkit-scrollbar-thumb {
        background: rgba(167,139,250,0.3);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(167,139,250,0.5); }

    /* ═══════════════════════════════════════════════════════════════
       ANIMACIONES
    ═══════════════════════════════════════════════════════════════ */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.5; }
    }
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 8px rgba(167,139,250,0.2); }
        50%       { box-shadow: 0 0 24px rgba(167,139,250,0.5); }
    }
    @keyframes scanline {
        0%   { transform: translateY(-100%); }
        100% { transform: translateY(100vh); }
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50%       { transform: translateY(-6px); }
    }

    .anim-fade  { animation: fadeIn .4s ease; }
    .anim-pulse { animation: pulse 2s infinite; }
    .anim-glow  { animation: glow 3s ease-in-out infinite; }
    .anim-float { animation: float 3s ease-in-out infinite; }

    /* Cursor parpadeante tipo terminal */
    .cursor::after {
        content: '█';
        animation: blink 1s step-end infinite;
        color: #a78bfa;
        margin-left: 2px;
    }

    /* ═══════════════════════════════════════════════════════════════
       GAME TITLE
    ═══════════════════════════════════════════════════════════════ */
    .game-title {
        font-family: 'Press Start 2P', monospace !important;
        font-size: clamp(1.4rem, 4vw, 2.2rem);
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        line-height: 1.4;
        filter: drop-shadow(0 0 20px rgba(167,139,250,0.4));
        margin-bottom: 6px;
    }

    /* ═══════════════════════════════════════════════════════════════
       HUD — PANEL PIXELADO
    ═══════════════════════════════════════════════════════════════ */
    .hud-panel {
        background: rgba(10,10,20,0.95);
        border: 2px solid rgba(167,139,250,0.3);
        border-radius: 0px;
        padding: 14px 18px;
        position: relative;
        clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
    }
    .hud-panel::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #a78bfa, #60a5fa, transparent);
    }

    /* ═══════════════════════════════════════════════════════════════
       BADGE / CHIPS
    ═══════════════════════════════════════════════════════════════ */
    .badge {
        display: inline-block;
        font-family: 'Courier Prime', monospace;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 3px 10px;
        border-radius: 20px;
        border: 1px solid;
    }

    /* ═══════════════════════════════════════════════════════════════
       PROGRESS BAR PERSONALIZADA
    ═══════════════════════════════════════════════════════════════ */
    .stProgress > div > div {
        background: rgba(167,139,250,0.15) !important;
        border-radius: 6px !important;
        height: 8px !important;
    }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #7c3aed, #a78bfa) !important;
        border-radius: 6px !important;
        transition: width .4s ease !important;
    }

    /* ═══════════════════════════════════════════════════════════════
       SCANLINE OVERLAY (sutil efecto CRT)
    ═══════════════════════════════════════════════════════════════ */
    .stApp::after {
        content: '';
        position: fixed;
        inset: 0;
        background: repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0,0,0,0.04) 2px,
            rgba(0,0,0,0.04) 4px
        );
        pointer-events: none;
        z-index: 9999;
    }

    /* ═══════════════════════════════════════════════════════════════
       RESPONSIVE
    ═══════════════════════════════════════════════════════════════ */
    @media (max-width: 768px) {
        .block-container { padding: 1rem !important; }
        .game-title { font-size: 1.1rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)


# ── Componentes reutilizables ─────────────────────────────────────────────────

def pixel_header(titulo, subtitulo="", emoji=""):
    """Cabecera estilo juego retro con efecto pixel."""
    sub_html = (f'<div style="font-family:Courier Prime,monospace;font-size:.8rem;'
                f'color:rgba(255,255,255,.35);margin-top:8px;letter-spacing:2px;'
                f'text-transform:uppercase">{subtitulo}</div>') if subtitulo else ""
    st.markdown(
        f'''<div class="anim-fade" style="text-align:center;padding:10px 0 20px">
            <div style="font-size:2rem;margin-bottom:8px;animation:float 3s ease-in-out infinite">
                {emoji}</div>
            <div class="game-title">{titulo}</div>
            {sub_html}
        </div>''', unsafe_allow_html=True)


def pixel_divider(color="#a78bfa", label=""):
    """Divisor pixelado con etiqueta opcional."""
    label_html = (
        f'<span style="background:#0a0a0f;padding:0 12px;'
        f'font-family:Courier Prime,monospace;font-size:.68rem;'
        f'color:{color};text-transform:uppercase;letter-spacing:2px">{label}</span>'
    ) if label else ""
    st.markdown(
        f'<div style="text-align:center;margin:18px 0;position:relative">'
        f'<div style="border-top:1px solid {color}33;width:100%;position:absolute;top:50%"></div>'
        f'<div style="position:relative;display:inline-block">{label_html}</div>'
        f'</div>', unsafe_allow_html=True)


def stat_badge(label, valor, color="#a78bfa", emoji=""):
    """Badge de estadística estilo HUD."""
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


def toast_mensaje(msg, tipo="info"):
    """Mensaje toast estilo consola."""
    colores = {
        "info":    ("#60a5fa", "ℹ"),
        "success": ("#34d399", "✓"),
        "warning": ("#fbbf24", "⚠"),
        "error":   ("#f87171", "✗"),
    }
    color, ico = colores.get(tipo, colores["info"])
    st.markdown(
        f'''<div class="anim-fade" style="background:rgba(10,10,20,.95);
            border-left:3px solid {color};border-radius:0 10px 10px 0;
            padding:10px 16px;margin:8px 0;
            font-family:Courier Prime,monospace;font-size:.84rem;
            color:{color};display:flex;gap:10px;align-items:center;
            box-shadow:0 0 20px {color}15">
            <span style="font-size:1rem">{ico}</span>
            <span style="color:#e2e8f0">{msg}</span>
        </div>''', unsafe_allow_html=True)
