---
name: pago-minimo-tarjetas
description: Calcula y proyecta el pago mínimo de tarjetas de crédito con la fórmula de la NCG 537 de la CMF (Ley 21.673) y simula cuánto cuesta pagar solo el mínimo. Úsala cuando pregunten por el pago mínimo, si pueden pagar solo el mínimo o cómo cambia el mínimo con las cuotas sin interés.
---

# Pago mínimo en tarjetas (NCG 537)

## Qué dice la norma (nivel: norma; fuente: texto de la NCG 537, 04-06-2025, leído completo el 26-11-2026; comunicados CMF del 04-06-2025 y 29-05-2026)
- **Pago mínimo = 100% del Monto No Financiable (MNF) + 5% del Monto Financiable (MF).**
  MNF = cuotas sin interés (según la etapa), intereses, comisiones y otros cargos. MF = el resto de lo facturado.
- Es un **piso**: el emisor puede exigir un mínimo mayor.
- **Calendario de las cuotas sin interés:** desde el 04-06-2026 están en el MF (entra solo 5% de su valor); luego pasan al MNF "a una tasa de 25% cada 6 meses" hasta 100% el 04-06-2028 (**norma**). El texto de la NCG fija 25%, 50% y 75% "luego de 6, 12 y 18 meses" de aplicada la fórmula (12 meses después de su publicación); las fechas 04-12-2026, 04-06-2027 y 04-12-2027 resultan de contar esos meses desde el 04-06-2026. En la etapa inicial la fórmula es PM ≥ MNF_A + 5% · (MF + 100% de las cuotas sin interés), donde MNF_A es el MNF sin las cuotas sin interés.
- **Componentes (NCG 537, numeral 5.2):** el MNF incluye cuotas sin interés pagaderas en el período; intereses (refundidos, rotativos, moratorios, de cuotas pagaderas en el período u otros); comisiones; y otros cargos (impuestos, cargos administrativos, operativos o de mantención, primas de seguros, cargos por productos voluntarios, saldos morosos, costos de cobranza). El MF es lo facturado menos el MNF e incluye las cuotas con interés. Se calcula sobre el monto facturado antes de cualquier renegociación que posponga el pago, aunque el deudor consienta.
- **Excepciones (numeral 5.3):** el emisor puede eximir del pago mínimo en situaciones excepcionales si la deuda exceptuada se amortiza totalmente en un máximo de 24 meses y la excepción dura como máximo dos meses consecutivos. La norma **no lista** las situaciones: cada emisor define y documenta su política, que la CMF puede revisar.
- **Emisores no bancarios:** se atienen a lo dispuesto por el Banco Central y al Capítulo 8-41 de la RAN (Circular N°1, numeral 6.6).
- Ojo: algunos medios dijeron "25% de la deuda en dic-2026". No coincide con el texto de la CMF: es el 25% de las *cuotas sin interés* que se reclasifica. Usa solo la fuente oficial.

## Contraste con liquidaciones reales (26-11-2026)
Con 7 estados de cuenta de una tarjeta BCI (ago-nov 2026), el piso `MNF + 5% · (facturado − MNF)` coincidió al peso (±1) en todos, tomando como MNF los intereses, las comisiones brutas y el impuesto de timbres. Dos detalles que el contraste mostró: el "traspaso de deuda internacional" quedó en el MF, y la devolución de comisión (DEV.COM) **no** redujo el MNF. En Santander y CMR el mínimo cobrado fue mayor que el piso, lo que es compatible con que la norma fije un piso; su regla propia no se pudo confirmar. Muestra pequeña y un solo emisor con calce exacto: no es una prueba general.

## Cómo usarla
1. `scripts/pago_minimo.py calcular --cargos X --cuotas-sin-interes Y --otros Z --fecha YYYY-MM-DD`
   - cargos = intereses + comisiones + otros cargos del período; cuotas-sin-interes = valor de las cuotas sin interés facturadas; otros = el resto facturado.
2. **Proyección:** `pago_minimo.py proyectar --json plan.json --flujo N` con los próximos meses (cuotas pactadas y su calendario); marca los meses en que el mínimo supera tu flujo. Es lo importante: el mínimo **sube** mientras tengas compras en cuotas sin interés.
3. **Costo de pagar solo el mínimo:** `pago_minimo.py solo-minimo --saldo S --tasa-mensual T`. Supone sin compras nuevas y tasa y cargos constantes. Pagar el 5% del saldo más intereses saldaría la deuda en años; la CMF estimó que amortizar solo 1% del saldo tomaría unos 180 meses y ~160% en intereses (régimen previo).

## Cómo interpretarlo
- El mínimo es un instrumento de **liquidez**, no de pago; sirve en un mes complicado, pero dejar saldo rotativo es la deuda más cara (en mayo de 2026 el rotativo promedió ~32% anual frente a ~11% en compras en cuotas: dato secundario de prensa).
- Alerta con anticipación los meses en que el mínimo proyectado supera el flujo; no esperes a que ocurra.

## Errores a evitar
- Tratar el mínimo de un mes como permanente.
- Suponer que el mínimo es 5% de todo.
- Antes del 04-06-2026 aplicaba la regla del emisor: el script rechaza esas fechas.

## Caso de ejemplo
`docs/casos/casos.md`, caso 7.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera. Verifica el cálculo con tu emisor y con la NCG 537.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
