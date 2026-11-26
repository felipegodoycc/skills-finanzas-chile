---
name: cotizacion-y-comparacion
description: Cómo cotizar y comparar créditos de consumo, hipotecarios y tarjetas entre entidades en Chile (CAE, CTC, hoja resumen, comparadores oficiales del Sernac y la CMF) y cómo leer rankings sin engañarse. Úsala cuando pregunten qué crédito, tarjeta o banco conviene, cómo cotizar o dónde ver rankings.
---

# Cotizar y comparar productos financieros

## Regla central
Compara **costo total para tu monto y plazo**, no la cuota ni la tasa sola. CAE y CTC solo son comparables con igual monto y plazo (Sernac). No existe un "ranking oficial de mejor banco": esta skill enseña el método y no recomienda entidades.

## Derechos y reglas (norma: Ley 20.555 "Sernac Financiero")
- Las cotizaciones incluyen una **hoja resumen** con los datos clave (monto, plazo, tasa, dividendo con y sin seguros, gastos, CAE y CTC).
- La cotización tiene **vigencia de al menos 7 días hábiles** (Sernac). La tasa queda fija dentro de esa vigencia.
- Tienes derecho a conocer el **CTC** y la **CAE**, y los motivos de un rechazo por escrito.
- Sernac recomienda cotizar en **al menos 3 instituciones**. Puedes buscar tus propios seguros.

## Pasos por producto
**Crédito de consumo.** 1) Explora con el *Comparador de créditos de consumo* del Sernac (monto, cuotas, con o sin desgravamen; entrega cuota, tasa, CAE y CTC; sus comparaciones **no** son una cotización ni obligan a otorgar el crédito). 2) Cotiza formalmente en ≥3 entidades con el mismo monto y plazo. 3) Ejecuta `scripts/comparar.py --json cotizaciones.json --hoy FECHA [--tmc X]`. 4) Verifica la TMC (skill `tasa-maxima-convencional`).
**Hipotecario.** 1) Simulador de Créditos Hipotecarios de la CMF (CMF Educa; compara tasa y dividendo con seguros obligatorios; datos aportados por las entidades; en su lanzamiento cubría mutuos en UF a tasa fija hasta 20.000 UF: confirma el alcance actual). 2) Hoja resumen hipotecaria en ≥3 entidades. 3) Compara también el seguro de desgravamen e incendio (una publicación antigua del Sernac vio diferencias de hasta 182%; verifica). 4) Si ya tienes hipotecario, mide la diferencia de **CTC** sobre el plazo restante, no solo de tasa (ver `prepago-y-portabilidad`).
**Tarjeta de crédito.** Comparador de tarjetas del Sernac (2022; **verifica que siga vigente**): comisión de mantención/administración a un año, costo de una compra de $100.000 en 12 cuotas, avance en efectivo. Compara también tasa del rotativo, condiciones de exención de comisión, cuotas, cupo necesario, y el efecto sobre tu pago mínimo (`pago-minimo-tarjetas`).

## Rankings: cómo leerlos
- **Comparadores oficiales** (Sernac, CMF) sirven para **precio**.
- **Reclamos al Sernac**: normalízalos por clientes; los números absolutos castigan a los bancos grandes (en 2025 los bancos concentraron 67% de los reclamos por Ley de Fraude, pero tienen más clientes).
- **Premios de satisfacción y rankings de blogs**: pueden tener conflicto de interés (el banco difunde su premio o el sitio gana por derivar clientes). Cítalos con nombre, fecha, método y quién los publica; nunca como única base.

## Qué entrega esta skill
Tabla comparativa ordenada por CTC, alertas (cotización vencida, CAE informada que no calza, monto o plazo distintos, CAE sobre TMC) y preguntas para la entidad. Dice "menor CTC bajo estos datos", nunca "el mejor banco".

## Límites
- Días hábiles sin feriados; la vigencia puede variar por feriados.
- La CAE aquí usa la ecuación de flujos con base 12 (misma que `credito-cae-ctc`); la vinculante es la de la hoja resumen.
- Datos de comparadores cambian: anota la fecha de consulta.

## Caso de ejemplo
`docs/casos/casos.md`, casos 2 y 3.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera ni crediticia regulada y no recomienda entidades. Verifica cada condición con la entidad.

