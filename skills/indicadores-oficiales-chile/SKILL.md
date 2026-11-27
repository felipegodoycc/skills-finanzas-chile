---
name: indicadores-oficiales-chile
description: "Indica dónde consultar UF, UTM, UTA, IPC y dólar en fuentes oficiales (SII, CMF, Banco Central) y lee con un script el archivo que el usuario descargó, sin conectarse a internet. Úsala cuando necesites un valor vigente de UF/UTM/UTA o tipo de cambio para convertir montos, topes o comisiones."
---

# Indicadores oficiales de Chile (UF, UTM, IPC, dólar)

**Estado: N3 en la fuente, código con tests sobre contenido simulado.** El lector del SII se probó con la página real (26-11-2026); el de CMF y Banco Central no.

## Por qué existe
Varias skills dependen de valores que cambian (UF para topes y comisiones, UTM para la bonificación del APV, UF de 20 para la CAE de tarjetas). Nunca los escribas de memoria: el valor viene de una fuente oficial, con fecha y fuente.

## El plugin no se conecta a internet
El script solo lee un archivo que el usuario ya descargó. Si tu entorno tiene una herramienta web propia y el usuario lo acepta, puedes abrir tú la página oficial; si no, pídele el valor o el archivo.

## Dónde consultar (fuentes oficiales)
| Fuente | Dónde | Clave | Cubre | `--fuente` |
|---|---|---|---|---|
| SII | `https://www.sii.cl/valores_y_fechas/` (UF: `uf/ufAAAA.htm`; UTM, UTA e IPC: `utm/utmAAAA.htm`) | no | UF, UTM, UTA, IPC (puntos) | `sii` |
| CMF | `https://api.cmfchile.cl/api-sbifv3/recursos_api/uf?formato=json&apikey=...` (también `uf/2026/11/dias/26`; `utm`, `ipc`, `dolar`, `euro` por confirmar) | sí, gratis | UF, UTM, IPC, dólar, euro | `cmf` |
| Banco Central (BDE) | `https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx?function=GetSeries&timeseries=...&token=...` | token gratis ("Mi Cuenta", "Apikey Token") | cualquier serie | `bcch` |

Series de la ayuda oficial de la BDE: UF `F073.UFF.PRE.Z.D`, UTM `F073.UTR.PRE.Z.M`, IPC base 2023 `F074.IPC.VAR.Z.EP23.C.M`, dólar observado `F073.TCO.PRE.Z.D`. El Banco Central pide mencionarse como propietario del dato. La UF mensual cubre del 10 de un mes al 9 del siguiente.

**No uses agregadores de terceros** (mindicador.cl y similares): no son la fuente oficial.

## Cómo usarla
1. Lo más simple: que el usuario abra la página del SII y te dé el valor y la fecha, o guarde la página ("Guardar como", HTML).
2. Si usa la CMF o el Banco Central, la clave va **solo en su navegador**. Nunca la pegues en el chat, en un archivo del repo ni en un argumento.
3. Con el archivo guardado, ejecuta `scripts/indicadores.py`:
   - `indicadores.py --fuente sii --archivo uf2026.htm uf --fecha 2026-11-26`
   - `indicadores.py --fuente sii --archivo utm2026.htm uta --fecha 2026-11`
   - `indicadores.py --fuente cmf --archivo uf.json uf`
   - `indicadores.py --fuente bcch --archivo serie.json dolar`
4. Informa el valor **con fecha y fuente**. Si el script falla (formato cambiado, valor aún no publicado), dilo y pide el valor; no lo inventes.
5. La **UTA** sale de la tabla del SII; no la derives por tu cuenta.

## Límites
- Los tests usan HTML y JSON simulados. El lector del SII se probó además con la página real (26-11-2026: UF 41.412,34, UTM 72.440, UTA 869.280). IPC del SII, CMF y Banco Central siguen sin prueba real.
- Si el SII rediseña la página, el lector falla con un mensaje claro: copia el valor a mano.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
