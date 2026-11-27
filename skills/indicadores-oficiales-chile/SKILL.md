---
name: indicadores-oficiales-chile
description: Obtiene UF, UTM, UTA, IPC y dólar con un script; el usuario elige la fuente (CMF, Banco Central, SII sin clave, o terceros). Úsala cuando necesites un valor vigente de UF/UTM/UTA o tipo de cambio para convertir montos, topes o comisiones.
---

# Indicadores oficiales de Chile (UF, UTM, IPC, dólar)

**Estado: N3 en la fuente, código con tests sobre respuestas simuladas.** El formato real de respuesta JSON no figura en la documentación revisada: confirma con una consulta real antes de automatizar.

## Por qué existe
Varias skills dependen de valores que cambian (UF para topes y comisiones, UTM para la bonificación del APV, UF de 20 para la CAE de tarjetas). Nunca los escribas de memoria: pídelos a la fuente oficial y cita fecha y fuente.

## Fuentes oficiales (gratuitas, con clave personal)
- **CMF:** `https://api.cmfchile.cl/api-sbifv3/recursos_api/` con `apikey` y `formato=json`. Rutas confirmadas para UF: del día (`uf`), por año, mes o día (`uf/2026/11/dias/26`) y por período. La UF mensual cubre del 10 de un mes al 9 del siguiente. `utm`, `ipc`, `dolar` y `euro` siguen el mismo patrón, **por confirmar**.
- **Banco Central (BDE):** `https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx` con `token`, `function=GetSeries` y `timeseries`. El token se obtiene en la BDE, "Mi Cuenta", "Apikey Token". Series de la ayuda oficial: UF `F073.UFF.PRE.Z.D`, UTM `F073.UTR.PRE.Z.M`, IPC base 2023 `F074.IPC.VAR.Z.EP23.C.M`, dólar observado `F073.TCO.PRE.Z.D`. Condición de uso: mencionar al Banco Central como propietario del dato.
- **No uses agregadores de terceros** (mindicador.cl y similares): no son la fuente oficial.
- El SII publica UTM y UTA en `sii.cl/valores_y_fechas`; no ofrece API, solo páginas.

## Opciones sin clave (el usuario elige)
| Fuente | `--fuente` | Clave | Oficial | Cubre | Riesgo |
|---|---|---|---|---|---|
| CMF | `cmf` | sí, gratis | sí | UF, UTM, IPC, dólar, euro | rutas distintas de `uf` por confirmar |
| Banco Central | `bcch` | token gratis | sí | cualquier serie de la BDE | formato JSON sin ejemplo oficial |
| SII | `sii` | no | sí | UF, UTM, UTA, IPC (puntos) | lee HTML: si el SII rediseña la página, falla. **Probado con la página real el 26-11-2026**: UF 41.412,34, UTM 72.440, UTA 869.280 |
| mindicador.cl | `mindicador` | no | **no, terceros** | UF, UTM, dólar, IPC, otros | depende de un tercero; rutas sin verificar |
| A mano | n/a | no | sí | lo que copies de sii.cl | error humano |

`--fuente auto` (por defecto) solo usa CMF o Banco Central si hay clave en el entorno. **Nunca elige SII ni terceros por su cuenta**: si no hay clave, el script lista las opciones y la persona decide. Si usas `mindicador`, dilo en la respuesta: no es fuente oficial.

## Cómo usarla
1. Si el usuario quiere CMF o Banco Central, pídele que cree su clave y la ponga en el entorno: `CMF_API_KEY` o `BCCH_API_TOKEN`. **Nunca la pegues en el chat, en un archivo del repo ni en un argumento de línea de comandos.**
2. Ejecuta `scripts/indicadores.py`:
   - `indicadores.py --fuente sii uf` (sin clave)
   - `indicadores.py uf` (hoy, con clave) o `uf --fecha 2026-11-26`
   - `indicadores.py utm --fecha 2026-11`
   - `indicadores.py serie --codigo F073.UFF.PRE.Z.D --desde 2026-11-01 --hasta 2026-11-26`
3. Informa el valor **con fecha y fuente**. Si falla (sin clave, sin red, respuesta inesperada), dilo y pide el valor al usuario; no lo inventes.
4. La **UTA** sale de la tabla del SII (`--fuente sii uta`); no la derives por tu cuenta.

## Límites
- Sin conexión desde un entorno restringido, el script falla con un mensaje claro: pasa el valor manualmente.
- Los tests usan respuestas y HTML simulados, no reales; los tests usan HTML simulado, pero el lector del SII se probó además contra la página real (26-11-2026, UF, UTM y UTA). IPC del SII, CMF, Banco Central y mindicador siguen sin prueba real.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
