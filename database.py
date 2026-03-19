"""
database.py — Intermediario entre la app y database.db (SQLite)

Toda la información de la aplicación se almacena en database.db:
  grupos              → nombre y contraseña de grupos
  estudiantes         → miembros de cada grupo
  progresojuego       → indicadores y ronda actual por grupo/dificultad
  cooldowndecisiones  → decisiones en cooldown por grupo/dificultad
  logros_grupo        → logros desbloqueados por grupo
  misiones_canjeadas  → misiones ya canjeadas (estrellas cobradas)
  misiones_pendientes → misiones completadas pero aún no canjeadas
  estrellas_grupo     → total de estrellas acumuladas por grupo
  ranking             → historial de partidas terminadas
"""

import sqlite3
import hashlib
import os

_DIR    = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_DIR, "database.db")
COOLDOWN = 3

# ── Definición de tablas ──────────────────────────────────────────────────────
_TABLAS = [
    """CREATE TABLE IF NOT EXISTS grupos (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nombregrupo TEXT UNIQUE NOT NULL,
        password    TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS estudiantes (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid          INTEGER NOT NULL,
        nombreestudiante TEXT NOT NULL,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS progresojuego (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid        INTEGER NOT NULL,
        dificultad     TEXT NOT NULL DEFAULT 'Normal',
        economia       INTEGER DEFAULT 50,
        medioambiente  INTEGER DEFAULT 50,
        energia        INTEGER DEFAULT 50,
        bienestarsocial INTEGER DEFAULT 50,
        rondaactual    INTEGER DEFAULT 1,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS cooldowndecisiones (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid        INTEGER NOT NULL,
        dificultad     TEXT NOT NULL DEFAULT 'Normal',
        decision       TEXT NOT NULL,
        rondasrestantes INTEGER NOT NULL,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS logros_grupo (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        logroid TEXT NOT NULL,
        UNIQUE(grupoid, logroid),
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS misiones_canjeadas (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid  INTEGER NOT NULL,
        misionid TEXT NOT NULL,
        UNIQUE(grupoid, misionid),
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS misiones_pendientes (
        id        INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid   INTEGER NOT NULL,
        misionid  TEXT NOT NULL,
        recompensa INTEGER NOT NULL DEFAULT 0,
        UNIQUE(grupoid, misionid),
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS estrellas_grupo (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER UNIQUE NOT NULL,
        total   INTEGER DEFAULT 0,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS ranking (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid     INTEGER NOT NULL,
        nombregrupo TEXT NOT NULL,
        puntaje     INTEGER NOT NULL,
        dificultad  TEXT DEFAULT 'Normal',
        fecha       TEXT,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
]

# ── Migraciones (columnas añadidas en versiones posteriores) ──────────────────
_MIGRACIONES = [
    ("progresojuego",     "dificultad",
     "ALTER TABLE progresojuego ADD COLUMN dificultad TEXT NOT NULL DEFAULT 'Normal'"),
    ("cooldowndecisiones","dificultad",
     "ALTER TABLE cooldowndecisiones ADD COLUMN dificultad TEXT NOT NULL DEFAULT 'Normal'"),
    ("ranking",           "dificultad",
     "ALTER TABLE ranking ADD COLUMN dificultad TEXT DEFAULT 'Normal'"),
    ("ranking",           "fecha",
     "ALTER TABLE ranking ADD COLUMN fecha TEXT"),
]


# ══════════════════════════════════════════════════════════════════════════════
#  CONEXIÓN
# ══════════════════════════════════════════════════════════════════════════════

def _migrar(conn):
    cur = conn.cursor()
    for tabla, col, sql in _MIGRACIONES:
        try:
            cur.execute(f"SELECT {col} FROM {tabla} LIMIT 1")
        except sqlite3.OperationalError:
            try:
                cur.execute(sql)
            except Exception:
                pass
    # Asegurar tabla misiones_pendientes (puede no existir en BDs antiguas)
    try:
        cur.execute("SELECT id FROM misiones_pendientes LIMIT 1")
    except sqlite3.OperationalError:
        cur.execute("""CREATE TABLE IF NOT EXISTS misiones_pendientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupoid INTEGER NOT NULL,
            misionid TEXT NOT NULL,
            recompensa INTEGER NOT NULL DEFAULT 0,
            UNIQUE(grupoid, misionid),
            FOREIGN KEY(grupoid) REFERENCES grupos(id)
        )""")
    conn.commit()


def _crear_tablas():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    for sql in _TABLAS:
        conn.execute(sql)
    conn.commit()
    _migrar(conn)
    conn.close()


def getconn():
    """Retorna una conexión abierta a database.db, creando tablas si no existen."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='grupos'")
    if cur.fetchone() is None:
        conn.close()
        _crear_tablas()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
    else:
        _migrar(conn)
    return conn


