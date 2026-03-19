import streamlit as st
import random
import time
from session_manager import navegar
from database import (obtener_progreso, obtener_estudiantes, obtener_cooldowns,
                      actualizar_progreso, actualizar_cooldown,
                      obtener_estrellas, guardar_estrellas)
from config import (TOTAL_RONDAS, TIEMPO_PREGUNTA, COOLDOWN,
                    DECISIONES, EVENTOS_NEGATIVOS, EVENTOS_POSITIVOS,
                    IND_COLOR, IND_LABEL, PREGUNTAS, DIFICULTADES,
                    MEZCLA_PREGUNTAS, ATRIBUTOS)

TIEMPO_RESULTADO = 4
TIEMPO_EVENTO    = 5

def _clamp(v): return max(0, min(100, v))

DIF_META = {
    "Fácil":   {"color": "#10b981", "emoji": "🟢", "bg": "rgba(16,185,129,.12)",  "glow": "#10b981"},
    "Normal":  {"color": "#f59e0b", "emoji": "🟡", "bg": "rgba(245,158,11,.12)",  "glow": "#f59e0b"},
    "Difícil": {"color": "#ef4444", "emoji": "🔴", "bg": "rgba(239,68,68,.12)",   "glow": "#ef4444"},
}

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
        d = PREGUNTAS[i].get("dif", "normal")
        if d in por_dif:
            por_dif[d].append(i)
    niveles = [k for k in mezcla if por_dif[k]]
    pesos   = [mezcla[k] for k in niveles]
    if not niveles:
        idx = random.choice(dispon)
    else:
        total_p = sum(pesos)
        nivel   = random.choices(niveles, weights=[p / total_p for p in pesos], k=1)[0]
        idx     = random.choice(por_dif[nivel])
    st.session_state.setdefault("preguntas_usadas", []).append(idx)
    return PREGUNTAS[idx]

def _aplicar_efectos(ind, efectos):
    r = dict(ind)
    for k, v in efectos.items():
        if k in r:
            r[k] = _clamp(r[k] + v)
    return r

def _atributo_activo(key):
    return key in st.session_state.get("atributos_activos", set())


# ══════════════════════════════════════════════════════════════════════════════
#  ENCABEZADO ESPECTACULAR
# ══════════════════════════════════════════════════════════════════════════════