## Normativa de información al consumidor (estado al 26-11-2026)
- Tarjetas: Decreto 75 de 2025 (Ministerio de Economía), publicado el 06-08-2026; entra en vigor 18 meses después de su publicación (≈ febrero de 2028) y deroga el Decreto 44 de 2012 desde esa fecha (https://www.diariooficial.interior.gob.cl/publicaciones/2026/08/06/44518/01/2846533.pdf). Hasta entonces rige el Decreto 44. Texto leído completo: la cotización de tarjetas debe tener vigencia de al menos 7 días hábiles (art. 6) y, mientras no rija la fórmula de la NCG 537, el mínimo no puede ser menor a los intereses devengados del período (art. 3° transitorio); el estado de cuenta debe advertir que pagar menos del mínimo genera mora e intereses (art. 23).
- Hipotecarios: Decreto 49 de 2024 (Ministerio de Economía), publicado el 27-02-2026 en el Diario Oficial (https://www.diariooficial.interior.gob.cl/publicaciones/2026/02/27/44387/01/2769135.pdf), aprueba el nuevo reglamento de información al consumidor de créditos hipotecarios y deja sin efecto el Decreto 42 de 2012. Texto leído completo: su artículo único transitorio fija la entrada en vigencia **12 meses después de la publicación** (≈ 27-02-2027), plazo en que los proveedores deben adecuar contratos, cartillas trimestrales, hojas de resumen, cotizaciones y simulaciones. La cotización hipotecaria debe tener vigencia de al menos 7 días hábiles (art. 8). Hasta entonces rige el Decreto 42.
- Retracto (Ley 19.496, art. 3 bis, texto leído): en compras por medios electrónicos o a distancia y en reuniones convocadas por el proveedor puedes terminar el contrato en 10 días; si el precio se pagó con crédito del proveedor o de un tercero asociado, el retracto resuelve el crédito, y los costos del crédito de un tercero quedan a cargo del consumidor. No es un derecho general para créditos de consumo contratados directamente: verifica el caso. Si el proveedor no envió la confirmación escrita (art. 12 A), el plazo sube a 90 días.
- Descuentos atados al medio de pago (Ley 21.398, art. 17 H, texto leído): un proveedor financiero no puede exigir que compres con su propio medio de pago ni ofrecer descuentos exclusivos de su tarjeta condicionados a un crédito en más de una cuota; si ofrece descuentos exclusivos con su medio de pago, debe informar antes el costo total del crédito, y la publicidad debe mostrar el **precio al contado** con tamaño y contraste iguales o mayores que el precio de la promoción.
- Seguros que acompañan un crédito (NCG 460 de la CMF, 13-08-2021, modificada por la NCG 464 de 31-01-2022; texto leído completo): junto con el otorgamiento, renegociación o repactación de un crédito o tarjeta solo se pueden contratar **sin ratificación** seguros cuyo objeto exclusivo sea asegurar el pago de la deuda (desgravamen, invalidez total y permanente de al menos 2/3, y con cobertura total o parcial cesantía, invalidez parcial, incapacidad temporal, hospitalización, paralización) o proteger los bienes en garantía; el beneficiario principal es el acreedor y el seguro de deuda termina cuando se extingue la deuda. **Cualquier otro seguro** ofrecido en el mismo acto debe ser **ratificado por el cliente dentro de 30 días** desde su contratación, de forma expresa e individual por cada seguro; si no se ratifica queda **nulo de pleno derecho**, la prima solo se cobra desde la ratificación, no puede sumarse al monto del crédito y el proveedor no puede rechazar el crédito porque no ratifiques. Para los seguros voluntarios, la norma dice que puedes **retractarte si contrataste por un medio a distancia** y terminarlos anticipadamente en cualquier momento; **el plazo del retracto no figura en la NCG 460**. Vigencia: 60 días desde su emisión.
- Retracto del seguro contratado a distancia (Código de Comercio, art. 538, incorporado por la Ley 20.667; lo contrasté el 26-11-2026 en dos transcripciones del texto y en la ficha divulgativa de la CMF, sin acceso directo al PDF del Diario Oficial): puedes retractarte **dentro de 10 días contados desde que recibes la póliza**, sin expresar causa ni pagar cargo, y te devuelven la prima pagada. No procede si ya ocurrió un siniestro ni en contratos cuyos efectos terminen antes de esos 10 días. Se considera "a distancia" el seguro convenido por cualquier sistema de transmisión y registro digital o electrónico de la palabra escrita o verbal (incluye el teléfono). Dos límites: (1) ese texto no trae una excepción para seguros asociados a créditos, pero una presentación de la CMF de la consulta de la NCG 460 propuso no permitir retracto en los seguros que cubren riesgos propios del endeudamiento; no confirmé qué quedó en la norma final, así que no afirmes que el retracto aplica al seguro de desgravamen sin consultarlo con la aseguradora o la CMF; (2) el plazo corre desde la póliza, no desde que aceptaste por teléfono: pídela por escrito y anota la fecha de recepción.
- Seguros asociados al crédito (Ley 20.448, art. 8, texto leído): si el proveedor exige un seguro, no puede condicionar el crédito ni ofrecer condiciones distintas a quien contrate los seguros que él ofrece o intermedia; el deudor puede contratar la póliza con cualquier entidad. El proveedor sí puede exigir una cobertura mínima, que la aseguradora tenga clasificación de riesgo al menos igual a la de la ofrecida por él y ser designado beneficiario. Úsalo para cotizar el seguro por separado.
- Consumo: el nuevo reglamento es una propuesta de octubre de 2025 (https://pac.economia.gob.cl/wp-content/uploads/2025/10/Propuesta-Nuevo-Reglamento-Credito-de-Consumo.pdf); no confirmé su publicación, así que se asume vigente el Decreto 43 de 2012.
- Comparadores del Sernac: crédito de consumo actualizado en octubre de 2025 (https://eldesconcierto.cl/2025/10/06/sernac-lanza-nuevo-comparador-de-creditos-de-consumo-filtra-por-monto-cuotas-y-seguros-con-datos-actualizados); tarjetas lanzado en 2022 (vigencia actual no confirmada).
