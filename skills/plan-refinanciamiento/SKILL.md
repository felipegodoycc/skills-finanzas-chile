---
name: plan-refinanciamiento
description: Ordena el pago de varias deudas (avalancha vs. bola de nieve), calcula el ahorro neto de prepagar y evalúa una compra de cartera o consolidación, siguiendo la ruta de la CMF (reducir gasto, consolidar, portar, renegociar, liquidar). Úsala cuando pregunten qué deuda pagar primero, si consolidar, prepagar o renegociar.
---

# Plan de refinanciamiento y orden de pago

## Ruta oficial (nivel: dato oficial; CMF Educa, "La Ruta del endeudamiento")
1 reducir gastos · 2 buscar ingresos extra · 3 **compra de cartera** (pide el certificado de deuda gratuito en "Conoce tu deuda"; la cuota nueva debe ser pagable; compromiso de no volver a endeudarte; puede haber comisión de prepago) · 4 **portabilidad** · 5 renegociación · 6 cerrar productos redundantes · 7 liquidación concursal como último recurso, con guía de la Superir. No fija umbrales numéricos.
- **Renegociación Superir** (ChileAtiende, act. 31-03-2026): gratuita y voluntaria; requiere ≥2 deudas vencidas por más de 90 días corridos que sumen más de 80 UF, no tener actividades de primera categoría en los últimos 24 meses y declarar todas las deudas. Superir actúa como facilitadora.

## Evidencia que guía el método
- **Avalancha** (mayor tasa primero) es la más barata. **Bola de nieve** (menor saldo primero) puede mejorar la motivación, pero la evidencia es mixta: (a) Amar et al. 2011 (*Journal of Marketing Research*, 48) muestran en cuatro experimentos que la gente tiende a pagar primero las deudas pequeñas aunque las grandes tengan mayor tasa ("aversión a la cuenta de deuda"), y que impedirles liquidar por completo las pequeñas y mostrarles el interés acumulado de cada deuda les ayudó a reducir la deuda total más rápido; (b) Kettle, Trudel, Blanchard y Häubl 2016 (*Journal of Consumer Research*, 43(3)), con un estudio de campo y tres experimentos, encuentran que concentrar el pago mensual en una cuenta, en vez de repartirlo, aumenta la motivación para salir de la deuda y lleva a pagar más agresivamente; (c) Gal y McShane 2012 (*Journal of Marketing Research*) analizan registros de una empresa de negociación de deudas: según resúmenes secundarios, cerrar cuentas predice salir de la deuda total (solo leí la referencia, no el resumen del artículo); (d) Brown y Lahey (borrador de trabajo, Texas A&M/NBER) prueban en laboratorio que completar tareas de la más chica a la más grande aumenta la probabilidad de terminarlas. **Ningún estudio que encontré evalúa un "híbrido" como tal.** Lo razonable, y es una inferencia mía, no un resultado de investigación: si las tasas son parecidas, concentra en la deuda más pequeña; si difieren mucho, el costo del interés pesa más y conviene avalancha. Explícaselo así al usuario y deja que elija.
- **Alargar el plazo para bajar la cuota no resolvió el estrés** en un experimento con 40.000 deudores de tarjeta; las rebajas de capital y el alivio de largo plazo sí (Dobbie y Song, NBER 23545).
- La consolidación puede revertirse si se vuelven a usar las tarjetas (evidencia anecdótica de industria).
- Clasificar deudas por **consecuencia del impago** es útil. MoneyHelper (Reino Unido) las separa en emergencias de deuda, **prioritarias** (las de consecuencias más graves, que no tienen por qué ser las más grandes ni las de mayor tasa) y no prioritarias. Esa lista es del Reino Unido y **no se puede copiar a Chile**. Lo que verifiqué para Chile: (1) **pensión de alimentos** (texto de la Ley 21.389, DO 18-11-2021, leído el 26-11-2026: arts. 22, 25, 26, 28, 30, 32 y 33, y art. 14 bis de la Ley 14.908): quien debe al menos tres mensualidades consecutivas o cinco discontinuas se inscribe en el Registro Nacional de Deudores; mientras tanto el proveedor retiene el 50% del crédito (o menos si basta para pagar lo adeudado) en créditos en cuotas de 50 UF o más, excepto rotativos, se retiene la devolución anual de impuestos, no se otorga pasaporte ni licencia de conducir (con excepciones judiciales), y el art. 14 bis de la Ley 14.908 aplica las penas del art. 14 a quien, **con el objeto de menoscabar o controlar la posición económica de la mujer**, incumple reiteradamente (más de 120 días en el Registro), de modo que no es una pena automática por deber alimentos; se sale pagando todo o con un acuerdo aprobado por el tribunal; (2) la **renegociación ante la Superir** exige dos o más deudas vencidas por más de 90 días que superen 80 UF en total, incluye a quienes emiten boletas de honorarios, y la propuesta debe incluir también las deudas al día y las pensiones de alimentos (ChileAtiende, actualizado el 31-03-2026). **No verifiqué** las consecuencias del impago de hipotecario, arriendo, servicios básicos, contribuciones, cotizaciones previsionales, impuestos, gastos comunes ni TAG; no los clasifiques como prioritarios ni no prioritarios sin que el usuario lo consulte con un abogado o la Superir.