def _cabecera(nombre_grp, estudiantes, ronda, est_turno, dif, ind, estrellas):
    dm  = DIF_META.get(dif, DIF_META["Normal"])
    pct = int((ronda - 1) / TOTAL_RONDAS * 100)

    fase_actual = st.session_state.get("fase_ronda", "decision")
    fase_map = {
        "decision":           ("⚙️", "DECISIÓN",  "#a78bfa", "rgba(167,139,250,.15)"),
        "pregunta":           ("❓", "PREGUNTA",   "#60a5fa", "rgba(96,165,250,.15)"),
        "evento":             ("🌐", "EVENTO",     "#34d399", "rgba(52,211,153,.15)"),
        "resultado_pregunta": ("📊", "RESULTADO",  "#f59e0b", "rgba(245,158,11,.15)"),
    }
    fase_ico, fase_txt, fase_col, fase_bg = fase_map.get(
        fase_actual, ("●", "—", "#a78bfa", "rgba(167,139,250,.15)"))

    # ── Chips de ronda ────────────────────────────────────────────────────────
    ronda_chips = ""
    for i in range(1, TOTAL_RONDAS + 1):
        if i < ronda:
            s = ("background:#7c3aed;color:#fff;border:1px solid #7c3aed;"
                 "box-shadow:0 0 6px #7c3aed66;")
        elif i == ronda:
            s = ("background:" + dm["color"] + ";color:#000;border:1px solid " + dm["color"] + ";"
                 "box-shadow:0 0 10px " + dm["color"] + ";font-weight:900;")
        else:
            s = "background:transparent;color:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.1);"
        ronda_chips += (
            "<span style='display:inline-flex;align-items:center;justify-content:center;"
            "width:24px;height:24px;border-radius:50%;" + s +
            "font-size:.6rem;font-weight:700;margin:1px 2px'>" + str(i) + "</span>")

    # ── Chips de estudiantes ──────────────────────────────────────────────────
    est_chips = ""
    for e in estudiantes:
        if e == est_turno:
            est_chips += (
                "<span style='display:inline-flex;align-items:center;gap:5px;"
                "background:linear-gradient(135deg,rgba(124,58,237,.4),rgba(99,102,241,.3));"
                "border:1px solid rgba(167,139,250,.65);"
                "border-radius:20px;padding:4px 14px;font-size:.78rem;"
                "color:#e9d5ff;font-weight:700;margin:2px;"
                "box-shadow:0 0 12px rgba(167,139,250,.3);"
                "text-shadow:0 0 8px rgba(167,139,250,.5)'>"
                "✏️ " + e + "</span>")
        else:
            est_chips += (
                "<span style='display:inline-flex;align-items:center;"
                "background:rgba(255,255,255,.03);"
                "border:1px solid rgba(255,255,255,.07);"
                "border-radius:20px;padding:4px 14px;font-size:.76rem;"
                "color:#475569;margin:2px'>" + e + "</span>")

    # ── Indicadores con mini sparkline ────────────────────────────────────────
    ind_html = ""
    for key in ["economia", "medio_ambiente", "energia", "bienestar_social"]:
        color, emoji = IND_COLOR[key]
        v   = _clamp(ind.get(key, 50))
        bc  = "#10b981" if v >= 60 else "#f59e0b" if v >= 30 else "#ef4444"
        crit = v < 30
        # Glow rojo si crítico
        ring = ("border:1.5px solid #ef444466;box-shadow:0 0 10px #ef444433;"
                if crit else "border:1px solid " + color + "18;")
        pulse = ("<div style='position:absolute;top:4px;right:4px;"
                 "width:7px;height:7px;border-radius:50%;background:#ef4444;"
                 "box-shadow:0 0 6px #ef4444;animation:pulse_dot 1s infinite'></div>"
                 if crit else "")
        ind_html += (
            "<div style='flex:1;min-width:72px;"
            "background:rgba(255,255,255,.03);" + ring +
            "border-radius:12px;padding:8px 10px;text-align:center;"
            "position:relative;transition:all .3s'>"
            + pulse +
            "<div style='font-size:.95rem;line-height:1'>" + emoji + "</div>"
            "<div style='font-size:.55rem;color:rgba(255,255,255,.28);"
            "letter-spacing:1.5px;text-transform:uppercase;margin:3px 0'>"
            + IND_LABEL[key].split()[0] + "</div>"
            "<div style='font-size:1rem;font-weight:900;color:" + bc + ";"
            "font-family:Courier Prime,monospace;line-height:1;"
            "text-shadow:0 0 8px " + bc + "66'>" + str(v) + "</div>"
            "<div style='margin-top:5px;background:rgba(255,255,255,.06);"
            "border-radius:3px;height:3px;overflow:hidden'>"
            "<div style='width:" + str(v) + "%;height:3px;border-radius:3px;"
            "background:linear-gradient(90deg," + color + "88," + color + ");"
            "transition:width .5s ease'></div></div>"
            "</div>")

    # ── LAYOUT: header + configuración ───────────────────────────────────────
    col_hdr, col_cfg = st.columns([13, 1])

    with col_hdr:
        st.markdown(
            "<style>"
            "@keyframes pulse_dot{0%,100%{opacity:1;transform:scale(1)}"
            "50%{opacity:.5;transform:scale(1.4)}}"
            "@keyframes hglow{0%,100%{box-shadow:0 0 20px " + dm["glow"] + "18,0 8px 32px rgba(0,0,0,.5)}"
            "50%{box-shadow:0 0 40px " + dm["glow"] + "30,0 8px 32px rgba(0,0,0,.5)}}"
            "</style>"

            "<div style='background:linear-gradient(135deg,rgba(8,8,22,.98),rgba(12,12,30,.96));"
            "border:1px solid " + dm["color"] + "28;"
            "border-top:2px solid " + dm["color"] + ";"
            "border-radius:16px;padding:12px 16px 10px;"
            "animation:hglow 3s ease-in-out infinite;"
            "position:relative;overflow:hidden'>"

            # Línea de energía sutil
            "<div style='position:absolute;top:0;left:0;right:0;height:2px;overflow:hidden'>"
            "<div style='height:2px;background:linear-gradient(90deg,transparent,"
            + dm["color"] + ",transparent);"
            "animation:sweep 2s linear infinite'></div></div>"
            "<style>@keyframes sweep{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}</style>"

            # Fila 1: nombre + dif + fase + estrellas
            "<div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:10px'>"

            # Nombre del grupo con font Press Start 2P y emoji visible
            "<div style='display:flex;align-items:center;gap:6px'>"
            "<span style='font-size:1.1rem;line-height:1;"
            "filter:drop-shadow(0 0 6px rgba(167,139,250,.6))'>🏙️</span>"
            "<span style='font-family:Press Start 2P,monospace;"
            "font-size:clamp(.55rem,1.6vw,.78rem);"
            "background:linear-gradient(90deg,#ddd6fe,#a5b4fc,#93c5fd);"
            "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
            "letter-spacing:1px;text-shadow:none'>"
            + nombre_grp + "</span>"
            "</div>"

            # Dificultad badge
            "<span style='background:" + dm["bg"] + ";color:" + dm["color"] + ";"
            "border:1px solid " + dm["color"] + "50;"
            "border-radius:20px;padding:3px 10px;"
            "font-size:.63rem;font-weight:700;letter-spacing:.5px;"
            "font-family:Rajdhani,sans-serif;"
            "box-shadow:0 0 8px " + dm["color"] + "30'>"
            + dm["emoji"] + " " + dif + "</span>"

            # Fase badge
            "<span style='background:" + fase_bg + ";color:" + fase_col + ";"
            "border:1px solid " + fase_col + "45;"
            "border-radius:20px;padding:3px 10px;"
            "font-size:.62rem;font-weight:700;"
            "font-family:Rajdhani,sans-serif'>"
            + fase_ico + " " + fase_txt + "</span>"

            # Estrellas — a la derecha
            "<div style='margin-left:auto'>"
            "<span style='display:inline-flex;align-items:center;gap:5px;"
            "background:rgba(251,191,36,.12);"
            "border:1px solid rgba(251,191,36,.35);"
            "border-radius:20px;padding:3px 12px;"
            "font-family:Courier Prime,monospace;"
            "font-size:.76rem;font-weight:800;color:#fbbf24;"
            "box-shadow:0 0 10px rgba(251,191,36,.2)'>⭐ " + str(estrellas) + "</span>"
            "</div></div>"

            # Fila 2: chips de estudiantes
            "<div style='display:flex;flex-wrap:wrap;gap:2px;margin-bottom:10px'>"
            + est_chips + "</div>"

            # Fila 3: rondas + progreso
            "<div style='display:flex;align-items:center;gap:8px;margin-bottom:8px'>"
            "<span style='font-family:Courier Prime,monospace;font-size:.57rem;"
            "color:rgba(255,255,255,.2);white-space:nowrap;min-width:42px'>"
            "R " + str(ronda) + "/" + str(TOTAL_RONDAS) + "</span>"
            "<div style='display:flex;flex:1;gap:2px;align-items:center'>"
            + ronda_chips + "</div>"
            "<span style='font-family:Courier Prime,monospace;font-size:.60rem;"
            "color:" + dm["color"] + ";font-weight:700;min-width:32px;text-align:right'>"
            + str(pct) + "%</span>"
            "</div>"

            # Barra de progreso animada
            "<div style='background:rgba(255,255,255,.04);border-radius:4px;height:4px;overflow:hidden'>"
            "<div style='width:" + str(pct) + "%;height:4px;"
            "background:linear-gradient(90deg,#7c3aed," + dm["color"] + ");"
            "border-radius:4px;transition:width .6s ease;"
            "box-shadow:0 0 10px " + dm["color"] + "80'></div></div>"

            "</div>",
            unsafe_allow_html=True)

        # Indicadores debajo del header
        st.markdown(
            "<div style='display:flex;gap:6px;margin-bottom:10px'>"
            + ind_html + "</div>",
            unsafe_allow_html=True)

    with col_cfg:
        # CSS para botones de configuración ultra-compactos
        st.markdown("""
        <style>
        div[data-testid="stExpander"] {
            background: rgba(15,15,30,.9) !important;
            border: 1px solid rgba(167,139,250,.15) !important;
            border-radius: 12px !important;
        }
        div[data-testid="stExpander"] .stButton button {
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 0.58rem !important;
            font-weight: 700 !important;
            padding: 5px 4px !important;
            min-height: 0 !important;
            height: auto !important;
            line-height: 1.2 !important;
            letter-spacing: 0.2px !important;
            text-transform: uppercase !important;
            white-space: normal !important;
            word-break: break-word !important;
            text-align: center !important;
        }
        </style>
        """, unsafe_allow_html=True)
        with st.expander("⚙️"):
            if st.button("📖\nInstruc.", use_container_width=True):
                st.session_state["_from_juego"] = True
                navegar("instrucciones")
            if st.button("🏠\nInicio", use_container_width=True):
                navegar("inicio")
            if st.button("⬅️\nLobby", use_container_width=True):
                navegar("lobby")


