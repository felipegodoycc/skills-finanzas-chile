<div align="center">

# 🇨🇱 skills-finanzas-chile

**Skills de finanzas personales para Chile, listas para tu agente de IA.**
Basadas en fuentes oficiales (CMF, SERNAC, Superir, leychile.cl). Cada cifra trae fuente y fecha. Los cálculos los hace código, no el modelo.

![Skills](https://img.shields.io/badge/skills-18-2ea44f)
![Licencia código](https://img.shields.io/badge/código-MIT-blue)
![Licencia textos](https://img.shields.io/badge/textos-CC%20BY%204.0-lightgrey)
![Python](https://img.shields.io/badge/python-3.9%2B%20stdlib-3776AB)
![Hecho con Claude](https://img.shields.io/badge/construido%20con-Claude-d97757)

</div>

> **Aviso.** Esto no es asesoría financiera, tributaria ni legal. El agente que use estas skills es un **asesor basado en IA**: debe decirlo y recomendar verificar con la entidad correspondiente. No recomienda bancos, tarjetas, créditos ni inversiones concretas (ver la nota sobre la Ley Fintec en `guardrails-finanzas-chile`). Las cifras normativas cambian; cada dato indica su fuente y fecha de consulta. Si algo está desactualizado o es incorrecto, abre un issue.

## ⚡ Instalación

**Con `npx` (cualquier agente compatible con Agent Skills):**

```bash
npx skills add felipegodoycc/skills-finanzas-chile            # elige interactivamente
npx skills add felipegodoycc/skills-finanzas-chile --list     # ver las 20 skills
npx skills add felipegodoycc/skills-finanzas-chile --skill diagnostico-financiero
```

**Como plugin de Claude Code:**

```
/plugin marketplace add felipegodoycc/skills-finanzas-chile
/plugin install skills-finanzas-chile --marketplace felipegodoycc/skills-finanzas-chile
```

**A mano:** copia las carpetas de `skills/` a `.claude/skills/` (proyecto) o `~/.claude/skills/` (global).

> Los comandos de arriba funcionan cuando el repositorio esté publicado. Para probar desde una copia local: `npx skills add ./ --list`. Otros asistentes (ChatGPT, NanoClaw, modelos locales): [docs/uso-con-otros-asistentes.md](docs/uso-con-otros-asistentes.md).

## 🧭 La necesidad

Endeudarse en Chile es fácil y entenderlo es difícil: CAE y CTC, tasa máxima convencional, pago mínimo de tarjetas, portabilidad, cobranza, renegociación. La información está dispersa entre normas de la CMF, leyes, el SERNAC y notas de prensa que a veces se contradicen entre sí.

Las skills de finanzas para agentes que encontré apuntan a EE. UU. o a finanzas institucionales. Ninguna hablaba de CMF, Superir ni de la nueva fórmula del pago mínimo. Y un modelo de lenguaje, solo, tiende a decir cifras "de memoria" con mucha seguridad.

Este repo busca lo contrario: que el agente **cite la fuente, calcule con código, distinga norma de heurística y diga "no sé, verifica aquí"** cuando corresponde. Y que quien lo use pueda entregarle sus datos de forma segura (ver `entrada-segura-de-datos`).

## 🤝 Construido en conjunto

Este proyecto lo construimos **Felipe y Claude** trabajando juntos, a partir de un problema real: ordenar las finanzas personales de Felipe con un agente asesor conectado a sus propios datos.

- Felipe puso el problema, las preguntas incómodas y la exigencia de no inventar nada.
- Claude investigó, contrastó fuentes, escribió las skills, los scripts y las pruebas.
- Los **casos de ejemplo** (`docs/casos/casos.md`) nacieron de conversaciones reales y están anonimizados: cifras ficticias, solo se conserva el método.
- Varias correcciones salieron de cuestionar lo que Claude afirmaba, y quedaron documentadas en `PENDIENTES.md`.

## 🧱 Principios de diseño

1. **Fuente y fecha por cada dato.** Nada de cifras de memoria.
2. **Se distingue** hecho normativo / dato descriptivo / heurística. La mediana de carga financiera no es una meta; el 50% de la CMF es un umbral de alerta, no un nivel sano.
3. **Los cálculos los hace código** (`scripts/`, solo librería estándar, con pruebas).
4. **Lo no verificado se marca.** Mejor "no sé, verifica aquí" que rellenar.
5. **Los datos que cambian** (TMC, UF, topes) viven en archivos con fecha de vigencia, no en el texto.
6. **Tus datos, tu control.** Enmascarado local antes de que algo llegue al modelo; rol de solo lectura para bases de datos.

## 📚 Qué incluye

### Escala de verificación
Cada skill declara qué tan verificada está. Los niveles se miden contra fuentes y tests, no por opinión:

| Nivel | Criterio |
|---|---|
| **N1** | Sin fuente: heurística o propuesta, declarada como tal |
| **N2** | Fuente secundaria o estudio citado, sin leer el texto oficial |
| **N3** | Texto oficial leído completo (artículo y fecha citados); el código tiene tests |
| **N4** | N3 más revisión independiente (abogado, CMF o un segundo lector). *Ninguna skill llega aquí todavía.* |

El tipo importa: una **norma** sube con el texto oficial; un **método** se sustenta con evidencia citada y casos de prueba, y no pasa de N2 salvo que descanse en un estudio leído completo; el **código** sube con tests y datos reales.

| Skill | Qué cubre | Verificación |
|---|---|---|
| `diagnostico-financiero` | Punto de entrada: objetivos, flujo, carga de deuda y derivación a las demás | Código con tests (datos sintéticos); método N1 |
| `entrada-segura-de-datos` | Cómo entregar datos a la IA según el origen (CSV, PDF, base de datos, automatización) | Normas N3 (Ley 21.719/21.855, NCG 569); código con tests; SQL **no ejecutado** |
| `lectura-pdf-segura` | PDF (con clave) → Markdown enmascarado | Código con tests (datos falsos); sin probar con PDFs reales |
| `calidad-de-datos-financieros` | Duplicados, reembolsos, fondos de terceros | Código con tests (datos sintéticos) |
| `endeudamiento-cmf` | Carga financiera, apalancamiento, alta carga | N2: definiciones por contrastar con el Informe de Endeudamiento de la CMF |
| `limites-sanos-endeudamiento` | Deuda vs. umbrales por ingreso (Lemus y Pulgar) | N3 sobre el estudio (Lemus y Pulgar, MPRA 106958); es un estudio, no una norma |
| `pago-minimo-tarjetas` | Pago mínimo NCG 537, proyección, costo de pagar solo el mínimo | **N3**: NCG 537 leída completa |
| `credito-cae-ctc` | CAE, CTC, comparar créditos, consolidación, CAE de tarjetas | Crédito de consumo: método N2; CAE y CAEP de tarjetas: **N3** (Decreto 75, fórmulas transcritas del PDF, con tests) |
| `tasa-maxima-convencional` | TMC y verificación del interés pactado | Método N2; tabla vigente no incluida |
| `cotizacion-y-comparacion` | Cómo cotizar y leer rankings: consumo, hipotecario, tarjetas | **N3 parcial**: Decretos 75 y 49, Ley 20.448 art. 8, Ley 19.496 art. 3 bis; reglamento de consumo sin publicar |
| `prepago-y-portabilidad` | Prepago (Ley 18.010 art. 10), portabilidad (Ley 21.236) | **N3**: Ley 18.010 art. 10, Ley 21.236, Decreto 1.154 |
| `plan-refinanciamiento` | Avalancha vs. bola de nieve, prepago, compra de cartera | Método N1-N2; cálculos con tests |
| `cobranza-y-renegociacion` | Derechos del deudor, cobranza, Superir | **N3**: Ley 19.496 art. 37, Ley 21.320, Ley 20.720 arts. 260-268, NCG 28, Ley 21.680, NCG 540; falta el historial crediticio |
| `presupuesto-personal` | Presupuesto de régimen y de transición | Método N1: metas son propuestas |
| `analisis-gasto-recurrente` | Suscripciones, gasto hormiga | Método N1: umbral operativo |
| `fondo-emergencia-y-metas` | Colchón y metas por tramos | Seguro de cesantía **N3** (Ley 19.728, Res. Ex. 383); "3 a 6 meses" N1 |
| `apv-chile` | APV régimen A y B | **N3**: DL 3.500, DL 824 y circulares SII; faltan costos de retiro por institución |
| `indicadores-oficiales-chile` | UF, UTM, UTA, IPC y dólar; el usuario elige fuente (CMF, Banco Central, SII sin clave, terceros) | Fuente oficial; lector del SII probado con la página real (UF, UTM, UTA); CMF, Banco Central y mindicador sin prueba real |
| `fraude-medios-de-pago` | Robo, extravío o fraude con tarjetas y transferencias: aviso, reclamo, plazos de restitución | **N3**: texto consolidado de la Ley 20.009 (BCN, versión 30-05-2024) leído completo; falta la NCG 538 y el decreto de 2026 del umbral |
| `guardrails-finanzas-chile` | Reglas de conducta del agente | n/a |

Casos de ejemplo con cifras ficticias: [docs/casos/casos.md](docs/casos/casos.md).

> La fórmula de CAE de `credito-cae-ctc/scripts/cae.py` (créditos de consumo) viene de un **borrador** de reglamento; no se verificó su vigencia. La CAE vinculante es siempre la que informa la institución.

## 🚀 Prueba rápida

```bash
python3 skills/limites-sanos-endeudamiento/scripts/limites.py --ingreso 1800000 --servicio-deuda 600000
python3 skills/pago-minimo-tarjetas/scripts/pago_minimo.py calcular --cargos 60000 --cuotas-sin-interes 200000 --otros 600000 --fecha 2026-12-20
python3 skills/credito-cae-ctc/scripts/cae.py credito --monto-neto 970000 --cuota 52000 --n 24
python3 skills/endeudamiento-cmf/scripts/indicadores.py --ingreso 1500000 --servicio-deuda 300000 --deuda-total 6000000
```

Tu **política personal** (reglas, metas, cifras) no va en este repo: usa `examples/politica-personal.plantilla.md`.

## 🔐 Privacidad

Nunca subas claves de PDF, contraseñas, tokens ni números completos de tarjeta o cuenta. Enmascara primero y revisa el resultado. Detalle en `skills/entrada-segura-de-datos/SKILL.md`.

## 🛠️ Contribuir

Lee `CONTRIBUTING.md`. Regla central: **toda cifra normativa debe traer URL oficial y fecha de verificación**. Lo pendiente está en `PENDIENTES.md`. Las pruebas corren en CI con cada push.

## 📖 Fuentes consultadas

Cada cifra normativa de las skills trae su URL y fecha. Aquí está el listado completo. **Texto completo** = el documento oficial se leyó íntegro (26-11-2026); **extracto** = solo se consultó el resumen oficial o una fuente secundaria, y la skill lo marca como no verificado.

### Leyes, decretos ley y decretos (texto completo)
| Norma | Para qué se usa | Skill |
|---|---|---|
| **Ley 18.010** (operaciones de crédito de dinero), art. 10, versión con Ley 21.398 | Prepago, comisión y umbral de consentimiento del 10% | `prepago-y-portabilidad` |
| **Ley 21.236** (portabilidad financiera, DO 09-06-2020) | Plazos, retracto, costos y sanciones de la portabilidad | `prepago-y-portabilidad` |
| **Ley 20.720** (insolvencia y reemprendimiento), arts. 2, 260-268, con Ley 21.563 | Renegociación de la persona deudora ante la Superir | `cobranza-y-renegociacion`, `plan-refinanciamiento` |
| **Ley 19.496** (protección del consumidor), arts. 3 bis y 37, y **Ley 21.320** (cobranza extrajudicial) | Retracto, tope de gastos de cobranza, límites a la cobranza | `cobranza-y-renegociacion`, `cotizacion-y-comparacion` |
| **Ley 21.398** (Pro Consumidor, DO 24-12-2021), arts. 3 bis, 17 A, 17 D, 17 H y 17 N de la Ley 19.496 | Término de contratos y suscripciones, retracto, bloqueo de tarjetas, certificados para renegociar, descuentos con medio de pago propio, análisis de solvencia | `analisis-gasto-recurrente`, `cobranza-y-renegociacion`, `cotizacion-y-comparacion` |
| **DFL 3 de 2021** (texto refundido de la Ley 19.496, leído) y **Ley 19.728** (seguro de cesantía, arts. 12, 15, 24 y 25, tablas leídas) | Informe de contratos financieros (art. 17 B), art. 17 D, retiro de la cuenta individual y Fondo Solidario | `cobranza-y-renegociacion`, `analisis-gasto-recurrente`, `fondo-emergencia-y-metas` |
| **Ley 21.680** (Registro de Deuda Consolidada) | Consentimiento, límite de 5 años y derechos en el REDEC | `cobranza-y-renegociacion` |
| **Ley 19.728** (seguro de desempleo) | Cotizaciones, cuenta individual y Fondo Solidario | `fondo-emergencia-y-metas` |
| **Decreto 1.154 de 2020** (reglamento de portabilidad financiera) | Oferta, arrepentimiento y certificados | `prepago-y-portabilidad` |
| **Ley 20.448** (integración del mercado de capitales), art. 8 | Seguros asociados a créditos | `cotizacion-y-comparacion` |
| **Ley 21.719** (protección de datos personales) y **Ley 21.855** (fija su vigencia el 15-10-2027) | Tratamiento de datos | `entrada-segura-de-datos` |
| **DL 3.500 de 1980**, arts. 20, 20 L y 20 O | Regímenes del APV y bonificación | `apv-chile` |
| **DL 824 de 1974** (Ley de la Renta), arts. 42 bis y 52 | Rebaja de base, impuesto al retiro del APV, tabla del Global Complementario | `apv-chile` |
| **Decreto 75 de 2025** (Economía, DO 06-08-2026), reglamento de información al consumidor de tarjetas | CAE de tarjetas, cotización, estado de cuenta | `cotizacion-y-comparacion`, `credito-cae-ctc` |
| **Decreto 49 de 2024** (Economía, DO 27-02-2026), reglamento de créditos hipotecarios | Cotización, cartillas y vigencia (12 meses) | `cotizacion-y-comparacion` |

### Normas de la CMF y circulares del SII (texto completo)
| Norma | Para qué se usa | Skill |
|---|---|---|
| **NCG 537** (CMF), pago mínimo de tarjetas, con calendario de gradualidad | Fórmula del monto mínimo a facturar | `pago-minimo-tarjetas` |
| **NCG 569** (CMF, 01-06-2026), modifica la **NCG 514** | Plazos del Sistema de Finanzas Abiertas | `entrada-segura-de-datos` |
| **NCG 540** (CMF, 14-07-2025) y **NCG 576** (CMF, 14-09-2026) | Funcionamiento del REDEC, consentimiento y revocación | `cobranza-y-renegociacion` |
| **Ley 20.009** (Leyes 21.234, DO 29-05-2020, y 21.673, DO 30-05-2024) y **Decreto 435 de Hacienda** (DO 17-12-2024) | Limitación de responsabilidad por fraude con medios de pago, plazos de restitución y umbral de 35 UF | `fraude-medios-de-pago` |
| **NCG 460** (CMF, 13-08-2021; mod. NCG 464) | Seguros que se pueden contratar con un crédito, ratificación a 30 días y retracto a distancia | `cotizacion-y-comparacion` |
| **Código de Comercio, arts. 538 y 538 bis** (Ley 20.667 y Ley 21.314) | Retracto de 10 días del seguro contratado a distancia (N3: texto oficial de la Ley 20.667 leído) y ratificación de seguros asociados a créditos | `cotizacion-y-comparacion` |
| **Certificados de interés corriente y máximo convencional N° 05/2026 y 07/2026** (CMF, Diario Oficial 15-05-2026 y 15-07-2026) | Verificación de la TMC por fecha | `tasa-maxima-convencional` |
| **NCG 28 de la Superir** (Res. Ex. 22802, 19-11-2025) | Requisitos y documentos de la renegociación | `cobranza-y-renegociacion` |
| **Res. Ex. 383 de la Superintendencia de Pensiones** (DO 17-03-2026), valores del Fondo de Cesantía Solidario (leída completa; con dos erratas del texto marcadas en la skill) | Montos vigentes hasta 28-02-2027 | `fondo-emergencia-y-metas` |
| Informe normativo de la CMF sobre la modificación de la NCG 514 (junio de 2026) | Fecha de publicación de la NCG 514 (julio de 2024) | `entrada-segura-de-datos` |
| **Circular SII N° 51 de 2008** y **Circular SII N° 08 de 2012** | Instrucciones sobre el tratamiento tributario del APV | `apv-chile` |

### Estudios académicos (texto completo)
- Lemus, A. y Pulgar, R. (2021), *Endeudamiento máximo sostenible de los hogares en Chile*, MPRA Paper 106958; publicado en Revista de Análisis Económico (2023). Base de los umbrales de `limites-sanos-endeudamiento`.

### Leyes y normas citadas pero no leídas completas (extracto o fuente secundaria)
- **Ley 21.521** (Ley Fintec): arts. 2, 3 y 5 y la NCG 502 de la CMF leídos (26-11-2026); lo que sigue pendiente es la revisión legal, no la lectura.
- **Ley 20.555** (Sernac Financiero), **Ley 21.673** (origen de la NCG 537) y **Decretos 42, 43 y 44 de 2012** (reglamentos anteriores de información al consumidor): base legal citada, sin lectura del texto.
- Reglamento de cobranza extrajudicial (consulta pública desde el 09-09-2025) y propuesta de reglamento de crédito de consumo (octubre de 2025): sin texto oficial publicado o leído.
- Fichas y comparadores oficiales: CMF Educa, simulador hipotecario de la CMF, comparadores del Sernac, ChileAtiende y Ventanilla Única Social.

### Pendientes de verificar
Lo que falta está en [`PENDIENTES.md`](PENDIENTES.md): por ejemplo, costos de retiro del APV por institución, el historial crediticio tras una renegociación (Superir) y si el retracto de seguros a distancia alcanza al seguro de desgravamen de un crédito (el art. 538 no lo excluye; el informe normativo de la NCG 460 no lo trata).

## 📄 Licencia

Código y datos: MIT (`LICENSE`). Textos: CC BY 4.0 (`LICENSE-CONTENT.md`).
