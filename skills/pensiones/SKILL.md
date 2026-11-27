---
name: pensiones
description: "Explica cómo funciona el sistema de pensiones chileno tras la reforma (Ley 21.735): cotización del empleador y su calendario, Seguro Social, beneficio por años cotizados, Cotización con Rentabilidad Protegida, compensación por expectativa de vida y PGU. Úsala cuando el usuario pregunte por su futura pensión, por la nueva cotización o por la PGU."
---

# Pensiones en Chile tras la Ley 21.735

Orientación informativa, no asesoría previsional ni de inversión. Consultado 2026-11-26. El agente es un asesor basado en IA: explica las reglas y lo que dice la ley, **no proyecta la pensión de una persona** (eso exige datos actuariales y de la AFP) ni recomienda cambiarse de AFP o de fondo. Para el APV y su beneficio tributario, ver `operacion-renta-beneficios` y `ahorro-bajo-riesgo`; para independientes, ver `independientes-honorarios`.

**Nivel de verificación: N3 en lo esencial.** Leí el texto consolidado de la Ley 21.735 en la BCN (publicada el 26-03-2025, con vigencia diferida): arts. 1 a 14, 15 a 23, el transitorio 4 (gradualidad), el 34 (PGU) y el 46. **No leí** los arts. 67 en adelante, que modifican el DL 3.500 (comisiones, licitación de afiliados, inversión, invalidez), ni los reglamentos y normas de la Superintendencia de Pensiones. Los montos de la PGU, el calendario de cotizaciones ya vigentes y la distribución del 3,5% vienen de páginas del IPS, de la Superintendencia de Pensiones y de ChileAtiende, no de la ley.

## Cuánto se cotiza hoy
- **Trabajador dependiente:** su cotización obligatoria de siempre (10% a la cuenta individual más comisión y seguro); la ley no la cambia.
- **Empleador (nuevo, art. 1):** una cotización adicional, **no se descuenta del sueldo**. La Superintendencia de Pensiones informa que entre agosto de 2025 y julio de 2026 fue 1% y que desde las remuneraciones de **agosto de 2026 es 3,5%**.
- **Cómo se reparte el 3,5% (ChileAtiende y Superintendencia):** 0,1% a la cuenta individual, 0,9% a la Cotización con Rentabilidad Protegida y 2,5% al seguro de invalidez y sobrevivencia y a la compensación por expectativa de vida.

## Calendario de la cotización del empleador (transitorio 4)
La ley fija los saltos por meses desde su publicación. El primer salto es el 5.º mes después (agosto de 2025); calculé el mes de cada tramo con esa regla, y coincide con lo que informan la Superintendencia (1% hasta julio de 2026, 3,5% desde agosto de 2026) y la prensa (8,5% en agosto de 2033):

| Desde | Total empleador | A la cuenta individual | CRP | Seguro Social (2,5%) |
|---|---|---|---|---|
| ago 2025 | 1,0% | 0,1% | — | 0,9% |
| ago 2026 | 3,5% | 0,1% | 0,9% | 2,5% |
| ago 2027 | 4,25% | 0,25% | 1,5% | 2,5% |
| ago 2028 | 5,0% | 1,0% | 1,5% | 2,5% |
| ago 2029 | 5,7% | 1,7% | 1,5% | 2,5% |
| ago 2030 | 6,4% | 2,4% | 1,5% | 2,5% |
| ago 2031 | 7,1% | 3,1% | 1,5% | 2,5% |
| ago 2032 | 7,8% | 3,8% | 1,5% | 2,5% |
| ago 2033 | 8,5% | 4,5% | 1,5% | 2,5% |

Los tramos desde agosto de 2026 están leídos en la ley; la distribución de 2025 y 2026 (por tramo) coincide con ChileAtiende. **Ojo:** la ley dice que si la evaluación externa de la Ley 21.713 muestra una recaudación menor a la esperada, y no se compensa con otra fuente, los tramos desde 2029 se reemplazan por otros más bajos (por ejemplo 5,5% en el 53.º mes, 6,0% en el 65.º). No sé si esa evaluación ya se hizo. Después, la cuenta individual llega a 6% en total con aumentos de 0,15 puntos al año, y la CRP baja hasta 0% (art. 1): es un detalle de largo plazo.

La Superintendencia de Pensiones explica que el 7% adicional que menciona se **suma** al aporte del empleador al seguro de invalidez y sobrevivencia. El art. 1 cuenta el 8,5% como total e incluye ese seguro dentro del 2,5%. No resolví esa diferencia de forma de contar; si el usuario necesita la cifra exacta de su empleador, que la pida a su empleador o a la Superintendencia.

## Qué prestaciones crea el Seguro Social (arts. 6 a 14)
Se financia con la CRP y el 2,5% del empleador, y entra en el Fondo Autónomo de Protección Previsional. Quedan sujetos los trabajadores dependientes con contrato vigente o que inicien o reinicien actividades desde el 5.º mes tras la publicación. Tres prestaciones, más el seguro de invalidez y sobrevivencia:

