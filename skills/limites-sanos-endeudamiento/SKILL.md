---
name: limites-sanos-endeudamiento
description: Compara la carga de deuda de una persona (pago mensual de deudas sobre ingreso) con umbrales sostenibles que dependen del tramo de ingreso y de si hay hipotecario, según Lemus y Pulgar (2021; publicado en 2023). Úsala cuando pregunten si su nivel de deuda es "sano", sostenible o preocupante.
---

# Límites "sanos" de endeudamiento

## La respuesta corta (y por qué no es un número)
**No existe un umbral único sano.** El estudio de Lemus y Pulgar (MPRA Paper 106958, 2021; Revista de Análisis Económico 38(1), 2023; Pulgar trabaja en la CMF) define "sostenible" como la carga máxima a la que la tasa implícita que cobraría un banco (con spread) no supera la TMC. Resultado: los umbrales **suben con el ingreso** y **con la deuda hipotecaria**.
- Sin hipotecario, RCI máximo por ingreso mensual: $300k 6%; $500k 13%; $1M 22%; $2M 31%; $4M 41% (agregado 23%).
- Con hipotecario: $300k 24%; $1M 43%; $2M 53%; $4M 65% (agregado 51%).
- El **50%** de la CMF es un umbral de *reporte* de alta carga, no un nivel sano. La mediana (11,9% en jun-2025) es descriptiva, no una meta.

## Cómo usarla
1. Pide ingreso líquido mensual, pago mensual de **todas** las deudas financieras (con intereses; incluye hipotecario si lo hay) y, opcional, la deuda total sin intereses futuros.
2. Ejecuta `scripts/limites.py --ingreso X --servicio-deuda Y [--hipotecario] [--deuda-sin-interes Z]`. Los umbrales están en `data/umbrales_lemus_pulgar_2021.json` (con fuente y limitaciones); los valores intermedios se interpolan linealmente (aproximación de este repositorio).
3. Reporta el RCI, el umbral de su tramo, el margen en puntos y la **banda** (holgado < 70% del umbral, cercano 70–100%, sobre ≥ 100%). Las bandas son una convención del repositorio.
4. Siempre agrega las limitaciones del estudio.

## Limitaciones (di al menos tres al usuario)
- Estimado con la EFH 2017 y un modelo, no es una norma.
- Son umbrales de **hogar**; con ingreso individual es una aproximación.
- Dependen de la TMC y del costo de fondeo supuestos; no modelan el gasto de subsistencia ni el racionamiento de crédito.
- Un RCI bajo el umbral no prueba que la deuda sea sana para tu caso; sobre el umbral tampoco implica impago.
- Fuera de rango de ingreso del estudio, el valor es el del extremo.

## Complementos
- Compara además con `endeudamiento-cmf` (definiciones del informe oficial).
- Evidencia internacional: el servicio de deuda predice estrés mejor que los ratios de stock (BIS WP 1235; Kronick y Ambler 2023), pero es evidencia a nivel macro; aplicarla a una persona es una analogía. El tope DTI 43% de EE.UU. fue una regla de crédito hipotecario, no una prueba de salud financiera.

## Caso de ejemplo
`docs/casos/casos.md`, caso 1.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera ni crediticia regulada. Verifica con la entidad correspondiente.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
