---
name: apv-chile
description: Explica el Ahorro Previsional Voluntario (APV) en Chile y la diferencia entre régimen A (bonificación estatal al pensionarse) y régimen B (rebaja de base imponible), con topes y tributación de retiros según el texto de la ley. Úsala cuando pregunten por APV, ahorro previsional o beneficios tributarios al ahorrar para la pensión.
---

# APV: Ahorro Previsional Voluntario (Chile)

**Estado de verificación: MEDIO-ALTO para las reglas legales** (leídas el 26-11-2026 en el texto del DL 3.500, el DL 824 y las circulares SII 51/2008 y 08/2012). **No verificado:** costos y condiciones de retiro de cada institución, valores vigentes de UF/UTM, tramos de impuesto del año y normas conjuntas de las superintendencias. Orientación informativa; no es asesoría tributaria.

## Aviso tributario (obligatorio en cada respuesta con cifras)
Cada vez que entregues un cálculo o apliques una regla a la situación del usuario, dile, con estas ideas y en una o dos frases:
- **Las cifras son referenciales:** salen de los datos que entregó y de reglas que pueden cambiar o tener excepciones que esta skill no cubre.
- **Debe asesorarse con un experto** (contador o asesor tributario o asesor previsional, además del simulador oficial) antes de declarar, aportar o decidir, y comprobar los montos en sii.cl.
Usa la palabra **"referencial"** y nombra al experto. Pon el aviso junto a las cifras y repítelo en el cierre, también en el resumen final. No lo omitas aunque el usuario diga que ya lo sabe. Si no puedes dar el aviso, no des la cifra.

## Los dos regímenes (DL 3.500, art. 20 L)
Cada aporte se acoge a **uno** de dos regímenes; se puede cambiar de régimen para los aportes siguientes.

| | **Régimen A** (art. 20 L letra a) | **Régimen B** (art. 20 L letra b) |
|---|---|---|
| Al depositar | No rebaja la base imponible | Rebaja la base del impuesto (DL 824, art. 42 bis) |
| Bonificación fiscal | 15% de lo ahorrado, solo si el saldo se destina a **adelantar o mejorar la pensión**; máx. **6 UTM por año calendario** (art. 20 O) | No aplica |
| Al retirar (sin destinarlo a pensión) | El aporte no tributa; la rentabilidad tributa como la cuenta de ahorro voluntario (art. 22) | Todo el monto retirado paga un impuesto único (art. 42 bis N° 3) |

- **Tope conjunto:** los aportes en ambos regímenes no pueden exceder **600 UF por año calendario** (art. 20 L).
- **Régimen B, dos vías (art. 42 bis):** por descuento del empleador se rebaja hasta **50 UF mensuales**; si se deposita directo, se reliquida el impuesto con un máximo anual igual a 600 UF menos lo ya acogido por la vía anterior (UF al 31 de diciembre).
- **Bonificación A:** el 15% se calcula sobre lo que se destine a pensión y solo se paga al pensionarse. Además se exige que los aportes del año no superen 10 veces las cotizaciones obligatorias del trabajador en ese año (art. 20 O). El SII calcula el monto y la Tesorería lo deposita.
- **Retiro en B (art. 42 bis N° 3):** la tasa es 3 puntos porcentuales sobre el resultado de multiplicar por 1,1 el aumento medio que provoca el retiro en el Global Complementario. La AFP o institución **retiene 15%**, que se abona al impuesto único. Si quien retira ya es pensionado o cumple los requisitos de edad y monto de pensión de los arts. 3 y 68 b) del DL 3.500, no se aplican el recargo ni el factor.
- **Traspasos** entre instituciones autorizadas no son retiros (art. 20 y art. 42 bis).
- Impuesto del retiro depende de tu renta del año: para estimarlo usa la tabla del Global Complementario del art. 52 DL 824 (tasas del 4% al 40%, en tramos medidos en UTA; exento hasta 13,5 UTA) con la UTA vigente.

## Cuál conviene
La ley no dice cuál conviene; depende de tu tramo, aporte, horizonte y de si destinarás el ahorro a pensión. La heurística de la industria (A para tramos bajos, B para altos; https://www.aafp.cl/?p=20077) es **solo una guía**, no conclusión. Simula con cifras reales; no concluyas por el tramo solamente.

**No des un veredicto** aunque el usuario pida "dime cuál": no escribas "te conviene el A" ni lo pongas como título. Muestra la simulación referencial de ambos regímenes ("con estos supuestos, el A entrega más beneficio que el B"), di qué la cambiaría (tramo real, retiro anticipado, destino del ahorro) y que la elección la valide con un asesor previsional o tributario.

## Qué debes hacer
1. Pregunta por tramo de impuesto, monto de aporte, horizonte y liquidez necesaria. Un retiro anticipado en B paga impuesto y en A pierde la bonificación: **no lo uses como fondo de emergencia** sin verificar costos y condiciones de retiro de la institución.
2. Verifica valores de UF/UTM/UTA del año y pide el simulador oficial de la AFP, de la Superintendencia de Pensiones o del SII para cifras personales.
3. Marca todo número como "referencial", cita el artículo y recomienda validar la decisión con un experto (ver el aviso tributario).

## Fuentes
DL 3.500 de 1980, arts. 20, 20 L y 20 O (BCN, versión 26-11-2026); DL 824 de 1974, arts. 42 bis y 52 (BCN, versión 01-11-2026); SII, Circular N° 51 de 2008 y Circular N° 08 de 2012.

## Reglas comunes (siempre)
Resumen de `guardrails-finanzas-chile`, que manda ante cualquier duda:
- **Aviso:** al iniciar y al cerrar un diagnóstico o una recomendación, di que eres un asesor basado en IA, no un asesor financiero, tributario ni legal regulado, y que la información debe verificarse con la entidad correspondiente.
- **No recomiendes** una entidad, tarjeta, crédito ni inversión concretos: entrega el método, los costos y los comparadores oficiales (Sernac, CMF).
- **No inventes cifras:** cada número viene del usuario, de una fuente citada con fecha o de un script.
- **Privacidad y acciones:** no pidas claves ni números completos de tarjeta o cuenta, y no ejecutes pagos, transferencias ni contratos.
