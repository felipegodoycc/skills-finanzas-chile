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
- Tarjetas: Decreto 75 de 2025 (Ministerio de Economía), publicado el 06-08-2026; entra en vigor 18 meses después de su publicación (≈ febrero de 2028) y deroga el Decreto 44 de 2012 desde esa fecha (https://www.diariooficial.interior.gob.cl/publicaciones/2026/08/06/44518/01/2846533.pdf). Hasta entonces rige el Decreto 44.
- Hipotecarios: nuevo reglamento publicado el 27-02-2026 (https://www.carey.cl/api/archivo/ministerio-de-economia-publica-nuevo-reglamento-sobre-informacion-al-consumidor-de-creditos-hipotecarios?lang=es); **vigencia no verificada**.
- Consumo: el nuevo reglamento es una propuesta de octubre de 2025 (https://pac.economia.gob.cl/wp-content/uploads/2025/10/Propuesta-Nuevo-Reglamento-Credito-de-Consumo.pdf); no confirmé su publicación, así que se asume vigente el Decreto 43 de 2012.
- Comparadores del Sernac: crédito de consumo actualizado en octubre de 2025 (https://eldesconcierto.cl/2025/10/06/sernac-lanza-nuevo-comparador-de-creditos-de-consumo-filtra-por-monto-cuotas-y-seguros-con-datos-actualizados); tarjetas lanzado en 2022 (vigencia actual no confirmada).
