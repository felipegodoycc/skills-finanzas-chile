#!/usr/bin/env python3
"""Indicadores de endeudamiento con las definiciones del Informe de Endeudamiento de la CMF.

- carga_financiera = servicio mensual de deuda financiera / ingreso líquido mensual
- apalancamiento   = deuda financiera total / ingreso mensual (veces el ingreso)
- alta_carga       = carga_financiera > 0.50 (umbral que usa la CMF para
                     "alta carga financiera / sobreendeudamiento")

ADVERTENCIA: 50% es un umbral de ALERTA usado para reportar, no una meta
saludable. Las cifras de referencia (medianas) son descriptivas, no normas.

Uso:
  indicadores.py --ingreso 1500000 --servicio-deuda 300000 --deuda-total 6000000
"""
import argparse
import json
import sys

UMBRAL_ALTA_CARGA = 0.50

# Mediana nacional, deudores del Informe de Endeudamiento CMF 2025 (jun-2025).
# Fuente: https://www.cmfchile.cl/portal/prensa/615/articles-102984_doc_pdf.pdf
REFERENCIA_CMF_JUN_2025 = {
    "deuda_mediana_clp_jun2025": 1680453,
    "carga_financiera_mediana": 0.119,
    "apalancamiento_mediano": 1.9,
    "pct_deudores_alta_carga": 0.141,
    "nota": "Datos descriptivos de deudores formales (cobertura ~84%). No son metas.",
}


def indicadores(ingreso, servicio_deuda, deuda_total):
    if ingreso <= 0:
        raise ValueError("ingreso debe ser > 0")
    carga = servicio_deuda / ingreso
    apal = deuda_total / ingreso
    return {
        "carga_financiera": round(carga, 4),
        "apalancamiento_veces_ingreso": round(apal, 2),
        "alta_carga_cmf": carga > UMBRAL_ALTA_CARGA,
        "umbral_alta_carga": UMBRAL_ALTA_CARGA,
        "referencia": REFERENCIA_CMF_JUN_2025,
        "advertencia": ("Usa ingreso LÍQUIDO y servicio de deuda FINANCIERA "
                        "(créditos, tarjetas, líneas). Un valor bajo el umbral no "
                        "implica que la deuda sea sostenible para tu caso."),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ingreso", type=float, required=True)
    p.add_argument("--servicio-deuda", type=float, required=True)
    p.add_argument("--deuda-total", type=float, required=True)
    a = p.parse_args(argv)
    json.dump(indicadores(a.ingreso, a.servicio_deuda, a.deuda_total),
              sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
