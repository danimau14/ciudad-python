import sqlite3, time, hashlib, os, sys

# Elegir directorio escribible automáticamente
def _get_db_path():
    candidates = ["/tmp", os.path.expanduser("~"), os.getcwd()]
    for d in candidates:
        try:
            test = os.path.join(d, "_test_write.tmp")
            with open(test, "w") as f:
                f.write("ok")
            os.remove(test)
            return os.path.join(d, "database.db")
        except Exception:
            continue
    return "database.db"  # fallback

DB_PATH = _get_db_path()


def get_conn():
    last_err = None
    for intento in range(8):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=15, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=8000")
            conn.execute("PRAGMA synchronous=NORMAL")
            return conn
        except Exception as e:
            last_err = e
            time.sleep(0.3 * (intento + 1))
    raise RuntimeError(f"No se pudo conectar a DB ({DB_PATH}): {last_err}")


def hp(p):
    return hashlib.sha256(p.encode()).hexdigest()


def inicializar_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS grupos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_grupo TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        dificultad TEXT DEFAULT 'Medio')""")
    c.execute("""CREATE TABLE IF NOT EXISTS estudiantes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        nombre_estudiante TEXT NOT NULL,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS progreso_juego(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL UNIQUE,
        economia INTEGER DEFAULT 50,
        medio_ambiente INTEGER DEFAULT 50,
        energia INTEGER DEFAULT 50,
        bienestar_social INTEGER DEFAULT 50,
        ronda_actual INTEGER DEFAULT 1,
        partida_terminada INTEGER DEFAULT 0,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS cooldown_decisiones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        decision TEXT NOT NULL,
        rondas_restantes INTEGER NOT NULL,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS ranking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        nombre_grupo TEXT NOT NULL,
        puntaje INTEGER DEFAULT 0,
        correctas INTEGER DEFAULT 0,
        incorrectas INTEGER DEFAULT 0,
        dificultad TEXT DEFAULT 'Medio',
        logros TEXT DEFAULT '',
        fecha TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS estrellas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL UNIQUE,
        total INTEGER DEFAULT 0,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
    # Migraciones automáticas
    for sql in [
        "ALTER TABLE grupos ADD COLUMN dificultad TEXT DEFAULT 'Medio'",
        "ALTER TABLE progreso_juego ADD COLUMN partida_terminada INTEGER DEFAULT 0",
        "CREATE TABLE IF NOT EXISTS estrellas(id INTEGER PRIMARY KEY AUTOINCREMENT, grupo_id INTEGER NOT NULL UNIQUE, total INTEGER DEFAULT 0)",
    ]:
        try:
            conn.execute(sql)
        except Exception:
            pass
    conn.commit()
    conn.close()


def hpv(v): return max(0, min(100, v))


# ─── GRUPOS ───────────────────────────────────────────────────────
def registrar_grupo(nombre, password, dificultad):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO grupos(nombre_grupo, password, dificultad) VALUES(?,?,?)",
                  (nombre.strip(), hp(password), dificultad))
        conn.commit()
        return c.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def login_grupo(nombre, password):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT id, dificultad FROM grupos WHERE nombre_grupo=? AND password=?",
                  (nombre.strip(), hp(password)))
        row = c.fetchone()
        return (row["id"], row["dificultad"]) if row else None
    finally:
        conn.close()


def nombre_grupo_por_id(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT nombre_grupo FROM grupos WHERE id=?", (gid,))
        row = c.fetchone()
        return row["nombre_grupo"] if row else ""
    finally:
        conn.close()


# ─── ESTUDIANTES ──────────────────────────────────────────────────
def guardar_estudiante(gid, nombre):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO estudiantes(grupo_id, nombre_estudiante) VALUES(?,?)",
                     (gid, nombre))
        conn.commit()
    finally:
        conn.close()


