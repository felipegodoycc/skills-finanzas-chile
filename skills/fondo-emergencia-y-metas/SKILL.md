---
name: fondo-emergencia-y-metas
description: Dimensiona el colchón de emergencia (meses de gastos esenciales cubiertos), fija metas por tramos y calcula en cuánto tiempo se alcanzan, y alinea los objetivos del usuario (comprar algo, ahorrar, salir de deuda) con la evidencia disponible. Úsala cuando pregunten cuánto ahorrar, cuánto fondo de emergencia necesitan o si pueden hacer una compra grande.
---

# Colchón de emergencia y metas

## Qué dicen las fuentes (todas heurísticas; ninguna es norma)
- **CMF:** menciona el fondo de emergencia como una posible meta, **sin dar monto ni meses**.
- **"3 a 6 meses"** es una convención; no hay evidencia oficial chilena. JPMorgan Chase Institute (EE.UU., datos bancarios) sugiere ~6 semanas de ingreso neto para volatilidad típica, y más con ingreso volátil. **Aplicabilidad a Chile no verificada.**
- **Seguro de Cesantía (AFC):** cuenta individual financiada con 3% de la renta imponible en contratos indefinidos; no cubre a todos ni reemplaza el colchón (funcionarios públicos excluidos; el Fondo de Cesantía Solidario exige causales y cotizaciones).
- **Datos descriptivos (CAF-CMF 2023, autorreporte):** 38% cubriría un gasto inesperado de un mes de ingreso; 25% se siente sobreendeudado.
- **Ahorro:** Save More Tomorrow (Thaler y Benartzi, 2004) funciona comprometiendo parte de los aumentos futuros (evidencia fuerte en jubilación de EE.UU.; en Chile es extrapolación, p. ej. APV). Fernandes et al. (2014): la educación sola cambia poco la conducta; automatiza.

## Método
1. **Gastos esenciales mensuales** = lo que no puedes dejar de pagar en un mes (vivienda, servicios, alimentación, salud, transporte, deudas obligatorias). Pídelos con datos.
2. **Liquidez real**: separa lo líquido (cuenta, fondo conservador con rescate de 1 a 3 días) de lo no líquido (renta variable, plazos largos, rescate con comisión o pérdida). Solo lo líquido es colchón.
3. `scripts/colchon.py --json datos.json` → meses cubiertos, metas (piso, 1 mes, 3 y 6 meses; 6 y 9 si el ingreso es variable; la referencia de 6 semanas de EE.UU.) y meses para alcanzarlas con tu aporte y con cuotas que se liberan.
4. **Orden:** piso de colchón → deuda más cara → completar meta. Con una deuda a >30% anual, el interés que evitas suele pesar más que el rendimiento del colchón; pero no te quedes sin piso.
5. **Compras grandes:** convierte el deseo en condiciones medibles (deuda cara en cero, flujo ≥ 0 por N meses, colchón sobre el piso después de comprar). Calcula el costo si se financia con `cotizacion-y-comparacion`.
6. **Objetivos del usuario:** pregunta para qué ahorra y para cuándo (corto, mediano, largo plazo, como en CMF Educa) y asigna instrumento por plazo, liquidez y riesgo, sin recomendar productos concretos.

## Errores a evitar
Contar como colchón dinero con riesgo de pérdida; usar una meta de meses como norma; fijar un piso sin explicar de dónde sale; ignorar la volatilidad del ingreso.

## Caso de ejemplo
`docs/casos/casos.md`, casos 2 y 3.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera ni de inversión. Las metas de meses son heurísticas.
