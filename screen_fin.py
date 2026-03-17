import streamlit as st
from navigation import navegar
from database import guardar_ranking, reiniciar_progreso, marcar_partida_terminada
from achievements import LOGROS, calcular_logros, calcular_puntaje
from config import IND_COLOR, IND_LABEL, TOTAL_RONDAS, DIFICULTADES
from ui_components import barra_indicador


def pantalla_fin():
    resultado   = st.session_state.get("resultado","victoria")
    ind_fin     = st.session_state.get("indicadores_finales",{})
    rondas_comp = st.session_state.get("rondas_completadas",0)
    correctas   = st.session_state.get("correctas",0)
    incorrectas = st.session_state.get("incorrectas",0)
    dificultad  = st.session_state.get("dificultad","Medio")
    nombre_grp  = st.session_state.get("grupo_nombre","Equipo")
    gid         = st.session_state.get("grupo_id")

    stats  = {"correctas": correctas, "ninguno_critico": st.session_state.get("ninguno_critico",True)}
    logros = calcular_logros(ind_fin, stats)
    st.session_state["logros_obtenidos"] = logros
    puntaje= calcular_puntaje(ind_fin, correctas, incorrectas, logros, dificultad)

    # Colapso si puntaje final < 40
    if puntaje < 40:
        resultado = "colapso"

    # Guardar ranking solo una vez (evitar duplicados al recargar)
    if gid and not st.session_state.get("ranking_guardado", False):
        guardar_ranking(gid, nombre_grp, puntaje, correctas, incorrectas, dificultad, logros)
        marcar_partida_terminada(gid)  # bloquear reingreso al juego sin JUGAR DE NUEVO
        st.session_state["ranking_guardado"] = True

    if resultado == "victoria":
        col_r="#22c55e"; bg_r="rgba(34,197,94,0.08)"; ico="🏆"
        tit="¡CIUDAD EQUILIBRADA!"; sub="El equipo administró la ciudad exitosamente."
        st.balloons()
    else:
        col_r="#ef4444"; bg_r="rgba(239,68,68,0.08)"; ico="💥"
        tit="LA CIUDAD COLAPSÓ"; sub=f"Puntaje final ({puntaje} pts) por debajo del mínimo de 40."

    st.markdown(
        "<div style='background:"+bg_r+";border:2px solid "+col_r+"44;"
        "border-radius:16px;padding:30px;text-align:center;margin-bottom:20px;'>"
        "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;font-size:3.5rem;'>"+ico+"</div>"
        "<div style='font-family:Orbitron,sans-serif;font-size:clamp(1.3rem,4vw,2rem);"
        "font-weight:900;color:"+col_r+";margin:10px 0 6px;'>"+tit+"</div>"
        "<div style='color:rgba(255,255,255,.5);font-size:.9rem;margin-bottom:14px;'>"+sub+"</div>"
        "<div style='font-family:Orbitron,sans-serif;font-size:2.2rem;font-weight:900;"
        "color:#f59e0b;text-shadow:0 0 20px rgba(245,158,11,0.6);'>"+str(puntaje)+" PTS</div>"
        "<div style='font-size:.65rem;color:rgba(255,255,255,.3);font-family:Orbitron,sans-serif;"
        "letter-spacing:2px;'>PUNTAJE FINAL — "+dificultad.upper()+"</div>"
        "</div>", unsafe_allow_html=True)

    left, right = st.columns([3,2])
    with left:
        st.markdown("<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
                    "color:rgba(0,212,255,.5);letter-spacing:2px;margin-bottom:8px;'>"
                    "ESTADO FINAL DE LA CIUDAD</div>", unsafe_allow_html=True)
        barra_indicador("Economía",        ind_fin.get("economia",0),        "💰")
        barra_indicador("Medio Ambiente",  ind_fin.get("medio_ambiente",0),  "🌿")
        barra_indicador("Energía",         ind_fin.get("energia",0),         "⚡")
        barra_indicador("Bienestar Social",ind_fin.get("bienestar_social",0),"🏥")
    with right:
        vals  = [ind_fin.get(k,0) for k in ["economia","medio_ambiente","energia","bienestar_social"]]
        prom  = int(sum(vals)/4) if vals else 0
        total_p = correctas + incorrectas
        pct_c = int(correctas/total_p*100) if total_p>0 else 0
        st.markdown("<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
                    "color:rgba(0,212,255,.5);letter-spacing:2px;margin-bottom:8px;'>"
                    "ESTADÍSTICAS</div>", unsafe_allow_html=True)
        for lb,vl,cl in [("RONDAS",str(rondas_comp)+"/"+str(TOTAL_RONDAS),"#00d4ff"),
                          ("CORRECTAS",str(correctas),"#22c55e"),
                          ("INCORRECTAS",str(incorrectas),"#ef4444"),
                          ("PRECISIÓN",str(pct_c)+"%","#f59e0b"),
                          ("PROMEDIO",str(prom),"#8b5cf6"),
                          ("DIFICULTAD",dificultad,"#00d4ff")]:
            st.markdown(
                "<div style='display:flex;justify-content:space-between;align-items:center;"
                "background:rgba(5,10,20,.8);border:1px solid rgba(0,212,255,.1);"
                "border-radius:8px;padding:8px 14px;margin-bottom:5px;'>"
                "<span style='font-family:Orbitron,sans-serif;font-size:.58rem;"
                "color:rgba(255,255,255,.35);letter-spacing:1px;'>"+lb+"</span>"
                "<span style='font-family:Orbitron,sans-serif;font-weight:700;"
                "font-size:.9rem;color:"+cl+";'>"+vl+"</span></div>",
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if logros:
        st.markdown("<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
                    "color:rgba(245,158,11,.7);letter-spacing:2px;margin-bottom:10px;'>"
                    "🏅 LOGROS DESBLOQUEADOS</div>", unsafe_allow_html=True)
        cols_l = st.columns(min(len(logros),4))
        for i,lkey in enumerate(logros):
            l = LOGROS.get(lkey,{})
            with cols_l[i%4]:
                st.markdown(
                    "<div style='background:rgba(245,158,11,0.08);"
                    "border:1px solid rgba(245,158,11,0.3);border-radius:10px;"
                    "padding:12px;text-align:center;'>"
                    "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                    "font-size:1.5rem;'>"+l.get("icon","🏅")+"</div>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:.63rem;"
                    "color:#f59e0b;font-weight:700;margin:4px 0 2px;'>"+l.get("nombre","")+"</div>"
                    "<div style='font-size:.62rem;color:rgba(255,255,255,.3);'>"+l.get("desc","")+"</div>"
                    "</div>", unsafe_allow_html=True)

    # Mapa final
    eco=ind_fin.get("economia",50); amb=ind_fin.get("medio_ambiente",50)
    ene=ind_fin.get("energia",50);  bie=ind_fin.get("bienestar_social",50)
    def _zc(v): return "#22c55e" if v>60 else "#f59e0b" if v>30 else "#ef4444"
    def _zi(v,a,b,c): return a if v>60 else b if v>30 else c
    def _zona(icon,label,val):
        c=_zc(val)
        return ("<div style='background:rgba(5,10,20,0.8);border:1px solid "+c+"44;"
                "border-radius:12px;padding:14px;text-align:center;'>"
                "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                "font-size:2rem;line-height:1;'>"+icon+"</div>"
                "<div style='font-family:Orbitron,sans-serif;font-size:.6rem;color:"+c+";"
                "letter-spacing:1px;font-weight:700;margin:5px 0 3px;'>"+label+"</div>"
                "<div style='font-family:Orbitron,sans-serif;font-size:1rem;"
                "font-weight:900;color:"+c+";'>"+str(val)+"</div>"
                "<div style='height:5px;background:rgba(255,255,255,.08);"
                "border-radius:3px;margin-top:8px;overflow:hidden;'>"
                "<div style='width:"+str(val)+"%;height:5px;border-radius:3px;"
                "background:"+c+";box-shadow:0 0 8px "+c+";'></div></div></div>")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
        "color:rgba(0,212,255,.5);letter-spacing:3px;text-align:center;"
        "margin-bottom:10px;'>🗺️ MAPA FINAL DE LA CIUDAD</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;"
        "max-width:500px;margin:0 auto;'>"
        +_zona(_zi(eco,"🏭","🏗️","💸"),"Industrial",eco)
        +_zona(_zi(amb,"🌳","🌿","🏜️"),"Ambiental",amb)
        +_zona(_zi(ene,"⚡","🔋","🌑"),"Energética",ene)
        +_zona(_zi(bie,"🏘️","🏚️","😰"),"Residencial",bie)
        +"</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("🔄 JUGAR DE NUEVO", use_container_width=True):
            if gid:
                reiniciar_progreso(gid)  # resetea indicadores + partida_terminada=0
            # Mantener la misma dificultad actual
            dif_actual = st.session_state.get("dificultad", "Medio")
            st.session_state.update({
                "pregunta_actual": None, "respuesta_correcta": False,
                "decision_elegida": None, "decision_efectos": None,
                "evento_ronda": None, "fase_ronda": "decision",
                "preguntas_usadas": [], "timer_inicio": None, "tiempo_agotado": False,
                "correctas": 0, "incorrectas": 0, "ninguno_critico": True,
                "logros_ganados": [], "energia_rondas_altas": 0,
                "ranking_guardado": False,
                "dificultad": dif_actual,
            })
            navegar("lobby")
    with c2:
        if st.button("🏆 VER RANKING", use_container_width=True): navegar("ranking")
    with c3:
        if st.button("🏠 MENÚ PRINCIPAL", use_container_width=True): navegar("lobby")
