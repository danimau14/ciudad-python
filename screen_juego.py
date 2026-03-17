import streamlit as st
import random
import time

from session_manager import navegar
from database import (obtener_progreso, obtener_estudiantes, obtener_cooldowns,
                      actualizar_progreso, actualizar_cooldown, reiniciar_progreso)
from config import (TOTAL_RONDAS, TIEMPO_PREGUNTA, COOLDOWN,
                    IND_COLOR, IND_LABEL, CAT_COLOR,
                    DECISIONES, EVENTOS, PREGUNTAS, DIFICULTADES)

# ── Utilidades ────────────────────────────────────────────────────────────────

def seleccionar_pregunta():
    disp = [i for i in range(len(PREGUNTAS))
            if i not in st.session_state["preguntas_usadas"]]
    if not disp:
        st.session_state["preguntas_usadas"] = []
        disp = list(range(len(PREGUNTAS)))
    idx = random.choice(disp)
    st.session_state["preguntas_usadas"].append(idx)
    return PREGUNTAS[idx]


def aplicar_efectos(ind, ef):
    r = dict(ind)
    for k, v in ef.items():
        if k in r:
            r[k] = max(0, min(100, r[k] + v))
    return r


def barra_indicador(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    if valor >= 60:   color, badge = "#10b981", "Estable"
    elif valor >= 30: color, badge = "#f59e0b", "Precaución"
    else:             color, badge = "#ef4444", "Crítico"
    bg = ("rgba(16,185,129,0.1)" if valor >= 60
          else "rgba(245,158,11,0.1)" if valor >= 30
          else "rgba(239,68,68,0.1)")
    st.markdown(f'''<div style="background:{bg};border:1px solid {color}44;
        border-radius:14px;padding:14px 18px;margin-bottom:10px">
        <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="font-weight:700;color:#f1f5f9">{emoji} {nombre}</span>
            <span style="font-size:0.72rem;color:{color};font-weight:600">{badge}</span>
        </div>
        <div style="background:rgba(255,255,255,0.1);border-radius:6px;height:8px">
            <div style="width:{valor}%;background:{color};height:8px;border-radius:6px"></div>
        </div>
        <div style="text-align:right;margin-top:5px;font-size:0.82rem;
            font-weight:700;color:{color}">{valor}/100</div>
    </div>''', unsafe_allow_html=True)


def cabecera_juego(nombre_grp, estudiantes, ronda, est_turno):
    top1, top2 = st.columns([3, 1])
    with top1:
        st.markdown(
            f'<h1 style="margin:0;background:linear-gradient(90deg,#a78bfa,#60a5fa);'
            f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            f'background-clip:text;font-size:1.8rem">{nombre_grp}</h1>',
            unsafe_allow_html=True)
        chips = " ".join(
            f'<span style="background:{"rgba(167,139,250,0.3)" if e == est_turno else "rgba(255,255,255,0.06)"};'
            f'border:1px solid {"rgba(167,139,250,0.5)" if e == est_turno else "rgba(255,255,255,0.08)"};'
            f'border-radius:20px;padding:3px 12px;margin:2px;font-size:0.82rem;'
            f'color:{"#c4b5fd" if e == est_turno else "#94a3b8"};display:inline-block">'
            f'{"🎤 " if e == est_turno else ""}{e}</span>'
            for e in estudiantes)
        st.markdown(f'<div style="margin-top:6px">{chips}</div>', unsafe_allow_html=True)
    with top2:
        with st.expander("☰"):
            st.caption("Menú de salida")
            if st.button("📖 Instrucciones",  use_container_width=True): navegar("instrucciones")
            if st.button("🏠 Volver al inicio", use_container_width=True): navegar("inicio")
            if st.button("⬅️ Volver al Lobby", use_container_width=True): navegar("lobby")

    m1, m2, m3, m4 = st.columns(4)
    pct = int((ronda - 1) / TOTAL_RONDAS * 100)
    fase_label = st.session_state.get("fase_ronda", "decision")
    fases_txt  = {"decision": "Elegir Decisión", "pregunta": "Responder Pregunta",
                  "evento": "Evento Aleatorio", "resultado_pregunta": "Resultado"}
    with m1: st.metric("Ronda",    f"{ronda}/{TOTAL_RONDAS}")
    with m2: st.metric("Turno",    est_turno)
    with m3: st.metric("Progreso", f"{pct}%")
    with m4: st.metric("Fase",     fases_txt.get(fase_label, fase_label))
    st.markdown(
        f'<div style="background:rgba(255,255,255,0.07);border-radius:4px;height:5px;margin:2px 0 14px">'
        f'<div style="width:{pct}%;background:linear-gradient(90deg,#a78bfa,#60a5fa);'
        f'height:5px;border-radius:4px"></div></div>', unsafe_allow_html=True)


# ── Pantalla principal ────────────────────────────────────────────────────────

def pantalla_juego():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    progreso   = obtener_progreso(gid)
    estudiantes = obtener_estudiantes(gid)
    cooldowns   = obtener_cooldowns(gid)
    ronda       = progreso["ronda_actual"]
    nombre_grp  = st.session_state["grupo_nombre"]
    dificultad  = st.session_state.get("dificultad_sel", "Normal")
    cfg_dif     = DIFICULTADES.get(dificultad, DIFICULTADES["Normal"])
    penalizacion_base = cfg_dif["penalizacion"]

    idx_turno  = (ronda - 1) % len(estudiantes)
    est_turno  = estudiantes[idx_turno]

    ind = {
        "economia":        progreso["economia"],
        "medio_ambiente":  progreso["medio_ambiente"],
        "energia":         progreso["energia"],
        "bienestar_social":progreso["bienestar_social"],
    }

    # ── Fin de juego ──────────────────────────────────────────────────────────
    if ronda > TOTAL_RONDAS:
        st.session_state.update({
            "resultado": "victoria",
            "indicadores_finales": ind,
            "rondas_completadas": TOTAL_RONDAS,
        })
        navegar("fin")
        return

    cabecera_juego(nombre_grp, estudiantes, ronda, est_turno)

    ci1, ci2, ci3, ci4 = st.columns(4)
    with ci1: barra_indicador("Economía",       ind["economia"],        "💰")
    with ci2: barra_indicador("Medio Ambiente", ind["medio_ambiente"],  "🌿")
    with ci3: barra_indicador("Energía",        ind["energia"],         "⚡")
    with ci4: barra_indicador("Bienestar",      ind["bienestar_social"],"❤️")
    st.markdown("---")

    fase = st.session_state.get("fase_ronda", "decision")

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 1 — DECISIÓN
    # ══════════════════════════════════════════════════════════════════════════
    if fase == "decision":
        st.markdown("### Paso 1: Elige una Decisión Estratégica")
        st.markdown('<p style="color:rgba(255,255,255,0.45);font-size:0.85rem;margin-top:-8px">'
                    'Si aciertas la pregunta, los efectos de esta decisión se aplicarán a la ciudad.</p>',
                    unsafe_allow_html=True)

        cols = st.columns(4)
        for i, (nom_dec, ef) in enumerate(DECISIONES.items()):
            col = cols[i % 4]
            disponible_en = cooldowns.get(nom_dec, 0)
            disp          = disponible_en == 0 or ronda >= disponible_en
            rondas_falta  = max(0, disponible_en - ronda) if disponible_en > 0 else 0

            # Filas de efectos
            filas_ef = ""
            for k, v in ef.items():
                if k == "emoji": continue
                col_ind, em_ind = IND_COLOR.get(k, ("#94a3b8", ""))
                signo   = "+" if v > 0 else ""
                col_val = "#4ade80" if v > 0 else "#f87171"
                filas_ef += (
                    f'<div style="display:flex;justify-content:space-between;'
                    f'align-items:center;padding:4px 0;'
                    f'border-bottom:1px solid rgba(255,255,255,0.05)">'
                    f'<span style="color:{col_ind};font-size:0.76rem">{em_ind} {IND_LABEL[k]}</span>'
                    f'<span style="color:{col_val};font-size:0.84rem;font-weight:700">'
                    f'{signo}{v}</span></div>'
                )

            if disp:
                borde, bg_card, opac = "rgba(167,139,250,0.45)", "rgba(167,139,250,0.07)", 1
                overlay, btn_txt     = "", "Elegir"
            else:
                borde, bg_card, opac = "rgba(245,158,11,0.35)", "rgba(245,158,11,0.04)", 0.55
                puntos_html = " ".join(
                    f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;'
                    f'background:{"#fbbf24" if j < rondas_falta else "rgba(255,255,255,0.15)"};'
                    f'margin:2px"></span>' for j in range(COOLDOWN))
                overlay = (
                    f'<div style="position:absolute;inset:0;border-radius:14px;'
                    f'background:rgba(0,0,0,0.45);display:flex;flex-direction:column;'
                    f'align-items:center;justify-content:center;gap:6px">'
                    f'<span style="font-size:1.6rem">⏳</span>'
                    f'<span style="color:#fbbf24;font-weight:800;font-size:0.9rem">'
                    f'{rondas_falta} ronda{"s" if rondas_falta != 1 else ""}</span>'
                    f'<div>{puntos_html}</div>'
                    f'<span style="color:rgba(255,255,255,0.45);font-size:0.68rem">'
                    f'Disponible en ronda {disponible_en}</span></div>'
                )
                btn_txt = "Bloqueada"

            with col:
                st.markdown(
                    f'<div style="position:relative;background:{bg_card};'
                    f'border:1px solid {borde};border-radius:14px;padding:14px 16px;'
                    f'margin-bottom:4px;opacity:{opac};min-height:185px;transition:all 0.2s">'
                    f'{overlay}'
                    f'<div style="font-size:1.6rem;margin-bottom:4px">{ef["emoji"]}</div>'
                    f'<div style="font-weight:700;color:#f1f5f9;font-size:0.88rem;'
                    f'margin-bottom:8px;line-height:1.2">{nom_dec}</div>'
                    f'{filas_ef}</div>', unsafe_allow_html=True)
                if st.button(btn_txt, disabled=not disp,
                             key=f"dec_{nom_dec}", use_container_width=True):
                    st.session_state["decision_elegida"]  = nom_dec
                    st.session_state["decision_efectos"]  = {k: v for k, v in ef.items() if k != "emoji"}
                    st.session_state["pregunta_actual"]   = seleccionar_pregunta()
                    st.session_state["timer_inicio"]      = None
                    st.session_state["tiempo_agotado"]    = False
                    st.session_state["fase_ronda"]        = "pregunta"
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 2 — PREGUNTA
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "pregunta":
        pregunta = st.session_state["pregunta_actual"]
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]

        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        timer_ini        = st.session_state["timer_inicio"]
        tiempo_transcurrido = time.time() - timer_ini
        tiempo_restante  = max(0.0, TIEMPO_PREGUNTA - tiempo_transcurrido)
        pct_timer        = tiempo_restante / TIEMPO_PREGUNTA
        seg              = int(tiempo_restante)
        col_timer        = ("#10b981" if pct_timer > 0.5
                            else "#f59e0b" if pct_timer > 0.25 else "#ef4444")

        # Resumen decisión elegida
        ef_resumen = " ".join(
            f'<span style="color:{IND_COLOR[k][0]}">{IND_COLOR[k][1]} '
            f'{"+" if v > 0 else ""}{v}</span>'
            for k, v in ef_dec.items() if k in IND_COLOR)
        dec_emoji = DECISIONES.get(nom_dec, {}).get("emoji", "")
        st.markdown(
            f'<div style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.3);'
            f'border-radius:12px;padding:10px 18px;margin-bottom:14px;'
            f'display:flex;flex-wrap:wrap;gap:6px;align-items:center">'
            f'<span style="color:#a78bfa;font-size:0.82rem">Decisión elegida:</span>'
            f'<span style="color:#f1f5f9;font-weight:700">{dec_emoji} {nom_dec}</span>'
            f'<span style="color:rgba(255,255,255,0.35);font-size:0.78rem">{ef_resumen}</span>'
            f'</div>', unsafe_allow_html=True)

        # Temporizador
        st.markdown(
            f'<div style="background:rgba(0,0,0,0.25);border:1px solid {col_timer}44;'
            f'border-radius:16px;padding:14px 20px;margin-bottom:16px">'
            f'<div style="display:flex;justify-content:space-between;'
            f'align-items:center;margin-bottom:8px">'
            f'<span style="color:rgba(255,255,255,0.5);font-size:0.82rem">Tiempo restante</span>'
            f'<span style="color:{col_timer};font-weight:900;'
            f'font-size:clamp(1.3rem,4vw,1.8rem);font-variant-numeric:tabular-nums">'
            f'{seg}s</span></div>'
            f'<div style="background:rgba(255,255,255,0.08);border-radius:6px;height:12px;overflow:hidden">'
            f'<div style="width:{int(pct_timer*100)}%;height:12px;border-radius:6px;'
            f'background:linear-gradient(90deg,{col_timer}aa,{col_timer});'
            f'transition:width 0.95s linear,background 0.95s"></div></div>'
            f'{"<div style=\'color:#ef4444;font-size:0.75rem;font-weight:600;margin-top:6px;text-align:center;animation:pulse 0.5s infinite\'>¡Responde ya!</div>" if seg <= 8 else ""}'
            f'</div>', unsafe_allow_html=True)

        # Tarjeta pregunta
        cat_color = CAT_COLOR.get(pregunta["cat"], "#94a3b8")
        st.markdown(
            f'<div class="card-glow">'
            f'<span style="background:{cat_color}22;color:{cat_color};'
            f'border:1px solid {cat_color}55;border-radius:20px;padding:2px 12px;'
            f'font-size:0.72rem;font-weight:600">{pregunta["cat"]}</span>'
            f'<h3 style="color:#f1f5f9;margin:10px 0 0;'
            f'font-size:clamp(0.95rem,2.5vw,1.1rem)">{pregunta["q"]}</h3>'
            f'</div>', unsafe_allow_html=True)

        opciones_letras = [f"{chr(65+i)}. {op}" for i, op in enumerate(pregunta["ops"])]

        if tiempo_restante <= 0:
            st.session_state["tiempo_agotado"]   = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["fase_ronda"]        = "resultado_pregunta"
            st.rerun()

        respuesta = st.radio("Selecciona tu respuesta:", opciones_letras, key="radio_resp")
        if st.button("Confirmar Respuesta ✅", use_container_width=True):
            idx_resp = opciones_letras.index(respuesta)
            st.session_state["respuesta_correcta"] = (idx_resp == pregunta["ok"])
            st.session_state["tiempo_agotado"]     = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

        time.sleep(1)
        st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 3 — RESULTADO PREGUNTA
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        pregunta = st.session_state["pregunta_actual"]
        correcta = st.session_state["respuesta_correcta"]
        agotado  = st.session_state.get("tiempo_agotado", False)
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]
        es_par   = ronda % 2 == 0
        penalizacion = int(penalizacion_base * (1.5 if es_par else 1.0))

        if correcta:
            st.session_state["correctas"] = st.session_state.get("correctas", 0) + 1
            nueva_ind = aplicar_efectos(ind, ef_dec)
            actualizar_progreso(gid, nueva_ind["economia"], nueva_ind["medio_ambiente"],
                                nueva_ind["energia"], nueva_ind["bienestar_social"], ronda)
            actualizar_cooldown(gid, nom_dec, ronda)

            cambios_html = ""
            for k, v in ef_dec.items():
                if k not in IND_COLOR: continue
                col_ind, em_ind = IND_COLOR[k]
                signo   = "+" if v > 0 else ""
                col_v   = "#4ade80" if v > 0 else "#f87171"
                cambios_html += (
                    f'<span style="background:rgba(255,255,255,0.07);border-radius:8px;'
                    f'padding:4px 10px;margin:3px;display:inline-block;'
                    f'color:#f1f5f9;font-size:0.85rem">'
                    f'{em_ind} {IND_LABEL[k]} <b style="color:{col_v}">{signo}{v}</b></span>'
                )
            st.markdown(
                f'<div style="background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.35);'
                f'border-radius:16px;padding:22px 26px;text-align:center;margin-bottom:14px">'
                f'<div style="font-size:2.5rem">✅</div>'
                f'<h3 style="color:#34d399;margin:8px 0 4px">¡Respuesta Correcta!</h3>'
                f'<p style="color:#6ee7b7;margin-bottom:10px">'
                f'Los efectos de <b>{nom_dec}</b> se aplicaron</p>'
                f'<div>{cambios_html}</div></div>', unsafe_allow_html=True)
        else:
            st.session_state["incorrectas"] = st.session_state.get("incorrectas", 0) + 1
            texto_ok = pregunta["ops"][pregunta["ok"]]
            causa    = "Tiempo agotado — " if agotado else ""
            aviso_par = f" (Ronda par: penalización ×1.5)" if es_par else ""
            nueva_ind = aplicar_efectos(ind, {k: -penalizacion for k in
                                              ["economia","medio_ambiente","energia","bienestar_social"]})
            actualizar_progreso(gid, nueva_ind["economia"], nueva_ind["medio_ambiente"],
                                nueva_ind["energia"], nueva_ind["bienestar_social"], ronda)
            st.markdown(
                f'<div style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.35);'
                f'border-radius:16px;padding:22px 26px;text-align:center;margin-bottom:14px">'
                f'<div style="font-size:2.5rem">❌</div>'
                f'<h3 style="color:#f87171;margin:8px 0 4px">{causa}Respuesta Incorrecta</h3>'
                f'<p style="color:#fca5a5">La correcta era: <b>{texto_ok}</b></p>'
                f'<p style="color:#fca5a5">Todos los indicadores pierden '
                f'<b>{penalizacion} puntos</b>{aviso_par}.</p>'
                f'</div>', unsafe_allow_html=True)

        st.session_state["fase_ronda"] = "evento"
        if st.button("Continuar → Evento Aleatorio ⚡", use_container_width=True):
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 4 — EVENTO ALEATORIO
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "evento":
        if st.session_state.get("evento_ronda") is None:
            st.session_state["evento_ronda"] = random.choice(EVENTOS)

        evento    = st.session_state["evento_ronda"]
        nom_ind   = evento["indicador"].replace("_", " ").title()
        col_ind, em_ind = IND_COLOR.get(evento["indicador"], ("#94a3b8", "❓"))
        positivo  = evento["valor"] > 0
        col_ev    = "#10b981" if positivo else "#ef4444"
        bg_ev     = "rgba(16,185,129,0.1)" if positivo else "rgba(239,68,68,0.1)"
        icono_ev  = "🎉" if positivo else "⚠️"
        signo     = "+" if positivo else ""

        progreso_ev = obtener_progreso(gid)
        ind_ev = {
            "economia":        progreso_ev["economia"],
            "medio_ambiente":  progreso_ev["medio_ambiente"],
            "energia":         progreso_ev["energia"],
            "bienestar_social":progreso_ev["bienestar_social"],
        }
        nueva_ind   = aplicar_efectos(ind_ev, {evento["indicador"]: evento["valor"]})
        valor_antes  = ind_ev[evento["indicador"]]
        valor_despues = nueva_ind[evento["indicador"]]

        st.markdown(
            f'<div style="background:{bg_ev};border:1px solid {col_ev}44;'
            f'border-radius:16px;padding:26px;text-align:center">'
            f'<div style="font-size:2.2rem">{icono_ev}</div>'
            f'<div style="font-size:0.78rem;color:rgba(255,255,255,0.45);'
            f'text-transform:uppercase;letter-spacing:2px;margin:6px 0 2px">'
            f'Evento Aleatorio — Ronda {ronda}</div>'
            f'<h2 style="color:#f1f5f9;margin:0 0 10px;font-size:1.4rem">'
            f'{evento["nombre"]}</h2>'
            f'<div style="display:inline-block;background:rgba(255,255,255,0.07);'
            f'border-radius:12px;padding:8px 20px">'
            f'<span style="color:{col_ind};font-size:1rem">{em_ind} '
            f'{IND_LABEL.get(evento["indicador"], nom_ind)}</span>'
            f'<span style="color:rgba(255,255,255,0.35);margin:0 8px">|</span>'
            f'<span style="color:rgba(255,255,255,0.5)">{valor_antes}</span>'
            f'<span style="color:rgba(255,255,255,0.35);margin:0 6px">→</span>'
            f'<span style="color:{col_ev};font-weight:700">{valor_despues}</span>'
            f'<span style="color:{col_ev};font-size:0.9rem;margin-left:8px">'
            f'{signo}{evento["valor"]}</span>'
            f'</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(f"Finalizar Ronda {ronda}/{TOTAL_RONDAS} →", use_container_width=True):
            actualizar_progreso(gid,
                                nueva_ind["economia"], nueva_ind["medio_ambiente"],
                                nueva_ind["energia"],  nueva_ind["bienestar_social"],
                                ronda + 1)
            st.session_state.update({
                "pregunta_actual":  None, "respuesta_correcta": False,
                "decision_elegida": None, "decision_efectos":   None,
                "evento_ronda":     None, "fase_ronda":         "decision",
                "timer_inicio":     None, "tiempo_agotado":     False,
            })
            st.rerun()
