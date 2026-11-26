---
name: ahorro-bajo-riesgo
description: Enseña a comparar opciones de ahorro de bajo riesgo en Chile (depósito a plazo en pesos o UF, cuenta de ahorro, fondo mutuo de deuda de corto plazo) por rentabilidad real, riesgo, liquidez, costo e impuesto, sin recomendar productos. Úsala cuando el usuario quiera saber dónde o cómo comparar dónde dejar un ahorro.
---

# Ahorro de bajo riesgo: cómo comparar (Chile)

Orientación informativa, no asesoría de inversión. Consultado 2026-11-26. El agente es un asesor basado en IA y **no recomienda instrumentos, instituciones ni series de fondos**: enseña a comparar. La Ley 21.521 regula la asesoría de inversión profesional y la NCG 502 de la CMF exige transparencia sobre los algoritmos; ver `guardrails-finanzas-chile`. Antes de ahorrar, revisa `fondo-emergencia-y-metas` y la deuda cara (`plan-refinanciamiento`): pagar una tarjeta al 40% rinde más que cualquier depósito.

**Nivel de verificación: N2 a N3.** El texto del DL 824 (arts. 41 bis y 57, BCN vigente al 01-11-2026) y la garantía estatal (CMF Educa) están verificados. Plazos mínimos de los depósitos, estructura de costos de los fondos y la tributación de los fondos mutuos en general vienen de páginas de la CMF y del SII, no de la Ley General de Bancos, la Ley 20.712 ni la circular de la CMF. **No incluyo tasas, rentabilidades ni inflación: tómalas en el momento** (`indicadores-oficiales-chile`).

## El método en 5 preguntas
1. **¿Cuándo necesito la plata?** El plazo decide el instrumento. Si es menos de un año, la prioridad es liquidez y bajo riesgo; si es más, importa la inflación.
2. **¿Cuánto rinde en términos reales?** Compara siempre en poder de compra, no en nominal (ver abajo).
3. **¿Qué riesgo asumo y quién me respalda?** Garantía estatal, solo riesgo del emisor o riesgo de mercado.
4. **¿Qué cuesta entrar, mantener y salir?** Comisiones, plazo de rescate y penalizaciones.
5. **¿Cómo tributa?** El impuesto puede cambiar el orden entre dos opciones con la misma tasa.

## 1. Rentabilidad real
- **Fórmula exacta:** tasa real = (1 + tasa nominal) / (1 + inflación) − 1. Una tasa nominal menor que la inflación pierde poder de compra aunque el saldo suba.
- Un **depósito en UF** ya paga reajuste por inflación más una tasa real pactada: su tasa se compara directamente contra la tasa real de un depósito en pesos. Para pasar uno al otro necesitas **un escenario de inflación**, que es un supuesto tuyo, no un dato.
- El script `scripts/rentabilidad.py` calcula la tasa real, anualiza una tasa de periodo (base 365, compuesta) y convierte entre UF y pesos dado un escenario. Tiene tests.
- Para efectos tributarios, el interés se mide sobre el capital reajustado por la UF (art. 41 bis DL 824, texto leído): lo gravado es el **interés real**, no el nominal.

## 2. Riesgo y respaldo
- **Depósitos a plazo y cuentas de ahorro a plazo en bancos o cooperativas fiscalizadas por la CMF**: la garantía estatal cubre el 100% hasta **200 UF por persona natural y por institución, al año calendario**, y hasta **400 UF** en todo el sistema (CMF Educa; Banco de Chile reproduce los requisitos). Solo para personas naturales, solo depósitos y captaciones a plazo, y se activa cuando la institución entra en liquidación forzosa.
- **Dato obsoleto en circulación:** hay comparadores que dicen "90% hasta 108 UF". Eso no coincide con el 100% hasta 200 UF que informa la CMF: usa la fuente de la CMF.
- **Cuentas a la vista y corrientes**: la CMF las trata aparte de los depósitos a plazo y tienen otro respaldo; no leí el detalle.
- **Fondos mutuos:** no tienen garantía ni rentabilidad asegurada: el valor de la cuota varía y la administradora no puede ofrecer una rentabilidad prefijada, salvo en los estructurados (CMF Educa). Los fondos de deuda de corto plazo también pueden tener rentabilidad negativa en un periodo; la CMF los clasifica por duración (menor o igual a 90 días, a 365 días, mediano y largo plazo, etc.).

