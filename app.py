# VERSIÓN: 2026-03-16 00:59:18
# ============================================================
# Ciudad en Equilibrio - Ingenieria Edition v3.0
# Mayor dificultad | Temporizador | Nuevo flujo de ronda
# ============================================================

import streamlit as st
import streamlit.components.v1
import sqlite3
import hashlib
import random
import re
import time

st.set_page_config(
    page_title="Ciudad en Equilibrio",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── ESTILOS NEÓN GAMING FUTURISTA ─────────────────────────────

# ─── CONSTANTES ─────────────────────────────────────────────────
VALOR_INICIAL    = 50
VALOR_MINIMO     = 0
TOTAL_RONDAS     = 10
COOLDOWN         = 3
MIN_EST          = 3
MAX_EST          = 5
REGEX_NOMBRE     = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$"
TIEMPO_PREGUNTA  = 30

# ─── NIVELES DE DIFICULTAD ───────────────────────────────────────
DIFICULTADES = {
    "Fácil":   {"mult_neg": 0.5,  "mult_pos": 1.2, "evento_neg_prob": 0.25, "icon": "🟢", "desc": "Penalizaciones reducidas al 50%"},
    "Medio":   {"mult_neg": 1.0,  "mult_pos": 1.0, "evento_neg_prob": 0.45, "icon": "🟡", "desc": "Reglas estándar del juego"},
    "Difícil": {"mult_neg": 1.6,  "mult_pos": 0.8, "evento_neg_prob": 0.65, "icon": "🔴", "desc": "Errores y eventos más devastadores"},
}

# ─── LOGROS ──────────────────────────────────────────────────────
LOGROS = {
    "admin_eficiente":  {"icon":"🏆","nombre":"Administrador Eficiente","desc":"Todos los indicadores sobre 60"},
    "ciudad_verde":     {"icon":"🌿","nombre":"Ciudad Verde",           "desc":"Medio ambiente sobre 80"},
    "energia_sost":     {"icon":"⚡","nombre":"Energía Sostenible",      "desc":"Energía alta 3 rondas seguidas"},
    "economia_boom":    {"icon":"💰","nombre":"Economía en Auge",        "desc":"Economía sobre 75"},
    "ciudad_feliz":     {"icon":"😊","nombre":"Ciudad Feliz",           "desc":"Bienestar Social sobre 80"},
    "superviviente":    {"icon":"🛡️","nombre":"Superviviente",          "desc":"Completar 10 rondas sin ningún indicador en crítico"},
    "maestro_preguntas":{"icon":"🧠","nombre":"Maestro de Preguntas",    "desc":"8 o más respuestas correctas"},
    "equilibrio_total": {"icon":"⚖️","nombre":"Equilibrio Total",        "desc":"Promedio de indicadores ≥ 70 al final"},
}

# ─── DECISIONES ──────────────────────────────────────────────────
DECISIONES = {
    "Construir fábrica":        {"emoji":"🏭","economia":18,"medio_ambiente":-15,"energia":-8,"bienestar_social":-3},
    "Crear parque natural":     {"emoji":"🌳","economia":-8,"medio_ambiente":18,"energia":-3,"bienestar_social":12},
    "Instalar paneles solares": {"emoji":"☀️","economia":-12,"medio_ambiente":12,"energia":22,"bienestar_social":-2},
    "Construir escuelas":       {"emoji":"🏫","economia":-12,"medio_ambiente":-2,"energia":-6,"bienestar_social":22},
    "Ampliar autopistas":       {"emoji":"🛣️","economia":12,"medio_ambiente":-18,"energia":-12,"bienestar_social":-5},
    "Agricultura urbana":       {"emoji":"🌾","economia":6,"medio_ambiente":12,"energia":4,"bienestar_social":10},
    "Mejorar hospitales":       {"emoji":"🏥","economia":-18,"medio_ambiente":-2,"energia":-6,"bienestar_social":28},
    "Planta de carbón":         {"emoji":"⚫","economia":22,"medio_ambiente":-25,"energia":28,"bienestar_social":-10},
}

# ─── EVENTOS NORMALES ────────────────────────────────────────────
EVENTOS = [
    {"nombre":"🌩️ Tormenta devastadora",    "efectos":{"medio_ambiente":-14}},
    {"nombre":"🤒 Pandemia regional",        "efectos":{"bienestar_social":-16,"economia":-8}},
    {"nombre":"🔌 Apagón masivo",            "efectos":{"energia":-14,"economia":-6}},
    {"nombre":"📉 Recesión económica",       "efectos":{"economia":-14,"bienestar_social":-6}},
    {"nombre":"🔥 Incendio forestal grave",  "efectos":{"medio_ambiente":-18,"bienestar_social":-5}},
    {"nombre":"💧 Sequía prolongada",        "efectos":{"medio_ambiente":-12,"energia":-8}},
    {"nombre":"💣 Crisis industrial",        "efectos":{"economia":-12,"medio_ambiente":-10}},
    {"nombre":"🌊 Inundación urbana",        "efectos":{"bienestar_social":-13,"energia":-8}},
    {"nombre":"⚡ Fallo de infraestructura", "efectos":{"energia":-16,"economia":-5}},
    {"nombre":"😷 Brote de enfermedad",      "efectos":{"bienestar_social":-12,"economia":-6}},
    {"nombre":"💰 Boom económico",           "efectos":{"economia":10,"bienestar_social":5}},
    {"nombre":"⚡ Ahorro energético",        "efectos":{"energia":9}},
    {"nombre":"🌽 Gran cosecha",             "efectos":{"medio_ambiente":8,"bienestar_social":6}},
    {"nombre":"🎉 Festival cultural",        "efectos":{"bienestar_social":10,"economia":4}},
    {"nombre":"🌍 Inversión extranjera",     "efectos":{"economia":12,"bienestar_social":4}},
    {"nombre":"🎓 Beca educativa masiva",    "efectos":{"bienestar_social":9,"economia":-4}},
    {"nombre":"🌬️ Energía renovable bonus", "efectos":{"energia":8,"medio_ambiente":5}},
    {"nombre":"🏗️ Protestas sociales",      "efectos":{"bienestar_social":-13,"economia":-8}},
    {"nombre":"🌱 Programa ambiental",       "efectos":{"medio_ambiente":15,"bienestar_social":4}},
]

# ─── EVENTOS ÉPICOS (rondas 7-10) ────────────────────────────────
EVENTOS_EPICOS = [
    {"nombre":"🚀 REVOLUCIÓN TECNOLÓGICA", "efectos":{"economia":20,"energia":18,"bienestar_social":10}},
    {"nombre":"💎 MEGA INVERSIÓN INTERNACIONAL","efectos":{"economia":25,"bienestar_social":12}},
    {"nombre":"🔋 DESCUBRIMIENTO ENERGÍA LIMPIA","efectos":{"energia":25,"medio_ambiente":18}},
    {"nombre":"🌍 CUMBRE AMBIENTAL MUNDIAL","efectos":{"medio_ambiente":22,"bienestar_social":14}},
    {"nombre":"☄️ CRISIS CLIMÁTICA GLOBAL","efectos":{"medio_ambiente":-25,"energia":-15,"bienestar_social":-12}},
    {"nombre":"💸 COLAPSO FINANCIERO MUNDIAL","efectos":{"economia":-25,"bienestar_social":-15}},
]

# ─── PREGUNTAS ───────────────────────────────────────────────────
PREGUNTAS = [
    {"cat":"Python","q":"¿Resultado de type(3.14)?","ops":["<class 'int'>","<class 'float'>","<class 'str'>","<class 'double'>"],"ok":1},
    {"cat":"Python","q":"¿Que hace len()?","ops":["Convierte a entero","Retorna la longitud","Imprime en pantalla","Crea una lista"],"ok":1},
    {"cat":"Python","q":"¿Como se define una funcion?","ops":["function f():","def f():","func f():","define f():"],"ok":1},
    {"cat":"Python","q":"¿Resultado de 2 ** 3?","ops":["6","8","9","5"],"ok":1},
    {"cat":"Python","q":"¿Tipo de dato de True?","ops":["int","str","bool","float"],"ok":2},
    {"cat":"Python","q":"¿Division entera en Python?","ops":["/","%","//","div"],"ok":2},
    {"cat":"Python","q":"¿Salida de print('Hi'*2)?","ops":["HiHi","Hi2","Error","Hi Hi"],"ok":0},
    {"cat":"Python","q":"¿Agregar elemento al final de lista?","ops":["lst.add(x)","lst.append(x)","lst.insert(x)","lst.push(x)"],"ok":1},
    {"cat":"Python","q":"¿Que devuelve range(3)?","ops":["[1,2,3]","[0,1,2,3]","[0,1,2]","[1,2]"],"ok":2},
    {"cat":"Python","q":"¿Resultado de 10 % 3?","ops":["3","1","0","2"],"ok":1},
    {"cat":"Python","q":"¿Que hace input()?","ops":["Imprime","Lee del usuario","Importa","Crea variables"],"ok":1},
    {"cat":"Python","q":"¿Estructura para recorrer lista?","ops":["foreach","for ... in ...","loop","while each"],"ok":1},
    {"cat":"PSeInt","q":"¿Como declarar variable en PSeInt?","ops":["var x <- 5","Definir x como Entero","int x = 5","x = 5"],"ok":1},
    {"cat":"PSeInt","q":"¿Instruccion para mostrar en PSeInt?","ops":["print()","Mostrar","Escribir","Display"],"ok":2},
    {"cat":"PSeInt","q":"¿Como inicia un algoritmo en PSeInt?","ops":["Start","Algoritmo Nombre","Begin","def main():"],"ok":1},
    {"cat":"PSeInt","q":"¿Instruccion para leer en PSeInt?","ops":["Leer","Input","Capturar","Ingresar"],"ok":0},
    {"cat":"PSeInt","q":"¿Como se escribe SI en PSeInt?","ops":["if(c)then","Si(c)Entonces","when(c)","check(c)"],"ok":1},
    {"cat":"PSeInt","q":"¿Operador de asignacion en PSeInt?","ops":["=","==","<-",":="],"ok":2},
    {"cat":"PSeInt","q":"¿Como inicia ciclo MIENTRAS en PSeInt?","ops":["while(c)do","Mientras(c)Hacer","loop(c)","repetir(c)"],"ok":1},
    {"cat":"PSeInt","q":"¿Palabra que cierra SI-ENTONCES?","ops":["End","FinSi","EndIf","Cerrar"],"ok":1},
    {"cat":"PSeInt","q":"¿Variable tipo real en PSeInt?","ops":["Definir x como Real","float x","real x","var x:real"],"ok":0},
    {"cat":"PSeInt","q":"¿Ciclo FOR en PSeInt?","ops":["for i=1 to 10","Para i<-1 Hasta 10 Hacer","loop i","repeat i"],"ok":1},
    {"cat":"Calculo","q":"Integral de x dx?","ops":["x+C","x^2+C","x^2/2+C","2x+C"],"ok":2},
    {"cat":"Calculo","q":"Integral de e^x dx?","ops":["e^x+C","xe^x+C","e^(x+1)+C","ln(x)+C"],"ok":0},
    {"cat":"Calculo","q":"Integral de cos(x) dx?","ops":["-sin(x)+C","sin(x)+C","-cos(x)+C","tan(x)+C"],"ok":1},
    {"cat":"Calculo","q":"Integral de (1/x) dx?","ops":["x^2+C","ln|x|+C","1/x^2+C","-1/x^2+C"],"ok":1},
    {"cat":"Calculo","q":"Integral de sin(x) dx?","ops":["cos(x)+C","-cos(x)+C","sin(x)+C","tan(x)+C"],"ok":1},
    {"cat":"Calculo","q":"Integral de 3x^2 dx?","ops":["x^3+C","6x+C","3x+C","x^3/3+C"],"ok":0},
    {"cat":"Calculo","q":"¿Que representa la integral definida geometricamente?","ops":["Pendiente","Area bajo la curva","Derivada","Volumen"],"ok":1},
    {"cat":"Calculo","q":"Integral de 0 dx?","ops":["0","C","x+C","1"],"ok":1},
    {"cat":"Calculo","q":"Integral de x^n dx (n≠-1)?","ops":["n*x^(n-1)+C","x^(n+1)/(n+1)+C","x^n/n+C","n*x^n+C"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de x^2?","ops":["x","2x","x^2","2"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de e^x?","ops":["x*e^(x-1)","e^x","e^(x+1)","ln(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de sin(x)?","ops":["-sin(x)","cos(x)","-cos(x)","tan(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de ln(x)?","ops":["e^x","1/x","x*ln(x)","log(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de una constante k?","ops":["k","1","0","k-1"],"ok":2},
    {"cat":"Derivadas","q":"Derivada de cos(x)?","ops":["sin(x)","-sin(x)","cos(x)","tan(x)"],"ok":1},
    {"cat":"Derivadas","q":"Regla de la cadena: d/dx[f(g(x))]?","ops":["f'(x)g(x)","f'(g(x))g'(x)","f(x)g'(x)","f'(x)+g'(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de x^3 - 4x + 2?","ops":["3x-4","3x^2-4","x^2-4","3x^2+2"],"ok":1},
    {"cat":"Fisica MRU","q":"En MRU ¿que tipo de velocidad tiene el objeto?","ops":["Acelerada","Constante","Nula","Variable"],"ok":1},
    {"cat":"Fisica MRU","q":"Formula del MRU:","ops":["d=v*t","d=v^2/2a","v=a*t","F=m*a"],"ok":0},
    {"cat":"Fisica MRU","q":"Auto recorre 120km en 2h. ¿Velocidad?","ops":["50km/h","60km/h","70km/h","80km/h"],"ok":1},
    {"cat":"Fisica MRU","q":"En MRU la aceleracion es:","ops":["Maxima","Creciente","Cero","Variable"],"ok":2},
    {"cat":"Fisica MRU","q":"Pendiente en grafica posicion-tiempo de MRU representa:","ops":["Aceleracion","Fuerza","Velocidad","Masa"],"ok":2},
    {"cat":"Fisica MRU","q":"v=10m/s, t=5s ¿cuanto recorre?","ops":["2m","15m","50m","100m"],"ok":2},
    {"cat":"Fisica MRU","q":"Grafica v-t de MRU:","ops":["Curva ascendente","Horizontal","Vertical","Diagonal"],"ok":1},
    {"cat":"Fisica MRUA","q":"¿Que caracteriza al MRUA?","ops":["Velocidad cte","Aceleracion cte","Aceleracion nula","Posicion fija"],"ok":1},
    {"cat":"Fisica MRUA","q":"v=v0+a*t corresponde a:","ops":["MRU","Caida libre","MRUA","MCU"],"ok":2},
    {"cat":"Fisica MRUA","q":"Reposo, a=3m/s^2. ¿Tiempo para 15m/s?","ops":["3s","4s","5s","6s"],"ok":2},
    {"cat":"Fisica MRUA","q":"Area bajo v-t en MRUA representa:","ops":["Aceleracion","Fuerza","Desplazamiento","Potencia"],"ok":2},
    {"cat":"Fisica MRUA","q":"d=v0*t+(1/2)*a*t^2 es:","ops":["Velocidad final","Desplazamiento MRUA","Fuerza neta","Energia"],"ok":1},
    {"cat":"Fisica MRUA","q":"Si a=0, MRUA se convierte en:","ops":["Caida libre","MCU","MRU","Reposo"],"ok":2},
    {"cat":"Fisica MRUA","q":"v^2=v0^2+2*a*d es la ecuacion de:","ops":["Energia","Velocidad sin tiempo","Posicion","Impulso"],"ok":1},
    {"cat":"Matrices","q":"¿Que es una matriz cuadrada?","ops":["Mas filas que col","Filas=columnas","Solo una fila","Elementos iguales"],"ok":1},
    {"cat":"Matrices","q":"A=[1,2], B=[3,4], A+B=?","ops":["[4,6]","[3,8]","[2,4]","[1,6]"],"ok":0},
    {"cat":"Matrices","q":"La transpuesta intercambia:","ops":["Filas por columnas","Sumas por restas","Signos","Diagonales"],"ok":0},
    {"cat":"Matrices","q":"Condicion para multiplicar A x B:","ops":["Ambas cuadradas","Col(A)=Fil(B)","Fil(A)=Fil(B)","A=B"],"ok":1},
    {"cat":"Matrices","q":"¿Que es la matriz identidad?","ops":["Matriz ceros","Unos en diagonal","Triangular","Nula"],"ok":1},
    {"cat":"Matrices","q":"Si det(A)=0, A es:","ops":["Invertible","Singular","Identidad","Ortogonal"],"ok":1},
    {"cat":"Matrices","q":"Dimension de producto 2x3 por 3x4:","ops":["3x3","2x4","3x4","2x3"],"ok":1},
    {"cat":"Matrices","q":"Matriz triangular superior tiene:","ops":["Todo cero","Ceros debajo diagonal","Ceros encima diagonal","Solo diagonal"],"ok":1},
    {"cat":"Matrices","q":"Traza de una matriz es:","ops":["Determinante","Suma diagonal principal","Mayor elemento","Transpuesta"],"ok":1},
    {"cat":"Matrices","q":"det([[1,2],[3,4]])=?","ops":["10","-2","2","-10"],"ok":1},
]

# ─── BASE DE DATOS ───────────────────────────────────────────────
import os as _os

def _get_db_path():
    for d in ["/tmp", _os.path.expanduser("~"), _os.getcwd()]:
        try:
            t = _os.path.join(d, "_tw.tmp")
            open(t,"w").close(); _os.remove(t)
            return _os.path.join(d, "database.db")
        except Exception:
            continue
    return "database.db"

DB_PATH = _get_db_path()

def get_conn():
    """Conexión con reintentos automáticos si la DB está bloqueada."""
    for intento in range(8):
        try:
            conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=20)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.OperationalError:
            time.sleep(0.3 * (intento + 1))
    # último intento sin capturar
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=60)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=8000")
    return conn

def inicializar_db():
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE IF NOT EXISTS grupos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_grupo TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS estudiantes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id INTEGER NOT NULL,
            nombre_estudiante TEXT NOT NULL,
            FOREIGN KEY(grupo_id) REFERENCES grupos(id))""")
        c.execute("""CREATE TABLE IF NOT EXISTS progreso_juego(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grupo_id INTEGER UNIQUE NOT NULL,
            economia INTEGER DEFAULT 50,
            medio_ambiente INTEGER DEFAULT 50,
            energia INTEGER DEFAULT 50,
            bienestar_social INTEGER DEFAULT 50,
            ronda_actual INTEGER DEFAULT 1,
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
        conn.commit()
    finally:
        conn.close()

def hp(p): return hashlib.sha256(p.encode()).hexdigest()

def registrar_grupo(nombre, pw):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("INSERT INTO grupos(nombre_grupo,password) VALUES(?,?)",(nombre.strip(),hp(pw)))
        conn.commit()
        gid = c.lastrowid
        return True, gid
    except sqlite3.IntegrityError:
        return False, None
    finally:
        conn.close()

def login_grupo(nombre, pw):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("SELECT id FROM grupos WHERE nombre_grupo=? AND password=?",(nombre.strip(),hp(pw)))
        row = c.fetchone()
        return row["id"] if row else None
    finally:
        conn.close()

def guardar_estudiante(gid, nombre):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("INSERT INTO estudiantes(grupo_id,nombre_estudiante) VALUES(?,?)",(gid,nombre.strip()))
        conn.commit()
    finally:
        conn.close()

def obtener_estudiantes(gid):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("SELECT nombre_estudiante FROM estudiantes WHERE grupo_id=? ORDER BY id",(gid,))
        rows = c.fetchall()
        return [r["nombre_estudiante"] for r in rows]
    finally:
        conn.close()

def obtener_progreso(gid):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("SELECT * FROM progreso_juego WHERE grupo_id=?",(gid,))
        row = c.fetchone()
        if not row:
            c.execute("INSERT INTO progreso_juego(grupo_id,economia,medio_ambiente,energia,bienestar_social,ronda_actual) VALUES(?,50,50,50,50,1)",(gid,))
            conn.commit()
            c.execute("SELECT * FROM progreso_juego WHERE grupo_id=?",(gid,))
            row = c.fetchone()
        return dict(row)
    finally:
        conn.close()

def actualizar_progreso(gid, eco, amb, ene, bie, ronda):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("UPDATE progreso_juego SET economia=?,medio_ambiente=?,energia=?,bienestar_social=?,ronda_actual=? WHERE grupo_id=?",(eco,amb,ene,bie,ronda,gid))
        conn.commit()
    finally:
        conn.close()

def reiniciar_progreso(gid):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("UPDATE progreso_juego SET economia=50,medio_ambiente=50,energia=50,bienestar_social=50,ronda_actual=1 WHERE grupo_id=?",(gid,))
        c.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=?",(gid,))
        conn.commit()
    finally:
        conn.close()

def obtener_cooldowns(gid):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("SELECT decision,rondas_restantes FROM cooldown_decisiones WHERE grupo_id=?",(gid,))
        rows = c.fetchall()
        return {r["decision"]: r["rondas_restantes"] for r in rows}
    finally:
        conn.close()

def actualizar_cooldown(gid, decision, ronda_usada):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("DELETE FROM cooldown_decisiones WHERE grupo_id=? AND decision=?",(gid,decision))
        disponible_en = ronda_usada + COOLDOWN
        c.execute("INSERT INTO cooldown_decisiones(grupo_id,decision,rondas_restantes) VALUES(?,?,?)",
                  (gid, decision, disponible_en))
        conn.commit()
    finally:
        conn.close()

def cooldown_disponible(ronda_actual, disponible_en):
    """True si la decision ya puede usarse."""
    return ronda_actual >= disponible_en

def decrementar_cooldowns(gid):
    # Ahora los cooldowns usan ronda absoluta, esta funcion no hace nada
    pass

def nombre_grupo_por_id(gid):
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("SELECT nombre_grupo FROM grupos WHERE id=?",(gid,))
        row = c.fetchone()
        return row["nombre_grupo"] if row else "Desconocido"
    finally:
        conn.close()

# ─── SESSION STATE ───────────────────────────────────────────────
def guardar_ranking(gid, nombre, puntaje, correctas, incorrectas, dificultad, logros):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO ranking(grupo_id,nombre_grupo,puntaje,correctas,"
            "incorrectas,dificultad,logros) VALUES(?,?,?,?,?,?,?)",
            (gid, nombre, puntaje, correctas, incorrectas, dificultad,
             ",".join(logros) if logros else ""))
        conn.commit()
    finally:
        conn.close()

def obtener_ranking():
    conn = get_conn()
    try:
        c = conn.cursor()
        c.execute("SELECT nombre_grupo,puntaje,correctas,dificultad,logros,fecha "
                  "FROM ranking ORDER BY puntaje DESC LIMIT 10")
        return [dict(r) for r in c.fetchall()]
    finally:
        conn.close()

def calcular_logros(ind, stats):
    ganados = []
    vals = [ind.get("economia",0), ind.get("medio_ambiente",0),
            ind.get("energia",0),  ind.get("bienestar_social",0)]
    prom = sum(vals) / 4 if vals else 0
    if all(v >= 60 for v in vals):           ganados.append("admin_eficiente")
    if ind.get("medio_ambiente",0) >= 80:    ganados.append("ciudad_verde")
    if ind.get("energia",0) >= 60:           ganados.append("energia_sost")
    if ind.get("economia",0) >= 75:          ganados.append("economia_boom")
    if ind.get("bienestar_social",0) >= 80:  ganados.append("ciudad_feliz")
    if stats.get("ninguno_critico", True):   ganados.append("superviviente")
    if stats.get("correctas", 0) >= 8:       ganados.append("maestro_preguntas")
    if prom >= 70:                           ganados.append("equilibrio_total")
    return ganados

def calcular_puntaje(ind, correctas, incorrectas, logros, dificultad):
    vals = [ind.get("economia",0), ind.get("medio_ambiente",0),
            ind.get("energia",0),  ind.get("bienestar_social",0)]
    prom = sum(vals) / 4 if vals else 0
    mult = {"Fácil": 0.8, "Medio": 1.0, "Difícil": 1.3}.get(dificultad, 1.0)
    base = int(prom * mult)
    return max(0, base + correctas * 5 - incorrectas * 3 + len(logros) * 10)

def inyectar_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Exo+2:wght@300;400;600;700;800&family=Rajdhani:wght@400;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Exo 2', sans-serif; }

/* ══ FONDO: grid digital + partículas ══ */
.stApp {
    background-color: #050a14;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px),
        radial-gradient(ellipse at 15% 40%, rgba(59,130,246,0.08) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 20%, rgba(139,92,246,0.09) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 90%, rgba(6,182,212,0.06) 0%, transparent 50%);
    background-size: 40px 40px, 40px 40px, 100% 100%, 100% 100%, 100% 100%;
    min-height: 100vh;
}

#MainMenu, header, footer { visibility: hidden; }
.block-container {
    padding-top: 1rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;
    max-width: 1500px !important;
}

/* ══ TARJETAS ══ */
.card {
    background: rgba(5,10,20,0.9);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    backdrop-filter: blur(16px);
    position: relative;
    overflow: hidden;
    transition: border-color .3s, box-shadow .3s;
}
.card::before {
    content:''; position:absolute; inset:0; border-radius:12px;
    background: linear-gradient(135deg, rgba(0,212,255,0.04), transparent 60%);
    pointer-events:none;
}
.card:hover {
    border-color: rgba(0,212,255,0.45);
    box-shadow: 0 0 28px rgba(0,212,255,0.1), inset 0 1px 0 rgba(0,212,255,0.08);
}

.card-glow {
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.12));
    border: 1px solid rgba(139,92,246,0.5);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    box-shadow: 0 0 30px rgba(139,92,246,0.15), inset 0 1px 0 rgba(255,255,255,0.04);
    animation: fadeInUp .4s ease;
    position: relative; overflow: hidden;
}

.card-danger {
    background: rgba(239,68,68,0.07);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    box-shadow: 0 0 20px rgba(239,68,68,0.08);
}
.card-success {
    background: rgba(34,197,94,0.07);
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 12px;
    padding: clamp(14px,2.5vw,20px);
    margin-bottom: 12px;
    box-shadow: 0 0 20px rgba(34,197,94,0.08);
}

/* ══ TÍTULO PRINCIPAL ══ */
.game-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(1.5rem, 5vw, 3rem);
    font-weight: 900;
    background: linear-gradient(90deg, #00d4ff, #8b5cf6, #22c55e, #00d4ff);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    line-height: 1.15;
    animation: shimmer 4s linear infinite;
    filter: drop-shadow(0 0 20px rgba(0,212,255,0.4));
    letter-spacing: 2px;
}
.game-sub {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(0.65rem, 1.8vw, 0.88rem);
    color: rgba(0,212,255,0.5);
    text-align: center;
    letter-spacing: clamp(3px, 0.8vw, 6px);
    text-transform: uppercase;
    margin-bottom: 2rem;
}
@keyframes shimmer {
    0%   { background-position: 0% center; }
    100% { background-position: 300% center; }
}

/* ══ BOTONES NEÓN ══ */
div.stButton > button {
    font-family: 'Exo 2', sans-serif !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: clamp(0.8rem, 2vw, 0.92rem) !important;
    padding: clamp(0.5rem,1.5vw,0.7rem) clamp(0.8rem,2vw,1.4rem) !important;
    transition: all 0.22s ease !important;
    border: 1px solid rgba(0,212,255,0.35) !important;
    background: rgba(5,10,20,0.95) !important;
    color: #94d8e8 !important;
    width: 100% !important;
    white-space: normal !important;
    position: relative !important;
    overflow: hidden !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}
div.stButton > button::after {
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.15), transparent);
    transition: left 0.5s ease;
}
div.stButton > button:hover:not(:disabled)::after { left: 150%; }
div.stButton > button:hover:not(:disabled) {
    background: rgba(0,212,255,0.1) !important;
    border-color: #00d4ff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 24px rgba(0,212,255,0.3), 0 0 8px rgba(0,212,255,0.2) inset !important;
    color: #fff !important;
}
div.stButton > button:active:not(:disabled) {
    transform: translateY(0px) scale(0.97) !important;
    box-shadow: 0 0 40px rgba(0,212,255,0.4) !important;
}
div.stButton > button:disabled {
    opacity: 0.2 !important;
    cursor: not-allowed !important;
}

