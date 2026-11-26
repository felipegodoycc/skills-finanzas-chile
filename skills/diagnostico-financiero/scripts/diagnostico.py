#!/usr/bin/env python3
"""Diagnóstico inicial: flujo mensual, carga de deuda y qué skill usar después.

Entrada JSON:
{"ingreso_liquido": 1800000,
 "gastos": {"arriendo": 400000, "supermercado": 220000},      # SIN cuotas de deuda
 "deudas": [{"nombre": "consumo", "saldo": 3000000, "cuota": 120000, "tasa_mensual": 0.018, "tipo": "consumo"}],
 "liquidez": 1700000,
 "objetivos": ["salir de la rotativa", "comprar un computador"]}
Clasifica el problema: flujo negativo, flujo ajustado (< 5% del ingreso) o flujo positivo, y entrega el
orden recomendado de skills. Si el flujo es negativo, ninguna consolidación lo resuelve por sí sola.

Uso: diagnostico.py --json datos.json
"""
import argparse
import json
import sys

AVISO = ("Soy un asesor basado en IA, no un asesor financiero, tributario ni legal regulado. La información "
         "debe verificarse con la entidad correspondiente. No recomiendo bancos, tarjetas, créditos ni inversiones concretas.")
OBJETIVO_A_SKILL = [
    (("rotativa", "deuda", "consolid", "refinanc", "renegoc", "portab"), "plan-refinanciamiento"),
    (("presupuesto", "gastos", "ahorrar", "ahorro"), "presupuesto-personal"),
    (("suscrip", "hormiga", "recurrent"), "analisis-gasto-recurrente"),
    (("emergencia", "colchón", "colchon", "meta"), "fondo-emergencia-y-metas"),
    (("cotiz", "comparar", "mejor tarjeta", "mejor crédito", "mejor credito", "hipotec"), "cotizacion-y-comparacion"),
    (("mínimo", "minimo", "tarjeta"), "pago-minimo-tarjetas"),
    (("comprar", "compra"), "fondo-emergencia-y-metas"),
]


def diagnosticar(d):
    ingreso = d["ingreso_liquido"]
    if ingreso <= 0:
        raise ValueError("ingreso_liquido debe ser > 0")
    gastos = sum(d.get("gastos", {}).values())
    deudas = d.get("deudas", [])
    servicio = sum(x["cuota"] for x in deudas)
    flujo = ingreso - gastos - servicio
    rci = servicio / ingreso
    if flujo < 0:
        tipo = "flujo_negativo"
        lectura = "Gastas más de lo que entra. Primero el flujo (gasto, ingreso); consolidar no cierra este hoyo."
    elif flujo < 0.05 * ingreso:
        tipo = "flujo_ajustado"
        lectura = "Sobra menos de 5% del ingreso: cualquier imprevisto genera deuda nueva."
    else:
        tipo = "flujo_positivo"
        lectura = "Hay holgura: el foco es el costo de la deuda y el colchón."
    caras = sorted((x for x in deudas if x.get("tasa_mensual") is not None), key=lambda x: -x["tasa_mensual"])
    orden = ["limites-sanos-endeudamiento"]
    if tipo != "flujo_positivo":
        orden += ["presupuesto-personal", "analisis-gasto-recurrente"]
    if deudas:
        orden.append("plan-refinanciamiento")
    for claves, skill in OBJETIVO_A_SKILL:
        if any(c in o.lower() for o in d.get("objetivos", []) for c in claves) and skill not in orden:
            orden.append(skill)
    preguntas = []
    if not d.get("objetivos"):
        preguntas.append("¿Cuál es tu objetivo principal (bajar deuda, ahorrar, comprar algo, ordenar el mes)?")
    if d.get("liquidez") is None:
        preguntas.append("¿Cuánto dinero líquido tienes hoy?")
    preguntas += ["¿Qué ingresos son seguros y cuáles variables?",
                  "¿Hay gastos que no están en la lista (arriendo, pensión, tarjetas adicionales)?",
                  "¿Alguna deuda está en mora?"]
    return {"flujo_mensual": round(flujo), "servicio_deuda": round(servicio), "rci": round(rci, 4),
            "gasto_mensual": round(gastos), "tipo_de_problema": tipo, "lectura": lectura,
            "deudas_por_costo_mensual": [{"nombre": x["nombre"], "tasa_mensual": x["tasa_mensual"]} for x in caras],
            "skills_en_orden": orden, "preguntas_pendientes": preguntas,
            "regla": "Antes de proponer cualquier acción: confirma los datos con el usuario y sus metas.",
            "aviso": AVISO}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", required=True)
    a = p.parse_args(argv)
    with open(a.json, encoding="utf-8") as f:
        json.dump(diagnosticar(json.load(f)), sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
