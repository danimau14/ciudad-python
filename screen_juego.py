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


def _clamp(v): return max(0, min(100, v))


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════

DIF_META = {
    "Fácil":   {"color": "#10b981", "emoji": "🟢", "bg": "rgba(16,185,129,.10)"},
    "Normal":  {"color": "#f59e0b", "emoji": "🟡", "bg": "rgba(245,158,11,.10)"},
    "Difícil": {"color": "#ef4444", "emoji": "🔴", "bg": "rgba(239,68,68,.10)"},
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
        nivel   = random.choices(niveles, weights=[p/total_p for p in pesos], k=1)[0]
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
    """True si el atributo está activo esta ronda."""
    return key in st.session_state.get("atributos_activos", set())


# ══════════════════════════════════════════════════════════════════════════════
#  ENCABEZADO REDISEÑADO
# ══════════════════════════════════════════════════════════════════════════════

def _cabecera(nombre_grp, estudiantes, ronda, est_turno, dif, ind, estrellas):
    dm  = DIF_META.get(dif, DIF_META["Normal"])
    pct = int((ronda - 1) / TOTAL_RONDAS * 100)
    fase_actual = st.session_state.get("fase_ronda", "decision")
    fase_labels = {
        "decision":           ("⚙️", "DECISIÓN",  "#a78bfa"),
        "pregunta":           ("❓", "PREGUNTA",   "#60a5fa"),
        "evento":             ("🌐", "EVENTO",     "#34d399"),
        "resultado_pregunta": ("📊", "RESULTADO",  "#f59e0b"),
    }
    fase_ico, fase_txt, fase_col = fase_labels.get(
        fase_actual, ("●", fase_actual.upper(), "#a78bfa"))

    # ── Chips de ronda ────────────────────────────────────────────────────────
    ronda_chips = ""
    for i in range(1, TOTAL_RONDAS + 1):
        if i < ronda:
            c = "#7c3aed"; op = "1"
        elif i == ronda:
            c = dm["color"]; op = "1"
        else:
            c = "rgba(255,255,255,.10)"; op = "0.6"
        ronda_chips += (
            f"<span style='display:inline-block;width:20px;height:20px;"
            f"border-radius:50%;background:{c};opacity:{op};"
            f"font-size:.58rem;font-weight:700;color:#fff;"
            f"text-align:center;line-height:20px;margin:1px'>{i}</span>")

    # ── Chips de estudiantes ──────────────────────────────────────────────────
    est_chips = ""
    for e in estudiantes:
        activo = (e == est_turno)
        est_chips += (
            f"<span style='display:inline-flex;align-items:center;gap:4px;"
            f"background:{'rgba(167,139,250,.18)' if activo else 'rgba(255,255,255,.04)'};"
            f"border:1px solid {'rgba(167,139,250,.5)' if activo else 'rgba(255,255,255,.07)'};"
            f"border-radius:20px;padding:4px 12px;font-size:.76rem;"
            f"color:{'#c4b5fd' if activo else '#64748b'};"
            f"font-weight:{'700' if activo else '400'};margin:2px'>"
            f"{'✏️ ' if activo else ''}{e}</span>")

    # ── Indicadores compactos ─────────────────────────────────────────────────
    ind_cards = ""
    for key in ["economia", "medio_ambiente", "energia", "bienestar_social"]:
        color, emoji = IND_COLOR[key]
        v  = _clamp(ind.get(key, 50))
        bc = "#10b981" if v >= 60 else "#f59e0b" if v >= 30 else "#ef4444"
        ind_cards += (
            f"<div style='flex:1;min-width:70px;max-width:110px;"
            f"background:rgba(255,255,255,.03);border:1px solid {color}20;"
            f"border-radius:10px;padding:7px 10px;text-align:center'>"
            f"<div style='font-size:.88rem'>{emoji}</div>"
            f"<div style='font-size:.62rem;color:rgba(255,255,255,.35);"
            f"font-family:Courier Prime,monospace;margin:2px 0'>"
            f"{IND_LABEL[key].split()[0]}</div>"
            f"<div style='font-size:.92rem;font-weight:800;color:{bc};"
            f"font-family:Courier Prime,monospace'>{v}</div>"
            f"<div style='width:100%;background:rgba(255,255,255,.07);"
            f"border-radius:3px;height:3px;margin-top:4px'>"
            f"<div style='width:{v}%;background:{color};height:3px;border-radius:3px'></div>"
            f"</div></div>")

    # ── Layout del encabezado ─────────────────────────────────────────────────
    col_hdr, col_cfg = st.columns([5, 1])

    with col_hdr:
        st.markdown(
            f"<div style='background:linear-gradient(135deg,"
            f"rgba(12,12,28,.98),rgba(18,18,40,.95));"
            f"border:1px solid {dm['color']}28;border-radius:18px;"
            f"padding:14px 18px;margin-bottom:10px;"
            f"box-shadow:0 4px 24px rgba(0,0,0,.4)'>"

            # Fila 1: nombre + dificultad + fase + estrellas
            f"<div style='display:flex;align-items:center;gap:8px;"
            f"flex-wrap:wrap;margin-bottom:10px'>"
            f"<span style='font-family:Press Start 2P,monospace;"
            f"font-size:clamp(.65rem,2vw,.9rem);"
            f"background:linear-gradient(90deg,#a78bfa,#60a5fa);"
            f"-webkit-background-clip:text;-webkit-text-fill-color:transparent'>"
            f"🏙️ {nombre_grp}</span>"
            f"<span style='background:{dm[\"bg\"]};color:{dm[\"color\"]};"
            f"border:1px solid {dm[\"color\"]}44;border-radius:20px;"
            f"padding:2px 10px;font-size:.66rem;font-weight:700'>"
            f"{dm['emoji']} {dif}</span>"
            f"<span style='background:{fase_col}18;color:{fase_col};"
            f"border:1px solid {fase_col}44;border-radius:20px;"
            f"padding:2px 10px;font-size:.64rem;font-weight:700'>"
            f"{fase_ico} {fase_txt}</span>"
            f"<span style='margin-left:auto;color:#fbbf24;font-size:.82rem;"
            f"font-weight:700'>⭐ {estrellas}</span>"
            f"</div>"

            # Fila 2: chips estudiantes
            f"<div style='margin-bottom:10px'>{est_chips}</div>"

            # Fila 3: chips de ronda + progreso
            f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>"
            f"<span style='font-size:.58rem;color:rgba(255,255,255,.25);"
            f"font-family:Courier Prime,monospace;white-space:nowrap'>"
            f"R {ronda}/{TOTAL_RONDAS}</span>"
            f"<div style='flex:1'>{ronda_chips}</div>"
            f"<span style='font-size:.62rem;color:{dm[\"color\"]};"
            f"font-weight:700;font-family:Courier Prime,monospace'>"
            f"{pct}%</span></div>"
            f"<div style='background:rgba(255,255,255,.05);"
            f"border-radius:3px;height:3px'>"
            f"<div style='width:{pct}%;background:linear-gradient("
            f"90deg,#7c3aed,{dm[\"color\"]});height:3px;border-radius:3px;"
            f"box-shadow:0 0 6px {dm[\"color\"]}60'></div></div>"
            f"</div>",
            unsafe_allow_html=True)

        # Indicadores
        st.markdown(
            f"<div style='display:flex;gap:6px;flex-wrap:wrap;"
            f"margin-bottom:12px'>{ind_cards}</div>",
            unsafe_allow_html=True)

    with col_cfg:
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        with st.expander("⚙️ Configuración"):
            if st.button("📖 Instrucciones", use_container_width=True):
                st.session_state["_from_juego"] = True
                navegar("instrucciones")
            if st.button("🏠 Volver al Inicio", use_container_width=True):
                navegar("inicio")
            if st.button("⬅️ Volver al Lobby", use_container_width=True):
                navegar("lobby")


# ══════════════════════════════════════════════════════════════════════════════
#  PANEL DE ESTRELLAS Y ATRIBUTOS
#  Reglas:
#    • Cada atributo cuesta N estrellas y se activa SOLO para la ronda actual
#    • Una vez usada la ronda, el atributo se desactiva automáticamente
#    • Para volver a usarlo hay que re-canjearlo con estrellas en otra ronda
#    • Se muestra cuáles están activos esta ronda con un badge verde
# ══════════════════════════════════════════════════════════════════════════════

def _panel_estrellas(gid, estrellas):
    atributos_activos = st.session_state.get("atributos_activos", set())

    st.markdown(
        "<div style='background:rgba(251,191,36,.05);"
        "border:1px solid rgba(251,191,36,.20);"
        "border-radius:16px;padding:14px 18px;margin-bottom:14px'>"
        "<div style='display:flex;align-items:center;gap:10px;margin-bottom:12px'>"
        "<span style='font-size:1.2rem'>⭐</span>"
        "<span style='font-family:Courier Prime,monospace;font-size:.72rem;"
        "text-transform:uppercase;letter-spacing:2px;color:#fbbf24;font-weight:700'>"
        f"Atributos de Ciudad &nbsp;·&nbsp; {estrellas} estrellas disponibles</span>"
        "<span style='margin-left:auto;font-size:.62rem;color:rgba(255,255,255,.3);"
        "font-family:Courier Prime,monospace'>Canjea estrellas · Activo solo esta ronda</span>"
        "</div>",
        unsafe_allow_html=True)

    # Grid de atributos 4 columnas
    cols = st.columns(4)
    for i, (key, atr) in enumerate(ATRIBUTOS.items()):
        activo   = key in atributos_activos
        col      = cols[i % 4]
        puede    = estrellas >= atr["costo"] and not activo
        tipo_col = "#60a5fa" if atr["tipo"] == "pregunta" else "#a78bfa"

        with col:
            # Card del atributo
            bg_a  = "rgba(52,211,153,.10)" if activo  else "rgba(255,255,255,.03)"
            brd_a = "rgba(52,211,153,.45)" if activo  else "rgba(255,255,255,.08)"
            sombra = "box-shadow:0 0 16px rgba(52,211,153,.25);" if activo else ""

            st.markdown(
                f"<div style='background:{bg_a};border:1px solid {brd_a};"
                f"border-radius:12px;padding:10px 8px;text-align:center;"
                f"min-height:115px;position:relative;{sombra}'>"
                + (
                    "<div style='position:absolute;top:5px;right:5px;"
                    "background:rgba(52,211,153,.2);color:#34d399;"
                    "font-size:.52rem;font-family:Courier Prime,monospace;"
                    "border:1px solid rgba(52,211,153,.4);border-radius:10px;"
                    "padding:1px 6px'>✓ ACTIVO</div>"
                    if activo else ""
                )
                + f"<div style='font-size:1.4rem;margin-bottom:4px'>{atr['emoji']}</div>"
                f"<div style='font-size:.68rem;font-weight:700;"
                f"color:#f1f5f9;line-height:1.2;margin-bottom:4px'>"
                f"{atr['nombre']}</div>"
                f"<div style='font-size:.58rem;color:rgba(255,255,255,.3);"
                f"line-height:1.3;margin-bottom:6px'>{atr['desc']}</div>"
                f"<div style='display:flex;align-items:center;justify-content:center;gap:4px'>"
                f"<span style='background:{tipo_col}18;color:{tipo_col};"
                f"border:1px solid {tipo_col}44;border-radius:10px;"
                f"padding:1px 7px;font-size:.55rem;font-family:Courier Prime,monospace'>"
                f"{atr['tipo'].upper()}</span>"
                f"<span style='color:#fbbf24;font-weight:700;font-size:.72rem'>"
                f"⭐ {atr['costo']}</span>"
                f"</div></div>",
                unsafe_allow_html=True)

            if activo:
                st.markdown(
                    "<div style='text-align:center;color:#34d399;"
                    "font-size:.65rem;font-family:Courier Prime,monospace;"
                    "margin-top:3px'>Activo esta ronda</div>",
                    unsafe_allow_html=True)
            elif puede:
                if st.button(
                        f"Canjear {atr['costo']}⭐",
                        key=f"atr_{key}",
                        use_container_width=True):
                    # Descontar estrellas de DB
                    guardar_estrellas(gid, -atr["costo"])
                    # Activar para esta ronda
                    activos = st.session_state.get("atributos_activos", set())
                    activos.add(key)
                    st.session_state["atributos_activos"] = activos
                    # Tracking para logros
                    st.session_state["estrellas_usadas_partida"] = \
                        st.session_state.get("estrellas_usadas_partida", 0) + atr["costo"]
                    st.rerun()
            else:
                motivo = "Activo" if activo else f"Faltan {atr['costo'] - estrellas}⭐"
                st.markdown(
                    f"<div style='text-align:center;color:rgba(255,255,255,.2);"
                    f"font-size:.62rem;font-family:Courier Prime,monospace;"
                    f"margin-top:3px'>{motivo}</div>",
                    unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PANTALLA PRINCIPAL DEL JUEGO
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

    # Verificar colapso o victoria
    if ronda > TOTAL_RONDAS:
        st.session_state.update(
            resultado="victoria",
            indicadores_finales=ind,
            rondas_completadas=TOTAL_RONDAS)
        navegar("fin")
        return

    if any(v <= 0 for v in ind.values()):
        st.session_state.update(
            resultado="colapso",
            indicadores_finales=ind,
            rondas_completadas=ronda - 1)
        navegar("fin")
        return

    # Encabezado rediseñado
    _cabecera(nombre_grp, estudiantes, ronda, est_turno, dif, ind, estrellas)

    st.markdown("---")
    fase = st.session_state.get("fase_ronda", "decision")

    # ══════════════════════════════════════════════════════════════════════════
    # FASE DECISIÓN
    # ══════════════════════════════════════════════════════════════════════════
    if fase == "decision":
        # Panel de estrellas antes de las decisiones
        _panel_estrellas(gid, estrellas)

        st.markdown(
            "<div style='font-family:Courier Prime,monospace;font-size:.68rem;"
            "text-transform:uppercase;letter-spacing:2px;color:rgba(255,255,255,.3);"
            "margin-bottom:10px'>⚙️ Elige una Decisión Estratégica</div>",
            unsafe_allow_html=True)
        st.markdown(
            "<p style='color:rgba(255,255,255,.35);font-size:.8rem;"
            "margin-top:-6px;margin-bottom:14px'>"
            "Si aciertas la pregunta, los efectos se aplicarán a la ciudad.</p>",
            unsafe_allow_html=True)

        cols = st.columns(4)
        for i, (nom_dec, ef) in enumerate(DECISIONES.items()):
            col         = cols[i % 4]
            cd          = cooldowns.get(nom_dec, 0)
            disp        = cd == 0 or ronda >= cd
            rondas_falta = max(0, cd - ronda) if cd > 0 else 0

            filas_ef = ""
            for k, v in ef.items():
                if k == "emoji": continue
                color_ind, em_ind = IND_COLOR.get(k, ("#94a3b8", ""))
                signo   = "+" if v > 0 else ""
                col_val = "#4ade80" if v > 0 else "#f87171"
                filas_ef += (
                    f"<div style='display:flex;justify-content:space-between;"
                    f"padding:2px 0;border-bottom:1px solid rgba(255,255,255,.04)'>"
                    f"<span style='color:{color_ind};font-size:.70rem'>"
                    f"{em_ind} {IND_LABEL.get(k,k)}</span>"
                    f"<span style='color:{col_val};font-size:.78rem;"
                    f"font-weight:700'>{signo}{v}</span></div>")

            overlay = ""
            if not disp:
                dots = "".join(
                    f"<span style='display:inline-block;width:8px;height:8px;"
                    f"border-radius:50%;"
                    f"background:{'#fbbf24' if j < rondas_falta else 'rgba(255,255,255,.1)'};"
                    f"margin:2px'></span>" for j in range(COOLDOWN))
                overlay = (
                    f"<div style='position:absolute;inset:0;border-radius:14px;"
                    f"background:rgba(0,0,0,.55);display:flex;flex-direction:column;"
                    f"align-items:center;justify-content:center;gap:4px'>"
                    f"<span style='font-size:1.2rem'>⏳</span>"
                    f"<span style='color:#fbbf24;font-weight:700;font-size:.82rem'>"
                    f"{rondas_falta} ronda{'s' if rondas_falta!=1 else ''}</span>"
                    f"{dots}</div>")

            borde = "rgba(167,139,250,.4)"  if disp else "rgba(245,158,11,.25)"
            bg    = "rgba(167,139,250,.05)" if disp else "rgba(245,158,11,.03)"

            with col:
                st.markdown(
                    f"<div style='position:relative;background:{bg};"
                    f"border:1px solid {borde};border-radius:14px;"
                    f"padding:13px;margin-bottom:4px;min-height:172px;"
                    f"opacity:{'1' if disp else '0.5'}'>"
                    f"{overlay}"
                    f"<div style='font-size:1.3rem;margin-bottom:4px'>{ef['emoji']}</div>"
                    f"<div style='font-weight:700;color:#f1f5f9;font-size:.82rem;"
                    f"margin-bottom:7px;line-height:1.2'>{nom_dec}</div>"
                    f"{filas_ef}</div>",
                    unsafe_allow_html=True)
                if st.button("Elegir" if disp else "Bloqueada",
                             disabled=not disp,
                             key=f"dec_{nom_dec}",
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
    # FASE PREGUNTA
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "pregunta":
        pregunta = st.session_state["pregunta_actual"]
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]

        # Aplicar atributo tiempo_extra
        tiempo_total = TIEMPO_PREGUNTA
        if _atributo_activo("tiempo_extra"):
            tiempo_total += 15

        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        transcurrido = time.time() - st.session_state["timer_inicio"]
        restante     = max(0.0, tiempo_total - transcurrido)
        pct_timer    = restante / tiempo_total
        seg          = int(restante)
        col_timer    = "#10b981" if pct_timer > 0.5 else "#f59e0b" if pct_timer > 0.25 else "#ef4444"

        # Panel de atributos activos (solo tipo "pregunta")
        activos_pregunta = [
            k for k in st.session_state.get("atributos_activos", set())
            if ATRIBUTOS.get(k, {}).get("tipo") == "pregunta"]
        if activos_pregunta:
            badges = "".join(
                f"<span style='background:rgba(52,211,153,.12);"
                f"color:#34d399;border:1px solid rgba(52,211,153,.35);"
                f"border-radius:10px;padding:2px 10px;font-size:.68rem;"
                f"font-family:Courier Prime,monospace;margin-right:4px'>"
                f"{ATRIBUTOS[k]['emoji']} {ATRIBUTOS[k]['nombre']} ACTIVO</span>"
                for k in activos_pregunta)
            st.markdown(
                f"<div style='background:rgba(52,211,153,.06);"
                f"border:1px solid rgba(52,211,153,.2);"
                f"border-radius:10px;padding:8px 14px;margin-bottom:10px'>"
                f"✨ Atributos activos esta ronda: {badges}</div>",
                unsafe_allow_html=True)

        # Mostrar decisión elegida
        ef_resumen = " ".join(
            f"<span style='color:{IND_COLOR[k][0]}'>"
            f"{IND_COLOR[k][1]} {'+'if v>0 else ''}{v}</span>"
            for k, v in ef_dec.items() if k in IND_COLOR)
        dec_emoji = DECISIONES.get(nom_dec, {}).get("emoji", "")
        st.markdown(
            f"<div style='background:rgba(99,102,241,.07);"
            f"border:1px solid rgba(99,102,241,.22);"
            f"border-radius:10px;padding:9px 16px;margin-bottom:12px'>"
            f"<span style='color:#a78bfa;font-size:.76rem'>Decisión: </span>"
            f"<span style='color:#f1f5f9;font-weight:700'>{dec_emoji} {nom_dec}</span>"
            f"&nbsp;&nbsp;<span style='color:rgba(255,255,255,.28);"
            f"font-size:.73rem'>{ef_resumen}</span></div>",
            unsafe_allow_html=True)

        # Temporizador
        if _atributo_activo("tiempo_extra"):
            timer_badge = (
                "<span style='color:#60a5fa;font-size:.62rem;"
                "font-family:Courier Prime,monospace'> +15s ⏱️</span>")
        else:
            timer_badge = ""

        st.markdown(
            f"<div style='background:rgba(0,0,0,.18);border:1px solid {col_timer}30;"
            f"border-radius:12px;padding:12px 18px;margin-bottom:14px'>"
            f"<div style='display:flex;justify-content:space-between;"
            f"align-items:center;margin-bottom:6px'>"
            f"<span style='color:rgba(255,255,255,.38);font-size:.76rem'>"
            f"Tiempo restante{timer_badge}</span>"
            f"<span style='color:{col_timer};font-weight:900;font-size:1.5rem;"
            f"font-variant-numeric:tabular-nums'>{seg}s</span></div>"
            f"<div style='background:rgba(255,255,255,.06);"
            f"border-radius:4px;height:9px;overflow:hidden'>"
            f"<div style='width:{int(pct_timer*100)}%;height:9px;border-radius:4px;"
            f"background:{col_timer};transition:width .95s linear'></div></div>"
            f"{'<div style=\"color:#ef4444;font-size:.70rem;font-weight:600;margin-top:5px;text-align:center\">¡Responde ya!</div>' if seg <= 8 else ''}"
            f"</div>",
            unsafe_allow_html=True)

        if restante <= 0:
            st.session_state["tiempo_agotado"]     = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

        # Pregunta
        cat_color = {
            "Python":"#6366f1","PSeInt":"#8b5cf6","Cálculo":"#06b6d4",
            "Derivadas":"#10b981","Física MRU":"#f59e0b","Física MRUA":"#ef4444",
            "Matrices":"#ec4899","Lógica":"#f97316","Álgebra":"#84cc16",
            "Estadística":"#a78bfa"}.get(pregunta["cat"], "#a78bfa")
        dif_col = {"facil":"#10b981","normal":"#f59e0b","dificil":"#ef4444"}.get(
            pregunta.get("dif","normal"), "#a78bfa")
        dif_lbl = {"facil":"FÁCIL","normal":"NORMAL","dificil":"DIFÍCIL"}.get(
            pregunta.get("dif","normal"), "")

        st.markdown(
            f"<div style='background:rgba(12,12,26,.9);border:1px solid {cat_color}22;"
            f"border-left:4px solid {cat_color};border-radius:14px;"
            f"padding:20px 22px;margin-bottom:14px'>"
            f"<div style='display:flex;gap:7px;margin-bottom:12px'>"
            f"<span style='background:{cat_color}18;color:{cat_color};"
            f"border:1px solid {cat_color}44;border-radius:20px;padding:2px 10px;"
            f"font-size:.68rem;font-weight:700'>{pregunta['cat']}</span>"
            f"<span style='background:{dif_col}18;color:{dif_col};"
            f"border:1px solid {dif_col}44;border-radius:20px;padding:2px 10px;"
            f"font-size:.68rem;font-weight:700'>{dif_lbl}</span></div>"
            f"<p style='color:#f0f4ff;margin:0;"
            f"font-family:Georgia,\"Times New Roman\",serif;"
            f"font-size:clamp(1rem,2.4vw,1.18rem);line-height:1.75'>"
            f"{pregunta['q']}</p></div>",
            unsafe_allow_html=True)

        opciones  = [f"{chr(65+i)}) {op}" for i, op in enumerate(pregunta["ops"])]
        respuesta = st.radio("Selecciona tu respuesta", opciones, key="radio_resp")

        if st.button("✅  Confirmar Respuesta", use_container_width=True, type="primary"):
            idx_resp = opciones.index(respuesta)
            st.session_state["respuesta_correcta"] = (idx_resp == pregunta["ok"])
            st.session_state["tiempo_agotado"]     = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE RESULTADO PREGUNTA
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        pregunta = st.session_state["pregunta_actual"]
        correcta = st.session_state["respuesta_correcta"]
        agotado  = st.session_state.get("tiempo_agotado", False)
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]
        es_par   = ronda % 2 == 0
        penaliz  = penalizacion * (dif_cfg.get("mult_par", 1) if es_par else 1)

        if correcta:
            # Aplicar doble_efecto si está activo
            ef_aplicar = dict(ef_dec)
            if _atributo_activo("doble_efecto"):
                ef_aplicar = {k: v*2 if v > 0 else v for k, v in ef_aplicar.items()}
                st.markdown(
                    "<div style='background:rgba(167,139,250,.08);"
                    "border:1px solid rgba(167,139,250,.25);"
                    "border-radius:10px;padding:8px 14px;margin-bottom:8px;"
                    "text-align:center;font-size:.78rem;color:#c4b5fd'>"
                    "✨ <b>Doble Efecto activo</b> — efectos positivos duplicados</div>",
                    unsafe_allow_html=True)

            nuevo_ind = _aplicar_efectos(ind, ef_aplicar)
            st.markdown(
                f"<div style='background:rgba(16,185,129,.08);"
                f"border:1px solid rgba(16,185,129,.28);"
                f"border-radius:16px;padding:22px;text-align:center;margin-bottom:14px'>"
                f"<div style='font-size:2.4rem'>✅</div>"
                f"<h3 style='color:#34d399;margin:8px 0 4px'>¡Respuesta Correcta!</h3>"
                f"<p style='color:#6ee7b7'>Los efectos de <b>{nom_dec}</b> se aplicaron.</p>"
                f"</div>",
                unsafe_allow_html=True)
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

        else:
            # Aplicar segunda_oportunidad si está activo y no agotó tiempo
            if _atributo_activo("segunda_oportunidad") and not agotado:
                activos = st.session_state.get("atributos_activos", set())
                activos.discard("segunda_oportunidad")
                st.session_state["atributos_activos"] = activos
                st.warning(
                    "🔄 **Segunda Oportunidad** activada — "
                    "responde nuevamente la misma pregunta.")
                st.session_state["fase_ronda"] = "pregunta"
                st.session_state["timer_inicio"] = None
                st.rerun()

            texto_ok  = pregunta["ops"][pregunta["ok"]]
            aviso_par = (f"Ronda par — penalización doble ({penaliz} pts)"
                         if es_par else f"Penalización: {penaliz} pts")

            # Escudo reduce 50% la penalización en rondas
            penaliz_final = penaliz
            if _atributo_activo("escudo_ciudad"):
                penaliz_final = max(1, penaliz // 2)
                st.markdown(
                    f"<div style='background:rgba(167,139,250,.06);"
                    f"border:1px solid rgba(167,139,250,.2);"
                    f"border-radius:10px;padding:8px 14px;margin-bottom:8px;"
                    f"text-align:center;font-size:.76rem;color:#a78bfa'>"
                    f"🛡️ <b>Escudo de Ciudad</b> activo — "
                    f"penalización reducida: {penaliz} → {penaliz_final}</div>",
                    unsafe_allow_html=True)

            nuevo_ind = {k: _clamp(v - penaliz_final) for k, v in ind.items()}

            # Protecciones individuales de indicadores
            for ind_key, atr_key in [
                ("economia",         "prot_economia"),
                ("medio_ambiente",   "prot_ambiente"),
                ("energia",          "prot_energia"),
                ("bienestar_social", "prot_bienestar"),
            ]:
                if _atributo_activo(atr_key):
                    nuevo_ind[ind_key] = ind[ind_key]  # ignorar penalización en ese indicador
                    activos = st.session_state.get("atributos_activos", set())
                    activos.discard(atr_key)
                    st.session_state["atributos_activos"] = activos

            st.markdown(
                f"<div style='background:rgba(239,68,68,.08);"
                f"border:1px solid rgba(239,68,68,.28);"
                f"border-radius:16px;padding:22px;text-align:center;margin-bottom:14px'>"
                f"<div style='font-size:2.4rem'>{'⏱️' if agotado else '❌'}</div>"
                f"<h3 style='color:#f87171;margin:8px 0 4px'>"
                f"{'Tiempo Agotado' if agotado else 'Respuesta Incorrecta'}</h3>"
                f"<p style='color:#fca5a5'>La correcta era <b>{texto_ok}</b></p>"
                f"<p style='color:#fca5a5'>{aviso_par}</p></div>",
                unsafe_allow_html=True)
            actualizar_progreso(gid,
                                nuevo_ind["economia"], nuevo_ind["medio_ambiente"],
                                nuevo_ind["energia"], nuevo_ind["bienestar_social"],
                                ronda, dif)
            st.session_state["incorrectas"]  = st.session_state.get("incorrectas", 0) + 1
            st.session_state["racha_actual"] = 0

        st.session_state["fase_ronda"] = "evento"
        if st.button("Continuar →", use_container_width=True):
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE EVENTO
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "evento":
        if st.session_state.get("evento_ronda") is None:
            peso_neg = DIFICULTADES.get(dif, DIFICULTADES["Normal"])["eventos_peso"]["negativos"]
            pool     = EVENTOS_NEGATIVOS if random.random() < peso_neg else EVENTOS_POSITIVOS
            st.session_state["evento_ronda"] = random.choice(pool)

        evento   = st.session_state["evento_ronda"]
        positivo = evento["valor"] > 0
        col_ev   = "#10b981" if positivo else "#ef4444"
        bg_ev    = "rgba(16,185,129,.07)" if positivo else "rgba(239,68,68,.07)"

        progreso2 = obtener_progreso(gid, dif)
        ind2 = {
            "economia":         progreso2["economia"],
            "medio_ambiente":   progreso2["medioambiente"],
            "energia":          progreso2["energia"],
            "bienestar_social": progreso2["bienestarsocial"],
        }
        ind_ev     = evento["indicador"]
        val_antes  = ind2.get(ind_ev, 50)

        # Escudo reduce impacto negativo en eventos también
        valor_ev = evento["valor"]
        escudo_msg = ""
        if not positivo and _atributo_activo("escudo_ciudad"):
            valor_ev   = int(valor_ev * 0.5)
            escudo_msg = (
                f"<div style='color:#a78bfa;font-size:.70rem;"
                f"margin-top:6px'>🛡️ Escudo activo — impacto reducido al 50%</div>")

        nuevo_ind2        = dict(ind2)
        nuevo_ind2[ind_ev] = _clamp(val_antes + valor_ev)
        val_despues        = nuevo_ind2[ind_ev]
        color_ind, em_ind  = IND_COLOR.get(ind_ev, ("#94a3b8", ""))
        signo              = "+" if valor_ev > 0 else ""

        st.markdown(
            f"<div style='background:{bg_ev};border:1px solid {col_ev}28;"
            f"border-radius:16px;padding:26px;text-align:center'>"
            f"<div style='font-size:1.8rem'>{'🌟' if positivo else '⚠️'}</div>"
            f"<div style='font-size:.68rem;color:rgba(255,255,255,.30);"
            f"text-transform:uppercase;letter-spacing:2px;margin:5px 0 4px'>"
            f"Evento · Ronda {ronda}</div>"
            f"<h2 style='color:#f1f5f9;margin:0 0 12px;font-size:1.25rem'>"
            f"{evento['nombre']}</h2>"
            f"<div style='display:inline-block;background:rgba(255,255,255,.05);"
            f"border-radius:10px;padding:8px 20px'>"
            f"<span style='color:{color_ind}'>{em_ind} {IND_LABEL.get(ind_ev,ind_ev)}</span>"
            f"<span style='color:rgba(255,255,255,.28);margin:0 8px'>→</span>"
            f"<span style='color:{col_ev};font-weight:700'>"
            f"{val_antes} → {val_despues} ({signo}{valor_ev})</span></div>"
            f"{escudo_msg}</div>",
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"Finalizar Ronda {ronda}/{TOTAL_RONDAS} →",
                     use_container_width=True):
            actualizar_progreso(gid,
                                nuevo_ind2["economia"], nuevo_ind2["medio_ambiente"],
                                nuevo_ind2["energia"], nuevo_ind2["bienestar_social"],
                                ronda + 1, dif)
            # Limpiar atributos de ronda (se consumen al finalizar)
            st.session_state["atributos_activos"] = set()
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False,
                decision_elegida=None, decision_efectos=None,
                evento_ronda=None, fase_ronda="decision",
                timer_inicio=None, tiempo_agotado=False)
            st.rerun()
