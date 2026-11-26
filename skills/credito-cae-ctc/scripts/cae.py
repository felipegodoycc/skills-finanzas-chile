#!/usr/bin/env python3
"""Calculadora referencial de CAE y CTC para créditos en Chile.

Implementa la ecuación de flujos del *borrador* de reglamento de crédito de
consumo del Ministerio de Economía (Ec. 2/3): la tasa periódica i_f que iguala
el valor presente de lo recibido con el de lo pagado, y CAE = i_f * f.

IMPORTANTE
- Es una herramienta para COMPARAR ofertas. La CAE vinculante es la que informa
  la institución en el contrato/cotización (Ley 20.555).
- f (periodos por año) no está fijado en el borrador; por defecto 12 (cuotas
  mensuales). Se informa también la tasa efectiva anual (1+i)^f - 1 para no
  mezclar bases al comparar con otras tasas.
- Sin dependencias externas. Python >= 3.8.

Uso:
  cae.py credito --monto-neto 1000000 --cuota 52000 --n 24
  cae.py credito --monto-neto 970000 --cuota 52000 --n 24 --pago-inicial 0
  cae.py saldo --cuota 52000 --n 24 --pagadas 6 --tasa-periodica 0.0158
  cae.py reemplazo --json deudas.json
"""
import argparse
import json
import sys


def _vp(i, flujos):
    """Valor presente de [(t, monto), ...] a tasa periódica i."""
    return sum(m / (1.0 + i) ** t for t, m in flujos)


def tasa_periodica(desembolsos, pagos, lo=-0.99, hi=10.0, tol=1e-12):
    """Resuelve VP(pagos) = VP(desembolsos) por bisección. t en periodos."""
    if not pagos or not desembolsos:
        raise ValueError("Se requieren desembolsos y pagos")
    if sum(m for _, m in pagos) <= 0:
        raise ValueError("Los pagos deben sumar un monto positivo")

    def g(i):
        return _vp(i, pagos) - _vp(i, desembolsos)

    g_lo, g_hi = g(lo), g(hi)
    if g_lo * g_hi > 0:
        raise ValueError("No se encontró raíz en el rango; revisa los datos")
    for _ in range(400):
        mid = (lo + hi) / 2.0
        g_mid = g(mid)
        if abs(g_mid) < tol:
            return mid
        if g_lo * g_mid <= 0:
            hi = mid
        else:
            lo, g_lo = mid, g_mid
    return (lo + hi) / 2.0


def cae_credito(monto_neto, cuota, n, pago_inicial=0.0, f=12):
    """CAE/CTC de un crédito con cuota constante.

    monto_neto : dinero efectivamente recibido (descontados gastos que se
                 retengan al desembolso).
    cuota      : Valor de la Cuota total (interés + amortización + cargos +
                 seguros/productos incluidos en la cuota).
    pago_inicial: pagos en t0 (p. ej. impuestos, comisiones pagadas al inicio).
    """
    desembolsos = [(0, monto_neto)]
    pagos = [(m, cuota) for m in range(1, n + 1)]
    if pago_inicial:
        pagos.append((0, pago_inicial))
    i = tasa_periodica(desembolsos, pagos)
    ctc = cuota * n + pago_inicial
    return {
        "tasa_periodica": i,
        "periodos_por_anio": f,
        "CAE_nominal_i_por_f": i * f,
        "tasa_efectiva_anual": (1.0 + i) ** f - 1.0,
        "CTC": ctc,
        "costo_total_sobre_neto": ctc - monto_neto,
        "nota": "Referencial. La CAE vinculante es la que informa la institución.",
    }


def saldo_capital(cuota, n, pagadas, tasa_periodica_):
    """Saldo de capital tras `pagadas` cuotas = VP de las cuotas restantes a i.

    Si la cuota incluye seguros/cargos, el resultado sobreestima el capital.
    El monto de prepago vinculante es el del certificado de prepago.
    """
    restantes = [(m - pagadas, cuota) for m in range(pagadas + 1, n + 1)]
    return _vp(tasa_periodica_, restantes)


def reemplazo(deudas, nuevo):
    """Compara costo mensual de deudas actuales vs un crédito que las reemplaza.

    deudas: [{"nombre":..., "saldo":..., "tasa_mensual":...}]
    nuevo : {"monto_neto":..., "cuota":..., "n":..., "pago_inicial":0}
    Devuelve tasa mensual ponderada actual, tasa periódica del nuevo (por CAE)
    y diferencia aproximada de costo mensual el primer mes.
    """
    total = sum(d["saldo"] for d in deudas)
    if total <= 0:
        raise ValueError("Saldo total debe ser positivo")
    ponderada = sum(d["saldo"] * d["tasa_mensual"] for d in deudas) / total
    r = cae_credito(nuevo["monto_neto"], nuevo["cuota"], nuevo["n"],
                    nuevo.get("pago_inicial", 0.0))
    return {
        "saldo_total_actual": total,
        "tasa_mensual_ponderada_actual": ponderada,
        "tasa_periodica_nuevo_credito": r["tasa_periodica"],
        "diferencia_costo_primer_mes_aprox":
            total * ponderada - nuevo["monto_neto"] * r["tasa_periodica"],
        "nuevo": r,
        "advertencia": ("Aproximación del primer mes. El ahorro real depende de "
                        "cuánto tardes en pagar las deudas actuales si NO tomas "
                        "el crédito y de los costos de prepago de este."),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("credito")
    c.add_argument("--monto-neto", type=float, required=True)
    c.add_argument("--cuota", type=float, required=True)
    c.add_argument("--n", type=int, required=True)
    c.add_argument("--pago-inicial", type=float, default=0.0)
    c.add_argument("--f", type=int, default=12)

    s = sub.add_parser("saldo")
    s.add_argument("--cuota", type=float, required=True)
    s.add_argument("--n", type=int, required=True)
    s.add_argument("--pagadas", type=int, required=True)
    s.add_argument("--tasa-periodica", type=float, required=True)

    r = sub.add_parser("reemplazo")
    r.add_argument("--json", required=True, help="archivo con {deudas:[...], nuevo:{...}}")

    a = p.parse_args(argv)
    if a.cmd == "credito":
        out = cae_credito(a.monto_neto, a.cuota, a.n, a.pago_inicial, a.f)
    elif a.cmd == "saldo":
        out = {"saldo_capital_aprox": saldo_capital(a.cuota, a.n, a.pagadas, a.tasa_periodica)}
    else:
        with open(a.json, encoding="utf-8") as fh:
            d = json.load(fh)
        out = reemplazo(d["deudas"], d["nuevo"])
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
