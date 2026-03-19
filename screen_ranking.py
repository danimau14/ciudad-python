import streamlit as st
from session_manager import navegar
from database import obtener_ranking, obtener_estudiantes, obtener_logros_grupo
from config import LOGROS


DIF_COLOR = {"Fácil": "#10b981", "Normal": "#f59e0b", "Difícil": "#ef4444"}
DIF_EMOJI = {"Fácil": "🟢",      "Normal": "🟡",      "Difícil": "🔴"}
MEDALLAS  = ["🥇", "🥈", "🥉"]


def _nivel(p):
    if   p >= 85: return "LEGENDARIO", "#fbbf24", "👑"
    elif p >= 70: return "EXCELENTE",  "#34d399", "🏆"
    elif p >= 55: return "BUENO",      "#60a5fa", "🌟"
    elif p >= 40: return "REGULAR",    "#f59e0b", "⚠️"
    else:         return "CRÍTICO",    "#ef4444", "🚨"


def _logros_obtenidos(gid):
    """Retorna lista de logros obtenidos por el grupo (emoji + nombre)."""
    ids = set(obtener_logros_grupo(gid))
    return [l for l in LOGROS if l["id"] in ids]


def _tabla_ranking(filas, label_dif):
    if not filas:
        st.markdown(
            f"<div style='background:rgba(255,255,255,.03);"
            f"border:1px solid rgba(255,255,255,.07);border-radius:14px;"
            f"padding:32px;text-align:center;color:rgba(255,255,255,.3);font-size:.9rem'>"
            f"📭 Sin partidas registradas en <b>{label_dif}</b>.</div>",
            unsafe_allow_html=True)
        return

    for i, row in enumerate(filas):
        pos        = MEDALLAS[i] if i < 3 else f"#{i+1}"
        niv_lbl, niv_col, niv_ico = _nivel(row["puntaje"])
        dif        = row.get("dificultad", "Normal")
        col_dif    = DIF_COLOR.get(dif, "#a78bfa")
        em_dif     = DIF_EMOJI.get(dif,  "⚪")
        gid_row    = row.get("grupoid")
        fecha      = row.get("fecha", "—")
        puntaje    = row["puntaje"]

        estudiantes = obtener_estudiantes(gid_row) if gid_row else []
        logros_obs  = _logros_obtenidos(gid_row)   if gid_row else []

        # Borde especial para podio
        borde = ("rgba(251,191,36,.6)"  if i == 0 else
                 "rgba(192,192,192,.5)" if i == 1 else
                 "rgba(180,120,60,.5)"  if i == 2 else
                 "rgba(167,139,250,.15)")
        bg    = ("rgba(251,191,36,.07)" if i == 0 else
                 "rgba(192,192,192,.04)"if i == 1 else
                 "rgba(180,120,60,.04)" if i == 2 else
                 "rgba(15,15,30,.6)")
        sombra = f"box-shadow:0 0 28px {niv_col}22;" if i < 3 else ""

        # ── Chips de estudiantes ──────────────────────────────────────────────
        est_html = "".join(
            f"<span style='background:rgba(167,139,250,.12);"
            f"border:1px solid rgba(167,139,250,.25);border-radius:20px;"
            f"padding:3px 12px;font-size:.72rem;color:#c4b5fd;"
            f"display:inline-block;margin:2px'>{e}</span>"
            for e in estudiantes
        ) or "<span style='color:rgba(255,255,255,.25);font-size:.72rem'>Sin estudiantes registrados</span>"

        # ── Chips de logros ───────────────────────────────────────────────────
        if logros_obs:
            logros_html = "".join(
                f"<span title='{l['nombre']}' style='display:inline-block;"
                f"background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.3);"
                f"border-radius:8px;padding:3px 8px;margin:2px;font-size:.82rem;"
                f"cursor:default'>{l['emoji']}</span>"
                for l in logros_obs
            )
        else:
            logros_html = "<span style='color:rgba(255,255,255,.25);font-size:.72rem'>Sin logros en esta partida</span>"

        st.markdown(
            f"<div style='background:{bg};border:1px solid {borde};"
            f"border-radius:18px;padding:18px 20px;margin-bottom:12px;{sombra}'>"

            # ── FILA 1: posición + nombre + puntaje ──────────────────────────
            f"<div style='display:flex;align-items:center;gap:14px;margin-bottom:14px;flex-wrap:wrap'>"
            f"<div style='font-size:2rem;min-width:44px;text-align:center;line-height:1'>{pos}</div>"
            f"<div style='flex:1;min-width:160px'>"
            f"<div style='font-family:Press Start 2P,monospace;font-size:clamp(.65rem,2vw,.82rem);"
            f"color:#f1f5f9;margin-bottom:6px'>{row['nombregrupo']}</div>"
            f"<div style='display:flex;gap:6px;flex-wrap:wrap;align-items:center'>"
            f"<span style='background:{col_dif}18;color:{col_dif};"
            f"border:1px solid {col_dif}44;border-radius:20px;"
            f"padding:2px 10px;font-size:.68rem;font-weight:700'>{em_dif} {dif}</span>"
            f"<span style='background:{niv_col}18;color:{niv_col};"
            f"border:1px solid {niv_col}44;border-radius:20px;"
            f"padding:2px 10px;font-size:.68rem;font-weight:700'>{niv_ico} {niv_lbl}</span>"
            f"<span style='color:rgba(255,255,255,.3);font-size:.65rem;"
            f"font-family:Courier Prime,monospace'>📅 {fecha}</span>"
            f"</div></div>"
            # Puntaje grande a la derecha
            f"<div style='text-align:right;min-width:80px'>"
            f"<div style='font-family:Press Start 2P,monospace;"
            f"font-size:clamp(1rem,3vw,1.3rem);color:{niv_col};"
            f"text-shadow:0 0 16px {niv_col}88'>{puntaje}</div>"
            f"<div style='font-size:.6rem;color:rgba(255,255,255,.3);"
            f"font-family:Courier Prime,monospace;margin-top:2px'>pts / 100</div>"
            f"</div></div>"

            # ── FILA 2: equipo ────────────────────────────────────────────────
            f"<div style='background:rgba(167,139,250,.06);"
            f"border:1px solid rgba(167,139,250,.12);"
            f"border-radius:10px;padding:10px 14px;margin-bottom:10px'>"
            f"<div style='font-family:Courier Prime,monospace;font-size:.62rem;"
            f"color:rgba(167,139,250,.6);letter-spacing:2px;text-transform:uppercase;"
            f"margin-bottom:6px'>👥 Equipo</div>"
            f"<div style='line-height:1.8'>{est_html}</div>"
            f"</div>"

            # ── FILA 3: logros ────────────────────────────────────────────────
            f"<div style='background:rgba(124,58,237,.05);"
            f"border:1px solid rgba(124,58,237,.15);"
            f"border-radius:10px;padding:10px 14px'>"
            f"<div style='font-family:Courier Prime,monospace;font-size:.62rem;"
            f"color:rgba(167,139,250,.6);letter-spacing:2px;text-transform:uppercase;"
            f"margin-bottom:6px'>🏅 Logros obtenidos ({len(logros_obs)})</div>"
            f"<div style='line-height:2'>{logros_html}</div>"
            f"</div>"

            f"</div>",
            unsafe_allow_html=True)


