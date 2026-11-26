"""Cálculos de la Ley 21.735 que se pueden hacer sin datos actuariales (arts. 7 y 10)."""

TOPE_MESES = 300  # art. 7: máximo de meses de cotización computables
UF_POR_12_MESES = 0.1  # art. 7: 0,1 UF mensual por cada 12 meses cotizados


def beneficio_anos_cotizados_bruto_uf(meses, jornada=1.0):
    """Tope mensual del beneficio por años cotizados, en UF, antes de restar la anualidad.

    El beneficio real es este monto menos la anualidad que generan las cotizaciones de
    cargo del empleador a la cuenta individual (art. 7); sin datos actuariales no se
    puede calcular el neto. jornada: proporción de jornada completa (0 a 1).
    """
    if meses < 0 or not 0 <= jornada <= 1:
        raise ValueError("meses >= 0 y jornada entre 0 y 1")
    return UF_POR_12_MESES * min(meses, TOPE_MESES) / 12 * jornada


def factor_compensacion(edad_pension):
    """Fracción de la compensación por expectativa de vida, mujer pensionada por vejez (art. 10 N° 1)."""
    tabla = {65: 1.0, 64: 0.75, 63: 0.5, 62: 0.25, 61: 0.15, 60: 0.05}
    if edad_pension >= 65:
        return 1.0
    return tabla.get(edad_pension, 0.0)  # antes de los 60 no hay compensación (art. 10 N° 1)
