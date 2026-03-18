import streamlit as st
from session_manager import navegar
from database import obtener_ranking, obtener_estudiantes, obtener_logros_grupo
from config import LOGROS


DIF_COLOR = {"Fácil": "#10b981", "Normal": "#f59e0b", "Difícil": "#ef4444"}
DIF_EMOJI = {"Fácil": "🟢", "Normal": "🟡", "Difícil": "🔴"}
MEDALLAS  = ["🥇", "🥈", "🥉"]


def _nivel(p):
    if   p >= 85: return "LEGENDARIO", "#fbbf24", "👑"
    elif p >= 70: return "EXCELENTE",  "#34d399", "🏆"
    elif p >= 55: return "BUENO",      "#60a5fa", "🌟"
    elif p >= 40: return "REGULAR",    "#f59e0b", "⚠️"
    else:         return "CRÍTICO",    "#ef4444", "🚨"


def _logros_chips(gid):
    ids   = set(obtener_logros_grupo(gid))
    chips = ""
    for l in LOGROS:
        if l["id"] in ids:
            chips += (
                f"<span title='{l['nombre']}' "
                f"style='font-size:.9rem;margin:1px;cursor:default'>{l['emoji']}</span>")
    return chips or "<span style='color:rgba(255,255,255,.2);font-size:.7rem'>Sin logros</span>"


def _tabla_ranking(filas, label_dif):
    if not filas:
        st.markdown(
            f"<div style='background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);"
            f"border-radius:14px;padding:32px;text-align:center;"
            f"color:rgba(255,255,255,.25);font-size:.85rem'>"
            f"Sin partidas registradas en {label_dif}.</div>",
            unsafe_allow_html=True)
        return

    for i, row in enumerate(filas):
        medalla = MEDALLAS[i] if i < 3 else f"#{i+1}"
        niv_lbl, niv_col, niv_ico = _nivel(row["puntaje"])
        dif      = row.get("dificultad", "Normal")
        col_dif  = DIF_COLOR.get(dif, "#a78bfa")
        em_dif   = DIF_EMOJI.get(dif, "⚪")
        gid_row  = row.get("grupoid")
        estudiantes = obtener_estudiantes(gid_row) if gid_row else []
        logros_h    = _logros_chips(gid_row)      if gid_row else ""

        est_chips = " ".join(
            f"<span style='background:rgba(167,139,250,.1);"
            f"border:1px solid rgba(167,139,250,.2);border-radius:20px;"
            f"padding:2px 10px;font-size:.68rem;color:#c4b5fd'>{e}</span>"
            for e in estudiantes
        ) or "<span style='color:rgba(255,255,255,.2);font-size:.7rem'>—</span>"

        borde = ("rgba(251,191,36,.5)"  if i == 0 else
                 "rgba(148,163,184,.3)" if i == 1 else
                 "rgba(180,120,60,.3)"  if i == 2 else
                 "rgba(255,255,255,.07)")
        bg    = ("rgba(251,191,36,.06)" if i == 0 else
                 "rgba(148,163,184,.03)"if i == 1 else
                 "rgba(180,120,60,.03)" if i == 2 else
                 "rgba(15,15,25,.55)")
        glow  = f"box-shadow:0 0 30px {niv_col}18;" if i == 0 else ""

        st.markdown(
            f"<div style='background:{bg};border:1px solid {borde};border-radius:16px;"
            f"padding:16px 20px;margin-bottom:10px;{glow}'>"

            # ── Fila 1: medalla + nombre + puntaje ──────────────────────────
            f"<div style='display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px'>"
            f"<div style='font-size:1.6rem;min-width:36px;text-align:center'>{medalla}</div>"
            f"<div style='flex:1'>"
            f"<div style='display:flex;align-items:center;gap:7px;flex-wrap:wrap'>"
            f"<span style='font-family:Press Start 2P,monospace;font-size:.78rem;"
            f"color:#f1f5f9'>{row['nombregrupo']}</span>"
            f"<span style='background:{col_dif}18;color:{col_dif};"
            f"border:1px solid {col_dif}44;border-radius:20px;"
            f"padding:1px 9px;font-size:.62rem;font-weight:700'>{em_dif} {dif}</span>"
            f"<span style='background:{niv_col}18;color:{niv_col};"
            f"border:1px solid {niv_col}44;border-radius:20px;"
            f"padding:1px 9px;font-size:.62rem;font-weight:700'>{niv_ico} {niv_lbl}</span>"
            f"</div></div>"
            f"<div style='text-align:right;min-width:70px'>"
            f"<div style='font-family:Press Start 2P,monospace;font-size:1.1rem;"
            f"color:{niv_col}'>{row['puntaje']}</div>"
            f"<div style='font-size:.6rem;color:rgba(255,255,255,.25)'>/100</div></div>"
            f"</div>"

            # ── Fila 2: estudiantes ──────────────────────────────────────────
            f"<div style='background:rgba(255,255,255,.03);border-radius:8px;"
            f"padding:8px 12px;margin-bottom:8px'>"
            f"<span style='color:rgba(255,255,255,.3);font-size:.65rem;"
            f"font-family:Courier Prime,monospace;margin-right:8px'>👥 EQUIPO</span>"
            f"{est_chips}</div>"

            # ── Fila 3: logros + fecha ───────────────────────────────────────
            f"<div style='display:flex;justify-content:space-between;align-items:center;"
            f"padding:0 2px'>"
            f"<div style='display:flex;align-items:center;gap:6px'>"
            f"<span style='color:rgba(255,255,255,.25);font-size:.62rem;"
            f"font-family:Courier Prime,monospace'>🏅 LOGROS</span>"
            f"<div>{logros_h}</div></div>"
            f"<div style='font-size:.62rem;color:rgba(255,255,255,.2);"
            f"font-family:Courier Prime,monospace'>{row.get('fecha','')}</div>"
            f"</div></div>",
            unsafe_allow_html=True)


def pantalla_ranking():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    st.markdown(
        "<div style='font-family:Press Start 2P,monospace;font-size:1.3rem;"
        "background:linear-gradient(90deg,#fbbf24,#f97316);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>🏆 RANKING GLOBAL</div>"
        "<div style='color:rgba(255,255,255,.3);font-size:.75rem;"
        "font-family:Courier Prime,monospace;margin-bottom:20px'>"
        "Clasificación por nivel de dificultad</div>",
        unsafe_allow_html=True)

    tab_f, tab_n, tab_d, tab_g = st.tabs(
        ["🟢 Fácil", "🟡 Normal", "🔴 Difícil", "🌐 Global"])

    with tab_f:
        _tabla_ranking(obtener_ranking("Fácil", 15), "Fácil")
    with tab_n:
        _tabla_ranking(obtener_ranking("Normal", 15), "Normal")
    with tab_d:
        _tabla_ranking(obtener_ranking("Difícil", 15), "Difícil")
    with tab_g:
        _tabla_ranking(obtener_ranking(limite=20), "Global")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
