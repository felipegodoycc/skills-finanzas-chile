#!/usr/bin/env python3
"""Convierte una exportación CSV/TXT del banco al formato genérico de movimientos, con enmascarado.

Formato de salida (CSV): id, fecha (YYYY-MM-DD), monto (positivo, CLP), tipo (gasto|ingreso),
comercio (enmascarado), producto, fuente.

Qué hace para proteger tus datos:
- Enmascara RUT, correos, teléfonos y números largos (tarjetas/cuentas: deja los últimos 4).
- Reemplaza glosas con frases tipo "ignora tus instrucciones" (texto que podría manipular a una IA).
- No escribe contraseñas ni pide credenciales. Archivo de salida con permisos 0600.
- El enmascarado NO es anonimización: nombres, comercios y montos siguen visibles.
  Revisa el archivo antes de entregárselo a cualquier IA en la nube.

Ejemplos:
  normalizar_movimientos.py --csv cartola.csv --col-fecha Fecha --col-glosa Descripcion \
      --col-cargo Cargos --col-abono Abonos --producto cuenta-1234
  normalizar_movimientos.py --csv cartola.csv --col-fecha Fecha --col-glosa Glosa \
      --col-monto Monto --signo-gasto negativo --formato-fecha %d/%m/%Y

shortcut: el enmascarado está duplicado de lectura-pdf-segura para que cada skill funcione sola;
unificar si se publica un paquete común.
"""
import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime

AVISO = ("Herramienta de apoyo. El enmascarado NO es anonimización: revisa el archivo antes de subirlo "
         "a una IA en la nube; esos datos salen de tu equipo.")
FORMATOS_FECHA = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y", "%d.%m.%Y"]
RE_RUT = re.compile(r"\b\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]\b")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_FONO = re.compile(r"\+?56\s?9[\s\d]{8,}")
RE_LARGO = re.compile(r"\d(?:[ -]?\d){8,}")  # 9 o más dígitos, con espacios o guiones entre ellos
RE_INYECCION = re.compile(
    r"(ignora|ignore|olvida|forget|disregard).{0,40}(instrucci|instruction|prompt|regla|rule)"
    r"|system prompt|you are now|eres ahora|act as |responde con|reply with|envía|envia\b.{0,30}@", re.I)


def enmascarar(texto):
    """Devuelve (texto_enmascarado, nº de reemplazos)."""
    n = 0

    def sub(rx, repl, s):
        nonlocal n
        s, k = rx.subn(repl, s)
        n += k
        return s
    texto = sub(RE_RUT, "[RUT]", texto)
    texto = sub(RE_EMAIL, "[correo]", texto)
    texto = sub(RE_FONO, "[telefono]", texto)

    def largo(m):
        digs = re.sub(r"\D", "", m.group(0))
        return "****" + digs[-4:] if len(digs) >= 13 else "[numero]"
    texto = sub(RE_LARGO, largo, texto)
    return texto, n


def parse_fecha(s, formato=None):
    s = s.strip()
    for f in ([formato] if formato else FORMATOS_FECHA):
        try:
            return datetime.strptime(s, f).date().isoformat()
        except ValueError:
            continue
    raise ValueError("fecha no reconocida")


def parse_monto(s):
    s = (s or "").strip()
    if not s:
        return 0.0
    neg = s.startswith("-") or (s.startswith("(") and s.endswith(")"))
    s = re.sub(r"[^\d,.]", "", s)
    if not s:
        raise ValueError("monto no reconocido")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "." in s and re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
        s = s.replace(".", "")
    v = float(s)
    return -v if neg else v