/* ══ INPUTS ══ */
div[data-baseweb="base-input"] > input,
div[data-baseweb="input"] > div {
    background: rgba(5,10,20,0.95) !important;
    border-color: rgba(0,212,255,0.25) !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Exo 2', sans-serif !important;
}
div[data-baseweb="base-input"] > input:focus {
    border-color: rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.1), 0 0 16px rgba(0,212,255,0.15) !important;
}

/* ══ RADIO BUTTONS ══ */
div[data-testid="stRadio"] > div { gap: 6px !important; }
div[data-testid="stRadio"] label {
    background: rgba(5,10,20,0.9);
    border: 1.5px solid rgba(0,212,255,0.18);
    border-radius: 8px;
    padding: clamp(10px,2vw,13px) clamp(12px,3vw,16px);
    margin: 0 !important;
    display: flex !important;
    cursor: pointer;
    transition: all 0.18s;
    color: #94d8e8;
    font-size: clamp(0.85rem, 2vw, 0.95rem);
    align-items: center; gap: 10px;
    font-family: 'Exo 2', sans-serif;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(0,212,255,0.08);
    border-color: rgba(0,212,255,0.5);
    transform: translateX(4px);
    box-shadow: 0 0 16px rgba(0,212,255,0.15), -3px 0 0 #00d4ff;
    color: #fff;
}