def inicializardb():
    """Inicializa database.db al arrancar la app."""
    conn = getconn()
    conn.close()

inicializar_db = inicializardb


def hp(pw):
    """Hash SHA-256 de la contraseña."""
    return hashlib.sha256(pw.encode()).hexdigest()


# ══════════════════════════════════════════════════════════════════════════════
#  GRUPOS
# ══════════════════════════════════════════════════════════════════════════════

def registrargrupo(nombre, pw):
    conn = getconn(); c = conn.cursor()
    try:
        c.execute("INSERT INTO grupos(nombregrupo,password) VALUES(?,?)",
                  (nombre.strip(), hp(pw)))
        conn.commit(); gid = c.lastrowid; conn.close()
        return True, gid
    except sqlite3.IntegrityError:
        conn.close(); return False, None

registrar_grupo = registrargrupo


def logingrupo(nombre, pw):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT id FROM grupos WHERE nombregrupo=? AND password=?",
              (nombre.strip(), hp(pw)))
    row = c.fetchone(); conn.close()
    return row["id"] if row else None

login_grupo = logingrupo


def nombregrupoporid(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT nombregrupo FROM grupos WHERE id=?", (gid,))
    row = c.fetchone(); conn.close()
    return row["nombregrupo"] if row else "Desconocido"

nombre_grupo_por_id = nombregrupoporid


# ══════════════════════════════════════════════════════════════════════════════
#  ESTUDIANTES
# ══════════════════════════════════════════════════════════════════════════════

def guardarestudiante(gid, nombre):
    conn = getconn(); c = conn.cursor()
    c.execute("INSERT INTO estudiantes(grupoid,nombreestudiante) VALUES(?,?)",
              (gid, nombre.strip()))
    conn.commit(); conn.close()

guardar_estudiante = guardarestudiante


def obtenerestudiantes(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT nombreestudiante FROM estudiantes WHERE grupoid=? ORDER BY id", (gid,))
    rows = c.fetchall(); conn.close()
    return [r["nombreestudiante"] for r in rows]

obtener_estudiantes = obtenerestudiantes


# ══════════════════════════════════════════════════════════════════════════════
#  PROGRESO DEL JUEGO
# ══════════════════════════════════════════════════════════════════════════════

def obtenerprogreso(gid, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()

    def _buscar():
        c.execute(
            "SELECT * FROM progresojuego WHERE grupoid=? AND dificultad=? ORDER BY id LIMIT 1",
            (gid, dificultad))
        return c.fetchone()

    row = _buscar()
    if row is None:
        try:
            c.execute(
                """INSERT INTO progresojuego
                   (grupoid,dificultad,economia,medioambiente,energia,bienestarsocial,rondaactual)
                   VALUES (?,?,50,50,50,50,1)""",
                (gid, dificultad))
            conn.commit()
        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            conn.rollback()
        row = _buscar()

    conn.close()
    if row is None:
        return {"grupoid": gid, "dificultad": dificultad,
                "economia": 50, "medioambiente": 50,
                "energia": 50, "bienestarsocial": 50, "rondaactual": 1}
    return dict(row)

obtener_progreso = obtenerprogreso


def actualizarprogreso(gid, eco, amb, ene, bie, ronda, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    n = c.execute(
        "UPDATE progresojuego SET economia=?,medioambiente=?,energia=?,bienestarsocial=?,"
        "rondaactual=? WHERE grupoid=? AND dificultad=?",
        (eco, amb, ene, bie, ronda, gid, dificultad)).rowcount
    if n == 0:
        try:
            c.execute(
                """INSERT INTO progresojuego
                   (grupoid,dificultad,economia,medioambiente,energia,bienestarsocial,rondaactual)
                   VALUES(?,?,?,?,?,?,?)""",
                (gid, dificultad, eco, amb, ene, bie, ronda))
        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            pass
    conn.commit(); conn.close()

actualizar_progreso = actualizarprogreso


def reiniciarprogreso(gid, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    c.execute("""UPDATE progresojuego
        SET economia=50,medioambiente=50,energia=50,bienestarsocial=50,rondaactual=1
        WHERE grupoid=? AND dificultad=?""", (gid, dificultad))
    c.execute("DELETE FROM cooldowndecisiones WHERE grupoid=? AND dificultad=?",
              (gid, dificultad))
    conn.commit(); conn.close()

reiniciar_progreso = reiniciarprogreso


# ══════════════════════════════════════════════════════════════════════════════
#  COOLDOWN DE DECISIONES
# ══════════════════════════════════════════════════════════════════════════════

def obtenercooldowns(gid, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    c.execute(
        "SELECT decision,rondasrestantes FROM cooldowndecisiones "
        "WHERE grupoid=? AND dificultad=?", (gid, dificultad))
    rows = c.fetchall(); conn.close()
    return {r["decision"]: r["rondasrestantes"] for r in rows}

obtener_cooldowns = obtenercooldowns


def actualizarcooldown(gid, decision, rondausada, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    c.execute("DELETE FROM cooldowndecisiones WHERE grupoid=? AND decision=? AND dificultad=?",
              (gid, decision, dificultad))
    c.execute(
        "INSERT INTO cooldowndecisiones(grupoid,dificultad,decision,rondasrestantes) VALUES(?,?,?,?)",
        (gid, dificultad, decision, rondausada + COOLDOWN))
    conn.commit(); conn.close()

actualizar_cooldown = actualizarcooldown


# ══════════════════════════════════════════════════════════════════════════════
#  LOGROS
# ══════════════════════════════════════════════════════════════════════════════

def obtener_logros_grupo(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT logroid FROM logros_grupo WHERE grupoid=?", (gid,))
    rows = c.fetchall(); conn.close()
    return [r["logroid"] for r in rows]


def guardar_logro(gid, logro_id):
    conn = getconn()
    conn.execute("INSERT OR IGNORE INTO logros_grupo(grupoid,logroid) VALUES(?,?)",
                 (gid, logro_id))
    conn.commit(); conn.close()


# ══════════════════════════════════════════════════════════════════════════════
#  MISIONES — canjeadas y pendientes (en database.db)
# ══════════════════════════════════════════════════════════════════════════════

def obtener_misiones_canjeadas(gid):
    """IDs de misiones ya canjeadas (estrellas cobradas)."""
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT misionid FROM misiones_canjeadas WHERE grupoid=?", (gid,))
    rows = c.fetchall(); conn.close()
    return [r["misionid"] for r in rows]


def guardar_mision(gid, mision_id):
    """Marca una misión como canjeada en database.db."""
    conn = getconn()
    conn.execute("INSERT OR IGNORE INTO misiones_canjeadas(grupoid,misionid) VALUES(?,?)",
                 (gid, mision_id))
    # Eliminar de pendientes si estaba ahí
    conn.execute("DELETE FROM misiones_pendientes WHERE grupoid=? AND misionid=?",
                 (gid, mision_id))
    conn.commit(); conn.close()


def obtener_misiones_pendientes(gid):
    """Misiones completadas pero aún no canjeadas (guardadas en database.db)."""
    conn = getconn(); c = conn.cursor()
    c.execute(
        "SELECT misionid, recompensa FROM misiones_pendientes WHERE grupoid=? ORDER BY id",
        (gid,))
    rows = c.fetchall(); conn.close()
    return [{"id": r["misionid"], "recompensa": r["recompensa"]} for r in rows]


def guardar_mision_pendiente(gid, mision_id, recompensa):
    """Guarda una misión como pendiente de canjear en database.db."""
    conn = getconn()
    conn.execute(
        "INSERT OR IGNORE INTO misiones_pendientes(grupoid,misionid,recompensa) VALUES(?,?,?)",
        (gid, mision_id, recompensa))
    conn.commit(); conn.close()


def eliminar_mision_pendiente(gid, mision_id):
    """Elimina una misión de pendientes (cuando se canjea)."""
    conn = getconn()
    conn.execute("DELETE FROM misiones_pendientes WHERE grupoid=? AND misionid=?",
                 (gid, mision_id))
    conn.commit(); conn.close()


def limpiar_misiones_pendientes(gid):
    """Limpia todas las misiones pendientes de un grupo."""
    conn = getconn()
    conn.execute("DELETE FROM misiones_pendientes WHERE grupoid=?", (gid,))
    conn.commit(); conn.close()


# ══════════════════════════════════════════════════════════════════════════════
#  ESTRELLAS  (acumuladas en database.db)
# ══════════════════════════════════════════════════════════════════════════════

def obtener_estrellas(gid):
    """Retorna el total de estrellas acumuladas del grupo desde database.db."""
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT total FROM estrellas_grupo WHERE grupoid=?", (gid,))
    row = c.fetchone(); conn.close()
    return row["total"] if row else 0


def guardar_estrellas(gid, cantidad):
    """
    Suma (o resta si negativo) estrellas al total del grupo en database.db.
    El total nunca baja de 0.
    """
    conn = getconn(); c = conn.cursor()
    conn.execute("INSERT OR IGNORE INTO estrellas_grupo(grupoid,total) VALUES(?,0)", (gid,))
    # Calcular nuevo total sin bajar de 0
    c.execute("SELECT total FROM estrellas_grupo WHERE grupoid=?", (gid,))
    row = c.fetchone()
    actual = row["total"] if row else 0
    nuevo  = max(0, actual + cantidad)
    conn.execute("UPDATE estrellas_grupo SET total=? WHERE grupoid=?", (nuevo, gid))
    conn.commit(); conn.close()
    return nuevo


# ══════════════════════════════════════════════════════════════════════════════
#  RANKING
# ══════════════════════════════════════════════════════════════════════════════

def guardar_ranking(gid, puntaje, dificultad="Normal"):
    import datetime
    nombre = nombregrupoporid(gid)
    fecha  = datetime.date.today().isoformat()
    conn   = getconn()
    conn.execute(
        "INSERT INTO ranking(grupoid,nombregrupo,puntaje,dificultad,fecha) VALUES(?,?,?,?,?)",
        (gid, nombre, puntaje, dificultad, fecha))
    conn.commit(); conn.close()


def obtener_ranking(dificultad=None, limite=10):
    conn = getconn(); c = conn.cursor()
    if dificultad:
        c.execute(
            """SELECT nombregrupo,puntaje,dificultad,fecha,grupoid FROM ranking
               WHERE dificultad=? ORDER BY puntaje DESC LIMIT ?""",
            (dificultad, limite))
    else:
        c.execute(
            """SELECT nombregrupo,puntaje,dificultad,fecha,grupoid FROM ranking
               ORDER BY puntaje DESC LIMIT ?""",
            (limite,))
    rows = c.fetchall(); conn.close()
    return [dict(r) for r in rows]
