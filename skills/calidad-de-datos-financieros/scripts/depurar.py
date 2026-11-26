#!/usr/bin/env python3
"""Depuración de movimientos: duplicados tiempo real/cartola y reembolsos de tarjeta adicional.

Formato genérico de movimiento (JSON/dict):
  {"id": 1, "fecha": "2026-10-05", "monto": 12000, "tipo": "gasto|ingreso|traspaso",
   "producto": "tarjeta-A", "fuente": "tiempo_real|cartola", "contraparte": "opcional"}

Reglas (nunca se borra nada: solo se marca y se explica):
1. Duplicado tiempo real/cartola: misma monto y producto, y la fecha de la compra en tiempo real cae
   entre 4 días ANTES y 2 días DESPUÉS de la línea de cartola (la cartola es posterior). Se conserva
   la fila de la cartola. Cada línea se enlaza 1 a 1 con la más cercana en fecha (una ventana
   simétrica de ±4 puede cruzar compras iguales).
2. Reembolso: una transferencia ENTRANTE de una contraparte indicada que paga una tarjeta adicional
   facturada dentro de tu estado se registra como devolución (monto negativo del gasto), no ingreso.
3. Verificación: compara el reembolso contra el total de la tarjeta adicional en el estado y declara la brecha.

Uso: depurar.py --json movimientos.json [--contrapartes "Contraparte X"]
"""
import argparse
import json
import sys
from datetime import date

AVISO = ("Herramienta de apoyo basada en IA. Las marcas son propuestas: revisa los casos dudosos con tus "
         "propios estados antes de aplicarlas. No se borra ningún dato.")
ANTES, DESPUES = 4, 2


def _f(m):
    return date.fromisoformat(m["fecha"]) if isinstance(m["fecha"], str) else m["fecha"]


def marcar_duplicados(movs):
    """Devuelve lista de pares {conservar, duplicado, dias} (conservar = cartola)."""
    cartola = sorted((m for m in movs if m.get("fuente") == "cartola"), key=_f)
    rt = [m for m in movs if m.get("fuente") == "tiempo_real"]
    usados, pares = set(), []
    for c in cartola:
        mejor, mejor_d = None, None
        for r in rt:
            if r["id"] in usados or r["monto"] != c["monto"] or r.get("producto") != c.get("producto"):
                continue
            dias = (_f(c) - _f(r)).days  # >0: la compra en tiempo real es anterior
            if -DESPUES <= dias <= ANTES:
                clave = (abs(dias), dias < 0)
                if mejor is None or clave < mejor_d:
                    mejor, mejor_d = r, clave
        if mejor is not None:
            usados.add(mejor["id"])
            pares.append({"conservar": c["id"], "duplicado": mejor["id"], "dias_de_diferencia": (_f(c) - _f(mejor)).days})
    return pares


def netear_reembolsos(movs, contrapartes):
    """Marca ingresos de contrapartes como devolución con monto negativo del gasto."""
    cambios = []
    for m in movs:
        if m.get("tipo") == "ingreso" and m.get("contraparte") in contrapartes:
            cambios.append({"id": m["id"], "tipo_nuevo": "gasto/devolucion", "monto_nuevo": -abs(m["monto"])})
    return cambios


def verificar_reembolso(total_tarjeta_adicional, reembolso, descuento_acordado=0):
    esperado = total_tarjeta_adicional - descuento_acordado
    brecha = reembolso - esperado
    return {"esperado": esperado, "reembolso": reembolso, "brecha": brecha,
            "estado": "calza" if brecha == 0 else "estimacion: brecha sin explicar, no la fuerces"}


def depurar(movs, contrapartes=()):
    pares = marcar_duplicados(movs)
    return {"duplicados": pares, "reembolsos": netear_reembolsos(movs, set(contrapartes)),
            "sin_enlazar_tiempo_real": [m["id"] for m in movs if m.get("fuente") == "tiempo_real"
                                         and m["id"] not in {p["duplicado"] for p in pares}],
            "aviso": AVISO}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", required=True)
    p.add_argument("--contrapartes", default="", help="Nombres separados por ';'")
    a = p.parse_args(argv)
    with open(a.json, encoding="utf-8") as f:
        movs = json.load(f)
    json.dump(depurar(movs, [x for x in a.contrapartes.split(";") if x]), sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
