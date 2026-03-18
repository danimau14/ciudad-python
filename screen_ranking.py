import streamlit as st
from session_manager import navegar
from database import obtener_ranking, obtener_estudiantes, obtener_logros_grupo
from config import LOGROS
from ui_styles import pixel_header, pixel_divider


DIF_COLOR = {"Fácil": "#10b981", "Normal": "#f59e0b", "Difícil": "#ef4444"}
DIF_EMOJI = {"Fácil": "🟢", "Normal": "🟡", "Difícil": "🔴"}
MEDALLAS  = ["🥇", "🥈", "🥉"]


def _nivel(p):
    if p >= 85:   return "LEGENDARIO", "#fbbf24", "👑"
    elif p >= 70: return "EXCELENTE",  "#34d399", "🏆"
    elif p >= 55: return "BUENO",      "#60a5fa", "🌟"
    elif p >= 40: return "REGULAR",    "#f59e0b", "⚠️"
    else:         return "CRÍTICO",    "#ef4444", "🚨"


def _logros_chip(gid):
    ids   = set(obtener_logros_grupo(gid))
    chips = ""
    for l in LOGROS:
        if l["id"] in ids:
            nombre = l["nombre"]
            emoji  = l["emoji"]
            chips += f"<span title='{nombre}' style='font-size:.85rem;margin:1px'>{emoji}</span>"
    return chips or "<span style='color:rgba(255,255,255,.2);font-size:.7rem'>Sin logros</span>"


def _tabla_ranking(filas, dif_label):
    if not filas:
        st.markdown(
            f"<div style='background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);"
            f"border-radius:14px;padding:24px;text-align:center;"
            f"color:rgba(255,255,255,.3);font-size:.85rem'>"
            f"Sin partidas registradas en {dif_label}</div>",
            unsafe_allow_html=True)
        return

    for i, row in enumerate(filas):
        medalla   = MEDALLAS[i] if i < 3 else f"#{i+1}"
        nivel_lbl, nivel_color, nivel_ico = _nivel(row["puntaje"])
        dif       = row.get("dificultad", "Normal")
        col_dif   = DIF_COLOR.get(dif, "#a78bfa")
        emoji_dif = DIF_EMOJI.get(dif, "⚪")
        gid_row   = row.get("grupoid")
        estudiantes  = obtener_estudiantes(gid_row) if gid_row else []
        logros_html  = _logros_chip(gid_row) if gid_row else ""
        est_html     = " ".join(
            f"<span style='background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.25);"
            f"border-radius:20px;padding:2px 10px;font-size:.7rem;color:#c4b5fd'>{e}</span>"
            for e in estudiantes
        ) or "<span style='color:rgba(255,255,255,.2);font-size:.7rem'>—</span>"

        borde = ("rgba(251,191,36,.5)" if i == 0 else
                 "rgba(148,163,184,.35)" if i == 1 else
                 "rgba(180,120,60,.35)" if i == 2 else
                 "rgba(255,255,255,.08)")
        bg    = ("rgba(251,191,36,.06)" if i == 0 else
                 "rgba(148,163,184,.04)" if i == 1 else
                 "rgba(180,120,60,.04)" if i == 2 else
                 "rgba(15,15,25,.6)")

        st.markdown(
            f"<div style='background:{bg};border:1px solid {borde};border-radius:16px;"
            f"padding:16px 20px;margin-bottom:10px'>"
            f"<div style='display:flex;align-items:center;gap:12px;flex-wrap:wrap'>"
            f"<div style='font-size:1.6rem;min-width:36px;text-align:center'>{medalla}</div>"
            f"<div style='flex:1;min-width:160px'>"
            f"<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px'>"
            f"<span style='font-family:Press Start 2P,monospace;font-size:.78rem;"
            f"color:#f1f5f9'>{row['nombregrupo']}</span>"
            f"<span style='background:{col_dif}22;color:{col_dif};border:1px solid {col_dif}44;"
            f"border-radius:20px;padding:1px 9px;font-size:.62rem;font-weight:700'>"
            f"{emoji_dif} {dif}</span>"
            f"<span style='background:{nivel_color}22;color:{nivel_color};"
            f"border:1px solid {nivel_color}44;border-radius:20px;"
            f"padding:1px 9px;font-size:.62rem;font-weight:700'>"
            f"{nivel_ico} {nivel_lbl}</span>"
            f"</div>"
            f"<div style='margin-bottom:4px'>{est_html}</div>"
            f"<div style='font-size:.65rem;color:rgba(255,255,255,.25)'>{row.get('fecha','')}</div>"
            f"</div>"
            f"<div style='text-align:right;min-width:80px'>"
            f"<div style='font-family:Press Start 2P,monospace;font-size:1.2rem;"
            f"color:{nivel_color}'>{row['puntaje']}</div>"
            f"<div style='font-size:.62rem;color:rgba(255,255,255,.3)'>/ 100</div>"
            f"<div style='margin-top:6px'>{logros_html}</div>"
            f"</div></div></div>",
            unsafe_allow_html=True)


def pantalla_ranking():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    pixel_header("RANKING GLOBAL", "Clasificación por dificultad", "🏆")

    tab_facil, tab_normal, tab_dificil, tab_global = st.tabs(
        ["🟢 Fácil", "🟡 Normal", "🔴 Difícil", "🌐 Global"])

    with tab_facil:
        pixel_divider("#10b981", "RANKING FÁCIL")
        _tabla_ranking(obtener_ranking("Fácil", 15), "Fácil")

    with tab_normal:
        pixel_divider("#f59e0b", "RANKING NORMAL")
        _tabla_ranking(obtener_ranking("Normal", 15), "Normal")

    with tab_dificil:
        pixel_divider("#ef4444", "RANKING DIFÍCIL")
        _tabla_ranking(obtener_ranking("Difícil", 15), "Difícil")

    with tab_global:
        pixel_divider("#a78bfa", "TOP GLOBAL")
        _tabla_ranking(obtener_ranking(limite=20), "Global")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
