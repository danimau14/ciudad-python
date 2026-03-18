import streamlit as st
import random
import time
from session_manager import navegar
from database import (obtener_progreso, obtener_estudiantes, obtener_cooldowns,
                      actualizar_progreso, actualizar_cooldown, reiniciar_progreso)
from config import (TOTAL_RONDAS, TIEMPO_PREGUNTA, COOLDOWN, DECISIONES, EVENTOS_NEGATIVOS,
                    EVENTOS_POSITIVOS, IND_COLOR, IND_LABEL, PREGUNTAS, DIFICULTADES,
                    MEZCLA_PREGUNTAS)
from ui_styles import pixel_divider


# ── Helpers ───────────────────────────────────────────────────────────────────
def _clamp(v): return max(0, min(100, v))


def _barra_indicador(nombre, valor, color, emoji):
    valor = _clamp(valor)
    badge = "Estable" if valor >= 60 else "Precaución" if valor >= 30 else "Crítico"
    b_col = "#10b981" if valor >= 60 else "#f59e0b" if valor >= 30 else "#ef4444"
    st.markdown(
        f"<div style='background:rgba(255,255,255,.04);border:1px solid {color}33;"
        f"border-radius:14px;padding:12px 16px;margin-bottom:8px'>"
        f"<div style='display:flex;justify-content:space-between;margin-bottom:6px'>"
        f"<span style='font-weight:700;color:#f1f5f9;font-size:.82rem'>{emoji} {nombre}</span>"
        f"<span style='color:{b_col};font-size:.68rem;border:1px solid {b_col}44;"
        f"border-radius:20px;padding:1px 8px'>{badge}</span></div>"
        f"<div style='background:rgba(255,255,255,.08);border-radius:6px;height:8px'>"
        f"<div style='width:{valor}%;background:{color};height:8px;border-radius:6px'></div></div>"
        f"<div style='text-align:right;margin-top:4px;color:{color};"
        f"font-weight:700;font-size:.8rem'>{valor}/100</div></div>",
        unsafe_allow_html=True)


def _seleccionar_pregunta():
    dif_partida = st.session_state.get("dificultad_sel", "Normal")
    mezcla = MEZCLA_PREGUNTAS.get(dif_partida, MEZCLA_PREGUNTAS["Normal"])
    usadas = set(st.session_state.get("preguntas_usadas", []))
    disponibles = [i for i, _ in enumerate(PREGUNTAS) if i not in usadas]
    if not disponibles:
        st.session_state["preguntas_usadas"] = []
        disponibles = list(range(len(PREGUNTAS)))

    # Agrupar por dificultad
    por_dif = {"facil": [], "normal": [], "dificil": []}
    for i in disponibles:
        d = PREGUNTAS[i].get("dif", "normal")
        if d in por_dif:
            por_dif[d].append(i)

    # Elegir nivel con peso
    niveles = [k for k, v in mezcla.items() if por_dif[k]]
    pesos   = [mezcla[k] for k in niveles]
    if not niveles:
        idx = random.choice(disponibles)
    else:
        total_p = sum(pesos)
        pesos_n = [p / total_p for p in pesos]
        nivel = random.choices(niveles, weights=pesos_n, k=1)[0]
        idx = random.choice(por_dif[nivel])

    st.session_state.setdefault("preguntas_usadas", []).append(idx)
    return PREGUNTAS[idx]


def _aplicar_efectos(ind, efectos):
    r = dict(ind)
    for k, v in efectos.items():
        if k in r:
            r[k] = _clamp(r[k] + v)
    return r


