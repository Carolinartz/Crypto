def calcular_senal(variacion_24h):
    if variacion_24h is None:
        return "-"
    return "B" if variacion_24h > 0 else "S"
