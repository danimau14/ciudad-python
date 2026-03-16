import random
import streamlit as st

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


def seleccionar_pregunta():
    usadas = st.session_state.get("preguntas_usadas", [])
    disponibles = [i for i in range(len(PREGUNTAS)) if i not in usadas]
    if not disponibles:
        st.session_state["preguntas_usadas"] = []
        disponibles = list(range(len(PREGUNTAS)))
    idx = random.choice(disponibles)
    st.session_state["preguntas_usadas"] = usadas + [idx]
    return PREGUNTAS[idx]
