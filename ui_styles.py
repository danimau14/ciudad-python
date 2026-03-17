import streamlit as st


def inyectar_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');
    *, *::before, *::after { box-sizing: border-box; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(-45deg,#0a0a1a,#0f0c29,#1a0533,#0d1117,#0a1628);
             background-size:400% 400%; animation:gradientShift 12s ease infinite; min-height:100vh; }
    @keyframes gradientShift { 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%} }
    [data-testid="stHeader"], footer, #MainMenu { visibility: hidden; }
    .block-container { padding-top:1.5rem!important; padding-left:1rem!important;
                       padding-right:1rem!important; max-width:1400px!important; }
    .card { background:rgba(255,255,255,0.055); border:1px solid rgba(255,255,255,0.11);
            border-radius:18px; padding:clamp(14px,3vw,24px); margin-bottom:14px;
            backdrop-filter:blur(14px); transition:border-color 0.2s,box-shadow 0.2s; }
    .card:hover { border-color:rgba(167,139,250,0.3); box-shadow:0 4px 24px rgba(167,139,250,0.08); }
    .card-glow { background:linear-gradient(135deg,rgba(99,102,241,0.13),rgba(168,85,247,0.1));
                 border:1px solid rgba(168,85,247,0.38); border-radius:18px;
                 padding:clamp(14px,3vw,24px); margin-bottom:14px; box-shadow:0 0 30px rgba(168,85,247,0.08); }
    .card-danger { background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.3);
                   border-radius:18px; padding:clamp(14px,3vw,24px); margin-bottom:14px; }
    .card-success { background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.3);
                    border-radius:18px; padding:clamp(14px,3vw,24px); margin-bottom:14px; }
    .game-title { font-size:clamp(1.8rem,6vw,3.2rem); font-weight:900;
                  background:linear-gradient(90deg,#a78bfa,#60a5fa,#34d399,#a78bfa);
                  background-size:200% auto; -webkit-background-clip:text;
                  -webkit-text-fill-color:transparent; background-clip:text;
                  text-align:center; line-height:1.1; animation:shimmer 3s linear infinite; }
    @keyframes shimmer { 0%{background-position:0% center} 100%{background-position:200% center} }
    .game-sub { font-size:clamp(0.65rem,2vw,0.88rem); color:rgba(255,255,255,0.38);
                text-align:center; letter-spacing:clamp(1px,0.5vw,3px);
                text-transform:uppercase; margin-bottom:1.8rem; }
    div.stButton > button { border-radius:12px!important; font-weight:700!important;
        font-size:clamp(0.82rem,2vw,0.95rem)!important;
        padding:clamp(0.5rem,1.5vw,0.7rem) clamp(0.8rem,2vw,1.4rem)!important;
        transition:all 0.22s ease!important; border:1px solid rgba(255,255,255,0.13)!important;
        background:rgba(255,255,255,0.07)!important; color:#fff!important;
        width:100%!important; white-space:normal!important; word-break:break-word!important; }
    div.stButton > button:hover:not(:disabled) { background:rgba(167,139,250,0.22)!important;
        border-color:rgba(167,139,250,0.55)!important; transform:translateY(-2px)!important;
        box-shadow:0 8px 24px rgba(167,139,250,0.22)!important; }
    div.stButton > button:disabled { opacity:0.3!important; cursor:not-allowed!important; }
    [data-testid="stMetricContainer"] { background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.09); border-radius:14px;
        padding:clamp(10px,2vw,16px) clamp(12px,2.5vw,20px); text-align:center; }
    [data-testid="stMetricContainer"] label { color:rgba(255,255,255,0.45)!important;
        font-size:clamp(0.6rem,1.5vw,0.75rem)!important; text-transform:uppercase; letter-spacing:1px; }
    [data-testid="stMetricContainer"] [data-testid="stMetricValue"] { color:#fff!important;
        font-size:clamp(1rem,3vw,1.5rem)!important; font-weight:800!important; }
    [data-testid="stProgressBar"] > div { background:rgba(255,255,255,0.08)!important; border-radius:8px!important; }
    [data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#7c3aed,#a78bfa)!important; border-radius:8px!important; }
    p, li, .stMarkdown p { color:#cbd5e1!important; font-size:clamp(0.85rem,2vw,0.95rem)!important; }
    h1, h2, h3 { color:#f8fafc!important; }
    hr { border-color:rgba(255,255,255,0.07)!important; margin:1.2rem 0!important; }
    ::-webkit-scrollbar { width:5px; height:5px; }
    ::-webkit-scrollbar-track { background:rgba(255,255,255,0.03); }
    ::-webkit-scrollbar-thumb { background:rgba(167,139,250,0.4); border-radius:3px; }
    @media(max-width:640px) {
        .block-container { padding-left:0.6rem!important; padding-right:0.6rem!important; }
        .game-title { font-size:1.7rem!important; }
    }
    </style>""", unsafe_allow_html=True)
