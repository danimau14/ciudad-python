import streamlit as st


def inyectar_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Fondo animado degradado */
    .stApp {
        background: linear-gradient(-45deg, #05051a, #0d0821, #0a1628, #06101f);
        background-size: 400% 400%;
        animation: bgShift 16s ease infinite;
        min-height: 100vh;
    }
    @keyframes bgShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Chrome de Streamlit */
    #MainMenu, header, footer { visibility: hidden; }
    .block-container {
        padding-top: 1.8rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 1400px !important;
    }

    /* ── Tarjetas ── */
    .card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 20px;
        padding: clamp(14px,3vw,24px);
        margin-bottom: 14px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        transition: border-color .25s, box-shadow .25s;
    }
    .card:hover {
        border-color: rgba(167,139,250,0.28);
        box-shadow: 0 6px 32px rgba(167,139,250,0.07);
    }
    .card-glow {
        background: linear-gradient(135deg, rgba(99,102,241,.12), rgba(168,85,247,.09));
        border: 1px solid rgba(168,85,247,.36);
        border-radius: 20px;
        padding: clamp(14px,3vw,24px);
        margin-bottom: 14px;
        box-shadow: 0 0 36px rgba(168,85,247,.07);
    }
    .card-danger {
        background: rgba(239,68,68,.07);
        border: 1px solid rgba(239,68,68,.28);
        border-radius: 20px;
        padding: clamp(14px,3vw,24px);
        margin-bottom: 14px;
    }
    .card-success {
        background: rgba(16,185,129,.07);
        border: 1px solid rgba(16,185,129,.28);
        border-radius: 20px;
        padding: clamp(14px,3vw,24px);
        margin-bottom: 14px;
    }

    /* ── Título principal ── */
    .game-title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: clamp(1.9rem, 6vw, 3.4rem);
        font-weight: 700;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399, #a78bfa);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        line-height: 1.1;
        animation: shimmer 3.5s linear infinite;
        letter-spacing: -0.5px;
    }
    @keyframes shimmer {
        0%   { background-position: 0 center; }
        100% { background-position: 200% center; }
    }
    .game-sub {
        font-size: clamp(.65rem, 2vw, .85rem);
        color: rgba(255,255,255,.35);
        text-align: center;
        letter-spacing: clamp(1px,.5vw,4px);
        text-transform: uppercase;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* ── Botones ── */
    div.stButton > button {
        border-radius: 14px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: clamp(.82rem,2vw,.95rem) !important;
        padding: clamp(.5rem,1.5vw,.7rem) clamp(.8rem,2vw,1.4rem) !important;
        transition: all .22s ease !important;
        border: 1px solid rgba(255,255,255,.11) !important;
        background: rgba(255,255,255,.06) !important;
        color: #fff !important;
        width: 100% !important;
        white-space: normal !important;
        word-break: break-word !important;
        letter-spacing: .2px;
    }
    div.stButton > button:hover:not(:disabled) {
        background: rgba(167,139,250,.2) !important;
        border-color: rgba(167,139,250,.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(167,139,250,.2) !important;
    }
    div.stButton > button:active:not(:disabled) { transform: translateY(0) !important; }
    div.stButton > button:disabled {
        opacity: .28 !important;
        transform: none !important;
        cursor: not-allowed !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg,#7c3aed,#4f46e5) !important;
        border-color: rgba(124,58,237,.6) !important;
    }

    /* ── Inputs ── */
    div[data-baseweb="base-input"] input,
    div[data-baseweb="input"] div {
        background: rgba(255,255,255,.055) !important;
        border-color: rgba(255,255,255,.11) !important;
        border-radius: 14px !important;
        color: #fff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: clamp(.9rem,2vw,1rem) !important;
    }
    div[data-baseweb="base-input"] input:focus {
        border-color: rgba(167,139,250,.5) !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,.14) !important;
    }

    /* ── Radio ── */
    div[data-testid="stRadio"] div { gap: 7px !important; }
    div[data-testid="stRadio"] label {
        background: rgba(255,255,255,.04);
        border: 1.5px solid rgba(255,255,255,.08);
        border-radius: 14px;
        padding: clamp(10px,2vw,14px) clamp(12px,3vw,18px);
        margin: 0 !important;
        display: flex !important;
        cursor: pointer;
        transition: all .18s;
        color: #e2e8f0;
        font-size: clamp(.85rem,2vw,.95rem);
        align-items: center;
        gap: 10px;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(99,102,241,.15);
        border-color: rgba(99,102,241,.42);
        transform: translateX(3px);
    }

    /* ── Métricas ── */
    div[data-testid="metric-container"] {
        background: rgba(255,255,255,.045);
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 16px;
        padding: clamp(10px,2vw,16px) clamp(12px,2.5vw,20px);
        text-align: center;
    }
    div[data-testid="metric-container"] label {
        color: rgba(255,255,255,.4) !important;
        font-size: clamp(.6rem,1.5vw,.72rem) !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-size: clamp(1rem,3vw,1.5rem) !important;
        font-weight: 700 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* ── Expander ── */
    details {
        background: rgba(255,255,255,.035) !important;
        border: 1px solid rgba(255,255,255,.08) !important;
        border-radius: 14px !important;
    }
    details summary { color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif !important; }

    /* ── Progress bar ── */
    div[data-testid="stProgressBar"] > div {
        background: rgba(255,255,255,.07) !important;
        border-radius: 10px !important;
    }
    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #7c3aed, #a78bfa) !important;
        border-radius: 10px !important;
    }

    /* ── Alerts ── */
    div[data-testid="stAlert"] {
        border-radius: 14px !important;
        font-size: clamp(.85rem,2vw,.95rem) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* ── Texto ── */
    hr { border-color: rgba(255,255,255,.06) !important; margin: 1.2rem 0 !important; }
    p, li, .stMarkdown p {
        color: #cbd5e1 !important;
        font-size: clamp(.85rem,2vw,.95rem) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    h1, h2, h3 {
        color: #f8fafc !important;
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -.3px;
    }
    h3 { font-size: clamp(.95rem,2.5vw,1.15rem) !important; }

    /* ── Tabs ── */
    div[data-testid="stTabs"] button {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        color: rgba(255,255,255,.5) !important;
        border-radius: 10px 10px 0 0 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #a78bfa !important;
        border-bottom: 2px solid #a78bfa !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,.02); }
    ::-webkit-scrollbar-thumb { background: rgba(167,139,250,.38); border-radius: 4px; }

    /* ── Animaciones ── */
    @keyframes pulse-border {
        0%,100% { box-shadow: 0 0 0 0 rgba(167,139,250,.4); }
        50%      { box-shadow: 0 0 0 7px rgba(167,139,250,0); }
    }
    .pulse { animation: pulse-border 2s infinite; }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(7px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .stApp > div { animation: fadeIn .4s ease; }

    /* ── Responsive ── */
    @media (max-width: 640px) {
        .block-container { padding-left: .6rem !important; padding-right: .6rem !important; }
        div[data-testid="column"] { min-width: 100% !important; }
        .game-title { font-size: 1.7rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)
