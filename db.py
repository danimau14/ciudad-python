import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.sqlite3")

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


def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.executescript(_SCHEMA)
    conn.commit()
    conn.close()


def get_connection():
    init_db()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def normalize_grupo_id(gid):
    """Convierte grupo_id de session_state a int o None (evita errores en la nube)."""
    if gid is None:
        return None
    if isinstance(gid, str) and not gid.strip():
        return None
    try:
        n = int(gid)
        return n if n > 0 else None
    except (TypeError, ValueError):
        return None


def fetch_all(sql, params=()):
    """Ejecuta SELECT y siempre cierra la conexion."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        conn.close()


def fetch_one(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()
    finally:
        conn.close()
