import streamlit as st
import random
import time


def pantalla_juego():
    # Imports dentro de la función para evitar ImportError al cargar el módulo
    from session_manager import navegar
    from database import (obtenerprogreso, obtenerestudiantes, obtenercooldowns,
                          actualizarprogreso, actualizarcooldown, decrementarcooldowns)
    from config import (DECISIONES, EVENTOS, TOTALRONDAS, TIEMPOPREGUNTA,
                        INDCOLOR, INDLABEL, PREGUNTAS, COOLDOWN)

    def _aplicar_efectos(ind, ef):
        r = dict(ind)
        for k, v in ef.items():
            if k in r:
                r[k] = max(0, min(100, r[k] + v))
        return r

    def _seleccionar_pregunta():
        usadas = st.session_state.get("preguntas_usadas", [])
        disponibles = [i for i in range(len(PREGUNTAS)) if i not in usadas]
        if not disponibles:
            st.session_state["preguntas_usadas"] = []
            disponibles = list(range(len(PREGUNTAS)))
        idx = random.choice(disponibles)
        st.session_state.setdefault("preguntas_usadas", []).append(idx)
        return PREGUNTAS[idx]

    def _barra(nombre, valor, emoji):
        valor = max(0, min(100, valor))
        if valor >= 60:
            color, badge, bg, borde = "#10b981","Estable","rgba(16,185,129,0.08)","rgba(16,185,129,0.3)"
        elif valor >= 30:
            color, badge, bg, borde = "#f59e0b","Precaucion","rgba(245,158,11,0.08)","rgba(245,158,11,0.3)"
        else:
            color, badge, bg, borde = "#ef4444","Critico","rgba(239,68,68,0.1)","rgba(239,68,68,0.35)"
        st.markdown(
            "<div style='background:" + bg + ";border:1px solid " + borde + ";"
            "border-radius:14px;padding:14px 18px;margin-bottom:10px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:8px'>"
            "<span style='font-weight:700;color:#f1f5f9'>" + emoji + " " + nombre + "</span>"
            "<span style='font-size:.7rem;color:" + color + ";border:1px solid " + color + "44;"
            "border-radius:20px;padding:2px 9px;font-family:Courier Prime,monospace'>"
            + badge + "</span></div>"
            "<div style='background:rgba(255,255,255,0.08);border-radius:6px;height:8px'>"
            "<div style='width:" + str(valor) + "%;background:" + color + ";height:8px;"
            "border-radius:6px'></div></div>"
            "<div style='text-align:right;margin-top:4px;font-size:.82rem;font-weight:700;color:"
            + color + "'>" + str(valor) + "/100</div></div>",
            unsafe_allow_html=True
        )

    # ── Setup ────────────────────────────────────────────────────────────────
    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    progreso    = obtenerprogreso(gid)
    estudiantes = obtenerestudiantes(gid)
    cooldowns   = obtenercooldowns(gid)
    ronda       = progreso["ronda_actual"]
    nombre_grp  = st.session_state.get("grupo_nombre", "")
    est_turno   = estudiantes[(ronda - 1) % len(estudiantes)]

    ind = {
        "economia":       progreso["economia"],
        "medioambiente":  progreso["medioambiente"],
        "energia":        progreso["energia"],
        "bienestarsocial":progreso["bienestarsocial"],
    }

    # ── Fin de juego: SOLO por 10 rondas ────────────────────────────────────
    if ronda > TOTALRONDAS:
        puntaje = int(sum(ind.values()) / 4)
        colapso = puntaje < 50 or any(v < 20 for v in ind.values())
        st.session_state.update(
            resultado="colapso" if colapso else "victoria",
            indicadores_finales=ind,
            rondas_completadas=TOTALRONDAS,
            puntaje_final=puntaje,
        )
        navegar("fin")
        return

    # ── Cabecera ─────────────────────────────────────────────────────────────
    top1, top2 = st.columns([3, 1])
    with top1:
        st.markdown(
            "<h1 style='margin:0;background:linear-gradient(90deg,#a78bfa,#60a5fa);"
            "-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:1.8rem'>"
            + nombre_grp + "</h1>",
            unsafe_allow_html=True
        )
        chips = " ".join(
            "<span style='background:" + ("rgba(167,139,250,0.3)" if e == est_turno else "rgba(255,255,255,0.06)") + ";"
            "border:1px solid " + ("rgba(167,139,250,0.5)" if e == est_turno else "rgba(255,255,255,0.08)") + ";"
            "border-radius:20px;padding:3px 12px;margin:2px;font-size:.82rem;"
            "color:" + ("#c4b5fd" if e == est_turno else "#94a3b8") + ";display:inline-block'>"
            + ("✏️ " if e == est_turno else "") + e + "</span>"
            for e in estudiantes
        )
        st.markdown("<div style='margin-top:6px'>" + chips + "</div>", unsafe_allow_html=True)

    with top2:
        if st.button("MENU", use_container_width=True, key="btn_menu"):
            st.session_state["_menu_abierto"] = not st.session_state.get("_menu_abierto", False)
            st.rerun()
        if st.session_state.get("_menu_abierto", False):
            if st.button("INSTRUCCIONES", use_container_width=True, key="btn_instr"):
                st.session_state["_ver_instrucciones"] = True
                st.session_state["_menu_abierto"] = False
                st.rerun()
            if st.button("VOLVER AL INICIO", use_container_width=True, key="btn_inicio"):
                navegar("inicio")
            if st.button("VOLVER AL LOBBY", use_container_width=True, key="btn_lobby"):
                navegar("lobby")

    # ── HUD métricas ─────────────────────────────────────────────────────────
    pct = int((ronda - 1) / TOTALRONDAS * 100)
    fase = st.session_state.get("fase_ronda", "decision")
    fase_txt = {"decision":"Elegir Dec...","pregunta":"Responder...","evento":"Evento","resultado_pregunta":"Resultado"}
    m1,m2,m3,m4 = st.columns(4)
    with m1: st.metric("Ronda", str(ronda)+"/"+str(TOTALRONDAS))
    with m2: st.metric("Turno", est_turno)
    with m3: st.metric("Progreso", str(pct)+"%")
    with m4: st.metric("Fase", fase_txt.get(fase, fase))
    st.markdown(
        "<div style='background:rgba(255,255,255,0.07);border-radius:4px;height:5px;margin:2px 0 14px'>"
        "<div style='width:"+str(pct)+"%;background:linear-gradient(90deg,#a78bfa,#60a5fa);height:5px;border-radius:4px'></div></div>",
        unsafe_allow_html=True
    )

    # ── Panel instrucciones ───────────────────────────────────────────────────
    if st.session_state.get("_ver_instrucciones", False):
        st.markdown(
            "<div style='background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.3);"
            "border-radius:16px;padding:20px 24px;margin-bottom:16px'>"
            "<h3 style='color:#a78bfa;margin-top:0'>Instrucciones</h3>"
            "<ul style='color:rgba(255,255,255,.6);font-size:.9rem;line-height:1.9;"
            "font-family:Inter,sans-serif;padding-left:18px'>"
            "<li>Elige una <b style='color:#e2e8f0'>decision estrategica</b> para la ciudad.</li>"
            "<li>El estudiante en turno responde una <b style='color:#e2e8f0'>pregunta de opcion multiple</b>.</li>"
            "<li>Si <b style='color:#4ade80'>acierta</b>, se aplican los efectos de la decision.</li>"
            "<li>Si <b style='color:#f87171'>falla</b>, todos los indicadores pierden puntos.</li>"
            "<li>Al final de cada ronda ocurre un <b style='color:#fbbf24'>evento aleatorio</b>.</li>"
            "<li>El juego termina al completar las <b style='color:#60a5fa'>10 rondas</b>.</li>"
            "</ul></div>",
            unsafe_allow_html=True
        )
        if st.button("REGRESAR AL JUEGO", use_container_width=True, key="btn_regresar"):
            st.session_state["_ver_instrucciones"] = False
            st.rerun()
        return

    # ── Indicadores ──────────────────────────────────────────────────────────
    ci1,ci2,ci3,ci4 = st.columns(4)
    with ci1: _barra("Economia",      ind["economia"],        "💰")
    with ci2: _barra("Medio Ambiente", ind["medioambiente"],   "🌿")
    with ci3: _barra("Energia",        ind["energia"],         "⚡")
    with ci4: _barra("Bienestar",      ind["bienestarsocial"], "❤️")
    st.markdown("---")

    # ══════ DECISION ══════════════════════════════════════════════════════════
    if fase == "decision":
        st.markdown(
            "<h3 style='color:#f1f5f9;margin-bottom:4px'>Paso 1 - Elige una Decision Estrategica</h3>"
            "<p style='color:rgba(255,255,255,.4);font-size:.85rem;margin-top:-6px;"
            "font-family:Courier Prime,monospace'>Si aciertas, los efectos se aplicaran a la ciudad.</p>",
            unsafe_allow_html=True
        )
        cols = st.columns(4)
        for i, (nom_dec, ef) in enumerate(DECISIONES.items()):
            col = cols[i % 4]
            disponible_en = cooldowns.get(nom_dec, 0)
            disp = (disponible_en == 0 or ronda >= disponible_en)
            rondas_falta  = max(0, disponible_en - ronda) if disponible_en > 0 else 0

            filas_ef = ""
            for k, v in ef.items():
                if k == "emoji": continue
                ind_data = INDCOLOR.get(k, ("#94a3b8",""))
                col_ind = ind_data[0] if isinstance(ind_data, tuple) else "#94a3b8"
                em_ind  = ind_data[1] if isinstance(ind_data, tuple) else ""
                signo   = "+" if v > 0 else ""
                col_val = "#4ade80" if v > 0 else "#f87171"
                filas_ef += (
                    "<div style='display:flex;justify-content:space-between;padding:3px 0;"
                    "border-bottom:1px solid rgba(255,255,255,0.05)'>"
                    "<span style='color:"+col_ind+";font-size:.74rem'>"+em_ind+" "+INDLABEL.get(k,"")+"</span>"
                    "<span style='color:"+col_val+";font-size:.82rem;font-weight:700'>"+signo+str(v)+"</span>"
                    "</div>"
                )

            borde = "rgba(167,139,250,0.45)" if disp else "rgba(245,158,11,0.3)"
            bg_c  = "rgba(167,139,250,0.07)" if disp else "rgba(245,158,11,0.04)"
            opac  = "1" if disp else "0.5"
            overlay = ""
            if not disp:
                overlay = (
                    "<div style='position:absolute;inset:0;border-radius:14px;"
                    "background:rgba(0,0,0,0.45);display:flex;flex-direction:column;"
                    "align-items:center;justify-content:center;gap:6px'>"
                    "<span style='font-size:1.4rem'>⏳</span>"
                    "<span style='color:#fbbf24;font-weight:800;font-size:.88rem'>"
                    +str(rondas_falta)+" ronda"+("s" if rondas_falta!=1 else "")+"</span>"
                    "<span style='color:rgba(255,255,255,.4);font-size:.65rem'>En ronda "+str(disponible_en)+"</span>"
                    "</div>"
                )
            with col:
                st.markdown(
                    "<div style='position:relative;background:"+bg_c+";border:1px solid "+borde+";"
                    "border-radius:14px;padding:14px 12px;margin-bottom:4px;opacity:"+opac+";"
                    "min-height:185px'>"+overlay+
                    "<div style='font-size:1.5rem;margin-bottom:4px'>"+ef.get("emoji","")+"</div>"
                    "<div style='font-weight:700;color:#f1f5f9;font-size:.86rem;margin-bottom:8px;line-height:1.25'>"
                    +nom_dec+"</div>"+filas_ef+"</div>",
                    unsafe_allow_html=True
                )
                if st.button("ELEGIR", disabled=not disp, key="dec_"+nom_dec, use_container_width=True):
                    st.session_state["decision_elegida"] = nom_dec
                    st.session_state["decision_efectos"] = {k:v for k,v in ef.items() if k!="emoji"}
                    st.session_state["pregunta_actual"]  = _seleccionar_pregunta()
                    st.session_state["timer_inicio"]     = None
                    st.session_state["tiempo_agotado"]   = False
                    st.session_state["fase_ronda"]       = "pregunta"
                    st.rerun()

    # ══════ PREGUNTA ══════════════════════════════════════════════════════════
    elif fase == "pregunta":
        pregunta = st.session_state["pregunta_actual"]
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]

        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        tiempo_restante = max(0.0, TIEMPOPREGUNTA - (time.time() - st.session_state["timer_inicio"]))
        pct_timer = tiempo_restante / TIEMPOPREGUNTA
        col_timer = "#10b981" if pct_timer > 0.5 else "#f59e0b" if pct_timer > 0.25 else "#ef4444"
        seg = int(tiempo_restante)

        if tiempo_restante == 0:
            st.session_state["tiempo_agotado"]     = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

        ef_resumen = "  ".join(
            ("+" if v>0 else "")+str(v)+" "+INDLABEL.get(k,"")
            for k,v in ef_dec.items() if k in INDLABEL
        )
        st.markdown(
            "<div style='background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.3);"
            "border-radius:12px;padding:10px 18px;margin-bottom:14px;display:flex;flex-wrap:wrap;gap:8px;align-items:center'>"
            "<span style='color:#a78bfa;font-size:.82rem'>Decision:</span>"
            "<span style='color:#f1f5f9;font-weight:700'>"+DECISIONES.get(nom_dec,{}).get("emoji","")+" "+nom_dec+"</span>"
            "<span style='color:rgba(255,255,255,.35);font-size:.76rem'>"+ef_resumen+"</span></div>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='background:rgba(0,0,0,0.25);border:1px solid "+col_timer+"44;"
            "border-radius:14px;padding:12px 18px;margin-bottom:14px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:6px'>"
            "<span style='color:rgba(255,255,255,.5);font-size:.82rem'>Tiempo restante</span>"
            "<span style='color:"+col_timer+";font-weight:900;font-size:1.5rem'>"+str(seg)+"s</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,.08);border-radius:6px;height:10px;overflow:hidden'>"
            "<div style='width:"+str(int(pct_timer*100))+"%;height:10px;background:"+col_timer+";"
            "border-radius:6px;transition:width .95s linear'></div></div>"
            +("<div style='color:#ef4444;font-size:.74rem;font-weight:700;margin-top:4px;text-align:center'>Responde ya!</div>" if seg<=8 else "")
            +"</div>",
            unsafe_allow_html=True
        )

        cat_color = {
            "Python":"#6366f1","PSeInt":"#8b5cf6","Calculo":"#06b6d4",
            "Derivadas":"#10b981","Fisica MRU":"#f59e0b","Fisica MRUA":"#ef4444","Matrices":"#ec4899",
        }.get(pregunta.get("cat",""), "#94a3b8")
        st.markdown(
            "<div style='background:rgba(15,15,25,.85);border:1px solid "+cat_color+"44;"
            "border-radius:16px;padding:18px 22px;margin-bottom:16px'>"
            "<span style='background:"+cat_color+"22;color:"+cat_color+";"
            "border:1px solid "+cat_color+"55;border-radius:20px;padding:2px 12px;"
            "font-size:.72rem;font-weight:600;font-family:Courier Prime,monospace'>"
            +pregunta.get("cat","")+"</span>"
            "<p style='color:#f1f5f9;font-size:1rem;font-weight:600;line-height:1.6;"
            "font-family:Inter,sans-serif;margin:12px 0 0'>"+pregunta.get("q","")+"</p>"
            "</div>",
            unsafe_allow_html=True
        )
        opciones = [chr(65+i)+". "+op for i,op in enumerate(pregunta["ops"])]
        respuesta = st.radio("Selecciona tu respuesta:", opciones, key="radio_resp")
        if st.button("Confirmar Respuesta", use_container_width=True, type="primary"):
            st.session_state["respuesta_correcta"] = (opciones.index(respuesta) == pregunta["ok"])
            st.session_state["tiempo_agotado"]     = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.rerun()

    # ══════ RESULTADO PREGUNTA ════════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        pregunta     = st.session_state["pregunta_actual"]
        correcta     = st.session_state["respuesta_correcta"]
        agotado      = st.session_state.get("tiempo_agotado", False)
        nom_dec      = st.session_state["decision_elegida"]
        ef_dec       = st.session_state["decision_efectos"]
        penalizacion = 20 if (ronda % 2 == 0) else 10

        if correcta:
            nueva_ind = _aplicar_efectos(ind, ef_dec)
            actualizarprogreso(gid, nueva_ind["economia"], nueva_ind["medioambiente"],
                               nueva_ind["energia"], nueva_ind["bienestarsocial"], ronda)
            actualizarcooldown(gid, nom_dec, ronda)
            cambios_html = " ".join(
                "<span style='background:rgba(255,255,255,.07);border-radius:8px;"
                "padding:4px 10px;margin:3px;display:inline-block;color:#f1f5f9'>"
                +INDLABEL.get(k,"")+" <b style='color:"+("#4ade80" if v>0 else "#f87171")+"'>"
                +("+" if v>0 else "")+str(v)+"</b></span>"
                for k,v in ef_dec.items() if k in INDLABEL
            )
            st.markdown(
                "<div style='background:rgba(16,185,129,0.12);border:1px solid rgba(16,185,129,0.35);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:14px'>"
                "<div style='font-size:2.5rem'>✅</div>"
                "<h3 style='color:#34d399;margin:8px 0 4px'>Respuesta Correcta!</h3>"
                "<p style='color:#6ee7b7;margin-bottom:10px'>Los efectos de <b>"+nom_dec+"</b> se aplicaron</p>"
                "<div>"+cambios_html+"</div></div>",
                unsafe_allow_html=True
            )
        else:
            texto_ok = pregunta["ops"][pregunta["ok"]]
            causa    = "Tiempo agotado" if agotado else "Respuesta Incorrecta"
            aviso_par = " (ronda par: DOBLE)" if ronda % 2 == 0 else ""
            nueva_ind = {k: max(0, v - penalizacion) for k, v in ind.items()}
            actualizarprogreso(gid, nueva_ind["economia"], nueva_ind["medioambiente"],
                               nueva_ind["energia"], nueva_ind["bienestarsocial"], ronda)
            st.markdown(
                "<div style='background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.35);"
                "border-radius:16px;padding:22px;text-align:center;margin-bottom:14px'>"
                "<div style='font-size:2.5rem'>❌</div>"
                "<h3 style='color:#f87171;margin:8px 0 4px'>"+causa+"</h3>"
                "<p style='color:#fca5a5'>La correcta era: <b>"+texto_ok+"</b></p>"
                "<p style='color:#fca5a5;font-size:.84rem'>Todos pierden <b>"
                +str(penalizacion)+" puntos</b>"+aviso_par+"</p></div>",
                unsafe_allow_html=True
            )

        if st.button("Continuar", use_container_width=True):
            st.session_state["fase_ronda"] = "evento"
            st.rerun()

    # ══════ EVENTO ════════════════════════════════════════════════════════════
    elif fase == "evento":
        if st.session_state.get("evento_ronda") is None:
            st.session_state["evento_ronda"] = random.choice(EVENTOS)

        evento   = st.session_state["evento_ronda"]
        nom_ind  = evento["indicador"]
        ind_data = INDCOLOR.get(nom_ind, ("#94a3b8",""))
        col_ind  = ind_data[0] if isinstance(ind_data, tuple) else "#94a3b8"
        em_ind   = ind_data[1] if isinstance(ind_data, tuple) else ""
        positivo = evento["valor"] > 0
        col_ev   = "#10b981" if positivo else "#ef4444"
        bg_ev    = "rgba(16,185,129,0.1)" if positivo else "rgba(239,68,68,0.1)"

        prog_ev = obtenerprogreso(gid)
        ind_ev  = {
            "economia":       prog_ev["economia"],
            "medioambiente":  prog_ev["medioambiente"],
            "energia":        prog_ev["energia"],
            "bienestarsocial":prog_ev["bienestarsocial"],
        }
        nueva_ind    = _aplicar_efectos(ind_ev, {nom_ind: evento["valor"]})
        valor_antes  = ind_ev[nom_ind]
        valor_despues= nueva_ind[nom_ind]
        signo        = "+" if evento["valor"] > 0 else ""

        st.markdown(
            "<div style='background:"+bg_ev+";border:1px solid "+col_ev+"44;"
            "border-radius:16px;padding:26px;text-align:center;margin-bottom:14px'>"
            "<div style='font-size:2.2rem'>"+("🌟" if positivo else "⚠️")+"</div>"
            "<div style='font-size:.76rem;color:rgba(255,255,255,.4);text-transform:uppercase;"
            "letter-spacing:2px;margin:6px 0 2px;font-family:Courier Prime,monospace'>"
            "Evento Aleatorio - Ronda "+str(ronda)+"</div>"
            "<h2 style='color:#f1f5f9;margin:0 0 10px;font-size:1.4rem'>"+evento["nombre"]+"</h2>"
            "<div style='display:inline-block;background:rgba(255,255,255,.07);border-radius:12px;padding:8px 20px'>"
            "<span style='color:"+col_ind+"'>"+em_ind+" "+INDLABEL.get(nom_ind,nom_ind)+"</span>"
            "<span style='color:rgba(255,255,255,.3);margin:0 8px'>|</span>"
            "<span style='color:rgba(255,255,255,.5)'>"+str(valor_antes)+"</span>"
            "<span style='color:rgba(255,255,255,.3);margin:0 6px'>→</span>"
            "<span style='color:"+col_ev+";font-weight:700'>"+str(valor_despues)+"</span>"
            "<span style='color:"+col_ev+";margin-left:8px'>"+signo+str(evento["valor"])+"</span>"
            "</div></div>",
            unsafe_allow_html=True
        )

        if st.button("Finalizar Ronda "+str(ronda)+"/"+str(TOTALRONDAS), use_container_width=True):
            actualizarprogreso(gid,
                nueva_ind["economia"], nueva_ind["medioambiente"],
                nueva_ind["energia"],  nueva_ind["bienestarsocial"],
                ronda + 1)
            decrementarcooldowns(gid)
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False,
                decision_elegida=None, decision_efectos=None,
                evento_ronda=None, fase_ronda="decision",
                timer_inicio=None, tiempo_agotado=False,
            )
            st.rerun()
