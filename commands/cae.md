---
description: Calcula la CAE y el costo total (CTC) de un crédito de consumo desde el monto recibido, la cuota y el número de cuotas
argument-hint: "<monto recibido> <cuota> <n° de cuotas> [pago inicial]"
---

Calcula el costo de un crédito de consumo con la skill `credito-cae-ctc` y las reglas de `guardrails-finanzas-chile`.

Datos que entregó el usuario (puede venir vacío o incompleto): $ARGUMENTS

1. **Primero descarta el crédito de estudios.** Si el usuario habla de la universidad, el instituto, la Comisión Ingresa o "mi CAE" sin un crédito de consumo a la vista, pregunta a cuál se refiere y, si es el Crédito con Aval del Estado, sigue la sección de la skill para ese caso, sin calcular.
2. Interpreta los argumentos en este orden: monto **efectivamente recibido** (neto de gastos retenidos), valor de la cuota total, número de cuotas y, opcionalmente, pago inicial. Si falta alguno o no está claro qué es, pregúntalo; no lo supongas.
3. Ejecuta `scripts/cae.py credito --monto-neto X --cuota Y --n N [--pago-inicial Z]` de esa skill. No calcules la CAE de memoria.
4. Informa la CAE, la tasa periódica y el CTC, y aclara que la fórmula viene de un **borrador** de reglamento cuya vigencia no está verificada: la CAE vinculante es la que informa la institución en la hoja resumen. Si el usuario tiene esa CAE, contrástala y reporta la diferencia sin asumir error de nadie.
5. Si quiere comparar ofertas, pide mismo monto y mismo plazo, y recuerda que una CAE menor no hace mejor un crédito por sí sola. No recomiendes una institución.