/* ══ MÉTRICAS ══ */
div[data-testid="metric-container"] {
    background: rgba(5,10,20,0.92);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 10px;
    padding: clamp(10px,2vw,14px) clamp(12px,2.5vw,18px);
    text-align: center;
    box-shadow: 0 0 20px rgba(0,212,255,0.06);
}
div[data-testid="metric-container"] label {
    color: rgba(0,212,255,0.6) !important;
    font-size: clamp(0.55rem,1.3vw,0.68rem) !important;
    text-transform: uppercase; letter-spacing: 2px;
    font-family: 'Orbitron', sans-serif !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-size: clamp(0.9rem,2.5vw,1.3rem) !important;
    font-weight: 800 !important;
    font-family: 'Orbitron', sans-serif !important;
}

/* ══ PROGRESS BAR ══ */
div[data-testid="stProgressBar"] > div {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 4px !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #00d4ff, #8b5cf6) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 12px rgba(0,212,255,0.5) !important;
    transition: width .6s ease !important;
}

/* ══ ALERTS ══ */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: 'Exo 2', sans-serif !important;
    border-left-width: 3px !important;
}

/* ══ EXPANDER ══ */
details {
    background: rgba(5,10,20,0.9) !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 8px !important;
}
details summary { color: #94d8e8 !important; font-family: 'Exo 2', sans-serif !important; }

/* ══ TEXTO ══ */
hr { border-color: rgba(0,212,255,0.1) !important; margin: 1rem 0 !important; }
p, li, .stMarkdown p {
    color: #94a3b8 !important;
    font-size: clamp(0.85rem,2vw,0.95rem) !important;
    font-family: 'Exo 2', sans-serif !important;
}
h1, h2, h3 { color: #e2e8f0 !important; font-family: 'Exo 2', sans-serif !important; }
h3 { font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important; }

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(5,10,20,0.5); }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.4); border-radius: 2px; }

