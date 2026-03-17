VALOR_INICIAL  = 50
VALOR_MINIMO   = 0
TOTAL_RONDAS   = 10
COOLDOWN       = 3
MIN_EST        = 3
MAX_EST        = 5
REGEX_NOMBRE   = r"[A-Za-záéíóúÁÉÍÓÚñÑ ]+"
TIEMPO_PREGUNTA = 30

DECISIONES = {
    "Construir fábrica":    {"emoji":"🏭","economia":18,"medio_ambiente":-15,"energia":-8,"bienestar_social":-3},
    "Crear parque natural":  {"emoji":"🌳","economia":-8,"medio_ambiente":18,"energia":-3,"bienestar_social":12},
    "Instalar paneles solares":{"emoji":"☀️","economia":-12,"medio_ambiente":12,"energia":22,"bienestar_social":-2},
    "Construir escuelas":   {"emoji":"🏫","economia":-12,"medio_ambiente":-2,"energia":-6,"bienestar_social":22},
    "Ampliar autopistas":   {"emoji":"🛣️","economia":12,"medio_ambiente":-18,"energia":-12,"bienestar_social":-5},
    "Agricultura urbana":   {"emoji":"🌾","economia":6,"medio_ambiente":12,"energia":4,"bienestar_social":10},
    "Mejorar hospitales":   {"emoji":"🏥","economia":-18,"medio_ambiente":-2,"energia":-6,"bienestar_social":28},
    "Planta de carbón":     {"emoji":"⚡","economia":22,"medio_ambiente":-25,"energia":28,"bienestar_social":-10},
}

EVENTOS = [
    {"nombre":"Tormenta devastadora","indicador":"medio_ambiente","valor":-14},
    {"nombre":"Pandemia regional","indicador":"bienestar_social","valor":-16},
    {"nombre":"Apagón masivo","indicador":"energia","valor":-14},
    {"nombre":"Recesión económica","indicador":"economia","valor":-14},
    {"nombre":"Incendio forestal grave","indicador":"medio_ambiente","valor":-18},
    {"nombre":"Sequía prolongada","indicador":"medio_ambiente","valor":-12},
    {"nombre":"Crisis industrial","indicador":"economia","valor":-12},
    {"nombre":"Inundación urbana","indicador":"bienestar_social","valor":-13},
    {"nombre":"Fallo de infraestructura","indicador":"energia","valor":-16},
    {"nombre":"Brote de enfermedad","indicador":"bienestar_social","valor":-12},
    {"nombre":"Boom económico","indicador":"economia","valor":10},
    {"nombre":"Ahorro energético","indicador":"energia","valor":9},
    {"nombre":"Gran cosecha","indicador":"medio_ambiente","valor":8},
    {"nombre":"Festival cultural","indicador":"bienestar_social","valor":10},
    {"nombre":"Inversión extranjera","indicador":"economia","valor":12},
    {"nombre":"Beca educativa masiva","indicador":"bienestar_social","valor":9},
    {"nombre":"Energía renovable bonus","indicador":"energia","valor":8},
]

