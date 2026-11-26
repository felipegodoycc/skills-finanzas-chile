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
npx skills add felipegodoycc/skills-finanzas-chile --list     # ver las 18 skills
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

| Skill | Qué cubre | Verificación |
|---|---|---|
| `diagnostico-financiero` | Punto de entrada: objetivos, flujo, carga de deuda y derivación a las demás | Probado |
| `entrada-segura-de-datos` | Cómo entregar datos a la IA según el origen (CSV, PDF, base de datos, automatización) | Probado; SQL no ejecutado |
| `lectura-pdf-segura` | PDF (con clave) → Markdown enmascarado | Probado, datos falsos |
| `calidad-de-datos-financieros` | Duplicados, reembolsos, fondos de terceros | Probado |
| `endeudamiento-cmf` | Carga financiera, apalancamiento, alta carga | Alto |
| `limites-sanos-endeudamiento` | Deuda vs. umbrales por ingreso (Lemus y Pulgar) | Alto en fuente; límites declarados |
| `pago-minimo-tarjetas` | Pago mínimo NCG 537, proyección, costo de pagar solo el mínimo | Verificada contra el texto completo de la NCG 537 |
| `credito-cae-ctc` | CAE, CTC, comparar créditos, consolidación | Alto (ver nota) |
| `tasa-maxima-convencional` | TMC y verificación del interés pactado | Alto en método; tabla vigente no incluida |
| `cotizacion-y-comparacion` | Cómo cotizar y leer rankings: consumo, hipotecario, tarjetas | Medio |
| `prepago-y-portabilidad` | Prepago (Ley 18.010 art. 10), portabilidad (Ley 21.236) | Medio-alto |
| `plan-refinanciamiento` | Avalancha vs. bola de nieve, prepago, compra de cartera | Medio |
| `cobranza-y-renegociacion` | Derechos del deudor, cobranza, Superir | Medio |
| `presupuesto-personal` | Presupuesto de régimen y de transición | Método; metas son propuestas |
| `analisis-gasto-recurrente` | Suscripciones, gasto hormiga | Umbral operativo |
| `fondo-emergencia-y-metas` | Colchón y metas por tramos | Heurísticas declaradas |
| `apv-chile` | APV régimen A y B | Medio-alto: leyes y circulares leídas; faltan costos de retiro |
| `guardrails-finanzas-chile` | Reglas de conducta del agente | n/a |

Casos de ejemplo con cifras ficticias: [docs/casos/casos.md](docs/casos/casos.md).

> La fórmula de CAE de `credito-cae-ctc/scripts/cae.py` viene de un **borrador** de reglamento; no se verificó su vigencia. La CAE vinculante es siempre la que informa la institución.

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
| **NCG 576** (CMF, 14-09-2026), modifica la **NCG 540** | Consentimiento y revocación en el REDEC | contexto (ver `PENDIENTES.md`) |
| **Circular SII N° 51 de 2008** y **Circular SII N° 08 de 2012** | Instrucciones sobre el tratamiento tributario del APV | `apv-chile` |

### Estudios académicos (texto completo)
- Lemus, A. y Pulgar, R. (2021), *Endeudamiento máximo sostenible de los hogares en Chile*, MPRA Paper 106958; publicado en Revista de Análisis Económico (2023). Base de los umbrales de `limites-sanos-endeudamiento`.

### Leyes y normas citadas pero no leídas completas (extracto o fuente secundaria)
- **Ley 19.496** (protección del consumidor, art. 37 y reglamentos) y **Ley 21.320** (cobranza extrajudicial): resumen del Sernac y de estudios jurídicos.
- **Ley 21.521** (Ley Fintec) y **Ley 21.680** (REDEC): consultadas a través de las NCG de la CMF.
- **Ley 20.555** (Sernac Financiero), **Ley 21.673** (origen de la NCG 537) y **Decretos 42, 43 y 44 de 2012** (reglamentos anteriores de información al consumidor): base legal citada, sin lectura del texto.
- **NCG 540 y NCG 567** (REDEC), reglamento de cobranza extrajudicial (consulta pública desde el 09-09-2025) y propuesta de reglamento de crédito de consumo (octubre de 2025): sin texto oficial publicado o leído.
- Fichas y comparadores oficiales: CMF Educa, simulador hipotecario de la CMF, comparadores del Sernac, ChileAtiende y Ventanilla Única Social.

### Pendientes de verificar
Lo que falta está en [`PENDIENTES.md`](PENDIENTES.md): por ejemplo, costos de retiro del APV por institución, el seguro de cesantía, el historial crediticio tras una renegociación y la regla de retracto en seguros asociados a créditos.

## 📄 Licencia

Código y datos: MIT (`LICENSE`). Textos: CC BY 4.0 (`LICENSE-CONTENT.md`).
