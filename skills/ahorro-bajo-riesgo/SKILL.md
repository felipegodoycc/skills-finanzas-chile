---
name: ahorro-bajo-riesgo
description: Enseña a comparar opciones de ahorro de bajo riesgo en Chile (depósito a plazo en pesos o UF, cuenta de ahorro, fondo mutuo de deuda de corto plazo) por rentabilidad real, riesgo, liquidez, costo e impuesto, sin recomendar productos. Úsala cuando el usuario quiera saber dónde o cómo comparar dónde dejar un ahorro.
---

# Ahorro de bajo riesgo: cómo comparar (Chile)

Orientación informativa, no asesoría de inversión. Consultado 2026-11-26. El agente es un asesor basado en IA y **no recomienda instrumentos, instituciones ni series de fondos**: enseña a comparar. La Ley 21.521 regula la asesoría de inversión profesional y la NCG 502 de la CMF exige transparencia sobre los algoritmos; ver `guardrails-finanzas-chile`. Antes de ahorrar, revisa `fondo-emergencia-y-metas` y la deuda cara (`plan-refinanciamiento`): pagar una tarjeta al 40% rinde más que cualquier depósito.

**Nivel de verificación: N3 en lo esencial.** Leí el texto del DL 824 (arts. 17, 20 N° 2, 41 bis, 57 y 107 N° 3, BCN vigente al 01-11-2026) y la normativa del Banco Central sobre plazos mínimos de depósitos (Compendio de Normas Financieras, vía su biblioteca). La garantía estatal (arts. 144 a 153 de la Ley General de Bancos), la TAC y la información de los fondos mutuos la verifiqué en páginas de la CMF, no en el texto de la ley ni de la Circular 1.782. **No incluyo tasas, rentabilidades ni inflación: tómalas en el momento** (`indicadores-oficiales-chile`).

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
- **Cuentas a la vista y corrientes**: no entran en esa garantía estatal; según un estudio de la CMF, los depósitos a la vista en bancos tienen una garantía del 100% otorgada por el Banco Central. No leí la norma que lo establece.
- **Fondos mutuos:** no tienen garantía ni rentabilidad asegurada: el valor de la cuota varía y la administradora no puede ofrecer una rentabilidad prefijada, salvo en los estructurados (CMF Educa). Los fondos de deuda de corto plazo también pueden tener rentabilidad negativa en un periodo; la CMF los clasifica por duración (menor o igual a 90 días, a 365 días, mediano y largo plazo, etc.).

## 3. Liquidez
- **Depósito a plazo:** el plazo mínimo de los no reajustables es de **7 días corridos** y el de los reajustables (UF, IVP) es de **90 días corridos**, salvo excepciones del propio Capítulo (Compendio de Normas Financieras del Banco Central; CMF Educa lo confirma). La renovación automática, si se pactó, surte efecto después de tres días hábiles bancarios. Rescatar antes del vencimiento puede tener castigo de tasa: lee el contrato.
- **Fondo mutuo:** permite el rescate total y permanente de las cuotas, pagado en 10 días o menos (CMF Educa). El plazo exacto está en el reglamento interno de cada fondo.

## 4. Costos
- **Fondos mutuos:** hay remuneración de administración y comisiones de cargo del partícipe (de entrada o salida), que deben considerarse al calcular la rentabilidad (CMF Educa). Las administradoras informan la TAC a la CMF según la Circular 1.782 de 2005 (con TAC de remuneración fija, variable, gastos y total) y la CMF publica la TAC por serie en su Portal de Costos; la rentabilidad que muestra el portal de la CMF viene neta de remuneraciones y gastos, pero **las comisiones de colocación o rescate hay que restarlas aparte**. Los folletos informativos publican la **TAC**, y la TAC varía mucho entre series (en los folletos que vi, desde 0% hasta más de 4% según la serie). Una TAC alta se come el rendimiento de un instrumento de bajo riesgo: compara la TAC de la serie con la TAC de la industria que el mismo folleto informa.
- **Series:** un mismo fondo tiene series con costos distintos según monto, plazo o canal (CMF Educa): pide la serie que te corresponde y su TAC.
- **Depósitos:** normalmente no cobran comisión, pero confirma costos de renovación automática y de rescate anticipado.

## 5. Impuestos (DL 824 leído; SII)
- Los intereses de depósitos a plazo de una persona natural son rentas del **Global Complementario** (SII). La exención general es el tramo exento del Global (13,5 UTA, art. 52).
- **Exención especial (art. 57):** las rentas del art. 20 N° 2 (capitales mobiliarios; el art. 20 N° 2 las define como frutos de bienes muebles y el SII incluye ahí los intereses de depósitos) están exentas del Global si no superan **20 UTM** (UTM de diciembre), siempre que **tus otras rentas sean solo sueldos** (art. 42 N° 1) o de pequeño contribuyente (art. 22). El mayor valor al rescatar cuotas de fondos mutuos también está exento hasta **30 UTM**, para los mismos contribuyentes.
- **Independientes y quienes tienen otras rentas** no entran en esa exención especial: sus intereses suman a la base del Global. Ver `operacion-renta-beneficios` e `independientes-honorarios`.
- **Mayor valor al rescatar cuotas de fondos mutuos (art. 107 N° 3, leído):** si el fondo es de la Ley 20.712 y su reglamento destina al menos el 90% de la cartera a valores con presencia bursátil o a instrumentos de deuda de oferta pública del art. 104 (y se cumplen los demás requisitos del artículo), el mayor valor paga un **impuesto único de 10%**; hay una variante para fondos con presencia bursátil. Otros fondos siguen reglas distintas que no leí completas. Lo práctico: pide a la administradora el certificado anual para el SII y revisa en el reglamento interno bajo qué régimen tributa la serie. Los fondos acogidos al art. 42 bis (APV) están en `apv-chile`.
- Un comparador que hable de una "retención del 10%" sobre depósitos no está citando texto que yo haya leído: no lo uses sin confirmar.

## Cómo usar esta skill con el usuario
1. Parte por el objetivo y el plazo, no por el producto. Pregunta qué parte del ahorro es fondo de emergencia, qué parte tiene fecha y qué parte es largo plazo.
2. Pide las tasas o rentabilidades que él ya cotizó, y calcula con ellas: tasa real, costo (TAC) y efecto del impuesto.
3. Si el monto supera 200 UF en una misma institución, menciona que la garantía estatal tiene ese tope por institución y año calendario, y deja la decisión al usuario.
4. No digas "conviene X": di "con estas cifras, X rinde más en real, con este riesgo y este costo".
5. Si el usuario pregunta por acciones, ETF, criptoactivos o inversión en el extranjero, esta skill no los cubre: dilo.

## Qué falta verificar
- Texto de los arts. 144 a 153 de la Ley General de Bancos (la garantía la verifiqué en la CMF y en la normativa que los bancos publican) y de la norma que respalda la garantía del Banco Central a los depósitos a la vista.
- Requisitos completos del art. 107 N° 3 y tributación de los fondos mutuos que no los cumplen; tributación de fondos de inversión.
- Metodología exacta de la TAC y de la rentabilidad neta (Circular 1.782 y documentos metodológicos de la CMF).
- Cuentas de ahorro a plazo: giros y condiciones (Capítulos III.E.1 y III.E.4 del Compendio del Banco Central).
- Ley Fintec: revisión legal pendiente de si este tipo de comparación cae dentro de la asesoría de inversión.
