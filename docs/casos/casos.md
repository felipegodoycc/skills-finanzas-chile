# Casos de ejemplo (métodos de análisis)

> **Casos ficticios inspirados en situaciones reales; personajes, entidades, montos y fechas inventados.** Muestran *cómo analizar* para llegar al objetivo del usuario, no resultados. Personaje: "Camila", ingreso líquido ficticio de $1.800.000. Toda salida de un agente termina con el aviso: *asesor de IA; verifica con la entidad correspondiente*.

Plantilla: **Petición → Objetivo real → Datos mínimos → Preguntas → Pasos de análisis → Criterio de decisión → Errores a evitar → Skill**.

## Caso 1. "Recorto gastos y no salgo del hoyo" (diagnóstico flujo vs. deuda)
- **Petición:** "Gano $1.800.000, tengo varias deudas y aunque gasto menos no logro salir."
- **Objetivo real:** saber si el problema es de flujo mensual (gasta más de lo que entra) o de estructura de deuda (costo, plazo), y qué palanca mueve más.
- **Datos mínimos:** ingreso líquido estable (sin bonos), listado de deudas (saldo, tasa o CAE, cuota, cuotas restantes, tipo), gasto real de 3 a 6 meses, liquidez disponible.
- **Preguntas:** ¿qué ingresos son seguros y cuáles no?, ¿qué deudas se pagan por planilla?, ¿hay obligaciones no financieras?, ¿cuál es su meta?
- **Pasos:** (1) inventario único de deudas; (2) servicio de deuda mensual total y su proporción del ingreso; (3) flujo = ingreso − servicio de deuda − gasto real; (4) si el flujo es negativo, el problema es de flujo y ninguna consolidación lo arregla; (5) clasificar deudas por costo (CAE) y por consecuencia del impago; (6) recién ahí, evaluar palancas: gasto, ingreso, consolidación o portabilidad, renegociación.
- **Criterio:** priorizar la palanca con mayor efecto mensual para el menor riesgo; contrastar la carga con la banda de su tramo de ingreso, no con un número único.
- **Errores a evitar:** mezclar ingreso variable con base; contar dos veces un pago por planilla; proponer consolidar sin flujo ≥ 0; recomendar una entidad.
- **Skills:** `diagnostico-financiero`, `limites-sanos-endeudamiento`, `plan-refinanciamiento`.

## Caso 2. Un gasto grande antes de ordenar las deudas
- **Petición:** "Quiero comprar un computador de $1.900.000."
- **Objetivo real:** decidir si la compra cabe sin empeorar su situación, y bajo qué condiciones.
- **Datos mínimos:** colchón líquido, deuda con costo alto, flujo mensual, fecha en que lo necesita, si genera ingresos.
- **Preguntas:** ¿es necesidad o deseo?, ¿qué pasa si espera 3 meses?, ¿lo pagaría con deuda?
- **Pasos:** (1) costo real si se financia (CAE de la alternativa); (2) meses de gastos esenciales que cubre el colchón hoy y después de comprar; (3) comparar con el piso de colchón acordado; (4) convertir el "sí/no" en condiciones verificables.
- **Criterio:** se compra cuando se cumplen condiciones medibles: deuda cara en cero, flujo ≥ 0 por N meses seguidos, colchón sobre el piso después de pagar.
- **Errores a evitar:** decir "no" sin alternativa; aceptar financiarlo con deuda cara; fijar un piso sin explicar de dónde sale.
- **Skills:** `fondo-emergencia-y-metas`, `cotizacion-y-comparacion`.

## Caso 3. Qué hacer con un ingreso extraordinario (bono, devolución de impuestos)
- **Petición:** "Me llegará un bono; ¿en qué lo uso?"
- **Objetivo real:** usar el dinero en el orden que más reduce costo y riesgo.
- **Datos mínimos:** monto neto probable (con escenarios), deudas con tasa y saldo, colchón, compromisos próximos.
- **Pasos:** (1) tres escenarios (conservador, central, optimista) con supuestos declarados; (2) verificar el neto, no el bruto; (3) ordenar usos por costo evitado: deuda más cara, colchón hasta el piso, luego el resto; (4) para cada prepago calcular el ahorro neto de interés (tasa implícita, saldo, cuotas restantes, comisión); (5) revisar antes planes de cuotas con interés que cuesten más que el crédito.
- **Criterio:** prepagar lo que más intereses evita por peso, no lo que tiene la cuota más grande; no prepagar un crédito con pocas cuotas restantes si el ahorro es mínimo.
- **Errores a evitar:** gastar el bono antes de que llegue; ignorar la comisión de prepago; comprometer el colchón.
- **Skills:** `plan-refinanciamiento`, `fondo-emergencia-y-metas`.

