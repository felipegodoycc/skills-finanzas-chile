#!/usr/bin/env python3
"""UF, UTM, IPC y tipo de cambio desde APIs OFICIALES (CMF y Banco Central).

Fuentes (ambas gratuitas, requieren clave personal):
- CMF   : https://api.cmfchile.cl/api-sbifv3/recursos_api/<indicador>
          clave en la variable de entorno CMF_API_KEY.
- BCCh  : https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx
          token de la BDE en la variable de entorno BCCH_API_TOKEN.
La clave se lee SOLO del entorno (nunca por argumento, para no dejarla en el
historial del shell) y no se imprime. No se usan agregadores de terceros.

LIMITES (declarados)
- La forma exacta de la respuesta JSON no figura en la documentación revisada
  (CMF solo muestra XML; BCCh no muestra ejemplo). El lector es tolerante, pero
  confirma con una consulta real antes de automatizar.
- Rutas CMF: `uf` confirmada en la documentación oficial; `utm`, `ipc`, `dolar`
  y `euro` siguen el mismo patrón y están por confirmar.
- Códigos de serie BCCh tomados de la ayuda oficial de la BDE (UF, UTM, IPC base
  2023, dólar observado).
- Cita la fuente: el Banco Central pide mencionarse como propietario del dato.

Uso:
  indicadores.py uf                      # UF de hoy
  indicadores.py uf --fecha 2026-11-26
  indicadores.py utm --fecha 2026-11     # UTM del mes
  indicadores.py ipc --fecha 2026-10
  indicadores.py dolar
  indicadores.py serie --codigo F073.UFF.PRE.Z.D --desde 2026-11-01 --hasta 2026-11-26
  --fuente cmf|bcch|auto (por defecto auto: la que tenga clave en el entorno)
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

CMF_BASE = "https://api.cmfchile.cl/api-sbifv3/recursos_api/"
BCCH_URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
BCCH_SERIES = {  # ayuda oficial de la BDE
    "uf": "F073.UFF.PRE.Z.D",
    "utm": "F073.UTR.PRE.Z.M",
    "ipc": "F074.IPC.VAR.Z.EP23.C.M",
    "dolar": "F073.TCO.PRE.Z.D",
}
CMF_INDICADORES = ("uf", "utm", "ipc", "dolar", "euro")


def numero(txt):
    """'20.939,49' (CMF) o '39123.45' (BCCh) -> float."""
    s = str(txt).strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return float(s)


def _fecha(fecha):
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-(\d{2}))?", fecha or "")
    if fecha and not m:
        raise ValueError("fecha inválida: usa YYYY-MM-DD o YYYY-MM")
    return m.groups() if m else (None, None, None)


def ruta_cmf(ind, fecha=None):
    a, m, d = _fecha(fecha)
    if a is None:
        return ind
    if d:
        return f"{ind}/{a}/{m}/dias/{d}"
    return f"{ind}/{a}/{m}"


def _get(url, fetch=None):
    if fetch:
        return fetch(url)
    req = urllib.request.Request(url, headers={"User-Agent": "skills-finanzas-chile"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"La API respondió HTTP {e.code}. Revisa la clave y la ruta.") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Sin conexión con la API ({e.reason}).") from None


def parse_cmf(texto):
    """Busca la lista de objetos con Valor y Fecha, sin depender del nombre raíz."""
    data = json.loads(texto)
    hallados = []

    def rec(x):
        if isinstance(x, dict):
            if "Valor" in x and "Fecha" in x:
                hallados.append(x)
            else:
                for v in x.values():
                    rec(v)
        elif isinstance(x, list):
            for v in x:
                rec(v)
    rec(data)
    if not hallados:
        raise ValueError("Respuesta CMF sin pares Valor/Fecha; revisa la clave o la ruta")
    return [{"fecha": h["Fecha"], "valor": numero(h["Valor"])} for h in hallados]


def parse_bcch(texto):
    data = json.loads(texto)
    if data.get("Codigo") not in (None, 0):
        raise ValueError(f"BCCh respondió error: {data.get('Descripcion')}")
    obs = (data.get("Series") or {}).get("Obs")
    if obs is None:
        raise ValueError("Respuesta BCCh sin Series/Obs; revisa token y código de serie")
    out = []
    for o in obs:
        if o.get("statusCode") not in (None, "OK") or o.get("value") in (None, "", "NaN"):
            continue  # observación sin dato
        out.append({"fecha": o["indexDateString"], "valor": numero(o["value"])})
    return out


def consultar(indicador, fecha=None, fuente="auto", env=None, fetch=None, codigo=None,
              desde=None, hasta=None):
    env = os.environ if env is None else env
    if fuente == "auto":
        fuente = "cmf" if env.get("CMF_API_KEY") else "bcch" if env.get("BCCH_API_TOKEN") else None
        if not fuente:
            raise RuntimeError("Define CMF_API_KEY o BCCH_API_TOKEN en el entorno (ver --help)")
    if fuente == "cmf":
        if not env.get("CMF_API_KEY"):
            raise RuntimeError("Falta CMF_API_KEY en el entorno")
        if indicador not in CMF_INDICADORES:
            raise ValueError("La API de la CMF cubre: " + ", ".join(CMF_INDICADORES))
        url = CMF_BASE + ruta_cmf(indicador, fecha)
        q = {"formato": "json"}
        base = url + "?" + urllib.parse.urlencode(q)
        filas = parse_cmf(_get(base + "&apikey=" + urllib.parse.quote(env["CMF_API_KEY"]), fetch))
    elif fuente == "bcch":
        if not env.get("BCCH_API_TOKEN"):
            raise RuntimeError("Falta BCCH_API_TOKEN en el entorno")
        serie = codigo or BCCH_SERIES.get(indicador)
        if not serie:
            raise ValueError("Sin serie BCCh para ese indicador; usa el comando `serie`")
        q = {"function": "GetSeries", "timeseries": serie}
        if fecha and not (desde or hasta):
            a, m, d = _fecha(fecha)
            desde = hasta = fecha if d else f"{a}-{m}-01"
            if not d:
                hasta = f"{a}-{m}-28"
        if desde:
            q["firstdate"] = desde
        if hasta:
            q["lastdate"] = hasta
        base = BCCH_URL + "?" + urllib.parse.urlencode(q)
        filas = parse_bcch(_get(base + "&token=" + urllib.parse.quote(env["BCCH_API_TOKEN"]), fetch))
        url = BCCH_URL + " (serie " + serie + ")"
    else:
        raise ValueError("fuente debe ser cmf, bcch o auto")
    return {"indicador": indicador, "fuente": "CMF" if fuente == "cmf" else "Banco Central de Chile (BDE)",
            "consulta": url, "datos": filas,
            "nota": "Cita la fuente. Confirma el formato de respuesta con una consulta real."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fuente", default="auto", choices=("auto", "cmf", "bcch"))
    sub = p.add_subparsers(dest="cmd", required=True)
    for ind in CMF_INDICADORES:
        s = sub.add_parser(ind)
        s.add_argument("--fecha", help="YYYY-MM-DD (UF, dólar) o YYYY-MM (UTM, IPC)")
    s = sub.add_parser("serie")
    s.add_argument("--codigo", required=True)
    s.add_argument("--desde")
    s.add_argument("--hasta")
    a = p.parse_args(argv)
    try:
        if a.cmd == "serie":
            out = consultar("serie", fuente="bcch", codigo=a.codigo, desde=a.desde, hasta=a.hasta)
        else:
            out = consultar(a.cmd, a.fecha, a.fuente)
    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
