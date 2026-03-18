import sqlite3
import hashlib
import os
import base64
import streamlit as st

DB_PATH = "database.db"
COOLDOWN = 3  # importado inline para evitar dependencia circular


# ── GitHub persistencia ───────────────────────────────────────────────────────
def _github_save():
    try:
        import requests
        token  = st.secrets.get("GITHUB_TOKEN", "")
        repo   = st.secrets.get("GITHUB_REPO", "")
        branch = st.secrets.get("GITHUB_BRANCH", "main")
        if not token or not repo:
            return
        url = f"https://api.github.com/repos/{repo}/contents/{DB_PATH}"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        with open(DB_PATH, "rb") as f:
            content = base64.b64encode(f.read()).decode()
        r = requests.get(url, headers=headers)
        sha = r.json().get("sha", "") if r.status_code == 200 else ""
        payload = {"message": "chore: auto-save database.db", "content": content, "branch": branch}
        if sha:
            payload["sha"] = sha
        requests.put(url, json=payload, headers=headers)
    except Exception:
        pass


def _github_restore():
    try:
        import requests
        if os.path.exists(DB_PATH):
            return
        token  = st.secrets.get("GITHUB_TOKEN", "")
        repo   = st.secrets.get("GITHUB_REPO", "")
        branch = st.secrets.get("GITHUB_BRANCH", "main")
        if not token or not repo:
            return
        url = f"https://api.github.com/repos/{repo}/contents/{DB_PATH}"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        r = requests.get(url, headers=headers, params={"ref": branch})
        if r.status_code == 200:
            data = base64.b64decode(r.json()["content"])
            with open(DB_PATH, "wb") as f:
                f.write(data)
    except Exception:
        pass


# ── Conexión ──────────────────────────────────────────────────────────────────
def getconn():
    _github_restore()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ── Tablas ────────────────────────────────────────────────────────────────────
def inicializardb():
    conn = getconn()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS grupos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombregrupo TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL)""")
    c.execute("""CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        nombreestudiante TEXT NOT NULL,
        FOREIGN KEY(grupoid) REFERENCES grupos(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS progresojuego (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER UNIQUE NOT NULL,
        economia INTEGER DEFAULT 50,
        medioambiente INTEGER DEFAULT 50,
        energia INTEGER DEFAULT 50,
        bienestarsocial INTEGER DEFAULT 50,
        rondaactual INTEGER DEFAULT 1,
        FOREIGN KEY(grupoid) REFERENCES grupos(id))""")
    c.execute("""CREATE TABLE IF NOT EXISTS cooldowndecisiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        grupoid INTEGER NOT NULL,
        decision TEXT NOT NULL,
        rondasrestantes INTEGER NOT NULL,
        FOREIGN KEY(grupoid) REFERENCES grupos(id))""")
    conn.commit()
    conn.close()

# Alias con guion bajo para compatibilidad con app.py
inicializar_db = inicializardb


def hp(p):
    return hashlib.sha256(p.encode()).hexdigest()


# ── Grupos ────────────────────────────────────────────────────────────────────
def registrargrupo(nombre, pw):
    conn = getconn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO grupos(nombregrupo,password) VALUES(?,?)", (nombre.strip(), hp(pw)))
        conn.commit()
        gid = c.lastrowid
        conn.close()
        _github_save()
        return True, gid
    except sqlite3.IntegrityError:
        conn.close()
        return False, None

registrar_grupo = registrargrupo


def logingrupo(nombre, pw):
    conn = getconn()
    c = conn.cursor()
    c.execute("SELECT id FROM grupos WHERE nombregrupo=? AND password=?", (nombre.strip(), hp(pw)))
    row = c.fetchone()
    conn.close()
    return row["id"] if row else None

login_grupo = logingrupo


def nombregrupoporid(gid):
    conn = getconn()
    c = conn.cursor()
    c.execute("SELECT nombregrupo FROM grupos WHERE id=?", (gid,))
    row = c.fetchone()
    conn.close()
    return row["nombregrupo"] if row else "Desconocido"

nombre_grupo_por_id = nombregrupoporid


# ── Estudiantes ───────────────────────────────────────────────────────────────
def guardarestudiante(gid, nombre):
    conn = getconn()
    c = conn.cursor()
    c.execute("INSERT INTO estudiantes(grupoid,nombreestudiante) VALUES(?,?)", (gid, nombre.strip()))
    conn.commit()
    conn.close()
    _github_save()

guardar_estudiante = guardarestudiante


def obtenerestudiantes(gid):
    conn = getconn()
    c = conn.cursor()
    c.execute("SELECT nombreestudiante FROM estudiantes WHERE grupoid=? ORDER BY id", (gid,))
    rows = c.fetchall()
    conn.close()
    return [r["nombreestudiante"] for r in rows]

obtener_estudiantes = obtenerestudiantes


# ── Progreso ──────────────────────────────────────────────────────────────────
def obtenerprogreso(gid):
    conn = getconn()
    c = conn.cursor()
    c.execute("SELECT * FROM progresojuego WHERE grupoid=?", (gid,))
    row = c.fetchone()
    if not row:
        c.execute("""INSERT INTO progresojuego
            (grupoid,economia,medioambiente,energia,bienestarsocial,rondaactual)
            VALUES(?,50,50,50,50,1)""", (gid,))
        conn.commit()
        c.execute("SELECT * FROM progresojuego WHERE grupoid=?", (gid,))
        row = c.fetchone()
    conn.close()
    return dict(row)

obtener_progreso = obtenerprogreso


def actualizarprogreso(gid, eco, amb, ene, bie, ronda):
    conn = getconn()
    c = conn.cursor()
    c.execute("""UPDATE progresojuego
        SET economia=?,medioambiente=?,energia=?,bienestarsocial=?,rondaactual=?
        WHERE grupoid=?""", (eco, amb, ene, bie, ronda, gid))
    conn.commit()
    conn.close()
    _github_save()

actualizar_progreso = actualizarprogreso


def reiniciarprogreso(gid):
    conn = getconn()
    c = conn.cursor()
    c.execute("""UPDATE progresojuego
        SET economia=50,medioambiente=50,energia=50,bienestarsocial=50,rondaactual=1
        WHERE grupoid=?""", (gid,))
    c.execute("DELETE FROM cooldowndecisiones WHERE grupoid=?", (gid,))
    conn.commit()
    conn.close()
    _github_save()

reiniciar_progreso = reiniciarprogreso


# ── Cooldowns ─────────────────────────────────────────────────────────────────
def obtenercooldowns(gid):
    conn = getconn()
    c = conn.cursor()
    c.execute("SELECT decision,rondasrestantes FROM cooldowndecisiones WHERE grupoid=?", (gid,))
    rows = c.fetchall()
    conn.close()
    return {r["decision"]: r["rondasrestantes"] for r in rows}

obtener_cooldowns = obtenercooldowns


def actualizarcooldown(gid, decision, rondausada):
    conn = getconn()
    c = conn.cursor()
    disponibleen = rondausada + COOLDOWN
    c.execute("DELETE FROM cooldowndecisiones WHERE grupoid=? AND decision=?", (gid, decision))
    c.execute("INSERT INTO cooldowndecisiones(grupoid,decision,rondasrestantes) VALUES(?,?,?)",
              (gid, decision, disponibleen))
    conn.commit()
    conn.close()
    _github_save()

actualizar_cooldown = actualizarcooldown


def decrementarcooldowns(gid):
    pass  # cooldowns usan ronda absoluta

decrementar_cooldowns = decrementarcooldowns
