import sqlite3
import hashlib
import os

_DIR    = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_DIR, "database.db")
COOLDOWN = 3

_TABLAS = [
    """CREATE TABLE IF NOT EXISTS grupos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombregrupo TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        nombreestudiante TEXT NOT NULL,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS progresojuego (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        dificultad TEXT NOT NULL DEFAULT 'Normal',
        economia INTEGER DEFAULT 50,
        medioambiente INTEGER DEFAULT 50,
        energia INTEGER DEFAULT 50,
        bienestarsocial INTEGER DEFAULT 50,
        rondaactual INTEGER DEFAULT 1,
        UNIQUE(grupoid, dificultad),
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS cooldowndecisiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        dificultad TEXT NOT NULL DEFAULT 'Normal',
        decision TEXT NOT NULL,
        rondasrestantes INTEGER NOT NULL,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS logros_grupo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        logroid TEXT NOT NULL,
        UNIQUE(grupoid, logroid),
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS misiones_canjeadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        misionid TEXT NOT NULL,
        UNIQUE(grupoid, misionid),
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS estrellas_grupo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER UNIQUE NOT NULL,
        total INTEGER DEFAULT 0,
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
    """CREATE TABLE IF NOT EXISTS ranking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        nombregrupo TEXT NOT NULL,
        puntaje INTEGER NOT NULL,
        dificultad TEXT DEFAULT 'Normal',
        fecha TEXT DEFAULT (date('now')),
        FOREIGN KEY(grupoid) REFERENCES grupos(id)
    )""",
]


def _crear_tablas():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    for sql in _TABLAS:
        conn.execute(sql)
    conn.commit()
    conn.close()


def getconn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='grupos'")
    if cur.fetchone() is None:
        conn.close()
        _crear_tablas()
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
    return conn


def inicializardb():
    conn = getconn(); conn.close()

inicializar_db = inicializardb


def hp(p):
    return hashlib.sha256(p.encode()).hexdigest()


# ── Grupos ────────────────────────────────────────────────────────────────────
def registrargrupo(nombre, pw):
    conn = getconn(); c = conn.cursor()
    try:
        c.execute("INSERT INTO grupos(nombregrupo,password) VALUES(?,?)", (nombre.strip(), hp(pw)))
        conn.commit(); gid = c.lastrowid; conn.close()
        return True, gid
    except sqlite3.IntegrityError:
        conn.close(); return False, None

registrar_grupo = registrargrupo


def logingrupo(nombre, pw):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT id FROM grupos WHERE nombregrupo=? AND password=?", (nombre.strip(), hp(pw)))
    row = c.fetchone(); conn.close()
    return row["id"] if row else None

login_grupo = logingrupo


def nombregrupoporid(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT nombregrupo FROM grupos WHERE id=?", (gid,))
    row = c.fetchone(); conn.close()
    return row["nombregrupo"] if row else "Desconocido"

nombre_grupo_por_id = nombregrupoporid


# ── Estudiantes ───────────────────────────────────────────────────────────────
def guardarestudiante(gid, nombre):
    conn = getconn(); c = conn.cursor()
    c.execute("INSERT INTO estudiantes(grupoid,nombreestudiante) VALUES(?,?)", (gid, nombre.strip()))
    conn.commit(); conn.close()

guardar_estudiante = guardarestudiante


def obtenerestudiantes(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT nombreestudiante FROM estudiantes WHERE grupoid=? ORDER BY id", (gid,))
    rows = c.fetchall(); conn.close()
    return [r["nombreestudiante"] for r in rows]

obtener_estudiantes = obtenerestudiantes


# ── Progreso por dificultad ───────────────────────────────────────────────────
def obtenerprogreso(gid, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT * FROM progresojuego WHERE grupoid=? AND dificultad=?", (gid, dificultad))
    row = c.fetchone()
    if not row:
        c.execute("""INSERT INTO progresojuego
            (grupoid,dificultad,economia,medioambiente,energia,bienestarsocial,rondaactual)
            VALUES(?,?,50,50,50,50,1)""", (gid, dificultad))
        conn.commit()
        c.execute("SELECT * FROM progresojuego WHERE grupoid=? AND dificultad=?", (gid, dificultad))
        row = c.fetchone()
    conn.close(); return dict(row)

obtener_progreso = obtenerprogreso


def actualizarprogreso(gid, eco, amb, ene, bie, ronda, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    c.execute("""UPDATE progresojuego
        SET economia=?,medioambiente=?,energia=?,bienestarsocial=?,rondaactual=?
        WHERE grupoid=? AND dificultad=?""", (eco, amb, ene, bie, ronda, gid, dificultad))
    conn.commit(); conn.close()

actualizar_progreso = actualizarprogreso


def reiniciarprogreso(gid, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    c.execute("""UPDATE progresojuego
        SET economia=50,medioambiente=50,energia=50,bienestarsocial=50,rondaactual=1
        WHERE grupoid=? AND dificultad=?""", (gid, dificultad))
    c.execute("DELETE FROM cooldowndecisiones WHERE grupoid=? AND dificultad=?", (gid, dificultad))
    conn.commit(); conn.close()

reiniciar_progreso = reiniciarprogreso


# ── Cooldowns ─────────────────────────────────────────────────────────────────
def obtenercooldowns(gid, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT decision,rondasrestantes FROM cooldowndecisiones WHERE grupoid=? AND dificultad=?",
              (gid, dificultad))
    rows = c.fetchall(); conn.close()
    return {r["decision"]: r["rondasrestantes"] for r in rows}

obtener_cooldowns = obtenercooldowns


def actualizarcooldown(gid, decision, rondausada, dificultad="Normal"):
    conn = getconn(); c = conn.cursor()
    disponibleen = rondausada + COOLDOWN
    c.execute("DELETE FROM cooldowndecisiones WHERE grupoid=? AND decision=? AND dificultad=?",
              (gid, decision, dificultad))
    c.execute("INSERT INTO cooldowndecisiones(grupoid,dificultad,decision,rondasrestantes) VALUES(?,?,?,?)",
              (gid, dificultad, decision, disponibleen))
    conn.commit(); conn.close()

actualizar_cooldown = actualizarcooldown
decrementar_cooldowns = lambda gid, dif="Normal": None
decrementarcooldowns  = decrementar_cooldowns


# ── Logros ────────────────────────────────────────────────────────────────────
def obtener_logros_grupo(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT logroid FROM logros_grupo WHERE grupoid=?", (gid,))
    rows = c.fetchall(); conn.close()
    return [r["logroid"] for r in rows]


def guardar_logro(gid, logro_id):
    conn = getconn()
    conn.execute("INSERT OR IGNORE INTO logros_grupo(grupoid,logroid) VALUES(?,?)", (gid, logro_id))
    conn.commit(); conn.close()


# ── Misiones ──────────────────────────────────────────────────────────────────
def obtener_misiones_canjeadas(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT misionid FROM misiones_canjeadas WHERE grupoid=?", (gid,))
    rows = c.fetchall(); conn.close()
    return [r["misionid"] for r in rows]


def guardar_mision(gid, mision_id):
    conn = getconn()
    conn.execute("INSERT OR IGNORE INTO misiones_canjeadas(grupoid,misionid) VALUES(?,?)", (gid, mision_id))
    conn.commit(); conn.close()


# ── Estrellas ─────────────────────────────────────────────────────────────────
def obtener_estrellas(gid):
    conn = getconn(); c = conn.cursor()
    c.execute("SELECT total FROM estrellas_grupo WHERE grupoid=?", (gid,))
    row = c.fetchone(); conn.close()
    return row["total"] if row else 0


def guardar_estrellas(gid, cantidad):
    conn = getconn()
    conn.execute("INSERT OR IGNORE INTO estrellas_grupo(grupoid,total) VALUES(?,0)", (gid,))
    conn.execute("UPDATE estrellas_grupo SET total=total+? WHERE grupoid=?", (cantidad, gid))
    conn.commit(); conn.close()


# ── Ranking ───────────────────────────────────────────────────────────────────
def guardar_ranking(gid, puntaje, dificultad="Normal"):
    nombre = nombregrupoporid(gid)
    conn = getconn()
    conn.execute("INSERT INTO ranking(grupoid,nombregrupo,puntaje,dificultad) VALUES(?,?,?,?)",
                 (gid, nombre, puntaje, dificultad))
    conn.commit(); conn.close()


def obtener_ranking(dificultad=None, limite=10):
    conn = getconn(); c = conn.cursor()
    if dificultad:
        c.execute("""SELECT nombregrupo,puntaje,dificultad,fecha,grupoid FROM ranking
                     WHERE dificultad=? ORDER BY puntaje DESC LIMIT ?""", (dificultad, limite))
    else:
        c.execute("""SELECT nombregrupo,puntaje,dificultad,fecha,grupoid FROM ranking
                     ORDER BY puntaje DESC LIMIT ?""", (limite,))
    rows = c.fetchall(); conn.close()
    return [dict(r) for r in rows]
