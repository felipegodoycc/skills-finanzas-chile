---
description: Revisa una cartola o estado de cuenta (PDF o CSV) - enmascara, limpia duplicados y reembolsos, y detecta suscripciones y gasto hormiga
argument-hint: "<ruta al PDF o CSV>"
---

Revisa el archivo de movimientos `$ARGUMENTS` aplicando las skills del plugin **en este orden**. El orden importa: los datos se enmascaran antes de que tú los leas o analices.

Si no viene una ruta, pídela y explica qué formatos sirven (PDF del banco o CSV/Excel exportado). No pidas que pegue la cartola en el chat.

1. **Entrada segura** (`entrada-segura-de-datos`, y para PDF `lectura-pdf-segura`):
   - PDF: convierte con `scripts/pdf_a_markdown.py` de `lectura-pdf-segura`. Si tiene clave, usa `--clave-stdin`, `--clave-archivo` o `--clave-env`; **nunca** pidas ni escribas la clave en el chat ni en la línea de comandos.
   - CSV/Excel: normaliza con `scripts/normalizar_movimientos.py` de `entrada-segura-de-datos` (pregunta qué columnas son fecha, glosa y monto si no es obvio).
   - Trabaja solo sobre la salida enmascarada, no sobre el archivo original. Recuérdale al usuario que el enmascarado no oculta nombres, comercios ni montos, y que revise la salida.
2. **Calidad de datos** (`calidad-de-datos-financieros`): marca duplicados, reembolsos y fondos de terceros con sus scripts. No borres nada; muestra los casos dudosos para que el usuario decida.
3. **Gasto recurrente** (`analisis-gasto-recurrente`): detecta suscripciones y gasto hormiga sobre los datos ya depurados, declarando que los umbrales son operativos, y propone eliminar, reemplazar o controlar cada uno.

Usa el formato de entrada que pide cada script según su SKILL.md; si un paso necesita convertir de formato, hazlo con código y dilo. Aplica `guardrails-finanzas-chile` en todo momento. Al final, si el usuario quiere ir más allá del gasto, sugiere `/diagnostico`.
