#!/usr/bin/env python3
"""Colchón de emergencia: meses cubiertos, metas por tramos y tiempo para alcanzarlas.

Las metas son HEURÍSTICAS: la CMF no da una cantidad de meses; "3 a 6 meses" es una convención;
JPMorgan Chase Institute (EE.UU.) sugiere ~6 semanas de ingreso neto para volatilidad típica y más si
el ingreso es volátil. Aplicabilidad a Chile no verificada. El Seguro de Cesantía (AFC) es un
complemento para quienes tienen contrato indefinido; no reemplaza el colchón.

Entrada JSON:
{"gastos_esenciales_mensuales": 1300000, "liquido": 1700000, "no_liquido": 1900000,
 "ingreso_neto_mensual": 1900000, "ingreso_variable": false,
 "aporte_mensual": 0, "liberaciones": [{"desde_mes": 3, "monto": 120000}], "piso_meses": 1.5}
liberaciones: dinero que se libera (cuotas que terminan) y se transfiere al colchón desde el mes indicado.

Uso: colchon.py --json datos.json
"""
import argparse
import json
import sys

AVISO = ("Herramienta de apoyo basada en IA; no es asesoría financiera. Las metas de meses son "
         "heurísticas, no normas ni recomendaciones de la CMF.")


def meses_para_meta(meta, inicial, aporte, liberaciones, tope=360):
    saldo, m = inicial, 0
    while saldo < meta and m < tope:
        m += 1
        saldo += aporte + sum(x["monto"] for x in liberaciones if m >= x["desde_mes"])
    return m if saldo >= meta else None


def evaluar(d):
    g = d["gastos_esenciales_mensuales"]
    if g <= 0:
        raise ValueError("gastos_esenciales_mensuales debe ser > 0")
    liquido, no_liq = d["liquido"], d.get("no_liquido", 0)
    metas_meses = [3, 6] if not d.get("ingreso_variable") else [6, 9]
    metas = {"piso": d.get("piso_meses", 1.0) * g, "1_mes": g}
    for mm in metas_meses:
        metas["%d_meses" % mm] = mm * g
    if d.get("ingreso_neto_mensual"):
        metas["referencia_6_semanas_ingreso_neto_EEUU"] = 1.5 * d["ingreso_neto_mensual"]
    out = {"meses_cubiertos_liquido": round(liquido / g, 2),
           "meses_cubiertos_total_con_no_liquido": round((liquido + no_liq) / g, 2),
           "nota_no_liquido": "El no líquido (renta variable, plazos de rescate) puede perder valor o demorar al rescatarlo.",
           "metas": {}}
    for k, meta in metas.items():
        m = meses_para_meta(meta, liquido, d.get("aporte_mensual", 0), d.get("liberaciones", []))
        out["metas"][k] = {"monto": round(meta), "falta": round(max(0, meta - liquido)),
                           "meses_para_alcanzar": m}
    out["bajo_el_piso"] = liquido < metas["piso"]
    out["supuestos"] = ["Gastos esenciales = lo que no puedes dejar de pagar en 1 mes sin consecuencias graves",
                        "Aporte y liberaciones constantes", "Sin rentabilidad ni inflación"]
    out["aviso"] = AVISO
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", required=True)
    a = p.parse_args(argv)
    with open(a.json, encoding="utf-8") as f:
        json.dump(evaluar(json.load(f)), sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
