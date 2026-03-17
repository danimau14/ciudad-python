import sqlite3, time, hashlib, os


def _get_db_path():
    for d in ["/tmp", os.path.expanduser("~"), os.getcwd()]:
        try:
            t = os.path.join(d, "_tw.tmp")
            open(t, "w").close()
            os.remove(t)
            return os.path.join(d, "database.db")
        except Exception:
            continue
    return "database.db"


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
        dificultad TEXT DEFAULT 'Medio'
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS estudiantes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        nombre_estudiante TEXT NOT NULL,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS progreso_juego(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER UNIQUE NOT NULL,
        economia INTEGER DEFAULT 50,
        medio_ambiente INTEGER DEFAULT 50,
        energia INTEGER DEFAULT 50,
        bienestar_social INTEGER DEFAULT 50,
        ronda_actual INTEGER DEFAULT 1,
        partida_terminada INTEGER DEFAULT 0,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS cooldown_decisiones(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER NOT NULL,
        decision TEXT NOT NULL,
        disponible_en INTEGER NOT NULL,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS ranking(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupo_id INTEGER,
        nombre_grupo TEXT NOT NULL,
        puntaje INTEGER NOT NULL,
        correctas INTEGER DEFAULT 0,
        incorrectas INTEGER DEFAULT 0,
        dificultad TEXT DEFAULT 'Medio',
        logros TEXT DEFAULT '',
        fecha TEXT DEFAULT (datetime('now','localtime'))
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS estrellas(
        grupo_id INTEGER PRIMARY KEY,
        total INTEGER DEFAULT 0,
        FOREIGN KEY(grupo_id) REFERENCES grupos(id)
    )""")
    # Agregar columnas faltantes si ya existe la tabla (migraciones seguras)
    try:
        c.execute("ALTER TABLE progreso_juego ADD COLUMN partida_terminada INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE ranking ADD COLUMN incorrectas INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        c.execute("ALTER TABLE ranking ADD COLUMN grupo_id INTEGER")
    except Exception:
        pass
    conn.commit()
    conn.close()


def registrar_grupo(nombre, pw):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO grupos(nombre_grupo,password) VALUES(?,?)",
                  (nombre.strip(), hp(pw)))
        conn.commit()
        gid = c.lastrowid
        # Inicializar estrellas
        c.execute("INSERT OR IGNORE INTO estrellas(grupo_id,total) VALUES(?,0)", (gid,))
        conn.commit()
        return True, gid
    except sqlite3.IntegrityError:
        return False, None
    finally:
        conn.close()


def login_grupo(nombre, pw):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT id FROM grupos WHERE nombre_grupo=? AND password=?",
                  (nombre.strip(), hp(pw)))
        row = c.fetchone()
        return row["id"] if row else None
    finally:
        conn.close()


def guardar_estudiante(gid, nombre):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO estudiantes(grupo_id,nombre_estudiante) VALUES(?,?)",
                  (gid, nombre.strip()))
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


def obtener_progreso(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM progreso_juego WHERE grupo_id=?", (gid,))
        row = c.fetchone()
        if not row:
            c.execute(
                "INSERT INTO progreso_juego(grupo_id,economia,medio_ambiente,energia,bienestar_social,ronda_actual) "
                "VALUES(?,50,50,50,50,1)", (gid,))
            conn.commit()
            c.execute("SELECT * FROM progreso_juego WHERE grupo_id=?", (gid,))
            row = c.fetchone()
        return dict(row)
    finally:
        conn.close()


def actualizar_progreso(gid, eco, amb, ene, bie, ronda):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute(
            "UPDATE progreso_juego SET economia=?,medio_ambiente=?,energia=?,"
            "bienestar_social=?,ronda_actual=? WHERE grupo_id=?",
            (eco, amb, ene, bie, ronda, gid))
        conn.commit()
    finally:
        conn.close()


def marcar_partida_terminada(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("UPDATE progreso_juego SET partida_terminada=1 WHERE grupo_id=?", (gid,))
        conn.commit()
    finally:
        conn.close()


def reiniciar_progreso(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute(
            "UPDATE progreso_juego SET economia=50,medio_ambiente=50,energia=50,"
            "bienestar_social=50,ronda_actual=1,partida_terminada=0 WHERE grupo_id=?", (gid,))
        c.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=?", (gid,))
        conn.commit()
    finally:
        conn.close()


def obtener_cooldowns(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT decision,disponible_en FROM cooldown_decisiones WHERE grupo_id=?", (gid,))
        return {r["decision"]: r["disponible_en"] for r in c.fetchall()}
    finally:
        conn.close()


def actualizar_cooldown(gid, decision, ronda_usada):
    from config import COOLDOWN
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=? AND decision=?",
                  (gid, decision))
        disponible_en = ronda_usada + COOLDOWN
        c.execute("INSERT INTO cooldown_decisiones(grupo_id,decision,disponible_en) VALUES(?,?,?)",
                  (gid, decision, disponible_en))
        conn.commit()
    finally:
        conn.close()


def decrementar_cooldowns(gid):
    # Los cooldowns usan ronda absoluta, no necesitan decrementarse
    pass


def guardar_ranking(gid, nombre_grupo, puntaje, correctas, incorrectas, dificultad, logros):
    conn = get_conn()
    try:
        c = conn.cursor()
        logros_str = ",".join(logros) if logros else ""
        c.execute(
            "INSERT INTO ranking(grupo_id,nombre_grupo,puntaje,correctas,incorrectas,dificultad,logros) "
            "VALUES(?,?,?,?,?,?,?)",
            (gid, nombre_grupo, puntaje, correctas, incorrectas, dificultad, logros_str))
        conn.commit()
    finally:
        conn.close()


def obtener_ranking(dificultad=None):
    conn = get_conn()
    try:
        c = conn.cursor()
        if dificultad:
            c.execute(
                "SELECT grupo_id,nombre_grupo,puntaje,correctas,dificultad,logros,fecha "
                "FROM ranking WHERE dificultad=? ORDER BY puntaje DESC LIMIT 10",
                (dificultad,))
        else:
            c.execute(
                "SELECT grupo_id,nombre_grupo,puntaje,correctas,dificultad,logros,fecha "
                "FROM ranking ORDER BY puntaje DESC LIMIT 10")
        return [dict(r) for r in c.fetchall()]
    finally:
        conn.close()


def obtener_estudiantes_ranking(gid):
    if not gid:
        return []
    return obtener_estudiantes(gid)


def nombre_grupo_por_id(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT nombre_grupo FROM grupos WHERE id=?", (gid,))
        row = c.fetchone()
        return row["nombre_grupo"] if row else "Desconocido"
    finally:
        conn.close()


def obtener_estrellas(gid):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO estrellas(grupo_id,total) VALUES(?,0)", (gid,))
        conn.commit()
        c.execute("SELECT total FROM estrellas WHERE grupo_id=?", (gid,))
        row = c.fetchone()
        return row["total"] if row else 0
    finally:
        conn.close()


def actualizar_estrellas(gid, delta):
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO estrellas(grupo_id,total) VALUES(?,0)", (gid,))
        c.execute("UPDATE estrellas SET total=MAX(0,total+?) WHERE grupo_id=?", (delta, gid))
        conn.commit()
    finally:
        conn.close()
