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


    # ════ PYTHON FÁCIL (dif:1) ════
    {"cat":"Python","q":"¿Cómo se escribe un comentario en Python?","ops":["// comentario","# comentario","/* comentario */","-- comentario"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Qué palabra clave se usa para importar módulos?","ops":["include","require","import","use"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Cuál es el resultado de bool(0)?","ops":["True","False","0","None"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Cómo se crea una lista vacía?","ops":["list{}","[]","()","{}"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Qué hace el método upper() en strings?","ops":["Convierte a minúsculas","Elimina espacios","Convierte a mayúsculas","Invierte el string"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Cuál es el operador de comparación de igualdad?","ops":["=","==","===","!="],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Qué tipo devuelve type('hola')?","ops":["<class 'str'>","<class 'text'>","<class 'char'>","<class 'string'>"],"dif":1,"ok":0},
    {"cat":"Python","q":"¿Cómo se crea un diccionario vacío?","ops":["[]","()","{}","<>"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Qué imprime print(type(True))?","ops":["<class 'int'>","<class 'str'>","<class 'bool'>","<class 'float'>"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Cuánto es int('42')?","ops":["Error","'42'","42","42.0"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Cuál es la forma correcta de una condición if?","ops":["if x = 5:","if (x == 5)","if x == 5:","if x == 5"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Qué hace str(123)?","ops":["Convierte a float","Convierte a bool","Convierte a string","Redondea el número"],"dif":1,"ok":2},
    {"cat":"Python","q":"¿Resultado de 'py' + 'thon'?","ops":["py thon","python","'python'","Error"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Cómo se accede al primer elemento de lista L?","ops":["L[1]","L[0]","L.first()","L.get(0)"],"dif":1,"ok":1},
    {"cat":"Python","q":"¿Qué hace el método split() en strings?","ops":["Une strings","Divide en lista","Convierte a mayúsculas","Elimina caracteres"],"dif":1,"ok":1},
    # ════ PYTHON MEDIO (dif:2) ════
    {"cat":"Python","q":"¿Qué hace zip([1,2],[3,4])?","ops":["[4,6]","[(1,3),(2,4)]","[1,2,3,4]","Error"],"dif":2,"ok":1},
    {"cat":"Python","q":"¿Resultado de {'a':1,'b':2}.values()?","ops":["['a','b']","dict_values([1,2])","[1,2]","(1,2)"],"dif":2,"ok":1},
    {"cat":"Python","q":"¿Qué hace enumerate(['a','b'])?","ops":["[(0,'a'),(1,'b')]","{'a':0,'b':1}","[0,1]","['a','b']"],"dif":2,"ok":0},
    {"cat":"Python","q":"¿Diferencia entre list y tuple?","ops":["Ninguna","List es inmutable","Tuple es inmutable","Tuple es más lenta"],"dif":2,"ok":2},
    {"cat":"Python","q":"¿Resultado de set([1,2,2,3,3])?","ops":["[1,2,3]","{1,2,2,3,3}","{1,2,3}","(1,2,3)"],"dif":2,"ok":2},
    {"cat":"Python","q":"¿Qué hace any([False,True,False])?","ops":["False","True","None","Error"],"dif":2,"ok":1},
    {"cat":"Python","q":"¿Resultado de 'hello'[::-1]?","ops":["hello","olleh","Error","helo"],"dif":2,"ok":1},
    {"cat":"Python","q":"¿Qué hace all([True,True,True])?","ops":["True","False","3","None"],"dif":2,"ok":0},
    {"cat":"Python","q":"¿Qué es una función lambda?","ops":["Clase anónima","Función anónima de una línea","Variable global","Módulo especial"],"dif":2,"ok":1},
    {"cat":"Python","q":"¿Resultado de list(range(2,8,2))?","ops":["[2,4,6,8]","[2,4,6]","[2,3,4,5,6,7]","[0,2,4,6]"],"dif":2,"ok":1},
    # ════ PYTHON DIFÍCIL (dif:3) ════
    {"cat":"Python","q":"¿Resultado de [(i,j) for i in range(2) for j in range(2)]?","ops":["[(0,0),(1,1)]","[(0,0),(0,1),(1,0),(1,1)]","[(0,1),(1,0)]","Error"],"dif":3,"ok":1},
    {"cat":"Python","q":"¿Qué hace @staticmethod?","ops":["Crea método de clase","Define método sin acceso a instancia ni clase","Hereda de otra clase","Sobrecarga operadores"],"dif":3,"ok":1},
    {"cat":"Python","q":"¿Qué devuelve iter([1,2,3]).__next__()?","ops":["[1,2,3]","1","3","iterator"],"dif":3,"ok":1},
    {"cat":"Python","q":"¿Resultado de {**{'a':1}, **{'b':2}}?","ops":["Error","{'a':1,'b':2}","{'a':1}","{'b':2}"],"dif":3,"ok":1},
    {"cat":"Python","q":"¿Qué hace functools.reduce(lambda x,y:x+y,[1,2,3,4])?","ops":["[1,3,6,10]","10","24","Error"],"dif":3,"ok":1},
    {"cat":"Python","q":"¿Resultado de sorted({'b':2,'a':1,'c':3})?","ops":["[1,2,3]","['a','b','c']","{'a':1,'b':2,'c':3}","[('a',1)]"],"dif":3,"ok":1},
    # ════ PSEINT FÁCIL (dif:1) ════
    {"cat":"PSeInt","q":"¿Cómo se imprime en PSeInt?","ops":["print()","Escribir","Mostrar","Display"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Cómo termina un algoritmo en PSeInt?","ops":["End","Fin","FinAlgoritmo","Stop"],"dif":1,"ok":2},
    {"cat":"PSeInt","q":"¿Operador lógico Y en PSeInt?","ops":["&&","AND","Y","and"],"dif":1,"ok":2},
    {"cat":"PSeInt","q":"¿Operador lógico O en PSeInt?","ops":["||","OR","O","or"],"dif":1,"ok":2},
    {"cat":"PSeInt","q":"¿Cómo se declara un arreglo en PSeInt?","ops":["int arr[5]","Definir arr como Arreglo[5] De Entero","arr = []","arreglo arr(5)"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Qué hace FinPara en PSeInt?","ops":["Inicia ciclo","Termina ciclo Para","Termina el algoritmo","Sale del if"],"dif":1,"ok":1},
    {"cat":"PSeInt","q":"¿Instrucción para ciclo Repetir-HastaQue?","ops":["do-while","Repetir...HastaQue","loop...until","repeat...until"],"dif":1,"ok":1},
    # ════ PSEINT MEDIO (dif:2) ════
    {"cat":"PSeInt","q":"¿Cómo se pasan argumentos a un subproceso en PSeInt?","ops":["call proc(x)","SubProceso proc(x)","Proceso proc Con Parametros x","proc(x)"],"dif":2,"ok":2},
    {"cat":"PSeInt","q":"¿Cómo se devuelve un valor en función PSeInt?","ops":["return x","Retornar x","Devolver x","Escribir x"],"dif":2,"ok":1},
    {"cat":"PSeInt","q":"¿Cómo se accede al elemento i de un arreglo en PSeInt?","ops":["arr.get(i)","arr[i]","arr(i)","arr{i}"],"dif":2,"ok":1},
    # ════ CÁLCULO FÁCIL (dif:1) ════
    {"cat":"Calculo","q":"¿Qué es una derivada?","ops":["Área bajo la curva","Tasa de cambio instantánea","Suma de infinitos términos","Longitud de un arco"],"dif":1,"ok":1},
    {"cat":"Calculo","q":"Derivada de f(x) = 5?","ops":["5","1","0","x"],"dif":1,"ok":2},
    {"cat":"Calculo","q":"Derivada de f(x) = x?","ops":["x","0","1","2x"],"dif":1,"ok":2},
    {"cat":"Calculo","q":"∫ 0 dx = ?","ops":["0","1","x","C"],"dif":1,"ok":3},
    {"cat":"Calculo","q":"∫ 1 dx = ?","ops":["0","1","x+C","x"],"dif":1,"ok":2},
    {"cat":"Calculo","q":"¿Qué es el límite de una función?","ops":["Su derivada","El valor al que se aproxima","Su integral","Su dominio"],"dif":1,"ok":1},
    # ════ CÁLCULO MEDIO (dif:2) ════
    {"cat":"Calculo","q":"Derivada de f(x) = 3x³ - 2x + 1?","ops":["9x² - 2","3x² - 2","9x² - 2x","6x - 2"],"dif":2,"ok":0},
    {"cat":"Calculo","q":"∫ 2x dx = ?","ops":["2","x²","x² + C","2x² + C"],"dif":2,"ok":2},
    {"cat":"Calculo","q":"Derivada de f(x) = sin(x)·cos(x)?","ops":["cos²(x)-sin²(x)","cos(2x)","2cos(x)sin(x)","1"],"dif":2,"ok":0},
    {"cat":"Calculo","q":"∫(1→3) 2x dx = ?","ops":["4","6","8","9"],"dif":2,"ok":2},
    {"cat":"Calculo","q":"Límite de (x²-1)/(x-1) cuando x→1?","ops":["0","1","2","∞"],"dif":2,"ok":2},
    {"cat":"Calculo","q":"Derivada de f(x) = tan(x)?","ops":["sin²(x)","sec²(x)","cos²(x)","csc²(x)"],"dif":2,"ok":1},
    # ════ CÁLCULO DIFÍCIL (dif:3) ════
    {"cat":"Calculo","q":"∫ x²·ln(x) dx usando partes?","ops":["x³ln(x)/3 - x³/9 + C","x³/3·ln(x) + C","ln(x)·x³/3 - C","x³ln(x) - x³/3 + C"],"dif":3,"ok":0},
    {"cat":"Calculo","q":"Límite de (1+1/n)^n cuando n→∞?","ops":["1","2","e","∞"],"dif":3,"ok":2},
    {"cat":"Calculo","q":"∫ 1/(1+x²) dx = ?","ops":["ln(1+x²)+C","arctan(x)+C","arcsin(x)+C","1/(2x)+C"],"dif":3,"ok":1},
    {"cat":"Calculo","q":"Derivada de f(x) = arcsin(x)?","ops":["1/√(1-x²)","1/(1+x²)","1/√(1+x²)","-1/√(1-x²)"],"dif":3,"ok":0},
    {"cat":"Calculo","q":"∫(0→∞) e^(-x) dx = ?","ops":["0","1","∞","e"],"dif":3,"ok":1},
    # ════ FÍSICA MRU FÁCIL (dif:1) ════
    {"cat":"Fisica MRU","q":"¿Qué significa MRU?","ops":["Movimiento Rápido Uniforme","Movimiento Rectilíneo Uniforme","Movimiento Rotacional Único","Masa Relativa Universal"],"dif":1,"ok":1},
    {"cat":"Fisica MRU","q":"Fórmula del MRU para distancia?","ops":["d = v·t","d = v/t","d = a·t²","d = v² + 2a"],"dif":1,"ok":0},
    {"cat":"Fisica MRU","q":"En MRU, ¿cómo es la aceleración?","ops":["Constante","Variable","Nula","Negativa"],"dif":1,"ok":2},
    {"cat":"Fisica MRU","q":"Un auto a 60 km/h, ¿qué recorre en 2h?","ops":["30 km","60 km","120 km","240 km"],"dif":1,"ok":2},
    # ════ FÍSICA MRU MEDIO (dif:2) ════
    {"cat":"Fisica MRU","q":"Un tren recorre 300m en 20s. ¿Velocidad en m/s?","ops":["10 m/s","15 m/s","20 m/s","6000 m/s"],"dif":2,"ok":1},
    {"cat":"Fisica MRU","q":"¿Cómo es la gráfica v-t en MRU?","ops":["Parábola","Recta oblicua","Recta horizontal","Curva exponencial"],"dif":2,"ok":2},
    {"cat":"Fisica MRU","q":"Tiempo para recorrer 450m a 15 m/s?","ops":["15s","30s","45s","60s"],"dif":2,"ok":1},
    {"cat":"Fisica MRU","q":"¿En qué unidades se mide la velocidad?","ops":["kg·m","m/s²","m/s","N"],"dif":2,"ok":2},
    # ════ FÍSICA MRUA FÁCIL (dif:1) ════
    {"cat":"Fisica MRUA","q":"¿Qué significa MRUA?","ops":["Movimiento Rectilíneo Uniforme Acelerado","Movimiento Rápido Uniforme con Aceleración","Masa Rectilínea Uniforme Aleatoria","Movimiento Regular Universal Acelerado"],"dif":1,"ok":0},
    {"cat":"Fisica MRUA","q":"Unidades de la aceleración?","ops":["m/s","m/s²","km/h","N/m"],"dif":1,"ok":1},
    {"cat":"Fisica MRUA","q":"Fórmula de velocidad final en MRUA?","ops":["vf = v0 + a","vf = v0·a·t","vf = v0 + a·t","vf = v0 - a·t"],"dif":1,"ok":2},
    {"cat":"Fisica MRUA","q":"Un objeto parte del reposo con a=4m/s². ¿v a t=3s?","ops":["4 m/s","8 m/s","12 m/s","16 m/s"],"dif":1,"ok":2},
    # ════ FÍSICA MRUA MEDIO (dif:2) ════
    {"cat":"Fisica MRUA","q":"Fórmula de posición en MRUA?","ops":["x = v0·t","x = v0·t + ½a·t²","x = ½a·t²","x = a·t²"],"dif":2,"ok":1},
    {"cat":"Fisica MRUA","q":"v0=10m/s, a=2m/s², t=5s. ¿Distancia recorrida?","ops":["50m","75m","100m","60m"],"dif":2,"ok":1},
    {"cat":"Fisica MRUA","q":"Un auto frena de 20m/s a 0 en 4s. ¿Aceleración?","ops":["5 m/s²","−5 m/s²","−4 m/s²","4 m/s²"],"dif":2,"ok":1},
    {"cat":"Fisica MRUA","q":"¿Qué representa la pendiente en gráfica v-t del MRUA?","ops":["Posición","Velocidad","Aceleración","Tiempo"],"dif":2,"ok":2},
    # ════ FÍSICA MRUA DIFÍCIL (dif:3) ════
    {"cat":"Fisica MRUA","q":"v0=5m/s, a=−2m/s². ¿Cuándo se detiene el objeto?","ops":["t=1s","t=2.5s","t=5s","t=3s"],"dif":3,"ok":1},
    {"cat":"Fisica MRUA","q":"Dos autos parten del mismo punto. A: v=10m/s constante. B: v0=0, a=2m/s². ¿Cuándo B alcanza a A?","ops":["t=5s","t=10s","t=8s","t=6s"],"dif":3,"ok":1},
    {"cat":"Fisica MRUA","q":"¿Cuánta distancia recorre un proyectil en caída libre desde 80m de altura? (g=10m/s²)","ops":["2s","3s","4s","5s"],"dif":3,"ok":2},
    # ════ MATRICES FÁCIL (dif:1) ════
    {"cat":"Matrices","q":"¿Qué es una matriz cuadrada?","ops":["Tiene más filas que columnas","Tiene igual número de filas y columnas","Tiene solo una fila","Tiene solo una columna"],"dif":1,"ok":1},
    {"cat":"Matrices","q":"¿Dimensión de una matriz con 3 filas y 4 columnas?","ops":["4×3","3×3","3×4","4×4"],"dif":1,"ok":2},
    {"cat":"Matrices","q":"¿Qué es la matriz identidad?","ops":["Matriz de ceros","Diagonal de unos, resto ceros","Matriz triangular","Matriz de unos"],"dif":1,"ok":1},
    {"cat":"Matrices","q":"¿Cuándo se pueden sumar dos matrices?","ops":["Siempre","Solo si son cuadradas","Solo si tienen mismas dimensiones","Solo si son diagonales"],"dif":1,"ok":2},
    {"cat":"Matrices","q":"Resultado de [[1,2],[3,4]] + [[0,0],[0,0]]?","ops":["[[0,0],[0,0]]","[[1,2],[3,4]]","[[2,4],[6,8]]","Error"],"dif":1,"ok":1},
    # ════ MATRICES MEDIO (dif:2) ════
    {"cat":"Matrices","q":"[[1,2],[3,4]] × [[1,0],[0,1]] = ?","ops":["[[1,0],[0,1]]","[[1,2],[3,4]]","[[2,4],[6,8]]","[[0,0],[0,0]]"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"Det de [[3,1],[2,4]] = ?","ops":["10","14","12","8"],"dif":2,"ok":0},
    {"cat":"Matrices","q":"¿Qué condición debe tener una matriz para ser invertible?","ops":["Det = 0","Det ≠ 0","Ser cuadrada","Ser diagonal"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"Transpuesta de [[1,2,3],[4,5,6]] tiene dimensión:","ops":["2×3","3×2","3×3","2×2"],"dif":2,"ok":1},
    {"cat":"Matrices","q":"Si A es 3×2 y B es 2×5, ¿A×B es posible y tiene dimensión?","ops":["No es posible","3×5","2×2","5×3"],"dif":2,"ok":1},
    # ════ MATRICES DIFÍCIL (dif:3) ════
    {"cat":"Matrices","q":"Det de [[1,2,3],[0,4,5],[1,0,6]] = ?","ops":["22","34","16","44"],"dif":3,"ok":0},
    {"cat":"Matrices","q":"La inversa de [[2,1],[5,3]] es:","ops":["[[3,-1],[-5,2]]","[[-3,1],[5,-2]]","[[3,5],[-1,-2]]","[[2,5],[1,3]]"],"dif":3,"ok":0},
    {"cat":"Matrices","q":"Rango de [[1,2],[2,4]] = ?","ops":["0","1","2","4"],"dif":3,"ok":1},
    # ════ PENSAMIENTO SISTÉMICO (dif:1,2,3) ════
    {"cat":"Sist","q":"¿Qué es un sistema?","ops":["Un conjunto aislado","Un conjunto de elementos interrelacionados","Una ecuación matemática","Un algoritmo"],"dif":1,"ok":1},
    {"cat":"Sist","q":"¿Qué es retroalimentación en un sistema?","ops":["La salida de un sistema","La entrada de información externa","El efecto de la salida sobre la entrada","El proceso interno"],"dif":1,"ok":2},
    {"cat":"Sist","q":"¿Qué característica tiene un sistema complejo?","ops":["Partes independientes","Emergencia y no linealidad","Comportamiento predecible","Pocas variables"],"dif":2,"ok":1},
    {"cat":"Sist","q":"¿Qué es un bucle de retroalimentación positiva?","ops":["Corrige desviaciones","Amplifica cambios","Estabiliza el sistema","Reduce oscilaciones"],"dif":2,"ok":1},
    {"cat":"Sist","q":"¿Qué es la homeostasis en sistemas?","ops":["Crecimiento descontrolado","Tendencia al equilibrio","Colapso del sistema","Retroalimentación positiva"],"dif":2,"ok":1},
    {"cat":"Sist","q":"En un sistema de ciudad, ¿cuál es una variable de stock?","ops":["Tasa de natalidad","Población total","Velocidad del tráfico","Consumo diario de agua"],"dif":3,"ok":1},
    {"cat":"Sist","q":"¿Qué diferencia un modelo mental de un modelo formal?","ops":["El modelo mental es más preciso","El formal usa ecuaciones y el mental es intuitivo","No hay diferencia","El mental es cuantitativo"],"dif":3,"ok":1},
    {"cat":"Sist","q":"¿Qué es un atractor en sistemas dinámicos?","ops":["Un estado que el sistema evita","Un estado hacia el que tiende el sistema","Un parámetro externo","Una variable de flujo"],"dif":3,"ok":1},
    # ════ LÓGICA Y ALGORITMOS (dif:1,2,3) ════
    {"cat":"Logica","q":"¿Cuántos pasos tiene el algoritmo de búsqueda lineal en peor caso con N elementos?","ops":["1","log N","N","N²"],"dif":1,"ok":2},
    {"cat":"Logica","q":"¿Qué es un algoritmo?","ops":["Un lenguaje de programación","Una secuencia finita de pasos para resolver un problema","Un tipo de dato","Una variable"],"dif":1,"ok":1},
    {"cat":"Logica","q":"¿Complejidad de búsqueda binaria?","ops":["O(1)","O(n)","O(log n)","O(n²)"],"dif":2,"ok":2},
    {"cat":"Logica","q":"¿Qué es un grafo dirigido?","ops":["Grafo con pesos","Grafo donde las aristas tienen dirección","Grafo sin ciclos","Grafo completo"],"dif":2,"ok":1},
    {"cat":"Logica","q":"¿Diferencia entre pila (stack) y cola (queue)?","ops":["No hay diferencia","Stack es LIFO, queue es FIFO","Stack es FIFO, queue es LIFO","Ambas son FIFO"],"dif":2,"ok":1},
    {"cat":"Logica","q":"¿Complejidad del ordenamiento burbuja en peor caso?","ops":["O(n)","O(n log n)","O(n²)","O(log n)"],"dif":2,"ok":2},
    {"cat":"Logica","q":"¿Qué es la notación Big-O?","ops":["Medida exacta del tiempo","Cota superior del crecimiento del tiempo","Medida de memoria","Número de instrucciones"],"dif":3,"ok":1},
    {"cat":"Logica","q":"¿Cuál es la complejidad del algoritmo Quicksort en caso promedio?","ops":["O(n)","O(n log n)","O(n²)","O(log n)"],"dif":3,"ok":1},
    {"cat":"Logica","q":"¿Qué es la recursión de cola (tail recursion)?","ops":["Recursión infinita","Recursión donde la llamada recursiva es la última operación","Recursión con múltiples llamadas","Recursión sin caso base"],"dif":3,"ok":1},


    # ════ ESTADÍSTICA BÁSICA ════
    {"cat":"Estadistica","q":"¿Qué es la media aritmética?","ops":["El valor más frecuente","El valor central ordenado","Suma de datos dividida entre cantidad","La diferencia entre máximo y mínimo"],"dif":1,"ok":2},
    {"cat":"Estadistica","q":"Mediana de [3,7,1,9,5]?","ops":["3","5","7","9"],"dif":1,"ok":1},
    {"cat":"Estadistica","q":"Moda de [2,4,4,6,4,8]?","ops":["2","4","6","8"],"dif":1,"ok":1},
    {"cat":"Estadistica","q":"¿Qué mide la varianza?","ops":["Valor central","Dispersión respecto a la media","Valor más frecuente","Rango de datos"],"dif":2,"ok":1},
    {"cat":"Estadistica","q":"Si la varianza es 16, ¿cuánto es la desviación estándar?","ops":["8","4","256","2"],"dif":2,"ok":1},
    {"cat":"Estadistica","q":"¿Qué es el coeficiente de correlación de Pearson?","ops":["Mide dispersión","Mide relación lineal entre variables","Mide la moda","Mide el rango"],"dif":3,"ok":1},
    {"cat":"Estadistica","q":"P(A∪B) = P(A)+P(B)-?","ops":["P(A·B)","P(A∩B)","P(A/B)","1-P(A)"],"dif":2,"ok":1},
    {"cat":"Estadistica","q":"En distribución normal, ¿qué porcentaje cae dentro de ±1σ?","ops":["68%","95%","99%","50%"],"dif":3,"ok":0},
    {"cat":"Estadistica","q":"¿Qué es un intervalo de confianza?","ops":["Un valor exacto","Rango donde cae el parámetro con cierta probabilidad","La desviación estándar","El valor de la muestra"],"dif":3,"ok":1},
    # ════ ÁLGEBRA BÁSICA ════
    {"cat":"Algebra","q":"Solución de 2x + 4 = 10?","ops":["x=2","x=3","x=4","x=7"],"dif":1,"ok":1},
    {"cat":"Algebra","q":"Factorizar x²-9?","ops":["(x-3)(x+3)","(x-9)(x+1)","(x-3)²","(x+3)²"],"dif":1,"ok":0},
    {"cat":"Algebra","q":"Solución de x²-5x+6=0?","ops":["x=1,x=6","x=2,x=3","x=-2,x=-3","x=5,x=1"],"dif":2,"ok":1},
    {"cat":"Algebra","q":"¿Qué es el discriminante en ecuación cuadrática?","ops":["a+b+c","b²-4ac","2a","b/2a"],"dif":2,"ok":1},
    {"cat":"Algebra","q":"Si f(x)=x²+2x, ¿cuánto es f(-1)?","ops":["1","−1","3","0"],"dif":2,"ok":1},
    {"cat":"Algebra","q":"Solución del sistema: x+y=5, x-y=1?","ops":["x=2,y=3","x=3,y=2","x=4,y=1","x=1,y=4"],"dif":2,"ok":1},
    {"cat":"Algebra","q":"¿Cuántas soluciones tiene ax²+bx+c=0 si b²-4ac<0?","ops":["2 reales","1 real","0 reales","Infinitas"],"dif":3,"ok":2},
    # ════ NÚMEROS Y LÓGICA ════
    {"cat":"Logica","q":"¿Cuánto es el factorial de 0?","ops":["0","1","indefinido","∞"],"dif":1,"ok":1},
    {"cat":"Logica","q":"¿Qué es un número primo?","ops":["Divisible por 2","Solo divisible por 1 y sí mismo","Número par","Número negativo"],"dif":1,"ok":1},
    {"cat":"Logica","q":"¿Cuánto es 2⁸?","ops":["64","128","256","512"],"dif":2,"ok":2},
    {"cat":"Logica","q":"¿Qué es el MCM de 4 y 6?","ops":["2","8","12","24"],"dif":2,"ok":2},
    {"cat":"Logica","q":"¿Cuántos números primos hay menores a 10?","ops":["3","4","5","6"],"dif":2,"ok":1},

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