---
name: tasa-maxima-convencional
description: Verifica si el interés pactado de un crédito en Chile excede la Tasa Máxima Convencional (TMC, Ley 18.010) usando una tabla de tasas con fecha de vigencia, y avisa cuando los datos están desactualizados. Úsala cuando pregunten si un interés es legal, usura, tasa máxima o cobros excesivos de intereses.
---

# Tasa Máxima Convencional (TMC)

## Hechos (fuente oficial, consultado 2026-11-26)
- Corresponde a la CMF determinar las tasas de interés corriente y máxima convencional a partir de las tasas cobradas por los bancos, según la Ley 18.010 (https://www.cmfchile.cl/portal/prensa/625/w4-article-102387.html).
- La CMF aprobó una **nueva metodología** de cálculo, vigente desde **febrero de 2026** (misma fuente). Metodología: https://www.cmfchile.cl/portal/estadisticas/617/articles-102391_doc_pdf.pdf
- Se **publica cada mes** en el Diario Oficial, con los promedios del mes anterior (ejemplo: publicación del 15-10-2026 basada en operaciones de septiembre 2026: https://www.diariooficial.interior.gob.cl/publicaciones/2026/10/15/44574/01/2885690.pdf).
- El límite aplica a los **intereses pactados** en operaciones de crédito de dinero o en saldos de precio (https://www.cmfchile.cl/portal/estadisticas/626/articles-111825_recurso_1.pdf).
- La CMF sanciona cobros sobre la TMC (ej.: https://www.cmfchile.cl/portal/prensa/625/articles-111995_doc_pdf.pdf).

## La TMC cambia: nunca la escribas de memoria
Los valores dependen del **tipo de operación** (reajustable o no, plazo, monto en UF) y del **mes**. Esta skill **no trae una tabla vigente**. Procedimiento:
1. Obtén la publicación más reciente (Diario Oficial / CMF) y llena `data/tmc.json` (modelo en `data/tmc.ejemplo.json`, que es un **ejemplo histórico no vigente**). Cada tramo con su fuente y fecha.
2. Ejecuta `scripts/check_tmc.py --datos data/tmc.json --tramo CLAVE --tasa-mensual 0.032`.
3. Si el archivo tiene más de 45 días el script lo avisa: **no concluyas** con datos vencidos.

## Qué certificado usar
- Cada certificado rige **desde su publicación en el Diario Oficial hasta el día anterior a la siguiente**. Para saber si un crédito excedió la TMC, usa el certificado vigente **el día en que se pactó**, no el de hoy.
- Certificados leídos completos (tramo 2.a, no reajustables, 90 días o más, hasta 50 UF; TMC anual lineal): N° 04/2026 (DO 15-04-2026, operaciones de marzo) 40,60%; N° 05/2026 (DO 15-05-2026, operaciones de abril) 41,28%; N° 07/2026 (DO 15-07-2026, operaciones de junio) 41,46%. Son datos históricos para contrastar, no valores vigentes.

## Límites a declarar
- La TMC se compara con la **tasa de interés pactada**, no con la CAE (la CAE incluye gastos y seguros).
- Base de anualización (certificado mensual de la CMF): la TMC en pesos no reajustables se expresa en forma **lineal anual** (tasa mensual × 12); para las demás operaciones se expresa en forma **compuesta** (https://www.cmfchile.cl/portal/estadisticas/626/articles-113468_recurso_1.pdf). Compara en la misma base que el tramo.
- Un exceso sobre la TMC es un **posible** cobro indebido: se reclama ante la institución, el SERNAC o la CMF. Esta skill no determina ilegalidad.
- No incluí los tramos por monto/plazo porque no tengo la tabla vigente verificada.
