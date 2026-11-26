"""Rentabilidad real y anualización para comparar ahorro de bajo riesgo. Stdlib, sin datos de mercado."""


def tasa_real(nominal, inflacion):
    """Fisher exacta: (1+nominal)/(1+inflacion)-1. Ambas tasas anuales en decimal."""
    return (1 + nominal) / (1 + inflacion) - 1


def anualizar(tasa_periodo, dias):
    """Efectiva anual compuesta de una tasa pagada al cabo de `dias` (base 365)."""
    if dias <= 0:
        raise ValueError("dias debe ser positivo")
    return (1 + tasa_periodo) ** (365 / dias) - 1


def tasa_dap_uf_a_nominal(tasa_real_anual, inflacion_esperada):
    """Tasa nominal equivalente de un depósito en UF, dada una inflación supuesta (no es un dato, es un escenario)."""
    return (1 + tasa_real_anual) * (1 + inflacion_esperada) - 1