1. **Beneficio por años cotizados (art. 7).** Para quien ya está pensionado por vejez o invalidez en el sistema de AFP, tiene **65 años o más** y sus empleadores enteraron al menos **120 meses (mujeres) o 240 meses (hombres)** al Fondo. Equivale a un máximo de **0,1 UF mensual por cada 12 meses cotizados, hasta 300 meses**; o sea, **2,5 UF mensuales como máximo bruto** (`scripts/pensiones.py`), proporcional a la jornada. **El valor real es ese máximo menos una anualidad** calculada con lo que aportan las cotizaciones del empleador a la cuenta individual (más el valor de la CRP): si la anualidad iguala o supera el máximo, el beneficio es cero. Por eso **no se puede calcular el neto sin datos de la AFP**. Se computan también las cotizaciones de la cuenta individual enteradas antes del primer día del 5.º mes tras la publicación (hasta completar 300 meses) y los bonos de reconocimiento; quedan excluidos los titulares de pensión de retiro de Capredena o Dipreca. Se interrumpe si la persona pasa más de 180 días al año fuera de Chile. Más adelante, el requisito de las mujeres sube gradualmente de 120 a 180 meses, el máximo computable baja y, tras el mes 361, no ingresan nuevos titulares (art. 7; sus fechas parten de la letra a) del art. 8 transitorio, que no leí).
2. **Cotización con Rentabilidad Protegida (art. 8).** El 1,5% (0,9% hoy) se registra como un **bono de seguridad previsional** a nombre del afiliado, en UF, con **garantía del Estado**, intransferible e inembargable, que devenga un interés real anual fijado por la Superintendencia con la tasa de los bonos de Tesorería en UF; se capitaliza mensualmente. Se rescata a la edad legal de pensión, canjeándolo por un bono amortizable. No leí el resto del art. 8 (amortización y endoso).
3. **Compensación por diferencias de expectativa de vida (arts. 9 a 13).** Es **solo para mujeres**, desde los 65 años, si reciben pensión de vejez o invalidez de la cuenta individual (no aplica a quienes están cubiertas por el seguro de invalidez y sobrevivencia, art. 9). Se calcula como la anualidad de su pensión por un factor de corrección que compara su tabla de mortalidad con la de un hombre de igual edad, con **tope de 18 UF de anualidad** y **mínimo de 0,25 UF mensuales**. Pagan 100% si se pensionan a los 65 años; 75% a los 64; 50% a los 63; 25% a los 62; 15% a los 61; 5% a los 60, y nada antes de los 60. Para acceder, la mujer debe haberse incorporado al Seguro Social y tener al menos una cotización en el Fondo antes de cumplir 50 años (art. 13). No incluye el ahorro voluntario ni el APV en el cálculo.

Quienes tienen trabajos pesados pueden acceder a esos beneficios a la edad que resulte de restar a 65 años los años de rebaja de su edad legal (art. 14).

## Pensión Garantizada Universal (PGU)
La ley sube el monto máximo por tramos de edad (transitorio 34): primero a $250.000 para quienes tienen 82 años o más (hacia septiembre de 2025), luego a 75 años o más (septiembre de 2026) y finalmente a todos los beneficiarios (**septiembre de 2027**, mes 30 desde la publicación). Los montos son reajustables; según IPS y la prensa, con el reajuste de IPC de febrero de 2026 el máximo es **$250.275** y rige desde el 1 de septiembre de 2026 para quienes tienen 75 años o más, mientras que los de 65 a 74 años reciben hasta **$231.732**. La pensión base para recibirla debe ser menor a **$1.252.602**, y hasta **$789.139** se recibe el monto máximo vigente (cifras de prensa, 2026). Para 2027 se esperan un reajuste en febrero y el máximo para todos desde septiembre. **Los montos cambian cada año: pídele al usuario que los confirme en el IPS o ChileAtiende**, y no los uses para proyectar.

## Independientes
La obligación de cotizar al Seguro Social para independientes con boleta depende de una ley posterior (transitorio 46), y los arts. 15 a 23 describen una cotización voluntaria: ver `independientes-honorarios`.

## Cómo usarla con el usuario
1. Pregunta si es dependiente, independiente o ambos, su edad y si ya cotiza. Las prestaciones del Seguro Social cuentan los meses en que el empleador cotizó al Fondo, y parten en 2025.
2. Explica qué cambia **para él** y qué es solo del empleador. La cotización nueva no baja su sueldo líquido.
3. Si pregunta "cuánto me va a quedar de pensión": explica que depende de su saldo, su densidad de cotización, la edad y el sexo (por la compensación), y que el beneficio por años cotizados se calcula restando una anualidad. Mándalo al simulador o a la consulta de saldo de su AFP o de la Superintendencia (no verifiqué sus URL).
4. Antes de recomendar APV o ahorro voluntario, remite a `ahorro-bajo-riesgo` y `operacion-renta-beneficios` y a sus tablas de costo de retiro.
5. No recomiendes AFP, fondo ni retiro anticipado: no cubre esta skill.

## Qué falta verificar
- Arts. 67 en adelante de la Ley 21.735 (cambios al DL 3.500: comisiones, licitación de afiliados nuevos, inversión, seguro de invalidez) y su efecto en el costo para el afiliado.
- Resto del art. 8 (amortización del bono, endoso) y el art. 8 transitorio (fechas de los cambios al requisito y al máximo del beneficio por años cotizados).
- Normas de carácter general de la Superintendencia de Pensiones sobre el cálculo de la compensación y del beneficio.
- Si la evaluación externa de la Ley 21.713 activó las tasas alternativas desde 2029.
- Cifras vigentes de la PGU, la pensión base y el simulador oficial (confirmar en IPS y la Superintendencia).
- Ley posterior sobre cotización de independientes y si se ingresó o se publicó.
- Ley Fintec: revisión legal pendiente de si explicar este tipo de prestaciones cae dentro de la asesoría previsional.
