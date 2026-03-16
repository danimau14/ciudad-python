import streamlit as st
from config import IND_COLOR, IND_LABEL, TOTAL_RONDAS
from navigation import navegar


def barra_indicador(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    if valor > 60:   color,badge,glow = "#22c55e","● ESTABLE","rgba(34,197,94,0.2)"
    elif valor > 30: color,badge,glow = "#f59e0b","● PRECAUCIÓN","rgba(245,158,11,0.18)"
    else:            color,badge,glow = "#ef4444","● CRÍTICO","rgba(239,68,68,0.2)"
    bg = ("rgba(34,197,94,0.05)" if valor>60 else "rgba(245,158,11,0.05)" if valor>30 else "rgba(239,68,68,0.06)")
    st.markdown(
        "<div style='background:"+bg+";border:1px solid "+color+"44;"
        "border-radius:10px;padding:12px 16px;margin-bottom:10px;"
        "box-shadow:0 0 18px "+glow+",inset 0 1px 0 rgba(255,255,255,0.03);"
        "transition:box-shadow .3s;position:relative;overflow:hidden;'>"
        "<div style='position:absolute;top:0;left:0;width:3px;height:100%;"
        "background:"+color+";box-shadow:0 0 8px "+color+";'></div>"
        "<div style='padding-left:8px;'>"
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>"
        "<span style='font-weight:700;color:#e2e8f0;font-size:0.88rem;"
        "font-family:Exo 2,sans-serif;display:flex;align-items:center;gap:6px;'>"
        "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>"+emoji+"</span>"
        "<span>"+nombre+"</span></span>"
        "<span style='font-size:0.62rem;color:"+color+";font-weight:800;"
        "font-family:Orbitron,sans-serif;letter-spacing:1px;'>"+badge+"</span>"
        "</div>"
        "<div style='background:rgba(255,255,255,0.06);border-radius:3px;height:8px;overflow:hidden;margin-bottom:6px;'>"
        "<div style='width:"+str(valor)+"%;background:linear-gradient(90deg,"+color+"66,"+color+");"
        "height:8px;border-radius:3px;box-shadow:0 0 8px "+color+";'></div>"
        "</div>"
        "<div style='display:flex;justify-content:space-between;align-items:center;'>"
        "<span style='font-size:0.68rem;color:rgba(255,255,255,0.2);font-family:Orbitron,sans-serif;'>0</span>"
        "<span style='font-size:0.88rem;font-weight:900;color:"+color+";"
        "font-family:Orbitron,sans-serif;text-shadow:0 0 8px "+color+";'>"+str(valor)+"</span>"
        "<span style='font-size:0.68rem;color:rgba(255,255,255,0.2);font-family:Orbitron,sans-serif;'>100</span>"
        "</div>"
        "</div></div>", unsafe_allow_html=True)


def cabecera_juego(nombre_grp, estudiantes, ronda, est_turno):
    pct = int(((ronda-1)/TOTAL_RONDAS)*100)
    fase_label = st.session_state.get("fase_ronda","decision")
    fases_txt  = {"decision":"DECIDIR","pregunta":"PREGUNTA","evento":"EVENTO","resultado_pregunta":"RESULTADO"}
    fase_txt   = fases_txt.get(fase_label, fase_label.upper())

    left, mid, right = st.columns([2.5, 4, 2.5])

    with left:
        # Nombre del grupo
        st.markdown(
            "<div style='background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.25);"
            "border-radius:10px;padding:10px 14px;margin-bottom:8px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;color:rgba(0,212,255,0.5);"
            "letter-spacing:2px;margin-bottom:4px;'>SMART CITY CONTROL</div>"
            "<div style='display:flex;align-items:center;gap:8px;'>"
            "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;font-size:1.3rem;'>🏙️</span>"
            "<span style='font-family:Orbitron,sans-serif;font-weight:900;font-size:clamp(0.85rem,2vw,1.1rem);"
            "background:linear-gradient(90deg,#00d4ff,#8b5cf6);-webkit-background-clip:text;"
            "-webkit-text-fill-color:transparent;background-clip:text;'>"+nombre_grp+"</span>"
            "</div></div>", unsafe_allow_html=True)
        # Lista de estudiantes
        chips = "".join([
            "<span style='background:"+(
                "rgba(0,212,255,0.18)" if e==est_turno else "rgba(255,255,255,0.04)"
            )+";border:1px solid "+(
                "rgba(0,212,255,0.6)" if e==est_turno else "rgba(255,255,255,0.07)"
            )+";border-radius:6px;padding:3px 10px;margin:2px;font-size:0.78rem;"
            "color:"+(
                "#00d4ff" if e==est_turno else "#64748b"
            )+";display:inline-block;font-family:Exo 2,sans-serif;"
            "box-shadow:"+(
                "0 0 8px rgba(0,212,255,0.25)" if e==est_turno else "none"
            )+";'>"
            +("▶ " if e==est_turno else "")+e+"</span>"
            for e in estudiantes])
        st.markdown("<div style='line-height:1.8;'>"+chips+"</div>", unsafe_allow_html=True)

    with mid:
        # ── Contador de ronda animado ──────────────────────────────
        uid = f"ronda_{ronda}"
        segs = "".join([
            "<div style='flex:1;height:10px;border-radius:3px;margin:0 2px;"
            "background:" + ("'linear-gradient(90deg,#00d4ff,#8b5cf6)'" ) + ";" 
            if False else ""
            for _ in range(1)
        ])
        segs = ""
        for i in range(TOTAL_RONDAS):
            if i < ronda - 1:
                bg   = "linear-gradient(90deg,#00d4ff,#8b5cf6)"
                glow = "0 0 8px rgba(0,212,255,0.7)"
                h    = "10px"
            elif i == ronda - 1:
                bg   = "#00d4ff"
                glow = "0 0 14px rgba(0,212,255,1), 0 0 28px rgba(0,212,255,0.5)"
                h    = "14px"
            else:
                bg   = "rgba(255,255,255,0.07)"
                glow = "none"
                h    = "10px"
            segs += (
                f"<div style='flex:1;height:{h};border-radius:3px;margin:0 2px;"
                f"background:{bg};box-shadow:{glow};"
                f"transition:all 0.5s ease {i*0.05:.2f}s;'></div>"
            )
        num_html = (
            f"<span style='font-family:Orbitron,sans-serif;"
            f"font-size:clamp(1.4rem,3.5vw,2rem);font-weight:900;"
            f"color:#00d4ff;text-shadow:0 0 20px rgba(0,212,255,0.8);"
            f"animation:pulse_ronda 1s ease-in-out;'>{ronda}</span>"
            f"<span style='font-family:Orbitron,sans-serif;"
            f"font-size:0.9rem;color:rgba(255,255,255,0.25);margin-left:4px;'>/ {TOTAL_RONDAS}</span>"
        )
        st.markdown(
            "<style>"
            "@keyframes pulse_ronda{"
            "  0%{transform:scale(0.7);opacity:0;text-shadow:0 0 40px rgba(0,212,255,1);}"
            "  60%{transform:scale(1.15);opacity:1;}"
            "  100%{transform:scale(1);opacity:1;}}"
            "@keyframes glow_seg{"
            "  0%,100%{box-shadow:0 0 8px rgba(0,212,255,0.5);}"
            "  50%{box-shadow:0 0 18px rgba(0,212,255,1),0 0 30px rgba(139,92,246,0.6);}}"
            "</style>"
            "<div style='background:rgba(5,10,20,0.9);border:1px solid rgba(0,212,255,0.2);"
            "border-radius:12px;padding:12px 16px;text-align:center;margin-bottom:8px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:3px;margin-bottom:8px;'>RONDA ACTUAL</div>"
            f"<div style='display:flex;align-items:center;justify-content:center;"
            f"margin-bottom:10px;'>{num_html}</div>"
            f"<div style='display:flex;align-items:center;justify-content:center;"
            f"gap:0;'>{segs}</div>"
            "</div>", unsafe_allow_html=True)
        # Barra de progreso
        st.markdown(
            f"<div style='background:rgba(255,255,255,0.05);border-radius:3px;"
            f"height:4px;overflow:hidden;margin-top:4px;'>"
            f"<div style='width:{pct}%;background:linear-gradient(90deg,#00d4ff,#8b5cf6,#22c55e);"
            f"height:4px;border-radius:3px;box-shadow:0 0 10px rgba(0,212,255,0.6);"
            f"transition:width 0.8s ease;'></div></div>", unsafe_allow_html=True)

    with right:
        # Fase actual + turno + menú
        st.markdown(
            "<div style='background:rgba(5,10,20,0.9);border:1px solid rgba(139,92,246,0.3);"
            "border-radius:10px;padding:10px 14px;margin-bottom:8px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;color:rgba(139,92,246,0.7);"
            "letter-spacing:2px;margin-bottom:4px;'>FASE</div>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.95rem;font-weight:700;"
            "color:#8b5cf6;text-shadow:0 0 12px rgba(139,92,246,0.5);'>"+fase_txt+"</div>"
            "<hr style='border-color:rgba(139,92,246,0.15);margin:6px 0;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;color:rgba(0,212,255,0.5);"
            "letter-spacing:2px;margin-bottom:2px;'>OPERADOR</div>"
            "<div style='font-size:0.85rem;color:#e2e8f0;font-weight:600;'>🎓 "+est_turno+"</div>"
            "</div>", unsafe_allow_html=True)
        with st.expander("⚙️ Menú"):
            if st.button("🏠 Volver al inicio", use_container_width=True):
                navegar("inicio")

    st.markdown("<hr style='border-color:rgba(0,212,255,0.08);margin:4px 0 10px;'>",
                unsafe_allow_html=True)
# ─── PANTALLAS ───────────────────────────────────────────────────
