import streamlit as st


def navegar(pantalla):
    st.session_state["pantalla"] = pantalla
    st.rerun()
