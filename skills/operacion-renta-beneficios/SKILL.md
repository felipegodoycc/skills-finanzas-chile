---
name: operacion-renta-beneficios
description: Explica los beneficios tributarios de la Operación Renta en Chile para personas naturales (APV, intereses hipotecarios, gastos de educación, gasto presunto de honorarios, devolución). Úsala cuando el usuario pregunte qué puede rebajar o recuperar en su declaración de renta.
---

# Operación Renta: beneficios para personas naturales (Chile)

Orientación informativa, no asesoría tributaria. Consultado 2026-11-26. El agente es un asesor basado en IA: la declaración y sus montos son responsabilidad del contribuyente; verifica en sii.cl y, si tu caso es complejo, con un contador.

**Nivel de verificación: N3 para las reglas, sin cifras en pesos.** Leí el texto consolidado del DL 824 (Ley de la Renta) de la BCN, versión vigente al 01-11-2026 (última modificación: Ley 21.850), arts. 42 bis, 47, 50, 52, 54, 55, 55 bis, 55 ter, 56, 74 N° 2 y 84. No leí los artículos de plazos y obligación de declarar (65 a 69), ni el art. 97 (devolución), ni el art. 43 (escala mensual del Impuesto Único de Segunda Categoría), ni circulares del SII. **No incluyo valores de UTA, UF ni UTM de 2026**: cópialos del SII en el momento (ver `indicadores-oficiales-chile`).

## Primero: qué tipo de contribuyente eres
- **Dependiente con un solo empleador:** tu impuesto es el Impuesto Único de Segunda Categoría (art. 43 N° 1), que tu empleador retiene mes a mes. Puedes pedir una reliquidación anual de lo retenido (art. 47) y así usar los beneficios de abajo (arts. 55 bis y 55 ter hablan expresamente de esta reliquidación).
- **Varios empleadores:** estás obligado a reliquidar (art. 47).
- **Honorarios u otras rentas:** pagas Global Complementario (art. 52). Rentas hasta **13,5 UTA** exentas; sobre eso rige una escala progresiva por tramos (4%, 8%, 13,5%, 23%, 30,4%, 35% y 40% sobre los tramos de UTA que fija el art. 52). La retención de la boleta o los PPM son abonos y se devuelve el exceso (ver `independientes-honorarios`).

## Beneficios, con la regla del texto

### 1. APV (art. 42 bis y art. 50)
- **Dependientes (art. 42 bis N° 1 y 2):** se rebaja de la base del impuesto el APV descontado por el empleador (hasta 50 UF por mes) y el depositado directamente hasta un máximo anual de 600 UF menos lo ya rebajado por planilla (UF al 31 de diciembre). Requiere manifestar la voluntad de acogerse al régimen ante la AFP o institución (art. 42 bis N° 4).
- **Independientes (art. 50):** pueden rebajar el APV hasta 600 UF aunque usen el gasto presunto, si cumplen las condiciones de los N° 3 y 4 del art. 42 bis.
- **Costo al retirar:** si el dinero no se usa para mejorar la pensión, el retiro paga un impuesto único con tasa de 3 puntos más que el promedio calculado según la fórmula del N° 3 (la AFP retiene 15% a cuenta). Para los detalles de régimen A y B y de cuándo conviene, usa `apv-chile`: esta skill no lo repite.

### 2. Intereses de crédito hipotecario (art. 55 bis)
- Se rebajan de la renta bruta imponible anual los **intereses efectivamente pagados** en el año de créditos con garantía hipotecaria para adquirir o construir una o más viviendas (o para refinanciarlos).
- **Tope:** el menor entre **8 UTA** y el interés realmente pagado.
- **Según tu renta bruta anual:** menos de 90 UTA, se rebaja todo el interés deducible; sobre 150 UTA, no procede; entre 90 y 150 UTA, el interés deducible se multiplica por (250 − 1,667 × renta en UTA) expresado como porcentaje.
- **Una sola persona por vivienda:** si hay varios deudores, la escritura debe indicar quién se acoge.
- El acreedor informa los intereses al SII; no necesitas adjuntar nada, pero revisa que coincidan con tu certificado anual.
- El script `scripts/beneficios.py` aplica la fórmula (con UTA que tú entregas) y tiene un test. Aviso: a exactamente 150 UTA la fórmula literal da un porcentaje levemente negativo por el redondeo de 1,667, y el script lo corta en 0; el texto no lo aclara.

### 3. Crédito por gastos de educación de los hijos (art. 55 ter)
- **Monto:** 4,4 UF por hijo, con la UF al término del ejercicio. Es un **crédito** (se resta del impuesto), no una rebaja de la base.
- **Qué cubre:** matrícula y colegiatura en instituciones de educación pre escolar, básica, diferencial y media reconocidas por el Estado, cuotas de centro de padres, transporte escolar particular y gastos similares relacionados con la educación.
- **Requisitos:** hijo de hasta 25 años, certificado de matrícula y **85% de asistencia mínima** (salvo impedimento justificado); las rentas anuales **sumadas del padre y la madre** no pueden superar **792 UF**.
- **Limitación:** si el crédito excede el impuesto, el excedente no se imputa a otro impuesto ni se devuelve. Solo se devuelve lo retenido o pagado en exceso.
- El detalle de los requisitos lo fija un reglamento del Ministerio de Educación y una resolución del SII: no los leí.

### 4. Otras rebajas que aparecen en el art. 55 (para quien las tenga)
- Impuesto territorial efectivamente pagado, en la medida que sea deducible (art. 55 letra a); no procede en los casos que el artículo excluye.
- Cotizaciones previsionales de empresarios individuales y socios (letra b), con las condiciones del texto.

### 5. Gasto presunto y cotizaciones de honorarios (art. 50)
- Gasto presunto: 30% de los ingresos brutos anuales, con tope de 15 UTA; con presunto, las cotizaciones no se rebajan. Ver `independientes-honorarios`.

## Devolución o pago
- Impuesto retenido o pagado en exceso: se devuelve por la Tesorería, reajustado según el art. 97 (no leí el plazo exacto; el SII publica el calendario en abril).
- Los montos retenidos y los créditos que se reajustan se actualizan con el IPC hasta noviembre (arts. 54 y 55). Por eso las cifras de tu declaración sugerida no coinciden con las boletas.

## Cómo usar esta skill con el usuario
1. Pregunta qué tipo de contribuyente es y su renta bruta anual del año calendario, porque el beneficio hipotecario depende de eso.
2. Calcula con las cifras que él entregue del SII; no pongas valores de UTA, UF ni UTM de memoria.
3. Dile qué debe comprobar en la declaración sugerida del SII (intereses, APV, certificados de matrícula) en vez de decidir por él.
4. No recomiendes productos de ahorro ni instituciones (ver `guardrails-finanzas-chile`).

## Qué falta verificar
- Obligación de declarar, plazos y fechas de la Operación Renta (arts. 65 a 69 y 97) y la escala mensual del art. 43 N° 1.
- Reglamento del Ministerio de Educación y resolución del SII sobre el crédito de educación.
- Circulares del SII 2025-2026 sobre estos beneficios; lo que hay en el repositorio (Circular 51 de 2008 y 08 de 2012) es del APV.
- Otros créditos y rebajas de la ley (donaciones, rentas de arriendo, ahorro para la vivienda) no están cubiertos aquí.
