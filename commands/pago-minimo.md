---
description: Calcula el pago mínimo de la tarjeta de crédito con la fórmula de la NCG 537 y el costo de pagar solo el mínimo
argument-hint: "[datos del estado de cuenta, sin el número de la tarjeta]"
---

Calcula el pago mínimo de una tarjeta de crédito con la skill `pago-minimo-tarjetas` y las reglas de `guardrails-finanzas-chile`.

Datos que entregó el usuario (puede venir vacío): $ARGUMENTS

1. Pide del estado de cuenta, si faltan: intereses, comisiones y otros cargos del período; valor de las cuotas sin interés facturadas; el resto de lo facturado; y la fecha de facturación. Nunca pidas el número de la tarjeta.
2. Ejecuta `scripts/pago_minimo.py calcular --cargos X --cuotas-sin-interes Y --otros Z --fecha YYYY-MM-DD` de esa skill. No calcules el mínimo de memoria. Si la fecha es anterior al 04-06-2026, el script la rechaza: explica que entonces regía la regla de cada emisor.
3. Contrasta con el mínimo que informa el estado de cuenta, si el usuario lo tiene.
4. Si el usuario piensa pagar solo el mínimo, ofrece calcular el costo con `pago_minimo.py solo-minimo --saldo S --tasa-mensual T`, y la proyección de los próximos meses con `proyectar` si tiene compras en cuotas (el mínimo sube mientras existan). Declara los supuestos de cada cálculo.
5. Explica que el mínimo sirve para la liquidez de un mes difícil, no para pagar la deuda, y que el saldo que queda paga la tasa del crédito rotativo.
