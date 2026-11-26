#!/usr/bin/env python3
"""UF, UTM, IPC y tipo de cambio desde APIs OFICIALES (CMF y Banco Central).

Fuentes: el usuario elige con --fuente (por defecto `auto`: solo las oficiales con clave).
- sii        : OFICIAL, sin clave. Lee las tablas HTML de sii.cl (UF, UTM, UTA, IPC).
               Frágil: si el SII cambia la página, falla con un mensaje claro.
- mindicador : TERCEROS (mindicador.cl), sin clave, NO oficial. Solo si se pide a mano.
- cmf y bcch (gratuitas, requieren clave personal):
- CMF   : https://api.cmfchile.cl/api-sbifv3/recursos_api/<indicador>
          clave en la variable de entorno CMF_API_KEY.
- BCCh  : https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx
          token de la BDE en la variable de entorno BCCH_API_TOKEN.
La clave se lee SOLO del entorno (nunca por argumento, para no dejarla en el
historial del shell) y no se imprime. No se usan agregadores de terceros.

LIMITES (declarados)
- SII: la estructura real del HTML no se pudo descargar desde el entorno de desarrollo
  (solo vista de texto); el lector busca filas <tr> y es tolerante. Los tests usan HTML
  simulado. UF: tabla anual con 12 meses por día. UTM/UTA/IPC: una fila por mes.
- mindicador: rutas y JSON sin documentación oficial revisada; lector tolerante.
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
  --fuente cmf|bcch|sii|mindicador|auto (auto: la oficial con clave en el entorno)
  Sin clave ni red a la API: usa --fuente sii, o copia el valor a mano desde sii.cl.
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
CLI_INDICADORES = CMF_INDICADORES + ("uta",)  # uta: solo SII


def numero(txt):
    """'20.939,49' (CMF) o '39123.45' (BCCh) -> float."""
    s = str(txt).strip()
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return float(s)


def numero_cl(txt):
    """Formato SII: punto = miles, coma = decimal ('72.440' -> 72440.0)."""
    return float(str(txt).strip().replace(".", "").replace(",", "."))


MESES = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre")
SII_BASE = "https://www.sii.cl/valores_y_fechas/"
MINDICADOR = "https://mindicador.cl/api/"


def _filas_html(html):
    filas = []
    for tr in re.findall(r"<tr\b.*?</tr>", html, re.S | re.I):
        celdas = re.findall(r"<t[dh]\b.*?>(.*?)</t[dh]>", tr, re.S | re.I)
        filas.append([re.sub(r"\s+", " ", re.sub(r"<[^>]+>|&nbsp;", " ", c)).strip() for c in celdas])
    return filas


def parse_sii_uf(html, mes, dia):
    """Tabla anual: fila = día (1-31), 12 columnas de mes tras la columna 'Día'."""
    for f in _filas_html(html):
        if len(f) == 13 and f[0] == str(dia):
            v = f[mes]
            if not v:
                raise ValueError("El SII aún no publica la UF de esa fecha")
            return numero_cl(v)
    raise ValueError("No encontré la tabla anual de UF en la página del SII; cambió su formato")


def parse_sii_mensual(html, mes, campo):
    """Una fila por mes: Mes | UTM | UTA | IPC puntos | var. mensual | acum. | 12 meses."""
    col = {"utm": 1, "uta": 2, "ipc": 3}[campo]
    for f in _filas_html(html):
        if f and f[0].strip().lower() == MESES[mes - 1] and len(f) > col:
            if not f[col]:
                raise ValueError("El SII aún no publica ese valor")
            return numero_cl(f[col])
    raise ValueError("No encontré la fila del mes en la página del SII; cambió su formato")


def parse_mindicador(texto, indicador):
    d = json.loads(texto)
    filas = d.get("serie") or ([d[indicador]] if isinstance(d.get(indicador), dict) else [d])
    out = [{"fecha": str(x["fecha"])[:10], "valor": float(x["valor"])}
           for x in filas if isinstance(x, dict) and "fecha" in x and "valor" in x]
    if not out:
        raise ValueError("Respuesta de mindicador.cl sin fecha/valor")
    return out


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
            raise RuntimeError("Sin clave en el entorno. Elige: define CMF_API_KEY o BCCH_API_TOKEN, "
                               "o usa --fuente sii (oficial, sin clave) o --fuente mindicador "
                               "(terceros), o copia el valor a mano desde sii.cl")
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
    elif fuente == "sii":
        import datetime
        a, m, d = _fecha(fecha)
        hoy = datetime.date.today()
        a, m = int(a or hoy.year), int(m or hoy.month)
        if indicador == "uf":
            d = int(d or hoy.day)
            url = f"{SII_BASE}uf/uf{a}.htm"
            valor = parse_sii_uf(_get(url, fetch), m, d)
            filas = [{"fecha": f"{a}-{m:02d}-{d:02d}", "valor": valor}]
        elif indicador in ("utm", "uta", "ipc"):
            url = f"{SII_BASE}utm/utm{a}.htm"
            valor = parse_sii_mensual(_get(url, fetch), m, indicador)
            filas = [{"fecha": f"{a}-{m:02d}", "valor": valor}]
        else:
            raise ValueError("El SII cubre uf, utm, uta e ipc (puntos)")
    elif fuente == "mindicador":
        if indicador == "serie":
            raise ValueError("`serie` solo existe para el Banco Central")
        a, m, d = _fecha(fecha)
        url = MINDICADOR + indicador + (f"/{d}-{m}-{a}" if d else "")
        filas = parse_mindicador(_get(url, fetch), indicador)
    else:
        raise ValueError("fuente debe ser cmf, bcch, sii, mindicador o auto")
    nombres = {"cmf": "CMF", "bcch": "Banco Central de Chile (BDE)", "sii": "SII (tablas web, oficial)",
               "mindicador": "mindicador.cl (TERCEROS, no oficial)"}
    return {"indicador": indicador, "fuente": nombres[fuente],
            "consulta": url, "datos": filas,
            "nota": "Cita la fuente. Confirma el formato de respuesta con una consulta real."}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fuente", default="auto", choices=("auto", "cmf", "bcch", "sii", "mindicador"))
    sub = p.add_subparsers(dest="cmd", required=True)
    for ind in CLI_INDICADORES:
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
