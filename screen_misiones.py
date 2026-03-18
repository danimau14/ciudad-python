import streamlit as st
from session_manager import navegar
from database import obtener_misiones_canjeadas, obtener_estrellas
from config import MISIONES
from ui_styles import pixel_header, pixel_divider, stat_badge


DIF_COLOR = {"Fácil":"#10b981","Normal":"#f59e0b","Difícil":"#ef4444","todas":"#a78bfa"}
DIF_LABEL = {"Fácil":"🟢 FÁCIL","Normal":"🟡 NORMAL","Difícil":"🔴 DIFÍCIL","todas":"🌐 TODAS"}


def pantalla_misiones():
    gid        = st.session_state.get("grupo_id")
    canjeadas  = set(obtener_misiones_canjeadas(gid)) if gid else set()
    estrellas  = obtener_estrellas(gid) if gid else 0
    completadas = len(canjeadas)
    total       = len(MISIONES)
    pct         = int(completadas / total * 100)

    pixel_header("MISIONES", f"{completadas}/{total} completadas · ⭐ {estrellas} estrellas", "📋")

    # Barra progreso
    st.markdown(f'''<div style="background:rgba(255,255,255,.05);border-radius:8px;
        height:10px;margin-bottom:4px;overflow:hidden">
        <div style="width:{pct}%;height:10px;border-radius:8px;
            background:linear-gradient(90deg,#7c3aed,#34d399);
            transition:width .6s ease"></div>
    </div>
    <div style="text-align:right;font-size:.68rem;color:rgba(255,255,255,.25);
        font-family:Courier Prime,monospace;margin-bottom:18px">
        {completadas}/{total} · {pct}%</div>''', unsafe_allow_html=True)

    # Stats rápidas
    total_recompensas = sum(m["recompensa"] for m in MISIONES if m["id"] in canjeadas)
    stats_html = (
        stat_badge("Canjeadas",   completadas,       "#34d399", "✅") +
        stat_badge("Pendientes",  total-completadas, "#64748b", "⏳") +
        stat_badge("Ganadas ⭐",  total_recompensas, "#fbbf24", "⭐")
    )
    st.markdown(f'<div style="text-align:center;margin-bottom:22px">{stats_html}</div>',
                unsafe_allow_html=True)

    pixel_divider("#a78bfa", "LISTA DE MISIONES")

    for m in MISIONES:
        canjeada  = m["id"] in canjeadas
        dif_color = DIF_COLOR.get(m.get("dif","todas"), "#a78bfa")
        dif_label = DIF_LABEL.get(m.get("dif","todas"), "🌐 TODAS")
        bg    = "rgba(52,211,153,.06)"  if canjeada else "rgba(15,15,25,.6)"
        borde = "rgba(52,211,153,.3)"   if canjeada else "rgba(167,139,250,.12)"
        ico   = "✅" if canjeada else f'<span style="color:#fbbf24;font-weight:700;font-size:.9rem">+{m["recompensa"]} ⭐</span>'

        dif_badge = (
            f'<span style="font-size:.62rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:1px;color:{dif_color};background:{dif_color}18;'
            f'border:1px solid {dif_color}44;border-radius:20px;padding:2px 9px;'
            f'font-family:Courier Prime,monospace">{dif_label}</span>'
        ) if m.get("dif") and m["dif"] != "todas" else ""

        estado_badge = (
            '<span style="font-size:.62rem;font-weight:700;text-transform:uppercase;'
            'color:#34d399;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.3);'
            'border-radius:20px;padding:2px 9px;letter-spacing:1px;'
            'font-family:Courier Prime,monospace">COMPLETADA</span>'
        ) if canjeada else ""

        c1, c2 = st.columns([5, 1])
        with c1:
            st.markdown(f'''<div class="anim-fade" style="background:{bg};border:1px solid {borde};
                border-radius:14px;padding:14px 18px;margin-bottom:8px;
                transition:border-color .2s,box-shadow .2s">
                <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px">
                    <span style="font-weight:700;color:#f1f5f9;
                        font-family:Courier Prime,monospace;font-size:.9rem">{m["nombre"]}</span>
                    {dif_badge}
                    {estado_badge}
                </div>
                <div style="font-size:.78rem;color:rgba(255,255,255,.4);
                    font-family:Courier Prime,monospace;line-height:1.5">{m["desc"]}</div>
            </div>''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div style="display:flex;align-items:center;justify-content:center;'
                        f'height:70px;font-family:Courier Prime,monospace">{ico}</div>',
                        unsafe_allow_html=True)

    # Aviso de canje
    st.markdown('''<div class="anim-fade" style="background:rgba(96,165,250,.07);
        border:1px solid rgba(96,165,250,.2);border-radius:14px;
        padding:14px 18px;margin-top:18px;margin-bottom:6px;
        font-family:Courier Prime,monospace;font-size:.8rem;
        color:rgba(255,255,255,.5);line-height:1.6">
        💡 Las misiones completadas se <b style="color:#60a5fa">canjean automáticamente</b>
        al finalizar una partida desde la pantalla de resultados.
    </div>''', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅  VOLVER AL LOBBY", use_container_width=True):
        navegar("lobby")
