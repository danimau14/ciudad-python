import streamlit as st
from session_manager import navegar
from database import reiniciarprogreso
from config import INDCOLOR, INDLABEL, TOTALRONDAS


def _barra_ind(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    if valor >= 60:   color, badge, bg, borde = "#10b981","Estable",  "rgba(16,185,129,.08)","rgba(16,185,129,.3)"
    elif valor >= 30: color, badge, bg, borde = "#f59e0b","Precaución","rgba(245,158,11,.08)","rgba(245,158,11,.3)"
    else:             color, badge, bg, borde = "#ef4444","Crítico",   "rgba(239,68,68,.1)",  "rgba(239,68,68,.35)"
    st.markdown(
        "<div style='background:" + bg + ";border:1px solid " + borde + ";"
        "border-radius:14px;padding:14px 18px;margin-bottom:10px'>"
        "<div style='display:flex;justify-content:space-between;margin-bottom:8px'>"
        "<span style='font-weight:700;color:#f1f5f9;font-size:.88rem'>" + emoji + " " + nombre + "</span>"
        "<span style='font-size:.7rem;background:" + color + "22;color:" + color + ";"
        "border:1px solid " + color + "44;border-radius:20px;padding:2px 9px;"
        "font-family:Courier Prime,monospace'>" + badge + "</span>"
        "</div>"
        "<div style='background:rgba(255,255,255,.08);border-radius:6px;height:8px'>"
        "<div style='width:" + str(valor) + "%;background:" + color + ";height:8px;"
        "border-radius:6px'></div></div>"
        "<div style='text-align:right;margin-top:5px;font-size:.82rem;font-weight:700;color:" + color + "'>"
        + str(valor) + "/100</div></div>",
        unsafe_allow_html=True
    )


def _nivel_puntaje(puntaje):
    if puntaje >= 85: return "LEGENDARIO",  "#fbbf24","👑","Gestión magistral de la ciudad"
    elif puntaje >= 70: return "EXCELENTE", "#34d399","🏆","Ciudad próspera y equilibrada"
    elif puntaje >= 55: return "BUENO",     "#60a5fa","🌟","Ciudad estable con áreas de mejora"
    elif puntaje >= 40: return "REGULAR",   "#f59e0b","⚠️","Ciudad en precaución"
    else: return "CRÍTICO",                 "#ef4444","🚨","La ciudad está en crisis"


def pantallafin():
    ind_fin     = st.session_state.get("indicadores_finales", {})
    rondas_comp = st.session_state.get("rondas_completadas", 0)
    puntaje     = st.session_state.get("puntaje_final",
                    int(sum(ind_fin.values()) / max(len(ind_fin),1)) if ind_fin else 0)
    gid         = st.session_state.get("grupo_id")

    colapso  = puntaje < 50 or any(v < 20 for v in ind_fin.values())
    resultado = "colapso" if colapso else "victoria"

    if resultado == "victoria":
        col_r, bg_r, ico, tit = "#10b981","rgba(16,185,129,.12)","🎉","¡Ciudad Equilibrada — 10 Rondas!"
        sub = "El grupo administró la ciudad durante todas las rondas exitosamente."
        st.balloons()
    else:
        col_r, bg_r, ico, tit = "#ef4444","rgba(239,68,68,.12)","💥","La Ciudad Colapsó"
        razon = ""
        if puntaje < 50:
            razon = " (promedio " + str(puntaje) + " < 50)"
        criticos = [INDLABEL.get(k,k) for k,v in ind_fin.items() if v < 20]
        if criticos:
            razon += " · Críticos: " + ", ".join(criticos)
        sub = "Un indicador llegó al límite crítico o el promedio fue insuficiente." + razon

    nivel_lbl, nivel_color, nivel_ico, nivel_desc = _nivel_puntaje(puntaje)

    st.markdown(
        "<div style='background:" + bg_r + ";border:2px solid " + col_r + "44;"
        "border-radius:20px;padding:36px;text-align:center;margin-bottom:24px'>"
        "<div style='font-size:3.5rem;margin-bottom:8px'>" + ico + "</div>"
        "<h1 style='color:" + col_r + ";margin:10px 0 8px;font-size:1.8rem'>" + tit + "</h1>"
        "<p style='color:rgba(255,255,255,.5);margin-bottom:18px;font-size:.9rem'>" + sub + "</p>"
        "<div style='display:flex;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:20px'>"
        "<span style='background:rgba(52,211,153,.15);color:#34d399;border:1px solid rgba(52,211,153,.3);"
        "border-radius:20px;padding:5px 14px;font-size:.82rem;font-family:Courier Prime,monospace'>"
        "✅ " + str(st.session_state.get("correctas_ronda",0)) + " correctas</span>"
        "<span style='background:rgba(248,113,113,.12);color:#f87171;border:1px solid rgba(248,113,113,.25);"
        "border-radius:20px;padding:5px 14px;font-size:.82rem;font-family:Courier Prime,monospace'>"
        "❌ " + str(st.session_state.get("incorrectas_ronda",0)) + " incorrectas</span>"
        "<span style='background:rgba(96,165,250,.12);color:#60a5fa;border:1px solid rgba(96,165,250,.25);"
        "border-radius:20px;padding:5px 14px;font-size:.82rem;font-family:Courier Prime,monospace'>"
        "🔄 " + str(rondas_comp) + "/10 rondas</span>"
        "<span style='background:rgba(167,139,250,.12);color:#a78bfa;border:1px solid rgba(167,139,250,.25);"
        "border-radius:20px;padding:5px 14px;font-size:.82rem;font-family:Courier Prime,monospace'>"
        "🎯 " + str(puntaje) + " pts</span>"
        "</div>"

        # ── NIVEL DE PUNTUACIÓN ───────────────────────────────────────────────
        "<div style='background:rgba(15,15,25,.6);border:2px solid " + nivel_color + "44;"
        "border-radius:16px;padding:18px 24px;margin:0 auto;max-width:420px'>"
        "<div style='font-size:.68rem;color:rgba(255,255,255,.35);text-transform:uppercase;"
        "letter-spacing:2px;font-family:Courier Prime,monospace;margin-bottom:6px'>"
        "NIVEL DE PUNTUACIÓN FINAL</div>"
        "<div style='font-size:2.2rem;margin-bottom:4px'>" + nivel_ico + "</div>"
        "<div style='font-family:Courier Prime,monospace;font-size:1.1rem;color:" + nivel_color + ";"
        "font-weight:700;letter-spacing:2px;margin-bottom:6px'>" + nivel_lbl + "</div>"
        "<div style='font-size:2.2rem;font-weight:900;color:#f1f5f9;margin-bottom:4px'>"
        + str(puntaje) + "<span style='font-size:1rem;color:rgba(255,255,255,.4)'> / 100</span></div>"
        "<div style='font-size:.8rem;color:rgba(255,255,255,.4);font-family:Courier Prime,monospace'>"
        + nivel_desc + "</div>"
        "<div style='margin-top:8px;font-size:.78rem;color:rgba(255,255,255,.3);"
        "font-family:Courier Prime,monospace'>"
        "Colapsa si promedio &lt; 50 o algún indicador &lt; 20</div>"
        "</div></div>",
        unsafe_allow_html=True
    )

    st.markdown("### 📊 Indicadores Finales")
    f1, f2, f3, f4 = st.columns(4)
    with f1: _barra_ind("Economía",       ind_fin.get("economia",0),        "💰")
    with f2: _barra_ind("Medio Ambiente",  ind_fin.get("medioambiente",0),   "🌿")
    with f3: _barra_ind("Energía",         ind_fin.get("energia",0),         "⚡")
    with f4: _barra_ind("Bienestar Social",ind_fin.get("bienestarsocial",0), "❤️")

    st.markdown(
        "<div style='text-align:center;margin:16px 0'>"
        "<span style='color:#fbbf24;font-weight:700;font-size:1.1rem'>⭐ Puntaje final registrado: "
        + str(puntaje) + " pts</span></div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
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
                tiempo_agotado=False, correctas_ronda=0, incorrectas_ronda=0,
            )
            navegar("juego")
    with c2:
        if st.button("🏆  VER RANKING", use_container_width=True):
            navegar("ranking")
    with c3:
        if st.button("🏙️  VOLVER AL LOBBY", use_container_width=True):
            navegar("lobby")
