import streamlit as st
import sqlite3
import os
import random
import time
from session_manager import navegar
from config import (TOTAL_RONDAS, TIEMPO_PREGUNTA, COOLDOWN,
                    DECISIONES, EVENTOS_NEGATIVOS, EVENTOS_POSITIVOS,
                    IND_COLOR, IND_LABEL, PREGUNTAS, DIFICULTADES,
                    MEZCLA_PREGUNTAS, ATRIBUTOS)

# ── Conexión directa a database.db ────────────────────────────────────────────
_DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

def _cx():
    c = sqlite3.connect(_DB, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

TIEMPO_RESULTADO = 4
TIEMPO_EVENTO    = 5

def _clamp(v): return max(0, min(100, v))

DIF_META = {
    "Fácil":   {"color":"#10b981","emoji":"🟢","bg":"rgba(16,185,129,.10)"},
    "Normal":  {"color":"#f59e0b","emoji":"🟡","bg":"rgba(245,158,11,.10)"},
    "Difícil": {"color":"#ef4444","emoji":"🔴","bg":"rgba(239,68,68,.10)"},
}

# ── Helpers de DB ─────────────────────────────────────────────────────────────
def _progreso(gid, dif):
    c = _cx(); cur = c.cursor()
    cur.execute("SELECT * FROM progresojuego WHERE grupoid=? AND dificultad=? LIMIT 1", (gid, dif))
    r = cur.fetchone()
    if r is None:
        try:
            cur.execute("INSERT INTO progresojuego(grupoid,dificultad,economia,medioambiente,energia,bienestarsocial,rondaactual) VALUES(?,?,50,50,50,50,1)", (gid, dif))
            c.commit()
        except Exception:
            c.rollback()
        cur.execute("SELECT * FROM progresojuego WHERE grupoid=? AND dificultad=? LIMIT 1", (gid, dif))
        r = cur.fetchone()
    c.close()
    if r is None:
        return {"economia":50,"medioambiente":50,"energia":50,"bienestarsocial":50,"rondaactual":1}
    return dict(r)

def _actualizar_progreso(gid, eco, amb, ene, bie, ronda, dif):
    c = _cx()
    n = c.execute("UPDATE progresojuego SET economia=?,medioambiente=?,energia=?,bienestarsocial=?,rondaactual=? WHERE grupoid=? AND dificultad=?",
                  (eco, amb, ene, bie, ronda, gid, dif)).rowcount
    if n == 0:
        try:
            c.execute("INSERT INTO progresojuego(grupoid,dificultad,economia,medioambiente,energia,bienestarsocial,rondaactual) VALUES(?,?,?,?,?,?,?)",
                      (gid, dif, eco, amb, ene, bie, ronda))
        except Exception:
            pass
    c.commit(); c.close()

def _cooldowns(gid, dif):
    c = _cx(); cur = c.cursor()
    cur.execute("SELECT decision,rondasrestantes FROM cooldowndecisiones WHERE grupoid=? AND dificultad=?", (gid, dif))
    r = cur.fetchall(); c.close()
    return {x["decision"]: x["rondasrestantes"] for x in r}

def _actualizar_cooldown(gid, decision, ronda, dif):
    c = _cx()
    c.execute("DELETE FROM cooldowndecisiones WHERE grupoid=? AND decision=? AND dificultad=?", (gid, decision, dif))
    c.execute("INSERT INTO cooldowndecisiones(grupoid,dificultad,decision,rondasrestantes) VALUES(?,?,?,?)",
              (gid, dif, decision, ronda + COOLDOWN))
    c.commit(); c.close()

def _estudiantes(gid):
    c = _cx(); cur = c.cursor()
    cur.execute("SELECT nombreestudiante FROM estudiantes WHERE grupoid=? ORDER BY id", (gid,))
    r = cur.fetchall(); c.close()
    return [x["nombreestudiante"] for x in r]

def _estrellas(gid):
    c = _cx(); cur = c.cursor()
    cur.execute("SELECT total FROM estrellas_grupo WHERE grupoid=?", (gid,))
    r = cur.fetchone(); c.close()
    return r["total"] if r else 0

def _guardar_estrellas(gid, cantidad):
    c = _cx(); cur = c.cursor()
    c.execute("INSERT OR IGNORE INTO estrellas_grupo(grupoid,total) VALUES(?,0)", (gid,))
    cur.execute("SELECT total FROM estrellas_grupo WHERE grupoid=?", (gid,))
    actual = (cur.fetchone() or {"total": 0})["total"]
    nuevo  = max(0, actual + cantidad)
    c.execute("UPDATE estrellas_grupo SET total=? WHERE grupoid=?", (nuevo, gid))
    c.commit(); c.close()

# ── Helpers de lógica ─────────────────────────────────────────────────────────
def _seleccionar_pregunta():
    dif_p  = st.session_state.get("dificultad_sel", "Normal")
    mezcla = MEZCLA_PREGUNTAS.get(dif_p, MEZCLA_PREGUNTAS["Normal"])
    usadas = set(st.session_state.get("preguntas_usadas", []))
    dispon = [i for i in range(len(PREGUNTAS)) if i not in usadas]
    if not dispon:
        st.session_state["preguntas_usadas"] = []
        dispon = list(range(len(PREGUNTAS)))
    por_dif = {"facil": [], "normal": [], "dificil": []}
    for i in dispon:
        por_dif.get(PREGUNTAS[i].get("dif", "normal"), por_dif["normal"]).append(i)
    niveles = [k for k in mezcla if por_dif[k]]
    if not niveles:
        idx = random.choice(dispon)
    else:
        total_p = sum(mezcla[k] for k in niveles)
        nivel   = random.choices(niveles, weights=[mezcla[k]/total_p for k in niveles], k=1)[0]
        idx     = random.choice(por_dif[nivel])
    st.session_state.setdefault("preguntas_usadas", []).append(idx)
    return PREGUNTAS[idx]

def _aplicar_efectos(ind, ef):
    r = dict(ind)
    for k, v in ef.items():
        if k in r:
            r[k] = _clamp(r[k] + v)
    return r

def _activo(key):
    return key in st.session_state.get("atributos_activos", set())


# ══════════════════════════════════════════════════════════════════════════════
#  ENCABEZADO
# ══════════════════════════════════════════════════════════════════════════════

def _cabecera(nombre_grp, estudiantes, ronda, est_turno, dif, ind, estrellas):
    dm  = DIF_META.get(dif, DIF_META["Normal"])
    pct = int((ronda - 1) / TOTAL_RONDAS * 100)
    fase_actual = st.session_state.get("fase_ronda", "decision")
    fase_map = {
        "decision":           ("⚙️","DECISIÓN","#a78bfa"),
        "pregunta":           ("❓","PREGUNTA","#60a5fa"),
        "evento":             ("🌐","EVENTO",  "#34d399"),
        "resultado_pregunta": ("📊","RESULTADO","#f59e0b"),
    }
    fase_ico, fase_txt, fase_col = fase_map.get(fase_actual, ("●","—","#a78bfa"))

    ronda_chips = "".join(
        "<span style='display:inline-flex;align-items:center;justify-content:center;"
        "width:22px;height:22px;border-radius:50%;"
        "background:" + ("#7c3aed" if i < ronda else dm["color"] if i == ronda else "transparent") + ";"
        "color:" + ("#fff" if i <= ronda else "rgba(255,255,255,.2)") + ";"
        "border:1px solid " + ("#7c3aed" if i < ronda else dm["color"] if i == ronda else "rgba(255,255,255,.1)") + ";"
        "font-size:.58rem;font-weight:700;margin:1px 2px'>" + str(i) + "</span>"
        for i in range(1, TOTAL_RONDAS + 1))

    est_chips = "".join(
        "<span style='display:inline-flex;align-items:center;gap:5px;"
        + ("background:linear-gradient(135deg,rgba(124,58,237,.4),rgba(99,102,241,.3));border:1px solid rgba(167,139,250,.65);border-radius:20px;padding:4px 14px;font-size:.78rem;color:#e9d5ff;font-weight:700;margin:2px;box-shadow:0 0 12px rgba(167,139,250,.3)'>✏️ " if e == est_turno else "background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:20px;padding:4px 14px;font-size:.76rem;color:#475569;margin:2px'>")
        + e + "</span>"
        for e in estudiantes)

    ind_html = ""
    for key in ["economia","medio_ambiente","energia","bienestar_social"]:
        color, emoji = IND_COLOR[key]
        v   = _clamp(ind.get(key, 50))
        bc  = "#10b981" if v >= 60 else "#f59e0b" if v >= 30 else "#ef4444"
        crit= v < 30
        ind_html += (
            "<div style='flex:1;min-width:72px;background:rgba(255,255,255,.03);"
            "border:" + ("1.5px solid #ef444466" if crit else "1px solid " + color + "18") + ";"
            "border-radius:12px;padding:8px 10px;text-align:center;position:relative'>"
            + ("<div style='position:absolute;top:4px;right:4px;width:7px;height:7px;border-radius:50%;background:#ef4444;box-shadow:0 0 6px #ef4444'></div>" if crit else "") +
            "<div style='font-size:.95rem;line-height:1'>" + emoji + "</div>"
            "<div style='font-size:.55rem;color:rgba(255,255,255,.28);letter-spacing:1.5px;text-transform:uppercase;margin:3px 0'>"
            + IND_LABEL[key].split()[0] + "</div>"
            "<div style='font-size:1rem;font-weight:900;color:" + bc + ";font-family:Courier Prime,monospace;line-height:1'>" + str(v) + "</div>"
            "<div style='margin-top:4px;background:rgba(255,255,255,.06);border-radius:3px;height:3px'>"
            "<div style='width:" + str(v) + "%;background:" + color + ";height:3px;border-radius:3px'></div></div></div>")

    col_hdr, col_cfg = st.columns([13, 1])
    with col_hdr:
        st.markdown(
            "<style>@keyframes hglow{0%,100%{box-shadow:0 0 20px " + dm["color"] + "18,0 8px 32px rgba(0,0,0,.5)}50%{box-shadow:0 0 40px " + dm["color"] + "30,0 8px 32px rgba(0,0,0,.5)}}"
            "@keyframes sweep{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}</style>"
            "<div style='background:linear-gradient(135deg,rgba(8,8,22,.98),rgba(12,12,30,.96));"
            "border:1px solid " + dm["color"] + "28;border-top:2px solid " + dm["color"] + ";"
            "border-radius:16px;padding:12px 16px 10px;animation:hglow 3s ease-in-out infinite;position:relative;overflow:hidden'>"
            "<div style='position:absolute;top:0;left:0;right:0;height:2px;overflow:hidden'>"
            "<div style='height:2px;background:linear-gradient(90deg,transparent," + dm["color"] + ",transparent);animation:sweep 2s linear infinite'></div></div>"
            # Fila 1
            "<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:10px'>"
            "<span style='font-size:1.1rem;filter:drop-shadow(0 0 6px rgba(167,139,250,.6))'>🏙️</span>"
            "<span style='font-family:Press Start 2P,monospace;font-size:clamp(.55rem,1.6vw,.78rem);"
            "background:linear-gradient(90deg,#ddd6fe,#a5b4fc,#93c5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>"
            + nombre_grp + "</span>"
            "<span style='background:" + dm["bg"] + ";color:" + dm["color"] + ";border:1px solid " + dm["color"] + "50;border-radius:20px;padding:2px 10px;font-size:.64rem;font-weight:700'>"
            + dm["emoji"] + " " + dif + "</span>"
            "<span style='background:" + fase_col + "18;color:" + fase_col + ";border:1px solid " + fase_col + "44;border-radius:20px;padding:2px 10px;font-size:.62rem;font-weight:700'>"
            + fase_ico + " " + fase_txt + "</span>"
            "<div style='margin-left:auto'>"
            "<span style='display:inline-flex;align-items:center;gap:5px;background:rgba(251,191,36,.12);color:#fbbf24;"
            "border:1px solid rgba(251,191,36,.38);border-radius:20px;padding:3px 12px;"
            "font-family:Courier Prime,monospace;font-size:.76rem;font-weight:800'>⭐ " + str(estrellas) + "</span>"
            "</div></div>"
            # Fila 2
            "<div style='display:flex;flex-wrap:wrap;gap:2px;margin-bottom:10px'>" + est_chips + "</div>"
            # Fila 3
            "<div style='display:flex;align-items:center;gap:8px;margin-bottom:8px'>"
            "<span style='font-family:Courier Prime,monospace;font-size:.57rem;color:rgba(255,255,255,.2);white-space:nowrap;min-width:42px'>"
            "R " + str(ronda) + "/" + str(TOTAL_RONDAS) + "</span>"
            "<div style='flex:1;display:flex;gap:2px;align-items:center'>" + ronda_chips + "</div>"
            "<span style='font-family:Courier Prime,monospace;font-size:.60rem;color:" + dm["color"] + ";font-weight:700;min-width:32px;text-align:right'>"
            + str(pct) + "%</span></div>"
            "<div style='background:rgba(255,255,255,.04);border-radius:4px;height:4px;overflow:hidden'>"
            "<div style='width:" + str(pct) + "%;height:4px;background:linear-gradient(90deg,#7c3aed," + dm["color"] + ");border-radius:4px;box-shadow:0 0 10px " + dm["color"] + "80'></div></div>"
            "</div>",
            unsafe_allow_html=True)
        st.markdown("<div style='display:flex;gap:5px;margin-bottom:10px'>" + ind_html + "</div>",
                    unsafe_allow_html=True)

    with col_cfg:
        st.markdown("<style>div[data-testid='stExpander'] .stButton button{font-size:0.58rem!important;padding:5px 4px!important;min-height:0!important;height:auto!important;line-height:1.2!important;white-space:normal!important;word-break:break-word!important}</style>",
                    unsafe_allow_html=True)
        with st.expander("⚙️"):
            if st.button("📖\nInstruc.", use_container_width=True):
                st.session_state["_from_juego"] = True
                navegar("instrucciones")
            if st.button("🏠\nInicio",   use_container_width=True): navegar("inicio")
            if st.button("⬅️\nLobby",   use_container_width=True): navegar("lobby")


# ══════════════════════════════════════════════════════════════════════════════
#  PANEL DE ATRIBUTOS
# ══════════════════════════════════════════════════════════════════════════════

def _panel_estrellas(gid, estrellas):
    activos = st.session_state.get("atributos_activos", set())
    st.markdown(
        "<div style='background:rgba(251,191,36,.04);border:1px solid rgba(251,191,36,.16);"
        "border-radius:14px;padding:12px 16px;margin-bottom:12px'>"
        "<div style='display:flex;align-items:center;gap:8px;margin-bottom:10px'>"
        "<span style='font-size:1rem'>⭐</span>"
        "<span style='font-family:Courier Prime,monospace;font-size:.68rem;"
        "text-transform:uppercase;letter-spacing:2px;color:#fbbf24;font-weight:700'>Atributos</span>"
        "<span style='background:rgba(251,191,36,.12);color:#fbbf24;"
        "border:1px solid rgba(251,191,36,.30);border-radius:20px;padding:2px 10px;font-size:.70rem;font-weight:800'>"
        "⭐ " + str(estrellas) + " acumuladas</span>"
        "<span style='margin-left:auto;font-size:.56rem;color:rgba(255,255,255,.2);"
        "font-family:Courier Prime,monospace'>Se consumen al finalizar ronda</span>"
        "</div>",
        unsafe_allow_html=True)

    cols = st.columns(len(ATRIBUTOS))
    for i, (key, atr) in enumerate(ATRIBUTOS.items()):
        ac     = key in activos
        col    = cols[i]
        puede  = estrellas >= atr["costo"] and not ac
        tc     = "#60a5fa" if atr["tipo"] == "pregunta" else "#a78bfa"
        bg_a   = "rgba(52,211,153,.10)" if ac else "rgba(255,255,255,.03)"
        brd_a  = "rgba(52,211,153,.40)" if ac else "rgba(255,255,255,.07)"
        sombra = "box-shadow:0 0 14px rgba(52,211,153,.20);" if ac else ""
        badge  = ("<div style='position:absolute;top:3px;right:3px;background:rgba(52,211,153,.18);color:#34d399;"
                  "font-size:.46rem;border:1px solid rgba(52,211,153,.35);border-radius:8px;padding:1px 4px'>✓</div>") if ac else ""
        with col:
            st.markdown(
                "<div style='background:" + bg_a + ";border:1px solid " + brd_a + ";"
                "border-radius:10px;padding:8px 5px;text-align:center;min-height:98px;"
                "position:relative;" + sombra + "'>" + badge +
                "<div style='font-size:1.2rem;margin-bottom:2px'>" + atr["emoji"] + "</div>"
                "<div style='font-size:.60rem;font-weight:700;color:#f1f5f9;line-height:1.2;margin-bottom:2px'>"
                + atr["nombre"] + "</div>"
                "<div style='font-size:.50rem;color:rgba(255,255,255,.25);line-height:1.25;margin-bottom:4px'>"
                + atr["desc"] + "</div>"
                "<div style='display:flex;align-items:center;justify-content:center;gap:3px'>"
                "<span style='background:" + tc + "15;color:" + tc + ";border:1px solid " + tc + "38;"
                "border-radius:7px;padding:1px 4px;font-size:.46rem'>" + atr["tipo"].upper() + "</span>"
                "<span style='color:#fbbf24;font-weight:700;font-size:.62rem'>⭐" + str(atr["costo"]) + "</span>"
                "</div></div>",
                unsafe_allow_html=True)
            if ac:
                st.markdown("<div style='text-align:center;color:#34d399;font-size:.56rem;margin-top:2px'>✓ Activo</div>",
                            unsafe_allow_html=True)
            elif puede:
                if st.button("+" + str(atr["costo"]) + "⭐", key="atr_" + key, use_container_width=True):
                    _guardar_estrellas(gid, -atr["costo"])   # resta en database.db
                    a = st.session_state.get("atributos_activos", set())
                    a.add(key)
                    st.session_state["atributos_activos"] = a
                    st.rerun()
            else:
                txt = "Activo" if ac else "-" + str(atr["costo"] - estrellas) + "⭐"
                st.markdown("<div style='text-align:center;color:rgba(255,255,255,.16);font-size:.56rem;margin-top:2px'>"
                            + txt + "</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def pantalla_juego():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    dif          = st.session_state.get("dificultad_sel", "Normal")
    progreso     = _progreso(gid, dif)
    estudiantes  = _estudiantes(gid)
    cooldowns    = _cooldowns(gid, dif)
    ronda        = progreso["rondaactual"]
    nombre_grp   = st.session_state.get("grupo_nombre", "")
    idx_turno    = (ronda - 1) % len(estudiantes)
    est_turno    = estudiantes[idx_turno]
    dif_cfg      = DIFICULTADES.get(dif, DIFICULTADES["Normal"])
    # Penalización: -5 pts (impar) o -10 pts (par = doble)
    base_pen     = dif_cfg["penalizacion"]   # = 5 para todas las dificultades
    penalizacion = base_pen * (dif_cfg["mult_par"] if ronda % 2 == 0 else 1)
    estrellas    = _estrellas(gid)

    ind = {
        "economia":         progreso["economia"],
        "medio_ambiente":   progreso["medioambiente"],
        "energia":          progreso["energia"],
        "bienestar_social": progreso["bienestarsocial"],
    }

    if ronda > TOTAL_RONDAS:
        st.session_state.update(resultado="victoria", indicadores_finales=ind,
                                rondas_completadas=TOTAL_RONDAS)
        navegar("fin"); return
    if any(v <= 0 for v in ind.values()):
        st.session_state.update(resultado="colapso", indicadores_finales=ind,
                                rondas_completadas=ronda - 1)
        navegar("fin"); return

    _cabecera(nombre_grp, estudiantes, ronda, est_turno, dif, ind, estrellas)
    st.markdown("---")
    fase = st.session_state.get("fase_ronda", "decision")

    # ══ FASE DECISIÓN ═════════════════════════════════════════════════════════
    if fase == "decision":
        _panel_estrellas(gid, estrellas)
        st.markdown("<div style='font-family:Courier Prime,monospace;font-size:.65rem;"
                    "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.25);"
                    "margin-bottom:10px'>⚙️ Elige una Decisión Estratégica</div>",
                    unsafe_allow_html=True)
        cols = st.columns(4)
        for i, (nom, ef) in enumerate(DECISIONES.items()):
            col  = cols[i % 4]
            cd   = cooldowns.get(nom, 0)
            disp = cd == 0 or ronda >= cd
            rf   = max(0, cd - ronda) if cd > 0 else 0
            filas = ""
            for k, v in ef.items():
                if k == "emoji": continue
                ci, ei = IND_COLOR.get(k, ("#94a3b8",""))
                filas += ("<div style='display:flex;justify-content:space-between;padding:2px 0;"
                          "border-bottom:1px solid rgba(255,255,255,.04)'>"
                          "<span style='color:" + ci + ";font-size:.68rem'>" + ei + " " + IND_LABEL.get(k,k) + "</span>"
                          "<span style='color:" + ("#4ade80" if v>0 else "#f87171") + ";font-size:.74rem;font-weight:700'>"
                          + ("+" if v>0 else "") + str(v) + "</span></div>")
            overlay = ""
            if not disp:
                dots = "".join("<span style='display:inline-block;width:7px;height:7px;border-radius:50%;"
                               "background:" + ("#fbbf24" if j<rf else "rgba(255,255,255,.08)") + ";margin:1px'></span>"
                               for j in range(COOLDOWN))
                overlay = ("<div style='position:absolute;inset:0;border-radius:14px;background:rgba(0,0,0,.62);"
                           "display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px'>"
                           "<span style='font-size:1.1rem'>⏳</span>"
                           "<span style='color:#fbbf24;font-weight:700;font-size:.78rem'>"
                           + str(rf) + " ronda" + ("s" if rf!=1 else "") + "</span>" + dots + "</div>")
            with col:
                st.markdown("<div style='position:relative;background:" +
                            ("rgba(167,139,250,.04)" if disp else "rgba(245,158,11,.02)") +
                            ";border:1px solid " + ("rgba(167,139,250,.32)" if disp else "rgba(245,158,11,.18)") +
                            ";border-radius:14px;padding:12px;margin-bottom:4px;min-height:165px;"
                            "opacity:" + ("1" if disp else ".45") + "'>" + overlay +
                            "<div style='font-size:1.3rem;margin-bottom:3px'>" + ef["emoji"] + "</div>"
                            "<div style='font-weight:700;color:#f1f5f9;font-size:.78rem;margin-bottom:6px;line-height:1.2'>"
                            + nom + "</div>" + filas + "</div>", unsafe_allow_html=True)
                if st.button("Elegir" if disp else "Bloqueada", disabled=not disp,
                             key="dec_" + nom, use_container_width=True):
                    st.session_state["decision_elegida"] = nom
                    st.session_state["decision_efectos"] = {k:v for k,v in ef.items() if k!="emoji"}
                    st.session_state["pregunta_actual"]  = _seleccionar_pregunta()
                    st.session_state["timer_inicio"]     = None
                    st.session_state["tiempo_agotado"]   = False
                    st.session_state["fase_ronda"]       = "pregunta"
                    d = st.session_state.get("decisiones_usadas_partida", set())
                    d.add(nom)
                    st.session_state["decisiones_usadas_partida"] = d
                    st.rerun()

    # ══ FASE PREGUNTA — countdown automático ══════════════════════════════════
    elif fase == "pregunta":
        pregunta = st.session_state["pregunta_actual"]
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]
        t_total  = TIEMPO_PREGUNTA + (15 if _activo("tiempo_extra") else 0)
        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()
        transcurrido = time.time() - st.session_state["timer_inicio"]
        restante     = max(0.0, t_total - transcurrido)
        pct_t        = restante / t_total
        seg          = int(restante)
        col_t        = "#10b981" if pct_t > 0.5 else "#f59e0b" if pct_t > 0.25 else "#ef4444"
        urgente      = seg <= 8

        # Decisión activa
        ef_res = " ".join("<span style='color:" + IND_COLOR[k][0] + "'>" +
                          IND_COLOR[k][1] + " " + ("+" if v>0 else "") + str(v) + "</span>"
                          for k,v in ef_dec.items() if k in IND_COLOR)
        st.markdown("<div style='background:rgba(99,102,241,.05);border:1px solid rgba(99,102,241,.18);"
                    "border-radius:10px;padding:8px 14px;margin-bottom:12px'>"
                    "<span style='color:#a78bfa;font-size:.72rem'>Decisión: </span>"
                    "<span style='color:#f1f5f9;font-weight:700'>" + DECISIONES.get(nom_dec,{}).get("emoji","") + " " + nom_dec + "</span>"
                    " <span style='color:rgba(255,255,255,.22);font-size:.68rem'>" + ef_res + "</span></div>",
                    unsafe_allow_html=True)

        # Reloj SVG
        radio = 38; circunf = 2 * 3.14159 * radio; offset = circunf * (1 - pct_t)
        st.markdown(
            "<div style='background:rgba(0,0,0,.22);border:1px solid " + col_t + "22;"
            "border-radius:14px;padding:14px 18px;margin-bottom:14px'>"
            "<div style='display:flex;align-items:center;gap:18px'>"
            "<svg width='88' height='88' viewBox='0 0 88 88'>"
            "<circle cx='44' cy='44' r='" + str(radio) + "' fill='none' stroke='rgba(255,255,255,.05)' stroke-width='5'/>"
            "<circle cx='44' cy='44' r='" + str(radio) + "' fill='none' stroke='" + col_t + "' stroke-width='5'"
            " stroke-dasharray='" + str(round(circunf,1)) + "' stroke-dashoffset='" + str(round(offset,1)) + "'"
            " stroke-linecap='round' transform='rotate(-90 44 44)' style='transition:stroke-dashoffset .95s linear'/>"
            "<text x='44' y='44' text-anchor='middle' dominant-baseline='central' fill='" + col_t + "'"
            " font-size='20' font-weight='900' font-family='Courier Prime,monospace'>" + str(seg) + "</text>"
            "</svg>"
            "<div style='flex:1'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
            "<span style='color:rgba(255,255,255,.35);font-size:.72rem'>Tiempo restante"
            + (" (+15s)" if _activo("tiempo_extra") else "") + "</span>"
            "<span style='color:" + col_t + ";font-size:.70rem;font-weight:700'>" + str(int(pct_t*100)) + "%</span></div>"
            "<div style='background:rgba(255,255,255,.05);border-radius:5px;height:8px;overflow:hidden'>"
            "<div style='width:" + str(int(pct_t*100)) + "%;height:8px;border-radius:5px;"
            "background:linear-gradient(90deg," + col_t + "80," + col_t + ");transition:width .95s linear'></div></div>"
            + ("<div style='color:#ef4444;font-size:.68rem;font-weight:700;margin-top:6px'>⚠️ ¡Responde ahora!</div>" if urgente else "") +
            "</div></div></div>",
            unsafe_allow_html=True)

        # Pregunta
        cat_c = {"Python":"#6366f1","PSeInt":"#8b5cf6","Calculo":"#06b6d4","Derivadas":"#10b981",
                 "Fisica MRU":"#f59e0b","Fisica MRUA":"#ef4444","Matrices":"#ec4899",
                 "Logica":"#f97316","Algebra":"#84cc16","Estadistica":"#a78bfa","Sistemas":"#34d399"}
        cc  = cat_c.get(pregunta.get("cat",""), "#a78bfa")
        dc  = {"facil":"#10b981","normal":"#f59e0b","dificil":"#ef4444"}.get(pregunta.get("dif","normal"),"#a78bfa")
        dl  = {"facil":"FÁCIL","normal":"NORMAL","dificil":"DIFÍCIL"}.get(pregunta.get("dif","normal"),"")
        st.markdown(
            "<div style='background:rgba(10,10,24,.94);border:1px solid " + cc + "1a;"
            "border-left:3px solid " + cc + ";border-radius:14px;padding:18px 20px;margin-bottom:14px'>"
            "<div style='display:flex;gap:6px;margin-bottom:10px'>"
            "<span style='background:" + cc + "14;color:" + cc + ";border:1px solid " + cc + "38;"
            "border-radius:20px;padding:2px 10px;font-size:.63rem;font-weight:700'>" + pregunta.get("cat","") + "</span>"
            "<span style='background:" + dc + "14;color:" + dc + ";border:1px solid " + dc + "38;"
            "border-radius:20px;padding:2px 10px;font-size:.63rem;font-weight:700'>" + dl + "</span></div>"
            "<p style='color:#f0f4ff;margin:0;font-family:Georgia,\"Times New Roman\",serif;"
            "font-size:clamp(.96rem,2.2vw,1.14rem);line-height:1.78'>" + pregunta["q"] + "</p></div>",
            unsafe_allow_html=True)

        opciones  = [chr(65+i) + ") " + op for i,op in enumerate(pregunta["ops"])]
        respuesta = st.radio("Selecciona tu respuesta:", opciones, key="radio_resp")
        if st.button("✅  Confirmar Respuesta", use_container_width=True, type="primary"):
            st.session_state["respuesta_correcta"] = (opciones.index(respuesta) == pregunta["ok"])
            st.session_state["tiempo_agotado"]     = False
            st.session_state["resultado_ts"]       = time.time()
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

        # AUTO-COUNTDOWN
        if restante <= 0:
            st.session_state["tiempo_agotado"]     = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["resultado_ts"]       = time.time()
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()
        else:
            time.sleep(1); st.rerun()

    # ══ FASE RESULTADO — countdown automático ════════════════════════════════
    elif fase == "resultado_pregunta":
        pregunta = st.session_state["pregunta_actual"]
        correcta = st.session_state["respuesta_correcta"]
        agotado  = st.session_state.get("tiempo_agotado", False)
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]
        es_par   = ronda % 2 == 0

        if st.session_state.get("resultado_ts") is None:
            st.session_state["resultado_ts"] = time.time()
        rr = max(0.0, TIEMPO_RESULTADO - (time.time() - st.session_state["resultado_ts"]))
        sr = int(rr) + 1

        if correcta:
            ef_ap = dict(ef_dec)
            if _activo("doble_efecto"):
                ef_ap = {k: v*2 if v>0 else v for k,v in ef_ap.items()}
            nuevo = _aplicar_efectos(ind, ef_ap)
            _actualizar_progreso(gid, nuevo["economia"], nuevo["medio_ambiente"],
                                 nuevo["energia"], nuevo["bienestar_social"], ronda, dif)
            _actualizar_cooldown(gid, nom_dec, ronda, dif)
            st.session_state["correctas"] = st.session_state.get("correctas",0) + 1
            racha = st.session_state.get("racha_actual",0) + 1
            st.session_state["racha_actual"] = racha
            if racha > st.session_state.get("mejor_racha",0):
                st.session_state["mejor_racha"] = racha
            st.markdown(
                "<div style='background:rgba(16,185,129,.07);border:1px solid rgba(16,185,129,.25);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:12px'>"
                "<div style='font-size:2.8rem;margin-bottom:5px'>✅</div>"
                "<h3 style='color:#34d399;margin:0 0 4px;font-size:1.25rem'>¡Respuesta Correcta!</h3>"
                "<p style='color:#6ee7b7;margin:0;font-size:.84rem'>Efectos de <b>" + nom_dec + "</b> aplicados.</p>"
                + ("<div style='margin-top:5px;font-size:.70rem;color:#c4b5fd'>✨ Doble Efecto aplicado</div>" if _activo("doble_efecto") else "") +
                "</div>", unsafe_allow_html=True)
        else:
            # Segunda oportunidad
            if _activo("segunda_oportunidad") and not agotado:
                a = st.session_state.get("atributos_activos", set()); a.discard("segunda_oportunidad")
                st.session_state["atributos_activos"] = a
                st.warning("🔄 **Segunda Oportunidad** — responde nuevamente.")
                st.session_state["fase_ronda"] = "pregunta"
                st.session_state["timer_inicio"] = st.session_state["resultado_ts"] = None
                st.rerun()

            texto_ok = pregunta["ops"][pregunta["ok"]]
            # -5 pts ronda normal, -10 pts ronda par
            pen_f = penalizacion
            escudo_msg = ""
            if _activo("escudo_ciudad"):
                pen_f = max(1, penalizacion // 2)
                escudo_msg = ("<div style='background:rgba(167,139,250,.04);border:1px solid rgba(167,139,250,.16);"
                              "border-radius:9px;padding:7px 12px;margin-bottom:7px;text-align:center;"
                              "font-size:.70rem;color:#a78bfa'>🛡️ Escudo: "
                              + str(penalizacion) + " → " + str(pen_f) + " pts</div>")
            st.markdown(escudo_msg, unsafe_allow_html=True)

            nuevo = {k: _clamp(v - pen_f) for k,v in ind.items()}
            # Protecciones individuales
            for ik, ak in [("economia","prot_economia"),("medio_ambiente","prot_ambiente"),
                           ("energia","prot_energia"),("bienestar_social","prot_bienestar")]:
                if _activo(ak):
                    nuevo[ik] = ind[ik]
                    a = st.session_state.get("atributos_activos", set()); a.discard(ak)
                    st.session_state["atributos_activos"] = a

            _actualizar_progreso(gid, nuevo["economia"], nuevo["medio_ambiente"],
                                 nuevo["energia"], nuevo["bienestar_social"], ronda, dif)
            st.session_state["incorrectas"]  = st.session_state.get("incorrectas",0) + 1
            st.session_state["racha_actual"] = 0

            aviso_par = ("Ronda par — penalización doble (" + str(pen_f) + " pts)"
                         if es_par else "Penalización: -" + str(pen_f) + " pts por indicador")
            icono  = "⏱️" if agotado else "❌"
            titulo = "Tiempo Agotado" if agotado else "Respuesta Incorrecta"
            st.markdown(
                "<div style='background:rgba(239,68,68,.07);border:1px solid rgba(239,68,68,.22);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:12px'>"
                "<div style='font-size:2.8rem;margin-bottom:5px'>" + icono + "</div>"
                "<h3 style='color:#f87171;margin:0 0 4px;font-size:1.25rem'>" + titulo + "</h3>"
                "<p style='color:#fca5a5;margin:0 0 2px;font-size:.84rem'>Correcta: <b>" + texto_ok + "</b></p>"
                "<p style='color:#fca5a5;font-size:.76rem;margin:0'>" + aviso_par + "</p></div>",
                unsafe_allow_html=True)

        # Barra countdown
        col_r = "#34d399" if correcta else "#f87171"
        st.markdown(
            "<div style='background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);"
            "border-radius:10px;padding:9px 14px;margin-bottom:8px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
            "<span style='color:rgba(255,255,255,.28);font-size:.66rem'>Avanzando al evento...</span>"
            "<span style='color:" + col_r + ";font-weight:700;font-size:1rem;font-family:Courier Prime,monospace'>"
            + str(sr) + "s</span></div>"
            "<div style='background:rgba(255,255,255,.05);border-radius:3px;height:5px;overflow:hidden'>"
            "<div style='width:" + str(int(rr/TIEMPO_RESULTADO*100)) + "%;height:5px;border-radius:3px;"
            "background:" + col_r + ";transition:width .95s linear'></div></div></div>",
            unsafe_allow_html=True)

        if st.button("Continuar al Evento →", use_container_width=True):
            st.session_state["fase_ronda"] = "evento"; st.session_state["resultado_ts"] = None; st.rerun()
        if rr <= 0:
            st.session_state["fase_ronda"] = "evento"; st.session_state["resultado_ts"] = None; st.rerun()
        else:
            time.sleep(1); st.rerun()

    # ══ FASE EVENTO — countdown automático ═══════════════════════════════════
    elif fase == "evento":
        if st.session_state.get("evento_ronda") is None:
            peso_neg = DIFICULTADES.get(dif, DIFICULTADES["Normal"])["eventos_peso"]["negativos"]
            pool = EVENTOS_NEGATIVOS if random.random() < peso_neg else EVENTOS_POSITIVOS
            st.session_state["evento_ronda"] = random.choice(pool)
            st.session_state["evento_ts"]    = time.time()
        if st.session_state.get("evento_ts") is None:
            st.session_state["evento_ts"] = time.time()

        evento  = st.session_state["evento_ronda"]
        pos     = evento["valor"] > 0
        col_ev  = "#10b981" if pos else "#ef4444"
        bg_ev   = "rgba(16,185,129,.06)" if pos else "rgba(239,68,68,.06)"
        rev     = max(0.0, TIEMPO_EVENTO - (time.time() - st.session_state["evento_ts"]))
        sev     = int(rev) + 1

        prog2 = _progreso(gid, dif)
        ind2  = {"economia":prog2["economia"],"medio_ambiente":prog2["medioambiente"],
                 "energia":prog2["energia"],"bienestar_social":prog2["bienestarsocial"]}
        iev   = evento["indicador"]; vant = ind2.get(iev, 50); vev = evento["valor"]
        escudo_ev = ""
        if not pos and _activo("escudo_ciudad"):
            vev = int(vev * 0.5)
            escudo_ev = "<div style='color:#a78bfa;font-size:.66rem;margin-top:5px'>🛡️ Escudo — impacto al 50%</div>"
        ni2 = dict(ind2); ni2[iev] = _clamp(vant + vev)
        vdp = ni2[iev]
        ci, ei = IND_COLOR.get(iev, ("#94a3b8",""))
        sgn    = "+" if vev > 0 else ""

        st.markdown(
            "<div style='background:" + bg_ev + ";border:1px solid " + col_ev + "22;"
            "border-radius:16px;padding:24px;text-align:center'>"
            "<div style='font-size:2rem;margin-bottom:4px'>" + ("🌟" if pos else "⚠️") + "</div>"
            "<div style='font-size:.62rem;color:rgba(255,255,255,.25);text-transform:uppercase;"
            "letter-spacing:2px;margin-bottom:4px'>Evento · Ronda " + str(ronda) + "</div>"
            "<h2 style='color:#f1f5f9;margin:0 0 14px;font-size:1.18rem'>" + evento["nombre"] + "</h2>"
            "<div style='display:inline-flex;align-items:center;gap:12px;"
            "background:rgba(255,255,255,.04);border-radius:10px;padding:10px 20px'>"
            "<span style='color:" + ci + ";font-size:.88rem'>" + ei + " " + IND_LABEL.get(iev,iev) + "</span>"
            "<span style='color:rgba(255,255,255,.18);font-size:1.1rem'>→</span>"
            "<span style='color:" + col_ev + ";font-weight:800;font-size:1.05rem;font-family:Courier Prime,monospace'>"
            + str(vant) + " → " + str(vdp) + " <span style='font-size:.75rem'>(" + sgn + str(vev) + ")</span></span>"
            "</div>" + escudo_ev + "</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);"
            "border-radius:10px;padding:9px 14px;margin-bottom:8px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
            "<span style='color:rgba(255,255,255,.25);font-size:.66rem'>Finalizando ronda...</span>"
            "<span style='color:#a78bfa;font-weight:700;font-size:1rem;font-family:Courier Prime,monospace'>"
            + str(sev) + "s</span></div>"
            "<div style='background:rgba(255,255,255,.05);border-radius:3px;height:5px;overflow:hidden'>"
            "<div style='width:" + str(int(rev/TIEMPO_EVENTO*100)) + "%;height:5px;border-radius:3px;"
            "background:#a78bfa;transition:width .95s linear'></div></div></div>",
            unsafe_allow_html=True)

        def _avanzar_ronda():
            _actualizar_progreso(gid, ni2["economia"], ni2["medio_ambiente"],
                                 ni2["energia"], ni2["bienestar_social"], ronda+1, dif)
            st.session_state["atributos_activos"] = set()
            st.session_state.update(pregunta_actual=None, respuesta_correcta=False,
                                    decision_elegida=None, decision_efectos=None,
                                    evento_ronda=None, evento_ts=None, resultado_ts=None,
                                    fase_ronda="decision", timer_inicio=None, tiempo_agotado=False)

        if st.button("Finalizar Ronda " + str(ronda) + "/" + str(TOTAL_RONDAS) + " →",
                     use_container_width=True):
            _avanzar_ronda(); st.rerun()
        if rev <= 0:
            _avanzar_ronda(); st.rerun()
        else:
            time.sleep(1); st.rerun()
