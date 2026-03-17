def aplicar_efectos(indicadores, efectos):
    nuevo = dict(indicadores)
    for k, v in efectos.items():
        if k in nuevo:
            nuevo[k] = max(0, min(100, nuevo[k] + v))
    return nuevo


def penalizacion_incorrecta(dificultad, ronda):
    base = {"Fácil": 10, "Medio": 15, "Difícil": 20}.get(dificultad, 15)
    if ronda % 2 == 0:
        base *= 2  # rondas pares: doble penalización
    return base


def aplicar_penalizacion(indicadores, dificultad, ronda):
    pen = penalizacion_incorrecta(dificultad, ronda)
    return {k: max(0, v - pen) for k, v in indicadores.items()}
