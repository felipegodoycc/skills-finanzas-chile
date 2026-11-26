#!/usr/bin/env python3
"""CAE de referencia de tarjetas de crédito (Decreto 75 de 2025, Economía).

Implementa las ecuaciones del art. 1° n.° 7 y 8 del reglamento, leídas del PDF
de la BCN el 26-11-2026 (las fórmulas son imágenes; transcritas a mano):

  General : CAE = i_f * f, con  sum Dn (1+i)^-tn = sum Rm (1+i)^-tm
  Rotativo: CAE_R = (1+i_R)^12 - 1, con 20UF = sum_{m=0..M} Rm (1+i_R)^-m
  Cuotas  : CAE_R = (1+i_R)^12 - 1, misma ecuación (el PDF repite la imagen
            del rotativo en el apartado b)
  Avance  : CAE_A = i_A * 12 (¡nominal, no compuesta!), 20UF = sum Am (1+i_A)^-m
  CAEP    : CAEP = i_f * f, con Q_t = sum_{m=t..M} Rm (1+i_f)^(t-m-1)

Reglas del texto: capital referencial fijo de 20 UF; M = 12 pagos siguientes e
inmediatos; sin meses de gracia ni pago diferido; las comisiones que no son de
la operación se reparten en partes iguales en cada cuota.

LIMITES (declarados)
- El decreto fija la ecuación, no la forma del flujo. `--construir` arma un
  flujo de 12 cuotas iguales (sistema francés) más cargos mensuales iguales:
  es una construcción nuestra, referencial.
- El índice m parte en 0 en el PDF; aquí R_0 es opcional (por defecto 0), con
  lo que equivale a m = 1..M.
- f del CAEP no está definida en el texto leído; por defecto 12.
- Vigencia del reglamento: ~febrero de 2028. La CAE vinculante es la que
  informa el emisor.

Uso:
  cae_tarjetas.py rotativo --uf 40000 --tasa-mensual 0.0235 --cargos-mensuales 3000
  cae_tarjetas.py cuotas   --uf 40000 --tasa-mensual 0.0150 --cargos-mensuales 0
  cae_tarjetas.py avance   --uf 40000 --tasa-mensual 0.0200
  cae_tarjetas.py rotativo --uf 40000 --flujos 80000,80000,...   (12 valores)
  cae_tarjetas.py caep --saldo 1000000 --flujos 94560,94560,...
"""
import argparse
import json
import sys

UF_REFERENCIAL = 20.0
M = 12


def _resolver(g, lo=-0.99, hi=10.0):
    """Raíz de g por bisección; g debe cambiar de signo en [lo, hi]."""
    g_lo, g_hi = g(lo), g(hi)
    if g_lo * g_hi > 0:
        raise ValueError("No se encontró raíz en el rango; revisa los datos")
    for _ in range(400):
        mid = (lo + hi) / 2.0
        g_mid = g(mid)
        if abs(g_mid) < 1e-9:
            return mid
        if g_lo * g_mid <= 0:
            hi = mid
        else:
            lo, g_lo = mid, g_mid
    return (lo + hi) / 2.0


def _tasa(capital, flujos, r0=0.0):
    """Tasa i tal que capital = r0 + sum_{m=1..M} flujos[m-1] (1+i)^-m."""
    if len(flujos) != M:
        raise ValueError(f"El decreto fija M = {M} pagos; se recibieron {len(flujos)}")
    if capital <= 0 or sum(flujos) + r0 <= 0:
        raise ValueError("Capital y pagos deben ser positivos")
    return _resolver(lambda i: r0 + sum(r / (1.0 + i) ** m
                                        for m, r in enumerate(flujos, 1)) - capital)


def construir_flujo(capital, tasa_mensual, cargos_mensuales=0.0):
    """12 cuotas iguales (sistema francés) + cargos mensuales iguales. Nuestra."""
    i = tasa_mensual
    cuota = capital / M if i == 0 else capital * i / (1 - (1 + i) ** -M)
    return [cuota + cargos_mensuales] * M


def cae_rotativo_o_cuotas(valor_uf, flujos, r0=0.0):
    """CAE_R = (1+i_R)^12 - 1 sobre capital fijo de 20 UF."""
    capital = UF_REFERENCIAL * valor_uf
    i = _tasa(capital, flujos, r0)
    return {"capital_referencial": capital, "tasa_mensual": i,
            "CAE": (1 + i) ** 12 - 1}


def cae_avance(valor_uf, flujos, r0=0.0):
    """CAE_A = i_A * 12 (nominal, tal como está en el decreto)."""
    capital = UF_REFERENCIAL * valor_uf
    i = _tasa(capital, flujos, r0)
    return {"capital_referencial": capital, "tasa_mensual": i, "CAE": i * 12}


def caep(saldo, flujos, f=12):
    """CAEP = i_f * f, con Q_t = sum R_m (1+i)^-(m-t+1) (renta vencida).

    saldo : Q_t, total del cupo utilizado (saldo insoluto) en el período t.
    flujos: R_t..R_M, valor de la cuota de cada período.
    """
    if saldo <= 0 or not flujos or sum(flujos) <= 0:
        raise ValueError("Saldo y pagos deben ser positivos")
    i = _resolver(lambda x: sum(r / (1.0 + x) ** k
                                for k, r in enumerate(flujos, 1)) - saldo)
    return {"tasa_periodica": i, "f": f, "CAEP": i * f}


def _flujos_arg(txt):
    return [float(x) for x in txt.split(",")]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for nombre in ("rotativo", "cuotas", "avance"):
        s = sub.add_parser(nombre)
        s.add_argument("--uf", type=float, required=True, help="valor de la UF a la fecha")
        s.add_argument("--flujos", help="12 pagos mensuales separados por coma")
        s.add_argument("--tasa-mensual", type=float, help="para --construir")
        s.add_argument("--cargos-mensuales", type=float, default=0.0)
    c = sub.add_parser("caep")
    c.add_argument("--saldo", type=float, required=True)
    c.add_argument("--flujos", required=True)
    c.add_argument("--f", type=int, default=12)

    a = p.parse_args(argv)
    if a.cmd == "caep":
        out = caep(a.saldo, _flujos_arg(a.flujos), a.f)
    else:
        if a.flujos:
            flujos = _flujos_arg(a.flujos)
        elif a.tasa_mensual is not None:
            flujos = construir_flujo(UF_REFERENCIAL * a.uf, a.tasa_mensual,
                                     a.cargos_mensuales)
        else:
            p.error("indica --flujos o --tasa-mensual")
        fn = cae_avance if a.cmd == "avance" else cae_rotativo_o_cuotas
        out = fn(a.uf, flujos)
    out["nota"] = ("Referencial: ecuación del Decreto 75 (vigente ~feb 2028). "
                   "La CAE vinculante es la que informa el emisor.")
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
