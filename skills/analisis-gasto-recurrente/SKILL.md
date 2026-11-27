---
name: analisis-gasto-recurrente
description: Detecta suscripciones, cobros recurrentes y gasto pequeño frecuente (gasto hormiga) en movimientos bancarios y propone eliminar, reemplazar o controlar cada uno. Úsala cuando pregunten en qué se les va la plata, cómo recortar suscripciones o gastos hormiga.
---

# Gastos recurrentes, suscripciones y gasto hormiga

## Qué dicen las fuentes
- **CMF (vía prensa y su directora de Estudios):** el gasto hormiga es no planificado y fuera del presupuesto fijo; su efecto acumulativo puede contribuir al sobreendeudamiento. Es **cualitativo, sin monto**. CMF Educa ofrece una calculadora y advierte que algunos pueden volverse fijos.
- **Evidencia:** el "latte factor" (David Bach) no tiene respaldo en estudios revisados por pares; los críticos señalan vivienda, transporte y deuda como las palancas grandes. La desatención en suscripciones sí está documentada: Einav, Klopack y Mahoney (NBER 31547) estiman que eleva los ingresos de las empresas (de 14% a más de 200% según el producto).
- **No hay definición oficial de monto.** Los umbrales de este repositorio son **definiciones operativas**, declaradas en la salida.

## Cómo usarla
1. Movimientos (CSV: `fecha,monto,comercio`) de 3 a 6 meses, limpios (`calidad-de-datos-financieros`).
2. `scripts/recurrentes.py --csv mov.csv [--umbral-hormiga 10000] [--frecuencia-minima 4]`
   - **Recurrente:** ≥3 cobros del mismo comercio, intervalo mediano de 26 a 35 días y monto estable (±10%).
   - **Hormiga:** monto mediano ≤ umbral y ≥4 compras al mes.
   - Con menos de 12 meses no ve cobros anuales: pregunta por ellos.
3. Para cada ítem pregunta: *¿lo usaste en los últimos 30 días?* y propone **eliminar**, **reemplazar** (alternativa más barata) o **controlar** (tope semanal, pago con débito).
4. Compara el ahorro posible con las palancas grandes; si estas pesan más, parte por ellas.

## Principios
- Sin moralizar: un gusto planificado no es una fuga.
- Prioriza por **gasto anual**, no por monto de cada cobro.
- Un cobro que sube sin aviso o un cargo desconocido: revisa con el comercio y, si no corresponde, con el banco; el consumidor puede terminar un contrato y el silencio no es aceptación (regla general de consumo; la regla precisa para suscripciones genéricas **no fue verificada**).
- Las suscripciones digitales se pueden pausar; anota la fecha de renovación.

## Cómo cancelar una suscripción (Ley 21.398, texto leído completo el 26-11-2026)
La Ley 21.398 modificó la Ley 19.496 (del consumidor). Para contratos de adhesión (los de "aceptar términos y condiciones", como la mayoría de las suscripciones):
- **Art. 17 A:** al contratar, el proveedor debe informar los mecanismos y condiciones para ponerle término. No puede condicionar el término al pago de montos adeudados ni a la devolución de bienes, ni imponer condiciones más gravosas que las exigidas para contratar; todo pacto en contrario se tiene por no escrito. Si no informó el mecanismo, solo quedas obligado a lo que se te informó al aceptar. Hay una excepción para el monto de término anticipado de productos financieros (art. 17 D).
- **Art. 3 bis (retracto):** en contratos por medios electrónicos o a distancia puedes retractarte sin expresión de causa, **pero en servicios el proveedor puede excluir el retracto si te lo informó de forma inequívoca, destacada y accesible antes de contratar y pagar**. Para ejercerlo puedes usar los mismos medios con que contrataste. El plazo corre desde la contratación (servicios) o la recepción (bienes) si el proveedor envió la confirmación escrita del art. 12 A; si no, es de 90 días.
- La Ley 21.398 y el texto refundido de la Ley 19.496 (DFL 3 de 2021, leído) **no contienen una regla específica sobre renovación automática** de suscripciones digitales. Solo en contratos de servicios financieros el art. 17 B exige informar la duración del contrato o si es indefinido o renovable automáticamente, las causales de término por voluntad del consumidor y los costos de término anticipado. La herramienta "Me quiero salir" del Sernac cubre telecomunicaciones y seguros generales, según su sitio (fuente secundaria).
- Si no te dejan cancelar, guarda pruebas, reclama al proveedor y luego al Sernac. El Sernac ha actuado por barreras para cancelar suscripciones: ofició a La Tercera y a El Mercurio tras reclamos de que el portal no ofrecía la opción de cancelar en línea, y publicó un hallazgo de que muchos sitios usan técnicas que dificultan cancelar (manipulación digital). Eso muestra el problema y que el Sernac lo está fiscalizando, no que exista una regla específica sobre renovación automática.

## Caso de ejemplo
`docs/casos/casos.md`, caso 5.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera. El umbral de "hormiga" es una definición operativa.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
