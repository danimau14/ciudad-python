def aplicar_efectos(indicadores, efectos):
    nuevo = dict(indicadores)
    for k, v in efectos.items():
        if k in nuevo:
            nuevo[k] = max(0, min(100, nuevo[k] + v))
    return nuevo
