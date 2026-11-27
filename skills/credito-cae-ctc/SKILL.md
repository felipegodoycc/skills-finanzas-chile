---
name: credito-cae-ctc
description: Compara y evalúa créditos de consumo en Chile usando CAE (Carga Anual Equivalente) y CTC (Costo Total del Crédito); calcula CAE desde monto recibido y cuota, estima saldo para prepago y compara un crédito que reemplaza deudas. Úsala cuando pregunten por costo real de un crédito, cotizaciones, consolidar deudas o refinanciar en Chile.
---

# Crédito: CAE y CTC (Chile)

## Qué son (fuente oficial)
- **CAE**: indicador porcentual del costo de un crédito en un período anual, que permite comparar ofertas. Incorpora todos los cobros, no solo la tasa. SERNAC: https://www.sernac.cl/618/w3-propertyvalue-27768.html
- **CTC**: monto total que terminará pagando el consumidor, la suma de todas las cuotas incluyendo costos adicionales. SERNAC: https://sernac.cl/portal/619/w3-article-7302.html
- **Base legal**: Ley 20.555 ("SERNAC Financiero"), que modificó la Ley 19.496. El consumidor tiene derecho a conocer CTC y CAE al contratar. https://www.sernac.cl/portal/607/w3-propertyvalue-28422.html
- La CAE incluye capital, tasa, plazo, gastos propios del crédito y productos voluntariamente contratados, según el *borrador* de reglamento del Ministerio de Economía (https://pac.economia.gob.cl/wp-content/uploads/2025/10/Propuesta-Nuevo-Reglamento-Credito-de-Consumo.pdf, consultado 2026-11-26).

## Estado del borrador (no lo presentes como norma vigente)
Ese documento es un **proyecto de decreto**; su artículo transitorio fija vigencia al 31-07-2026, pero **no verifiqué si fue publicado ni si está en vigor**. Su fórmula (CAE = i_f × f, con i_f la tasa que iguala valor presente de lo recibido y lo pagado) es la que implementa `scripts/cae.py`. El borrador no fija f, ni convención de días, ni redondeo.

## Procedimiento
1. Pide los datos **del contrato o cotización**: monto efectivamente recibido (neto de gastos retenidos), valor de la cuota total, número de cuotas, pagos iniciales, y la CAE y CTC informados.
2. Ejecuta `scripts/cae.py credito --monto-neto X --cuota Y --n N [--pago-inicial Z]`. No calcules la CAE "a mano" con el LLM.
3. Contrasta con la CAE que informa la institución. Si difieren de forma relevante, reporta la diferencia y pide la hoja resumen; no asumas error de ninguno.
4. Para comparar ofertas, usa mismo monto y mismo plazo: un CTC o CAE más bajo significa ahorro (SERNAC: https://www.sernac.cl/portal/618/w3-propertyvalue-66843.html).
5. Para consolidación de deudas: `scripts/cae.py reemplazo --json archivo.json`. Compara la tasa mensual ponderada de lo que se paga hoy con la tasa periódica del nuevo crédito.

## Límites que debes declarar
- La CAE **vinculante** es la informada por la institución. Esta skill compara, no certifica.
- La tasa efectiva anual `(1+i)^12-1` y la CAE nominal `i×12` son bases distintas: nunca las compares entre sí.
- Un crédito de menor CAE **no es automáticamente mejor**: puede alargar el plazo (más CTC), exigir seguros, o no calzar con tu liquidez. Cuantifica el efecto antes de recomendar.
- El saldo de `saldo` incluye seguros/cargos de la cuota, por lo que **sobreestima el capital**. El prepago real lo da el certificado de prepago de la institución (ver `prepago-y-portabilidad`).
- Esto no es asesoría financiera licenciada: presenta opciones con costo numérico y deja la decisión a la persona.

## Dato útil con fuente
SERNAC publicó un estudio donde el CTC de $2.000.000 a 36 meses fluctuaba entre $2.501.928 y $3.547.512 según la institución (https://sernac.cl/portal/619/w3-article-7302.html; fecha del estudio no visible en el extracto, verifícala antes de citarlo como actual). Conclusión robusta: **cotizar en más de una institución importa**.

## CAE de tarjetas de crédito (Decreto 75 de 2025, leído completo el 26-11-2026)
- Es otro reglamento (información al consumidor de **tarjetas**): publicado el 06-08-2026, vigente 18 meses después (≈ 07-02-2028). Hasta entonces rige el Decreto 44 de 2012.
- Ecuación general: la CAE es la tasa que iguala el valor presente de los pagos (amortización, intereses, gastos y productos voluntarios) con el del capital recibido o adeudado.
- Para rotativo, compra en cuotas y avance en efectivo, la CAE de referencia usa un capital fijo de **20 UF**, **M = 12** pagos futuros, sin meses de gracia, y reparte en partes iguales las comisiones que no son de la operación. También define la CAE de prepago (CAEP).
- **Fórmulas (transcritas de las imágenes del PDF, 26-11-2026):** CAE rotativo y compra en cuotas: `CAE = (1+i)^12 − 1`, con `20 UF = Σ Rm (1+i)^−m`. **Avance en efectivo: `CAE = i × 12` (nominal, no compuesta)**, con la misma ecuación. CAEP: `Qt = Σ Rm (1+i)^(t−m−1)` y `CAEP = i × f`. El PDF repite en el apartado b) la imagen del rotativo, así que la de cuotas se asume idéntica.
- `scripts/cae_tarjetas.py` las implementa (`rotativo`, `cuotas`, `avance`, `caep`) con tests. El decreto fija la ecuación, no el flujo: con `--tasa-mensual` el script construye 12 cuotas iguales más cargos mensuales iguales (**construcción nuestra, referencial**); con `--flujos` usas los 12 pagos reales del emisor. El índice m parte en 0 en el PDF: aquí R0 es opcional y vale 0. La definición de f del CAEP no está en el texto leído (por defecto 12). El valor de la UF sale de `indicadores-oficiales-chile`.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
