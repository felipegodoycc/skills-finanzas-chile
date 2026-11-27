---
name: fondo-emergencia-y-metas
description: Dimensiona el colchón de emergencia (meses de gastos esenciales cubiertos), fija metas por tramos y calcula en cuánto tiempo se alcanzan, y alinea los objetivos del usuario (comprar algo, ahorrar, salir de deuda) con la evidencia disponible. Úsala cuando pregunten cuánto ahorrar, cuánto fondo de emergencia necesitan o si pueden hacer una compra grande.
---

# Colchón de emergencia y metas

## Qué dicen las fuentes (todas heurísticas; ninguna es norma)
- **CMF:** menciona el fondo de emergencia como una posible meta, **sin dar monto ni meses**.
- **"3 a 6 meses"** es una convención; no hay evidencia oficial chilena. JPMorgan Chase Institute (EE.UU., datos bancarios) sugiere ~6 semanas de ingreso neto para volatilidad típica, y más con ingreso volátil. **Aplicabilidad a Chile no verificada.**
- **Seguro de Cesantía (Ley 19.728, texto leído, versión 01-06-2026):** contrato indefinido cotiza 0,6% el trabajador y 2,4% el empleador (a plazo fijo u obra: 3% el empleador; casa particular: 3% el empleador). De eso, el 0,6% del trabajador más 1,6% del empleador (2,8% en plazo fijo) van a tu **Cuenta Individual por Cesantía** y el 0,8% del empleador (0,2% en plazo fijo) al **Fondo de Cesantía Solidario** (arts. 5, 9 y 23). Las cotizaciones a la cuenta se enteran hasta 11 años por relación laboral. Requisitos para retirar de la cuenta: contrato terminado por las causales de los arts. 159, 160, 161 y 163 bis del Código del Trabajo, 10 cotizaciones (indefinido) o 5 (plazo fijo) y estar cesante (art. 12). El Fondo Solidario exige 10 cotizaciones en los últimos 24 meses, las tres últimas continuas con el mismo empleador, causales de los n.° 4, 5 y 6 del art. 159 o de los arts. 161 y 163 bis, y saldo de la cuenta insuficiente; máximo 10 pagos en cinco años (art. 24). **Montos del Fondo Solidario vigentes (art. 25):** Resolución Exenta N° 383 de la Superintendencia de Pensiones (6-03-2026, DO 17-03-2026; reemplaza a la N° 290; PDF completo leído el 26-11-2026), con valores hasta el 28-02-2027. Contrato indefinido, % del promedio de las remuneraciones de los últimos 10 meses, con valor superior / inferior: mes 1: 70% ($1.004.003 / $301.201); mes 2: 60% ($860.574 / $258.171); mes 3: 45% ($645.429 / $193.629); mes 4: 40% ($573.718 / $172.115); mes 5: 35% ($502.002 / $150.602). Plazo fijo u obra: mes 1: 60% ($860.574 / $258.161); mes 2: 40% ($573.718 / $172.115); mes 3: 35% ($502.002 / $150.602); meses 4 y 5: 30% ($430.288 / $129.085). Giros por alto desempleo (meses 6 y 7): 30% ($430.288 / $129.085). Dos reparos del texto: el valor inferior del mes 1 a plazo fijo ($258.161) difiere en un dígito del del mes 2 indefinido ($258.171), y es probable que sea una errata; y la tabla del art. 70 (prestaciones mejoradas por catástrofe o alerta sanitaria) dice que rige "hasta el 28 de febrero de 2026", fecha anterior a la propia resolución, así que se trata de una errata de año que no resuelvo: no uses la tabla del art. 70 sin confirmarla con la Superintendencia. Los valores se reajustan cada marzo: reconfirma. **Retiro de la Cuenta Individual (art. 15; tabla leída en el PDF de la ley, 26-11-2026):** si el contrato termina por los n.° 4, 5 y 6 del art. 159 o el art. 161 del Código del Trabajo, giras cada mes, mientras alcance el saldo, el 70%, 60%, 45%, 40%, 35% y desde el sexto mes el 30% del promedio de las remuneraciones de los últimos 10 meses con cotizaciones (indefinido o casa particular) o de los últimos 5 (plazo fijo u obra). El último giro puede ser menor y corresponde al saldo; si es igual o inferior al 20% del giro anterior, se pagan juntos. Se paga mes vencido desde el día siguiente al término del contrato. Los porcentajes del Fondo Solidario (art. 25: 70/60/45/40/35% en indefinido; 60/40/35/30/30% en plazo fijo) coinciden con los de esta skill; además hay un sexto y un séptimo giro de 30% si la tasa nacional de desempleo del INE supera en 1 punto el promedio de los 4 años anteriores. Los topes en pesos de la ley se reajustan cada 1 de marzo (IPC y, si es positiva, remuneraciones reales). No reemplaza el colchón de emergencia.
- **Datos descriptivos (CAF-CMF 2023, autorreporte):** solo 38% cubriría un gasto inesperado equivalente a un mes de ingreso sin pedir créditos ni ayuda a familiares o amigos; 25% de la población se siente sobreendeudada; 42% declara que su ingreso alcanza para cubrir sus gastos (informe CAF-CMF, Chile 2023, resumen ejecutivo y secciones 6.2 y 6.4; comunicado CMF del 14-12-2023, https://www.cmfchile.cl/portal/estadisticas/626/articles-76205_doc_pdf.pdf).
- **Ahorro:** Save More Tomorrow (Thaler y Benartzi, 2004) funciona comprometiendo parte de los aumentos futuros (evidencia fuerte en jubilación de EE.UU.; en Chile es extrapolación, p. ej. APV). Fernandes et al. (2014): la educación sola cambia poco la conducta; automatiza.

## Método
1. **Gastos esenciales mensuales** = lo que no puedes dejar de pagar en un mes (vivienda, servicios, alimentación, salud, transporte, deudas obligatorias). Pídelos con datos.
2. **Liquidez real**: separa lo líquido (cuenta, fondo conservador con rescate de 1 a 3 días) de lo no líquido (renta variable, plazos largos, rescate con comisión o pérdida). Solo lo líquido es colchón.
3. `scripts/colchon.py --json datos.json` → meses cubiertos, metas (piso, 1 mes, 3 y 6 meses; 6 y 9 si el ingreso es variable; la referencia de 6 semanas de EE.UU.) y meses para alcanzarlas con tu aporte y con cuotas que se liberan.
4. **Orden:** piso de colchón → deuda más cara → completar meta. Con una deuda a >30% anual, el interés que evitas suele pesar más que el rendimiento del colchón; pero no te quedes sin piso.
5. **Compras grandes:** convierte el deseo en condiciones medibles (deuda cara en cero, flujo ≥ 0 por N meses, colchón sobre el piso después de comprar). Calcula el costo si se financia con `cotizacion-y-comparacion`.
6. **Objetivos del usuario:** pregunta para qué ahorra y para cuándo (corto, mediano, largo plazo, como en CMF Educa) y asigna instrumento por plazo, liquidez y riesgo, sin recomendar productos concretos.

## Errores a evitar
Contar como colchón dinero con riesgo de pérdida; usar una meta de meses como norma; fijar un piso sin explicar de dónde sale; ignorar la volatilidad del ingreso.

## Caso de ejemplo
`docs/casos/casos.md`, casos 2 y 3.

## Aviso obligatorio
Herramienta de apoyo basada en IA; no es asesoría financiera ni de inversión. Las metas de meses son heurísticas.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
