---
description: Diagnóstico financiero guiado (objetivos, flujo, carga de deuda) y derivación a las skills que correspondan
argument-hint: "[descripción breve de tu situación, opcional]"
---

Inicia un diagnóstico financiero siguiendo la skill `diagnostico-financiero` del plugin, con su flujo en el orden que indica, su aviso obligatorio al inicio y al final, y las reglas de `guardrails-finanzas-chile`.

Situación que entregó el usuario (puede venir vacía): $ARGUMENTS

- Si viene vacía, parte preguntando por los objetivos y luego por ingresos, gastos y deudas; pide solo lo mínimo para el siguiente paso.
- Si el usuario va a entregar datos reales (cartolas, movimientos), aplica antes `entrada-segura-de-datos` o sugiere `/revisar-cartola`.
- Los cálculos los hacen los scripts de las skills, no estimaciones de memoria.
