#!/usr/bin/env python3
"""Compara cotizaciones de crédito de distintas entidades por costo total (CAE y CTC).

Entrada: JSON con una lista de cotizaciones:
  [{"entidad":"Entidad A","producto":"consumo","monto":3000000,"n":36,"cuota":118000,
    "gastos_descontados":0,"gastos_aparte":0,"fecha_emision":"2026-11-20",
    "cae_informada":0.2150,"tasa_anual_informada":0.19}, ...]
- monto: monto solicitado; gastos_descontados: se restan del desembolso;
  gastos_aparte: se pagan al inicio fuera de las cuotas; cuota: incluye seguros si van en la cuota.
- CAE = tasa periódica de la ecuación de flujos x 12 (misma base que cae.py de credito-cae-ctc).
- CTC = cuota x n + gastos_aparte.

Esta herramienta compara; la CAE/CTC vinculante es la de la hoja resumen de cotización
(Ley 20.555). No declara "el mejor banco": solo el menor costo bajo estos datos.
Vigencia: 7 días hábiles (Sernac); se cuentan lunes a viernes SIN feriados (límite conocido).

Uso:
  comparar.py --json cotizaciones.json --hoy 2026-11-26 [--tmc 0.34]
"""
import argparse
import json
import sys
from datetime import date, timedelta

AVISO = ("Herramienta de apoyo basada en IA; no es asesoría financiera ni crediticia regulada y no "
         "recomienda entidades. Verifica cada condición con la entidad y pide la hoja resumen de cotización.")
VIGENCIA_DIAS_HABILES = 7
TOLERANCIA_CAE = 0.005  # 0,5 puntos porcentuales


def tasa_periodica(neto, cuota, n):
    """i que cumple neto = suma_{t=1..n} cuota/(1+i)^t (bisección)."""
    if neto <= 0 or cuota <= 0 or n <= 0:
        raise ValueError("neto, cuota y n deben ser > 0")
    if cuota * n < neto:
        raise ValueError("la suma de cuotas es menor que el monto recibido")
    lo, hi = 0.0, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        vp = sum(cuota / (1 + mid) ** t for t in range(1, n + 1))
        if vp > neto:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def dias_habiles(desde, hasta):
    """Días hábiles (lun-vie) transcurridos entre dos fechas, sin feriados."""
    d, c = desde, 0
    while d < hasta:
        d += timedelta(days=1)
        if d.weekday() < 5:
            c += 1
    return c


def analizar(c, hoy):
    neto = c["monto"] - c.get("gastos_descontados", 0) - c.get("gastos_aparte", 0)
    i = tasa_periodica(neto, c["cuota"], c["n"])
    ctc = c["cuota"] * c["n"] + c.get("gastos_aparte", 0)
    r = {
        "entidad": c["entidad"], "producto": c.get("producto"), "monto": c["monto"], "n": c["n"],
        "cuota": c["cuota"], "ctc": round(ctc),
        "costo_total_sobre_monto": round(ctc - c["monto"]),
        "cae_calculada": round(i * 12, 4),
        "tasa_efectiva_anual_calculada": round((1 + i) ** 12 - 1, 4),
        "alertas": [],
    }
    if c.get("cae_informada") is not None and abs(c["cae_informada"] - r["cae_calculada"]) > TOLERANCIA_CAE:
        r["alertas"].append("CAE informada (%.2f%%) difiere de la calculada (%.2f%%): revisa seguros, gastos o la hoja resumen"
                            % (c["cae_informada"] * 100, r["cae_calculada"] * 100))
    if c.get("fecha_emision"):
        dh = dias_habiles(date.fromisoformat(c["fecha_emision"]), hoy)
        r["dias_habiles_desde_emision"] = dh
        if dh > VIGENCIA_DIAS_HABILES:
            r["alertas"].append("cotización vencida (más de 7 días hábiles; sin feriados): pide una nueva")
    else:
        r["alertas"].append("sin fecha de emisión: no se puede verificar vigencia")
    return r


def comparar(cotizaciones, hoy, tmc=None):
    if len(cotizaciones) < 2:
        raise ValueError("se necesitan al menos 2 cotizaciones")
    base_m, base_n = cotizaciones[0]["monto"], cotizaciones[0]["n"]
    filas = [analizar(c, hoy) for c in cotizaciones]
    comparables = all(c["monto"] == base_m and c["n"] == base_n for c in cotizaciones)
    for f in filas:
        if tmc is not None and f["cae_calculada"] > tmc:
            f["alertas"].append("CAE calculada sobre la TMC indicada: revisa si el cobro es legal")
    filas.sort(key=lambda f: f["ctc"])
    out = {"comparables": comparables, "filas": filas, "aviso": AVISO}
    if not comparables:
        out["advertencia"] = ("Monto o plazo distintos: CAE y CTC NO son comparables entre sí. "
                              "Pide cotizaciones con el mismo monto y plazo.")
    else:
        out["diferencia_ctc_mayor_menor"] = filas[-1]["ctc"] - filas[0]["ctc"]
        out["menor_ctc_bajo_estos_datos"] = filas[0]["entidad"]
        out["preguntas_para_la_entidad"] = [
            "¿La cuota incluye seguro de desgravamen? ¿Es obligatorio u opcional?",
            "¿Hay comisión de prepago o de administración?",
            "¿La tasa queda fija durante la vigencia de la cotización (7 días hábiles)?",
            "Entrégame la hoja resumen de cotización con CAE y CTC.",
        ]
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", required=True)
    p.add_argument("--hoy", default=date.today().isoformat())
    p.add_argument("--tmc", type=float, default=None, help="TMC vigente en fracción (0.34 = 34%)")
    a = p.parse_args(argv)
    with open(a.json, encoding="utf-8") as f:
        data = json.load(f)
    json.dump(comparar(data, date.fromisoformat(a.hoy), a.tmc), sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
