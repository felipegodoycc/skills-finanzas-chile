#!/usr/bin/env python3
"""Lee UF, UTM, UTA, IPC y dólar desde un archivo que el usuario descargó de una fuente OFICIAL.

El script NO se conecta a internet. El usuario abre la página o la API oficial en su
navegador, guarda la respuesta y pasa el archivo con --archivo:
- sii  : página HTML de https://www.sii.cl/valores_y_fechas/ ("Guardar como").
         UF: uf/ufAAAA.htm (tabla anual, una fila por día). UTM/UTA/IPC: utm/utmAAAA.htm.
- cmf  : JSON de https://api.cmfchile.cl/api-sbifv3/recursos_api/<indicador>?formato=json&apikey=...
- bcch : JSON de https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?function=GetSeries&...
La clave de la CMF o del Banco Central queda en el navegador del usuario: el script no la ve.

LIMITES (declarados)
- SII: el lector busca filas <tr> y es tolerante; si el SII rediseña la página, falla
  con un mensaje claro. Probado con la página real el 26-11-2026 (UF, UTM, UTA).
- CMF y BCCh: la forma exacta del JSON no figura en la documentación revisada; el lector
  es tolerante (busca pares Valor/Fecha u Obs). Sin prueba con una respuesta real.
- Cita la fuente: el Banco Central pide mencionarse como propietario del dato.

Uso:
  indicadores.py --fuente sii --archivo uf2026.htm uf --fecha 2026-11-26
  indicadores.py --fuente sii --archivo utm2026.htm utm --fecha 2026-11
  indicadores.py --fuente cmf --archivo uf.json uf
  indicadores.py --fuente bcch --archivo serie.json dolar
"""
import argparse
import datetime
import json
import re
import sys

INDICADORES = ("uf", "utm", "uta", "ipc", "dolar", "euro")
NOMBRES = {"cmf": "CMF", "bcch": "Banco Central de Chile (BDE)", "sii": "SII (tablas web, oficial)"}


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


def _fecha(fecha):
    m = re.fullmatch(r"(\d{4})-(\d{2})(?:-(\d{2}))?", fecha or "")
    if fecha and not m:
        raise ValueError("fecha inválida: usa YYYY-MM-DD o YYYY-MM")
    return m.groups() if m else (None, None, None)


def leer(indicador, texto, fuente, fecha=None):
    """Extrae el indicador del contenido ya descargado por el usuario."""
    if fuente == "cmf":
        filas = parse_cmf(texto)
    elif fuente == "bcch":
        filas = parse_bcch(texto)
    elif fuente == "sii":
        a, m, d = _fecha(fecha)
        hoy = datetime.date.today()
        a, m = int(a or hoy.year), int(m or hoy.month)
        if indicador == "uf":
            d = int(d or hoy.day)
            filas = [{"fecha": f"{a}-{m:02d}-{d:02d}", "valor": parse_sii_uf(texto, m, d)}]
        elif indicador in ("utm", "uta", "ipc"):
            filas = [{"fecha": f"{a}-{m:02d}", "valor": parse_sii_mensual(texto, m, indicador)}]
        else:
            raise ValueError("El SII cubre uf, utm, uta e ipc (puntos)")
    else:
        raise ValueError("fuente debe ser sii, cmf o bcch")
    return {"indicador": indicador, "fuente": NOMBRES[fuente], "datos": filas,
            "nota": "Cita la fuente y la fecha de descarga del archivo."}


USO_NUEVO = ("uso: indicadores.py --fuente sii|cmf|bcch --archivo <HTML o JSON guardado> <indicador> [--fecha ...]. "
             "Abre la página oficial en tu navegador, guárdala y pasa el archivo; ver la skill indicadores-oficiales-chile.")


def migrar(a, extra):
    """Explica en vez de fallar con un error genérico cuando llega la interfaz antigua (con red)."""
    if a.fuente in ("auto", "mindicador") or a.indicador == "serie" or "--codigo" in extra:
        return ("desde la versión 0.3 el script ya no se conecta a internet: se quitaron --fuente auto, "
                "--fuente mindicador (no oficial) y el comando serie. " + USO_NUEVO)
    if extra:
        return "argumentos no reconocidos: " + " ".join(extra) + ". " + USO_NUEVO
    if a.fuente not in ("sii", "cmf", "bcch"):
        return ("falta --fuente sii, cmf o bcch. " if not a.fuente else f"fuente desconocida: {a.fuente}. ") + USO_NUEVO
    if not a.archivo:
        return "falta --archivo: el script ya no descarga datos. " + USO_NUEVO
    if a.indicador not in INDICADORES:
        return f"indicador desconocido: {a.indicador} (usa {', '.join(INDICADORES)})"
    return None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--fuente", help="sii, cmf o bcch")
    p.add_argument("--archivo", help="HTML o JSON guardado desde la fuente oficial")
    p.add_argument("indicador", help=", ".join(INDICADORES))
    p.add_argument("--fecha", help="YYYY-MM-DD (UF) o YYYY-MM (UTM, UTA, IPC); solo para --fuente sii")
    a, extra = p.parse_known_args(argv)
    error = migrar(a, extra)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    try:
        with open(a.archivo, encoding="utf-8", errors="replace") as f:
            out = leer(a.indicador, f.read(), a.fuente, a.fecha)
    except (OSError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