def obtener_estudiantes(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT nombre_estudiante FROM estudiantes WHERE grupo_id=? ORDER BY id", (gid,))
        return [r["nombre_estudiante"] for r in c.fetchall()]
    finally:
        conn.close()


# ─── PROGRESO ─────────────────────────────────────────────────────
def obtener_progreso(gid):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM progreso_juego WHERE grupo_id=?", (gid,))
        row = c.fetchone()
        if not row:
            c.execute("INSERT INTO progreso_juego(grupo_id,economia,medio_ambiente,"
                      "energia,bienestar_social,ronda_actual) VALUES(?,50,50,50,50,1)", (gid,))
            conn.commit()
            c.execute("SELECT * FROM progreso_juego WHERE grupo_id=?", (gid,))
            row = c.fetchone()
        return dict(row)
    finally:
        conn.close()


def actualizar_progreso(gid, eco, amb, ene, bie, ronda):
    conn = get_conn()
    try:
        conn.execute("UPDATE progreso_juego SET economia=?,medio_ambiente=?,energia=?,"
                     "bienestar_social=?,ronda_actual=? WHERE grupo_id=?",
                     (hpv(eco), hpv(amb), hpv(ene), hpv(bie), ronda, gid))
        conn.commit()
    finally:
        conn.close()




def marcar_partida_terminada(gid):
    conn = get_conn()
    try:
        conn.execute("UPDATE progreso_juego SET partida_terminada=1 WHERE grupo_id=?", (gid,))
        conn.commit()
    finally:
        conn.close()
def reiniciar_progreso(gid):
    conn = get_conn()
    try:
        conn.execute("UPDATE progreso_juego SET economia=50,medio_ambiente=50,"
                     "energia=50,bienestar_social=50,ronda_actual=1,partida_terminada=0 WHERE grupo_id=?", (gid,))
        conn.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=?", (gid,))
        conn.commit()
    finally:
        conn.close()


# ─── COOLDOWNS ────────────────────────────────────────────────────
def obtener_cooldowns(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT decision, rondas_restantes FROM cooldown_decisiones WHERE grupo_id=?", (gid,))
        return {r["decision"]: r["rondas_restantes"] for r in c.fetchall()}
    finally:
        conn.close()


def actualizar_cooldown(gid, decision, ronda_actual):
    from config import COOLDOWN
    conn = get_conn()
    try:
        disponible_en = ronda_actual + COOLDOWN
        c = conn.cursor()
        c.execute("SELECT id FROM cooldown_decisiones WHERE grupo_id=? AND decision=?",
                  (gid, decision))
        row = c.fetchone()
        if row:
            conn.execute("UPDATE cooldown_decisiones SET rondas_restantes=? "
                         "WHERE grupo_id=? AND decision=?",
                         (disponible_en, gid, decision))
        else:
            conn.execute("INSERT INTO cooldown_decisiones(grupo_id,decision,rondas_restantes) "
                         "VALUES(?,?,?)", (gid, decision, disponible_en))
        conn.commit()
    finally:
        conn.close()


def cooldown_disponible(gid, decision, ronda_actual):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT rondas_restantes FROM cooldown_decisiones "
                  "WHERE grupo_id=? AND decision=?", (gid, decision))
        row = c.fetchone()
        return (not row) or (ronda_actual >= row["rondas_restantes"])
    finally:
        conn.close()


def decrementar_cooldowns(gid):
    conn = get_conn()
    try:
        conn.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=? "
                     "AND rondas_restantes <= 0", (gid,))
        conn.commit()
    finally:
        conn.close()


# ─── RANKING ──────────────────────────────────────────────────────
def guardar_ranking(gid, nombre, puntaje, correctas, incorrectas, dificultad, logros):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT id, puntaje FROM ranking WHERE grupo_id=? AND dificultad=?",
                  (gid, dificultad))
        existing = c.fetchone()
        logros_str = ",".join(logros) if logros else ""
        if existing:
            if puntaje > existing["puntaje"]:
                conn.execute("UPDATE ranking SET puntaje=?,correctas=?,incorrectas=?,logros=?,"
                             "fecha=CURRENT_TIMESTAMP WHERE id=?",
                             (puntaje, correctas, incorrectas, logros_str, existing["id"]))
                conn.commit()
        else:
            conn.execute("INSERT INTO ranking(grupo_id,nombre_grupo,puntaje,correctas,"
                         "incorrectas,dificultad,logros) VALUES(?,?,?,?,?,?,?)",
                         (gid, nombre, puntaje, correctas, incorrectas, dificultad, logros_str))
            conn.commit()
    finally:
        conn.close()




def dificultad_jugada(gid, dificultad):
    """Retorna True si el grupo ya tiene una partida registrada en ese nivel."""
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM ranking WHERE grupo_id=? AND dificultad=?",
                  (gid, dificultad))
        return c.fetchone() is not None
    finally:
        conn.close()


def obtener_estrellas(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT total FROM estrellas WHERE grupo_id=?", (gid,))
        row = c.fetchone()
        if not row:
            conn.execute("INSERT INTO estrellas(grupo_id,total) VALUES(?,0)", (gid,))
            conn.commit()
            return 0
        return row["total"]
    finally:
        conn.close()


def actualizar_estrellas(gid, delta):
    """Suma o resta estrellas. Nunca baja de 0."""
    conn = get_conn()
    try:
        actual = obtener_estrellas(gid)
        nuevo  = max(0, actual + delta)
        conn.execute("INSERT INTO estrellas(grupo_id,total) VALUES(?,?) "
                     "ON CONFLICT(grupo_id) DO UPDATE SET total=?", (gid, nuevo, nuevo))
        conn.commit()
        return nuevo
    finally:
        conn.close()


def obtener_estudiantes_ranking(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT nombre_estudiante FROM estudiantes WHERE grupo_id=? ORDER BY id", (gid,))
        return [r["nombre_estudiante"] for r in c.fetchall()]
    finally:
        conn.close()

def obtener_ranking(dificultad=None):
    conn = get_conn()
    try:
        c = conn.cursor()
        if dificultad:
            c.execute("SELECT grupo_id,nombre_grupo,puntaje,correctas,dificultad,logros,fecha "
                      "FROM ranking WHERE dificultad=? ORDER BY puntaje DESC LIMIT 10",
                      (dificultad,))
        else:
            c.execute("SELECT grupo_id,nombre_grupo,puntaje,correctas,dificultad,logros,fecha "
                      "FROM ranking ORDER BY puntaje DESC LIMIT 10")
        return [dict(r) for r in c.fetchall()]
    finally:
        conn.close()