PREGUNTAS = [
    {"cat":"Python","q":"Resultado de type(3.14)?","ops":["<class 'int'>","<class 'float'>","<class 'str'>","<class 'double'>"],"ok":1},
    {"cat":"Python","q":"¿Qué hace len()?","ops":["Convierte a entero","Retorna la longitud","Imprime en pantalla","Crea una lista"],"ok":1},
    {"cat":"Python","q":"¿Cómo se define una función?","ops":["function f():","def f():","func f():","define f():"],"ok":1},
    {"cat":"Python","q":"Resultado de 2**3?","ops":["6","8","9","5"],"ok":1},
    {"cat":"Python","q":"Tipo de dato de True?","ops":["int","str","bool","float"],"ok":2},
    {"cat":"Python","q":"División entera en Python?","ops":["//","/%","\\","div"],"ok":0},
    {"cat":"Python","q":"Salida de print('Hi'*2)?","ops":["HiHi","Hi2","Error","Hi Hi"],"ok":0},
    {"cat":"Python","q":"Agregar elemento al final de lista?","ops":["lst.add(x)","lst.append(x)","lst.insert(x)","lst.push(x)"],"ok":1},
    {"cat":"Python","q":"¿Qué devuelve range(3)?","ops":["1,2,3","0,1,2,3","0,1,2","1,2"],"ok":2},
    {"cat":"Python","q":"Resultado de 10%3?","ops":["3","1","0","2"],"ok":1},
    {"cat":"Python","q":"¿Qué hace input()?","ops":["Imprime","Lee del usuario","Importa","Crea variables"],"ok":1},
    {"cat":"Python","q":"Estructura para recorrer lista?","ops":["foreach","for ... in ...","loop","while each"],"ok":1},
    {"cat":"PSeInt","q":"¿Cómo declarar variable en PSeInt?","ops":["var x = 5","Definir x como Entero","int x=5","x=5"],"ok":1},
    {"cat":"PSeInt","q":"Instrucción para mostrar en PSeInt?","ops":["print","Mostrar","Escribir","Display"],"ok":2},
    {"cat":"PSeInt","q":"¿Cómo inicia un algoritmo en PSeInt?","ops":["Start","Algoritmo Nombre","Begin","def main"],"ok":1},
    {"cat":"PSeInt","q":"Instrucción para leer en PSeInt?","ops":["Leer","Input","Capturar","Ingresar"],"ok":0},
    {"cat":"PSeInt","q":"¿Cómo se escribe SI en PSeInt?","ops":["if(c)then","Si(c)Entonces","when(c)","check(c)"],"ok":1},
    {"cat":"PSeInt","q":"Operador de asignación en PSeInt?","ops":["=","==","<-","=>"],"ok":2},
    {"cat":"PSeInt","q":"¿Cómo inicia ciclo MIENTRAS en PSeInt?","ops":["while(c)do","Mientras(c)Hacer","loop(c)","repetir(c)"],"ok":1},
    {"cat":"PSeInt","q":"Palabra que cierra SI-ENTONCES?","ops":["End","FinSi","EndIf","Cerrar"],"ok":1},
    {"cat":"PSeInt","q":"Variable tipo real en PSeInt?","ops":["Definir x como Real","float x","real x","var x:real"],"ok":0},
    {"cat":"PSeInt","q":"Ciclo FOR en PSeInt?","ops":["for i=1 to 10","Para i<-1 Hasta 10 Hacer","loop i","repeat i"],"ok":1},
    {"cat":"Cálculo","q":"Integral de x dx?","ops":["x+C","x²+C","x²/2+C","2x+C"],"ok":2},
    {"cat":"Cálculo","q":"Integral de eˣ dx?","ops":["eˣ+C","xeˣ+C","eˣ⁺¹+C","ln(x)+C"],"ok":0},
    {"cat":"Cálculo","q":"Integral de cos(x) dx?","ops":["-sin(x)+C","sin(x)+C","-cos(x)+C","tan(x)+C"],"ok":1},
    {"cat":"Cálculo","q":"Integral de 1/x dx?","ops":["x²+C","ln|x|+C","1/x²+C","-1/x²+C"],"ok":1},
    {"cat":"Cálculo","q":"Integral de sin(x) dx?","ops":["cos(x)+C","-cos(x)+C","sin(x)+C","tan(x)+C"],"ok":1},
    {"cat":"Cálculo","q":"Integral de 3x² dx?","ops":["x³+C","6x+C","3x+C","x³/3+C"],"ok":0},
    {"cat":"Cálculo","q":"¿Qué representa la integral definida geométricamente?","ops":["Pendiente","Área bajo la curva","Derivada","Volumen"],"ok":1},
    {"cat":"Cálculo","q":"Integral de 0 dx?","ops":["0","C","x+C","1"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de x²?","ops":["x","2x","x/2","2"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de eˣ?","ops":["xe^(x-1)","eˣ","e^(x+1)","ln(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de sin(x)?","ops":["-sin(x)","cos(x)","-cos(x)","tan(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de ln(x)?","ops":["eˣ","1/x","x·ln(x)","log(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de una constante k?","ops":["k","1","0","k-1"],"ok":2},
    {"cat":"Derivadas","q":"Derivada de cos(x)?","ops":["sin(x)","-sin(x)","cos(x)","tan(x)"],"ok":1},
    {"cat":"Derivadas","q":"Regla de la cadena d/dx[f(g(x))]?","ops":["f'(x)·g(x)","f'(g(x))·g'(x)","f(x)·g'(x)","f'(x)·g'(x)"],"ok":1},
    {"cat":"Derivadas","q":"Derivada de x³ - 4x + 2?","ops":["3x-4","3x²-4","x²-4","3x²+2"],"ok":1},
    {"cat":"Física MRU","q":"En MRU ¿qué tipo de velocidad tiene el objeto?","ops":["Acelerada","Constante","Nula","Variable"],"ok":1},
    {"cat":"Física MRU","q":"Fórmula del MRU","ops":["d=v/t","d=v²/2a","v=a·t","F=ma"],"ok":0},
    {"cat":"Física MRU","q":"Auto recorre 120km en 2h. ¿Velocidad?","ops":["50km/h","60km/h","70km/h","80km/h"],"ok":1},
    {"cat":"Física MRU","q":"En MRU la aceleración es","ops":["Máxima","Creciente","Cero","Variable"],"ok":2},
    {"cat":"Física MRU","q":"Pendiente en gráfica posición-tiempo de MRU representa","ops":["Aceleración","Fuerza","Velocidad","Masa"],"ok":2},
    {"cat":"Física MRU","q":"v=10m/s, t=5s ¿cuánto recorre?","ops":["2m","15m","50m","100m"],"ok":2},
    {"cat":"Física MRU","q":"Gráfica v-t de MRU","ops":["Curva ascendente","Horizontal","Vertical","Diagonal"],"ok":1},
    {"cat":"Física MRUA","q":"¿Qué caracteriza al MRUA?","ops":["Velocidad cte","Aceleración cte","Aceleración nula","Posición fija"],"ok":1},
    {"cat":"Física MRUA","q":"v=v₀+a·t corresponde a","ops":["MRU","Caída libre","MRUA","MCU"],"ok":2},
    {"cat":"Física MRUA","q":"Reposo, a=3m/s². ¿Tiempo para 15m/s?","ops":["3s","4s","5s","6s"],"ok":2},
    {"cat":"Física MRUA","q":"Área bajo v-t en MRUA representa","ops":["Aceleración","Fuerza","Desplazamiento","Potencia"],"ok":2},
    {"cat":"Física MRUA","q":"d=v₀t+½at² es","ops":["Velocidad final","Desplazamiento MRUA","Fuerza neta","Energía"],"ok":1},
    {"cat":"Física MRUA","q":"Si a=0, MRUA se convierte en","ops":["Caída libre","MCU","MRU","Reposo"],"ok":2},
    {"cat":"Física MRUA","q":"v²=v₀²+2ad es la ecuación de","ops":["Energía","Velocidad sin tiempo","Posición","Impulso"],"ok":1},
    {"cat":"Matrices","q":"¿Qué es una matriz cuadrada?","ops":["Más filas que col","Filas=columnas","Solo una fila","Elementos iguales"],"ok":1},
    {"cat":"Matrices","q":"A=[1,2], B=[3,4], A+B?","ops":["[4,6]","[3,8]","[2,4]","[1,6]"],"ok":0},
    {"cat":"Matrices","q":"La transpuesta intercambia","ops":["Filas por columnas","Sumas por restas","Signos","Diagonales"],"ok":0},
    {"cat":"Matrices","q":"Condición para multiplicar A x B","ops":["Ambas cuadradas","Col(A)=Fil(B)","Fil(A)=Fil(B)","A=B"],"ok":1},
    {"cat":"Matrices","q":"¿Qué es la matriz identidad?","ops":["Matriz ceros","Unos en diagonal","Triangular","Nula"],"ok":1},
    {"cat":"Matrices","q":"Si det(A)≠0, A es","ops":["Invertible","Singular","Identidad","Ortogonal"],"ok":0},
    {"cat":"Matrices","q":"Dimensión de producto 2x3 por 3x4","ops":["3x3","2x4","3x4","2x3"],"ok":1},
    {"cat":"Matrices","q":"Matriz triangular superior tiene","ops":["Todo cero","Ceros debajo diagonal","Ceros encima diagonal","Solo diagonal"],"ok":1},
    {"cat":"Matrices","q":"Traza de una matriz es","ops":["Determinante","Suma diagonal principal","Mayor elemento","Transpuesta"],"ok":1},
    {"cat":"Matrices","q":"det([[1,2],[3,4]])?","ops":["10","-2","2","-10"],"ok":1},
]

IND_COLOR  = {"economia":("#fbbf24","💰"),"medio_ambiente":("#34d399","🌿"),"energia":("#60a5fa","⚡"),"bienestar_social":("#f472b6","❤️")}
IND_LABEL  = {"economia":"Economía","medio_ambiente":"Medio Amb.","energia":"Energía","bienestar_social":"Bienestar"}
CAT_COLOR  = {"Python":"#6366f1","PSeInt":"#8b5cf6","Cálculo":"#06b6d4","Derivadas":"#10b981","Física MRU":"#f59e0b","Física MRUA":"#ef4444","Matrices":"#ec4899"}

DIFICULTADES = {
    "Fácil":   {"penalizacion": 5,  "evento_neg_peso": 1, "multiplicador": 0.7},
    "Normal":  {"penalizacion": 10, "evento_neg_peso": 2, "multiplicador": 1.0},
    "Difícil": {"penalizacion": 20, "evento_neg_peso": 3, "multiplicador": 1.3},
}

ATRIBUTOS = ["economia", "medio_ambiente", "energia", "bienestar_social"]
