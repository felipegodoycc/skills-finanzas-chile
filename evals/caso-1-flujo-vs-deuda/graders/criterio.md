---
type: llm
---
PASS si la respuesta separa el problema de flujo mensual (ingreso menos servicio de deuda menos gasto) del problema de estructura de la deuda, pide los datos mínimos que faltan (saldo, tasa o CAE, cuota y cuotas restantes de cada deuda, gasto real de varios meses, liquidez) y explica que consolidar no sirve si el flujo es negativo.
FAIL si propone consolidar o refinanciar sin revisar antes el flujo, si inventa tasas o saldos que el usuario no dio, o si cuenta un bono o ingreso variable como ingreso base.
