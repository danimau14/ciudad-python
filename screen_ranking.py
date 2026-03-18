import streamlit as st


def pantalla_ranking():
    from database import (obtenerprogreso, obtenerestudiantes,
                          nombregrupoporid)
    from session_manager import navegar

    gid = st.session_state.get("grupo_id")
    if not gid:
        navegar("inicio")
        return

    nombre_grp  = nombregrupoporid(gid)
    estudiantes = obtenerestudiantes(gid)
    progreso    = obtenerprogreso(gid)

    eco  = progreso.get("economia", 50)
    amb  = progreso.get("medioambiente", 50)
    ene  = progreso.get("energia", 50)
    bie  = progreso.get("bienestarsocial", 50)
    ronda = progreso.get("ronda_actual", 1)
    puntaje = int((eco + amb + ene + bie) / 4)

    def _nivel(p):
        if p >= 85:   return "LEGENDARIO", "#fbbf24", "👑"
        elif p >= 70: return "EXCELENTE",  "#34d399", "🏆"
        elif p >= 55: return "BUENO",      "#60a5fa", "🌟"
        elif p >= 40: return "REGULAR",    "#f59e0b", "⚠️"
        else:         return "CRITICO",    "#ef4444", "🚨"

    nivel_lbl, nivel_color, nivel_ico = _nivel(puntaje)

    # ── Cabecera ──────────────────────────────────────────────────────────────
    st.markdown(
        "<h1 style='background:linear-gradient(90deg,#fbbf24,#f59e0b);"
        "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "font-size:2rem;margin-bottom:4px'>🏆 Ranking del Grupo</h1>",
        unsafe_allow_html=True
    )

    # ── Tarjeta de puntaje ────────────────────────────────────────────────────
    st.markdown(
        f"<div style='background:rgba(251,191,36,0.08);border:2px solid rgba(251,191,36,0.3);"
        f"border-radius:20px;padding:28px;text-align:center;margin-bottom:20px'>"
        f"<div style='font-size:3rem'>{nivel_ico}</div>"
        f"<div style='font-family:Courier Prime,monospace;color:{nivel_color};"
        f"font-size:1.1rem;font-weight:700;letter-spacing:2px;margin:8px 0'>{nivel_lbl}</div>"
        f"<div style='font-size:3rem;font-weight:900;color:#f1f5f9'>{puntaje}"
        f"<span style='font-size:1.2rem;color:rgba(255,255,255,0.4)'> / 100</span></div>"
        f"<div style='color:rgba(255,255,255,0.4);font-size:.85rem;margin-top:6px'>"
        f"Grupo: <b style='color:#e2e8f0'>{nombre_grp}</b> · "
        f"Ronda <b style='color:#e2e8f0'>{min(ronda-1,10)}/10</b> completadas</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # ── Indicadores con barras ────────────────────────────────────────────────
    st.markdown("### 📊 Detalle de Indicadores")
    indicadores = [
        ("💰 Economía",       eco,  "#fbbf24"),
        ("🌿 Medio Ambiente",  amb,  "#34d399"),
        ("⚡ Energía",          ene,  "#60a5fa"),
        ("❤️ Bienestar Social", bie,  "#f472b6"),
    ]
    c1, c2 = st.columns(2)
    for i, (nombre, valor, color) in enumerate(indicadores):
        valor = max(0, min(100, valor))
        badge = "Estable" if valor >= 60 else "Precaución" if valor >= 30 else "Crítico"
        col = c1 if i % 2 == 0 else c2
        with col:
            st.markdown(
                f"<div style='background:rgba(255,255,255,0.04);border:1px solid {color}33;"
                f"border-radius:14px;padding:14px 18px;margin-bottom:10px'>"
                f"<div style='display:flex;justify-content:space-between;margin-bottom:8px'>"
                f"<span style='font-weight:700;color:#f1f5f9;font-size:.9rem'>{nombre}</span>"
                f"<span style='color:{color};font-size:.75rem;border:1px solid {color}44;"
                f"border-radius:20px;padding:2px 10px'>{badge}</span></div>"
                f"<div style='background:rgba(255,255,255,0.08);border-radius:6px;height:10px'>"
                f"<div style='width:{valor}%;background:{color};height:10px;border-radius:6px'></div></div>"
                f"<div style='text-align:right;margin-top:5px;color:{color};"
                f"font-weight:700;font-size:.9rem'>{valor}/100</div></div>",
                unsafe_allow_html=True
            )

    # ── Estudiantes ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 👥 Integrantes del Equipo")
    ronda_actual = progreso.get("ronda_actual", 1)
    cols = st.columns(len(estudiantes)) if estudiantes else []
    for i, (col, est) in enumerate(zip(cols, estudiantes)):
        turno = (ronda_actual - 1) % len(estudiantes)
        es_turno = (i == turno)
        with col:
            st.markdown(
                f"<div style='background:{'rgba(167,139,250,0.15)' if es_turno else 'rgba(255,255,255,0.04)'};"
                f"border:1px solid {'rgba(167,139,250,0.5)' if es_turno else 'rgba(255,255,255,0.08)'};"
                f"border-radius:12px;padding:14px;text-align:center'>"
                f"<div style='font-size:1.6rem'>{'✏️' if es_turno else '👤'}</div>"
                f"<div style='color:{'#c4b5fd' if es_turno else '#94a3b8'};"
                f"font-weight:{'700' if es_turno else '400'};font-size:.85rem;margin-top:6px'>{est}</div>"
                f"{'<div style=\"color:#a78bfa;font-size:.7rem;margin-top:4px\">Turno actual</div>' if es_turno else ''}"
                f"</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botones ───────────────────────────────────────────────────────────────
    b1, b2 = st.columns(2)
    with b1:
        if st.button("▶️  VOLVER AL JUEGO", use_container_width=True, type="primary"):
            navegar("juego")
    with b2:
        if st.button("🏠  VOLVER AL INICIO", use_container_width=True):
            navegar("inicio")
