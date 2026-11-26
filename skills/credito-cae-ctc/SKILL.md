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