## Cómo usarla (`scripts/refinanciar.py`)
1. **Antes de cualquier opción: ¿el flujo mensual es ≥ 0?** Si no, el problema es de flujo (ver `diagnostico-financiero`).
2. **Orden de pago:** `refinanciar.py pago --json deudas.json` con presupuesto mensual y deudas (saldo, tasa mensual, cuota mínima); compara avalancha y nieve en meses e intereses y muestra el orden de cierre.
3. **Prepago:** `refinanciar.py prepago --json ...` → intereses futuros que evitas menos la comisión de prepago. Con pocas cuotas restantes el ahorro es bajo; compáralo con otras deudas o con el colchón. Las condiciones de prepago están en tu contrato.
4. **Compra de cartera:** `refinanciar.py cartera --json ...` compara lo que pagarías hoy con la oferta (cuota, plazo, gastos). Alerta si el plazo se alarga o la cuota no baja. Pide la hoja resumen y compara con `cotizacion-y-comparacion`.
5. **Portabilidad** (Ley 21.236): el nuevo proveedor tramita; el certificado de liquidación es gratis. Los plazos y costos legales deben leerse en la ley (la página de la CMF no los detalla). Ver `prepago-y-portabilidad`.
6. **Renegociación y cobranza:** ver `cobranza-y-renegociacion`.

## Contraste con datos reales (26-11-2026)
- `tasa_implicita` devuelve 0% en compras en cuotas sin interés (cuota × n = capital) y tasas mensuales de 2,8% a 5,1% en 6 planes con interés de dos emisores; el total pagado coincide con cuota × n salvo redondeo (hasta $99).
- En un crédito hipotecario en UF (9 cuotas reales), el interés de cada mes, calculado como cuota menos amortización del saldo, da una tasa mensual casi constante (0,349% a 0,350%): consistente con amortización francesa. La tasa implícita calculada sobre la cuota completa salió algo mayor (0,362%); lo más probable es que la cuota incluya seguros u otros cargos (inferencia, no verificada). Por eso `tasa_implicita` sobre una cuota con seguros sobrestima la tasa del crédito.
- No se comparó con la tasa máxima convencional del mes: requiere el valor publicado por la CMF.

## Errores a evitar
Consolidar con flujo negativo; mirar solo la cuota; ignorar la comisión de prepago; mezclar tasas con bases distintas (usa la tasa implícita mensual); prometer que una opción es "la mejor": muestra el costo numérico de cada una.

## Caso de ejemplo
`docs/casos/casos.md`, casos 1 y 3.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera ni crediticia regulada y no recomienda entidades. Confirma saldos, comisiones y condiciones con cada entidad.
