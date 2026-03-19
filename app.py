import streamlit as st
import sqlite3
import os
from ui_styles import inyectar_css
from session_manager import init_session
from router import router

# ── Ruta absoluta del archivo database.db ─────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")

# ── Esquema completo de la base de datos ──────────────────────────────────────
_SCHEMA = """
CREATE TABLE IF NOT EXISTS grupos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombregrupo TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS estudiantes (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid          INTEGER NOT NULL,
    nombreestudiante TEXT NOT NULL,
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
CREATE TABLE IF NOT EXISTS progresojuego (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid         INTEGER NOT NULL,
    dificultad      TEXT NOT NULL DEFAULT 'Normal',
    economia        INTEGER DEFAULT 50,
    medioambiente   INTEGER DEFAULT 50,
    energia         INTEGER DEFAULT 50,
    bienestarsocial INTEGER DEFAULT 50,
    rondaactual     INTEGER DEFAULT 1,
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
CREATE TABLE IF NOT EXISTS cooldowndecisiones (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid         INTEGER NOT NULL,
    dificultad      TEXT NOT NULL DEFAULT 'Normal',
    decision        TEXT NOT NULL,
    rondasrestantes INTEGER NOT NULL,
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
CREATE TABLE IF NOT EXISTS logros_grupo (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid INTEGER NOT NULL,
    logroid TEXT NOT NULL,
    UNIQUE(grupoid, logroid),
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
CREATE TABLE IF NOT EXISTS misiones_canjeadas (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid  INTEGER NOT NULL,
    misionid TEXT NOT NULL,
    UNIQUE(grupoid, misionid),
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
CREATE TABLE IF NOT EXISTS misiones_pendientes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid    INTEGER NOT NULL,
    misionid   TEXT NOT NULL,
    recompensa INTEGER NOT NULL DEFAULT 0,
    UNIQUE(grupoid, misionid),
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
CREATE TABLE IF NOT EXISTS estrellas_grupo (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid INTEGER UNIQUE NOT NULL,
    total   INTEGER DEFAULT 0,
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
CREATE TABLE IF NOT EXISTS ranking (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    grupoid     INTEGER NOT NULL,
    nombregrupo TEXT NOT NULL,
    puntaje     INTEGER NOT NULL,
    dificultad  TEXT DEFAULT 'Normal',
    fecha       TEXT DEFAULT (date('now')),
    FOREIGN KEY(grupoid) REFERENCES grupos(id)
);
"""

def _init_db():
    """Crea database.db y todas las tablas si no existen."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.executescript(_SCHEMA)
    conn.commit()
    conn.close()


st.set_page_config(
    page_title="Ciudad en Equilibrio",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    _init_db()          # genera database.db automáticamente
    init_session()
    inyectar_css()
    router()


if __name__ == "__main__":
    main()