def _cabecera(nombre_grp, estudiantes, ronda, est_turno):
    top1, top2 = st.columns([3, 1])
    with top1:
        chips = " ".join(
            f"<span style='background:{'rgba(167,139,250,0.3)' if e == est_turno else 'rgba(255,255,255,0.06)'};"
            f"border:1px solid {'rgba(167,139,250,0.5)' if e == est_turno else 'rgba(255,255,255,0.08)'};"
            f"border-radius:20px;padding:3px 12px;margin:2px;font-size:.82rem;"
            f"color:{'#c4b5fd' if e == est_turno else '#94a3b8'};display:inline-block'>{e}</span>"
            for e in estudiantes)
        st.markdown(
            f"<h2 style='margin:0;font-family:Press Start 2P,monospace;font-size:1rem;"
            f"color:#a78bfa'>{nombre_grp}</h2>"
            f"<div style='margin-top:6px'>{chips}</div>",
            unsafe_allow_html=True)
    with top2:
        with st.expander("⚙️"):
            if st.button("🏠 Salir al lobby", use_container_width=True):
                navegar("lobby")

    m1, m2, m3, m4 = st.columns(4)
    pct = int((ronda - 1) / TOTAL_RONDAS * 100)
    fase_label = {"decision": "Elegir Decisión", "pregunta": "Responder Pregunta",
                  "evento": "Evento Aleatorio", "resultado_pregunta": "Resultado"}
    fase_actual = st.session_state.get("fase_ronda", "decision")
    with m1: st.metric("Ronda", f"{ronda}/{TOTAL_RONDAS}")
    with m2: st.metric("Turno", est_turno)
    with m3: st.metric("Progreso", f"{pct}%")
    with m4: st.metric("Fase", fase_label.get(fase_actual, fase_actual))

    st.markdown(
        f"<div style='background:rgba(255,255,255,.07);border-radius:4px;height:5px;margin:2px 0 14px'>"
        f"<div style='width:{pct}%;background:linear-gradient(90deg,#a78bfa,#60a5fa);"
        f"height:5px;border-radius:4px'></div></div>",
        unsafe_allow_html=True)