/* ══ ANIMACIONES ══ */
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(16px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
@keyframes pulse-neon {
    0%,100% { box-shadow: 0 0 4px rgba(0,212,255,0.4); }
    50%      { box-shadow: 0 0 16px rgba(0,212,255,0.8), 0 0 30px rgba(0,212,255,0.3); }
}
.pulse { animation: pulse-neon 2s infinite; }

/* ══ EMOJI FIX ══ */
.emoji-title {
    font-family: 'Apple Color Emoji','Segoe UI Emoji','Noto Color Emoji',sans-serif !important;
    -webkit-text-fill-color: initial !important;
    filter: none !important;
    display: inline-block;
}

/* ══════════════════════════════════
   RESPONSIVE — MULTI-DISPOSITIVO
   ══════════════════════════════════ */

/* ── Tablet (≤ 900px) ── */
@media (max-width: 900px) {
    .block-container {
        padding-left: .8rem !important;
        padding-right: .8rem !important;
    }
    /* Botones más grandes para touch */
    div.stButton > button {
        padding: .65rem 1rem !important;
        font-size: .9rem !important;
    }
    /* Texto base más legible */
    p, li, .stMarkdown p {
        font-size: .95rem !important;
        line-height: 1.6 !important;
    }
    /* Métricas más compactas */
    div[data-testid="metric-container"] {
        padding: 10px 12px !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
    }
    /* Game title más pequeño */
    .game-title { font-size: clamp(1.1rem,4vw,2rem) !important; }
}

/* ── Móvil (≤ 640px) ── */
@media (max-width: 640px) {
    .block-container {
        padding-left: .4rem !important;
        padding-right: .4rem !important;
        padding-top: .6rem !important;
    }

    /* Forzar columnas Streamlit a stack vertical */
    div[data-testid="column"] {
        min-width: 100% !important;
        width: 100% !important;
    }

    /* Botones grandes para dedo */
    div.stButton > button {
        padding: .8rem 1rem !important;
        font-size: .88rem !important;
        min-height: 48px !important;
        touch-action: manipulation !important;
    }

    /* Inputs más altos para touch */
    div[data-baseweb="base-input"] > input {
        min-height: 48px !important;
        font-size: 1rem !important;
        padding: .6rem .9rem !important;
    }

    /* Radio options más grandes */
    div[data-testid="stRadio"] label {
        padding: 14px 14px !important;
        font-size: .9rem !important;
        min-height: 50px !important;
    }

    /* Cards con menos padding */
    .card, .card-glow, .card-danger, .card-success {
        padding: 12px !important;
        border-radius: 10px !important;
    }

    /* Título */
    .game-title {
        font-size: clamp(1rem,7vw,1.6rem) !important;
        letter-spacing: 1px !important;
    }
    .game-sub {
        font-size: .65rem !important;
        letter-spacing: 2px !important;
    }

    /* Texto legible */
    p, li, .stMarkdown p {
        font-size: .9rem !important;
        line-height: 1.65 !important;
    }
    h3 { font-size: .95rem !important; }

    /* Métricas compactas */
    div[data-testid="metric-container"] {
        padding: 8px 10px !important;
    }
    div[data-testid="metric-container"] label {
        font-size: .5rem !important;
        letter-spacing: 1px !important;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: .9rem !important;
    }

    /* Expander más cómodo */
    details summary { padding: 10px !important; font-size: .88rem !important; }

    /* Separadores */
    hr { margin: .6rem 0 !important; }
}

/* ── Pantalla grande (≥ 1280px) ── */
@media (min-width: 1280px) {
    .block-container { max-width: 1500px !important; }
    .game-title { font-size: 2.8rem !important; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

def init_session():
    d = {
        "pantalla":"inicio","grupo_id":None,"grupo_nombre":"",
        "grupo_id_registro":None,"estudiantes_temp":[],"msg_est":"",
        "pregunta_actual":None,"respuesta_correcta":False,
        "decision_elegida":None,"decision_efectos":None,
        "evento_ronda":None,"fase_ronda":"decision",
        "preguntas_usadas":[],"resultado":None,
        "indicadores_finales":{},"rondas_completadas":0,
        "timer_inicio":None,"tiempo_agotado":False,
    }
    for k,v in d.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ─── UTILIDADES ──────────────────────────────────────────────────
def navegar(p):
    st.session_state["pantalla"] = p
    st.rerun()

IND_COLOR = {"economia":("#fbbf24","💰"),"medio_ambiente":("#34d399","🌿"),
             "energia":("#60a5fa","⚡"),"bienestar_social":("#f472b6","🏥")}
IND_LABEL = {"economia":"Economia","medio_ambiente":"Medio Amb.",
             "energia":"Energia","bienestar_social":"Bienestar"}
CAT_COLOR = {"Python":"#6366f1","PSeInt":"#8b5cf6","Calculo":"#06b6d4",
             "Derivadas":"#10b981","Fisica MRU":"#f59e0b",
             "Fisica MRUA":"#ef4444","Matrices":"#ec4899"}

def barra_indicador(nombre, valor, emoji):
    valor = max(0, min(100, valor))
    if valor > 60:   color,badge,glow = "#22c55e","● ESTABLE","rgba(34,197,94,0.2)"
    elif valor > 30: color,badge,glow = "#f59e0b","● PRECAUCIÓN","rgba(245,158,11,0.18)"
    else:            color,badge,glow = "#ef4444","● CRÍTICO","rgba(239,68,68,0.2)"
    bg = ("rgba(34,197,94,0.05)" if valor>60 else "rgba(245,158,11,0.05)" if valor>30 else "rgba(239,68,68,0.06)")
    st.markdown(
        "<div style='background:"+bg+";border:1px solid "+color+"44;"
        "border-radius:10px;padding:12px 16px;margin-bottom:10px;"
        "box-shadow:0 0 18px "+glow+",inset 0 1px 0 rgba(255,255,255,0.03);"
        "transition:box-shadow .3s;position:relative;overflow:hidden;'>"
        "<div style='position:absolute;top:0;left:0;width:3px;height:100%;"
        "background:"+color+";box-shadow:0 0 8px "+color+";'></div>"
        "<div style='padding-left:8px;'>"
        "<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>"
        "<span style='font-weight:700;color:#e2e8f0;font-size:0.88rem;"
        "font-family:Exo 2,sans-serif;display:flex;align-items:center;gap:6px;'>"
        "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>"+emoji+"</span>"
        "<span>"+nombre+"</span></span>"
        "<span style='font-size:0.62rem;color:"+color+";font-weight:800;"
        "font-family:Orbitron,sans-serif;letter-spacing:1px;'>"+badge+"</span>"
        "</div>"
        "<div style='background:rgba(255,255,255,0.06);border-radius:3px;height:8px;overflow:hidden;margin-bottom:6px;'>"
        "<div style='width:"+str(valor)+"%;background:linear-gradient(90deg,"+color+"66,"+color+");"
        "height:8px;border-radius:3px;box-shadow:0 0 8px "+color+";'></div>"
        "</div>"
        "<div style='display:flex;justify-content:space-between;align-items:center;'>"
        "<span style='font-size:0.68rem;color:rgba(255,255,255,0.2);font-family:Orbitron,sans-serif;'>0</span>"
        "<span style='font-size:0.88rem;font-weight:900;color:"+color+";"
        "font-family:Orbitron,sans-serif;text-shadow:0 0 8px "+color+";'>"+str(valor)+"</span>"
        "<span style='font-size:0.68rem;color:rgba(255,255,255,0.2);font-family:Orbitron,sans-serif;'>100</span>"
        "</div>"
        "</div></div>", unsafe_allow_html=True)
def seleccionar_pregunta():
    disp = [i for i in range(len(PREGUNTAS)) if i not in st.session_state["preguntas_usadas"]]
    if not disp:
        st.session_state["preguntas_usadas"] = []
        disp = list(range(len(PREGUNTAS)))
    idx = random.choice(disp)
    st.session_state["preguntas_usadas"].append(idx)
    return PREGUNTAS[idx]

def aplicar_efectos(ind, ef):
    r = dict(ind)
    for k,v in ef.items():
        if k in r:
            r[k] = max(0, min(100, r[k]+v))
    return r

def cabecera_juego(nombre_grp, estudiantes, ronda, est_turno):
    pct = int(((ronda-1)/TOTAL_RONDAS)*100)
    fase_label = st.session_state.get("fase_ronda","decision")
    fases_txt  = {"decision":"DECIDIR","pregunta":"PREGUNTA","evento":"EVENTO","resultado_pregunta":"RESULTADO"}
    fase_txt   = fases_txt.get(fase_label, fase_label.upper())

    left, mid, right = st.columns([2.5, 4, 2.5])

    with left:
        # Nombre del grupo
        st.markdown(
            "<div style='background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.25);"
            "border-radius:10px;padding:10px 14px;margin-bottom:8px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;color:rgba(0,212,255,0.5);"
            "letter-spacing:2px;margin-bottom:4px;'>SMART CITY CONTROL</div>"
            "<div style='display:flex;align-items:center;gap:8px;'>"
            "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;font-size:1.3rem;'>🏙️</span>"
            "<span style='font-family:Orbitron,sans-serif;font-weight:900;font-size:clamp(0.85rem,2vw,1.1rem);"
            "background:linear-gradient(90deg,#00d4ff,#8b5cf6);-webkit-background-clip:text;"
            "-webkit-text-fill-color:transparent;background-clip:text;'>"+nombre_grp+"</span>"
            "</div></div>", unsafe_allow_html=True)
        # Lista de estudiantes
        chips = "".join([
            "<span style='background:"+(
                "rgba(0,212,255,0.18)" if e==est_turno else "rgba(255,255,255,0.04)"
            )+";border:1px solid "+(
                "rgba(0,212,255,0.6)" if e==est_turno else "rgba(255,255,255,0.07)"
            )+";border-radius:6px;padding:3px 10px;margin:2px;font-size:0.78rem;"
            "color:"+(
                "#00d4ff" if e==est_turno else "#64748b"
            )+";display:inline-block;font-family:Exo 2,sans-serif;"
            "box-shadow:"+(
                "0 0 8px rgba(0,212,255,0.25)" if e==est_turno else "none"
            )+";'>"
            +("▶ " if e==est_turno else "")+e+"</span>"
            for e in estudiantes])
        st.markdown("<div style='line-height:1.8;'>"+chips+"</div>", unsafe_allow_html=True)

    with mid:
        # Contador de ronda futurista
        st.markdown(
            "<div style='background:rgba(5,10,20,0.9);border:1px solid rgba(0,212,255,0.2);"
            "border-radius:10px;padding:10px 16px;text-align:center;margin-bottom:8px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;color:rgba(0,212,255,0.5);"
            "letter-spacing:3px;margin-bottom:6px;'>RONDA ACTUAL</div>"
            "<div style='display:flex;align-items:center;justify-content:center;gap:8px;'>"
            # Segmentos de ronda
            +"".join([
                "<div style='width:clamp(18px,2.5vw,26px);height:6px;border-radius:2px;"
                "background:"+("linear-gradient(90deg,#00d4ff,#8b5cf6)" if i<ronda-1 else
                               ("rgba(0,212,255,0.5)" if i==ronda-1 else "rgba(255,255,255,0.07)"))+
                ";box-shadow:"+("0 0 8px rgba(0,212,255,0.5)" if i<ronda else "none")+";'></div>"
                for i in range(TOTAL_RONDAS)
            ])+
            "</div>"
            "<div style='font-family:Orbitron,sans-serif;font-size:clamp(1rem,3vw,1.5rem);"
            "font-weight:900;color:#00d4ff;margin-top:6px;text-shadow:0 0 16px rgba(0,212,255,0.6);'>"
            +str(ronda)+" <span style='color:rgba(255,255,255,0.3);font-size:0.6em;'>/ "+str(TOTAL_RONDAS)+"</span>"
            "</div>"
            "</div>", unsafe_allow_html=True)
        # Barra de progreso
        st.markdown(
            "<div style='background:rgba(255,255,255,0.05);border-radius:3px;height:4px;overflow:hidden;'>"
            "<div style='width:"+str(pct)+"%;background:linear-gradient(90deg,#00d4ff,#8b5cf6,#22c55e);"
            "height:4px;border-radius:3px;box-shadow:0 0 10px rgba(0,212,255,0.6);"
            "transition:width .8s ease;'></div></div>", unsafe_allow_html=True)

    with right:
        # Fase actual + turno + menú
        st.markdown(
            "<div style='background:rgba(5,10,20,0.9);border:1px solid rgba(139,92,246,0.3);"
            "border-radius:10px;padding:10px 14px;margin-bottom:8px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;color:rgba(139,92,246,0.7);"
            "letter-spacing:2px;margin-bottom:4px;'>FASE</div>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.95rem;font-weight:700;"
            "color:#8b5cf6;text-shadow:0 0 12px rgba(139,92,246,0.5);'>"+fase_txt+"</div>"
            "<hr style='border-color:rgba(139,92,246,0.15);margin:6px 0;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;color:rgba(0,212,255,0.5);"
            "letter-spacing:2px;margin-bottom:2px;'>OPERADOR</div>"
            "<div style='font-size:0.85rem;color:#e2e8f0;font-weight:600;'>🎓 "+est_turno+"</div>"
            "</div>", unsafe_allow_html=True)
        with st.expander("⚙️ Menú"):
            if st.button("🏠 Volver al inicio", use_container_width=True):
                navegar("inicio")

    st.markdown("<hr style='border-color:rgba(0,212,255,0.08);margin:4px 0 10px;'>",
                unsafe_allow_html=True)
# ─── PANTALLAS ───────────────────────────────────────────────────

def pantalla_inicio():
    # ── Núcleo holográfico animado + título ──
    st.markdown(
        "<div style='text-align:center;padding:40px 0 20px;'>"
        "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,Noto Color Emoji,sans-serif;"
        "font-size:clamp(2.5rem,8vw,4rem);line-height:1;margin-bottom:12px;'>🏙️</div>"
        "<div style='font-family:Orbitron,sans-serif;"
        "font-size:clamp(1.4rem,5vw,2.8rem);font-weight:900;"
        "background:linear-gradient(90deg,#00d4ff,#8b5cf6,#22c55e,#00d4ff);"
        "background-size:300%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
        "background-clip:text;animation:shimmer 4s linear infinite;"
        "letter-spacing:4px;margin-bottom:6px;'>CIUDAD EN EQUILIBRIO</div>"
        "<div style='font-family:Rajdhani,sans-serif;font-size:.8rem;"
        "color:rgba(255,255,255,0.3);letter-spacing:4px;'>SIMULADOR DE PENSAMIENTO SISTÉMICO</div>"
        "</div>",
        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Selector de dificultad ──
    st.markdown(
        "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
        "color:rgba(0,212,255,0.5);letter-spacing:3px;text-align:center;"
        "margin-bottom:8px;'>NIVEL DE DIFICULTAD</div>", unsafe_allow_html=True)
    d1,d2,d3 = st.columns(3)
    dif_actual = st.session_state.get("dificultad","Medio")
    for col_d, (dif_key, dif_val) in zip([d1,d2,d3], DIFICULTADES.items()):
        with col_d:
            selected = dif_actual == dif_key
            border   = "rgba(0,212,255,0.7)" if selected else "rgba(255,255,255,0.1)"
            bg       = "rgba(0,212,255,0.12)" if selected else "rgba(5,10,20,0.8)"
            glow     = "0 0 16px rgba(0,212,255,0.25)" if selected else "none"
            st.markdown(
                "<div style='background:"+bg+";border:1.5px solid "+border+";"
                "border-radius:10px;padding:10px;text-align:center;"
                "box-shadow:"+glow+";cursor:pointer;'>"
                "<div style='font-size:1.3rem;'>"+dif_val["icon"]+"</div>"
                "<div style='font-family:Orbitron,sans-serif;font-size:0.7rem;"
                "color:"+("#00d4ff" if selected else "#94a3b8")+";font-weight:700;"
                "margin:4px 0 2px;'>"+dif_key.upper()+"</div>"
                "<div style='font-size:0.65rem;color:rgba(255,255,255,0.3);'>"
                +dif_val["desc"]+"</div></div>", unsafe_allow_html=True)
            if st.button(("✅ " if selected else "")+"Seleccionar",
                         key="dif_"+dif_key, use_container_width=True):
                st.session_state["dificultad"] = dif_key
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Botones de menú ──
    b1,b2,b3,b4 = st.columns(4)
    with b1:
        if st.button("🔐  INICIAR SESIÓN", use_container_width=True): navegar("login")
    with b2:
        if st.button("📝  REGISTRAR GRUPO", use_container_width=True): navegar("registro")
    with b3:
        if st.button("📖  INSTRUCCIONES", use_container_width=True): navegar("instrucciones")
    with b4:
        if st.button("🏆  RANKING", use_container_width=True): navegar("ranking")
def pantalla_instrucciones():
    st.markdown("<div style='text-align:center;'><span class='emoji-title' style='font-size:2rem;'>📖</span></div><div class='game-title' style='font-size:1.8rem;'>Instrucciones</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='card'>
<h3 style='color:#a78bfa;margin-top:0;'>🎯 Objetivo</h3>
<p>Administrar la ciudad durante <b>10 rondas</b>. El juego siempre completa las 10 rondas.</p>
<h3 style='color:#60a5fa;'>📊 Indicadores (inician en 50)</h3>
<p>💰 Economia &nbsp;|&nbsp; 🌿 Medio Ambiente<br>⚡ Energia &nbsp;|&nbsp; 🏥 Bienestar Social</p>
<h3 style='color:#f59e0b;'>⏱️ Temporizador</h3>
<p>Cada pregunta tiene <b>30 segundos</b>. Si se acaba el tiempo, se cuenta como respuesta incorrecta automaticamente.</p>
</div>""",unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='card-glow'>
<h3 style='color:#34d399;margin-top:0;'>🔄 Mecanica de Rondas</h3>
<ol style='padding-left:18px;'>
<li>Se selecciona el <b>estudiante en turno</b></li>
<li>El grupo <b>elige una decision estrategica</b></li>
<li>El estudiante responde una <b>pregunta de opcion multiple</b></li>
<li>✅ Acierta → se aplican los puntos de la decision</li>
<li>❌ Falla → <b>todos pierden 10 pts</b> (20 en rondas pares)</li>
<li>Ocurre un <b>evento aleatorio</b></li>
</ol>
</div>
<div class='card-danger'>
<h3 style='color:#f87171;margin-top:0;'>⚠️ Dificultad</h3>
<p>Los eventos negativos son <b>mas frecuentes y severos</b>. Las decisiones tienen <b>mayor impacto</b> positivo y negativo. Mantener el equilibrio es un verdadero reto.</p>
</div>""",unsafe_allow_html=True)
    if st.button("⬅️  Volver al Inicio"): navegar("inicio")


def pantalla_registro():
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown(
            "<div style='text-align:center;padding:6px 0 2px;'>"
            "<span class='emoji-title' style='font-size:2.2rem;'>📝</span></div>"
            "<div class='game-title' style='font-size:1.5rem;letter-spacing:3px;'>REGISTRAR GRUPO</div>"
            "<div class='game-sub' style='font-size:.7rem;'>NUEVO EQUIPO DE CONTROL</div>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Info: el grupo se registra al finalizar con estudiantes
        st.markdown(
            "<div style='background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.18);"
            "border-radius:8px;padding:10px 14px;margin-bottom:14px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:2px;margin-bottom:4px;'>PROCESO</div>"
            "<div style='color:#94a3b8;font-size:0.82rem;line-height:1.6;'>"
            "1️⃣ Define el nombre y contraseña del grupo<br>"
            "2️⃣ Agrega entre <b style='color:#00d4ff;'>"+str(MIN_EST)+"</b> y "
            "<b style='color:#00d4ff;'>"+str(MAX_EST)+"</b> operadores<br>"
            "3️⃣ El grupo se crea solo al finalizar con el mínimo requerido"
            "</div></div>", unsafe_allow_html=True)

        with st.form("form_reg"):
            nombre = st.text_input("👥 Nombre del grupo", placeholder="Ej: Equipo Titan",
                                   value=st.session_state.get("reg_nombre_temp",""))
            pw     = st.text_input("🔒 Contraseña", type="password")
            pw2    = st.text_input("🔒 Confirmar contraseña", type="password")
            sub    = st.form_submit_button("SIGUIENTE → AGREGAR OPERADORES",
                                           use_container_width=True)
        if sub:
            nombre = nombre.strip()
            if not nombre:
                st.error("⚠️ El nombre del grupo es requerido.")
            elif len(pw) < 4:
                st.error("⚠️ La contraseña debe tener mínimo 4 caracteres.")
            elif pw != pw2:
                st.error("⚠️ Las contraseñas no coinciden.")
            else:
                # Solo guardar en session_state — NO escribir en DB todavía
                st.session_state["reg_nombre_temp"]   = nombre
                st.session_state["reg_pw_temp"]       = pw
                st.session_state["grupo_id_registro"] = None  # aún no existe en DB
                st.session_state["estudiantes_temp"]  = []
                navegar("agregar_estudiantes")

        if st.button("⬅️ VOLVER", use_container_width=True, key="btn_volver_reg"):
            navegar("inicio")


def pantalla_agregar_estudiantes():
    # El grupo aún no está en DB — verificar que se pasó por pantalla_registro
    if not st.session_state.get("reg_nombre_temp"):
        navegar("inicio"); return
    gid = None  # se asignará al finalizar

    # Nombre del grupo viene de session_state (aún no está en DB)
    nombre_grupo = st.session_state.get("reg_nombre_temp", "Nuevo Grupo")
    _,col,_ = st.columns([0.5,3,0.5])
    with col:
        # Título
        st.markdown(
            "<div style='text-align:center;padding:6px 0 2px;'>"
            "<span class='emoji-title' style='font-size:2.2rem;'>👨‍🎓</span></div>"
            "<div class='game-title' style='font-size:1.5rem;letter-spacing:3px;'>AGREGAR OPERADORES</div>"
            "<div class='game-sub' style='font-size:.7rem;'>EQUIPO DE INGENIERÍA</div>",
            unsafe_allow_html=True)

        # Info del grupo
        st.markdown(
            "<div style='background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);"
            "border-radius:8px;padding:8px 14px;text-align:center;margin-bottom:14px;'>"
            "<span style='color:rgba(0,212,255,0.5);font-size:0.72rem;font-family:Orbitron,sans-serif;"
            "letter-spacing:2px;'>GRUPO: </span>"
            "<span style='color:#00d4ff;font-weight:700;font-family:Orbitron,sans-serif;'>"
            +nombre_grupo+"</span></div>", unsafe_allow_html=True)

        estudiantes = st.session_state.get("estudiantes_temp", [])
        n = len(estudiantes)

        # Barra de progreso
        pct_est = int(n / MAX_EST * 100)
        st.markdown(
            "<div style='display:flex;justify-content:space-between;"
            "align-items:center;margin-bottom:6px;'>"
            "<span style='font-family:Orbitron,sans-serif;font-size:0.6rem;"
            "color:rgba(0,212,255,0.5);letter-spacing:2px;'>OPERADORES</span>"
            "<span style='font-family:Orbitron,sans-serif;font-size:0.75rem;"
            "color:#00d4ff;font-weight:700;'>"+str(n)+" / "+str(MAX_EST)+"</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,0.06);border-radius:3px;"
            "height:6px;overflow:hidden;margin-bottom:14px;'>"
            "<div style='width:"+str(pct_est)+"%;height:6px;border-radius:3px;"
            "background:linear-gradient(90deg,#00d4ff,#8b5cf6);"
            "box-shadow:0 0 8px rgba(0,212,255,0.5);transition:width .4s;'></div>"
            "</div>", unsafe_allow_html=True)

        # Input + botón (sin st.form para evitar bugs de estado)
        if n < MAX_EST:
            nombre_est = st.text_input(
                "👤 Nombre completo del operador",
                placeholder="Ej: Ana López",
                key="input_est_nombre")

            if st.button("➕ AGREGAR OPERADOR", use_container_width=True, key="btn_agregar"):
                nombre_est = nombre_est.strip()
                if not nombre_est:
                    st.error("⚠️ El nombre no puede estar vacío.")
                elif not re.match(REGEX_NOMBRE, nombre_est):
                    st.error("⚠️ Solo se permiten letras y espacios.")
                elif nombre_est.lower() in [e.lower() for e in estudiantes]:
                    st.error("⚠️ Ya existe un operador con ese nombre.")
                else:
                    st.session_state["estudiantes_temp"].append(nombre_est)
                    st.session_state["msg_est"] = "✅ " + nombre_est + " agregado al equipo."
                    st.rerun()
        else:
            st.markdown(
                "<div style='background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.3);"
                "border-radius:8px;padding:10px;text-align:center;margin-bottom:10px;'>"
                "<span style='color:#22c55e;font-family:Orbitron,sans-serif;font-size:0.75rem;'>"
                "✅ EQUIPO COMPLETO ("+str(MAX_EST)+" operadores)</span></div>",
                unsafe_allow_html=True)

        # Mensaje de éxito
        if st.session_state.get("msg_est"):
            st.success(st.session_state["msg_est"])
            st.session_state["msg_est"] = ""

        # Lista de estudiantes agregados
        if estudiantes:
            st.markdown(
                "<div style='font-family:Orbitron,sans-serif;font-size:0.62rem;"
                "color:rgba(0,212,255,0.5);letter-spacing:2px;margin:10px 0 8px;'>"
                "EQUIPO ACTUAL</div>", unsafe_allow_html=True)
            for idx_e, est in enumerate(list(estudiantes)):
                cn, cb = st.columns([5, 1])
                with cn:
                    st.markdown(
                        "<div style='background:rgba(0,212,255,0.05);"
                        "border:1px solid rgba(0,212,255,0.18);border-radius:8px;"
                        "padding:8px 14px;margin-bottom:4px;display:flex;align-items:center;gap:8px;'>"
                        "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>👤</span>"
                        "<span style='color:#e2e8f0;font-size:0.9rem;'>"+est+"</span>"
                        "<span style='margin-left:auto;font-family:Orbitron,sans-serif;"
                        "font-size:0.6rem;color:rgba(0,212,255,0.4);'>#"+str(idx_e+1)+"</span>"
                        "</div>", unsafe_allow_html=True)
                with cb:
                    if st.button("✕", key="del_"+str(idx_e)+"_"+est,
                                 use_container_width=True):
                        st.session_state["estudiantes_temp"].remove(est)
                        st.rerun()

        # Requisito mínimo
        st.markdown("<br>", unsafe_allow_html=True)
        puede = n >= MIN_EST

        if not puede:
            faltantes = MIN_EST - n
            st.markdown(
                "<div style='background:rgba(245,158,11,0.08);"
                "border:1px solid rgba(245,158,11,0.3);border-radius:8px;"
                "padding:10px 14px;text-align:center;margin-bottom:10px;'>"
                "<span style='font-family:Orbitron,sans-serif;font-size:0.7rem;"
                "color:#f59e0b;'>⚠️ FALTAN "+str(faltantes)+" OPERADOR"
                +("ES" if faltantes>1 else "")+" MÍNIMO</span></div>",
                unsafe_allow_html=True)

        ca, cb = st.columns(2)
        with ca:
            if st.button("⬅️ CANCELAR", use_container_width=True, key="btn_cancel_est"):
                st.session_state["estudiantes_temp"] = []
                navegar("inicio")
        with cb:
            if st.button(
                "🚀 INICIAR MISIÓN" if puede else "🔒 MÍNIMO "+str(MIN_EST)+" OPERADORES",
                disabled=not puede,
                use_container_width=True,
                key="btn_finalizar_est"
            ):
                # Registrar el grupo en DB solo ahora que tiene los estudiantes mínimos
                nombre_reg = st.session_state.get("reg_nombre_temp","")
                pw_reg     = st.session_state.get("reg_pw_temp","")
                ok, new_gid = registrar_grupo(nombre_reg, pw_reg)
                if not ok:
                    st.error("⚠️ Ya existe un grupo con ese nombre. Vuelve y elige otro.")
                else:
                    for est in estudiantes:
                        guardar_estudiante(new_gid, est)
                    obtener_progreso(new_gid)
                    st.session_state["grupo_id"]          = new_gid
                    st.session_state["grupo_nombre"]      = nombre_reg
                    st.session_state["grupo_id_registro"] = None
                    st.session_state["estudiantes_temp"]  = []
                    st.session_state["reg_nombre_temp"]   = ""
                    st.session_state["reg_pw_temp"]       = ""
                    st.session_state["fase_ronda"]        = "decision"
                    navegar("juego")

def pantalla_login():
    _,col,_ = st.columns([1,2,1])
    with col:
        st.markdown("<div style='text-align:center;'><span class='emoji-title' style='font-size:1.8rem;'>🔐</span></div><div class='game-title' style='font-size:1.6rem;'>Iniciar Sesion</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        with st.form("form_login"):
            nombre = st.text_input("👥 Nombre del grupo")
            pw     = st.text_input("🔒 Contrasena", type="password")
            sub    = st.form_submit_button("Entrar 🚀", use_container_width=True)
        if sub:
            gid = login_grupo(nombre, pw)
            if gid:
                st.session_state["grupo_id"]     = gid
                st.session_state["grupo_nombre"] = nombre.strip()
                st.session_state["fase_ronda"]   = "decision"
                navegar("juego")
            else: st.error("Credenciales incorrectas.")
        if st.button("⬅️ Volver", use_container_width=True): navegar("inicio")


def pantalla_juego():
    gid = st.session_state.get("grupo_id")
    if not gid: navegar("inicio"); return

    progreso    = obtener_progreso(gid)
    estudiantes = obtener_estudiantes(gid)
    cooldowns   = obtener_cooldowns(gid)
    ronda       = progreso["ronda_actual"]
    nombre_grp  = st.session_state["grupo_nombre"]

    # Guardia: si no hay estudiantes redirigir al inicio
    if not estudiantes:
        st.error("⚠️ No se encontraron estudiantes para este grupo. Regresa e inicia sesión nuevamente.")
        if st.button("🏠 Volver al inicio"):
            navegar("inicio")
        return

    idx_turno   = (ronda - 1) % len(estudiantes)
    est_turno   = estudiantes[idx_turno]

    ind = {"economia":progreso["economia"],"medio_ambiente":progreso["medio_ambiente"],
           "energia":progreso["energia"],"bienestar_social":progreso["bienestar_social"]}

    # Fin de juego: solo por rondas completadas
    if ronda > TOTAL_RONDAS:
        st.session_state.update({"resultado":"victoria","indicadores_finales":ind,"rondas_completadas":TOTAL_RONDAS})
        navegar("fin"); return

    cabecera_juego(nombre_grp, estudiantes, ronda, est_turno)

    # Indicadores responsivos: 4 cols en desktop, 2 en tablet, 1 en móvil
    st.markdown("""
<style>
.ind-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-bottom:10px; }
@media(max-width:900px){ .ind-grid { grid-template-columns:repeat(2,1fr); } }
@media(max-width:640px){ .ind-grid { grid-template-columns:1fr; } }
</style>""", unsafe_allow_html=True)
    ci1,ci2,ci3,ci4 = st.columns(4)
    with ci1: barra_indicador("Economía",        ind["economia"],        "💰")
    with ci2: barra_indicador("Medio Ambiente",  ind["medio_ambiente"],  "🌿")
    with ci3: barra_indicador("Energía",         ind["energia"],         "⚡")
    with ci4: barra_indicador("Bienestar Social",ind["bienestar_social"], "🏥")
    st.markdown("<hr style='border-color:rgba(0,212,255,0.08);margin:4px 0 10px;'>",
                unsafe_allow_html=True)

    fase = st.session_state.get("fase_ronda","decision")

    # ══════════════════════════════════════════════
    # FASE 1: ELEGIR DECISION
    # ══════════════════════════════════════════════
    if fase == "decision":
        st.markdown("### 🗳️ Paso 1 — Elige una Decision Estrategica")
        st.markdown("<p style='color:rgba(255,255,255,0.45);font-size:0.85rem;margin-top:-8px;'>Si aciertas la pregunta, los efectos de esta decision se aplicaran a la ciudad.</p>",unsafe_allow_html=True)

        cols = st.columns(4)
        for i,(nom_dec,ef) in enumerate(DECISIONES.items()):
            col_card     = cols[i%4]
            disponible_en = cooldowns.get(nom_dec, 0)
            disp          = (disponible_en == 0) or (ronda >= disponible_en)
            rondas_falta  = max(0, disponible_en - ronda) if disponible_en > 0 else 0

            # Efectos de la decisión
            filas_ef = ""
            for k,v in ef.items():
                if k=="emoji": continue
                col_ind,em_ind = IND_COLOR.get(k,("#94a3b8","•"))
                signo   = "+" if v>0 else ""
                col_val = "#22c55e" if v>0 else "#ef4444"
                filas_ef += (
                    "<div style='display:flex;justify-content:space-between;"
                    "align-items:center;padding:3px 0;"
                    "border-bottom:1px solid rgba(255,255,255,0.04);'>"
                    "<span style='color:"+col_ind+";font-size:0.74rem;'>"
                    "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>"+em_ind+"</span>"
                    " "+IND_LABEL[k]+"</span>"
                    "<span style='color:"+col_val+";font-size:0.82rem;font-weight:700;'>"+signo+str(v)+"</span>"
                    "</div>")

            dec_emoji_raw = ef.get("emoji","")

            if disp:
                borde   = "rgba(59,130,246,0.5)"
                bg_card = "rgba(59,130,246,0.07)"
                opac    = "1"
                btn_txt = "✅ Elegir decisión"
                cd_html = ""
                glow    = "0 0 20px rgba(59,130,246,0.12)"
            else:
                borde   = "rgba(245,158,11,0.4)"
                bg_card = "rgba(245,158,11,0.05)"
                opac    = "0.6"
                btn_txt = "🔒 En cooldown"
                glow    = "none"
                # Puntos de rondas restantes
                puntos_html = "".join([
                    "<span style='display:inline-block;width:9px;height:9px;"
                    "border-radius:50%;background:"
                    +("'#fbbf24'" if j < rondas_falta else "'rgba(255,255,255,0.15)'")+
                    ";margin:2px;box-shadow:"+(
                        "'0 0 6px #fbbf24'" if j < rondas_falta else "none"
                    )+";'></span>"
                    for j in range(COOLDOWN)
                ])
                disp_en_ronda = disponible_en
                cd_pct = int((COOLDOWN - rondas_falta) / COOLDOWN * 100)
                cd_html = (
                    "<div style='background:rgba(245,158,11,0.1);"
                    "border:1px solid rgba(245,158,11,0.3);"
                    "border-radius:10px;padding:8px 10px;margin-top:8px;text-align:center;'>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:0.58rem;"
                    "color:#fbbf24;letter-spacing:1px;margin-bottom:5px;'>🔒 COOLDOWN</div>"
                    "<div style='display:flex;justify-content:center;gap:5px;margin-bottom:5px;'>"
                    +puntos_html+
                    "</div>"
                    "<div style='height:4px;background:rgba(255,255,255,.08);"
                    "border-radius:2px;overflow:hidden;margin-bottom:5px;'>"
                    "<div style='width:"+str(cd_pct)+"%;height:4px;background:#fbbf24;"
                    "border-radius:2px;box-shadow:0 0 6px #fbbf24;'></div></div>"
                    "<div style='font-size:0.7rem;color:#fbbf24;font-weight:700;'>"
                    +str(rondas_falta)+" ronda"+("s" if rondas_falta!=1 else "")+" · disponible en R"+str(disp_en_ronda)
                    +"</div></div>")

            with col_card:
                st.markdown(
                    "<div style='background:"+bg_card+";border:1px solid "+borde+";"
                    "border-radius:14px;padding:14px;opacity:"+opac+";"
                    "box-shadow:"+glow+";min-height:220px;'>"
                    "<div style='text-align:center;margin-bottom:8px;'>"
                    "<span style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                    "font-size:1.8rem;'>"+dec_emoji_raw+"</span></div>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:0.7rem;"
                    "color:#e2e8f0;font-weight:700;text-align:center;margin-bottom:8px;'>"
                    +nom_dec+"</div>"
                    "<div style='border-top:1px solid rgba(255,255,255,0.06);padding-top:8px;'>"
                    +filas_ef+"</div>"
                    +cd_html+
                    "</div>", unsafe_allow_html=True)
                if st.button(btn_txt, key="dec_"+str(i),
                             disabled=not disp, use_container_width=True):
                    st.session_state["decision_elegida"]  = nom_dec
                    st.session_state["decision_efectos"]  = {k:v for k,v in ef.items() if k!="emoji"}
                    st.session_state["pregunta_actual"]   = seleccionar_pregunta()
                    st.session_state["timer_inicio"]      = None
                    st.session_state["tiempo_agotado"]    = False
                    st.session_state["fase_ronda"]        = "pregunta"
                    st.rerun()

    # ══════════════════════════════════════════════
    # FASE 2: PREGUNTA CON TEMPORIZADOR AUTOMÁTICO
    # ══════════════════════════════════════════════
    elif fase == "pregunta":
        pregunta = st.session_state["pregunta_actual"]
        nom_dec  = st.session_state["decision_elegida"]
        ef_dec   = st.session_state["decision_efectos"]

        if st.session_state.get("timer_inicio") is None:
            st.session_state["timer_inicio"] = time.time()

        tiempo_restante = max(0.0, TIEMPO_PREGUNTA - (time.time() - st.session_state["timer_inicio"]))
        seg = int(tiempo_restante)

        # Timeout automático
        if tiempo_restante <= 0:
            st.session_state["tiempo_agotado"]     = True
            st.session_state["respuesta_correcta"] = False
            st.session_state["fase_ronda"]         = "resultado_pregunta"
            st.session_state["incorrectas"]        = st.session_state.get("incorrectas",0) + 1
            st.rerun()

        # Chip de decisión elegida
        ef_resumen = "  ".join([IND_COLOR[k][1]+" "+("+"+str(v) if v>0 else str(v))
                                 for k,v in ef_dec.items() if k in IND_COLOR])
        dec_emoji = DECISIONES.get(nom_dec,{}).get("emoji","")
        st.markdown(
            "<div style='background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.25);"
            "border-radius:12px;padding:8px 16px;margin-bottom:12px;display:flex;"
            "flex-wrap:wrap;gap:6px;align-items:center;'>"
            "<span style='color:#a78bfa;font-size:0.8rem;'>Decisión:</span>"
            "<span style='color:#f1f5f9;font-weight:700;font-size:.88rem;'>"+dec_emoji+" "+nom_dec+"</span>"
            "<span style='color:rgba(255,255,255,0.3);font-size:0.76rem;'>"+ef_resumen+"</span>"
            "</div>", unsafe_allow_html=True)

        # Colores del timer
        cat_color = CAT_COLOR.get(pregunta["cat"],"#94a3b8")
        q_safe    = pregunta["q"].replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
        cat_safe  = pregunta["cat"]
        pct       = max(0, int(seg / TIEMPO_PREGUNTA * 100))
        if seg > TIEMPO_PREGUNTA * 0.5:    tcol = "#10b981"
        elif seg > TIEMPO_PREGUNTA * 0.25: tcol = "#f59e0b"
        else:                              tcol = "#ef4444"
        urgente = ("<div style='color:#ef4444;font-size:.72rem;font-weight:700;"
                   "margin-top:5px;text-align:center;letter-spacing:1px;'>⚠️ ¡RESPONDE YA!</div>"
                   if seg <= 8 else "")

        left_col, right_col = st.columns([1, 2])
        with left_col:
            st.markdown(
                "<div style='background:rgba(0,0,0,0.5);border:3px solid "+tcol+";"
                "border-radius:16px;padding:16px;text-align:center;"
                "box-shadow:0 0 30px "+tcol+"55;'>"
                "<div style='font-size:.65rem;color:rgba(255,255,255,.4);"
                "font-family:Orbitron,sans-serif;letter-spacing:2px;margin-bottom:4px;'>⏱️ TIEMPO</div>"
                "<div style='font-size:3.5rem;font-weight:900;color:"+tcol+";"
                "text-shadow:0 0 20px "+tcol+";font-variant-numeric:tabular-nums;line-height:1;'>"
                +str(seg)+"</div>"
                "<div style='font-size:.7rem;color:rgba(255,255,255,.35);margin-top:2px;'>segundos</div>"
                "<div style='height:8px;background:rgba(255,255,255,.08);border-radius:4px;"
                "margin-top:10px;overflow:hidden;'>"
                "<div style='width:"+str(pct)+"%;height:8px;border-radius:4px;"
                "background:linear-gradient(90deg,"+tcol+"88,"+tcol+");"
                "box-shadow:0 0 10px "+tcol+";'></div></div>"
                +urgente+"</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown(
                "<div style='background:rgba(8,12,30,.9);border:1px solid "+cat_color+"55;"
                "border-radius:14px;padding:16px;box-shadow:0 0 20px "+cat_color+"14;'>"
                "<div style='background:"+cat_color+"22;color:"+cat_color+";"
                "border:1px solid "+cat_color+"44;border-radius:20px;"
                "padding:3px 14px;font-size:.7rem;font-weight:600;"
                "display:inline-block;margin-bottom:10px;'>"+cat_safe+"</div>"
                "<p style='color:#f1f5f9;font-size:1.05rem;font-weight:600;"
                "line-height:1.6;margin:0;'>"+q_safe+"</p>"
                "</div>", unsafe_allow_html=True)

        st.markdown(
            "<div style='font-family:Orbitron,sans-serif;font-size:.6rem;"
            "color:rgba(0,212,255,.5);letter-spacing:2px;margin:12px 0 8px;'>"
            "SELECCIONA TU RESPUESTA</div>", unsafe_allow_html=True)

        cols_op = st.columns(2)
        respondio = False
        for idx_op, op_texto in enumerate(pregunta["ops"]):
            letra = chr(65 + idx_op)
            with cols_op[idx_op % 2]:
                if st.button(f"{letra})  {op_texto}", key=f"op_{idx_op}",
                             use_container_width=True):
                    es_correcta = (idx_op == pregunta["ok"])
                    st.session_state["respuesta_correcta"] = es_correcta
                    st.session_state["tiempo_agotado"]     = False
                    st.session_state["fase_ronda"]         = "resultado_pregunta"
                    if es_correcta:
                        st.session_state["correctas"]   = st.session_state.get("correctas",0) + 1
                    else:
                        st.session_state["incorrectas"] = st.session_state.get("incorrectas",0) + 1
                    respondio = True
                    st.rerun()

        # ── Auto-refresh 1s para actualizar el reloj automáticamente ──
        if not respondio:
            time.sleep(1)
            st.rerun()

    # ══════════════════════════════════════════════
    # FASE 3: RESULTADO DE PREGUNTA
    # ══════════════════════════════════════════════
    elif fase == "resultado_pregunta":
        correcto    = st.session_state.get("respuesta_correcta", False)
        timeout     = st.session_state.get("tiempo_agotado", False)
        nom_dec     = st.session_state.get("decision_elegida","")
        ef_dec      = st.session_state.get("decision_efectos",{})
        pregunta    = st.session_state.get("pregunta_actual",{})

        if correcto:
            col_r,bg_r,ico,tit = "#22c55e","rgba(34,197,94,0.1)","✅","¡Respuesta Correcta!"
            sub = "Los efectos de tu decisión se aplicarán a la ciudad."
        elif timeout:
            col_r,bg_r,ico,tit = "#f59e0b","rgba(245,158,11,0.1)","⏰","¡Tiempo Agotado!"
            sub = "No respondiste a tiempo. La decisión no tendrá efecto."
        else:
            col_r,bg_r,ico,tit = "#ef4444","rgba(239,68,68,0.1)","❌","Respuesta Incorrecta"
            sub = "La decisión no tendrá efecto esta ronda."

        resp_correcta_txt = pregunta.get("ops",[""])[pregunta.get("ok",0)] if pregunta else ""

        st.markdown(
            "<div style='background:"+bg_r+";border:2px solid "+col_r+"44;"
            "border-radius:16px;padding:28px;text-align:center;margin-bottom:20px;'>"
            "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
            "font-size:3rem;line-height:1;'>"+ico+"</div>"
            "<h2 style='color:"+col_r+";margin:10px 0 6px;font-family:Orbitron,sans-serif;"
            "font-size:1.3rem;'>"+tit+"</h2>"
            "<p style='color:rgba(255,255,255,0.5);margin:0 0 10px;font-size:.9rem;'>"+sub+"</p>"
            +(  "<div style='background:rgba(255,255,255,0.05);border-radius:8px;"
                "padding:8px 16px;display:inline-block;font-size:.85rem;'>"
                "<span style='color:rgba(255,255,255,.4);'>Respuesta correcta: </span>"
                "<span style='color:#22c55e;font-weight:700;'>"+resp_correcta_txt+"</span></div>"
                if not correcto else "")
            +"</div>", unsafe_allow_html=True)

        progreso_r = obtener_progreso(gid)
        ind_r = {k: progreso_r[k] for k in ["economia","medio_ambiente","energia","bienestar_social"]}

        if correcto:
            nueva_ind_r = aplicar_efectos(ind_r, ef_dec)
            actualizar_cooldown(gid, nom_dec, ronda)
            st.markdown("**Efectos aplicados:**")
            ef_cols = st.columns(4)
            for ci,(k,v) in enumerate(ef_dec.items()):
                if k in IND_COLOR:
                    cc,ei = IND_COLOR[k]
                    sg = "+" if v>0 else ""
                    cv = "#22c55e" if v>0 else "#ef4444"
                    with ef_cols[ci % 4]:
                        st.markdown(
                            "<div style='background:rgba(5,10,20,.8);border:1px solid "+cc+"33;"
                            "border-radius:8px;padding:8px;text-align:center;'>"
                            "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                            "font-size:1.3rem;'>"+ei+"</div>"
                            "<div style='font-size:.7rem;color:"+cc+";'>"+IND_LABEL[k]+"</div>"
                            "<div style='font-size:1rem;font-weight:900;color:"+cv+";'>"+sg+str(v)+"</div>"
                            "</div>", unsafe_allow_html=True)
        else:
            nueva_ind_r = ind_r

        # Verificar fin del juego
        vals_r = list(nueva_ind_r.values())
        juego_terminado = ronda >= TOTAL_RONDAS

        st.markdown("<br>", unsafe_allow_html=True)
        btn_lbl = "⚡ Continuar al Evento" if not juego_terminado else "🏁 Ver Resultado Final"
        if st.button(btn_lbl, use_container_width=True, key="btn_continuar_res"):
            if correcto:
                actualizar_progreso(gid, nueva_ind_r["economia"], nueva_ind_r["medio_ambiente"],
                                    nueva_ind_r["energia"], nueva_ind_r["bienestar_social"], ronda)
            if juego_terminado:
                st.session_state["indicadores_finales"]  = nueva_ind_r
                st.session_state["rondas_completadas"]   = ronda
                st.session_state["resultado"]            = "victoria"
                navegar("fin")
            else:
                st.session_state["fase_ronda"] = "evento"
                st.rerun()

    # ══════════════════════════════════════════════
    # FASE 4: EVENTO ALEATORIO
    # ══════════════════════════════════════════════
    elif fase == "evento":
        dificultad = st.session_state.get("dificultad","Medio")
        mult_neg   = DIFICULTADES[dificultad]["mult_neg"]
        mult_pos   = DIFICULTADES[dificultad]["mult_pos"]

        if st.session_state["evento_ronda"] is None:
            if ronda >= 7 and random.random() < 0.35:
                base_ev  = random.choice(EVENTOS_EPICOS).copy()
                es_epico = True
            else:
                neg_pool = [e for e in EVENTOS if any(v<0 for v in e["efectos"].values())]
                pos_pool = [e for e in EVENTOS if all(v>=0 for v in e["efectos"].values())]
                prob_neg = DIFICULTADES[dificultad]["evento_neg_prob"]
                base_ev  = random.choice(neg_pool if random.random()<prob_neg else pos_pool).copy()
                es_epico = False
            efectos_mod = {k: int(v*(mult_neg if v<0 else mult_pos))
                           for k,v in base_ev["efectos"].items()}
            base_ev["efectos"] = efectos_mod
            base_ev["epico"]   = es_epico
            st.session_state["evento_ronda"] = base_ev

        evento   = st.session_state["evento_ronda"]
        efectos  = evento["efectos"]
        es_epico = evento.get("epico", False)
        positivo = sum(efectos.values()) >= 0
        col_ev   = "#22c55e" if positivo else "#ef4444"
        bg_ev    = "rgba(34,197,94,0.08)" if positivo else "rgba(239,68,68,0.08)"
        borde_ev = "rgba(34,197,94,0.45)" if positivo else "rgba(239,68,68,0.45)"
        if es_epico:
            col_ev,bg_ev,borde_ev = "#f59e0b","rgba(245,158,11,0.1)","rgba(245,158,11,0.5)"

        progreso_ev = obtener_progreso(gid)
        ind_ev = {k: progreso_ev[k] for k in ["economia","medio_ambiente","energia","bienestar_social"]}
        nueva_ind_ev = aplicar_efectos(ind_ev, efectos)

        badge_epico = ("<div style='background:#f59e0b;color:#000;font-family:Orbitron,sans-serif;"
                       "font-size:0.6rem;font-weight:900;border-radius:20px;padding:2px 12px;"
                       "display:inline-block;margin-bottom:8px;letter-spacing:2px;'>⚡ EVENTO ÉPICO</div>"
                       if es_epico else "")

        filas_ef = ""
        for k,v in efectos.items():
            ci,ei = IND_COLOR.get(k,("#94a3b8","•"))
            sg = "+" if v>0 else ""
            cv = "#22c55e" if v>0 else "#ef4444"
            antes   = ind_ev.get(k,0)
            despues = nueva_ind_ev.get(k,0)
            filas_ef += (
                "<div style='display:flex;align-items:center;justify-content:center;gap:10px;"
                "background:rgba(255,255,255,0.04);border-radius:8px;padding:6px 14px;"
                "margin:4px auto;max-width:340px;'>"
                "<span style='color:"+ci+";font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                "font-size:1rem;'>"+ei+"</span>"
                "<span style='color:#e2e8f0;font-size:.85rem;'>"+IND_LABEL.get(k,k)+"</span>"
                "<span style='color:rgba(255,255,255,.3);'>"+str(antes)+"</span>"
                "<span style='color:rgba(255,255,255,.2);'>→</span>"
                "<span style='color:"+cv+";font-weight:700;'>"+str(despues)+"</span>"
                "<span style='color:"+cv+";font-size:.8rem;'>("+sg+str(v)+")</span></div>")

        st.markdown(
            "<div style='background:"+bg_ev+";border:2px solid "+borde_ev+";"
            "border-radius:16px;padding:28px;text-align:center;"
            "box-shadow:0 0 40px "+col_ev+"22;'>"
            +badge_epico+
            "<div style='font-size:.72rem;color:rgba(255,255,255,.4);"
            "font-family:Orbitron,sans-serif;letter-spacing:2px;margin-bottom:6px;'>"
            "EVENTO — RONDA "+str(ronda)+"</div>"
            "<h2 style='color:#f1f5f9;margin:0 0 14px;font-size:1.3rem;"
            "font-family:Orbitron,sans-serif;'>"+evento["nombre"]+"</h2>"
            +filas_ef+"</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⏭️ FINALIZAR RONDA "+str(ronda)+" / "+str(TOTAL_RONDAS),
                     use_container_width=True):
            actualizar_progreso(gid, nueva_ind_ev["economia"], nueva_ind_ev["medio_ambiente"],
                                nueva_ind_ev["energia"], nueva_ind_ev["bienestar_social"], ronda+1)
            if any(v <= 20 for v in nueva_ind_ev.values()):
                st.session_state["ninguno_critico"] = False
            decrementar_cooldowns(gid)
            st.session_state.update({
                "pregunta_actual":None,"respuesta_correcta":False,
                "decision_elegida":None,"decision_efectos":None,
                "evento_ronda":None,"fase_ronda":"decision",
                "timer_inicio":None,"tiempo_agotado":False,
            })
            st.rerun()


def pantalla_fin():
    resultado   = st.session_state.get("resultado","victoria")
    ind_fin     = st.session_state.get("indicadores_finales",{})
    rondas_comp = st.session_state.get("rondas_completadas",0)
    correctas   = st.session_state.get("correctas",0)
    incorrectas = st.session_state.get("incorrectas",0)
    dificultad  = st.session_state.get("dificultad","Medio")
    nombre_grp  = st.session_state.get("grupo_nombre","Equipo")
    gid         = st.session_state.get("grupo_id")

    stats  = {"correctas": correctas, "ninguno_critico": st.session_state.get("ninguno_critico",True)}
    logros = calcular_logros(ind_fin, stats)
    puntaje= calcular_puntaje(ind_fin, correctas, incorrectas, logros, dificultad)

    if gid:
        guardar_ranking(gid, nombre_grp, puntaje, correctas, incorrectas, dificultad, logros)

    if resultado == "victoria":
        col_r="#22c55e"; bg_r="rgba(34,197,94,0.08)"; ico="🏆"
        tit="¡CIUDAD EQUILIBRADA!"; sub="El equipo administró la ciudad exitosamente."
        st.balloons()
    else:
        col_r="#ef4444"; bg_r="rgba(239,68,68,0.08)"; ico="💥"
        tit="LA CIUDAD COLAPSÓ"; sub="Un indicador llegó al límite crítico."

    st.markdown(
        "<div style='background:"+bg_r+";border:2px solid "+col_r+"44;"
        "border-radius:16px;padding:30px;text-align:center;margin-bottom:20px;'>"
        "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;font-size:3.5rem;'>"+ico+"</div>"
        "<div style='font-family:Orbitron,sans-serif;font-size:clamp(1.3rem,4vw,2rem);"
        "font-weight:900;color:"+col_r+";margin:10px 0 6px;'>"+tit+"</div>"
        "<div style='color:rgba(255,255,255,.5);font-size:.9rem;margin-bottom:14px;'>"+sub+"</div>"
        "<div style='font-family:Orbitron,sans-serif;font-size:2.2rem;font-weight:900;"
        "color:#f59e0b;text-shadow:0 0 20px rgba(245,158,11,0.6);'>"+str(puntaje)+" PTS</div>"
        "<div style='font-size:.65rem;color:rgba(255,255,255,.3);font-family:Orbitron,sans-serif;"
        "letter-spacing:2px;'>PUNTAJE FINAL — "+dificultad.upper()+"</div>"
        "</div>", unsafe_allow_html=True)

    left, right = st.columns([3,2])
    with left:
        st.markdown("<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
                    "color:rgba(0,212,255,.5);letter-spacing:2px;margin-bottom:8px;'>"
                    "ESTADO FINAL DE LA CIUDAD</div>", unsafe_allow_html=True)
        barra_indicador("Economía",        ind_fin.get("economia",0),        "💰")
        barra_indicador("Medio Ambiente",  ind_fin.get("medio_ambiente",0),  "🌿")
        barra_indicador("Energía",         ind_fin.get("energia",0),         "⚡")
        barra_indicador("Bienestar Social",ind_fin.get("bienestar_social",0),"🏥")
    with right:
        vals  = [ind_fin.get(k,0) for k in ["economia","medio_ambiente","energia","bienestar_social"]]
        prom  = int(sum(vals)/4) if vals else 0
        total_p = correctas + incorrectas
        pct_c = int(correctas/total_p*100) if total_p>0 else 0
        st.markdown("<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
                    "color:rgba(0,212,255,.5);letter-spacing:2px;margin-bottom:8px;'>"
                    "ESTADÍSTICAS</div>", unsafe_allow_html=True)
        for lb,vl,cl in [("RONDAS",str(rondas_comp)+"/"+str(TOTAL_RONDAS),"#00d4ff"),
                          ("CORRECTAS",str(correctas),"#22c55e"),
                          ("INCORRECTAS",str(incorrectas),"#ef4444"),
                          ("PRECISIÓN",str(pct_c)+"%","#f59e0b"),
                          ("PROMEDIO",str(prom),"#8b5cf6"),
                          ("DIFICULTAD",dificultad,"#00d4ff")]:
            st.markdown(
                "<div style='display:flex;justify-content:space-between;align-items:center;"
                "background:rgba(5,10,20,.8);border:1px solid rgba(0,212,255,.1);"
                "border-radius:8px;padding:8px 14px;margin-bottom:5px;'>"
                "<span style='font-family:Orbitron,sans-serif;font-size:.58rem;"
                "color:rgba(255,255,255,.35);letter-spacing:1px;'>"+lb+"</span>"
                "<span style='font-family:Orbitron,sans-serif;font-weight:700;"
                "font-size:.9rem;color:"+cl+";'>"+vl+"</span></div>",
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if logros:
        st.markdown("<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
                    "color:rgba(245,158,11,.7);letter-spacing:2px;margin-bottom:10px;'>"
                    "🏅 LOGROS DESBLOQUEADOS</div>", unsafe_allow_html=True)
        cols_l = st.columns(min(len(logros),4))
        for i,lkey in enumerate(logros):
            l = LOGROS.get(lkey,{})
            with cols_l[i%4]:
                st.markdown(
                    "<div style='background:rgba(245,158,11,0.08);"
                    "border:1px solid rgba(245,158,11,0.3);border-radius:10px;"
                    "padding:12px;text-align:center;'>"
                    "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                    "font-size:1.5rem;'>"+l.get("icon","🏅")+"</div>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:.63rem;"
                    "color:#f59e0b;font-weight:700;margin:4px 0 2px;'>"+l.get("nombre","")+"</div>"
                    "<div style='font-size:.62rem;color:rgba(255,255,255,.3);'>"+l.get("desc","")+"</div>"
                    "</div>", unsafe_allow_html=True)

    # Mapa final
    eco=ind_fin.get("economia",50); amb=ind_fin.get("medio_ambiente",50)
    ene=ind_fin.get("energia",50);  bie=ind_fin.get("bienestar_social",50)
    def _zc(v): return "#22c55e" if v>60 else "#f59e0b" if v>30 else "#ef4444"
    def _zi(v,a,b,c): return a if v>60 else b if v>30 else c
    def _zona(icon,label,val):
        c=_zc(val)
        return ("<div style='background:rgba(5,10,20,0.8);border:1px solid "+c+"44;"
                "border-radius:12px;padding:14px;text-align:center;'>"
                "<div style='font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;"
                "font-size:2rem;line-height:1;'>"+icon+"</div>"
                "<div style='font-family:Orbitron,sans-serif;font-size:.6rem;color:"+c+";"
                "letter-spacing:1px;font-weight:700;margin:5px 0 3px;'>"+label+"</div>"
                "<div style='font-family:Orbitron,sans-serif;font-size:1rem;"
                "font-weight:900;color:"+c+";'>"+str(val)+"</div>"
                "<div style='height:5px;background:rgba(255,255,255,.08);"
                "border-radius:3px;margin-top:8px;overflow:hidden;'>"
                "<div style='width:"+str(val)+"%;height:5px;border-radius:3px;"
                "background:"+c+";box-shadow:0 0 8px "+c+";'></div></div></div>")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-family:Orbitron,sans-serif;font-size:.62rem;"
        "color:rgba(0,212,255,.5);letter-spacing:3px;text-align:center;"
        "margin-bottom:10px;'>🗺️ MAPA FINAL DE LA CIUDAD</div>"
        "<div style='display:grid;grid-template-columns:1fr 1fr;gap:10px;"
        "max-width:500px;margin:0 auto;'>"
        +_zona(_zi(eco,"🏭","🏗️","💸"),"Industrial",eco)
        +_zona(_zi(amb,"🌳","🌿","🏜️"),"Ambiental",amb)
        +_zona(_zi(ene,"⚡","🔋","🌑"),"Energética",ene)
        +_zona(_zi(bie,"🏘️","🏚️","😰"),"Residencial",bie)
        +"</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("🔄 JUGAR DE NUEVO", use_container_width=True):
            if gid: reiniciar_progreso(gid)
            st.session_state.update({
                "pregunta_actual":None,"respuesta_correcta":False,
                "decision_elegida":None,"decision_efectos":None,
                "evento_ronda":None,"fase_ronda":"decision",
                "preguntas_usadas":[],"timer_inicio":None,"tiempo_agotado":False,
                "correctas":0,"incorrectas":0,"ninguno_critico":True,
                "logros_ganados":[],"energia_rondas_altas":0,
            })
            navegar("juego")
    with c2:
        if st.button("🏆 VER RANKING", use_container_width=True): navegar("ranking")
    with c3:
        if st.button("🏠 MENÚ PRINCIPAL", use_container_width=True): navegar("inicio")


def pantalla_ranking():
    _,col,_ = st.columns([0.5,3,0.5])
    with col:
        st.markdown(
            "<div style='text-align:center;padding:10px 0 6px;'>"
            "<div style='font-family:Orbitron,sans-serif;font-size:1.4rem;font-weight:900;"
            "color:#f59e0b;text-shadow:0 0 20px rgba(245,158,11,.5);"
            "letter-spacing:3px;margin-bottom:4px;'>🏆 RANKING GLOBAL</div>"
            "<div style='font-size:.7rem;color:rgba(255,255,255,.3);letter-spacing:2px;'>"
            "TOP 10 EQUIPOS</div></div>", unsafe_allow_html=True)

        filas = obtener_ranking()
        if not filas:
            st.markdown(
                "<div style='text-align:center;padding:40px;color:rgba(255,255,255,.3);'>"
                "No hay partidas registradas aún.</div>", unsafe_allow_html=True)
        else:
            medallas = ["🥇","🥈","🥉"] + ["🏅"]*(len(filas)-3)
            for pos,(med,fila) in enumerate(zip(medallas,filas), 1):
                col_pos = "#f59e0b" if pos==1 else "#94a3b8" if pos==2 else "#cd7f32" if pos==3 else "#64748b"
                logros_str = " ".join([LOGROS[k]["icon"] for k in fila["logros"].split(",") if k in LOGROS]) if fila["logros"] else ""
                dif_icon = DIFICULTADES.get(fila["dificultad"],{}).get("icon","")
                st.markdown(
                    "<div style='background:rgba(5,10,20,.85);border:1px solid "+col_pos+"44;"
                    "border-radius:12px;padding:14px 18px;margin-bottom:8px;"
                    "display:flex;align-items:center;gap:14px;"
                    "box-shadow:0 0 16px "+col_pos+"18;'>"
                    "<div style='font-size:1.6rem;min-width:36px;text-align:center;"
                    "font-family:Apple Color Emoji,Segoe UI Emoji,sans-serif;'>"+med+"</div>"
                    "<div style='flex:1;'>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:.85rem;"
                    "color:#f1f5f9;font-weight:700;'>"+fila["nombre_grupo"]+"</div>"
                    "<div style='font-size:.7rem;color:rgba(255,255,255,.35);margin-top:2px;'>"
                    +dif_icon+" "+fila["dificultad"]+" · ✅"+str(fila["correctas"])+" · "+logros_str+"</div>"
                    "</div>"
                    "<div style='font-family:Orbitron,sans-serif;font-size:1.3rem;"
                    "font-weight:900;color:"+col_pos+";text-shadow:0 0 12px "+col_pos+"66;'>"
                    +str(fila["puntaje"])+"</div>"
                    "</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⬅️ VOLVER AL MENÚ", use_container_width=True):
            navegar("inicio")


# ─── MAIN ────────────────────────────────────────────────────────
def main():
    init_session()
    inyectar_css()
    import os
    for ext in ["-wal","-shm","-journal"]:
        f_lock = DB_PATH + ext
        try:
            if os.path.exists(f_lock): os.remove(f_lock)
        except Exception:
            pass
    inicializar_db()
    {
        "inicio":               pantalla_inicio,
        "registro":             pantalla_registro,
        "agregar_estudiantes":  pantalla_agregar_estudiantes,
        "login":                pantalla_login,
        "juego":                pantalla_juego,
        "fin":                  pantalla_fin,
        "ranking":              pantalla_ranking,
    }.get(st.session_state["pantalla"], pantalla_inicio)()

if __name__ == "__main__":
    main()
