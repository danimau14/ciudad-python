import streamlit as st
from session_manager import navegar


def pantalla_fin():
    # Imports dentro de la función para evitar ImportError al cargar el módulo
    from database import reiniciarprogreso
    from config import INDLABEL, TOTALRONDAS

    def _barra(nombre, valor, emoji):
        valor = max(0, min(100, valor))
        if valor >= 60:
            color, badge, bg, borde = "#10b981","Estable","rgba(16,185,129,0.08)","rgba(16,185,129,0.3)"
        elif valor >= 30:
            color, badge, bg, borde = "#f59e0b","Precaucion","rgba(245,158,11,0.08)","rgba(245,158,11,0.3)"
        else:
            color, badge, bg, borde = "#ef4444","Critico","rgba(239,68,68,0.1)","rgba(239,68,68,0.35)"
        st.markdown(
            "<div style='background:"+bg+";border:1px solid "+borde+";"
            "border-radius:14px;padding:14px 18px;margin-bottom:10px'>"
            "<div style='display:flex;justify-content:space-between;margin-bottom:8px'>"
            "<span style='font-weight:700;color:#f1f5f9'>"+emoji+" "+nombre+"</span>"
            "<span style='font-size:.7rem;color:"+color+";border:1px solid "+color+"44;"
            "border-radius:20px;padding:2px 9px;font-family:Courier Prime,monospace'>"+badge+"</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,0.08);border-radius:6px;height:8px'>"
            "<div style='width:"+str(valor)+"%;background:"+color+";height:8px;border-radius:6px'></div></div>"
            "<div style='text-align:right;margin-top:4px;font-size:.82rem;font-weight:700;color:"+color+"'>"+str(valor)+"/100</div></div>",
            unsafe_allow_html=True
        )

    def _nivel(puntaje):
        if puntaje >= 85:   return "LEGENDARIO", "#fbbf24", "👑", "Gestion magistral de la ciudad"
        elif puntaje >= 70: return "EXCELENTE",  "#34d399", "🏆", "Ciudad prospera y equilibrada"
        elif puntaje >= 55: return "BUENO",      "#60a5fa", "🌟", "Ciudad estable con areas de mejora"
        elif puntaje >= 40: return "REGULAR",    "#f59e0b", "⚠️", "Ciudad en precaucion"
        else:               return "CRITICO",    "#ef4444", "🚨", "La ciudad esta en crisis"

    # ── Datos de sesión ───────────────────────────────────────────────────────
    ind_fin     = st.session_state.get("indicadores_finales", {})
    rondas_comp = st.session_state.get("rondas_completadas", 0)
    puntaje     = st.session_state.get("puntaje_final",
                    int(sum(ind_fin.values()) / max(len(ind_fin), 1)) if ind_fin else 0)
    gid         = st.session_state.get("grupo_id")

    colapso  = puntaje < 50 or any(v < 20 for v in ind_fin.values())
    resultado = "colapso" if colapso else "victoria"

    if resultado == "victoria":
        col_r, bg_r, ico, tit = "#10b981","rgba(16,185,129,0.12)","🎉","Ciudad Equilibrada - 10 Rondas!"
        sub = "El grupo administro la ciudad durante todas las rondas exitosamente."
        st.balloons()
    else:
        col_r, bg_r, ico, tit = "#ef4444","rgba(239,68,68,0.12)","💥","La Ciudad Colapso"
        criticos = [INDLABEL.get(k, k) for k, v in ind_fin.items() if v < 20]
        razon = ""
        if puntaje < 50:
            razon = " (promedio " + str(puntaje) + " < 50)"
        if criticos:
            razon += " · Criticos: " + ", ".join(criticos)
        sub = "Un indicador llego al limite critico o el promedio fue insuficiente." + razon

    nivel_lbl, nivel_color, nivel_ico, nivel_desc = _nivel(puntaje)

    # ── Banner principal ──────────────────────────────────────────────────────
    st.markdown(
        "<div style='background:"+bg_r+";border:2px solid "+col_r+"44;"
        "border-radius:20px;padding:36px;text-align:center;margin-bottom:24px'>"
        "<div style='font-size:3.5rem;margin-bottom:8px'>"+ico+"</div>"
        "<h1 style='color:"+col_r+";margin:10px 0 8px;font-size:1.8rem'>"+tit+"</h1>"
        "<p style='color:rgba(255,255,255,.5);margin-bottom:18px;font-size:.9rem'>"+sub+"</p>"
        "<div style='display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:20px'>"
        "<span style='background:rgba(52,211,153,.15);color:#34d399;border:1px solid rgba(52,211,153,.3);"
        "border-radius:20px;padding:5px 14px;font-size:.82rem;font-family:Courier Prime,monospace'>"
        "🔄 "+str(rondas_comp)+"/10 rondas</span>"
        "<span style='background:rgba(167,139,250,.12);color:#a78bfa;border:1px solid rgba(167,139,250,.25);"
        "border-radius:20px;padding:5px 14px;font-size:.82rem;font-family:Courier Prime,monospace'>"
        "🎯 "+str(puntaje)+" pts</span>"
        "</div>"
        "<div style='background:rgba(15,15,25,.6);border:2px solid "+nivel_color+"44;"
        "border-radius:16px;padding:18px 24px;margin:0 auto;max-width:420px'>"
        "<div style='font-size:.68rem;color:rgba(255,255,255,.35);text-transform:uppercase;"
        "letter-spacing:2px;font-family:Courier Prime,monospace;margin-bottom:6px'>NIVEL FINAL</div>"
        "<div style='font-size:2.2rem;margin-bottom:4px'>"+nivel_ico+"</div>"
        "<div style='font-family:Courier Prime,monospace;font-size:1.1rem;color:"+nivel_color+";"
        "font-weight:700;letter-spacing:2px;margin-bottom:6px'>"+nivel_lbl+"</div>"
        "<div style='font-size:2.2rem;font-weight:900;color:#f1f5f9;margin-bottom:4px'>"
        +str(puntaje)+"<span style='font-size:1rem;color:rgba(255,255,255,.4)'> / 100</span></div>"
        "<div style='font-size:.8rem;color:rgba(255,255,255,.4);font-family:Courier Prime,monospace'>"
        +nivel_desc+"</div></div></div>",
        unsafe_allow_html=True
    )

    # ── Indicadores finales ───────────────────────────────────────────────────
    st.markdown("### Indicadores Finales")
    f1, f2, f3, f4 = st.columns(4)
    with f1: _barra("Economia",      ind_fin.get("economia", 0),        "💰")
    with f2: _barra("Medio Ambiente", ind_fin.get("medioambiente", 0),   "🌿")
    with f3: _barra("Energia",        ind_fin.get("energia", 0),         "⚡")
    with f4: _barra("Bienestar",      ind_fin.get("bienestarsocial", 0), "❤️")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botones ───────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄  JUGAR DE NUEVO", use_container_width=True):
            if gid:
                reiniciarprogreso(gid)
            st.session_state.update(
                pregunta_actual=None, respuesta_correcta=False,
                decision_elegida=None, decision_efectos=None,
                evento_ronda=None, fase_ronda="decision",
                preguntas_usadas=[], timer_inicio=None,
                tiempo_agotado=False,
            )
            navegar("juego")
    with c2:
        if st.button("🏆  VER RANKING", use_container_width=True):
            navegar("ranking")
    with c3:
        if st.button("🏠  VOLVER AL INICIO", use_container_width=True):
            navegar("inicio")