# ── Pantalla principal ────────────────────────────────────────────────────────
def pantalla_juego():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    progreso    = obtener_progreso(gid)
    estudiantes = obtener_estudiantes(gid)
    cooldowns   = obtener_cooldowns(gid)
    ronda       = progreso["rondaactual"]
    nombre_grp  = st.session_state.get("grupo_nombre", "")
    idx_turno   = (ronda - 1) % len(estudiantes)
    est_turno   = estudiantes[idx_turno]

    dif_cfg = DIFICULTADES.get(st.session_state.get("dificultad_sel", "Normal"), DIFICULTADES["Normal"])
    penalizacion = dif_cfg["penalizacion"]

    ind = {
        "economia":         progreso["economia"],
        "medio_ambiente":   progreso["medioambiente"],
        "energia":          progreso["energia"],
        "bienestar_social": progreso["bienestarsocial"],
    }

    # Fin por rondas completadas
    if ronda > TOTAL_RONDAS:
        st.session_state.update(
            resultado="victoria",
            indicadores_finales=ind,
            rondas_completadas=TOTAL_RONDAS,
        )
        navegar("fin")
        return

    _cabecera(nombre_grp, estudiantes, ronda, est_turno)

    # Indicadores
    ci1, ci2, ci3, ci4 = st.columns(4)
    for col, key in zip([ci1, ci2, ci3, ci4],
                        ["economia", "medio_ambiente", "energia", "bienestar_social"]):
        color, emoji = IND_COLOR[key]
        with col:
            _barra_indicador(IND_LABEL[key], ind[key], color, emoji)

    st.markdown("---")
    fase = st.session_state.get("fase_ronda", "decision")

    # ── FASE: DECISIÓN ────────────────────────────────────────────────────────
    if fase == "decision":
        st.markdown("### ⚙️ Elige una Decisión Estratégica")
        st.markdown(
            "<p style='color:rgba(255,255,255,.45);font-size:.85rem;margin-top:-8px'>"
            "Si aciertas la pregunta, los efectos se aplicarán a la ciudad.</p>",
            unsafe_allow_html=True)
        cols = st.columns(4)
        for i, (nom_dec, ef) in enumerate(DECISIONES.items()):
            col = cols[i % 4]
            disponibleen = cooldowns.get(nom_dec, 0)
            disp = disponibleen == 0 or ronda >= disponibleen
            rondas_falta = max(0, disponibleen - ronda) if disponibleen > 0 else 0

            filas_ef = ""
            for k, v in ef.items():
                if k == "emoji":
                    continue
                color_ind, em_ind = IND_COLOR.get(k, ("#94a3b8", ""))
                signo = "+" if v > 0 else ""
                col_val = "#4ade80" if v > 0 else "#f87171"
                filas_ef += (
                    f"<div style='display:flex;justify-content:space-between;align-items:center;"
                    f"padding:3px 0;border-bottom:1px solid rgba(255,255,255,.05)'>"
                    f"<span style='color:{color_ind};font-size:.74rem'>{em_ind} {IND_LABEL.get(k,k)}</span>"
                    f"<span style='color:{col_val};font-size:.82rem;font-weight:700'>{signo}{v}</span></div>")

            borde = "rgba(167,139,250,.45)" if disp else "rgba(245,158,11,.35)"
            bg    = "rgba(167,139,250,.07)" if disp else "rgba(245,158,11,.04)"
            opac  = 1 if disp else 0.55
            btn_txt = "Elegir" if disp else "Bloqueada"

            overlay = ""
            if not disp:
                puntos = "".join(
                    f"<span style='display:inline-block;width:10px;height:10px;border-radius:50%;"
                    f"background:{'#fbbf24' if j < rondas_falta else 'rgba(255,255,255,.15)'};"
                    f"margin:2px'></span>"
                    for j in range(COOLDOWN))
                overlay = (
                    f"<div style='position:absolute;inset:0;border-radius:14px;"
                    f"background:rgba(0,0,0,.45);display:flex;flex-direction:column;"
                    f"align-items:center;justify-content:center;gap:6px'>"
                    f"<span style='font-size:1.4rem'>⏳</span>"
                    f"<span style='color:#fbbf24;font-weight:800;font-size:.88rem'>"
                    f"{rondas_falta} ronda{'s' if rondas_falta != 1 else ''}</span>"
                    f"{puntos}"
                    f"<span style='color:rgba(255,255,255,.4);font-size:.66rem'>"
                    f"Disponible ronda {disponibleen}</span></div>")

            with col:
                st.markdown(
                    f"<div style='position:relative;background:{bg};border:1px solid {borde};"
                    f"border-radius:14px;padding:14px 16px;margin-bottom:4px;opacity:{opac};"
                    f"min-height:185px;transition:all .2s'>"
                    f"{overlay}"
                    f"<div style='font-size:1.5rem;margin-bottom:4px'>{ef['emoji']}</div>"
                    f"<div style='font-weight:700;color:#f1f5f9;font-size:.86rem;"
                    f"margin-bottom:8px;line-height:1.2'>{nom_dec}</div>"
                    f"{filas_ef}</div>",
                    unsafe_allow_html=True)
                if st.button(btn_txt, disabled=not disp,
                             key=f"dec_{nom_dec}", use_container_width=True):
                    st.session_state["decision_elegida"] = nom_dec
                    st.session_state["decision_efectos"] = {k: v for k, v in ef.items() if k != "emoji"}
                    st.session_state["pregunta_actual"]  = _seleccionar_pregunta()
                    st.session_state["timer_inicio"]     = None
                    st.session_state["tiempo_agotado"]   = False
                    st.session_state["fase_ronda"]       = "pregunta"
                    st.rerun()

    # ── FASE: PREGUNTA ────────────────────────────────────────────────────────
    elif fase == "pregunta":
        pregunta  = st.session_state["pregunta_actual"]
        nom_dec   = st.session_state["decision_elegida"]
        ef_dec    = st.session_state["decision_efectos"]

        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        tiempo_extra = 15 if st.session_state.get("atributo_tiempo_extra") else 0
        tiempo_total = TIEMPO_PREGUNTA + tiempo_extra
        transcurrido = time.time() - st.session_state["timer_inicio"]
        restante     = max(0.0, tiempo_total - transcurrido)
        pct_timer    = restante / tiempo_total
        seg          = int(restante)
        col_timer    = "#10b981" if pct_timer > 0.5 else "#f59e0b" if pct_timer > 0.25 else "#ef4444"

        # Resumen decisión
        ef_resumen = " ".join(
            f"<span style='color:{IND_COLOR[k][0]}'>{IND_COLOR[k][1]} "
            f"{'+'if v>0 else ''}{v}</span>"
            for k, v in ef_dec.items() if k in IND_COLOR)
        dec_emoji = DECISIONES.get(nom_dec, {}).get("emoji", "")
        st.markdown(
            f"<div style='background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);"
            f"border-radius:12px;padding:10px 18px;margin-bottom:14px;display:flex;"
            f"flex-wrap:wrap;gap:6px;align-items:center'>"
            f"<span style='color:#a78bfa;font-size:.82rem'>Decisión elegida</span>"
            f"<span style='color:#f1f5f9;font-weight:700'>{dec_emoji} {nom_dec}</span>"
            f"<span style='color:rgba(255,255,255,.35);font-size:.78rem'>{ef_resumen}</span></div>",
            unsafe_allow_html=True)

        # Timer
        st.markdown(
            f"<div style='background:rgba(0,0,0,.25);border:1px solid {col_timer}44;"
            f"border-radius:16px;padding:14px 20px;margin-bottom:16px'>"
            f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>"
            f"<span style='color:rgba(255,255,255,.5);font-size:.82rem'>Tiempo restante</span>"
            f"<span style='color:{col_timer};font-weight:900;font-size:1.6rem;"
            f"font-variant-numeric:tabular-nums'>{seg}s</span></div>"
            f"<div style='background:rgba(255,255,255,.08);border-radius:6px;height:12px;overflow:hidden'>"
            f"<div style='width:{int(pct_timer*100)}%;height:12px;border-radius:6px;"
            f"background:linear-gradient(90deg,{col_timer}aa,{col_timer});"
            f"transition:width .95s linear'></div></div>"
            f"{'<div style="color:#ef4444;font-size:.75rem;font-weight:600;margin-top:6px;text-align:center;animation:pulse 0.5s infinite">¡Responde ya!</div>' if seg <= 8 else ''}"
            f"</div>",
            unsafe_allow_html=True)

        if restante <= 0:
            st.session_state["tiempo_agotado"]   = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["fase_ronda"]       = "resultado_pregunta"
            st.rerun()

        # Pregunta
        cat_color = {"Python":"#6366f1","PSeInt":"#8b5cf6","Cálculo":"#06b6d4",
                     "Derivadas":"#10b981","Física MRU":"#f59e0b","Física MRUA":"#ef4444",
                     "Matrices":"#ec4899","Lógica":"#f97316","Álgebra":"#84cc16",
                     "Estadística":"#a78bfa"}.get(pregunta["cat"], "#a78bfa")
        dif_col = {"facil":"#10b981","normal":"#f59e0b","dificil":"#ef4444"}.get(pregunta.get("dif","normal"),"#a78bfa")
        dif_lbl = {"facil":"FÁCIL","normal":"NORMAL","dificil":"DIFÍCIL"}.get(pregunta.get("dif","normal"),"")

        st.markdown(
            f"<div style='background:rgba(15,15,25,.85);border:1px solid {cat_color}33;"
            f"border-radius:14px;padding:18px 22px;margin-bottom:16px'>"
            f"<div style='display:flex;gap:8px;margin-bottom:10px'>"
            f"<span style='background:{cat_color}22;color:{cat_color};"
            f"border:1px solid {cat_color}55;border-radius:20px;padding:2px 12px;"
            f"font-size:.72rem;font-weight:600'>{pregunta['cat']}</span>"
            f"<span style='background:{dif_col}22;color:{dif_col};"
            f"border:1px solid {dif_col}55;border-radius:20px;padding:2px 12px;"
            f"font-size:.72rem;font-weight:600'>{dif_lbl}</span></div>"
            f"<h3 style='color:#f1f5f9;margin:10px 0 0;font-size:clamp(.95rem,2.5vw,1.1rem)'>"
            f"{pregunta['q']}</h3></div>",
            unsafe_allow_html=True)

        opciones = [f"{chr(65+i)}) {op}" for i, op in enumerate(pregunta["ops"])]
        respuesta = st.radio("Selecciona tu respuesta", opciones, key="radio_resp")
        if st.button("✅ Confirmar Respuesta", use_container_width=True, type="primary"):
            idx_resp = opciones.index(respuesta)
            st.session_state["respuesta_correcta"] = (idx_resp == pregunta["ok"])
            st.session_state["tiempo_agotado"]     = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

    # ── FASE: RESULTADO PREGUNTA ──────────────────────────────────────────────
    elif fase == "resultado_pregunta":
        pregunta  = st.session_state["pregunta_actual"]
        correcta  = st.session_state["respuesta_correcta"]
        agotado   = st.session_state.get("tiempo_agotado", False)
        nom_dec   = st.session_state["decision_elegida"]
        ef_dec    = st.session_state["decision_efectos"]
        es_par    = ronda % 2 == 0
        penaliz   = penalizacion * (dif_cfg["mult_par"] if es_par else 1)

        if correcta:
            nuevo_ind = _aplicar_efectos(ind, ef_dec)
            st.markdown(
                f"<div style='background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.35);"
                f"border-radius:16px;padding:22px 26px;text-align:center;margin-bottom:14px'>"
                f"<div style='font-size:2.5rem'>✅</div>"
                f"<h3 style='color:#34d399;margin:8px 0 4px'>¡Respuesta Correcta!</h3>"
                f"<p style='color:#6ee7b7;margin-bottom:10px'>Los efectos de <b>{nom_dec}</b> se aplicaron.</p>"
                f"</div>",
                unsafe_allow_html=True)
            actualizar_progreso(gid,
                nuevo_ind["economia"], nuevo_ind["medio_ambiente"],
                nuevo_ind["energia"], nuevo_ind["bienestar_social"], ronda)
            actualizar_cooldown(gid, nom_dec, ronda)
            st.session_state["correctas"] = st.session_state.get("correctas", 0) + 1
        else:
            texto_ok  = pregunta["ops"][pregunta["ok"]]
            causa     = "Tiempo agotado" if agotado else ""
            aviso_par = f"Ronda par — penalización DOBLE ({penaliz} pts)" if es_par else f"Penalización: {penaliz} pts"
            nuevo_ind = {k: _clamp(v - penaliz) for k, v in ind.items()}
            st.markdown(
                f"<div style='background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.35);"
                f"border-radius:16px;padding:22px 26px;text-align:center;margin-bottom:14px'>"
                f"<div style='font-size:2.5rem'>❌</div>"
                f"{'<h3 style=chr(39)color:#f87171;margin:8px 0 4px chr(39)>Tiempo Agotado</h3>' if agotado else '<h3 style=chr(39)color:#f87171;margin:8px 0 4px chr(39)>Respuesta Incorrecta</h3>'}"
                f"<p style='color:#fca5a5'>La correcta era <b>{texto_ok}</b></p>"
                f"<p style='color:#fca5a5'>{aviso_par}</p></div>",
                unsafe_allow_html=True)
            actualizar_progreso(gid,
                nuevo_ind["economia"], nuevo_ind["medio_ambiente"],
                nuevo_ind["energia"], nuevo_ind["bienestar_social"], ronda)
            st.session_state["incorrectas"] = st.session_state.get("incorrectas", 0) + 1

        st.session_state["fase_ronda"] = "evento"
        if st.button("Continuar →", use_container_width=True):
            st.rerun()

    # ── FASE: EVENTO ──────────────────────────────────────────────────────────
    elif fase == "evento":
        if st.session_state.get("evento_ronda") is None:
            dif_cfg2 = DIFICULTADES.get(st.session_state.get("dificultad_sel", "Normal"), DIFICULTADES["Normal"])
            peso_neg = dif_cfg2["eventos_peso"]["negativos"]
            pool = (EVENTOS_NEGATIVOS if random.random() < peso_neg else EVENTOS_POSITIVOS)
            st.session_state["evento_ronda"] = random.choice(pool)

        evento = st.session_state["evento_ronda"]
        positivo = evento["valor"] > 0
        col_ev = "#10b981" if positivo else "#ef4444"
        bg_ev  = "rgba(16,185,129,.1)" if positivo else "rgba(239,68,68,.1)"
        icono  = "🌟" if positivo else "⚠️"

        progreso2 = obtener_progreso(gid)
        ind2 = {
            "economia":         progreso2["economia"],
            "medio_ambiente":   progreso2["medioambiente"],
            "energia":          progreso2["energia"],
            "bienestar_social": progreso2["bienestarsocial"],
        }
        ind_ev = evento["indicador"]
        valor_antes   = ind2.get(ind_ev, 50)
        nuevo_ind2    = dict(ind2)
        nuevo_ind2[ind_ev] = _clamp(valor_antes + evento["valor"])
        valor_despues = nuevo_ind2[ind_ev]
        color_ind, em_ind = IND_COLOR.get(ind_ev, ("#94a3b8", ""))
        signo = "+" if evento["valor"] > 0 else ""

        st.markdown(
            f"<div style='background:{bg_ev};border:1px solid {col_ev}44;"
            f"border-radius:16px;padding:26px;text-align:center'>"
            f"<div style='font-size:2.2rem'>{icono}</div>"
            f"<div style='font-size:.78rem;color:rgba(255,255,255,.45);text-transform:uppercase;"
            f"letter-spacing:2px;margin:6px 0 2px'>Evento Aleatorio · Ronda {ronda}</div>"
            f"<h2 style='color:#f1f5f9;margin:0 0 10px;font-size:1.4rem'>{evento['nombre']}</h2>"
            f"<div style='display:inline-block;background:rgba(255,255,255,.07);"
            f"border-radius:12px;padding:8px 20px'>"
            f"<span style='color:{color_ind};font-size:1rem'>{em_ind} {IND_LABEL.get(ind_ev,ind_ev)}</span>"
            f"<span style='color:rgba(255,255,255,.35);margin:0 8px'>→</span>"
            f"<span style='color:{col_ev};font-weight:700'>{valor_antes} → {valor_despues}"
            f" ({signo}{evento['valor']})</span></div></div>",
            unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"Finalizar Ronda {ronda}/{TOTAL_RONDAS} →", use_container_width=True):
            actualizar_progreso(gid,
                nuevo_ind2["economia"], nuevo_ind2["medio_ambiente"],
                nuevo_ind2["energia"], nuevo_ind2["bienestar_social"],
                ronda + 1)
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False,
                decision_elegida=None, decision_efectos=None,
                evento_ronda=None, fase_ronda="decision",
                timer_inicio=None, tiempo_agotado=False,
            )
            st.rerun()