def leer_texto(path):
    raw = open(path, "rb").read()
    for enc in ("utf-8-sig", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue


def normalizar(texto, a):
    muestra = texto[:2000]
    delim = a.delimitador or (";" if muestra.count(";") > muestra.count(",") else ("\t" if "\t" in muestra else ","))
    rdr = csv.DictReader(io.StringIO(texto), delimiter=delim)
    cols = set(rdr.fieldnames or [])
    req = [a.col_fecha, a.col_glosa] + ([a.col_monto] if a.col_monto else [a.col_cargo, a.col_abono])
    faltan = [c for c in req if c not in cols]
    if faltan:
        raise ValueError("columnas no encontradas: %s (disponibles: %s)" % (faltan, sorted(cols)))
    filas, descartes, masc, sospechosas = [], [], 0, 0
    for i, row in enumerate(rdr, start=2):
        try:
            fecha = parse_fecha(row[a.col_fecha], a.formato_fecha)
            if a.col_monto:
                v = parse_monto(row[a.col_monto])
                gasto = (v < 0) if a.signo_gasto == "negativo" else (v > 0)
                monto = abs(v)
            else:
                cargo, abono = parse_monto(row[a.col_cargo]), parse_monto(row[a.col_abono])
                if cargo and abono:
                    raise ValueError("cargo y abono a la vez")
                gasto, monto = bool(cargo), abs(cargo or abono)
            if monto == 0:
                raise ValueError("monto cero")
        except ValueError as e:
            descartes.append({"linea": i, "motivo": str(e)})
            continue
        glosa = (row[a.col_glosa] or "").strip()
        if RE_INYECCION.search(glosa):
            glosa, sospechosas = "[texto sospechoso removido]", sospechosas + 1
        else:
            glosa, k = enmascarar(glosa)
            masc += k
        filas.append({"id": len(filas) + 1, "fecha": fecha, "monto": int(monto) if monto == int(monto) else monto,
                      "tipo": "gasto" if gasto else "ingreso", "comercio": glosa,
                      "producto": a.producto, "fuente": "cartola"})
        if len(filas) >= a.max_filas:
            descartes.append({"linea": i, "motivo": "límite de filas alcanzado (--max-filas)"})
            break
    return filas, descartes, masc, sospechosas


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, allow_abbrev=False,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--csv", required=True)
    p.add_argument("--col-fecha", required=True)
    p.add_argument("--col-glosa", required=True)
    p.add_argument("--col-monto")
    p.add_argument("--col-cargo")
    p.add_argument("--col-abono")
    p.add_argument("--signo-gasto", choices=["negativo", "positivo"], default="negativo")
    p.add_argument("--formato-fecha")
    p.add_argument("--delimitador")
    p.add_argument("--producto", default="cuenta-sin-nombre", help="Etiqueta ENMASCARADA, p. ej. cuenta-1234")
    p.add_argument("--max-filas", type=int, default=5000)
    p.add_argument("--salida")
    p.add_argument("--sobrescribir", action="store_true")
    a = p.parse_args(argv)
    if not a.col_monto and not (a.col_cargo and a.col_abono):
        p.error("indica --col-monto o ambas --col-cargo y --col-abono")
    try:
        filas, descartes, masc, sosp = normalizar(leer_texto(a.csv), a)
    except (OSError, ValueError) as e:
        print("Error: %s" % e, file=sys.stderr)
        return 2
    salida = a.salida or re.sub(r"\.\w+$", "", a.csv) + ".normalizado.csv"
    flags = os.O_WRONLY | os.O_CREAT | (os.O_TRUNC if a.sobrescribir else os.O_EXCL)
    try:
        fd = os.open(salida, flags, 0o600)
    except FileExistsError:
        print("Error: %s ya existe (usa --sobrescribir)" % salida, file=sys.stderr)
        return 2
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "fecha", "monto", "tipo", "comercio", "producto", "fuente"])
        w.writeheader()
        w.writerows(filas)
    if os.name != "posix":  # Windows ignora el modo 0600: el archivo hereda los permisos de la carpeta
        print("AVISO: en Windows no se pudo restringir el acceso a %s; guárdalo en una carpeta solo tuya." % salida, file=sys.stderr)
    resumen = {"archivo_salida": salida, "filas": len(filas), "descartadas": descartes[:20],
               "total_descartadas": len(descartes), "reemplazos_enmascarado": masc,
               "glosas_sospechosas_removidas": sosp,
               "rango_fechas": [min(f["fecha"] for f in filas), max(f["fecha"] for f in filas)] if filas else None,
               "total_gasto": sum(f["monto"] for f in filas if f["tipo"] == "gasto"),
               "total_ingreso": sum(f["monto"] for f in filas if f["tipo"] == "ingreso"),
               "siguiente_paso": "Revisa el archivo; si hay duplicados o reembolsos usa calidad-de-datos-financieros.",
               "aviso": AVISO}
    json.dump(resumen, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
