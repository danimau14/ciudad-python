import streamlit as st
from navigation import navegar
from database import login_grupo, obtener_progreso, reiniciar_progreso, dificultad_jugada
from config import TOTAL_RONDAS


def pantalla_login():
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown(
            "<div style='text-align:center;'>"
            "<span class='emoji-title' style='font-size:1.8rem;'>🔐</span></div>"
            "<div class='game-title' style='font-size:1.6rem;'>Iniciar Sesion</div>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("form_login"):
            nombre = st.text_input("👥 Nombre del grupo")
            pw     = st.text_input("🔒 Contrasena", type="password")
            sub    = st.form_submit_button("Entrar 🚀", use_container_width=True)
        if sub:
            resultado = login_grupo(nombre, pw)
            if resultado:
                gid, dificultad_guardada = resultado
                # Dificultad seleccionada en pantalla inicio
                dif_seleccionada = st.session_state.get("dificultad", "Medio")
                progreso = obtener_progreso(gid)
                partida_terminada = progreso.get("partida_terminada", 0) == 1

                st.session_state["grupo_id"]        = gid
                st.session_state["grupo_nombre"]    = nombre.strip()
                st.session_state["fase_ronda"]      = "decision"
                st.session_state["ranking_guardado"]= False

                if partida_terminada and dif_seleccionada == dificultad_guardada:
                    # ── Mismo nivel ya terminado → ir a fin (JUGAR DE NUEVO) ──
                    st.session_state["dificultad"]          = dificultad_guardada
                    st.session_state["resultado"]           = "victoria"
                    st.session_state["indicadores_finales"] = {
                        k: progreso[k] for k in ["economia","medio_ambiente","energia","bienestar_social"]
                    }
                    st.session_state["rondas_completadas"]  = TOTAL_RONDAS
                    st.session_state["ranking_guardado"]    = True
                    navegar("fin")

                elif dif_seleccionada != dificultad_guardada:
                    # ── Nivel diferente → reiniciar y jugar como primera vez ──
                    reiniciar_progreso(gid)
                    # Actualizar dificultad del grupo en DB
                    from database import get_conn
                    conn = get_conn()
                    conn.execute("UPDATE grupos SET dificultad=? WHERE id=?",
                                 (dif_seleccionada, gid))
                    conn.commit()
                    conn.close()
                    st.session_state["dificultad"]    = dif_seleccionada
                    st.session_state.update({
                        "pregunta_actual": None, "respuesta_correcta": False,
                        "decision_elegida": None, "decision_efectos": None,
                        "evento_ronda": None, "correctas": 0, "incorrectas": 0,
                        "ninguno_critico": True, "preguntas_usadas": [],
                        "timer_inicio": None, "tiempo_agotado": False,
                    })
                    navegar("juego")

                else:
                    # ── Mismo nivel, partida en curso → continuar ──
                    st.session_state["dificultad"] = dificultad_guardada
                    navegar("juego")
            else:
                st.error("Credenciales incorrectas.")
        if st.button("⬅️ Volver", use_container_width=True):
            navegar("inicio")
