import streamlit as st
import sqlite3
import os
from session_manager import navegar
from config import MISIONES, LOGROS

_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
def _cx():
    c = sqlite3.connect(_DB, check_same_thread=False); c.row_factory = sqlite3.Row; return c

def _estrellas(gid):
    c=_cx(); cur=c.cursor(); cur.execute("SELECT total FROM estrellas_grupo WHERE grupoid=?",(gid,))
    r=cur.fetchone(); c.close(); return r["total"] if r else 0

def _guardar_estrellas(gid, cantidad):
    c=_cx(); cur=c.cursor()
    c.execute("INSERT OR IGNORE INTO estrellas_grupo(grupoid,total) VALUES(?,0)",(gid,))
    cur.execute("SELECT total FROM estrellas_grupo WHERE grupoid=?",(gid,))
    actual=(cur.fetchone() or {"total":0})["total"]
    c.execute("UPDATE estrellas_grupo SET total=? WHERE grupoid=?",(max(0,actual+cantidad),gid))
    c.commit(); c.close()

def _logros_grupo(gid):
    c=_cx(); cur=c.cursor(); cur.execute("SELECT logroid FROM logros_grupo WHERE grupoid=?",(gid,))
    r=c.fetchall(); c.close(); return [x["logroid"] for x in r]

def _est_grupo(gid):
    c=_cx(); cur=c.cursor(); cur.execute("SELECT nombreestudiante FROM estudiantes WHERE grupoid=? ORDER BY id",(gid,))
    r=c.fetchall(); c.close(); return [x["nombreestudiante"] for x in r]

def pantalla_logros():
    gid        = st.session_state.get("grupo_id")
    logros_ids = set(_logros_grupo(gid)) if gid else set()
    total      = len(LOGROS)
    obtenidos  = len(logros_ids)
    pct        = int(obtenidos/total*100) if total else 0

    st.markdown(
        "<div style='font-family:Press Start 2P,monospace;font-size:1.3rem;"
        "background:linear-gradient(90deg,#a78bfa,#60a5fa);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>🏅 LOGROS</div>"
        "<div style='color:rgba(255,255,255,.3);font-size:.75rem;"
        "font-family:Courier Prime,monospace;margin-bottom:14px'>"
        + str(obtenidos) + "/" + str(total) + " desbloqueados</div>",
        unsafe_allow_html=True)

    col_pct = "#34d399" if pct>=70 else "#f59e0b" if pct>=30 else "#a78bfa"
    st.markdown(
        "<div style='background:rgba(255,255,255,.05);border-radius:8px;height:10px;margin-bottom:4px;overflow:hidden'>"
        "<div style='width:" + str(pct) + "%;height:10px;border-radius:8px;"
        "background:linear-gradient(90deg,#7c3aed," + col_pct + ");transition:width .6s ease'></div></div>"
        "<div style='text-align:right;font-size:.68rem;color:rgba(255,255,255,.25);"
        "font-family:Courier Prime,monospace;margin-bottom:18px'>"
        + str(obtenidos) + "/" + str(total) + " · " + str(pct) + "%</div>",
        unsafe_allow_html=True)

    n_cols = 4
    filas  = [LOGROS[i:i+n_cols] for i in range(0, len(LOGROS), n_cols)]
    for fila in filas:
        cols = st.columns(n_cols)
        for j, logro in enumerate(fila):
            ob   = logro["id"] in logros_ids
            filt = "none" if ob else "grayscale(1) opacity(.25)"
            bg   = "rgba(124,58,237,.12)" if ob else "rgba(255,255,255,.02)"
            brd  = "rgba(124,58,237,.4)"  if ob else "rgba(255,255,255,.07)"
            gc   = "#a78bfa" if ob else "rgba(255,255,255,.18)"
            nm   = logro["nombre"] if ob else "???"
            desc = logro.get("desc","") if ob else "Logro bloqueado"
            with cols[j]:
                st.markdown(
                    "<div style='background:" + bg + ";border:1px solid " + brd + ";"
                    "border-radius:14px;padding:14px;text-align:center;margin-bottom:8px;"
                    "min-height:110px'>"
                    "<div style='font-size:1.8rem;margin-bottom:6px;filter:" + filt + "'>"
                    + (logro["emoji"] if ob else "🔒") + "</div>"
                    "<div style='font-size:.70rem;font-weight:700;color:" + gc + ";"
                    "margin-bottom:4px;font-family:Courier Prime,monospace'>" + nm + "</div>"
                    "<div style='font-size:.60rem;color:rgba(255,255,255,.25);line-height:1.3'>"
                    + desc + "</div></div>",
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True): navegar("lobby")


# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA RANKING
# ══════════════════════════════════════════════════════════════════════════════

