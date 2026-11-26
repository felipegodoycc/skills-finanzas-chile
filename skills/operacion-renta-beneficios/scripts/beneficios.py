"""Beneficios de la Operación Renta del DL 824 (texto BCN vigente 01-11-2026).
Valores en UTA/UF que el usuario entrega; no se incluye ningún valor de UTA ni UF."""


def rebaja_intereses_hipotecarios(intereses, renta_bruta_uta, uta):
    """Art. 55 bis: monto a rebajar de la renta imponible. `intereses` y `uta` en pesos."""
    deducible = min(intereses, 8 * uta)
    if renta_bruta_uta < 90:
        return deducible
    if renta_bruta_uta > 150:
        return 0.0
    # entre 90 y 150 UTA (inclusive): porcentaje = 250 - 1,667 x renta en UTA
    # a 150 UTA la fórmula da -0,05% por el redondeo del factor 1,667: se corta en 0
    return max(0.0, deducible * (250 - 1.667 * renta_bruta_uta) / 100)


def credito_educacion(hijos_con_requisitos, uf, renta_padre_madre_uf):
    """Art. 55 ter: 4,4 UF por hijo; no procede si las rentas del padre y la madre superan 792 UF."""
    if renta_padre_madre_uf > 792:
        return 0.0
    return 4.4 * uf * hijos_con_requisitos


def gasto_presunto(ingresos_brutos, uta):
    """Art. 50: 30% de los ingresos brutos anuales, con tope de 15 UTA."""
    return min(0.30 * ingresos_brutos, 15 * uta)
