---
name: endeudamiento-cmf
description: Calcula e interpreta indicadores de endeudamiento personal con las definiciones del Informe de Endeudamiento de la CMF de Chile (carga financiera, apalancamiento, alta carga >50%) y los compara con la mediana nacional sin confundir datos descriptivos con metas. Úsala cuando pregunten si su nivel de deuda es alto, sobreendeudamiento o carga de deuda sobre ingreso.
---

# Indicadores de endeudamiento (definiciones CMF)

## Definiciones (fuente: CMF)
La metodología del informe evalúa tres dimensiones: **nivel de deuda**, **carga financiera** (porcentaje del ingreso mensual destinado al pago de obligaciones financieras) y **apalancamiento** (deuda total medida en veces el ingreso mensual). https://www.cmfchile.cl/portal/prensa/615/articles-60458_doc_pdf.pdf — el informe define la carga sobre el **ingreso líquido total** (https://www.cmfchile.cl/portal/estadisticas/617/articles-77055_doc_pdf.pdf).

**Alta carga financiera o sobreendeudamiento** = destinar **más del 50%** del ingreso mensual a pagar deuda.

## Cifras de referencia (Informe de Endeudamiento 2025, datos a junio 2025, publicado 21-01-2026)
Fuente: https://www.cmfchile.cl/portal/prensa/615/articles-102984_doc_pdf.pdf
- Deuda mediana: $1.680.453 (caída real anual de 16,9%).
- Carga financiera mediana: 11,9% del ingreso mensual (13,6% en jun-2024).
- Deudores con alta carga (>50%): 14,1% (16,5% el año anterior).
- Cobertura estimada: ~84% de las obligaciones de los hogares, 6,1 millones de deudores.
- El informe **no captura** parte de la deuda no bancaria formal ni la informal.

## Cómo usarlo
1. Ingreso **líquido** mensual (confiable, no bonos esporádicos) y servicio de deuda **financiera** mensual (cuotas de créditos, pagos de tarjetas, líneas). Excluye gastos corrientes.
2. Ejecuta `scripts/indicadores.py --ingreso X --servicio-deuda Y --deuda-total Z`.
3. Reporta carga, apalancamiento y si supera el umbral.

## Errores que debes evitar (importante)
- **Mediana ≠ meta.** 11,9% es lo que observa la CMF en deudores formales, no una carga recomendable. Nadie en las fuentes oficiales consultadas la propone como objetivo.
- **50% ≠ nivel sano.** Es el umbral con que la CMF clasifica sobreendeudamiento para reportar. Estar en 35% no significa estar bien.
- **La sostenibilidad es individual.** Depende de gastos fijos, dependientes, estabilidad del ingreso y liquidez. Esta skill mide el indicador; no concluye sostenibilidad.
- La guía educativa de la CMF advierte que sus pasos son generales y cada persona debe distinguir qué le sirve (https://www.cmfchile.cl/educa/621/w3-article-93975.html).

## Para quien está sobreendeudado
La CMF propone en "La Ruta del endeudamiento" pasos para quien ya está sobreendeudado; su criterio clave: que la nueva carga financiera mensual **sea algo que se pueda pagar** y que la persona se comprometa a no seguir aumentando su endeudamiento (https://www.cmfchile.cl/educa/621/w3-article-93975.html). Ver también `cobranza-y-renegociacion`.

## Pendiente
El Banco Central publicó un estudio sobre **endeudamiento máximo sostenible de los hogares en Chile** (https://www.bcentral.cl/documents/d/banco-central/lemus-y-pulgar-2023); no lo revisé en detalle, así que esta skill no cita umbrales de él.
