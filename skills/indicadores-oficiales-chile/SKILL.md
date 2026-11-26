---
name: indicadores-oficiales-chile
description: Obtiene UF, UTM, IPC y dólar desde APIs oficiales (CMF y Banco Central) con un script y clave personal. Úsala cuando necesites un valor vigente de UF/UTM/UTA o tipo de cambio para convertir montos, topes o comisiones.
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

## Cómo usarla
1. Pide al usuario que cree su clave y la ponga en el entorno: `CMF_API_KEY` o `BCCH_API_TOKEN`. **Nunca la pegues en el chat, en un archivo del repo ni en un argumento de línea de comandos.**
2. Ejecuta `scripts/indicadores.py`:
   - `indicadores.py uf` (hoy) o `uf --fecha 2026-11-26`
   - `indicadores.py utm --fecha 2026-11`
   - `indicadores.py serie --codigo F073.UFF.PRE.Z.D --desde 2026-11-01 --hasta 2026-11-26`
3. Informa el valor **con fecha y fuente**. Si falla (sin clave, sin red, respuesta inesperada), dilo y pide el valor al usuario; no lo inventes.
4. La **UTA** es 12 veces la UTM del mes de diciembre del año anterior solo si la fuente lo define así: toma el valor de la fuente oficial, no lo derives por tu cuenta.

## Límites
- Sin conexión desde un entorno restringido, el script falla con un mensaje claro: pasa el valor manualmente.
- Los tests usan respuestas simuladas, no reales.
