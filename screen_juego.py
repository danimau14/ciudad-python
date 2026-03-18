import streamlit as st
import random
import time

from session_manager import navegar
from database import (obtener_progreso, obtener_estudiantes, obtener_cooldowns,
                      actualizar_progreso, actualizar_cooldown, reiniciar_progreso,
                      marcar_partida_terminada, obtener_estrellas, gastar_estrellas)
from config import (TOTAL_RONDAS, TIEMPO_PREGUNTA, COOLDOWN,
                    IND_COLOR, IND_LABEL, CAT_COLOR, ATRIBUTOS,
                    DECISIONES, EVENTOS, PREGUNTAS, DIFICULTADES,
                    UMBRAL_ROJO, MEZCLA_PREGUNTAS)


# ── Selección de pregunta con mezcla por dificultad ───────────────────────────
def seleccionar_pregunta(dificultad="Normal"):
    mezcla = MEZCLA_PREGUNTAS.get(dificultad, {"facil":.33,"normal":.34,"dificil":.33})
    usadas = st.session_state.get("preguntas_usadas", [])
    pesos  = [mezcla.get(p["dif"], 0.33) for p in PREGUNTAS]
    disponibles = [(i, pesos[i]) for i in range(len(PREGUNTAS)) if i not in usadas]
    if not disponibles:
        st.session_state["preguntas_usadas"] = []
        disponibles = [(i, pesos[i]) for i in range(len(PREGUNTAS))]
    idxs   = [d[0] for d in disponibles]
    pesos2 = [d[1] for d in disponibles]
    total  = sum(pesos2) or 1
    pesos2 = [w / total for w in pesos2]
    idx    = random.choices(idxs, weights=pesos2, k=1)[0]
    st.session_state.setdefault("preguntas_usadas", []).append(idx)
    return PREGUNTAS[idx]


def aplicar_efectos(ind, ef):
    r = dict(ind)
    for k, v in ef.items():
        if k in r:
            r[k] = max(0, min(100, r[k] + v))
    return r


def hay_colapso_inmediato(ind):
    return any(v <= UMBRAL_ROJO for v in ind.values())


