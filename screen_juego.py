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

# Tiempo que se muestra el resultado antes de avanzar automáticamente
TIEMPO_RESULTADO = 4   # segundos
TIEMPO_EVENTO    = 5   # segundos


def _clamp(v): return max(0, min(100, v))


DIF_META = {
    "Fácil":   {"color": "#10b981", "emoji": "🟢", "bg": "rgba(16,185,129,.10)", "glow": "rgba(16,185,129,.15)"},
    "Normal":  {"color": "#f59e0b", "emoji": "🟡", "bg": "rgba(245,158,11,.10)", "glow": "rgba(245,158,11,.15)"},
    "Difícil": {"color": "#ef4444", "emoji": "🔴", "bg": "rgba(239,68,68,.10)",  "glow": "rgba(239,68,68,.15)"},
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
#  ENCABEZADO — diseño nuevo
# ══════════════════════════════════════════════════════════════════════════════

def _cabecera(nombre_grp, estudiantes, ronda, est_turno, dif, ind, estrellas):
    dm  = DIF_META.get(dif, DIF_META["Normal"])
    pct = int((ronda - 1) / TOTAL_RONDAS * 100)

    fase_actual = st.session_state.get("fase_ronda", "decision")
    fase_map = {
        "decision":           ("⚙️", "DECISIÓN",  "#a78bfa"),
        "pregunta":           ("❓", "PREGUNTA",   "#60a5fa"),
        "evento":             ("🌐", "EVENTO",     "#34d399"),
        "resultado_pregunta": ("📊", "RESULTADO",  "#f59e0b"),
    }
    fase_ico, fase_txt, fase_col = fase_map.get(fase_actual, ("●", "—", "#a78bfa"))

    # ── Chips de ronda ────────────────────────────────────────────────────────
    ronda_chips = ""
    for i in range(1, TOTAL_RONDAS + 1):
        if i < ronda:
            bg_r = "#7c3aed"; col_r = "#fff"; brd_r = "#7c3aed"
        elif i == ronda:
            bg_r = dm["color"]; col_r = "#000"; brd_r = dm["color"]
        else:
            bg_r = "transparent"; col_r = "rgba(255,255,255,.25)"; brd_r = "rgba(255,255,255,.12)"
        ronda_chips += (
            "<span style='display:inline-flex;align-items:center;justify-content:center;"
            "width:22px;height:22px;border-radius:50%;"
            "background:" + bg_r + ";color:" + col_r + ";"
            "border:1px solid " + brd_r + ";"
            "font-size:.58rem;font-weight:700;margin:1px'>" + str(i) + "</span>")

    # ── Chips de estudiantes ──────────────────────────────────────────────────
    est_chips = ""
    for e in estudiantes:
        activo = (e == est_turno)
        if activo:
            est_chips += (
                "<span style='display:inline-flex;align-items:center;gap:5px;"
                "background:linear-gradient(135deg,rgba(124,58,237,.35),rgba(99,102,241,.25));"
                "border:1px solid rgba(167,139,250,.6);"
                "border-radius:20px;padding:4px 14px;font-size:.78rem;"
                "color:#e9d5ff;font-weight:700;margin:2px;"
                "box-shadow:0 0 10px rgba(167,139,250,.25)'>"
                "✏️ " + e + "</span>")
        else:
            est_chips += (
                "<span style='display:inline-flex;align-items:center;"
                "background:rgba(255,255,255,.04);"
                "border:1px solid rgba(255,255,255,.08);"
                "border-radius:20px;padding:4px 14px;font-size:.78rem;"
                "color:#475569;margin:2px'>" + e + "</span>")

    # ── Indicadores compactos en fila ─────────────────────────────────────────
    ind_html = ""
    for key in ["economia", "medio_ambiente", "energia", "bienestar_social"]:
        color, emoji = IND_COLOR[key]
        v  = _clamp(ind.get(key, 50))
        bc = "#10b981" if v >= 60 else "#f59e0b" if v >= 30 else "#ef4444"
        # Alerta si está en crítico
        ring = "border:1px solid " + bc + "66;" if v < 30 else "border:1px solid " + color + "18;"
        ind_html += (
            "<div style='flex:1;min-width:68px;"
            "background:rgba(255,255,255,.03);" + ring +
            "border-radius:10px;padding:7px 8px;text-align:center;"
            "position:relative'>"
            "<div style='font-size:.9rem'>" + emoji + "</div>"
            "<div style='font-size:.58rem;color:rgba(255,255,255,.3);"
            "letter-spacing:1px;margin:2px 0'>"
            + IND_LABEL[key].split()[0].upper() + "</div>"
            "<div style='font-size:.95rem;font-weight:900;color:" + bc + ";"
            "font-family:Courier Prime,monospace;line-height:1'>" + str(v) + "</div>"
            "<div style='margin-top:4px;background:rgba(255,255,255,.07);"
            "border-radius:3px;height:3px'>"
            "<div style='width:" + str(v) + "%;background:" + color + ";"
            "height:3px;border-radius:3px'></div></div>"
            + ("<div style='position:absolute;top:3px;right:3px;width:6px;height:6px;"
               "border-radius:50%;background:#ef4444;"
               "box-shadow:0 0 4px #ef4444'></div>" if v < 30 else "")
            + "</div>")

    # ── Layout ────────────────────────────────────────────────────────────────
    col_hdr, col_cfg = st.columns([11, 1])

    with col_hdr:
        st.markdown(
            # Contenedor principal
            "<div style='background:linear-gradient(135deg,"
            "rgba(10,10,25,.98),rgba(15,15,35,.96));"
            "border:1px solid " + dm["color"] + "22;"
            "border-top:2px solid " + dm["color"] + "66;"
            "border-radius:16px;"
            "padding:12px 18px 10px;margin-bottom:8px;"
            "box-shadow:0 8px 32px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.04)'>"

            # Fila 1 — nombre grupo | dif + fase | estrellas
            "<div style='display:flex;align-items:center;gap:8px;"
            "flex-wrap:wrap;margin-bottom:10px'>"

            # Nombre grupo
            "<span style='font-family:Press Start 2P,monospace;"
            "font-size:clamp(.6rem,1.8vw,.82rem);"
            "background:linear-gradient(90deg,#c4b5fd,#93c5fd);"
            "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
            "letter-spacing:1px'>🏙️ " + nombre_grp + "</span>"

            # Dificultad
            "<span style='background:" + dm["bg"] + ";color:" + dm["color"] + ";"
            "border:1px solid " + dm["color"] + "44;border-radius:20px;"
            "padding:3px 10px;font-size:.64rem;font-weight:700;letter-spacing:.5px'>"
            + dm["emoji"] + " " + dif + "</span>"

            # Fase actual
            "<span style='background:" + fase_col + "15;color:" + fase_col + ";"
            "border:1px solid " + fase_col + "40;border-radius:20px;"
            "padding:3px 10px;font-size:.62rem;font-weight:700;letter-spacing:.5px'>"
            + fase_ico + " " + fase_txt + "</span>"

            # Estrellas (a la derecha)
            "<div style='margin-left:auto;display:flex;align-items:center;gap:6px'>"
            "<span style='background:rgba(251,191,36,.10);color:#fbbf24;"
            "border:1px solid rgba(251,191,36,.30);border-radius:20px;"
            "padding:3px 12px;font-size:.75rem;font-weight:800;"
            "font-family:Courier Prime,monospace'>⭐ " + str(estrellas) + "</span>"
            "</div></div>"

            # Fila 2 — estudiantes
            "<div style='display:flex;flex-wrap:wrap;gap:2px;margin-bottom:10px'>"
            + est_chips + "</div>"

            # Fila 3 — ronda + barra progreso
            "<div style='display:flex;align-items:center;gap:10px'>"
            "<span style='font-size:.58rem;color:rgba(255,255,255,.2);"
            "font-family:Courier Prime,monospace;white-space:nowrap;"
            "min-width:44px'>R " + str(ronda) + "/" + str(TOTAL_RONDAS) + "</span>"
            "<div style='flex:1;display:flex;align-items:center;gap:3px'>"
            + ronda_chips +
            "</div>"
            "<span style='font-size:.60rem;color:" + dm["color"] + ";"
            "font-weight:700;font-family:Courier Prime,monospace;"
            "min-width:34px;text-align:right'>" + str(pct) + "%</span>"
            "</div>"

            # Barra de progreso continua
            "<div style='margin-top:8px;background:rgba(255,255,255,.05);"
            "border-radius:3px;height:2px;overflow:hidden'>"
            "<div style='width:" + str(pct) + "%;height:2px;"
            "background:linear-gradient(90deg,#7c3aed," + dm["color"] + ");"
            "border-radius:3px;transition:width .5s ease;"
            "box-shadow:0 0 8px " + dm["color"] + "80'></div></div>"
            "</div>",
            unsafe_allow_html=True)

        # Indicadores en fila debajo del header
        st.markdown(
            "<div style='display:flex;gap:5px;margin-bottom:10px'>"
            + ind_html + "</div>",
            unsafe_allow_html=True)

    with col_cfg:
        # CSS para botones pequeños dentro del expander
        st.markdown("""
        <style>
        div[data-testid="stExpander"] .stButton button {
            font-size: 0.62rem !important;
            padding: 5px 6px !important;
            min-height: 0 !important;
            height: auto !important;
            line-height: 1.2 !important;
            letter-spacing: 0.3px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        with st.expander("⚙️"):
            if st.button("📖 Instrucciones", use_container_width=True):
                st.session_state["_from_juego"] = True
                navegar("instrucciones")
            if st.button("🏠 Inicio", use_container_width=True):
                navegar("inicio")
            if st.button("⬅️ Lobby", use_container_width=True):
                navegar("lobby")


# ══════════════════════════════════════════════════════════════════════════════
#  PANEL DE ESTRELLAS Y ATRIBUTOS
# ══════════════════════════════════════════════════════════════════════════════

def _panel_estrellas(gid, estrellas):
    atributos_activos = st.session_state.get("atributos_activos", set())

    st.markdown(
        "<div style='background:rgba(251,191,36,.04);"
        "border:1px solid rgba(251,191,36,.18);"
        "border-radius:14px;padding:12px 16px;margin-bottom:12px'>"
        "<div style='display:flex;align-items:center;gap:8px;margin-bottom:10px'>"
        "<span style='font-size:1rem'>⭐</span>"
        "<span style='font-family:Courier Prime,monospace;font-size:.68rem;"
        "text-transform:uppercase;letter-spacing:2px;color:#fbbf24;font-weight:700'>"
        "Atributos</span>"
        "<span style='color:rgba(255,255,255,.4);font-size:.68rem'>"
        + str(estrellas) + " estrellas disponibles</span>"
        "<span style='margin-left:auto;font-size:.58rem;color:rgba(255,255,255,.25);"
        "font-family:Courier Prime,monospace'>Se consumen al finalizar la ronda</span>"
        "</div>",
        unsafe_allow_html=True)

    cols = st.columns(len(ATRIBUTOS))
    for i, (key, atr) in enumerate(ATRIBUTOS.items()):
        activo   = key in atributos_activos
        col      = cols[i]
        puede    = estrellas >= atr["costo"] and not activo
        tipo_col = "#60a5fa" if atr["tipo"] == "pregunta" else "#a78bfa"
        bg_a     = "rgba(52,211,153,.10)"  if activo else "rgba(255,255,255,.03)"
        brd_a    = "rgba(52,211,153,.40)"  if activo else "rgba(255,255,255,.07)"
        sombra   = "box-shadow:0 0 14px rgba(52,211,153,.20);" if activo else ""

        badge = (
            "<div style='position:absolute;top:4px;right:4px;"
            "background:rgba(52,211,153,.18);color:#34d399;"
            "font-size:.48rem;border:1px solid rgba(52,211,153,.35);"
            "border-radius:8px;padding:1px 5px;font-family:Courier Prime,monospace'>"
            "✓</div>"
        ) if activo else ""

        with col:
            st.markdown(
                "<div style='background:" + bg_a + ";border:1px solid " + brd_a + ";"
                "border-radius:10px;padding:8px 6px;text-align:center;"
                "min-height:100px;position:relative;" + sombra + "'>"
                + badge +
                "<div style='font-size:1.2rem;margin-bottom:3px'>" + atr["emoji"] + "</div>"
                "<div style='font-size:.60rem;font-weight:700;"
                "color:#f1f5f9;line-height:1.2;margin-bottom:3px'>"
                + atr["nombre"] + "</div>"
                "<div style='font-size:.52rem;color:rgba(255,255,255,.28);"
                "line-height:1.3;margin-bottom:5px'>" + atr["desc"] + "</div>"
                "<div style='display:flex;align-items:center;justify-content:center;gap:3px'>"
                "<span style='background:" + tipo_col + "15;color:" + tipo_col + ";"
                "border:1px solid " + tipo_col + "40;border-radius:8px;"
                "padding:1px 5px;font-size:.48rem'>"
                + atr["tipo"].upper() + "</span>"
                "<span style='color:#fbbf24;font-weight:700;font-size:.65rem'>"
                "⭐" + str(atr["costo"]) + "</span>"
                "</div></div>",
                unsafe_allow_html=True)

            if activo:
                st.markdown(
                    "<div style='text-align:center;color:#34d399;"
                    "font-size:.58rem;font-family:Courier Prime,monospace;"
                    "margin-top:2px'>✓ Activo</div>",
                    unsafe_allow_html=True)
            elif puede:
                if st.button("+" + str(atr["costo"]) + "⭐",
                             key="atr_" + key,
                             use_container_width=True):
                    guardar_estrellas(gid, -atr["costo"])
                    activos = st.session_state.get("atributos_activos", set())
                    activos.add(key)
                    st.session_state["atributos_activos"] = activos
                    st.session_state["estrellas_usadas_partida"] = (
                        st.session_state.get("estrellas_usadas_partida", 0) + atr["costo"])
                    st.rerun()
            else:
                falta = atr["costo"] - estrellas
                txt   = "Activo" if activo else ("-" + str(falta) + "⭐")
                st.markdown(
                    "<div style='text-align:center;color:rgba(255,255,255,.18);"
                    "font-size:.58rem;margin-top:2px'>" + txt + "</div>",
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
        st.session_state.update(resultado="victoria",
                                indicadores_finales=ind,
                                rondas_completadas=TOTAL_RONDAS)
        navegar("fin")
        return

    if any(v <= 0 for v in ind.values()):
        st.session_state.update(resultado="colapso",
                                indicadores_finales=ind,
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
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.28);"
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
                if k == "emoji":
                    continue
                color_ind, em_ind = IND_COLOR.get(k, ("#94a3b8", ""))
                signo   = "+" if v > 0 else ""
                col_val = "#4ade80" if v > 0 else "#f87171"
                filas_ef += (
                    "<div style='display:flex;justify-content:space-between;"
                    "padding:2px 0;border-bottom:1px solid rgba(255,255,255,.04)'>"
                    "<span style='color:" + color_ind + ";font-size:.68rem'>"
                    + em_ind + " " + IND_LABEL.get(k, k) + "</span>"
                    "<span style='color:" + col_val + ";font-size:.75rem;"
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
                    "background:rgba(0,0,0,.60);display:flex;flex-direction:column;"
                    "align-items:center;justify-content:center;gap:4px;"
                    "backdrop-filter:blur(2px)'>"
                    "<span style='font-size:1.1rem'>⏳</span>"
                    "<span style='color:#fbbf24;font-weight:700;font-size:.78rem'>"
                    + str(rondas_falta) + " ronda" + ("s" if rondas_falta != 1 else "") + "</span>"
                    + dots + "</div>")

            borde = "rgba(167,139,250,.35)"  if disp else "rgba(245,158,11,.20)"
            bg    = "rgba(167,139,250,.04)"  if disp else "rgba(245,158,11,.02)"
            op    = "1" if disp else "0.45"

            with col:
                st.markdown(
                    "<div style='position:relative;background:" + bg + ";"
                    "border:1px solid " + borde + ";border-radius:14px;"
                    "padding:12px;margin-bottom:4px;min-height:168px;"
                    "opacity:" + op + "'>"
                    + overlay +
                    "<div style='font-size:1.3rem;margin-bottom:4px'>" + ef["emoji"] + "</div>"
                    "<div style='font-weight:700;color:#f1f5f9;font-size:.80rem;"
                    "margin-bottom:7px;line-height:1.2'>" + nom_dec + "</div>"
                    + filas_ef + "</div>",
                    unsafe_allow_html=True)
                if st.button("Elegir" if disp else "Bloqueada",
                             disabled=not disp,
                             key="dec_" + nom_dec,
                             use_container_width=True):
                    st.session_state["decision_elegida"] = nom_dec
                    st.session_state["decision_efectos"] = {
                        k: v for k, v in ef.items() if k != "emoji"}
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

        tiempo_total = TIEMPO_PREGUNTA
        if _atributo_activo("tiempo_extra"):
            tiempo_total += 15

        # Iniciar timer al entrar a esta fase
        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        transcurrido = time.time() - st.session_state["timer_inicio"]
        restante     = max(0.0, tiempo_total - transcurrido)
        pct_timer    = restante / tiempo_total
        seg          = int(restante)
        col_timer    = "#10b981" if pct_timer > 0.5 else "#f59e0b" if pct_timer > 0.25 else "#ef4444"

        # Atributos activos
        activos_preg = [k for k in st.session_state.get("atributos_activos", set())
                        if ATRIBUTOS.get(k, {}).get("tipo") == "pregunta"]
        if activos_preg:
            badges = "".join(
                "<span style='background:rgba(52,211,153,.10);color:#34d399;"
                "border:1px solid rgba(52,211,153,.30);border-radius:10px;"
                "padding:2px 9px;font-size:.65rem;"
                "font-family:Courier Prime,monospace;margin-right:4px'>"
                + ATRIBUTOS[k]["emoji"] + " " + ATRIBUTOS[k]["nombre"] + "</span>"
                for k in activos_preg)
            st.markdown(
                "<div style='background:rgba(52,211,153,.05);"
                "border:1px solid rgba(52,211,153,.18);"
                "border-radius:10px;padding:7px 12px;margin-bottom:10px'>"
                "✨ Activos: " + badges + "</div>",
                unsafe_allow_html=True)

        # Decisión elegida
        ef_resumen = " ".join(
            "<span style='color:" + IND_COLOR[k][0] + "'>"
            + IND_COLOR[k][1] + " " + ("+" if v > 0 else "") + str(v) + "</span>"
            for k, v in ef_dec.items() if k in IND_COLOR)
        dec_emoji = DECISIONES.get(nom_dec, {}).get("emoji", "")
        st.markdown(
            "<div style='background:rgba(99,102,241,.06);"
            "border:1px solid rgba(99,102,241,.20);"
            "border-radius:10px;padding:8px 14px;margin-bottom:12px'>"
            "<span style='color:#a78bfa;font-size:.73rem'>Decisión elegida: </span>"
            "<span style='color:#f1f5f9;font-weight:700'>" + dec_emoji + " " + nom_dec + "</span>"
            " &nbsp;<span style='color:rgba(255,255,255,.25);font-size:.70rem'>"
            + ef_resumen + "</span></div>",
            unsafe_allow_html=True)

        # ── COUNTDOWN grande y visual ─────────────────────────────────────────
        extra_txt = " (+15s)" if _atributo_activo("tiempo_extra") else ""
        urgente   = seg <= 8

        # Aro circular con SVG + número grande
        radio = 38
        circunf = 2 * 3.14159 * radio
        offset  = circunf * (1 - pct_timer)

        st.markdown(
            "<div style='background:rgba(0,0,0,.25);"
            "border:1px solid " + col_timer + "25;"
            "border-radius:16px;padding:14px 20px;margin-bottom:14px'>"

            "<div style='display:flex;align-items:center;gap:20px'>"

            # SVG circular
            "<div style='position:relative;flex-shrink:0'>"
            "<svg width='90' height='90' viewBox='0 0 90 90'>"
            "<circle cx='45' cy='45' r='" + str(radio) + "' fill='none' "
            "stroke='rgba(255,255,255,.06)' stroke-width='5'/>"
            "<circle cx='45' cy='45' r='" + str(radio) + "' fill='none' "
            "stroke='" + col_timer + "' stroke-width='5' "
            "stroke-dasharray='" + str(round(circunf, 1)) + "' "
            "stroke-dashoffset='" + str(round(offset, 1)) + "' "
            "stroke-linecap='round' "
            "transform='rotate(-90 45 45)'/>"
            "<text x='45' y='45' text-anchor='middle' dominant-baseline='central' "
            "fill='" + col_timer + "' font-size='20' font-weight='900' "
            "font-family='Courier Prime,monospace'>" + str(seg) + "</text>"
            "</svg>"
            "</div>"

            # Barra + texto
            "<div style='flex:1'>"
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;margin-bottom:6px'>"
            "<span style='color:rgba(255,255,255,.4);font-size:.73rem'>"
            "Tiempo restante" + extra_txt + "</span>"
            "<span style='color:" + col_timer + ";font-size:.70rem;"
            "font-weight:700;font-family:Courier Prime,monospace'>"
            + str(int(pct_timer * 100)) + "%</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,.06);"
            "border-radius:6px;height:10px;overflow:hidden'>"
            "<div style='width:" + str(int(pct_timer * 100)) + "%;height:10px;"
            "border-radius:6px;background:linear-gradient(90deg,"
            + col_timer + "99," + col_timer + ");"
            "transition:width .95s linear'></div></div>"
            + ("<div style='color:#ef4444;font-size:.70rem;font-weight:700;"
               "margin-top:6px;animation:pulse 0.8s infinite'>⚠️ ¡Responde ahora!</div>"
               if urgente else "") +
            "</div></div></div>",
            unsafe_allow_html=True)

        # ── Pregunta ──────────────────────────────────────────────────────────
        cat_map = {
            "Python": "#6366f1", "PSeInt": "#8b5cf6", "Cálculo": "#06b6d4",
            "Derivadas": "#10b981", "Física MRU": "#f59e0b", "Física MRUA": "#ef4444",
            "Matrices": "#ec4899", "Lógica": "#f97316", "Álgebra": "#84cc16",
            "Estadística": "#a78bfa"}
        cat_color = cat_map.get(pregunta["cat"], "#a78bfa")
        dif_col_map = {"facil": "#10b981", "normal": "#f59e0b", "dificil": "#ef4444"}
        dif_lbl_map = {"facil": "FÁCIL",   "normal": "NORMAL",  "dificil": "DIFÍCIL"}
        dif_col = dif_col_map.get(pregunta.get("dif", "normal"), "#a78bfa")
        dif_lbl = dif_lbl_map.get(pregunta.get("dif", "normal"), "")

        st.markdown(
            "<div style='background:rgba(10,10,24,.92);"
            "border:1px solid " + cat_color + "20;"
            "border-left:3px solid " + cat_color + ";"
            "border-radius:14px;padding:18px 20px;margin-bottom:14px'>"
            "<div style='display:flex;gap:6px;margin-bottom:10px'>"
            "<span style='background:" + cat_color + "15;color:" + cat_color + ";"
            "border:1px solid " + cat_color + "40;border-radius:20px;padding:2px 10px;"
            "font-size:.65rem;font-weight:700'>" + pregunta["cat"] + "</span>"
            "<span style='background:" + dif_col + "15;color:" + dif_col + ";"
            "border:1px solid " + dif_col + "40;border-radius:20px;padding:2px 10px;"
            "font-size:.65rem;font-weight:700'>" + dif_lbl + "</span></div>"
            "<p style='color:#f0f4ff;margin:0;"
            "font-family:Georgia,\"Times New Roman\",serif;"
            "font-size:clamp(.98rem,2.3vw,1.15rem);line-height:1.78'>"
            + pregunta["q"] + "</p></div>",
            unsafe_allow_html=True)

        opciones  = [chr(65 + i) + ") " + op for i, op in enumerate(pregunta["ops"])]
        respuesta = st.radio("Selecciona tu respuesta:", opciones, key="radio_resp")

        if st.button("✅  Confirmar Respuesta", use_container_width=True, type="primary"):
            idx_resp = opciones.index(respuesta)
            st.session_state["respuesta_correcta"] = (idx_resp == pregunta["ok"])
            st.session_state["tiempo_agotado"]     = False
            st.session_state["resultado_ts"]       = time.time()
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

        # ── AUTO-COUNTDOWN: rerun cada segundo ───────────────────────────────
        if restante <= 0:
            st.session_state["tiempo_agotado"]     = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["resultado_ts"]       = time.time()
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()
        else:
            # Pausa 1 segundo y recarga para actualizar el timer automáticamente
            time.sleep(1)
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE RESULTADO PREGUNTA — countdown automático hacia evento
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        pregunta = st.session_state["pregunta_actual"]
        correcta = st.session_state["respuesta_correcta"]
        agotado  = st.session_state.get("tiempo_agotado", False)
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]
        es_par   = ronda % 2 == 0
        penaliz  = penalizacion * (dif_cfg.get("mult_par", 1) if es_par else 1)

        # Timer de resultado
        if st.session_state.get("resultado_ts") is None:
            st.session_state["resultado_ts"] = time.time()
        transcurrido_res = time.time() - st.session_state["resultado_ts"]
        restante_res     = max(0.0, TIEMPO_RESULTADO - transcurrido_res)
        seg_res          = int(restante_res) + 1

        # ── Procesar resultado ────────────────────────────────────────────────
        if correcta:
            ef_aplicar = dict(ef_dec)
            if _atributo_activo("doble_efecto"):
                ef_aplicar = {k: v * 2 if v > 0 else v for k, v in ef_aplicar.items()}

            nuevo_ind = _aplicar_efectos(ind, ef_aplicar)
            actualizar_progreso(gid,
                                nuevo_ind["economia"], nuevo_ind["medio_ambiente"],
                                nuevo_ind["energia"], nuevo_ind["bienestar_social"],
                                ronda, dif)
            actualizar_cooldown(gid, nom_dec, ronda, dif)
            st.session_state["correctas"] = st.session_state.get("correctas", 0) + 1
            racha = st.session_state.get("racha_actual", 0) + 1
            st.session_state["racha_actual"] = racha
            if racha > st.session_state.get("mejor_racha", 0):
                st.session_state["mejor_racha"] = racha

            doble_msg = ""
            if _atributo_activo("doble_efecto"):
                doble_msg = (
                    "<div style='margin-top:6px;font-size:.72rem;color:#c4b5fd'>"
                    "✨ Doble Efecto — efectos positivos duplicados</div>")

            st.markdown(
                "<div style='background:rgba(16,185,129,.08);"
                "border:1px solid rgba(16,185,129,.28);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:14px'>"
                "<div style='font-size:2.8rem;margin-bottom:6px'>✅</div>"
                "<h3 style='color:#34d399;margin:0 0 4px;font-size:1.3rem'>"
                "¡Respuesta Correcta!</h3>"
                "<p style='color:#6ee7b7;margin:0;font-size:.85rem'>"
                "Los efectos de <b>" + nom_dec + "</b> se aplicaron.</p>"
                + doble_msg + "</div>",
                unsafe_allow_html=True)

        else:
            # Segunda oportunidad
            if _atributo_activo("segunda_oportunidad") and not agotado:
                activos = st.session_state.get("atributos_activos", set())
                activos.discard("segunda_oportunidad")
                st.session_state["atributos_activos"] = activos
                st.warning("🔄 **Segunda Oportunidad** — responde nuevamente.")
                st.session_state["fase_ronda"]   = "pregunta"
                st.session_state["timer_inicio"] = None
                st.session_state["resultado_ts"] = None
                st.rerun()

            texto_ok  = pregunta["ops"][pregunta["ok"]]
            aviso_par = ("Ronda par — penalización ×2 (" + str(penaliz) + " pts)"
                         if es_par else "Penalización: " + str(penaliz) + " pts")

            penaliz_final = penaliz
            if _atributo_activo("escudo_ciudad"):
                penaliz_final = max(1, penaliz // 2)
                st.markdown(
                    "<div style='background:rgba(167,139,250,.05);"
                    "border:1px solid rgba(167,139,250,.18);"
                    "border-radius:10px;padding:7px 12px;margin-bottom:8px;"
                    "text-align:center;font-size:.73rem;color:#a78bfa'>"
                    "🛡️ Escudo activo — penalización: "
                    + str(penaliz) + " → " + str(penaliz_final) + "</div>",
                    unsafe_allow_html=True)

            nuevo_ind = {k: _clamp(v - penaliz_final) for k, v in ind.items()}
            prot_map = {
                "economia":         "prot_economia",
                "medio_ambiente":   "prot_ambiente",
                "energia":          "prot_energia",
                "bienestar_social": "prot_bienestar",
            }
            for ind_key, atr_key in prot_map.items():
                if _atributo_activo(atr_key):
                    nuevo_ind[ind_key] = ind[ind_key]
                    activos = st.session_state.get("atributos_activos", set())
                    activos.discard(atr_key)
                    st.session_state["atributos_activos"] = activos

            actualizar_progreso(gid,
                                nuevo_ind["economia"], nuevo_ind["medio_ambiente"],
                                nuevo_ind["energia"], nuevo_ind["bienestar_social"],
                                ronda, dif)
            st.session_state["incorrectas"]  = st.session_state.get("incorrectas", 0) + 1
            st.session_state["racha_actual"] = 0

            icono_res  = "⏱️" if agotado else "❌"
            titulo_res = "Tiempo Agotado" if agotado else "Respuesta Incorrecta"
            st.markdown(
                "<div style='background:rgba(239,68,68,.07);"
                "border:1px solid rgba(239,68,68,.25);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:14px'>"
                "<div style='font-size:2.8rem;margin-bottom:6px'>" + icono_res + "</div>"
                "<h3 style='color:#f87171;margin:0 0 4px;font-size:1.3rem'>"
                + titulo_res + "</h3>"
                "<p style='color:#fca5a5;margin:0 0 2px;font-size:.85rem'>"
                "La correcta era: <b>" + texto_ok + "</b></p>"
                "<p style='color:#fca5a5;font-size:.78rem;margin:0'>"
                + aviso_par + "</p></div>",
                unsafe_allow_html=True)

        # ── Barra de countdown para avanzar ───────────────────────────────────
        pct_res = restante_res / TIEMPO_RESULTADO
        col_res = "#34d399" if correcta else "#f87171"
        st.markdown(
            "<div style='background:rgba(255,255,255,.03);"
            "border:1px solid rgba(255,255,255,.08);"
            "border-radius:10px;padding:10px 16px;margin-bottom:10px'>"
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;margin-bottom:6px'>"
            "<span style='color:rgba(255,255,255,.3);font-size:.68rem'>"
            "Avanzando al evento en...</span>"
            "<span style='color:" + col_res + ";font-weight:700;"
            "font-size:1.1rem;font-family:Courier Prime,monospace'>"
            + str(seg_res) + "s</span></div>"
            "<div style='background:rgba(255,255,255,.06);"
            "border-radius:4px;height:6px;overflow:hidden'>"
            "<div style='width:" + str(int(pct_res * 100)) + "%;height:6px;"
            "border-radius:4px;background:" + col_res + ";transition:width .95s linear'>"
            "</div></div></div>",
            unsafe_allow_html=True)

        # Botón manual para quienes no quieran esperar
        if st.button("Continuar al Evento →", use_container_width=True):
            st.session_state["fase_ronda"]   = "evento"
            st.session_state["resultado_ts"] = None
            st.rerun()

        # ── AUTO-ADVANCE al evento ────────────────────────────────────────────
        if restante_res <= 0:
            st.session_state["fase_ronda"]   = "evento"
            st.session_state["resultado_ts"] = None
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE EVENTO — countdown automático para finalizar ronda
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
        bg_ev    = "rgba(16,185,129,.07)" if positivo else "rgba(239,68,68,.07)"

        transcurrido_ev = time.time() - st.session_state["evento_ts"]
        restante_ev     = max(0.0, TIEMPO_EVENTO - transcurrido_ev)
        seg_ev          = int(restante_ev) + 1

        progreso2 = obtener_progreso(gid, dif)
        ind2 = {
            "economia":         progreso2["economia"],
            "medio_ambiente":   progreso2["medioambiente"],
            "energia":          progreso2["energia"],
            "bienestar_social": progreso2["bienestarsocial"],
        }
        ind_ev    = evento["indicador"]
        val_antes = ind2.get(ind_ev, 50)
        valor_ev  = evento["valor"]

        escudo_msg = ""
        if not positivo and _atributo_activo("escudo_ciudad"):
            valor_ev   = int(valor_ev * 0.5)
            escudo_msg = (
                "<div style='color:#a78bfa;font-size:.68rem;margin-top:6px'>"
                "🛡️ Escudo — impacto reducido al 50%</div>")

        nuevo_ind2        = dict(ind2)
        nuevo_ind2[ind_ev] = _clamp(val_antes + valor_ev)
        val_despues        = nuevo_ind2[ind_ev]
        color_ind, em_ind  = IND_COLOR.get(ind_ev, ("#94a3b8", ""))
        signo              = "+" if valor_ev > 0 else ""

        st.markdown(
            "<div style='background:" + bg_ev + ";"
            "border:1px solid " + col_ev + "25;"
            "border-radius:16px;padding:24px;text-align:center'>"
            "<div style='font-size:2rem;margin-bottom:4px'>"
            + ("🌟" if positivo else "⚠️") + "</div>"
            "<div style='font-size:.65rem;color:rgba(255,255,255,.28);"
            "text-transform:uppercase;letter-spacing:2px;margin-bottom:4px'>"
            "Evento · Ronda " + str(ronda) + "</div>"
            "<h2 style='color:#f1f5f9;margin:0 0 14px;font-size:1.2rem'>"
            + evento["nombre"] + "</h2>"
            "<div style='display:inline-flex;align-items:center;gap:12px;"
            "background:rgba(255,255,255,.04);border-radius:10px;padding:10px 20px'>"
            "<span style='color:" + color_ind + ";font-size:.9rem'>"
            + em_ind + " " + IND_LABEL.get(ind_ev, ind_ev) + "</span>"
            "<span style='color:rgba(255,255,255,.2);font-size:1.2rem'>→</span>"
            "<span style='color:" + col_ev + ";font-weight:800;"
            "font-size:1.1rem;font-family:Courier Prime,monospace'>"
            + str(val_antes) + " → " + str(val_despues)
            + " <span style='font-size:.8rem'>(" + signo + str(valor_ev) + ")</span></span>"
            "</div>"
            + escudo_msg + "</div>",
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Barra de countdown para finalizar ronda
        pct_ev = restante_ev / TIEMPO_EVENTO
        st.markdown(
            "<div style='background:rgba(255,255,255,.03);"
            "border:1px solid rgba(255,255,255,.07);"
            "border-radius:10px;padding:10px 16px;margin-bottom:10px'>"
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;margin-bottom:6px'>"
            "<span style='color:rgba(255,255,255,.3);font-size:.68rem'>"
            "Finalizando ronda en...</span>"
            "<span style='color:#a78bfa;font-weight:700;"
            "font-size:1.1rem;font-family:Courier Prime,monospace'>"
            + str(seg_ev) + "s</span></div>"
            "<div style='background:rgba(255,255,255,.06);"
            "border-radius:4px;height:6px;overflow:hidden'>"
            "<div style='width:" + str(int(pct_ev * 100)) + "%;height:6px;"
            "border-radius:4px;background:#a78bfa;transition:width .95s linear'>"
            "</div></div></div>",
            unsafe_allow_html=True)

        if st.button("Finalizar Ronda " + str(ronda) + "/" + str(TOTAL_RONDAS) + " →",
                     use_container_width=True):
            actualizar_progreso(gid,
                                nuevo_ind2["economia"], nuevo_ind2["medio_ambiente"],
                                nuevo_ind2["energia"], nuevo_ind2["bienestar_social"],
                                ronda + 1, dif)
            st.session_state["atributos_activos"] = set()
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False,
                decision_elegida=None, decision_efectos=None,
                evento_ronda=None, evento_ts=None,
                resultado_ts=None, fase_ronda="decision",
                timer_inicio=None, tiempo_agotado=False)
            st.rerun()

        # ── AUTO-ADVANCE al finalizar el countdown ────────────────────────────
        if restante_ev <= 0:
            actualizar_progreso(gid,
                                nuevo_ind2["economia"], nuevo_ind2["medio_ambiente"],
                                nuevo_ind2["energia"], nuevo_ind2["bienestar_social"],
                                ronda + 1, dif)
            st.session_state["atributos_activos"] = set()
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False,
                decision_elegida=None, decision_efectos=None,
                evento_ronda=None, evento_ts=None,
                resultado_ts=None, fase_ronda="decision",
                timer_inicio=None, tiempo_agotado=False)
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()
