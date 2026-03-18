import sqlite3, hashlib

DB_PATH = "database.db"

def _conn():
    c = sqlite3.connect(DB_PATH, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c

def _migrar(con):
    cur = con.cursor()
    def _cols(tabla):
        cur.execute(f"PRAGMA table_info({tabla})")
        return {r["name"] for r in cur.fetchall()}

    g = _cols("grupos")
    if "estrellas" not in g:
        cur.execute("ALTER TABLE grupos ADD COLUMN estrellas INTEGER DEFAULT 0")

    p = _cols("progreso_juego")
    if "dificultad" not in p:
        cur.execute("ALTER TABLE progreso_juego ADD COLUMN dificultad TEXT NOT NULL DEFAULT 'Normal'")
    if "en_curso" not in p:
        cur.execute("ALTER TABLE progreso_juego ADD COLUMN en_curso INTEGER DEFAULT 1")

    c2 = _cols("cooldown_decisiones")
    if "dificultad" not in c2:
        cur.execute("ALTER TABLE cooldown_decisiones ADD COLUMN dificultad TEXT NOT NULL DEFAULT 'Normal'")
    if "disponible_en" not in c2 and "rondas_restantes" in c2:
        try: cur.execute("ALTER TABLE cooldown_decisiones RENAME COLUMN rondas_restantes TO disponible_en")
        except: pass

    con.commit()

def inicializar_db():
    con = _conn(); cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS grupos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_grupo TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        estrellas INTEGER DEFAULT 0)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS estudiantes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        nombre_estudiante TEXT NOT NULL,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS progreso_juego(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        dificultad TEXT NOT NULL DEFAULT 'Normal',
        economia INTEGER DEFAULT 50,
        medio_ambiente INTEGER DEFAULT 50,
        energia INTEGER DEFAULT 50,
        bienestar_social INTEGER DEFAULT 50,
        ronda_actual INTEGER DEFAULT 1,
        en_curso INTEGER DEFAULT 1,
        UNIQUE(grupo_id,dificultad),
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS cooldown_decisiones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        dificultad TEXT NOT NULL DEFAULT 'Normal',
        decision TEXT NOT NULL,
        disponible_en INTEGER NOT NULL,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS ranking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER,
        nombre_grupo TEXT NOT NULL,
        dificultad TEXT NOT NULL DEFAULT 'Normal',
        puntaje INTEGER NOT NULL,
        correctas INTEGER DEFAULT 0,
        incorrectas INTEGER DEFAULT 0,
        logros TEXT DEFAULT '',
        fecha TEXT DEFAULT (date('now')))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS logros_obtenidos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        logro_id TEXT NOT NULL,
        fecha TEXT DEFAULT (date('now')),
        UNIQUE(grupo_id,logro_id),
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS misiones_canjeadas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        mision_id TEXT NOT NULL,
        fecha TEXT DEFAULT (date('now')),
        UNIQUE(grupo_id,mision_id),
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    cur.execute("""CREATE TABLE IF NOT EXISTS stats_grupo(
        grupo_id INTEGER PRIMARY KEY,
        partidas_total INTEGER DEFAULT 0,
        correctas_total INTEGER DEFAULT 0,
        victorias_facil INTEGER DEFAULT 0,
        victorias_normal INTEGER DEFAULT 0,
        victorias_dificil INTEGER DEFAULT 0,
        racha_max INTEGER DEFAULT 0,
        decisiones_usadas TEXT DEFAULT '',
        dias_jugados TEXT DEFAULT '',
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    con.commit()
    _migrar(con)
    con.close()

def _hp(p): return hashlib.sha256(p.encode()).hexdigest()

# ── Grupos ────────────────────────────────────────────────────────────────────
def registrar_grupo(nombre, pw):
    con = _conn(); cur = con.cursor()
    try:
        cur.execute("INSERT INTO grupos(nombre_grupo,password) VALUES(?,?)",
                    (nombre.strip(), _hp(pw)))
        con.commit(); gid = cur.lastrowid
        cur.execute("INSERT OR IGNORE INTO stats_grupo(grupo_id) VALUES(?)",(gid,))
        con.commit(); con.close()
        return True, gid
    except sqlite3.IntegrityError:
        con.close(); return False, None

def login_grupo(nombre, pw):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT id FROM grupos WHERE nombre_grupo=? AND password=?",
                (nombre.strip(), _hp(pw)))
    row = cur.fetchone(); con.close()
    return row["id"] if row else None

def nombre_grupo_por_id(gid):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT nombre_grupo FROM grupos WHERE id=?", (gid,))
    row = cur.fetchone(); con.close()
    return row["nombre_grupo"] if row else "Desconocido"

# ── Estrellas ─────────────────────────────────────────────────────────────────
def obtener_estrellas(gid):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT estrellas FROM grupos WHERE id=?", (gid,))
    row = cur.fetchone(); con.close()
    return row["estrellas"] if row else 0

def sumar_estrellas(gid, cantidad):
    if cantidad <= 0: return
    con = _conn(); cur = con.cursor()
    cur.execute("UPDATE grupos SET estrellas=estrellas+? WHERE id=?", (cantidad, gid))
    con.commit(); con.close()

def gastar_estrellas(gid, cantidad):
    """Descuenta estrellas. Retorna True si había suficientes."""
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT estrellas FROM grupos WHERE id=?", (gid,))
    row = cur.fetchone()
    if not row or row["estrellas"] < cantidad:
        con.close(); return False
    cur.execute("UPDATE grupos SET estrellas=estrellas-? WHERE id=?", (cantidad, gid))
    con.commit(); con.close()
    return True

# ── Estudiantes ───────────────────────────────────────────────────────────────
def guardar_estudiante(gid, nombre):
    con = _conn(); cur = con.cursor()
    cur.execute("INSERT INTO estudiantes(grupo_id,nombre_estudiante) VALUES(?,?)",
                (gid, nombre.strip()))
    con.commit(); con.close()

def obtener_estudiantes(gid):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT nombre_estudiante FROM estudiantes WHERE grupo_id=? ORDER BY id", (gid,))
    rows = cur.fetchall(); con.close()
    return [r["nombre_estudiante"] for r in rows]

# ── Progreso ──────────────────────────────────────────────────────────────────
def obtener_progreso(gid, dificultad="Normal"):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT * FROM progreso_juego WHERE grupo_id=? AND dificultad=?", (gid, dificultad))
    row = cur.fetchone()
    if not row:
        cur.execute("""INSERT OR IGNORE INTO progreso_juego
            (grupo_id,dificultad,economia,medio_ambiente,energia,bienestar_social,ronda_actual,en_curso)
            VALUES(?,?,50,50,50,50,1,1)""", (gid, dificultad))
        con.commit()
        cur.execute("SELECT * FROM progreso_juego WHERE grupo_id=? AND dificultad=?", (gid, dificultad))
        row = cur.fetchone()
    con.close()
    return dict(row)

def actualizar_progreso(gid, eco, amb, ene, bie, ronda, dificultad="Normal"):
    con = _conn(); cur = con.cursor()
    cur.execute("""UPDATE progreso_juego SET economia=?,medio_ambiente=?,energia=?,
        bienestar_social=?,ronda_actual=?,en_curso=1 WHERE grupo_id=? AND dificultad=?""",
                (eco, amb, ene, bie, ronda, gid, dificultad))
    con.commit(); con.close()

def reiniciar_progreso(gid, dificultad="Normal"):
    con = _conn(); cur = con.cursor()
    cur.execute("""UPDATE progreso_juego SET economia=50,medio_ambiente=50,energia=50,
        bienestar_social=50,ronda_actual=1,en_curso=1 WHERE grupo_id=? AND dificultad=?""",
                (gid, dificultad))
    cur.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=? AND dificultad=?", (gid, dificultad))
    con.commit(); con.close()

def marcar_partida_terminada(gid, dificultad="Normal"):
    con = _conn(); cur = con.cursor()
    cur.execute("UPDATE progreso_juego SET en_curso=0 WHERE grupo_id=? AND dificultad=?",
                (gid, dificultad))
    con.commit(); con.close()

def partida_en_curso(gid, dificultad="Normal"):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT en_curso,ronda_actual FROM progreso_juego WHERE grupo_id=? AND dificultad=?",
                (gid, dificultad))
    row = cur.fetchone(); con.close()
    if not row: return False
    return bool(row["en_curso"]) and row["ronda_actual"] > 1

# ── Cooldowns ─────────────────────────────────────────────────────────────────
def obtener_cooldowns(gid, dificultad="Normal"):
    con = _conn(); cur = con.cursor()
    cur.execute("PRAGMA table_info(cooldown_decisiones)")
    cols = {r["name"] for r in cur.fetchall()}
    col = "disponible_en" if "disponible_en" in cols else "rondas_restantes"
    cur.execute(f"SELECT decision,{col} FROM cooldown_decisiones WHERE grupo_id=? AND dificultad=?",
                (gid, dificultad))
    rows = cur.fetchall(); con.close()
    return {r[0]: r[1] for r in rows}

def actualizar_cooldown(gid, decision, ronda_usada, dificultad="Normal"):
    from config import COOLDOWN
    con = _conn(); cur = con.cursor()
    cur.execute("PRAGMA table_info(cooldown_decisiones)")
    cols = {r["name"] for r in cur.fetchall()}
    col = "disponible_en" if "disponible_en" in cols else "rondas_restantes"
    cur.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=? AND decision=? AND dificultad=?",
                (gid, decision, dificultad))
    cur.execute(f"INSERT INTO cooldown_decisiones(grupo_id,dificultad,decision,{col}) VALUES(?,?,?,?)",
                (gid, dificultad, decision, ronda_usada + COOLDOWN))
    con.commit(); con.close()

# ── Ranking ───────────────────────────────────────────────────────────────────
def guardar_ranking(gid, nombre_grupo, puntaje, correctas, incorrectas, dificultad, logros):
    logros_str = ", ".join(logros) if logros else ""
    con = _conn(); cur = con.cursor()
    cur.execute("""INSERT INTO ranking(grupo_id,nombre_grupo,dificultad,puntaje,
        correctas,incorrectas,logros) VALUES(?,?,?,?,?,?,?)""",
                (gid, nombre_grupo, dificultad, puntaje, correctas, incorrectas, logros_str))
    con.commit(); con.close()

def obtener_ranking(dificultad=None):
    con = _conn(); cur = con.cursor()
    if dificultad:
        cur.execute("SELECT * FROM ranking WHERE dificultad=? ORDER BY puntaje DESC LIMIT 20", (dificultad,))
    else:
        cur.execute("SELECT * FROM ranking ORDER BY puntaje DESC LIMIT 20")
    rows = cur.fetchall(); con.close()
    return [dict(r) for r in rows]

def obtener_estudiantes_ranking(gid):
    return obtener_estudiantes(gid)

# ── Logros ────────────────────────────────────────────────────────────────────
def obtener_logros_grupo(gid):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT logro_id FROM logros_obtenidos WHERE grupo_id=?", (gid,))
    rows = cur.fetchall(); con.close()
    return {r["logro_id"] for r in rows}

def desbloquear_logro(gid, logro_id):
    con = _conn(); cur = con.cursor()
    try:
        cur.execute("INSERT OR IGNORE INTO logros_obtenidos(grupo_id,logro_id) VALUES(?,?)",
                    (gid, logro_id))
        changed = cur.rowcount
        con.commit(); con.close()
        return changed > 0
    except: con.close(); return False

# ── Misiones ──────────────────────────────────────────────────────────────────
def obtener_misiones_canjeadas(gid):
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT mision_id FROM misiones_canjeadas WHERE grupo_id=?", (gid,))
    rows = cur.fetchall(); con.close()
    return {r["mision_id"] for r in rows}

def canjear_mision(gid, mision_id, estrellas):
    """Marca misión como canjeada y suma estrellas. Retorna True si fue nuevo canje."""
    con = _conn(); cur = con.cursor()
    try:
        cur.execute("INSERT OR IGNORE INTO misiones_canjeadas(grupo_id,mision_id) VALUES(?,?)",
                    (gid, mision_id))
        changed = cur.rowcount
        if changed:
            cur.execute("UPDATE grupos SET estrellas=estrellas+? WHERE id=?", (estrellas, gid))
        con.commit(); con.close()
        return changed > 0
    except: con.close(); return False

# ── Stats ─────────────────────────────────────────────────────────────────────
def obtener_stats(gid):
    con = _conn(); cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO stats_grupo(grupo_id) VALUES(?)", (gid,))
    con.commit()
    cur.execute("SELECT * FROM stats_grupo WHERE grupo_id=?", (gid,))
    row = cur.fetchone(); con.close()
    return dict(row) if row else {}

def actualizar_stats(gid, **kwargs):
    if not kwargs: return
    con = _conn(); cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO stats_grupo(grupo_id) VALUES(?)", (gid,))
    for k, v in kwargs.items():
        try: cur.execute(f"UPDATE stats_grupo SET {k}=? WHERE grupo_id=?", (v, gid))
        except: pass
    con.commit(); con.close()
