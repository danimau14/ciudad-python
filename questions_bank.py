_TOPICS = [
    "Python",
    "PSeInt",
    "Calculo",
    "Fisica",
    "Matrices",
    "Introduccion Ingenieria de Sistemas",
    "Pensamiento Sistemico",
]

_TEMPLATES = {
    "facil": [
        ("Concepto basico de {topic}.", ["Opcion A", "Opcion B", "Opcion C", "Opcion D"], 1),
        ("Definicion principal en {topic}.", ["Incorrecta", "Correcta", "Parcial", "Ninguna"], 1),
        ("Aplicacion elemental de {topic}.", ["Error", "Valida", "Invalida", "Ambigua"], 1),
        ("Identifica la afirmacion correcta de {topic}.", ["Falsa", "Verdadera", "Depende", "No aplica"], 1),
    ],
    "normal": [
        ("Analiza este caso de {topic} y elige la opcion correcta.", ["A", "B", "C", "D"], 2),
        ("Relacion entre dos conceptos de {topic}.", ["Incorrecta", "Parcial", "Correcta", "No definida"], 2),
        ("Escenario intermedio en {topic}.", ["Alternativa 1", "Alternativa 2", "Alternativa 3", "Alternativa 4"], 2),
        ("Selecciona la respuesta mas precisa en {topic}.", ["Baja", "Media", "Alta", "Nula"], 2),
    ],
    "dificil": [
        ("Caso avanzado de {topic} con analisis integrado.", ["Hipotesis 1", "Hipotesis 2", "Hipotesis 3", "Hipotesis 4"], 3),
        ("Determina la mejor decision tecnica en {topic}.", ["Aproximacion A", "Aproximacion B", "Aproximacion C", "Aproximacion D"], 3),
        ("Evaluacion de impacto sistemico en {topic}.", ["Minimo", "Moderado", "Alto", "Critico"], 3),
        ("Pregunta de juicio experto en {topic}.", ["Opc 1", "Opc 2", "Opc 3", "Opc 4"], 3),
    ],
}


def _build_level(level_key):
    rows = []
    i = 0
    while len(rows) < 100:
        topic = _TOPICS[i % len(_TOPICS)]
        base_q, base_ops, ok = _TEMPLATES[level_key][(i // len(_TOPICS)) % len(_TEMPLATES[level_key])]
        rows.append(
            {
                "cat": topic,
                "q": f"{base_q.format(topic=topic)} [{level_key.upper()} #{len(rows)+1}]",
                "ops": base_ops,
                "dif": level_key,
                "ok": ok,
            }
        )
        i += 1
    return rows


PREGUNTAS = _build_level("facil") + _build_level("normal") + _build_level("dificil")
