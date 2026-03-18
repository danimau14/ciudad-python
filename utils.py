import random, time
import streamlit as st
from config import (PREGUNTAS, MEZCLA_PREGUNTAS, IND_COLOR, IND_LABEL,
                    CAT_COLOR, TOTAL_RONDAS, LOGROS, MISIONES,
                    UMBRAL_COLAPSO, UMBRAL_ROJO, DIFICULTADES)
from database import (obtener_logros_grupo, desbloquear_logro,
                      obtener_misiones_canjeadas, obtener_stats, sumar_estrellas)


# ── Selección de preguntas con mezcla por dificultad ─────────────────────────
def seleccionar_pregunta(dificultad="Normal"):
    usadas = st.session_state.get("preguntas_usadas", [])
    mezcla = MEZCLA_PREGUNTAS.get(dificultad, {"facil":.33,"normal":.34,"dificil":.33})
    pesos  = [mezcla.get(p["dif"], 0.33) for p in PREGUNTAS]
    # Excluir usadas
    disponibles = [(i, pesos[i]) for i in range(len(PREGUNTAS)) if i not in usadas]
    if not disponibles:
        st.session_state["preguntas_usadas"] = []
        disponibles = [(i, pesos[i]) for i in range(len(PREGUNTAS))]
    idxs  = [d[0] for d in disponibles]
    pesos2 = [d[1] for d in disponibles]
    total = sum(pesos2)
    pesos2 = [w/total for w in pesos2]
    idx = random.choices(idxs, weights=pesos2, k=1)[0]
    st.session_state.setdefault("preguntas_usadas", []).append(idx)
    return PREGUNTAS[idx]


# ── Aplicar efectos a indicadores ────────────────────────────────────────────
def aplicar_efectos(ind, efectos):
    r = dict(ind)
    for k, v in efectos.items():
        if k in r:
            r[k] = max(0, min(100, r[k] + v))
    return r


