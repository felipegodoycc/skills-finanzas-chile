#!/usr/bin/env python3
"""Detecta cobros recurrentes (suscripciones) y gasto pequeño frecuente ("hormiga") en movimientos.

Entrada CSV con columnas: fecha (YYYY-MM-DD), monto (CLP, gasto positivo), comercio.
Definiciones OPERATIVAS de este repositorio (la CMF define "gasto hormiga" solo de forma
cualitativa: gasto no planificado fuera del presupuesto fijo; no da un monto):
- recurrente: >= 3 cobros del mismo comercio, intervalo mediano entre 26 y 35 días y montos
  dentro de +-10% de la mediana en >= 80% de los cobros.
- hormiga: comercio con monto mediano <= umbral (por defecto $10.000) y frecuencia >= 4 compras al mes.
Con menos de 12 meses de datos no se pueden detectar cobros anuales.

Uso: recurrentes.py --csv movimientos.csv [--umbral-hormiga 10000] [--frecuencia-minima 4]
"""
import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from datetime import date

AVISO = ("Herramienta de apoyo basada en IA; no es asesoría financiera. El umbral de 'hormiga' es una "
         "definición operativa, no una norma. Revisa cada ítem contigo: un gusto planificado no es una fuga.")


def normalizar(comercio):
    s = re.sub(r"[^a-záéíóúñ ]", " ", comercio.lower())
    return re.sub(r"\s+", " ", s).strip() or "sin_glosa"


def leer(path):
    movs = []
    with open(path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            movs.append({"fecha": date.fromisoformat(row["fecha"]),
                         "monto": float(row["monto"]), "comercio": normalizar(row["comercio"])})
    return movs


def analizar(movs, umbral_hormiga=10000, frecuencia_minima=4):
    if not movs:
        raise ValueError("sin movimientos")
    grupos = defaultdict(list)
    for m in movs:
        grupos[m["comercio"]].append(m)
    fechas = [m["fecha"] for m in movs]
    meses_datos = max(1, (max(fechas).year - min(fechas).year) * 12 + max(fechas).month - min(fechas).month + 1)
    recurrentes, hormiga = [], []
    for nombre, g in grupos.items():
        g.sort(key=lambda m: m["fecha"])
        montos = [m["monto"] for m in g]
        med = statistics.median(montos)
        total_mensual = sum(montos) / meses_datos
        if len(g) >= 3:
            inter = [(b["fecha"] - a["fecha"]).days for a, b in zip(g, g[1:])]
            estables = sum(1 for x in montos if med and abs(x - med) / med <= 0.10) / len(montos)
            if 26 <= statistics.median(inter) <= 35 and estables >= 0.8:
                recurrentes.append({"comercio": nombre, "cobros": len(g), "monto_mediano": round(med),
                                    "gasto_mensual": round(total_mensual), "gasto_anual": round(total_mensual * 12),
                                    "ultimo_cobro": g[-1]["fecha"].isoformat(),
                                    "pregunta": "¿Lo usaste en los últimos 30 días? Opciones: eliminar, reemplazar o controlar."})
        if med <= umbral_hormiga and len(g) / meses_datos >= frecuencia_minima:
            hormiga.append({"comercio": nombre, "compras": len(g),
                            "compras_por_mes": round(len(g) / meses_datos, 1), "monto_mediano": round(med),
                            "gasto_mensual": round(total_mensual), "gasto_anual": round(total_mensual * 12),
                            "pregunta": "¿Es planificado o automático? Opciones: tope semanal, reemplazo o eliminar."})
    recurrentes.sort(key=lambda x: -x["gasto_anual"])
    hormiga.sort(key=lambda x: -x["gasto_anual"])
    return {
        "meses_de_datos": meses_datos,
        "recurrentes": recurrentes,
        "total_recurrentes_mensual": sum(r["gasto_mensual"] for r in recurrentes),
        "hormiga": hormiga,
        "total_hormiga_mensual": sum(h["gasto_mensual"] for h in hormiga),
        "criterios": {"umbral_hormiga_clp": umbral_hormiga, "frecuencia_minima_mensual": frecuencia_minima,
                      "limite": "No detecta cobros anuales con <12 meses de datos."},
        "recordatorio": "Revisa primero las palancas grandes (vivienda, deuda, transporte); estos ítems suelen pesar menos.",
        "aviso": AVISO,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csv", required=True)
    p.add_argument("--umbral-hormiga", type=float, default=10000)
    p.add_argument("--frecuencia-minima", type=float, default=4)
    a = p.parse_args(argv)
    json.dump(analizar(leer(a.csv), a.umbral_hormiga, a.frecuencia_minima),
              sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
