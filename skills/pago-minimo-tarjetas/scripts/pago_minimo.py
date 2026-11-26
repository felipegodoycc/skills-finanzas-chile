#!/usr/bin/env python3
"""Pago mínimo de tarjetas de crédito según la NCG 537 de la CMF (Ley 21.673).

Fórmula (NCG 537 de la CMF, 04-06-2025, numerales 5.2 y 7): pago_minimo = 100% del Monto No Financiable (MNF)
+ 5% del Monto Financiable (MF). Es un PISO: el emisor puede exigir más.
- MNF = cuotas sin interés (en la proporción que corresponda a la etapa) + intereses + comisiones + otros cargos.
- MF  = remanente del monto facturado.

Calendario de las cuotas sin interés dentro del MNF:
  desde 04-06-2026: 0%   (NORMA: entra solo 5% de su valor, por estar en el MF)
  04-12-2026: 25%, 04-06-2027: 50%, 04-12-2027: 75%   (NORMA: "luego de 6, 12 y 18 meses"; fechas contadas desde 04-06-2026)
  04-06-2028: 100%       (NORMA)
Antes del 04-06-2026 el emisor aplicaba su propia regla: esta herramienta no la modela.
Texto de la NCG 537 leído completo. Las excepciones (máx. 24 meses de amortización y 2 meses consecutivos) dependen de la política de cada emisor; esta herramienta no las modela.

Uso:
  pago_minimo.py calcular --cargos 60000 --cuotas-sin-interes 200000 --otros 600000 --fecha 2026-12-20
  pago_minimo.py solo-minimo --saldo 1000000 --tasa-mensual 0.025
  pago_minimo.py proyectar --json plan.json --flujo 400000
"""
import argparse
import json
import math
import sys
from datetime import date

AVISO = ("Herramienta de apoyo basada en IA; no es asesoría financiera. "
         "Verifica el cálculo con tu emisor y con la NCG 537 de la CMF.")
INICIO = date(2026, 6, 4)
ETAPAS = [  # (desde, fracción de cuotas sin interés en el MNF, estatus de la fecha)
    (date(2026, 6, 4), 0.0, "norma"),
    (date(2026, 12, 4), 0.25, "norma"),
    (date(2027, 6, 4), 0.50, "norma"),
    (date(2027, 12, 4), 0.75, "norma"),
    (date(2028, 6, 4), 1.00, "norma"),
]
PCT_FINANCIABLE = 0.05


def etapa(fecha):
    if fecha < INICIO:
        raise ValueError("Antes del 04-06-2026 aplica la regla previa de cada emisor; no se modela")
    actual = ETAPAS[0]
    for e in ETAPAS:
        if fecha >= e[0]:
            actual = e
    return actual


def pago_minimo(cargos, cuotas_sin_interes, otros_financiable, fecha):
    """cargos = intereses + comisiones + otros cargos del período; otros_financiable = resto facturado."""
    for nombre, v in (("cargos", cargos), ("cuotas_sin_interes", cuotas_sin_interes),
                      ("otros_financiable", otros_financiable)):
        if v < 0:
            raise ValueError(nombre + " no puede ser negativo")
    desde, frac, estatus = etapa(fecha)
    mnf = cargos + frac * cuotas_sin_interes
    mf = otros_financiable + (1 - frac) * cuotas_sin_interes
    minimo = mnf + PCT_FINANCIABLE * mf
    total = cargos + cuotas_sin_interes + otros_financiable
    return {
        "fecha": fecha.isoformat(),
        "fraccion_cuotas_sin_interes_en_mnf": frac,
        "estatus_de_la_fecha_del_calendario": estatus,
        "monto_no_financiable": round(mnf),
        "monto_financiable": round(mf),
        "pago_minimo": round(minimo),
        "pct_del_total_facturado": round(minimo / total, 4) if total else 0,
        "nota": "Piso de la norma: tu emisor puede fijar un mínimo mayor.",
        "aviso": AVISO,
    }


def solo_minimo(saldo, tasa_mensual, cargos_mensuales=0.0, max_meses=1200):
    """Simula pagar solo el mínimo sobre un saldo rotativo SIN nuevas compras.
    Cada mes: intereses = saldo*tasa; mínimo = intereses + cargos + 5% del saldo."""
    if saldo <= 0 or tasa_mensual < 0:
        raise ValueError("saldo debe ser > 0 y tasa_mensual >= 0")
    meses, intereses_tot, pagado = 0, 0.0, 0.0
    s = saldo
    while s >= 1 and meses < max_meses:
        i = s * tasa_mensual
        minimo = i + cargos_mensuales + PCT_FINANCIABLE * s
        s -= PCT_FINANCIABLE * s
        intereses_tot += i
        pagado += minimo
        meses += 1
    return {"meses_para_saldar": meses,
            "intereses_total": round(intereses_tot),
            "cargos_total": round(cargos_mensuales * meses),
            "total_pagado": round(pagado),
            "primer_minimo": round(saldo * tasa_mensual + cargos_mensuales + PCT_FINANCIABLE * saldo),
            "supuestos": "Sin compras nuevas, tasa y cargos constantes, mínimo = intereses + cargos + 5% del saldo.",
            "aviso": AVISO}


def proyectar(meses, flujo_disponible):
    """meses: [{mes:'2026-12', dia:15, cargos, cuotas_sin_interes, otros_financiable, flujo(opc)}]."""
    out = []
    for m in meses:
        y, mo = (int(x) for x in m["mes"].split("-"))
        r = pago_minimo(m.get("cargos", 0), m.get("cuotas_sin_interes", 0),
                        m.get("otros_financiable", 0), date(y, mo, m.get("dia", 15)))
        flujo = m.get("flujo", flujo_disponible)
        r["mes"] = m["mes"]
        r["flujo_disponible"] = flujo
        r["alerta_minimo_supera_flujo"] = flujo is not None and r["pago_minimo"] > flujo
        out.append(r)
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("calcular")
    c.add_argument("--cargos", type=float, default=0)
    c.add_argument("--cuotas-sin-interes", type=float, default=0)
    c.add_argument("--otros", type=float, default=0)
    c.add_argument("--fecha", required=True, help="YYYY-MM-DD")
    s = sub.add_parser("solo-minimo")
    s.add_argument("--saldo", type=float, required=True)
    s.add_argument("--tasa-mensual", type=float, required=True)
    s.add_argument("--cargos-mensuales", type=float, default=0)
    q = sub.add_parser("proyectar")
    q.add_argument("--json", required=True, help="Archivo con la lista de meses")
    q.add_argument("--flujo", type=float, default=None)
    a = p.parse_args(argv)
    if a.cmd == "calcular":
        r = pago_minimo(a.cargos, a.cuotas_sin_interes, a.otros, date.fromisoformat(a.fecha))
    elif a.cmd == "solo-minimo":
        r = solo_minimo(a.saldo, a.tasa_mensual, a.cargos_mensuales)
    else:
        with open(a.json, encoding="utf-8") as f:
            r = proyectar(json.load(f), a.flujo)
    json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