def pantalla_ranking():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown(
        "<div style='font-family:Press Start 2P,monospace;"
        "font-size:clamp(.9rem,3vw,1.3rem);"
        "background:linear-gradient(90deg,#fbbf24,#f97316);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>🏆 RANKING GLOBAL</div>"
        "<div style='color:rgba(255,255,255,.4);font-size:.78rem;"
        "font-family:Courier Prime,monospace;margin-bottom:4px'>"
        "Clasificación general por nivel de dificultad.</div>"
        "<div style='color:rgba(255,255,255,.25);font-size:.70rem;"
        "font-family:Courier Prime,monospace;margin-bottom:20px'>"
        "Muestra nombre del grupo, equipo, logros obtenidos y puntaje de cada partida.</div>",
        unsafe_allow_html=True)

    # ── Tabs por dificultad ───────────────────────────────────────────────────
    tab_f, tab_n, tab_d, tab_g = st.tabs(
        ["🟢 Fácil", "🟡 Normal", "🔴 Difícil", "🌐 Global"])

    with tab_f:
        st.markdown(
            "<div style='color:#10b981;font-family:Courier Prime,monospace;"
            "font-size:.72rem;margin-bottom:12px;letter-spacing:1px'>"
            "🟢 Top 15 partidas en dificultad Fácil</div>",
            unsafe_allow_html=True)
        _tabla_ranking(obtener_ranking("Fácil", 15), "Fácil")

    with tab_n:
        st.markdown(
            "<div style='color:#f59e0b;font-family:Courier Prime,monospace;"
            "font-size:.72rem;margin-bottom:12px;letter-spacing:1px'>"
            "🟡 Top 15 partidas en dificultad Normal</div>",
            unsafe_allow_html=True)
        _tabla_ranking(obtener_ranking("Normal", 15), "Normal")

    with tab_d:
        st.markdown(
            "<div style='color:#ef4444;font-family:Courier Prime,monospace;"
            "font-size:.72rem;margin-bottom:12px;letter-spacing:1px'>"
            "🔴 Top 15 partidas en dificultad Difícil</div>",
            unsafe_allow_html=True)
        _tabla_ranking(obtener_ranking("Difícil", 15), "Difícil")

    with tab_g:
        st.markdown(
            "<div style='color:#a78bfa;font-family:Courier Prime,monospace;"
            "font-size:.72rem;margin-bottom:12px;letter-spacing:1px'>"
            "🌐 Top 20 partidas de todas las dificultades</div>",
            unsafe_allow_html=True)
        _tabla_ranking(obtener_ranking(limite=20), "Global")

    # ── Leyenda de niveles ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='background:rgba(255,255,255,.03);"
        "border:1px solid rgba(255,255,255,.08);"
        "border-radius:12px;padding:12px 18px;margin-bottom:16px'>"
        "<div style='font-family:Courier Prime,monospace;font-size:.62rem;"
        "color:rgba(255,255,255,.3);letter-spacing:2px;text-transform:uppercase;"
        "margin-bottom:8px'>📊 Niveles de puntaje</div>"
        "<div style='display:flex;flex-wrap:wrap;gap:8px'>"
        "<span style='color:#fbbf24;font-size:.72rem'>👑 85–100 LEGENDARIO</span>"
        "<span style='color:rgba(255,255,255,.2);font-size:.72rem'>·</span>"
        "<span style='color:#34d399;font-size:.72rem'>🏆 70–84 EXCELENTE</span>"
        "<span style='color:rgba(255,255,255,.2);font-size:.72rem'>·</span>"
        "<span style='color:#60a5fa;font-size:.72rem'>🌟 55–69 BUENO</span>"
        "<span style='color:rgba(255,255,255,.2);font-size:.72rem'>·</span>"
        "<span style='color:#f59e0b;font-size:.72rem'>⚠️ 40–54 REGULAR</span>"
        "<span style='color:rgba(255,255,255,.2);font-size:.72rem'>·</span>"
        "<span style='color:#ef4444;font-size:.72rem'>🚨 0–39 CRÍTICO</span>"
        "</div></div>",
        unsafe_allow_html=True)

    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