# ── Barra de indicador ────────────────────────────────────────────────────────
def barra_indicador(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    if valor >= 60:
        color, badge = "#10b981", "Estable"
    elif valor >= UMBRAL_ROJO:
        color, badge = "#f59e0b", "Precaución"
    else:
        color, badge = "#ef4444", "Crítico"
    st.markdown(f'''<div style="background:rgba(255,255,255,.04);border:1px solid {color}44;
        border-radius:16px;padding:12px 16px;margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="font-weight:700;color:#f1f5f9;font-family:Outfit,sans-serif">
                {emoji} {nombre}</span>
            <span style="font-size:.72rem;color:{color};font-weight:700;
                background:{color}22;border-radius:20px;padding:2px 9px">{badge}</span>
        </div>
        <div style="background:rgba(255,255,255,.09);border-radius:8px;height:9px">
            <div style="width:{valor}%;background:{color};height:9px;
                border-radius:8px;transition:width .4s ease"></div>
        </div>
        <div style="text-align:right;margin-top:5px;font-size:.82rem;
            font-weight:700;color:{color}">{valor}/100</div>
    </div>''', unsafe_allow_html=True)


# ── Cabecera de juego ─────────────────────────────────────────────────────────
def cabecera_juego(nombre_grp, estudiantes, ronda, est_turno):
    from session_manager import navegar
    top1, top2 = st.columns([3, 1])
    with top1:
        chips = " ".join(
            f'<span style="background:{"rgba(167,139,250,.28)" if e==est_turno else "rgba(255,255,255,.05)"};'
            f'border:1px solid {"rgba(167,139,250,.5)" if e==est_turno else "rgba(255,255,255,.07)"};'
            f'border-radius:20px;padding:3px 12px;margin:2px;font-size:.82rem;'
            f'color:{"#c4b5fd" if e==est_turno else "#94a3b8"};display:inline-block">'
            f'{"▶ " if e==est_turno else ""}{e}</span>' for e in estudiantes)
        st.markdown(f'''<div style="font-size:1.5rem;font-weight:800;
            background:linear-gradient(90deg,#a78bfa,#60a5fa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;margin-bottom:6px">{nombre_grp}</div>
            <div>{chips}</div>''', unsafe_allow_html=True)
    with top2:
        with st.expander("⚙️"):
            if st.button("🏠 Inicio",    use_container_width=True): navegar("inicio")
            if st.button("⬅️ Lobby",     use_container_width=True): navegar("lobby")
            if st.button("📖 Instrucciones", use_container_width=True): navegar("instrucciones")

    m1, m2, m3, m4 = st.columns(4)
    pct = int((ronda - 1) / TOTAL_RONDAS * 100)
    fase = st.session_state.get("fase_ronda", "decision")
    fases_txt = {"decision":"Elegir Decisión","pregunta":"Responder Pregunta",
                 "evento":"Evento Aleatorio","resultado_pregunta":"Resultado"}
    with m1: st.metric("Ronda", f"{ronda}/{TOTAL_RONDAS}")
    with m2: st.metric("Turno", est_turno)
    with m3: st.metric("Progreso", f"{pct}%")
    with m4: st.metric("Fase", fases_txt.get(fase, fase))
    st.markdown(f'''<div style="background:rgba(255,255,255,.06);border-radius:6px;
        height:5px;margin:2px 0 14px">
        <div style="width:{pct}%;background:linear-gradient(90deg,#7c3aed,#a78bfa);
            height:5px;border-radius:6px"></div></div>''', unsafe_allow_html=True)


# ── Calcular puntaje final ────────────────────────────────────────────────────
def calcular_puntaje(ind, correctas, incorrectas):
    prom = sum(ind.values()) / len(ind)
    base = int(prom)
    bonus = correctas * 5
    malus = incorrectas * 3
    return max(0, base + bonus - malus)


def hay_colapso(ind):
    """True si promedio ≤ UMBRAL_COLAPSO o algún indicador en rojo."""
    if any(v <= UMBRAL_ROJO for v in ind.values()):
        return True
    return sum(ind.values()) / len(ind) <= UMBRAL_COLAPSO


# ── Evaluar logros al final de partida ───────────────────────────────────────
def evaluar_logros(gid, ind, correctas, incorrectas, dificultad,
                   racha_max, decisiones_usadas_set, tiempo_seg,
                   estudiantes, correctas_por_est):
    """
    Evalúa todos los logros posibles y desbloquea los nuevos.
    Retorna lista de IDs desbloqueados en esta evaluación.
    """
    ya_tiene = obtener_logros_grupo(gid)
    stats = obtener_stats(gid)
    nuevos = []

    prom = sum(ind.values()) / len(ind)
    todos_sobre_50  = all(v > 50  for v in ind.values())
    todos_sobre_75  = all(v > 75  for v in ind.values())
    victoria = not hay_colapso(ind)

    check = {
        "l01": True,  # primera ronda (llegó al fin)
        "l02": True,  # primera partida completa
        "l03": correctas >= 1,
        "l04": correctas == TOTAL_RONDAS,
        "l05": st.session_state.get("_logro_velocidad", False),
        "l06": racha_max >= 5,
        "l07": racha_max >= 10,
        "l08": stats.get("correctas_total", 0) + correctas >= 50,
        "l09": stats.get("correctas_total", 0) + correctas >= 100,
        "l10": st.session_state.get("_logro_casi_tiempo", False),
        "l11": victoria and dificultad == "Fácil",
        "l12": victoria and dificultad == "Normal",
        "l13": victoria and dificultad == "Difícil",
        "l16": ind.get("medio_ambiente", 0) > 80,
        "l17": ind.get("economia", 0) > 80,
        "l18": ind.get("energia", 0) > 80,
        "l19": ind.get("bienestar_social", 0) > 80,
        "l20": todos_sobre_75,
        "l21": st.session_state.get("_min_global_ok", True),
        "l22": st.session_state.get("_logro_recuperacion", False),
        "l25": len(decisiones_usadas_set) >= 8,
        "l26": "Construir fábrica" not in decisiones_usadas_set and
               "Planta de carbón" not in decisiones_usadas_set,
        "l27": obtener_stats(gid).get("estrellas_check", False),  # se evalúa aparte
        "l35": ind.get("energia",0)>85 and ind.get("medio_ambiente",0)>85,
        "l37": tiempo_seg < 480,
        "l39": len(estudiantes) > 0 and all(correctas_por_est.get(e,0)>=1 for e in estudiantes),
        "l40": st.session_state.get("_correctas_dificil", 0) >= 3,
        "l46": victoria and dificultad=="Fácil"  and correctas==TOTAL_RONDAS,
        "l47": victoria and dificultad=="Normal" and correctas==TOTAL_RONDAS,
        "l48": victoria and dificultad=="Difícil"and correctas==TOTAL_RONDAS,
        "l49": len(estudiantes) == 5,
        "l43": stats.get("partidas_total", 0) + 1 >= 5,
        "l44": stats.get("partidas_total", 0) + 1 >= 10,
        "l45": stats.get("partidas_total", 0) + 1 >= 20,
    }

    for lid, cond in check.items():
        if cond and lid not in ya_tiene:
            if desbloquear_logro(gid, lid):
                nuevos.append(lid)

    return nuevos


# ── Evaluar misiones al final de partida ─────────────────────────────────────
def evaluar_misiones_partida(gid, ind, correctas, dificultad, racha_max, victoria):
    """Retorna lista de misiones cumplidas pero aún no canjeadas."""
    canjeadas = obtener_misiones_canjeadas(gid)
    cumplidas = []
    for m in MISIONES:
        if m["id"] in canjeadas:
            continue
        ok = False
        t = m["tipo"]
        if t == "racha"        and racha_max >= m["meta"]: ok=True
        if t == "indicador"    and ind.get(m.get("ind",""),0) >= m["meta"]: ok=True
        if t == "sin_rojo"     and not any(v<=UMBRAL_ROJO for v in ind.values()): ok=True
        if t == "victoria"     and victoria and (m["dif"]=="todas" or m["dif"]==dificultad): ok=True
        if t == "correctas"    and correctas >= m["meta"]: ok=True
        if t == "todos_sobre"  and all(v>m["meta"] for v in ind.values()): ok=True
        if t == "partidas":
            from database import obtener_stats
            s = obtener_stats(gid)
            if s.get("partidas_total",0)+1 >= m["meta"]: ok=True
        if ok:
            cumplidas.append(m)
    return cumplidas