# ══════════════════════════════════════════════════════════════════════════════
#  PANEL DE ESTRELLAS Y ATRIBUTOS
# ══════════════════════════════════════════════════════════════════════════════

def _panel_estrellas(gid, estrellas):
    atributos_activos = st.session_state.get("atributos_activos", set())

    st.markdown(
        "<div style='background:rgba(251,191,36,.04);"
        "border:1px solid rgba(251,191,36,.16);"
        "border-radius:14px;padding:12px 16px;margin-bottom:12px'>"
        "<div style='display:flex;align-items:center;gap:8px;margin-bottom:10px'>"
        "<span style='font-size:1rem'>⭐</span>"
        "<span style='font-family:Courier Prime,monospace;font-size:.68rem;"
        "text-transform:uppercase;letter-spacing:2px;color:#fbbf24;font-weight:700'>"
        "Atributos</span>"
        "<span style='color:rgba(255,255,255,.35);font-size:.68rem'>"
        + str(estrellas) + " disponibles</span>"
        "<span style='margin-left:auto;font-size:.56rem;color:rgba(255,255,255,.2);"
        "font-family:Courier Prime,monospace'>Se consumen al finalizar ronda</span>"
        "</div>",
        unsafe_allow_html=True)

    cols = st.columns(len(ATRIBUTOS))
    for i, (key, atr) in enumerate(ATRIBUTOS.items()):
        activo   = key in atributos_activos
        col      = cols[i]
        puede    = estrellas >= atr["costo"] and not activo
        tipo_col = "#60a5fa" if atr["tipo"] == "pregunta" else "#a78bfa"
        bg_a     = "rgba(52,211,153,.10)" if activo else "rgba(255,255,255,.03)"
        brd_a    = "rgba(52,211,153,.40)" if activo else "rgba(255,255,255,.07)"
        sombra   = "box-shadow:0 0 14px rgba(52,211,153,.20);" if activo else ""
        badge    = (
            "<div style='position:absolute;top:3px;right:3px;"
            "background:rgba(52,211,153,.18);color:#34d399;"
            "font-size:.46rem;border:1px solid rgba(52,211,153,.35);"
            "border-radius:8px;padding:1px 4px'>✓</div>"
        ) if activo else ""

        with col:
            st.markdown(
                "<div style='background:" + bg_a + ";border:1px solid " + brd_a + ";"
                "border-radius:10px;padding:8px 5px;text-align:center;"
                "min-height:98px;position:relative;" + sombra + "'>"
                + badge +
                "<div style='font-size:1.2rem;margin-bottom:2px'>" + atr["emoji"] + "</div>"
                "<div style='font-size:.60rem;font-weight:700;"
                "color:#f1f5f9;line-height:1.2;margin-bottom:2px'>"
                + atr["nombre"] + "</div>"
                "<div style='font-size:.50rem;color:rgba(255,255,255,.25);"
                "line-height:1.25;margin-bottom:4px'>" + atr["desc"] + "</div>"
                "<div style='display:flex;align-items:center;justify-content:center;gap:3px'>"
                "<span style='background:" + tipo_col + "15;color:" + tipo_col + ";"
                "border:1px solid " + tipo_col + "38;border-radius:7px;"
                "padding:1px 4px;font-size:.46rem'>"
                + atr["tipo"].upper() + "</span>"
                "<span style='color:#fbbf24;font-weight:700;font-size:.62rem'>⭐" + str(atr["costo"]) + "</span>"
                "</div></div>",
                unsafe_allow_html=True)

            if activo:
                st.markdown(
                    "<div style='text-align:center;color:#34d399;"
                    "font-size:.56rem;margin-top:2px'>✓ Activo</div>",
                    unsafe_allow_html=True)
            elif puede:
                if st.button("+" + str(atr["costo"]) + "⭐", key="atr_" + key, use_container_width=True):
                    guardar_estrellas(gid, -atr["costo"])
                    activos = st.session_state.get("atributos_activos", set())
                    activos.add(key)
                    st.session_state["atributos_activos"] = activos
                    st.session_state["estrellas_usadas_partida"] = (
                        st.session_state.get("estrellas_usadas_partida", 0) + atr["costo"])
                    st.rerun()
            else:
                falta = atr["costo"] - estrellas
                txt   = "Activo" if activo else "-" + str(falta) + "⭐"
                st.markdown(
                    "<div style='text-align:center;color:rgba(255,255,255,.16);"
                    "font-size:.56rem;margin-top:2px'>" + txt + "</div>",
                    unsafe_allow_html=True)

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
    progreso     = obtener_progreso(gid, dif)
    estudiantes  = obtener_estudiantes(gid)
    cooldowns    = obtener_cooldowns(gid, dif)
    ronda        = progreso["rondaactual"]
    nombre_grp   = st.session_state.get("grupo_nombre", "")
    idx_turno    = (ronda - 1) % len(estudiantes)
    est_turno    = estudiantes[idx_turno]
    dif_cfg      = DIFICULTADES.get(dif, DIFICULTADES["Normal"])
    penalizacion = dif_cfg["penalizacion"]
    estrellas    = obtener_estrellas(gid)

    ind = {
        "economia":         progreso["economia"],
        "medio_ambiente":   progreso["medioambiente"],
        "energia":          progreso["energia"],
        "bienestar_social": progreso["bienestarsocial"],
    }

    if ronda > TOTAL_RONDAS:
        st.session_state.update(resultado="victoria", indicadores_finales=ind,
                                rondas_completadas=TOTAL_RONDAS)
        navegar("fin")
        return
    if any(v <= 0 for v in ind.values()):
        st.session_state.update(resultado="colapso", indicadores_finales=ind,
                                rondas_completadas=ronda - 1)
        navegar("fin")
        return

    _cabecera(nombre_grp, estudiantes, ronda, est_turno, dif, ind, estrellas)
    st.markdown("---")
    fase = st.session_state.get("fase_ronda", "decision")

    # ══════════════════════════════════════════════════════════════════════════
    # FASE DECISIÓN
    # ══════════════════════════════════════════════════════════════════════════
    if fase == "decision":
        _panel_estrellas(gid, estrellas)

        st.markdown(
            "<div style='font-family:Courier Prime,monospace;font-size:.65rem;"
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.25);"
            "margin-bottom:10px'>⚙️ Elige una Decisión Estratégica</div>",
            unsafe_allow_html=True)

        cols = st.columns(4)
        for i, (nom_dec, ef) in enumerate(DECISIONES.items()):
            col          = cols[i % 4]
            cd           = cooldowns.get(nom_dec, 0)
            disp         = cd == 0 or ronda >= cd
            rondas_falta = max(0, cd - ronda) if cd > 0 else 0
            filas_ef = ""
            for k, v in ef.items():
                if k == "emoji": continue
                color_ind, em_ind = IND_COLOR.get(k, ("#94a3b8", ""))
                signo   = "+" if v > 0 else ""
                col_val = "#4ade80" if v > 0 else "#f87171"
                filas_ef += (
                    "<div style='display:flex;justify-content:space-between;"
                    "padding:2px 0;border-bottom:1px solid rgba(255,255,255,.04)'>"
                    "<span style='color:" + color_ind + ";font-size:.68rem'>"
                    + em_ind + " " + IND_LABEL.get(k, k) + "</span>"
                    "<span style='color:" + col_val + ";font-size:.74rem;"
                    "font-weight:700'>" + signo + str(v) + "</span></div>")
            overlay = ""
            if not disp:
                dots = "".join(
                    "<span style='display:inline-block;width:7px;height:7px;"
                    "border-radius:50%;background:"
                    + ("#fbbf24" if j < rondas_falta else "rgba(255,255,255,.08)") + ";"
                    "margin:1px'></span>" for j in range(COOLDOWN))
                overlay = (
                    "<div style='position:absolute;inset:0;border-radius:14px;"
                    "background:rgba(0,0,0,.62);display:flex;flex-direction:column;"
                    "align-items:center;justify-content:center;gap:4px'>"
                    "<span style='font-size:1.1rem'>⏳</span>"
                    "<span style='color:#fbbf24;font-weight:700;font-size:.78rem'>"
                    + str(rondas_falta) + " ronda" + ("s" if rondas_falta != 1 else "") + "</span>"
                    + dots + "</div>")
            borde = "rgba(167,139,250,.32)"  if disp else "rgba(245,158,11,.18)"
            bg    = "rgba(167,139,250,.04)"  if disp else "rgba(245,158,11,.02)"
            with col:
                st.markdown(
                    "<div style='position:relative;background:" + bg + ";"
                    "border:1px solid " + borde + ";border-radius:14px;"
                    "padding:12px;margin-bottom:4px;min-height:165px;"
                    "opacity:" + ("1" if disp else "0.45") + "'>"
                    + overlay +
                    "<div style='font-size:1.3rem;margin-bottom:3px'>" + ef["emoji"] + "</div>"
                    "<div style='font-weight:700;color:#f1f5f9;font-size:.78rem;"
                    "margin-bottom:6px;line-height:1.2'>" + nom_dec + "</div>"
                    + filas_ef + "</div>", unsafe_allow_html=True)
                if st.button("Elegir" if disp else "Bloqueada", disabled=not disp,
                             key="dec_" + nom_dec, use_container_width=True):
                    st.session_state["decision_elegida"] = nom_dec
                    st.session_state["decision_efectos"] = {k: v for k, v in ef.items() if k != "emoji"}
                    st.session_state["pregunta_actual"]  = _seleccionar_pregunta()
                    st.session_state["timer_inicio"]     = None
                    st.session_state["tiempo_agotado"]   = False
                    st.session_state["fase_ronda"]       = "pregunta"
                    dec_u = st.session_state.get("decisiones_usadas_partida", set())
                    dec_u.add(nom_dec)
                    st.session_state["decisiones_usadas_partida"] = dec_u
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE PREGUNTA — countdown automático
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "pregunta":
        pregunta = st.session_state["pregunta_actual"]
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]
        tiempo_total = TIEMPO_PREGUNTA + (15 if _atributo_activo("tiempo_extra") else 0)
        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()
        transcurrido = time.time() - st.session_state["timer_inicio"]
        restante     = max(0.0, tiempo_total - transcurrido)
        pct_timer    = restante / tiempo_total
        seg          = int(restante)
        col_timer    = "#10b981" if pct_timer > 0.5 else "#f59e0b" if pct_timer > 0.25 else "#ef4444"
        urgente      = seg <= 8

        # Atributos activos
        activos_preg = [k for k in st.session_state.get("atributos_activos", set())
                        if ATRIBUTOS.get(k, {}).get("tipo") == "pregunta"]
        if activos_preg:
            badges = "".join(
                "<span style='background:rgba(52,211,153,.08);color:#34d399;"
                "border:1px solid rgba(52,211,153,.25);border-radius:10px;"
                "padding:2px 9px;font-size:.63rem;margin-right:4px'>"
                + ATRIBUTOS[k]["emoji"] + " " + ATRIBUTOS[k]["nombre"] + "</span>"
                for k in activos_preg)
            st.markdown(
                "<div style='background:rgba(52,211,153,.04);"
                "border:1px solid rgba(52,211,153,.15);"
                "border-radius:10px;padding:7px 12px;margin-bottom:10px'>"
                "✨ Activos: " + badges + "</div>", unsafe_allow_html=True)

        # Decisión
        ef_resumen = " ".join(
            "<span style='color:" + IND_COLOR[k][0] + "'>"
            + IND_COLOR[k][1] + " " + ("+" if v > 0 else "") + str(v) + "</span>"
            for k, v in ef_dec.items() if k in IND_COLOR)
        dec_emoji = DECISIONES.get(nom_dec, {}).get("emoji", "")
        st.markdown(
            "<div style='background:rgba(99,102,241,.05);"
            "border:1px solid rgba(99,102,241,.18);"
            "border-radius:10px;padding:8px 14px;margin-bottom:12px'>"
            "<span style='color:#a78bfa;font-size:.72rem'>Decisión: </span>"
            "<span style='color:#f1f5f9;font-weight:700'>" + dec_emoji + " " + nom_dec + "</span>"
            " <span style='color:rgba(255,255,255,.22);font-size:.68rem'>" + ef_resumen + "</span></div>",
            unsafe_allow_html=True)

        # Reloj circular
        radio   = 38
        circunf = 2 * 3.14159 * radio
        offset  = circunf * (1 - pct_timer)
        extra_t = " (+15s)" if _atributo_activo("tiempo_extra") else ""
        alerta  = ("<div style='color:#ef4444;font-size:.68rem;font-weight:700;"
                   "margin-top:6px'>⚠️ ¡Responde ahora!</div>" if urgente else "")
        st.markdown(
            "<div style='background:rgba(0,0,0,.22);"
            "border:1px solid " + col_timer + "22;"
            "border-radius:14px;padding:14px 18px;margin-bottom:14px'>"
            "<div style='display:flex;align-items:center;gap:18px'>"
            "<svg width='88' height='88' viewBox='0 0 88 88'>"
            "<circle cx='44' cy='44' r='" + str(radio) + "' fill='none'"
            " stroke='rgba(255,255,255,.05)' stroke-width='5'/>"
            "<circle cx='44' cy='44' r='" + str(radio) + "' fill='none'"
            " stroke='" + col_timer + "' stroke-width='5'"
            " stroke-dasharray='" + str(round(circunf, 1)) + "'"
            " stroke-dashoffset='" + str(round(offset, 1)) + "'"
            " stroke-linecap='round' transform='rotate(-90 44 44)'"
            " style='transition:stroke-dashoffset .95s linear'/>"
            "<text x='44' y='44' text-anchor='middle' dominant-baseline='central'"
            " fill='" + col_timer + "' font-size='20' font-weight='900'"
            " font-family='Courier Prime,monospace'>" + str(seg) + "</text>"
            "</svg>"
            "<div style='flex:1'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
            "<span style='color:rgba(255,255,255,.35);font-size:.72rem'>"
            "Tiempo restante" + extra_t + "</span>"
            "<span style='color:" + col_timer + ";font-size:.70rem;font-weight:700'>"
            + str(int(pct_timer * 100)) + "%</span></div>"
            "<div style='background:rgba(255,255,255,.05);border-radius:5px;height:8px;overflow:hidden'>"
            "<div style='width:" + str(int(pct_timer * 100)) + "%;height:8px;border-radius:5px;"
            "background:linear-gradient(90deg," + col_timer + "80," + col_timer + ");"
            "transition:width .95s linear'></div></div>"
            + alerta + "</div></div></div>",
            unsafe_allow_html=True)

        # Pregunta
        cat_map = {"Python":"#6366f1","PSeInt":"#8b5cf6","Cálculo":"#06b6d4",
                   "Derivadas":"#10b981","Física MRU":"#f59e0b","Física MRUA":"#ef4444",
                   "Matrices":"#ec4899","Lógica":"#f97316","Álgebra":"#84cc16","Estadística":"#a78bfa"}
        cat_color = cat_map.get(pregunta["cat"], "#a78bfa")
        dif_col_map = {"facil":"#10b981","normal":"#f59e0b","dificil":"#ef4444"}
        dif_lbl_map = {"facil":"FÁCIL","normal":"NORMAL","dificil":"DIFÍCIL"}
        dif_col = dif_col_map.get(pregunta.get("dif","normal"), "#a78bfa")
        dif_lbl = dif_lbl_map.get(pregunta.get("dif","normal"), "")
        st.markdown(
            "<div style='background:rgba(10,10,24,.94);"
            "border:1px solid " + cat_color + "1a;"
            "border-left:3px solid " + cat_color + ";"
            "border-radius:14px;padding:18px 20px;margin-bottom:14px'>"
            "<div style='display:flex;gap:6px;margin-bottom:10px'>"
            "<span style='background:" + cat_color + "14;color:" + cat_color + ";"
            "border:1px solid " + cat_color + "38;border-radius:20px;padding:2px 10px;"
            "font-size:.63rem;font-weight:700'>" + pregunta["cat"] + "</span>"
            "<span style='background:" + dif_col + "14;color:" + dif_col + ";"
            "border:1px solid " + dif_col + "38;border-radius:20px;padding:2px 10px;"
            "font-size:.63rem;font-weight:700'>" + dif_lbl + "</span></div>"
            "<p style='color:#f0f4ff;margin:0;"
            "font-family:Georgia,\"Times New Roman\",serif;"
            "font-size:clamp(.96rem,2.2vw,1.14rem);line-height:1.78'>"
            + pregunta["q"] + "</p></div>", unsafe_allow_html=True)

        opciones  = [chr(65 + i) + ") " + op for i, op in enumerate(pregunta["ops"])]
        respuesta = st.radio("Selecciona tu respuesta:", opciones, key="radio_resp")
        if st.button("✅  Confirmar Respuesta", use_container_width=True, type="primary"):
            idx_resp = opciones.index(respuesta)
            st.session_state["respuesta_correcta"] = (idx_resp == pregunta["ok"])
            st.session_state["tiempo_agotado"]     = False
            st.session_state["resultado_ts"]       = time.time()
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

        if restante <= 0:
            st.session_state["tiempo_agotado"]     = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["resultado_ts"]       = time.time()
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE RESULTADO — countdown automático
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        pregunta = st.session_state["pregunta_actual"]
        correcta = st.session_state["respuesta_correcta"]
        agotado  = st.session_state.get("tiempo_agotado", False)
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]
        es_par   = ronda % 2 == 0
        penaliz  = penalizacion * (dif_cfg.get("mult_par", 1) if es_par else 1)

        if st.session_state.get("resultado_ts") is None:
            st.session_state["resultado_ts"] = time.time()
        restante_res = max(0.0, TIEMPO_RESULTADO - (time.time() - st.session_state["resultado_ts"]))
        seg_res      = int(restante_res) + 1

        if correcta:
            ef_aplicar = dict(ef_dec)
            if _atributo_activo("doble_efecto"):
                ef_aplicar = {k: v * 2 if v > 0 else v for k, v in ef_aplicar.items()}
            nuevo_ind = _aplicar_efectos(ind, ef_aplicar)
            actualizar_progreso(gid, nuevo_ind["economia"], nuevo_ind["medio_ambiente"],
                                nuevo_ind["energia"], nuevo_ind["bienestar_social"], ronda, dif)
            actualizar_cooldown(gid, nom_dec, ronda, dif)
            st.session_state["correctas"] = st.session_state.get("correctas", 0) + 1
            racha = st.session_state.get("racha_actual", 0) + 1
            st.session_state["racha_actual"] = racha
            if racha > st.session_state.get("mejor_racha", 0):
                st.session_state["mejor_racha"] = racha
            doble_msg = ("<div style='margin-top:5px;font-size:.70rem;color:#c4b5fd'>"
                         "✨ Doble Efecto aplicado</div>" if _atributo_activo("doble_efecto") else "")
            st.markdown(
                "<div style='background:rgba(16,185,129,.07);"
                "border:1px solid rgba(16,185,129,.25);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:12px'>"
                "<div style='font-size:2.8rem;margin-bottom:5px'>✅</div>"
                "<h3 style='color:#34d399;margin:0 0 4px;font-size:1.25rem'>¡Respuesta Correcta!</h3>"
                "<p style='color:#6ee7b7;margin:0;font-size:.84rem'>"
                "Efectos de <b>" + nom_dec + "</b> aplicados.</p>"
                + doble_msg + "</div>", unsafe_allow_html=True)
        else:
            if _atributo_activo("segunda_oportunidad") and not agotado:
                activos = st.session_state.get("atributos_activos", set())
                activos.discard("segunda_oportunidad")
                st.session_state["atributos_activos"] = activos
                st.warning("🔄 **Segunda Oportunidad** — responde nuevamente.")
                st.session_state["fase_ronda"]   = "pregunta"
                st.session_state["timer_inicio"] = None
                st.session_state["resultado_ts"] = None
                st.rerun()
            texto_ok      = pregunta["ops"][pregunta["ok"]]
            aviso_par     = ("×2 ronda par (" + str(penaliz) + " pts)" if es_par
                             else "Penalización: " + str(penaliz) + " pts")
            penaliz_final = penaliz
            if _atributo_activo("escudo_ciudad"):
                penaliz_final = max(1, penaliz // 2)
                st.markdown(
                    "<div style='background:rgba(167,139,250,.04);"
                    "border:1px solid rgba(167,139,250,.16);"
                    "border-radius:9px;padding:7px 12px;margin-bottom:7px;"
                    "text-align:center;font-size:.70rem;color:#a78bfa'>"
                    "🛡️ Escudo: " + str(penaliz) + " → " + str(penaliz_final) + " pts</div>",
                    unsafe_allow_html=True)
            nuevo_ind = {k: _clamp(v - penaliz_final) for k, v in ind.items()}
            for ind_key, atr_key in [("economia","prot_economia"),("medio_ambiente","prot_ambiente"),
                                      ("energia","prot_energia"),("bienestar_social","prot_bienestar")]:
                if _atributo_activo(atr_key):
                    nuevo_ind[ind_key] = ind[ind_key]
                    activos = st.session_state.get("atributos_activos", set())
                    activos.discard(atr_key)
                    st.session_state["atributos_activos"] = activos
            actualizar_progreso(gid, nuevo_ind["economia"], nuevo_ind["medio_ambiente"],
                                nuevo_ind["energia"], nuevo_ind["bienestar_social"], ronda, dif)
            st.session_state["incorrectas"]  = st.session_state.get("incorrectas", 0) + 1
            st.session_state["racha_actual"] = 0
            icono_res  = "⏱️" if agotado else "❌"
            titulo_res = "Tiempo Agotado" if agotado else "Respuesta Incorrecta"
            st.markdown(
                "<div style='background:rgba(239,68,68,.07);"
                "border:1px solid rgba(239,68,68,.22);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:12px'>"
                "<div style='font-size:2.8rem;margin-bottom:5px'>" + icono_res + "</div>"
                "<h3 style='color:#f87171;margin:0 0 4px;font-size:1.25rem'>" + titulo_res + "</h3>"
                "<p style='color:#fca5a5;margin:0 0 2px;font-size:.84rem'>"
                "Correcta: <b>" + texto_ok + "</b></p>"
                "<p style='color:#fca5a5;font-size:.76rem;margin:0'>" + aviso_par + "</p></div>",
                unsafe_allow_html=True)

        pct_res = restante_res / TIEMPO_RESULTADO
        col_res = "#34d399" if correcta else "#f87171"
        st.markdown(
            "<div style='background:rgba(255,255,255,.02);"
            "border:1px solid rgba(255,255,255,.06);"
            "border-radius:10px;padding:9px 14px;margin-bottom:8px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
            "<span style='color:rgba(255,255,255,.28);font-size:.66rem'>Avanzando al evento...</span>"
            "<span style='color:" + col_res + ";font-weight:700;font-size:1rem;"
            "font-family:Courier Prime,monospace'>" + str(seg_res) + "s</span></div>"
            "<div style='background:rgba(255,255,255,.05);border-radius:3px;height:5px;overflow:hidden'>"
            "<div style='width:" + str(int(pct_res * 100)) + "%;height:5px;border-radius:3px;"
            "background:" + col_res + ";transition:width .95s linear'></div></div></div>",
            unsafe_allow_html=True)

        if st.button("Continuar al Evento →", use_container_width=True):
            st.session_state["fase_ronda"]   = "evento"
            st.session_state["resultado_ts"] = None
            st.rerun()
        if restante_res <= 0:
            st.session_state["fase_ronda"]   = "evento"
            st.session_state["resultado_ts"] = None
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE EVENTO — countdown automático
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "evento":
        if st.session_state.get("evento_ronda") is None:
            peso_neg = DIFICULTADES.get(dif, DIFICULTADES["Normal"])["eventos_peso"]["negativos"]
            pool     = EVENTOS_NEGATIVOS if random.random() < peso_neg else EVENTOS_POSITIVOS
            st.session_state["evento_ronda"] = random.choice(pool)
            st.session_state["evento_ts"]    = time.time()
        if st.session_state.get("evento_ts") is None:
            st.session_state["evento_ts"] = time.time()

        evento   = st.session_state["evento_ronda"]
        positivo = evento["valor"] > 0
        col_ev   = "#10b981" if positivo else "#ef4444"
        bg_ev    = "rgba(16,185,129,.06)" if positivo else "rgba(239,68,68,.06)"

        restante_ev = max(0.0, TIEMPO_EVENTO - (time.time() - st.session_state["evento_ts"]))
        seg_ev      = int(restante_ev) + 1

        progreso2 = obtener_progreso(gid, dif)
        ind2 = {"economia": progreso2["economia"], "medio_ambiente": progreso2["medioambiente"],
                "energia": progreso2["energia"], "bienestar_social": progreso2["bienestarsocial"]}
        ind_ev    = evento["indicador"]
        val_antes = ind2.get(ind_ev, 50)
        valor_ev  = evento["valor"]
        escudo_msg = ""
        if not positivo and _atributo_activo("escudo_ciudad"):
            valor_ev   = int(valor_ev * 0.5)
            escudo_msg = ("<div style='color:#a78bfa;font-size:.66rem;margin-top:5px'>"
                          "🛡️ Escudo — impacto al 50%</div>")
        nuevo_ind2        = dict(ind2)
        nuevo_ind2[ind_ev] = _clamp(val_antes + valor_ev)
        val_despues        = nuevo_ind2[ind_ev]
        color_ind, em_ind  = IND_COLOR.get(ind_ev, ("#94a3b8", ""))
        signo              = "+" if valor_ev > 0 else ""

        st.markdown(
            "<div style='background:" + bg_ev + ";"
            "border:1px solid " + col_ev + "22;"
            "border-radius:16px;padding:24px;text-align:center'>"
            "<div style='font-size:2rem;margin-bottom:4px'>"
            + ("🌟" if positivo else "⚠️") + "</div>"
            "<div style='font-size:.62rem;color:rgba(255,255,255,.25);"
            "text-transform:uppercase;letter-spacing:2px;margin-bottom:4px'>"
            "Evento · Ronda " + str(ronda) + "</div>"
            "<h2 style='color:#f1f5f9;margin:0 0 14px;font-size:1.18rem'>"
            + evento["nombre"] + "</h2>"
            "<div style='display:inline-flex;align-items:center;gap:12px;"
            "background:rgba(255,255,255,.04);border-radius:10px;padding:10px 20px'>"
            "<span style='color:" + color_ind + ";font-size:.88rem'>"
            + em_ind + " " + IND_LABEL.get(ind_ev, ind_ev) + "</span>"
            "<span style='color:rgba(255,255,255,.18);font-size:1.1rem'>→</span>"
            "<span style='color:" + col_ev + ";font-weight:800;font-size:1.05rem;"
            "font-family:Courier Prime,monospace'>"
            + str(val_antes) + " → " + str(val_despues)
            + " <span style='font-size:.75rem'>(" + signo + str(valor_ev) + ")</span></span>"
            "</div>" + escudo_msg + "</div>",
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        pct_ev = restante_ev / TIEMPO_EVENTO
        st.markdown(
            "<div style='background:rgba(255,255,255,.02);"
            "border:1px solid rgba(255,255,255,.06);"
            "border-radius:10px;padding:9px 14px;margin-bottom:8px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:5px'>"
            "<span style='color:rgba(255,255,255,.25);font-size:.66rem'>Finalizando ronda...</span>"
            "<span style='color:#a78bfa;font-weight:700;font-size:1rem;"
            "font-family:Courier Prime,monospace'>" + str(seg_ev) + "s</span></div>"
            "<div style='background:rgba(255,255,255,.05);border-radius:3px;height:5px;overflow:hidden'>"
            "<div style='width:" + str(int(pct_ev * 100)) + "%;height:5px;border-radius:3px;"
            "background:#a78bfa;transition:width .95s linear'></div></div></div>",
            unsafe_allow_html=True)

        if st.button("Finalizar Ronda " + str(ronda) + "/" + str(TOTAL_RONDAS) + " →",
                     use_container_width=True):
            actualizar_progreso(gid, nuevo_ind2["economia"], nuevo_ind2["medio_ambiente"],
                                nuevo_ind2["energia"], nuevo_ind2["bienestar_social"], ronda + 1, dif)
            st.session_state["atributos_activos"] = set()
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False, decision_elegida=None,
                decision_efectos=None, evento_ronda=None, evento_ts=None,
                resultado_ts=None, fase_ronda="decision", timer_inicio=None, tiempo_agotado=False)
            st.rerun()
        if restante_ev <= 0:
            actualizar_progreso(gid, nuevo_ind2["economia"], nuevo_ind2["medio_ambiente"],
                                nuevo_ind2["energia"], nuevo_ind2["bienestar_social"], ronda + 1, dif)
            st.session_state["atributos_activos"] = set()
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False, decision_elegida=None,
                decision_efectos=None, evento_ronda=None, evento_ts=None,
                resultado_ts=None, fase_ronda="decision", timer_inicio=None, tiempo_agotado=False)
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()
