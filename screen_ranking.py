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

def _ranking(dif=None, limite=10):
    c=_cx(); cur=c.cursor()
    if dif:
        cur.execute("SELECT nombregrupo,puntaje,dificultad,fecha,grupoid FROM ranking WHERE dificultad=? ORDER BY puntaje DESC LIMIT ?",(dif,limite))
    else:
        cur.execute("SELECT nombregrupo,puntaje,dificultad,fecha,grupoid FROM ranking ORDER BY puntaje DESC LIMIT ?",(limite,))
    r=c.fetchall(); c.close(); return [dict(x) for x in r]

def pantalla_ranking():
    DIF_COLOR = {"Fácil":"#10b981","Normal":"#f59e0b","Difícil":"#ef4444"}
    DIF_EMOJI = {"Fácil":"🟢","Normal":"🟡","Difícil":"🔴"}
    MEDALLAS  = ["🥇","🥈","🥉"]

    def _nivel(p):
        if p>=85: return "LEGENDARIO","#fbbf24","👑"
        elif p>=70: return "EXCELENTE","#34d399","🏆"
        elif p>=55: return "BUENO","#60a5fa","🌟"
        elif p>=40: return "REGULAR","#f59e0b","⚠️"
        else: return "CRÍTICO","#ef4444","🚨"

    st.markdown(
        "<div style='font-family:Press Start 2P,monospace;font-size:1.3rem;"
        "background:linear-gradient(90deg,#fbbf24,#f97316);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "margin-bottom:4px'>🏆 RANKING</div>"
        "<div style='color:rgba(255,255,255,.3);font-size:.75rem;"
        "font-family:Courier Prime,monospace;margin-bottom:18px'>Top 10 · Mejores partidas</div>",
        unsafe_allow_html=True)

    tab_all, tab_facil, tab_normal, tab_dificil = st.tabs(["🌐 Global","🟢 Fácil","🟡 Normal","🔴 Difícil"])

    for tab, filtro in [(tab_all,None),(tab_facil,"Fácil"),(tab_normal,"Normal"),(tab_dificil,"Difícil")]:
        with tab:
            rows = _ranking(dif=filtro, limite=10)
            if not rows:
                st.markdown("<div style='color:rgba(255,255,255,.3);text-align:center;padding:20px;"
                            "font-family:Courier Prime,monospace'>Sin partidas registradas.</div>",
                            unsafe_allow_html=True)
                continue
            for idx, r in enumerate(rows):
                nivel_txt, nivel_col, nivel_ico = _nivel(r["puntaje"])
                medalla = MEDALLAS[idx] if idx < 3 else f"#{idx+1}"
                dc = DIF_COLOR.get(r["dificultad"],"#a78bfa")
                de = DIF_EMOJI.get(r["dificultad"],"⚪")
                gid_r = r.get("grupoid")
                est   = _est_grupo(gid_r) if gid_r else []
                lids  = set(_logros_grupo(gid_r)) if gid_r else set()
                chips_e = " ".join("<span style='background:rgba(167,139,250,.1);color:#c4b5fd;"
                                   "border:1px solid rgba(167,139,250,.25);border-radius:20px;"
                                   "padding:2px 10px;font-size:.65rem'>" + e + "</span>"
                                   for e in est[:5])
                chips_l = "".join("<span title='" + l["nombre"] + "' style='font-size:.9rem;margin:1px'>"
                                  + l["emoji"] + "</span>"
                                  for l in LOGROS if l["id"] in lids) or \
                          "<span style='color:rgba(255,255,255,.2);font-size:.7rem'>Sin logros</span>"
                fecha = r.get("fecha","")
                st.markdown(
                    "<div style='background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);"
                    "border-radius:16px;padding:16px 20px;margin-bottom:10px'>"
                    "<div style='display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:10px'>"
                    "<span style='font-size:1.4rem'>" + medalla + "</span>"
                    "<div style='flex:1'>"
                    "<div style='font-weight:700;color:#f1f5f9;font-size:.92rem;margin-bottom:3px'>"
                    + r["nombregrupo"] + "</div>"
                    "<div style='display:flex;gap:7px;flex-wrap:wrap;align-items:center'>"
                    "<span style='background:" + dc + "18;color:" + dc + ";border:1px solid " + dc + "44;"
                    "border-radius:20px;padding:2px 9px;font-size:.65rem;font-weight:700'>"
                    + de + " " + r["dificultad"] + "</span>"
                    "<span style='background:" + nivel_col + "18;color:" + nivel_col + ";"
                    "border:1px solid " + nivel_col + "44;border-radius:20px;padding:2px 9px;"
                    "font-size:.65rem;font-weight:700'>" + nivel_ico + " " + nivel_txt + "</span>"
                    + ("<span style='color:rgba(255,255,255,.3);font-size:.65rem'>" + fecha + "</span>" if fecha else "") +
                    "</div></div>"
                    "<div style='text-align:right'>"
                    "<div style='font-size:1.5rem;font-weight:900;color:" + nivel_col + ";"
                    "font-family:Courier Prime,monospace'>" + str(r["puntaje"]) + "</div>"
                    "<div style='font-size:.62rem;color:rgba(255,255,255,.3)'>pts</div>"
                    "</div></div>"
                    + ("<div style='margin-bottom:6px'>" + chips_e + "</div>" if chips_e else "") +
                    "<div>" + chips_l + "</div></div>",
                    unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True): navegar("lobby")
