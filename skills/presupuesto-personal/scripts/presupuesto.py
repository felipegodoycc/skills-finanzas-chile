#!/usr/bin/env python3
"""Presupuesto de régimen estable y de transición mes a mes.

Entrada (JSON):
{
 "ingreso_mensual": 1800000,                 # líquido estable (sin bonos)
 "fijos": {"arriendo": 400000, "servicios": 120000},
 "cuotas_pactadas": {"2026-12": 300000, "2027-01": 250000, "2027-02": 100000},
 "variable_actual": {"supermercado": 220000, "restaurantes": 270000},   # promedio real
 "metas": {"supermercado": 220000, "restaurantes": 150000},
 "meses_para_la_meta": 4
}
Idea: el margen para gasto variable de cada mes = ingreso - fijos - cuotas pactadas. El límite de
alerta de cada categoría baja de forma lineal desde el promedio real hasta la meta en N meses
(una meta igual a cero margen desde el día 1 genera alertas diarias que se ignoran).
Los bonos y el aguinaldo NO cuentan como ingreso mensual.

Uso: presupuesto.py --json plan.json
"""
import argparse
import json
import sys

AVISO = ("Herramienta de apoyo basada en IA; no es asesoría financiera. Las metas son propuestas "
         "tuyas o de la herramienta, no datos ni normas.")


def planificar(d):
    ingreso = d["ingreso_mensual"]
    if ingreso <= 0:
        raise ValueError("ingreso_mensual debe ser > 0")
    fijos = sum(d["fijos"].values())
    actual = d["variable_actual"]
    metas = d.get("metas", actual)
    n = max(1, int(d.get("meses_para_la_meta", 3)))
    cuotas = d.get("cuotas_pactadas", {})
    total_actual, total_meta = sum(actual.values()), sum(metas.get(k, v) for k, v in actual.items())
    meses, acumulado, peor = [], 0.0, 0.0
    for k, mes in enumerate(sorted(cuotas), start=1):
        margen = ingreso - fijos - cuotas[mes]
        paso = min(k, n) / n
        limites = {c: round(v + (metas.get(c, v) - v) * paso) for c, v in actual.items()}
        lim_total = sum(limites.values())
        brecha = margen - lim_total
        acumulado += brecha
        peor = min(peor, acumulado)
        meses.append({"mes": mes, "cuotas_pactadas": cuotas[mes], "margen_para_variable": round(margen),
                      "limite_variable_total": lim_total, "brecha": round(brecha),
                      "brecha_acumulada": round(acumulado), "limites_por_categoria": limites})
    margen_reg = ingreso - fijos
    return {
        "regimen_estable": {"margen_para_variable": round(margen_reg),
                            "meta_variable_total": round(total_meta),
                            "ahorro_posible": round(margen_reg - total_meta),
                            "gasto_variable_actual": round(total_actual),
                            "recorte_necesario": round(total_actual - total_meta),
                            "recorte_pct": round(1 - total_meta / total_actual, 3) if total_actual else 0},
        "transicion": meses,
        "colchon_requerido_para_cubrir_transicion": round(-peor),
        "supuestos": ["Ingreso estable sin bonos", "Cuotas pactadas conocidas", "Promedios reales de movimientos limpios"],
        "aviso": AVISO,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", required=True)
    a = p.parse_args(argv)
    with open(a.json, encoding="utf-8") as f:
        json.dump(planificar(json.load(f)), sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
