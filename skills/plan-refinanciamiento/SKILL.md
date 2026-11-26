---
name: plan-refinanciamiento
description: Ordena el pago de varias deudas (avalancha vs. bola de nieve), calcula el ahorro neto de prepagar y evalúa una compra de cartera o consolidación, siguiendo la ruta de la CMF (reducir gasto, consolidar, portar, renegociar, liquidar). Úsala cuando pregunten qué deuda pagar primero, si consolidar, prepagar o renegociar.
---

# Plan de refinanciamiento y orden de pago

## Ruta oficial (nivel: dato oficial; CMF Educa, "La Ruta del endeudamiento")
1 reducir gastos · 2 buscar ingresos extra · 3 **compra de cartera** (pide el certificado de deuda gratuito en "Conoce tu deuda"; la cuota nueva debe ser pagable; compromiso de no volver a endeudarte; puede haber comisión de prepago) · 4 **portabilidad** · 5 renegociación · 6 cerrar productos redundantes · 7 liquidación concursal como último recurso, con guía de la Superir. No fija umbrales numéricos.
- **Renegociación Superir** (ChileAtiende, act. 31-03-2026): gratuita y voluntaria; requiere ≥2 deudas vencidas por más de 90 días corridos que sumen más de 80 UF, no tener actividades de primera categoría en los últimos 24 meses y declarar todas las deudas. Superir actúa como facilitadora.

## Evidencia que guía el método
- **Avalancha** (mayor tasa primero) es la más barata. **Bola de nieve** (menor saldo primero) puede mejorar la adherencia (Amar et al. 2011, aversión a la cuenta de deuda). Un híbrido es común; **no hay fuente académica encontrada**.
- **Alargar el plazo para bajar la cuota no resolvió el estrés** en un experimento con 40.000 deudores de tarjeta; las rebajas de capital y el alivio de largo plazo sí (Dobbie y Song, NBER 23545).
- La consolidación puede revertirse si se vuelven a usar las tarjetas (evidencia anecdótica de industria).
- Clasificar deudas por **consecuencia del impago** (MoneyHelper, UK: de emergencia, prioritarias, no prioritarias) es útil; su adaptación a Chile (vivienda, servicios básicos, crédito con garantía, pensión de alimentos) es inferencia **no sourced**.

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
