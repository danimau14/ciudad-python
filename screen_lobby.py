import streamlit as st
from session_manager import navegar
from database import obtener_estrellas, obtener_logros_grupo
from config import LOGROS, LOGROS_LOBBY, DIFICULTADES, ATRIBUTOS
from ui_styles import inyectar_css, pixel_header, pixel_divider, stat_badge


DIF_INFO = {
    "Fácil":   {"color":"#10b981","dot":"🟢","pen":"x1","ev":"Suaves",   "stars":"+1"},
    "Normal":  {"color":"#f59e0b","dot":"🟡","pen":"x1.5","ev":"Estándar","stars":"+2"},
    "Difícil": {"color":"#ef4444","dot":"🔴","pen":"x2",  "ev":"Intensos","stars":"+4"},
}


def pantalla_lobby():
    inyectar_css()

    grupo_nombre = st.session_state.get("grupo_nombre","Ciudad")
    gid          = st.session_state.get("grupo_id")
    estrellas    = obtener_estrellas(gid) if gid else 0

    # ── Cabecera ─────────────────────────────────────────────────────────────
    pixel_header("CIUDAD EN EQUILIBRIO", "pensamiento sistémico · trivia urbana", "🏙️")

    st.markdown(f"""
    <div style="text-align:center;margin-bottom:24px">
        <div style="display:inline-flex;align-items:center;gap:10px;
            background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.25);
            border-radius:30px;padding:8px 20px">
            <span style="font-size:1.1rem">⭐</span>
            <span style="font-family:Courier Prime,monospace;font-weight:700;
                color:#fbbf24;font-size:.9rem">{estrellas}</span>
            <span style="font-family:Courier Prime,monospace;font-size:.75rem;
                color:rgba(251,191,36,.6);text-transform:uppercase;letter-spacing:1px">
                estrellas acumuladas</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Selector de dificultad ────────────────────────────────────────────────
    st.markdown("""
    <div style="font-family:Courier Prime,monospace;font-size:.7rem;font-weight:700;
        text-transform:uppercase;letter-spacing:2px;color:rgba(167,139,250,.7);
        margin-bottom:12px">
        &#9635; SELECCIONA LA DIFICULTAD
    </div>""", unsafe_allow_html=True)

    dif_actual = st.session_state.get("dificultad","Fácil")
    c1, c2, c3 = st.columns(3)

    for col, nombre in zip([c1,c2,c3], ["Fácil","Normal","Difícil"]):
        info     = DIF_INFO[nombre]
        selected = dif_actual == nombre
        bg       = f"rgba(15,15,25,.9);border-color:{info['color']}66" if selected else "rgba(15,15,25,.5)"
        sombra   = f"0 0 22px {info['color']}22" if selected else "none"
        check    = f"<div style='font-size:.65rem;color:{info['color']};text-transform:uppercase;"                    f"letter-spacing:1px;margin-top:8px;font-family:Courier Prime,monospace'>"                    f"✓ SELECCIONADO</div>" if selected else ""

        with col:
            st.markdown(f"""
            <div style="background:{bg};border:2px solid {'rgba(167,139,250,.15)' if not selected else info['color']+'66'};
                border-radius:16px;padding:20px 14px;text-align:center;
                box-shadow:{sombra};transition:all .25s;margin-bottom:10px">
                <div style="font-size:2rem;margin-bottom:8px">{info['dot']}</div>
                <div style="font-family:Press Start 2P,monospace;font-size:.85rem;
                    color:{'#f1f5f9' if selected else '#94a3b8'};margin-bottom:10px">
                    {nombre}</div>
                <div style="font-family:Courier Prime,monospace;font-size:.7rem;
                    color:rgba(255,255,255,.35);line-height:1.8">
                    Penalización {info['pen']}<br>
                    Eventos {info['ev']}<br>
                    <span style="color:{info['color']}99">{info['stars']} &#9733; por victoria</span>
                </div>
                {check}
            </div>""", unsafe_allow_html=True)

            if st.button(
                f"{'✓ ' if selected else ''}Elegir {nombre}",
                key=f"btn_dif_{nombre}",
                use_container_width=True,
                disabled=selected
            ):
                st.session_state["dificultad"] = nombre
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botón Nueva Partida ───────────────────────────────────────────────────
    if st.button("🚀  NUEVA PARTIDA", use_container_width=True, type="primary"):
        navegar("juego")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Navegación ────────────────────────────────────────────────────────────
    n1, n2, n3, n4 = st.columns(4)
    with n1:
        if st.button("🏆  Ranking",      use_container_width=True): navegar("ranking")
    with n2:
        if st.button("📋  Misiones",     use_container_width=True): navegar("misiones")
    with n3:
        if st.button("🏅  Logros",       use_container_width=True): navegar("logros")
    with n4:
        if st.button("📖  Instrucciones",use_container_width=True): navegar("instrucciones")

    pixel_divider("#a78bfa", "LOGROS DESTACADOS")

    # ── Logros destacados — SOLO HTML, sin st.expander ───────────────────────
    logros_map  = {l["id"]: l for l in LOGROS}
    logros_ids  = set(obtener_logros_grupo(gid)) if gid else set()
    cols_logros = st.columns(4)

    for i, lid in enumerate(LOGROS_LOBBY):
        logro    = logros_map.get(lid)
        if not logro:
            continue
        obtenido = lid in logros_ids
        emoji    = logro["emoji"] if obtenido else "&#10067;"
        nombre   = logro["nombre"] if obtenido else "???"
        stars    = logro.get("estrellas", 0)
        color    = "#a78bfa" if obtenido else "rgba(255,255,255,.15)"
        bg       = "rgba(124,58,237,.08)" if obtenido else "rgba(15,15,25,.4)"
        borde    = "rgba(124,58,237,.3)"  if obtenido else "rgba(255,255,255,.06)"
        stars_h  = f"<div style='color:#fbbf24;font-size:.65rem;margin-top:4px'>{'⭐'*min(stars,5)}</div>" if obtenido and stars else ""

        with cols_logros[i % 4]:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {borde};border-radius:14px;
                padding:14px 8px;text-align:center;min-height:110px;margin-bottom:10px">
                <div style="font-size:1.5rem;margin-bottom:5px;
                    filter:{'none' if obtenido else 'grayscale(1) opacity(.2)'}">
                    {emoji}</div>
                <div style="font-size:.65rem;font-weight:700;color:{color};
                    font-family:Courier Prime,monospace;line-height:1.3">
                    {nombre}</div>
                {stars_h}
            </div>""", unsafe_allow_html=True)

    # ── Tienda de Atributos — sin st.expander ────────────────────────────────
    pixel_divider("#60a5fa", "TIENDA DE ATRIBUTOS")

    if estrellas > 0:
        a_cols = st.columns(4)
        for i, (clave, atr) in enumerate(ATRIBUTOS.items()):
            puede = estrellas >= atr["costo"]
            bg    = "rgba(96,165,250,.07)" if puede else "rgba(15,15,25,.4)"
            borde = "rgba(96,165,250,.3)"  if puede else "rgba(255,255,255,.06)"
            color = "#93c5fd" if puede else "rgba(255,255,255,.2)"
            with a_cols[i % 4]:
                st.markdown(f"""
                <div style="background:{bg};border:1px solid {borde};border-radius:14px;
                    padding:14px 10px;text-align:center;margin-bottom:10px">
                    <div style="font-size:1.4rem;margin-bottom:6px">{atr['emoji']}</div>
                    <div style="font-size:.68rem;font-weight:700;color:{color};
                        font-family:Courier Prime,monospace;margin-bottom:4px">
                        {atr['nombre']}</div>
                    <div style="font-size:.6rem;color:rgba(255,255,255,.25);
                        font-family:Courier Prime,monospace;line-height:1.4;margin-bottom:8px">
                        {atr['desc']}</div>
                    <div style="font-size:.72rem;color:#fbbf24;font-weight:700;
                        font-family:Courier Prime,monospace">
                        ⭐ {atr['costo']}</div>
                </div>""", unsafe_allow_html=True)
                if puede:
                    if st.button(f"Comprar", key=f"buy_{clave}", use_container_width=True):
                        if "atributos_activos" not in st.session_state:
                            st.session_state["atributos_activos"] = []
                        st.session_state["atributos_activos"].append(clave)
                        st.success(f"¡{atr['nombre']} activado para la próxima ronda!")
    else:
        st.markdown("""
        <div style="text-align:center;padding:18px;
            font-family:Courier Prime,monospace;font-size:.78rem;
            color:rgba(255,255,255,.25);border:1px solid rgba(255,255,255,.06);
            border-radius:14px">
            &#9971; Gana estrellas completando partidas para desbloquear atributos
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Cerrar sesión ─────────────────────────────────────────────────────────
    if st.button("🚪  CERRAR SESIÓN", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        navegar("login")
