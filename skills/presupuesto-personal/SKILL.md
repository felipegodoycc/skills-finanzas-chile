---
name: presupuesto-personal
description: Construye un presupuesto realista en Chile con fase de transición mes a mes mientras duran las cuotas pactadas, límites de alerta graduales por categoría y brecha acumulada. Úsala cuando pidan armar un presupuesto, saber cuánto pueden gastar o cómo cumplir una meta de ahorro.
---

# Presupuesto personal (régimen y transición)

## Base oficial (nivel: dato oficial)
CMF Educa propone 3 pasos: **1)** revisar gastos e ingresos y qué % del ingreso va a cada categoría, **2)** definir el objetivo de ahorro (corto, mediano, largo plazo), **3)** respetar el plan. Clasifica como fijos: servicios, supermercado, farmacia, transporte, colegiaturas y cuotas de deudas; y menciona los gastos "hormiga". **La CMF no da cifras**: ni % de ahorro, ni meses de fondo de emergencia, ni proporción máxima para deuda.
- **50/30/20** (Warren y Tyagi, 2005) es una heurística sin evidencia de efectividad encontrada; en Chile arriendo más deuda pueden superar el 50%. Úsala solo como referencia.

## Método
1. **Ingreso estable.** Solo lo seguro; bonos, aguinaldo e ingresos variables quedan fuera del mensual (se usan según `plan-refinanciamiento` y `fondo-emergencia-y-metas`).
2. **Gasto real.** Promedio de 3 a 6 meses de movimientos limpios (`calidad-de-datos-financieros`). Presupuestar con lo que la persona *cree* gastar falla.
3. **Fijos y cuotas pactadas.** Separa fijos y el calendario de cuotas pactadas (tarjetas, créditos).
4. **Margen variable por mes** = ingreso − fijos − cuotas de ese mes.
5. **Metas por categoría** (propuestas, no normas) y **límites graduales**: el límite baja linealmente del promedio real a la meta en N meses (`scripts/presupuesto.py --json plan.json`). Una meta igual a cero margen desde el día 1 produce alertas diarias que se ignoran.
6. **Brecha y colchón.** Brecha mensual = margen − límite variable; acumulada. Si es negativa, dice cuánto colchón o ingreso extra cubre la transición.
7. **Revisión mensual** de límites; las alertas parten del promedio real (para no empeorar) y terminan en la meta.

## Interpretación
- Recorte necesario: si supera ~30-40% de las líneas identificables, el plan es frágil; piensa en ingreso o en deuda, no solo en recorte.
- Primero las palancas grandes (vivienda, deuda, transporte); luego las pequeñas (`analisis-gasto-recurrente`).
- Un gusto planificado y acotado hace el plan más sostenible; no lo elimines.
- La evidencia (Fernandes et al. 2014) dice que la educación sola cambia poco la conducta: automatiza ahorro el día del sueldo cuando puedas.

## Errores a evitar
Presupuestar con el gasto percibido; olvidar cuotas ya pactadas; contar bonos como ingreso mensual; fijar metas sin un camino.

## Caso de ejemplo
`docs/casos/casos.md`, caso 4.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera. Las metas son propuestas, no datos ni normas.
