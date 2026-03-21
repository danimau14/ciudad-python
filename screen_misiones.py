import streamlit as st
from session_manager import navegar
from config import MISIONES, LOGROS
from db import get_connection

def _cx():
    return get_connection()

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
    r=cur.fetchall(); c.close(); return [x["logroid"] for x in r]

def _est_grupo(gid):
    c=_cx(); cur=c.cursor(); cur.execute("SELECT nombreestudiante FROM estudiantes WHERE grupoid=? ORDER BY id",(gid,))
    r=cur.fetchall(); c.close(); return [x["nombreestudiante"] for x in r]

def _canjeadas(gid):
    c=_cx(); cur=c.cursor(); cur.execute("SELECT misionid FROM misiones_canjeadas WHERE grupoid=?",(gid,))
    r=cur.fetchall(); c.close(); return [x["misionid"] for x in r]

def _pendientes(gid):
    c=_cx(); cur=c.cursor()
    cur.execute("SELECT misionid,recompensa FROM misiones_pendientes WHERE grupoid=? ORDER BY id",(gid,))
    r=cur.fetchall(); c.close(); return [{"id":x["misionid"],"recompensa":x["recompensa"]} for x in r]

def _canjear(gid, mid, rec):
    c=_cx()
    c.execute("INSERT OR IGNORE INTO misiones_canjeadas(grupoid,misionid) VALUES(?,?)",(gid,mid))
    c.execute("DELETE FROM misiones_pendientes WHERE grupoid=? AND misionid=?",(gid,mid))
    c.commit(); c.close()
    _guardar_estrellas(gid, rec)