## Caso 4. Presupuesto realista con fase de transición
- **Petición:** "Ayúdame a armar un presupuesto."
- **Objetivo real:** un plan que se pueda cumplir mes a mes hasta llegar al régimen estable.
- **Datos mínimos:** ingresos estables, gastos reales por categoría (promedio de varios meses), cuotas pactadas con su calendario, metas.
- **Pasos:** (1) separar fijos, variables y deuda; (2) promedio real por categoría con datos limpios; (3) margen para variable = ingreso − fijos − cuotas; (4) presupuesto de régimen estable con meta por línea; (5) presupuesto de transición mes a mes mientras duren las cuotas; (6) cuantificar el déficit acumulado y cómo se cubre; (7) límites de alerta = promedio real al inicio, meta al final, revisión mensual.
- **Criterio:** parte de lo que gasta hoy y baja gradualmente; una meta igual a cero margen desde el primer día se abandona.
- **Errores a evitar:** presupuestar con el gasto que la persona *cree* tener; olvidar las cuotas ya pactadas; contar bonos como ingreso mensual.
- **Skills:** `presupuesto-personal`.

## Caso 5. Gastos recurrentes, suscripciones y gasto hormiga
- **Petición:** "¿En qué se me va la plata?"
- **Objetivo real:** encontrar los cobros recurrentes y pequeños que pueden recortarse sin dañar su bienestar, después de revisar las palancas grandes.
- **Datos mínimos:** movimientos de 3 a 6 meses con fecha, monto y comercio.
- **Pasos:** (1) normalizar comercios; (2) detectar recurrencia y frecuencia alta de montos bajos; (3) totalizar por mes y por año; (4) preguntar uso de cada suscripción en los últimos 30 días; (5) proponer *eliminar*, *reemplazar* o *controlar*; (6) comparar el ahorro posible con las palancas grandes.
- **Criterio:** actuar primero sobre lo de mayor monto anual; el umbral de "hormiga" es una definición operativa declarada (la CMF solo lo define cualitativamente).
- **Errores a evitar:** moralizar el gasto; tratar un gusto planificado como fuga; ignorar renovaciones anuales.
- **Skills:** `analisis-gasto-recurrente`.

## Caso 6. Preparar datos antes de analizar (duplicados y reembolsos)
- **Petición:** cualquier análisis basado en movimientos del banco.
- **Objetivo real:** que los totales sean verdad antes de sacar conclusiones.
- **Pasos:** (1) unificar el formato; (2) buscar duplicados entre fuente en tiempo real y cartola, con ventana de fechas asimétrica; (3) buscar pares entre un estado parcial y uno oficial del mismo periodo; (4) separar traspasos propios, fondos de terceros y reembolsos; (5) tratar el reembolso de una tarjeta adicional como devolución (monto negativo del gasto), no como ingreso; (6) contar el sueldo una sola vez; (7) verificación cruzada y declarar la brecha en vez de forzarla.
- **Criterio:** nunca borrar; toda corrección con respaldo y regla registrada; las cifras sin evidencia se rotulan "estimación".
- **Skills:** `calidad-de-datos-financieros`.

## Caso 7. Anticipar el pago mínimo de las tarjetas
- **Petición:** "¿Puedo pagar solo el mínimo este mes?"
- **Objetivo real:** saber cuánto cuesta y cómo evolucionará el mínimo con las cuotas ya pactadas.
- **Datos mínimos:** monto facturado, parte financiable y no financiable, cuotas sin interés pactadas con su calendario, tasa del rotativo.
- **Pasos:** (1) calcular el mínimo con la fórmula vigente y la etapa de la fecha; (2) proyectar los próximos meses con la reclasificación gradual de cuotas sin interés; (3) comparar con el flujo disponible de cada mes; (4) simular cuántos meses toma y cuánto interés genera pagar solo el mínimo; (5) alertar con anticipación los meses en que el mínimo supera el flujo.
- **Criterio:** pagar el mínimo es un instrumento de liquidez, no de pago.
- **Errores a evitar:** usar el mínimo de un mes como si fuera permanente; suponer que es 5% de todo; no declarar que los hitos intermedios del calendario se dedujeron.
- **Skills:** `pago-minimo-tarjetas`.
