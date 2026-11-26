#!/usr/bin/env python3
"""Plan de pago y refinanciamiento: avalancha vs bola de nieve, prepago neto y compra de cartera.

Subcomandos (todos aceptan --json con la entrada):
  pago      {"presupuesto_mensual": N, "metodo": "avalancha|nieve", "deudas":[{"nombre","saldo","tasa_mensual","cuota_minima"}]}
  prepago   {"saldo","cuota","cuotas_restantes","comision_prepago_pct":0.0, "tasa_mensual": opc}
  cartera   {"deudas":[{"nombre","cuota","cuotas_restantes"}], "oferta":{"monto","cuota","n","gastos":0}}

Evidencia: la avalancha (mayor tasa primero) es la más barata; la bola de nieve (menor saldo primero)
puede mejorar la adherencia (Amar et al. 2011). Alargar el plazo para bajar la cuota no resolvió el estrés
en un experimento con 40.000 deudores de tarjeta (Dobbie y Song, NBER 23545).
Comisión de prepago y condiciones: verifica con tu contrato (RAN 7-1 / Ley 18.010).
"""
import argparse
import json
import sys

AVISO = ("Herramienta de apoyo basada en IA; no es asesoría financiera ni crediticia regulada y no recomienda "
         "entidades. Confirma saldos, comisiones y condiciones con cada entidad.")


def simular_pago(deudas, presupuesto, metodo="avalancha", max_meses=600):
    d = [dict(x, saldo=float(x["saldo"])) for x in deudas]
    minimos = sum(x["cuota_minima"] for x in d)
    if presupuesto < minimos:
        raise ValueError("el presupuesto (%d) no cubre las cuotas mínimas (%d)" % (presupuesto, minimos))
    if metodo not in ("avalancha", "nieve"):
        raise ValueError("metodo debe ser avalancha o nieve")
    meses, intereses, cierre = 0, 0.0, []
    while any(x["saldo"] > 0.5 for x in d) and meses < max_meses:
        meses += 1
        for x in d:
            if x["saldo"] > 0:
                i = x["saldo"] * x["tasa_mensual"]
                x["saldo"] += i
                intereses += i
        disponible = presupuesto
        for x in d:  # mínimos primero
            if x["saldo"] > 0:
                p = min(x["cuota_minima"], x["saldo"])
                x["saldo"] -= p
                disponible -= p
        vivas = [x for x in d if x["saldo"] > 0.5]
        vivas.sort(key=(lambda x: -x["tasa_mensual"]) if metodo == "avalancha" else (lambda x: x["saldo"]))
        for x in vivas:
            p = min(disponible, x["saldo"])
            x["saldo"] -= p
            disponible -= p
            if disponible <= 0:
                break
        for x in d:
            if x["saldo"] <= 0.5 and x["nombre"] not in [c["nombre"] for c in cierre]:
                x["saldo"] = 0
                cierre.append({"nombre": x["nombre"], "mes": meses})
    return {"metodo": metodo, "meses_para_saldar": meses, "intereses_total": round(intereses),
            "orden_de_cierre": cierre, "completo": all(x["saldo"] <= 0.5 for x in d)}


def tasa_implicita(saldo, cuota, n):
    lo, hi = 0.0, 5.0
    for _ in range(200):
        mid = (lo + hi) / 2
        vp = sum(cuota / (1 + mid) ** t for t in range(1, n + 1))
        lo, hi = (mid, hi) if vp > saldo else (lo, mid)
    return (lo + hi) / 2


def ahorro_prepago(saldo, cuota, cuotas_restantes, comision_pct=0.0, tasa_mensual=None):
    """Ahorro neto de prepagar el saldo hoy: intereses que no pagarás - comisión de prepago."""
    if tasa_mensual is None:
        tasa_mensual = tasa_implicita(saldo, cuota, cuotas_restantes)
    intereses_futuros = cuota * cuotas_restantes - saldo
    comision = saldo * comision_pct
    return {"tasa_mensual_usada": round(tasa_mensual, 5),
            "tasa_anual_implicita": round(((1 + tasa_mensual) ** 12 - 1), 4),
            "intereses_futuros_si_sigues": round(intereses_futuros), "comision_prepago": round(comision),
            "ahorro_neto": round(intereses_futuros - comision),
            "lectura": "El ahorro es bajo si quedan pocas cuotas: compáralo con usar ese dinero en una deuda más cara o en el colchón."}


def compra_cartera(deudas, oferta):
    actual = sum(x["cuota"] * x["cuotas_restantes"] for x in deudas)
    cuota_actual = sum(x["cuota"] for x in deudas)
    nuevo = oferta["cuota"] * oferta["n"] + oferta.get("gastos", 0)
    plazo_actual = max(x["cuotas_restantes"] for x in deudas)
    alertas = []
    if oferta["n"] > plazo_actual:
        alertas.append("El plazo nuevo es mayor: la cuota baja pero el costo puede subir (alargar el plazo no resolvió el estrés en el experimento de Dobbie y Song).")
    if oferta["cuota"] >= cuota_actual:
        alertas.append("La cuota nueva no baja frente a la suma de las actuales.")
    alertas.append("Compromiso necesario: no volver a endeudarte en las tarjetas liberadas (la consolidación suele revertirse si se vuelven a usar).")
    return {"pagarias_si_sigues": round(actual), "pagarias_con_la_oferta": round(nuevo),
            "diferencia_total": round(actual - nuevo), "cuota_actual_suma": round(cuota_actual),
            "cuota_oferta": round(oferta["cuota"]), "plazo_actual_max": plazo_actual, "plazo_oferta": oferta["n"],
            "alertas": alertas, "pide": "Certificado de deuda gratuito y la hoja resumen de cotización con CAE y CTC."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["pago", "prepago", "cartera"])
    p.add_argument("--json", required=True)
    a = p.parse_args(argv)
    with open(a.json, encoding="utf-8") as f:
        d = json.load(f)
    if a.cmd == "pago":
        r = {m: simular_pago(d["deudas"], d["presupuesto_mensual"], m) for m in ([d["metodo"]] if "metodo" in d else ["avalancha", "nieve"])}
    elif a.cmd == "prepago":
        r = ahorro_prepago(d["saldo"], d["cuota"], d["cuotas_restantes"], d.get("comision_prepago_pct", 0.0), d.get("tasa_mensual"))
    else:
        r = compra_cartera(d["deudas"], d["oferta"])
    r = {"resultado": r, "aviso": AVISO}
    json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
