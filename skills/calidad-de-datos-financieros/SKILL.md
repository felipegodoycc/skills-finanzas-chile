---
name: calidad-de-datos-financieros
description: Limpia y concilia movimientos bancarios antes de analizarlos - formato genérico, duplicados entre tiempo real y cartola, estados parciales vs. oficiales, reembolsos de tarjetas adicionales y fondos de terceros. Úsala antes de calcular gasto promedio, presupuesto o diagnóstico con datos de movimientos.
---

# Calidad de datos financieros

Si los datos están sucios, todos los totales mienten. Esta skill es método más una herramienta; nunca borra: marca y explica.

## Formato genérico de movimiento
`id, fecha (YYYY-MM-DD), monto (positivo), tipo (gasto|ingreso|traspaso), producto (cuenta/tarjeta enmascarada), fuente (tiempo_real|cartola), comercio, contraparte (opcional)`. Cada adaptador (banco, planilla, base de datos) convierte al formato genérico; los adaptadores personales no se publican.

## Reglas (cada una con su porqué)
1. **Tiempo real vs. cartola.** La línea de la cartola es posterior a la compra en tiempo real (hasta 3 o 4 días, más en fines de semana y feriados). Se enlazan por **mismo monto y producto**, con la compra en tiempo real entre **4 días antes y 2 después** de la línea de cartola (ventana asimétrica) y 1 a 1 con la más cercana: una ventana simétrica de ±4 puede cruzar dos compras iguales. Se conserva la fila de la cartola.
2. **Estado parcial y estado oficial del mismo periodo.** Busca pares (mismo monto y tipo, estados distintos, fechas a menos de 5 días) y marca uno como duplicado. Copiar la categoría específica a la fila que se conserva **no es confiable**: revísala.
3. **Reembolsos de tarjeta adicional.** Si la tarjeta adicional se factura dentro del estado de la titular, sus compras ya están en tu gasto; la transferencia entrante de reembolso debe registrarse como **devolución** (monto negativo del gasto), no como ingreso. Verifica con el total de la tarjeta adicional en el estado y **declara la brecha** (no la fuerces): sin el detalle de las compras anteriores, el neteo es una estimación.
4. **Fondos de terceros.** El depósito de un tercero para una operación conjunta no es ingreso ni gasto: categoría neutra "fondos de terceros".
5. **Traspasos propios.** Entre cuentas tuyas son neutros; un sueldo que cae en una cuenta y pasa a otra se cuenta una sola vez.
6. **Trazabilidad.** Todo cambio con respaldo del valor anterior y la regla aplicada; las cifras sin evidencia se rotulan "estimación".

## Cómo usarla
`scripts/depurar.py --json movimientos.json [--contrapartes "X;Y"]` devuelve duplicados propuestos, reembolsos y los movimientos en tiempo real sin enlazar. Revisa los casos dudosos con tus propios estados antes de aplicar. Funciones para verificar reembolsos: `verificar_reembolso`.

## Errores a evitar
Contar dos veces un pago por planilla; tratar un reembolso como ingreso; borrar filas; dejar que una regla automática revierta una corrección manual (registra las correcciones).

## Caso de ejemplo
`docs/casos/casos.md`, caso 6.

## Aviso obligatorio
Herramienta de apoyo basada en IA. Las marcas son propuestas; no se borra ningún dato.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