# ── Barra de indicador ────────────────────────────────────────────────────────
def barra_indicador(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    if valor >= 60:   color, badge = "#10b981", "Estable"
    elif valor >= UMBRAL_ROJO: color, badge = "#f59e0b", "Precaución"
    else:             color, badge = "#ef4444", "Crítico"
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
    top1, top2 = st.columns([3, 1])
    with top1:
        st.markdown(
            f'<div style="font-size:clamp(1.3rem,4vw,1.8rem);font-weight:800;'
            f'background:linear-gradient(90deg,#a78bfa,#60a5fa);'
            f'-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            f'background-clip:text;margin-bottom:6px;font-family:Outfit,sans-serif">'
            f'{nombre_grp}</div>', unsafe_allow_html=True)
        chips = " ".join(
            f'<span style="background:{"rgba(167,139,250,.28)" if e==est_turno else "rgba(255,255,255,.05)"};'
            f'border:1px solid {"rgba(167,139,250,.5)" if e==est_turno else "rgba(255,255,255,.07)"};'
            f'border-radius:20px;padding:3px 12px;margin:2px;font-size:.82rem;'
            f'color:{"#c4b5fd" if e==est_turno else "#94a3b8"};display:inline-block;'
            f'font-family:Outfit,sans-serif">'
            f'{"🎤 " if e==est_turno else ""}{e}</span>'
            for e in estudiantes)
        st.markdown(f'<div style="margin-top:6px">{chips}</div>', unsafe_allow_html=True)
    with top2:
        with st.expander("☰"):
            if st.button("📖 Instrucciones",    use_container_width=True): navegar("instrucciones")
            if st.button("🏠 Volver al inicio", use_container_width=True): navegar("inicio")
            if st.button("⬅️ Volver al Lobby",  use_container_width=True): navegar("lobby")

    m1, m2, m3, m4 = st.columns(4)
    pct        = int((ronda - 1) / TOTAL_RONDAS * 100)
    fase_label = st.session_state.get("fase_ronda", "decision")
    fases_txt  = {"decision":"Elegir Decisión","pregunta":"Responder Pregunta",
                  "evento":"Evento Aleatorio","resultado_pregunta":"Resultado"}
    with m1: st.metric("Ronda",    f"{ronda}/{TOTAL_RONDAS}")
    with m2: st.metric("Turno",    est_turno)
    with m3: st.metric("Progreso", f"{pct}%")
    with m4: st.metric("Fase",     fases_txt.get(fase_label, fase_label))
    st.markdown(
        f'<div style="background:rgba(255,255,255,.06);border-radius:6px;height:5px;margin:2px 0 14px">'
        f'<div style="width:{pct}%;background:linear-gradient(90deg,#7c3aed,#a78bfa);'
        f'height:5px;border-radius:6px"></div></div>', unsafe_allow_html=True)


# ── Panel de atributos comprables ─────────────────────────────────────────────
def panel_atributos(gid, estrellas):
    """Muestra los atributos que se pueden activar con estrellas esta ronda."""
    activos = st.session_state.get("atributos_activos", {})
    with st.expander(f"⭐ Activar Atributo  ({estrellas} ⭐ disponibles)"):
        cols = st.columns(4)
        for ci, (aid, atr) in enumerate(ATRIBUTOS.items()):
            with cols[ci % 4]:
                ya_activo = aid in activos
                puede     = estrellas >= atr["costo"] and not ya_activo
                color     = "#a78bfa" if ya_activo else ("#fbbf24" if puede else "rgba(255,255,255,.2)")
                label_btn = f"✅ Activo" if ya_activo else f"Activar {atr['costo']} ⭐"
                st.markdown(f'''<div style="background:rgba(255,255,255,.03);
                    border:1px solid {color}55;border-radius:12px;
                    padding:10px 8px;text-align:center;margin-bottom:6px">
                    <div style="font-size:1.2rem">{atr["emoji"]}</div>
                    <div style="font-size:.72rem;font-weight:700;color:{color};margin:3px 0">
                        {atr["nombre"]}</div>
                    <div style="font-size:.65rem;color:rgba(255,255,255,.3);margin-bottom:4px">
                        {atr["desc"]}</div>
                </div>''', unsafe_allow_html=True)
                if st.button(label_btn, key=f"atr_{aid}_{st.session_state.get('_ronda_atr',0)}",
                             disabled=not puede, use_container_width=True):
                    if gastar_estrellas(gid, atr["costo"]):
                        st.session_state.setdefault("atributos_activos", {})[aid] = True
                        st.rerun()


# ── Pantalla principal ────────────────────────────────────────────────────────
def pantalla_juego():
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio"); return

    dificultad        = st.session_state.get("dificultad_sel", "Normal")
    progreso          = obtener_progreso(gid, dificultad)
    estudiantes       = obtener_estudiantes(gid)
    cooldowns         = obtener_cooldowns(gid, dificultad)
    ronda             = progreso["ronda_actual"]
    nombre_grp        = st.session_state["grupo_nombre"]
    cfg_dif           = DIFICULTADES.get(dificultad, DIFICULTADES["Normal"])
    penalizacion_base = cfg_dif["penalizacion"]
    estrellas         = obtener_estrellas(gid)

    idx_turno = (ronda - 1) % len(estudiantes)
    est_turno = estudiantes[idx_turno]

    ind = {
        "economia":         progreso["economia"],
        "medio_ambiente":   progreso["medio_ambiente"],
        "energia":          progreso["energia"],
        "bienestar_social": progreso["bienestar_social"],
    }

    # ── Colapso inmediato por indicador en rojo ───────────────────────────────
    if hay_colapso_inmediato(ind):
        marcar_partida_terminada(gid, dificultad)
        st.session_state.update({
            "resultado":          "derrota",
            "indicadores_finales": ind,
            "rondas_completadas":  ronda - 1,
        })
        navegar("fin"); return

    # ── Fin de 10 rondas ──────────────────────────────────────────────────────
    if ronda > TOTAL_RONDAS:
        marcar_partida_terminada(gid, dificultad)
        prom = sum(ind.values()) / len(ind)
        resultado = "derrota" if prom <= 60 else "victoria"
        st.session_state.update({
            "resultado":          resultado,
            "indicadores_finales": ind,
            "rondas_completadas":  TOTAL_RONDAS,
        })
        navegar("fin"); return

    cabecera_juego(nombre_grp, estudiantes, ronda, est_turno)

    ci1, ci2, ci3, ci4 = st.columns(4)
    with ci1: barra_indicador("Economía",       ind["economia"],         "💰")
    with ci2: barra_indicador("Medio Ambiente", ind["medio_ambiente"],   "🌿")
    with ci3: barra_indicador("Energía",        ind["energia"],          "⚡")
    with ci4: barra_indicador("Bienestar",      ind["bienestar_social"], "❤️")
    st.markdown("---")

    fase = st.session_state.get("fase_ronda", "decision")

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 1 — DECISIÓN
    # ══════════════════════════════════════════════════════════════════════════
    if fase == "decision":
        # Panel de atributos antes de decidir
        panel_atributos(gid, obtener_estrellas(gid))
        st.markdown("---")

        st.markdown(
            '<div style="font-size:1rem;font-weight:700;color:#f1f5f9;'
            'font-family:Outfit,sans-serif;margin-bottom:4px">'
            'Paso 1 — Elige una Decisión Estratégica</div>'
            '<p style="color:rgba(255,255,255,.4);font-size:.84rem;margin-top:0;margin-bottom:16px">'
            'Si aciertas la pregunta, los efectos se aplicarán a la ciudad.</p>',
            unsafe_allow_html=True)

        cols = st.columns(4)
        for i, (nom_dec, ef) in enumerate(DECISIONES.items()):
            col           = cols[i % 4]
            disponible_en = cooldowns.get(nom_dec, 0)
            disp          = disponible_en == 0 or ronda >= disponible_en
            rondas_falta  = max(0, disponible_en - ronda) if disponible_en > 0 else 0

            filas_ef = ""
            for k, v in ef.items():
                if k == "emoji": continue
                col_ind, em_ind = IND_COLOR.get(k, ("#94a3b8", ""))
                signo   = "+" if v > 0 else ""
                col_val = "#4ade80" if v > 0 else "#f87171"
                filas_ef += (
                    f'<div style="display:flex;justify-content:space-between;'
                    f'align-items:center;padding:4px 0;'
                    f'border-bottom:1px solid rgba(255,255,255,.05)">'
                    f'<span style="color:{col_ind};font-size:.76rem">{em_ind} {IND_LABEL[k]}</span>'
                    f'<span style="color:{col_val};font-size:.84rem;font-weight:700">'
                    f'{signo}{v}</span></div>'
                )

            if disp:
                borde, bg_card, opac, overlay, btn_txt = (
                    "rgba(167,139,250,.45)", "rgba(167,139,250,.07)", 1, "", "Elegir")
            else:
                borde, bg_card, opac = "rgba(245,158,11,.35)", "rgba(245,158,11,.04)", 0.55
                puntos_html = " ".join(
                    f'<span style="display:inline-block;width:10px;height:10px;'
                    f'border-radius:50%;background:{"#fbbf24" if j<rondas_falta else "rgba(255,255,255,.15)"};'
                    f'margin:2px"></span>' for j in range(COOLDOWN))
                overlay = (
                    f'<div style="position:absolute;inset:0;border-radius:16px;'
                    f'background:rgba(0,0,0,.45);display:flex;flex-direction:column;'
                    f'align-items:center;justify-content:center;gap:6px">'
                    f'<span style="font-size:1.6rem">⏳</span>'
                    f'<span style="color:#fbbf24;font-weight:800;font-size:.9rem">'
                    f'{rondas_falta} ronda{"s" if rondas_falta!=1 else ""}</span>'
                    f'<div>{puntos_html}</div>'
                    f'<span style="color:rgba(255,255,255,.4);font-size:.68rem">'
                    f'Disponible en ronda {disponible_en}</span></div>'
                )
                btn_txt = "Bloqueada"

            with col:
                st.markdown(
                    f'<div style="position:relative;background:{bg_card};'
                    f'border:1px solid {borde};border-radius:16px;padding:14px 16px;'
                    f'margin-bottom:4px;opacity:{opac};min-height:185px;transition:all .2s">'
                    f'{overlay}'
                    f'<div style="font-size:1.6rem;margin-bottom:4px">{ef["emoji"]}</div>'
                    f'<div style="font-weight:700;color:#f1f5f9;font-size:.88rem;'
                    f'margin-bottom:8px;line-height:1.2;font-family:Outfit,sans-serif">{nom_dec}</div>'
                    f'{filas_ef}</div>', unsafe_allow_html=True)
                if st.button(btn_txt, disabled=not disp,
                             key=f"dec_{nom_dec}", use_container_width=True):
                    # Rastrear decisiones usadas para logros
                    st.session_state.setdefault("decisiones_usadas_set", set()).add(nom_dec)
                    st.session_state["decision_elegida"] = nom_dec
                    st.session_state["decision_efectos"] = {k:v for k,v in ef.items() if k!="emoji"}
                    st.session_state["pregunta_actual"]  = seleccionar_pregunta(dificultad)
                    st.session_state["timer_inicio"]     = None
                    st.session_state["tiempo_agotado"]   = False
                    st.session_state["fase_ronda"]       = "pregunta"
                    st.session_state["_ronda_atr"]       = ronda
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 2 — PREGUNTA
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "pregunta":
        pregunta  = st.session_state["pregunta_actual"]
        nom_dec   = st.session_state["decision_elegida"]
        ef_dec    = st.session_state["decision_efectos"]
        atributos = st.session_state.get("atributos_activos", {})

        # Tiempo extra si se activó ese atributo
        tiempo_total = TIEMPO_PREGUNTA + (15 if "tiempo_extra" in atributos else 0)

        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        timer_ini          = st.session_state["timer_inicio"]
        tiempo_transcurrido = time.time() - timer_ini
        tiempo_restante    = max(0.0, tiempo_total - tiempo_transcurrido)
        pct_timer          = tiempo_restante / tiempo_total
        seg                = int(tiempo_restante)
        col_timer          = ("#10b981" if pct_timer > 0.5
                              else "#f59e0b" if pct_timer > 0.25 else "#ef4444")

        # Logro velocidad: respondió en < 5 s
        if tiempo_transcurrido < 5:
            st.session_state["_logro_velocidad"] = True
        # Logro casi tiempo: respondió con < 3 s restantes
        if seg <= 2 and seg > 0:
            st.session_state["_logro_casi_tiempo"] = True

        # Resumen decisión elegida
        ef_resumen = " ".join(
            f'<span style="color:{IND_COLOR[k][0]}">{IND_COLOR[k][1]} '
            f'{"+" if v>0 else ""}{v}</span>'
            for k, v in ef_dec.items() if k in IND_COLOR)
        dec_emoji = DECISIONES.get(nom_dec, {}).get("emoji", "")
        st.markdown(
            f'<div style="background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);'
            f'border-radius:14px;padding:10px 18px;margin-bottom:14px;'
            f'display:flex;flex-wrap:wrap;gap:6px;align-items:center">'
            f'<span style="color:#a78bfa;font-size:.82rem">Decisión:</span>'
            f'<span style="color:#f1f5f9;font-weight:700;font-family:Outfit,sans-serif">'
            f'{dec_emoji} {nom_dec}</span>'
            f'<span style="color:rgba(255,255,255,.3);font-size:.78rem">{ef_resumen}</span>'
            f'</div>', unsafe_allow_html=True)

        # Temporizador
        urgencia = ('<div style="color:#ef4444;font-size:.75rem;font-weight:700;'
                    'margin-top:6px;text-align:center">¡Responde ya!</div>') if seg <= 8 else ""
        st.markdown(
            f'<div style="background:rgba(0,0,0,.22);border:1px solid {col_timer}44;'
            f'border-radius:16px;padding:14px 20px;margin-bottom:16px">'
            f'<div style="display:flex;justify-content:space-between;'
            f'align-items:center;margin-bottom:8px">'
            f'<span style="color:rgba(255,255,255,.45);font-size:.82rem">Tiempo restante</span>'
            f'<span style="color:{col_timer};font-weight:900;'
            f'font-size:clamp(1.3rem,4vw,1.8rem);font-variant-numeric:tabular-nums">{seg}s</span></div>'
            f'<div style="background:rgba(255,255,255,.08);border-radius:6px;height:12px;overflow:hidden">'
            f'<div style="width:{int(pct_timer*100)}%;height:12px;border-radius:6px;'
            f'background:linear-gradient(90deg,{col_timer}aa,{col_timer});'
            f'transition:width .95s linear,background .95s"></div></div>'
            f'{urgencia}</div>', unsafe_allow_html=True)

        # Badge dificultad de la pregunta
        dif_preg = pregunta.get("dif","normal")
        dif_col  = {"facil":"#10b981","normal":"#f59e0b","dificil":"#ef4444"}.get(dif_preg,"#94a3b8")
        dif_lbl  = {"facil":"🟢 Fácil","normal":"🟡 Normal","dificil":"🔴 Difícil"}.get(dif_preg,"")
        cat_color = CAT_COLOR.get(pregunta["cat"], "#94a3b8")
        st.markdown(
            f'<div class="card-glow">'
            f'<div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap">'
            f'<span style="background:{cat_color}22;color:{cat_color};'
            f'border:1px solid {cat_color}55;border-radius:20px;padding:2px 12px;font-size:.72rem;font-weight:600">'
            f'{pregunta["cat"]}</span>'
            f'<span style="background:{dif_col}22;color:{dif_col};'
            f'border:1px solid {dif_col}55;border-radius:20px;padding:2px 10px;font-size:.72rem;font-weight:600">'
            f'{dif_lbl}</span></div>'
            f'<h3 style="color:#f1f5f9;margin:0;font-size:clamp(.95rem,2.5vw,1.1rem);'
            f'font-family:Outfit,sans-serif">{pregunta["q"]}</h3>'
            f'</div>', unsafe_allow_html=True)

        opciones_letras = [f"{chr(65+i)}. {op}" for i, op in enumerate(pregunta["ops"])]

        if tiempo_restante <= 0:
            st.session_state["tiempo_agotado"]    = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["fase_ronda"]        = "resultado_pregunta"
            st.rerun()

        respuesta = st.radio("Selecciona tu respuesta:", opciones_letras, key="radio_resp")
        if st.button("Confirmar Respuesta ✅", use_container_width=True):
            idx_resp = opciones_letras.index(respuesta)
            correcta = idx_resp == pregunta["ok"]

            # Segunda oportunidad: si falla, guarda que puede reintentar
            if not correcta and "segunda_oportunidad" in atributos and not st.session_state.get("_segunda_usada"):
                st.session_state["_segunda_usada"] = True
                st.warning("❌ Fallaste, pero tienes **Segunda Oportunidad**. Inténtalo de nuevo.")
                st.rerun()

            st.session_state["respuesta_correcta"] = correcta
            st.session_state["tiempo_agotado"]     = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.session_state["_segunda_usada"]     = False
            st.rerun()

        time.sleep(1)
        st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 3 — RESULTADO PREGUNTA
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        pregunta     = st.session_state["pregunta_actual"]
        correcta     = st.session_state["respuesta_correcta"]
        agotado      = st.session_state.get("tiempo_agotado", False)
        nom_dec      = st.session_state["decision_elegida"]
        ef_dec       = st.session_state["decision_efectos"]
        atributos    = st.session_state.get("atributos_activos", {})
        es_par        = ronda % 2 == 0
        penalizacion  = penalizacion_base * (2 if es_par else 1)

        if correcta:
            st.session_state["correctas"] = st.session_state.get("correctas", 0) + 1

            # Racha
            racha = st.session_state.get("racha_actual", 0) + 1
            st.session_state["racha_actual"] = racha
            st.session_state["racha_max"]    = max(st.session_state.get("racha_max", 0), racha)

            # Conteo de preguntas difíciles acertadas
            if pregunta.get("dif") == "dificil":
                st.session_state["_correctas_dificil"] = st.session_state.get("_correctas_dificil", 0) + 1

            # Doble efecto si está activo
            ef_aplicar = {k: v*2 if "doble_efecto" in atributos else v
                          for k, v in ef_dec.items()}

            nueva_ind = aplicar_efectos(ind, ef_aplicar)
            actualizar_progreso(gid, nueva_ind["economia"], nueva_ind["medio_ambiente"],
                                nueva_ind["energia"], nueva_ind["bienestar_social"], ronda, dificultad)
            actualizar_cooldown(gid, nom_dec, ronda, dificultad)

            # Registro de correctas por estudiante
            cpe = st.session_state.setdefault("correctas_por_est", {})
            cpe[est_turno] = cpe.get(est_turno, 0) + 1

            cambios_html = ""
            for k, v in ef_aplicar.items():
                if k not in IND_COLOR: continue
                col_ind, em_ind = IND_COLOR[k]
                signo   = "+" if v > 0 else ""
                col_v   = "#4ade80" if v > 0 else "#f87171"
                cambios_html += (
                    f'<span style="background:rgba(255,255,255,.07);border-radius:8px;'
                    f'padding:4px 10px;margin:3px;display:inline-block;font-family:Outfit,sans-serif">'
                    f'<span style="color:#f1f5f9">{em_ind} {IND_LABEL[k]}</span> '
                    f'<b style="color:{col_v}">{signo}{v}</b></span>'
                )
            doble_badge = '<div style="color:#fbbf24;font-size:.78rem;margin-top:6px">✨ Doble efecto activo</div>' if "doble_efecto" in atributos else ""
            st.markdown(
                f'<div style="background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.35);'
                f'border-radius:18px;padding:22px 26px;text-align:center;margin-bottom:14px">'
                f'<div style="font-size:2.5rem">✅</div>'
                f'<h3 style="color:#34d399;margin:8px 0 4px;font-family:Outfit,sans-serif">¡Respuesta Correcta!</h3>'
                f'<p style="color:#6ee7b7;margin-bottom:10px">Los efectos de <b>{nom_dec}</b> se aplicaron</p>'
                f'<div>{cambios_html}</div>{doble_badge}</div>', unsafe_allow_html=True)

        else:
            st.session_state["incorrectas"]  = st.session_state.get("incorrectas", 0) + 1
            st.session_state["racha_actual"] = 0  # romper racha
            texto_ok  = pregunta["ops"][pregunta["ok"]]
            causa     = "⏱️ Tiempo agotado — " if agotado else ""
            aviso_par = f" (Ronda par: penalización ×2)" if es_par else ""

            nueva_ind = aplicar_efectos(ind,
                {k: -penalizacion for k in ["economia","medio_ambiente","energia","bienestar_social"]})
            actualizar_progreso(gid, nueva_ind["economia"], nueva_ind["medio_ambiente"],
                                nueva_ind["energia"], nueva_ind["bienestar_social"], ronda, dificultad)

            # Detectar recuperación: indicador subió desde rojo
            for k, v in nueva_ind.items():
                if ind[k] <= UMBRAL_ROJO and v > 60:
                    st.session_state["_logro_recuperacion"] = True

            st.markdown(
                f'<div style="background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.35);'
                f'border-radius:18px;padding:22px 26px;text-align:center;margin-bottom:14px">'
                f'<div style="font-size:2.5rem">❌</div>'
                f'<h3 style="color:#f87171;margin:8px 0 4px;font-family:Outfit,sans-serif">'
                f'{causa}Respuesta Incorrecta</h3>'
                f'<p style="color:#fca5a5">La correcta era: <b>{texto_ok}</b></p>'
                f'<p style="color:#fca5a5">Todos los indicadores pierden '
                f'<b>{penalizacion} puntos</b>{aviso_par}</p>'
                f'</div>', unsafe_allow_html=True)

        # Limpiar atributos de tipo "pregunta" después de usarlos
        activos = st.session_state.get("atributos_activos", {})
        for aid in ["segunda_oportunidad","tiempo_extra"]:
            activos.pop(aid, None)
        st.session_state["atributos_activos"] = activos

        st.session_state["fase_ronda"] = "evento"
        if st.button("Continuar → Evento Aleatorio ⚡", use_container_width=True):
            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FASE 4 — EVENTO ALEATORIO
    # ══════════════════════════════════════════════════════════════════════════
    elif fase == "evento":
        if st.session_state.get("evento_ronda") is None:
            # Ponderar negativos/positivos según dificultad
            cfg_dif = DIFICULTADES.get(dificultad, DIFICULTADES["Normal"])
            from config import EVENTOS_NEGATIVOS, EVENTOS_POSITIVOS
            peso_neg = cfg_dif["eventos_peso"]["negativos"]
            peso_pos = cfg_dif["eventos_peso"]["positivos"]
            pool  = (EVENTOS_NEGATIVOS * int(peso_neg * 10) +
                     EVENTOS_POSITIVOS  * int(peso_pos * 10))
            st.session_state["evento_ronda"] = random.choice(pool)

        evento   = st.session_state["evento_ronda"]
        col_ind, em_ind = IND_COLOR.get(evento["indicador"], ("#94a3b8", "❓"))
        positivo = evento["valor"] > 0
        col_ev   = "#10b981" if positivo else "#ef4444"
        bg_ev    = "rgba(16,185,129,.1)" if positivo else "rgba(239,68,68,.1)"
        icono_ev = "🎉" if positivo else "⚠️"
        signo    = "+" if positivo else ""

        progreso_ev = obtener_progreso(gid, dificultad)
        ind_ev = {
            "economia":         progreso_ev["economia"],
            "medio_ambiente":   progreso_ev["medio_ambiente"],
            "energia":          progreso_ev["energia"],
            "bienestar_social": progreso_ev["bienestar_social"],
        }

        # Atributo escudo: reduce evento negativo al 50%
        atributos = st.session_state.get("atributos_activos", {})
        val_evento = evento["valor"]
        if not positivo and "escudo_ciudad" in atributos:
            val_evento = int(val_evento * 0.5)

        # Atributos de protección individual
        prot_map = {
            "prot_economia":   "economia",
            "prot_ambiente":   "medio_ambiente",
            "prot_energia":    "energia",
            "prot_bienestar":  "bienestar_social",
        }
        for aid, ind_key in prot_map.items():
            if aid in atributos and evento["indicador"] == ind_key and not positivo:
                val_evento = 0  # ignora el efecto negativo

        nueva_ind    = aplicar_efectos(ind_ev, {evento["indicador"]: val_evento})
        valor_antes  = ind_ev[evento["indicador"]]
        valor_despues = nueva_ind[evento["indicador"]]

        escudo_badge = ""
        if "escudo_ciudad" in atributos and not positivo:
            escudo_badge = '<div style="color:#a78bfa;font-size:.78rem;margin-top:8px">🛡️ Escudo activo — impacto reducido al 50%</div>'

        st.markdown(
            f'<div style="background:{bg_ev};border:1px solid {col_ev}44;'
            f'border-radius:18px;padding:26px;text-align:center">'
            f'<div style="font-size:2.2rem">{icono_ev}</div>'
            f'<div style="font-size:.78rem;color:rgba(255,255,255,.4);'
            f'text-transform:uppercase;letter-spacing:2px;margin:6px 0 2px">'
            f'Evento Aleatorio — Ronda {ronda}</div>'
            f'<h2 style="color:#f1f5f9;margin:0 0 10px;font-size:1.4rem;font-family:Outfit,sans-serif">'
            f'{evento["nombre"]}</h2>'
            f'<div style="display:inline-block;background:rgba(255,255,255,.07);'
            f'border-radius:14px;padding:10px 22px">'
            f'<span style="color:{col_ind};font-size:1rem">{em_ind} {IND_LABEL.get(evento["indicador"],evento["indicador"])}</span>'
            f'<span style="color:rgba(255,255,255,.3);margin:0 8px">|</span>'
            f'<span style="color:rgba(255,255,255,.5)">{valor_antes}</span>'
            f'<span style="color:rgba(255,255,255,.3);margin:0 6px">→</span>'
            f'<span style="color:{col_ev};font-weight:700">{valor_despues}</span>'
            f'<span style="color:{col_ev};font-size:.9rem;margin-left:8px">{signo}{val_evento}</span>'
            f'</div>{escudo_badge}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(f"Finalizar Ronda {ronda}/{TOTAL_RONDAS} →", use_container_width=True):
            # Detectar si algún indicador estuvo por debajo del mínimo global durante la ronda
            if any(v < 40 for v in nueva_ind.values()):
                st.session_state["_min_global_ok"] = False

            actualizar_progreso(gid,
                                nueva_ind["economia"], nueva_ind["medio_ambiente"],
                                nueva_ind["energia"],  nueva_ind["bienestar_social"],
                                ronda + 1, dificultad)

            # Limpiar atributos de tipo "ronda" al terminar la ronda
            activos = st.session_state.get("atributos_activos", {})
            for aid in ["escudo_ciudad","prot_economia","prot_ambiente",
                        "prot_energia","prot_bienestar","doble_efecto"]:
                activos.pop(aid, None)
            st.session_state["atributos_activos"] = activos

            st.session_state.update({
                "pregunta_actual":  None, "respuesta_correcta": False,
                "decision_elegida": None, "decision_efectos":   None,
                "evento_ronda":     None, "fase_ronda":         "decision",
                "timer_inicio":     None, "tiempo_agotado":     False,
                "_segunda_usada":   False,
            })
            st.rerun()
