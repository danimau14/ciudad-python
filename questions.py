import random
import streamlit as st

PREGUNTAS = [
    {"cat":"Python","q":"¿Resultado de type(3.14)?","ops":["<class 'int'>","<class 'float'>","<class 'str'>","<class 'double'>"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Que hace len()?","ops":["Convierte a entero","Retorna la longitud","Imprime en pantalla","Crea una lista"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Como se define una funcion?","ops":["function f():","def f():","func f():","define f():"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Resultado de 2 ** 3?","ops":["6","8","9","5"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Tipo de dato de True?","ops":["int","str","bool","float"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Division entera en Python?","ops":["/","%","//","div"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Salida de print('Hi'*2)?","ops":["HiHi","Hi2","Error","Hi Hi"],"dif":1,"ok":0},
    {"cat":"Python","q":"¿Agregar elemento al final de lista?","ops":["lst.add(x)","lst.append(x)","lst.insert(x)","lst.push(x)"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Que devuelve range(3)?","ops":["[1,2,3]","[0,1,2,3]","[0,1,2]","[1,2]"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Resultado de 10 % 3?","ops":["3","1","0","2"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Que hace input()?","ops":["Imprime","Lee del usuario","Importa","Crea variables"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Estructura para recorrer lista?","ops":["foreach","for ... in ...","loop","while each"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Como declarar variable en PSeInt?","ops":["var x <- 5","Definir x como Entero","int x = 5","x = 5"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Instruccion para mostrar en PSeInt?","ops":["print()","Mostrar","Escribir","Display"],"dif":1,"ok":2},
    {"cat":"PSeInt","q":"¿Como inicia un algoritmo en PSeInt?","ops":["Start","Algoritmo Nombre","Begin","def main():"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Instruccion para leer en PSeInt?","ops":["Leer","Input","Capturar","Ingresar"],"dif":1,"ok":0},
    {"cat":"PSeInt","q":"¿Como se escribe SI en PSeInt?","ops":["if(c)then","Si(c)Entonces","when(c)","check(c)"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Operador de asignacion en PSeInt?","ops":["=","==","<-",":="],"dif":1,"ok":2},
    {"cat":"PSeInt","q":"¿Como inicia ciclo MIENTRAS en PSeInt?","ops":["while(c)do","Mientras(c)Hacer","loop(c)","repetir(c)"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Palabra que cierra SI-ENTONCES?","ops":["End","FinSi","EndIf","Cerrar"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Variable tipo real en PSeInt?","ops":["Definir x como Real","float x","real x","var x:real"],"dif":1,"ok":0},
    {"cat":"PSeInt","q":"¿Ciclo FOR en PSeInt?","ops":["for i=1 to 10","Para i<-1 Hasta 10 Hacer","loop i","repeat i"],"dif":1,"ok":1},
    {"cat":"Calculo","q":"Integral de x dx?","ops":["x+C","x^2+C","x^2/2+C","2x+C"],"dif":2,"ok":2},
    {"cat":"Calculo","q":"Integral de e^x dx?","ops":["e^x+C","xe^x+C","e^(x+1)+C","ln(x)+C"],"dif":2,"ok":0},
    {"cat":"Calculo","q":"Integral de cos(x) dx?","ops":["-sin(x)+C","sin(x)+C","-cos(x)+C","tan(x)+C"],"dif":2,"ok":1},
    {"cat":"Calculo","q":"Integral de (1/x) dx?","ops":["x^2+C","ln|x|+C","1/x^2+C","-1/x^2+C"],"dif":2,"ok":1},
    {"cat":"Calculo","q":"Integral de sin(x) dx?","ops":["cos(x)+C","-cos(x)+C","sin(x)+C","tan(x)+C"],"dif":2,"ok":1},
    {"cat":"Calculo","q":"Integral de 3x^2 dx?","ops":["x^3+C","6x+C","3x+C","x^3/3+C"],"dif":2,"ok":0},
    {"cat":"Calculo","q":"¿Que representa la integral definida geometricamente?","ops":["Pendiente","Area bajo la curva","Derivada","Volumen"],"dif":2,"ok":1},
    {"cat":"Calculo","q":"Integral de 0 dx?","ops":["0","C","x+C","1"],"dif":2,"ok":1},
    {"cat":"Calculo","q":"Integral de x^n dx (n≠-1)?","ops":["n*x^(n-1)+C","x^(n+1)/(n+1)+C","x^n/n+C","n*x^n+C"],"dif":2,"ok":1},
    {"cat":"Derivadas","q":"Derivada de x^2?","ops":["x","2x","x^2","2"],"dif":2,"ok":1},
    {"cat":"Derivadas","q":"Derivada de e^x?","ops":["x*e^(x-1)","e^x","e^(x+1)","ln(x)"],"dif":2,"ok":1},
    {"cat":"Derivadas","q":"Derivada de sin(x)?","ops":["-sin(x)","cos(x)","-cos(x)","tan(x)"],"dif":2,"ok":1},
    {"cat":"Derivadas","q":"Derivada de ln(x)?","ops":["e^x","1/x","x*ln(x)","log(x)"],"dif":2,"ok":1},
    {"cat":"Derivadas","q":"Derivada de una constante k?","ops":["k","1","0","k-1"],"dif":2,"ok":2},
    {"cat":"Derivadas","q":"Derivada de cos(x)?","ops":["sin(x)","-sin(x)","cos(x)","tan(x)"],"dif":2,"ok":1},
    {"cat":"Derivadas","q":"Regla de la cadena: d/dx[f(g(x))]?","ops":["f'(x)g(x)","f'(g(x))g'(x)","f(x)g'(x)","f'(x)+g'(x)"],"dif":2,"ok":1},
    {"cat":"Derivadas","q":"Derivada de x^3 - 4x + 2?","ops":["3x-4","3x^2-4","x^2-4","3x^2+2"],"dif":2,"ok":1},
    {"cat":"Fisica MRU","q":"En MRU ¿que tipo de velocidad tiene el objeto?","ops":["Acelerada","Constante","Nula","Variable"],"dif":2,"ok":1},
    {"cat":"Fisica MRU","q":"Formula del MRU:","ops":["d=v*t","d=v^2/2a","v=a*t","F=m*a"],"dif":2,"ok":0},
    {"cat":"Fisica MRU","q":"Auto recorre 120km en 2h. ¿Velocidad?","ops":["50km/h","60km/h","70km/h","80km/h"],"dif":2,"ok":1},
    {"cat":"Fisica MRU","q":"En MRU la aceleracion es:","ops":["Maxima","Creciente","Cero","Variable"],"dif":2,"ok":2},
    {"cat":"Fisica MRU","q":"Pendiente en grafica posicion-tiempo de MRU representa:","ops":["Aceleracion","Fuerza","Velocidad","Masa"],"dif":2,"ok":2},
    {"cat":"Fisica MRU","q":"v=10m/s, t=5s ¿cuanto recorre?","ops":["2m","15m","50m","100m"],"dif":2,"ok":2},
    {"cat":"Fisica MRU","q":"Grafica v-t de MRU:","ops":["Curva ascendente","Horizontal","Vertical","Diagonal"],"dif":2,"ok":1},
    {"cat":"Fisica MRUA","q":"¿Que caracteriza al MRUA?","ops":["Velocidad cte","Aceleracion cte","Aceleracion nula","Posicion fija"],"dif":2,"ok":1},
    {"cat":"Fisica MRUA","q":"v=v0+a*t corresponde a:","ops":["MRU","Caida libre","MRUA","MCU"],"dif":2,"ok":2},
    {"cat":"Fisica MRUA","q":"Reposo, a=3m/s^2. ¿Tiempo para 15m/s?","ops":["3s","4s","5s","6s"],"dif":2,"ok":2},
    {"cat":"Fisica MRUA","q":"Area bajo v-t en MRUA representa:","ops":["Aceleracion","Fuerza","Desplazamiento","Potencia"],"dif":2,"ok":2},
    {"cat":"Fisica MRUA","q":"d=v0*t+(1/2)*a*t^2 es:","ops":["Velocidad final","Desplazamiento MRUA","Fuerza neta","Energia"],"dif":2,"ok":1},
    {"cat":"Fisica MRUA","q":"Si a=0, MRUA se convierte en:","ops":["Caida libre","MCU","MRU","Reposo"],"dif":2,"ok":2},
    {"cat":"Fisica MRUA","q":"v^2=v0^2+2*a*d es la ecuacion de:","ops":["Energia","Velocidad sin tiempo","Posicion","Impulso"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"¿Que es una matriz cuadrada?","ops":["Mas filas que col","Filas=columnas","Solo una fila","Elementos iguales"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"A=[1,2], B=[3,4], A+B=?","ops":["[4,6]","[3,8]","[2,4]","[1,6]"],"dif":2,"ok":0},
    {"cat":"Matrices","q":"La transpuesta intercambia:","ops":["Filas por columnas","Sumas por restas","Signos","Diagonales"],"dif":2,"ok":0},
    {"cat":"Matrices","q":"Condicion para multiplicar A x B:","ops":["Ambas cuadradas","Col(A)=Fil(B)","Fil(A)=Fil(B)","A=B"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"¿Que es la matriz identidad?","ops":["Matriz ceros","Unos en diagonal","Triangular","Nula"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"Si det(A)=0, A es:","ops":["Invertible","Singular","Identidad","Ortogonal"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"Dimension de producto 2x3 por 3x4:","ops":["3x3","2x4","3x4","2x3"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"Matriz triangular superior tiene:","ops":["Todo cero","Ceros debajo diagonal","Ceros encima diagonal","Solo diagonal"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"Traza de una matriz es:","ops":["Determinante","Suma diagonal principal","Mayor elemento","Transpuesta"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"det([[1,2],[3,4]])=?","ops":["10","-2","2","-10"],"dif":2,"ok":1},

    # ── DIFÍCILES Python ────────────────────────────────────────────
    {"cat":"Python","q":"¿Resultado de [x**2 for x in range(4) if x%2==0]?","ops":["[0,4]","[0,1,4,9]","[4,16]","[0,4,16]"],"dif":3,"ok":0},
    {"cat":"Python","q":"¿Qué imprime: d={1:'a',2:'b'}; print(d.get(3,'z'))?","ops":["None","KeyError","z","3"],"dif":3,"ok":2},
    {"cat":"Python","q":"¿Resultado de list(map(lambda x:x*2,[1,2,3]))?","ops":["[1,2,3]","[2,4,6]","[1,4,9]","[3,6,9]"],"dif":3,"ok":1},
    {"cat":"Python","q":"¿Resultado de sorted([3,1,2],reverse=True)?","ops":["[1,2,3]","[3,2,1]","[2,1,3]","Error"],"dif":3,"ok":1},
    {"cat":"Python","q":"¿Qué hace *args en una función?","ops":["Retorna múltiples valores","Recibe argumentos de palabras clave","Recibe argumentos posicionales variables","Define una función anónima"],"dif":3,"ok":2},
    # ── DIFÍCILES Cálculo ───────────────────────────────────────────
    {"cat":"Calculo","q":"∫(0→1) x² dx = ?","ops":["1/2","1/3","2/3","1/4"],"dif":3,"ok":1},
    {"cat":"Calculo","q":"∫ x·e^x dx usando integración por partes = ?","ops":["e^x(x-1)+C","e^x(x+1)+C","x·e^x+C","e^x/x+C"],"dif":3,"ok":0},
    {"cat":"Calculo","q":"∫(0→π) sin(x) dx = ?","ops":["0","1","2","-2"],"dif":3,"ok":2},
    # ── DIFÍCILES Derivadas ─────────────────────────────────────────
    {"cat":"Derivadas","q":"Derivada de f(x)=ln(x²+1)?","ops":["1/(x²+1)","2x/(x²+1)","2x·ln(x²+1)","x/(x²+1)"],"dif":3,"ok":1},
    {"cat":"Derivadas","q":"Derivada de f(x)=x·sin(x) usando regla del producto?","ops":["cos(x)","sin(x)+x·cos(x)","x·cos(x)","sin(x)-x·cos(x)"],"dif":3,"ok":1},
    {"cat":"Derivadas","q":"Si f(x)=e^(2x), ¿cuánto es f''(x)?","ops":["2e^(2x)","4e^(2x)","e^(2x)","2xe^(2x)"],"dif":3,"ok":1},
    # ── DIFÍCILES Física MRU ────────────────────────────────────────
    {"cat":"Fisica MRU","q":"Un móvil recorre 180m en 12s. ¿Velocidad en km/h?","ops":["15 km/h","54 km/h","50 km/h","18 km/h"],"dif":3,"ok":1},
    {"cat":"Fisica MRU","q":"¿En qué tipo de gráfica x-t el MRU produce una recta de pendiente positiva?","ops":["Parábola","Recta horizontal","Recta con pendiente positiva","Curva exponencial"],"dif":3,"ok":2},
    # ── DIFÍCILES Física MRUA ───────────────────────────────────────
    {"cat":"Fisica MRUA","q":"Un auto parte del reposo con a=3m/s². ¿Velocidad a t=6s?","ops":["9 m/s","12 m/s","18 m/s","21 m/s"],"dif":3,"ok":2},
    {"cat":"Fisica MRUA","q":"Distancia recorrida con v0=0, a=2m/s², t=5s?","ops":["10m","25m","50m","20m"],"dif":3,"ok":1},
    # ── DIFÍCILES Matrices ──────────────────────────────────────────
    {"cat":"Matrices","q":"Det de [[2,1],[5,3]] = ?","ops":["1","11","6","13"],"dif":3,"ok":0},
    {"cat":"Matrices","q":"Transpuesta de [[1,2],[3,4]] = ?","ops":["[[1,3],[2,4]]","[[4,3],[2,1]]","[[1,2],[3,4]]","[[2,1],[4,3]]"],"dif":3,"ok":0},
    {"cat":"Matrices","q":"Si A es 2×3 y B es 3×4, ¿dimensión de A·B?","ops":["2×4","3×3","4×2","2×3"],"dif":3,"ok":0},

]


def seleccionar_pregunta(dificultad="Medio"):
    # Mapear nivel a dificultades permitidas
    dif_map = {"Fácil": [1], "Medio": [1, 2], "Difícil": [2, 3]}
    niveles = dif_map.get(dificultad, [1, 2])
    pool = [i for i, p in enumerate(PREGUNTAS) if p.get("dif", 1) in niveles]
    usadas = st.session_state.get("preguntas_usadas", [])
    disponibles = [i for i in pool if i not in usadas]
    if not disponibles:
        st.session_state["preguntas_usadas"] = []
        disponibles = list(pool)
    idx = random.choice(disponibles)
    st.session_state["preguntas_usadas"] = usadas + [idx]
    return PREGUNTAS[idx]