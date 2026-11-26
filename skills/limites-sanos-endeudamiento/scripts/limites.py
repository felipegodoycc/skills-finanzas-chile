#!/usr/bin/env python3
"""Compara tu carga de deuda (RCI) con el umbral sostenible según tu tramo de ingreso.

Fuente de los umbrales: Lemus y Pulgar 2021/2023, MPRA 106958 (ver data/umbrales_lemus_pulgar_2021.json).
NO existe un umbral único sano: los umbrales suben con el ingreso y con la
deuda hipotecaria. Las bandas "holgado/cercano/sobre" son una convención de
este repositorio, no de la CMF.

Uso:
  limites.py --ingreso 1800000 --servicio-deuda 600000 --hipotecario
  limites.py --ingreso 900000 --servicio-deuda 250000 --deuda-sin-interes 4000000
"""
import argparse
import json
import os
import sys

AVISO = ("Herramienta de apoyo basada en IA; no es asesoría financiera ni crediticia regulada. "
         "Verifica cifras y condiciones con la entidad correspondiente.")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data",
                    "umbrales_lemus_pulgar_2021.json")


def interpolar(x, xs, ys):
    """Interpolación lineal con extremos fijos (sin extrapolar). Devuelve (valor, fuera_de_rango)."""
    if x <= xs[0]:
        return ys[0], x < xs[0]
    if x >= xs[-1]:
        return ys[-1], x > xs[-1]
    for i in range(1, len(xs)):
        if x <= xs[i]:
            t = (x - xs[i - 1]) / (xs[i] - xs[i - 1])
            return ys[i - 1] + t * (ys[i] - ys[i - 1]), False


def banda(ratio):
    if ratio < 0.7:
        return "holgado"
    if ratio < 1.0:
        return "cercano_al_umbral"
    return "sobre_el_umbral"


def evaluar(ingreso, servicio_deuda, hipotecario=False, deuda_sin_interes=None, datos=None):
    if ingreso <= 0:
        raise ValueError("ingreso debe ser > 0")
    if servicio_deuda < 0:
        raise ValueError("servicio_deuda no puede ser negativo")
    if datos is None:
        with open(DATA, encoding="utf-8") as f:
            datos = json.load(f)
    nodos = datos["nodos_con_hipotecario" if hipotecario else "nodos_sin_hipotecario"]
    xs = nodos["ingreso_mensual_clp"]
    rci = servicio_deuda / ingreso
    umbral_rci, fuera = interpolar(ingreso, xs, nodos["rci_maximo"])
    res = {
        "ingreso_mensual": ingreso,
        "servicio_deuda_mensual": servicio_deuda,
        "grupo": "con_hipotecario" if hipotecario else "sin_hipotecario",
        "rci": round(rci, 4),
        "umbral_rci_cmf_dt": round(umbral_rci, 4),
        "margen_rci_puntos": round((umbral_rci - rci) * 100, 1),
        "banda": banda(rci / umbral_rci) if umbral_rci > 0 else "sobre_el_umbral",
        "sobre_50pct_reporte_cmf": rci > datos["umbral_cmf_reporte"],
        "ingreso_fuera_del_rango_del_estudio": fuera,
    }
    if deuda_sin_interes is not None:
        rdi = deuda_sin_interes / ingreso
        umbral_rdi, _ = interpolar(ingreso, xs, nodos["rdi_maximo"])
        res.update({"rdi_veces_ingreso": round(rdi, 2),
                    "umbral_rdi_cmf_dt": round(umbral_rdi, 2),
                    "rdi_sobre_umbral": rdi > umbral_rdi})
    res["limitaciones"] = datos["limitaciones"]
    res["nota"] = ("Un RCI bajo el umbral NO prueba que tu deuda sea sana para tu caso: "
                   "depende de gastos fijos, dependientes y estabilidad del ingreso. "
                   "Sobre el umbral tampoco implica impago.")
    res["aviso"] = AVISO
    return res


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ingreso", type=float, required=True, help="Ingreso líquido mensual (CLP)")
    p.add_argument("--servicio-deuda", type=float, required=True,
                   help="Pago mensual total de deudas financieras, con intereses (CLP)")
    p.add_argument("--hipotecario", action="store_true", help="Tienes deuda hipotecaria")
    p.add_argument("--deuda-sin-interes", type=float, default=None,
                   help="Deuda total sin intereses futuros (CLP), opcional")
    a = p.parse_args(argv)
    json.dump(evaluar(a.ingreso, a.servicio_deuda, a.hipotecario, a.deuda_sin_interes),
              sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
