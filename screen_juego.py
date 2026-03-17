import streamlit as st
import time
import random
from navigation import navegar
from config import TOTAL_RONDAS, TIEMPO_PREGUNTA, COOLDOWN, IND_COLOR, IND_LABEL, CAT_COLOR, DIFICULTADES, ATRIBUTOS
from database import (
    obtener_progreso, obtener_estudiantes, obtener_cooldowns,
    actualizar_progreso, actualizar_cooldown, decrementar_cooldowns,
    obtener_estrellas, actualizar_estrellas
)
from decisions import DECISIONES
from questions import seleccionar_pregunta
from events import EVENTOS, EVENTOS_EPICOS, generar_evento
from game_engine import aplicar_efectos
from ui_components import barra_indicador, cabecera_juego


def pantalla_juego():
    gid = st.session_state.get("grupo_id")
    if not gid: navegar("inicio"); return

    progreso    = obtener_progreso(gid)
    estudiantes = obtener_estudiantes(gid)
    cooldowns   = obtener_cooldowns(gid)
    ronda       = progreso["ronda_actual"]
    nombre_grp  = st.session_state["grupo_nombre"]

    # Guardia: si no hay estudiantes redirigir al inicio
    if not estudiantes:
        st.error("⚠️ No se encontraron estudiantes para este grupo. Regresa e inicia sesión nuevamente.")
        if st.button("🏠 Volver al inicio"):
            navegar("inicio")
        return

    idx_turno   = (ronda - 1) % len(estudiantes)
    est_turno   = estudiantes[idx_turno]

    ind = {"economia":progreso["economia"],"medio_ambiente":progreso["medio_ambiente"],
           "energia":progreso["energia"],"bienestar_social":progreso["bienestar_social"]}

    # Fin de juego: solo por rondas completadas
    if ronda > TOTAL_RONDAS:
        st.session_state.update({"resultado":"victoria","indicadores_finales":ind,"rondas_completadas":TOTAL_RONDAS})
        navegar("fin"); return

    cabecera_juego(nombre_grp, estudiantes, ronda, est_turno)

    # Indicadores responsivos: 4 cols en desktop, 2 en tablet, 1 en móvil
    st.markdown("""
<style>
.ind-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-bottom:10px; }
@media(max-width:900px){ .ind-grid { grid-template-columns:repeat(2,1fr); } }
@media(max-width:640px){ .ind-grid { grid-template-columns:1fr; } }
</style>""", unsafe_allow_html=True)
    ci1,ci2,ci3,ci4 = st.columns(4)
    with ci1: barra_indicador("Economía",        ind["economia"],        "💰")
    with ci2: barra_indicador("Medio Ambiente",  ind["medio_ambiente"],  "🌿")
    with ci3: barra_indicador("Energía",         ind["energia"],         "⚡")
    with ci4: barra_indicador("Bienestar Social",ind["bienestar_social"], "🏥")
    st.markdown("<hr style='border-color:rgba(0,212,255,0.08);margin:4px 0 10px;'>",
                unsafe_allow_html=True)

    fase = st.session_state.get("fase_ronda","decision")

    # ══════════════════════════════════════════════
    # FASE 1: ELEGIR DECISION
    # ══════════════════════════════════════════════
    if fase == "decision":
        # ── Panel de Estrellas ──────────────────────────────────
        estrellas = obtener_estrellas(gid)
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:10px;background:rgba(251,191,36,0.06);"
            f"border:1px solid rgba(251,191,36,0.2);border-radius:10px;padding:8px 16px;"
            f"margin-bottom:10px;'>"
            f"<span style='font-size:1.2rem;'>⭐</span>"
            f"<span style='font-family:Orbitron,sans-serif;font-size:0.7rem;color:#fbbf24;"
            f"font-weight:700;letter-spacing:1px;'>ESTRELLAS: {estrellas}</span>"
            f"</div>", unsafe_allow_html=True)

        with st.expander("🌟 Usar atributo de estrellas"):
            a_cols = st.columns(4)
            atrib_activo = st.session_state.get("atributo_activo")
            for ai, (akey, aval) in enumerate(ATRIBUTOS.items()):
                puede   = estrellas >= aval["costo"]
                activo  = atrib_activo == akey
                bcolor  = "#22c55e" if activo else ("#f59e0b" if puede else "rgba(255,255,255,.08)")
                op      = "1" if puede else "0.35"
                badge   = f"<div style=\'font-size:.5rem;color:#22c55e;font-weight:700;\'>✅ ACTIVO</div>" if activo else ""
                with a_cols[ai % 4]:
                    st.markdown(
                        f"<div style=\'border:1px solid {bcolor};border-radius:10px;padding:8px;"
                        f"text-align:center;opacity:{op};background:rgba(0,0,0,0.3);margin-bottom:4px;\'>"
                        f"<div style=\'font-size:1.3rem;\'>{aval['icon']}</div>"
                        f"<div style=\'font-family:Orbitron,sans-serif;font-size:.55rem;"
                        f"color:#fbbf24;font-weight:700;margin:3px 0;\'>{aval['nombre']}</div>"
                        f"<div style=\'font-size:.5rem;color:rgba(255,255,255,.35);line-height:1.3;\'>"
                        f"{aval['desc']}</div>"
                        f"<div style=\'font-size:.6rem;color:#facc15;margin-top:4px;\'>⭐ {aval['costo']}</div>"
                        f"{badge}</div>", unsafe_allow_html=True)
                    if puede and not activo:
                        if st.button("Activar", key=f"attr_{akey}_{ronda}", use_container_width=True):
                            actualizar_estrellas(gid, -aval["costo"])
                            st.session_state["atributo_activo"] = akey
                            st.rerun()
                    elif activo:
                        if st.button("Cancelar", key=f"attr_cancel_{akey}_{ronda}", use_container_width=True):
                            actualizar_estrellas(gid, aval["costo"])  # devolver estrellas
                            st.session_state["atributo_activo"] = None
                            st.rerun()

        st.markdown("### 🗳️ Paso 1 — Elige una Decision Estrategica")
        st.markdown("<p style='color:rgba(255,255,255,0.45);font-size:0.85rem;margin-top:-8px;'>Si aciertas la pregunta, los efectos de esta decision se aplicaran a la ciudad.</p>",unsafe_allow_html=True)

        cols = st.columns(4)
        for i,(nom_dec,ef) in enumerate(DECISIONES.items()):
            col_card     = cols[i%4]
            disponible_en = cooldowns.get(nom_dec, 0)
            disp          = (disponible_en == 0) or (ronda >= disponible_en)
            rondas_falta  = max(0, disponible_en - ronda) if disponible_en > 0 else 0

            # Efectos de la decisión
            filas_ef = ""
            for k,v in ef.items():
                if k=="emoji": continue
                col_ind,em_ind = IND_COLOR.get(k,("#94a3b8","•"))
                signo   = "+" if v>0 else ""
                col_val = "#22c55e" if v>0 else "#ef4444"
                filas_ef += (
                    "<div style='display:flex;justify-content:space-between;"
                    "align-items:center;padding:3px 0;"
                    "border-bottom:1px solid rgba(255,255,255,0.04);'>"
                    "<span style='color:"+col_ind+";font-size:0.74rem;'>"
                    "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>"+em_ind+"</span>"
                    " "+IND_LABEL[k]+"</span>"
                    "<span style='color:"+col_val+";font-size:0.82rem;font-weight:700;'>"+signo+str(v)+"</span>"
                    "</div>")

            dec_emoji_raw = ef.get("emoji","")

            if disp:
                borde   = "rgba(59,130,246,0.5)"
                bg_card = "rgba(59,130,246,0.07)"
                opac    = "1"
                btn_txt = "✅ Elegir decisión"
                cd_html = ""
                glow    = "0 0 20px rgba(59,130,246,0.12)"
            else:
                borde   = "rgba(245,158,11,0.4)"
                bg_card = "rgba(245,158,11,0.05)"
                opac    = "0.6"
                btn_txt = "🔒 En cooldown"
                glow    = "none"
                # Puntos de rondas restantes
                puntos_html = "".join([
                    "<span style='display:inline-block;width:9px;height:9px;"
                    "border-radius:50%;background:"
                    +("'#fbbf24'" if j < rondas_falta else "'rgba(255,255,255,0.15)'")+
                    ";margin:2px;box-shadow:"+(
                        "'0 0 6px #fbbf24'" if j < rondas_falta else "none"
                    )+";'></span>"
                    for j in range(COOLDOWN)
                ])
                disp_en_ronda = disponible_en
                cd_pct = int((COOLDOWN - rondas_falta) / COOLDOWN * 100)
                cd_html = (
                    "<div style='background:rgba(245,158,11,0.1);"
                    "border:1px solid rgba(245,158,11,0.3);"
                    "border-radius:10px;padding:8px 10px;margin-top:8px;text-align:center;'>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;"
                    "color:#fbbf24;letter-spacing:1px;margin-bottom:5px;'>🔒 COOLDOWN</div>"
                    "<div style='display:flex;justify-content:center;gap:5px;margin-bottom:5px;'>"
                    +puntos_html+
                    "</div>"
                    "<div style='height:4px;background:rgba(255,255,255,.08);"
                    "border-radius:2px;overflow:hidden;margin-bottom:5px;'>"
                    "<div style='width:"+str(cd_pct)+"%;height:4px;background:#fbbf24;"
                    "border-radius:2px;box-shadow:0 0 6px #fbbf24;'></div></div>"
                    "<div style='font-size:0.7rem;color:#fbbf24;font-weight:700;'>"
                    +str(rondas_falta)+" ronda"+("s" if rondas_falta!=1 else "")+" · disponible en R"+str(disp_en_ronda)
                    +"</div></div>")

            with col_card:
                st.markdown(
                    "<div style='background:"+bg_card+";border:1px solid "+borde+";"
                    "border-radius:14px;padding:14px;opacity:"+opac+";"
                    "box-shadow:"+glow+";min-height:220px;'>"
                    "<div style='text-align:center;margin-bottom:8px;'>"
                    "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                    "font-size:1.8rem;'>"+dec_emoji_raw+"</span></div>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:0.7rem;"
                    "color:#e2e8f0;font-weight:700;text-align:center;margin-bottom:8px;'>"
                    +nom_dec+"</div>"
                    "<div style='border-top:1px solid rgba(255,255,255,0.06);padding-top:8px;'>"
                    +filas_ef+"</div>"
                    +cd_html+
                    "</div>", unsafe_allow_html=True)
                if st.button(btn_txt, key="dec_"+str(i),
                             disabled=not disp, use_container_width=True):
                    st.session_state["decision_elegida"]  = nom_dec
                    st.session_state["decision_efectos"]  = {k:v for k,v in ef.items() if k!="emoji"}
                    st.session_state["pregunta_actual"]   = seleccionar_pregunta(st.session_state.get("dificultad","Medio"))
                    st.session_state["timer_inicio"]      = None
                    st.session_state["tiempo_agotado"]    = False
                    st.session_state["fase_ronda"]        = "pregunta"
                    st.rerun()

    # ══════════════════════════════════════════════
    # FASE 2: PREGUNTA CON TEMPORIZADOR AUTOMÁTICO
    # ══════════════════════════════════════════════
    elif fase == "pregunta":
        pregunta = st.session_state["pregunta_actual"]
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]

        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        tiempo_restante = max(0.0, TIEMPO_PREGUNTA - (time.time() - st.session_state["timer_inicio"]))
        seg = int(tiempo_restante)

        # Timeout automático
        if tiempo_restante <= 0:
            st.session_state["tiempo_agotado"]     = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.session_state["incorrectas"]        = st.session_state.get("incorrectas",0) + 1
            st.rerun()

        # Chip de decisión elegida
        ef_resumen = "  ".join([IND_COLOR[k][1]+" "+("+"+str(v) if v>0 else str(v))
                                 for k,v in ef_dec.items() if k in IND_COLOR])
        dec_emoji = DECISIONES.get(nom_dec,{}).get("emoji","")
        st.markdown(
            "<div style='background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.25);"
            "border-radius:12px;padding:8px 16px;margin-bottom:12px;display:flex;"
            "flex-wrap:wrap;gap:6px;align-items:center;'>"
            "<span style='color:#a78bfa;font-size:0.8rem;'>Decisión:</span>"
            "<span style='color:#f1f5f9;font-weight:700;font-size:.88rem;'>"+dec_emoji+" "+nom_dec+"</span>"
            "<span style='color:rgba(255,255,255,0.3);font-size:0.76rem;'>"+ef_resumen+"</span>"
            "</div>", unsafe_allow_html=True)

        # Colores del timer
        cat_color = CAT_COLOR.get(pregunta["cat"],"#94a3b8")
        q_safe    = pregunta["q"].replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
        cat_safe  = pregunta["cat"]
        pct       = max(0, int(seg / TIEMPO_PREGUNTA * 100))
        if seg > TIEMPO_PREGUNTA * 0.5:    tcol = "#10b981"
        elif seg > TIEMPO_PREGUNTA * 0.25: tcol = "#f59e0b"
        else:                              tcol = "#ef4444"
        urgente = ("<div style='color:#ef4444;font-size:.72rem;font-weight:700;"
                   "margin-top:5px;text-align:center;letter-spacing:1px;'>⚠️ ¡RESPONDE YA!</div>"
                   if seg <= 8 else "")

        left_col, right_col = st.columns([1, 2])
        with left_col:
            st.markdown(
                "<div style='background:rgba(0,0,0,0.5);border:3px solid "+tcol+";"
                "border-radius:16px;padding:16px;text-align:center;"
                "box-shadow:0 0 30px "+tcol+"55;'>"
                "<div style='font-size:.65rem;color:rgba(255,255,255,.4);"
                "font-family:Orbitron,sans-serif;letter-spacing:2px;margin-bottom:4px;'>⏱️ TIEMPO</div>"
                "<div style='font-size:3.5rem;font-weight:900;color:"+tcol+";"
                "text-shadow:0 0 20px "+tcol+";font-variant-numeric:tabular-nums;line-height:1;'>"
                +str(seg)+"</div>"
                "<div style='font-size:.7rem;color:rgba(255,255,255,.35);margin-top:2px;'>segundos</div>"
                "<div style='height:8px;background:rgba(255,255,255,.08);border-radius:4px;"
                "margin-top:10px;overflow:hidden;'>"
                "<div style='width:"+str(pct)+"%;height:8px;border-radius:4px;"
                "background:linear-gradient(90deg,"+tcol+"88,"+tcol+");"
                "box-shadow:0 0 10px "+tcol+";'></div></div>"
                +urgente+"</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown(
                "<div style='background:rgba(8,12,30,.9);border:1px solid "+cat_color+"55;"
                "border-radius:14px;padding:16px;box-shadow:0 0 20px "+cat_color+"14;'>"
                "<div style='background:"+cat_color+"22;color:"+cat_color+";"
                "border:1px solid "+cat_color+"44;border-radius:20px;"
                "padding:3px 14px;font-size:.7rem;font-weight:600;"
                "display:inline-block;margin-bottom:10px;'>"+cat_safe+"</div>"
                "<p style='color:#f1f5f9;font-size:1.05rem;font-weight:600;"
                "line-height:1.6;margin:0;'>"+q_safe+"</p>"
                "</div>", unsafe_allow_html=True)

        st.markdown(
            "<div style='font-family:Orbitron,sans-serif;font-size:.6rem;"
            "color:rgba(0,212,255,.5);letter-spacing:2px;margin:12px 0 8px;'>"
            "SELECCIONA TU RESPUESTA</div>", unsafe_allow_html=True)

        cols_op = st.columns(2)
        respondio = False
        for idx_op, op_texto in enumerate(pregunta["ops"]):
            letra = chr(65 + idx_op)
            with cols_op[idx_op % 2]:
                if st.button(f"{letra})  {op_texto}", key=f"op_{idx_op}",
                             use_container_width=True):
                    es_correcta = (idx_op == pregunta["ok"])
                    st.session_state["respuesta_correcta"] = es_correcta
                    st.session_state["tiempo_agotado"]     = False
                    st.session_state["fase_ronda"]         = "resultado_pregunta"
                    if es_correcta:
                        st.session_state["correctas"]   = st.session_state.get("correctas",0) + 1
                    else:
                        st.session_state["incorrectas"] = st.session_state.get("incorrectas",0) + 1
                    respondio = True
                    st.rerun()

        # ── Auto-refresh 1s para actualizar el reloj automáticamente ──
        if not respondio:
            time.sleep(1)
            st.rerun()

    # ══════════════════════════════════════════════
    # FASE 3: RESULTADO DE PREGUNTA
    # ══════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        correcto    = st.session_state.get("respuesta_correcta", False)
        timeout     = st.session_state.get("tiempo_agotado", False)
        nom_dec     = st.session_state.get("decision_elegida","")
        ef_dec      = st.session_state.get("decision_efectos",{})
        pregunta    = st.session_state.get("pregunta_actual",{})

        if correcto:
            col_r,bg_r,ico,tit = "#22c55e","rgba(34,197,94,0.1)","✅","¡Respuesta Correcta!"
            sub = "Los efectos de tu decisión se aplicarán a la ciudad."
        elif timeout:
            col_r,bg_r,ico,tit = "#f59e0b","rgba(245,158,11,0.1)","⏰","¡Tiempo Agotado!"
            sub = "No respondiste a tiempo. La decisión no tendrá efecto."
        else:
            col_r,bg_r,ico,tit = "#ef4444","rgba(239,68,68,0.1)","❌","Respuesta Incorrecta"
            sub = "La decisión no tendrá efecto esta ronda."

        resp_correcta_txt = pregunta.get("ops",[""])[pregunta.get("ok",0)] if pregunta else ""

        st.markdown(
            "<div style='background:"+bg_r+";border:2px solid "+col_r+"44;"
            "border-radius:16px;padding:28px;text-align:center;margin-bottom:20px;'>"
            "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
            "font-size:3rem;line-height:1;'>"+ico+"</div>"
            "<h2 style='color:"+col_r+";margin:10px 0 6px;font-family:Orbitron,sans-serif;"
            "font-size:1.3rem;'>"+tit+"</h2>"
            "<p style='color:rgba(255,255,255,0.5);margin:0 0 10px;font-size:.9rem;'>"+sub+"</p>"
            +(  "<div style='background:rgba(255,255,255,0.05);border-radius:8px;"
                "padding:8px 16px;display:inline-block;font-size:.85rem;'>"
                "<span style='color:rgba(255,255,255,.4);'>Respuesta correcta: </span>"
                "<span style='color:#22c55e;font-weight:700;'>"+resp_correcta_txt+"</span></div>"
                if not correcto else "")
            +"</div>", unsafe_allow_html=True)

        progreso_r = obtener_progreso(gid)
        ind_r = {k: progreso_r[k] for k in ["economia","medio_ambiente","energia","bienestar_social"]}

        # Cooldown siempre se aplica independiente de si acertó o no
        actualizar_cooldown(gid, nom_dec, ronda)
        if correcto:
            nueva_ind_r = aplicar_efectos(ind_r, ef_dec)
            st.markdown("**Efectos aplicados:**")
            ef_cols = st.columns(4)
            for ci,(k,v) in enumerate(ef_dec.items()):
                if k in IND_COLOR:
                    cc,ei = IND_COLOR[k]
                    sg = "+" if v>0 else ""
                    cv = "#22c55e" if v>0 else "#ef4444"
                    with ef_cols[ci % 4]:
                        st.markdown(
                            "<div style='background:rgba(5,10,20,.8);border:1px solid "+cc+"33;"
                            "border-radius:8px;padding:8px;text-align:center;'>"
                            "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                            "font-size:1.3rem;'>"+ei+"</div>"
                            "<div style='font-size:.7rem;color:"+cc+";'>"+IND_LABEL[k]+"</div>"
                            "<div style='font-size:1rem;font-weight:900;color:"+cv+";'>"+sg+str(v)+"</div>"
                            "</div>", unsafe_allow_html=True)
        else:
            nueva_ind_r = ind_r

        # Verificar fin del juego
        vals_r = list(nueva_ind_r.values())
        juego_terminado = ronda >= TOTAL_RONDAS

        st.markdown("<br>", unsafe_allow_html=True)
        btn_lbl = "⚡ Continuar al Evento" if not juego_terminado else "🏁 Ver Resultado Final"
        if st.button(btn_lbl, use_container_width=True, key="btn_continuar_res"):
            if correcto:
                actualizar_progreso(gid, nueva_ind_r["economia"], nueva_ind_r["medio_ambiente"],
                                    nueva_ind_r["energia"], nueva_ind_r["bienestar_social"], ronda)
            if juego_terminado:
                st.session_state["indicadores_finales"] = nueva_ind_r
                st.session_state["rondas_completadas"]  = ronda
                # Ciudad colapsa si hay indicador crítico (≤30)
                hay_critico = any(v <= 30 for v in nueva_ind_r.values())
                from achievements import calcular_puntaje
                logros_tmp  = st.session_state.get("logros_obtenidos", [])
                dif_tmp     = st.session_state.get("dificultad", "Medio")
                correctas_t = st.session_state.get("correctas", 0)
                incorrectas_t = st.session_state.get("incorrectas", 0)
                puntaje_tmp = calcular_puntaje(nueva_ind_r, correctas_t, incorrectas_t, logros_tmp, dif_tmp)
                if hay_critico or puntaje_tmp < 60:
                    st.session_state["resultado"] = "derrota"
                else:
                    st.session_state["resultado"] = "victoria"
                navegar("fin")
            else:
                st.session_state["fase_ronda"] = "evento"
                st.rerun()

    # ══════════════════════════════════════════════
    # FASE 4: EVENTO ALEATORIO
    # ══════════════════════════════════════════════
    elif fase == "evento":
        dificultad = st.session_state.get("dificultad","Medio")
        mult_neg   = DIFICULTADES[dificultad]["mult_neg"]
        mult_pos   = DIFICULTADES[dificultad]["mult_pos"]

        if st.session_state["evento_ronda"] is None:
            if ronda >= 7 and random.random() < 0.35:
                base_ev  = random.choice(EVENTOS_EPICOS).copy()
                es_epico = True
            else:
                neg_pool = [e for e in EVENTOS if any(v<0 for v in e["efectos"].values())]
                pos_pool = [e for e in EVENTOS if all(v>=0 for v in e["efectos"].values())]
                prob_neg = DIFICULTADES[dificultad]["evento_neg_prob"]
                base_ev  = random.choice(neg_pool if random.random()<prob_neg else pos_pool).copy()
                es_epico = False
            efectos_mod = {k: int(v*(mult_neg if v<0 else mult_pos))
                           for k,v in base_ev["efectos"].items()}
            base_ev["efectos"] = efectos_mod
            base_ev["epico"]   = es_epico
            st.session_state["evento_ronda"] = base_ev

        evento   = st.session_state["evento_ronda"]
        efectos  = evento["efectos"]
        es_epico = evento.get("epico", False)
        positivo = sum(efectos.values()) >= 0
        col_ev   = "#22c55e" if positivo else "#ef4444"
        bg_ev    = "rgba(34,197,94,0.08)" if positivo else "rgba(239,68,68,0.08)"
        borde_ev = "rgba(34,197,94,0.45)" if positivo else "rgba(239,68,68,0.45)"
        if es_epico:
            col_ev,bg_ev,borde_ev = "#f59e0b","rgba(245,158,11,0.1)","rgba(245,158,11,0.5)"

        progreso_ev = obtener_progreso(gid)
        ind_ev = {k: progreso_ev[k] for k in ["economia","medio_ambiente","energia","bienestar_social"]}
        nueva_ind_ev = aplicar_efectos(ind_ev, efectos)

        badge_epico = ("<div style='background:#f59e0b;color:#000;font-family:Orbitron,sans-serif;"
                       "font-size:0.6rem;font-weight:900;border-radius:20px;padding:2px 12px;"
                       "display:inline-block;margin-bottom:8px;letter-spacing:2px;'>⚡ EVENTO ÉPICO</div>"
                       if es_epico else "")

        filas_ef = ""
        for k,v in efectos.items():
            ci,ei = IND_COLOR.get(k,("#94a3b8","•"))
            sg = "+" if v>0 else ""
            cv = "#22c55e" if v>0 else "#ef4444"
            antes   = ind_ev.get(k,0)
            despues = nueva_ind_ev.get(k,0)
            filas_ef += (
                "<div style='display:flex;align-items:center;justify-content:center;gap:10px;"
                "background:rgba(255,255,255,0.04);border-radius:8px;padding:6px 14px;"
                "margin:4px auto;max-width:340px;'>"
                "<span style='color:"+ci+";font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                "font-size:1rem;'>"+ei+"</span>"
                "<span style='color:#e2e8f0;font-size:.85rem;'>"+IND_LABEL.get(k,k)+"</span>"
                "<span style='color:rgba(255,255,255,.3);'>"+str(antes)+"</span>"
                "<span style='color:rgba(255,255,255,.2);'>→</span>"
                "<span style='color:"+cv+";font-weight:700;'>"+str(despues)+"</span>"
                "<span style='color:"+cv+";font-size:.8rem;'>("+sg+str(v)+")</span></div>")

        st.markdown(
            "<div style='background:"+bg_ev+";border:2px solid "+borde_ev+";"
            "border-radius:16px;padding:28px;text-align:center;"
            "box-shadow:0 0 40px "+col_ev+"22;'>"
            +badge_epico+
            "<div style='font-size:.72rem;color:rgba(255,255,255,.4);"
            "font-family:Orbitron,sans-serif;letter-spacing:2px;margin-bottom:6px;'>"
            "EVENTO — RONDA "+str(ronda)+"</div>"
            "<h2 style='color:#f1f5f9;margin:0 0 14px;font-size:1.3rem;"
            "font-family:Orbitron,sans-serif;'>"+evento["nombre"]+"</h2>"
            +filas_ef+"</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⏭️ FINALIZAR RONDA "+str(ronda)+" / "+str(TOTAL_RONDAS),
                     use_container_width=True):
            actualizar_progreso(gid, nueva_ind_ev["economia"], nueva_ind_ev["medio_ambiente"],
                                nueva_ind_ev["energia"], nueva_ind_ev["bienestar_social"], ronda+1)
            if any(v <= 20 for v in nueva_ind_ev.values()):
                st.session_state["ninguno_critico"] = False
            decrementar_cooldowns(gid)
            st.session_state.update({
                "pregunta_actual":None,"respuesta_correcta":False,
                "decision_elegida":None,"decision_efectos":None,
                "evento_ronda":None,"fase_ronda":"decision",
                "timer_inicio":None,"tiempo_agotado":False,
                "atributo_activo":None,
            })
            st.rerun()