def pantalla_misiones():
    gid        = st.session_state.get("grupo_id")
    canjeadas  = set(_canjeadas(gid)) if gid else set()
    pendientes = _pendientes(gid) if gid else []
    estrellas  = _estrellas(gid) if gid else 0
    pend_ids   = {p["id"] for p in pendientes}
    completadas= len(canjeadas)
    total      = len(MISIONES)
    pct        = int(completadas/total*100) if total else 0
    mision_map = {m["id"]:m for m in MISIONES}

    DIF_COLOR = {"Facil":"#10b981","Normal":"#f59e0b","Dificil":"#ef4444","todas":"#a78bfa"}
    DIF_LABEL = {"Facil":"FÁCIL","Normal":"NORMAL","Dificil":"DIFÍCIL","todas":"TODAS"}
    def _dk(d): return {"Fácil":"Facil","Difícil":"Dificil"}.get(d,d)

    top_cols = st.columns([1,8])
    with top_cols[0]:
        if st.button("⬅  VOLVER AL LOBBY", use_container_width=True, key="top_lobby_misiones"):
            navegar("lobby")
    with top_cols[1]:
        pass

    st.markdown(
        "<div style='display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:12px'>"
        "<div>"
        "<div style='font-family:Press Start 2P,monospace;font-size:clamp(.8rem,2.5vw,1.3rem);"
        "background:linear-gradient(90deg,#a78bfa,#34d399);-webkit-background-clip:text;"
        "-webkit-text-fill-color:transparent;margin-bottom:4px'>📋 MISIONES</div>"
        "<div style='color:rgba(255,255,255,.3);font-size:.72rem;font-family:Courier Prime,monospace'>"
        + str(completadas) + "/" + str(total) + " canjeadas</div></div>"
        "<span style='background:rgba(251,191,36,.12);color:#fbbf24;"
        "border:1px solid rgba(251,191,36,.35);border-radius:20px;"
        "padding:4px 14px;font-family:Courier Prime,monospace;font-size:.80rem;font-weight:800'>"
        "⭐ " + str(estrellas) + " acumuladas</span></div>",
        unsafe_allow_html=True)

    st.markdown(
        "<div style='background:rgba(255,255,255,.05);border-radius:8px;height:10px;margin-bottom:4px;overflow:hidden'>"
        "<div style='width:" + str(pct) + "%;height:10px;border-radius:8px;"
        "background:linear-gradient(90deg,#7c3aed,#34d399);transition:width .6s ease'></div></div>"
        "<div style='text-align:right;font-size:.66rem;color:rgba(255,255,255,.22);"
        "font-family:Courier Prime,monospace;margin-bottom:14px'>"
        + str(completadas) + "/" + str(total) + " · " + str(pct) + "%</div>",
        unsafe_allow_html=True)

    misiones_mostradas = MISIONES

    total_rec = sum(m["recompensa"] for m in MISIONES if m["id"] in canjeadas)
    total_pend = sum(p["recompensa"] for p in pendientes)
    s1,s2,s3 = st.columns(3)
    for col,label,val,color,emoji in [
        (s1,"Canjeadas",completadas,"#34d399","✅"),
        (s2,"Pendientes",len(pendientes),"#fbbf24","⏳"),
        (s3,"Acumuladas",str(estrellas)+" ⭐","#fbbf24","⭐"),
    ]:
        with col:
            st.markdown(
                "<div style='background:rgba(255,255,255,.03);border:1px solid " + color + "22;"
                "border-radius:12px;padding:12px;text-align:center;margin-bottom:16px'>"
                "<div style='font-size:1.3rem'>" + emoji + "</div>"
                "<div style='font-size:1.1rem;font-weight:700;color:" + color + "'>" + str(val) + "</div>"
                "<div style='font-size:.65rem;color:rgba(255,255,255,.3);font-family:Courier Prime,monospace'>"
                + label + "</div></div>", unsafe_allow_html=True)

    if pendientes:
        st.markdown(
            "<div style='background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.22);"
            "border-radius:10px;padding:9px 14px;margin-bottom:14px;"
            "font-family:Courier Prime,monospace;font-size:.70rem;color:#fbbf24;text-align:center'>"
            "⭐ Tienes <b>" + str(total_pend) + " estrellas</b> de misiones completadas por canjear</div>",
            unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(167,139,250,.2);margin:0 0 14px'>",
                unsafe_allow_html=True)

    def _texto_meta(m):
        t = m.get("tipo","partidas")
        if t == "partidas":
            return f"Completa {m.get('meta',1)} partidas para desbloquear."
        if t == "racha":
            return f"Consigue {m.get('meta',3)} respuestas correctas seguidas."
        if t == "correctas":
            return f"Acumula {m.get('meta',8)} respuestas correctas en una partida."
        if t == "indicador":
            ind = m.get('ind','indicador')
            return f"Lleva {ind.replace('_',' ')} a {m.get('meta',70)} puntos al final." 
        if t == "sin_rojo":
            return "Finaliza sin ninguna alerta roja de indicador." 
        if t == "victoria":
            return f"Gana 1 partida en dificultad {m.get('dif','todas')}."
        return m.get('desc','Cumple la misión especificada.')

    st.markdown(
        "<div style='background:rgba(96,165,250,.07);border:1px solid rgba(96,165,250,.2);border-radius:14px;padding:12px 18px;margin-bottom:14px;"
        "font-family:Courier Prime,monospace;font-size:.75rem;color:rgba(255,255,255,.45);line-height:1.6'>"
        "💡 Las misiones <b style='color:#fbbf24'>⏳ PENDIENTE</b> fueron completadas en una partida "
        "pero no se canjearon en la pantalla final. Canjéalas aquí para sumar estrellas a tu cuenta.</div>",
        unsafe_allow_html=True)

    n_cols = 4
    filas = [MISIONES[i:i+n_cols] for i in range(0, len(MISIONES), n_cols)]
    for fila in filas:
        cols = st.columns(n_cols)
        for j, m in enumerate(fila):
            mid = m["id"]
            canjeada = mid in canjeadas
            pendiente = mid in pend_ids
            ob = canjeada or pendiente
            filt = "none" if ob else "grayscale(1) opacity(.25)"
            bg = "rgba(124,58,237,.12)" if ob else "rgba(255,255,255,.02)"
            brd = "rgba(124,58,237,.4)" if ob else "rgba(255,255,255,.07)"
            gc = "#a78bfa" if ob else "rgba(255,255,255,.18)"
            nm = m["desc"]
            with cols[j]:
                st.markdown(
                    "<div style='background:" + bg + ";border:1px solid " + brd + ";"
                    "border-radius:14px;padding:14px;text-align:center;margin-bottom:8px;"
                    "min-height:110px'>"
                    "<div style='font-size:.70rem;font-weight:700;color:" + gc + ";"
                    "margin-bottom:4px;font-family:Courier Prime,monospace'>" + nm + "</div>"
                    "</div>",
                    unsafe_allow_html=True)
                if pendiente:
                    if st.button("Canjear", key="canjear_" + mid):
                        _canjear(gid, mid, m["recompensa"])
                        st.experimental_rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    # Botón final eliminado porque se añadió botón superior.


# ══════════════════════════════════════════════════════════════════════════════
# PANTALLA LOGROS
# ══════════════════════════════════════════════════════════════════════════════

