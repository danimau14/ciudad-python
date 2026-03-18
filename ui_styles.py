import streamlit as st

def inyectar_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"], .stApp, .stMarkdown, p, li, span, div,
    button, input, label, h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
    }
    code, pre, .mono { font-family: 'JetBrains Mono', monospace !important; }

    /* Fondo */
    .stApp {
        background: linear-gradient(-45deg,#05051a,#0c0820,#081428,#040e1c);
        background-size: 400% 400%;
        animation: bgShift 18s ease infinite;
        min-height: 100vh;
    }
    @keyframes bgShift {
        0%  {background-position:0% 50%}
        50% {background-position:100% 50%}
        100%{background-position:0% 50%}
    }

    #MainMenu, header, footer { visibility: hidden; }
    .block-container {
        padding-top: 1.8rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 1400px !important;
    }

    /* Tarjetas */
    .card {
        background: rgba(255,255,255,.042);
        border: 1px solid rgba(255,255,255,.085);
        border-radius: 22px;
        padding: clamp(14px,3vw,26px);
        margin-bottom: 14px;
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        transition: border-color .25s, box-shadow .25s;
    }
    .card:hover { border-color: rgba(167,139,250,.26); box-shadow: 0 6px 32px rgba(167,139,250,.07); }
    .card-glow {
        background: linear-gradient(135deg,rgba(99,102,241,.11),rgba(168,85,247,.08));
        border: 1px solid rgba(168,85,247,.35);
        border-radius: 22px;
        padding: clamp(14px,3vw,26px);
        margin-bottom: 14px;
        box-shadow: 0 0 40px rgba(168,85,247,.06);
    }
    .card-danger {
        background: rgba(239,68,68,.065);
        border: 1px solid rgba(239,68,68,.26);
        border-radius: 22px;
        padding: clamp(14px,3vw,26px);
        margin-bottom: 14px;
    }
    .card-success {
        background: rgba(16,185,129,.065);
        border: 1px solid rgba(16,185,129,.26);
        border-radius: 22px;
        padding: clamp(14px,3vw,26px);
        margin-bottom: 14px;
    }

    /* Títulos */
    .game-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: clamp(2rem,6.5vw,3.6rem);
        font-weight: 800;
        background: linear-gradient(90deg,#a78bfa,#60a5fa,#34d399,#a78bfa);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        line-height: 1.1;
        letter-spacing: -0.5px;
        animation: shimmer 3.5s linear infinite;
    }
    @keyframes shimmer {
        0%  {background-position:0 center}
        100%{background-position:200% center}
    }
    .game-sub {
        font-size: clamp(.7rem,2vw,.88rem);
        color: rgba(255,255,255,.32);
        text-align: center;
        letter-spacing: clamp(2px,1vw,5px);
        text-transform: uppercase;
        margin-bottom: 2rem;
        font-weight: 500;
    }

    /* Botones */
    div.stButton > button {
        border-radius: 14px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: clamp(.84rem,2vw,.97rem) !important;
        padding: clamp(.5rem,1.5vw,.72rem) clamp(.8rem,2vw,1.4rem) !important;
        transition: all .22s ease !important;
        border: 1px solid rgba(255,255,255,.1) !important;
        background: rgba(255,255,255,.055) !important;
        color: #fff !important;
        width: 100% !important;
        white-space: normal !important;
        word-break: break-word !important;
        letter-spacing: .15px;
    }
    div.stButton > button:hover:not(:disabled) {
        background: rgba(167,139,250,.19) !important;
        border-color: rgba(167,139,250,.48) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(167,139,250,.18) !important;
    }
    div.stButton > button:active:not(:disabled) { transform: translateY(0) !important; }
    div.stButton > button:disabled { opacity: .26 !important; cursor: not-allowed !important; }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg,#7c3aed,#4f46e5) !important;
        border-color: rgba(124,58,237,.58) !important;
    }

    /* Inputs */
    div[data-baseweb="base-input"] input,
    div[data-baseweb="input"] div {
        background: rgba(255,255,255,.05) !important;
        border-color: rgba(255,255,255,.1) !important;
        border-radius: 14px !important;
        color: #fff !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: clamp(.9rem,2vw,1rem) !important;
    }
    div[data-baseweb="base-input"] input:focus {
        border-color: rgba(167,139,250,.48) !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,.13) !important;
    }

    /* Radio */
    div[data-testid="stRadio"] div { gap: 8px !important; }
    div[data-testid="stRadio"] label {
        background: rgba(255,255,255,.038);
        border: 1.5px solid rgba(255,255,255,.075);
        border-radius: 14px;
        padding: clamp(10px,2vw,14px) clamp(12px,3vw,18px);
        margin: 0 !important;
        display: flex !important;
        cursor: pointer;
        transition: all .18s;
        color: #e2e8f0;
        font-size: clamp(.85rem,2vw,.96rem);
        align-items: center;
        gap: 10px;
        font-family: 'Outfit', sans-serif !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(99,102,241,.14);
        border-color: rgba(99,102,241,.4);
        transform: translateX(3px);
    }

    /* Métricas */
    div[data-testid="metric-container"] {
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.075);
        border-radius: 18px;
        padding: clamp(10px,2vw,16px) clamp(12px,2.5vw,20px);
        text-align: center;
    }
    div[data-testid="metric-container"] label {
        color: rgba(255,255,255,.38) !important;
        font-size: clamp(.58rem,1.5vw,.72rem) !important;
        text-transform: uppercase;
        letter-spacing: 1.8px;
        font-family: 'Outfit', sans-serif !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #fff !important;
        font-size: clamp(1rem,3vw,1.5rem) !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Expander */
    details {
        background: rgba(255,255,255,.032) !important;
        border: 1px solid rgba(255,255,255,.075) !important;
        border-radius: 14px !important;
    }
    details summary { color: #e2e8f0 !important; font-family: 'Outfit', sans-serif !important; }

    /* Progress bar */
    div[data-testid="stProgressBar"] > div { background: rgba(255,255,255,.07) !important; border-radius: 10px !important; }
    div[data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg,#7c3aed,#a78bfa) !important;
        border-radius: 10px !important;
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 14px !important;
        font-size: clamp(.85rem,2vw,.95rem) !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Tabs */
    div[data-testid="stTabs"] button {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        color: rgba(255,255,255,.45) !important;
        border-radius: 10px 10px 0 0 !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #a78bfa !important;
        border-bottom: 2px solid #a78bfa !important;
    }

    /* Texto general */
    hr { border-color: rgba(255,255,255,.055) !important; margin: 1.2rem 0 !important; }
    p, li, .stMarkdown p { color: #cbd5e1 !important; font-size: clamp(.85rem,2vw,.96rem) !important; }
    h1, h2, h3 { color: #f8fafc !important; letter-spacing: -.3px; }
    h3 { font-size: clamp(.95rem,2.5vw,1.15rem) !important; }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: rgba(255,255,255,.02); }
    ::-webkit-scrollbar-thumb { background: rgba(167,139,250,.36); border-radius: 4px; }

    /* Animaciones */
    @keyframes pulse-border {
        0%,100%{box-shadow:0 0 0 0 rgba(167,139,250,.4)}
        50%    {box-shadow:0 0 0 7px rgba(167,139,250,0)}
    }
    .pulse { animation: pulse-border 2s infinite; }
    @keyframes fadeIn {
        from{opacity:0;transform:translateY(7px)}
        to  {opacity:1;transform:translateY(0)}
    }
    .stApp > div { animation: fadeIn .4s ease; }

    /* Responsive */
    @media(max-width:640px){
        .block-container { padding-left:.6rem !important; padding-right:.6rem !important; }
        div[data-testid="column"] { min-width:100% !important; }
        .game-title { font-size:1.8rem !important; }
    }
    </style>""", unsafe_allow_html=True)
