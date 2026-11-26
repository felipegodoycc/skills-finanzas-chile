---
name: pago-minimo-tarjetas
description: Calcula y proyecta el pago mínimo de tarjetas de crédito con la fórmula de la NCG 537 de la CMF (Ley 21.673) y simula cuánto cuesta pagar solo el mínimo. Úsala cuando pregunten por el pago mínimo, si pueden pagar solo el mínimo o cómo cambia el mínimo con las cuotas sin interés.
---

# Pago mínimo en tarjetas (NCG 537)

## Qué dice la norma (nivel: norma; fuente: CMF, comunicado del 29-05-2026)
- **Pago mínimo = 100% del Monto No Financiable (MNF) + 5% del Monto Financiable (MF).**
  MNF = cuotas sin interés (según la etapa), intereses, comisiones y otros cargos. MF = el resto de lo facturado.
- Es un **piso**: el emisor puede exigir un mínimo mayor.
- **Calendario de las cuotas sin interés:** desde el 04-06-2026 están en el MF (entra solo 5% de su valor); luego pasan al MNF "a una tasa de 25% cada 6 meses" hasta 100% el 04-06-2028 (**norma**). Los hitos intermedios (04-12-2026, 04-06-2027, 04-12-2027) son **deducidos** del texto, no datos explícitos.
- Excepciones (comunicado CMF de la NCG 537: https://www.cmfchile.cl/portal/prensa/615/w3-article-95105.html): el emisor puede eximir del pago mínimo según sus políticas internas, con dos condiciones: la deuda exceptuada debe amortizarse totalmente en un máximo de 24 meses y cada excepción dura como máximo dos meses consecutivos. El comunicado no lista las situaciones que las habilitan: consulta el texto de la NCG 537 y la política de tu emisor.
- Ojo: algunos medios dijeron "25% de la deuda en dic-2026". No coincide con el texto de la CMF: es el 25% de las *cuotas sin interés* que se reclasifica. Usa solo la fuente oficial.

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
- No declarar que las fechas intermedias fueron deducidas.

## Caso de ejemplo
`docs/casos/casos.md`, caso 7.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera. Verifica el cálculo con tu emisor y con la NCG 537.
