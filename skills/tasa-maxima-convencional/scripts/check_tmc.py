#!/usr/bin/env python3
"""Compara la tasa de interés PACTADA de un crédito con la Tasa Máxima Convencional (TMC).

La TMC cambia cada mes (la fija la CMF según Ley 18.010 y se publica en el
Diario Oficial), por eso NO está escrita en el código: se lee de un archivo
de datos con fecha de vigencia (ver data/tmc.ejemplo.json).

La TMC aplica a los INTERESES pactados, no a la CAE (que incluye gastos y
seguros). No compares CAE contra TMC.

La base de anualización de las tasas de la CMF no está confirmada aquí: el
script calcula las dos formas (nominal x12 y compuesta) y avisa si el veredicto
depende de la forma. Confirma con la metodología vigente de la CMF.

Uso:
  check_tmc.py --datos data/tmc.json --tramo no_reaj_90d_hasta_50uf --tasa-mensual 0.032
"""
import argparse
import datetime as dt
import json
import sys

MAX_ANTIGUEDAD_DIAS = 45


def evaluar(datos, tramo, tasa_mensual, hoy=None):
    hoy = hoy or dt.date.today()
    vigencia = dt.date.fromisoformat(datos["vigencia_desde"])
    tramos = {t["clave"]: t for t in datos["tramos"]}
    if tramo not in tramos:
        raise KeyError(f"tramo '{tramo}' no existe; disponibles: {sorted(tramos)}")
    tmc = tramos[tramo]["tasa_anual_pct"] / 100.0
    nominal = tasa_mensual * 12
    compuesta = (1 + tasa_mensual) ** 12 - 1
    excede = {"nominal_x12": nominal > tmc, "compuesta": compuesta > tmc}
    antig = (hoy - vigencia).days
    return {
        "tmc_anual": tmc,
        "tasa_anual_nominal_x12": round(nominal, 5),
        "tasa_anual_compuesta": round(compuesta, 5),
        "excede_tmc": excede,
        "veredicto": ("EXCEDE" if all(excede.values()) else
                      "NO EXCEDE" if not any(excede.values()) else
                      "DEPENDE DE LA BASE: verificar metodología CMF"),
        "datos_vigentes_desde": datos["vigencia_desde"],
        "datos_desactualizados": antig > MAX_ANTIGUEDAD_DIAS,
        "fuente": datos.get("fuente"),
        "aviso": ("Datos con más de %d días: la TMC se publica mensualmente; "
                  "actualiza el archivo antes de concluir." % MAX_ANTIGUEDAD_DIAS)
                 if antig > MAX_ANTIGUEDAD_DIAS else None,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--datos", required=True)
    p.add_argument("--tramo", required=True)
    p.add_argument("--tasa-mensual", type=float, required=True,
                   help="interés pactado mensual, p. ej. 0.032 = 3,2%%")
    a = p.parse_args(argv)
    with open(a.datos, encoding="utf-8") as fh:
        datos = json.load(fh)
    json.dump(evaluar(datos, a.tramo, a.tasa_mensual), sys.stdout,
              ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