## 3. Liquidez
- **Depósito a plazo:** el plazo mínimo es de 7 días en pesos y 90 días en UF, según comparadores de mercado que citan la normativa de la CMF (fuente secundaria). Rescatar antes del vencimiento puede tener castigo de tasa: lee el contrato.
- **Fondo mutuo:** permite el rescate total y permanente de las cuotas, pagado en 10 días o menos (CMF Educa). El plazo exacto está en el reglamento interno de cada fondo.

## 4. Costos
- **Fondos mutuos:** hay remuneración de administración y comisiones de cargo del partícipe (de entrada o salida), que deben considerarse al calcular la rentabilidad (CMF Educa). Los folletos informativos publican la **Tasa Anual de Costos (TAC)**, y la TAC varía mucho entre series (en los folletos que vi, desde 0% hasta más de 4% según la serie). Una TAC alta se come el rendimiento de un instrumento de bajo riesgo: compara la TAC de la serie con la TAC de la industria que el mismo folleto informa.
- **Series:** un mismo fondo tiene series con costos distintos según monto, plazo o canal (CMF Educa): pide la serie que te corresponde y su TAC.
- **Depósitos:** normalmente no cobran comisión, pero confirma costos de renovación automática y de rescate anticipado.

## 5. Impuestos (DL 824 leído; SII)
- Los intereses de depósitos a plazo de una persona natural son rentas del **Global Complementario** (SII). La exención general es el tramo exento del Global (13,5 UTA, art. 52).
- **Exención especial (art. 57):** las rentas del art. 20 N° 2 (capitales mobiliarios; el SII incluye ahí los intereses de depósitos, aunque no leí ese artículo) están exentas del Global si no superan **20 UTM** (UTM de diciembre), siempre que **tus otras rentas sean solo sueldos** (art. 42 N° 1) o de pequeño contribuyente (art. 22). El mayor valor al rescatar cuotas de fondos mutuos también está exento hasta **30 UTM**, para los mismos contribuyentes.
- **Independientes y quienes tienen otras rentas** no entran en esa exención especial: sus intereses suman a la base del Global. Ver `operacion-renta-beneficios` e `independientes-honorarios`.
- La tributación del mayor valor de fondos mutuos en general (art. 17 N° 8 y art. 107) y de los fondos acogidos al art. 42 bis (APV, ver `apv-chile`) no la leí completa: no la afirmes sin revisarla.
- Un comparador que hable de una "retención del 10%" sobre depósitos no está citando texto que yo haya leído: no lo uses sin confirmar.

## Cómo usar esta skill con el usuario
1. Parte por el objetivo y el plazo, no por el producto. Pregunta qué parte del ahorro es fondo de emergencia, qué parte tiene fecha y qué parte es largo plazo.
2. Pide las tasas o rentabilidades que él ya cotizó, y calcula con ellas: tasa real, costo (TAC) y efecto del impuesto.
3. Si el monto supera 200 UF en una misma institución, menciona que la garantía estatal tiene ese tope por institución y año calendario, y deja la decisión al usuario.
4. No digas "conviene X": di "con estas cifras, X rinde más en real, con este riesgo y este costo".
5. Si el usuario pregunta por acciones, ETF, criptoactivos o inversión en el extranjero, esta skill no los cubre: dilo.

## Qué falta verificar
- Ley General de Bancos (garantía estatal, texto) y plazos mínimos de los depósitos en la normativa del Banco Central o de la CMF.
- Tributación general de fondos mutuos (art. 17 N° 8, art. 107, circulares SII) y de los fondos de inversión.
- Cuentas de ahorro a plazo: giros y condiciones.
- Metodología oficial de la TAC (Circular 1.782 de la CMF) y si la rentabilidad publicada de una serie ya está neta de costos.
- Ley Fintec: revisión legal pendiente de si este tipo de comparación cae dentro de la asesoría de inversión.
