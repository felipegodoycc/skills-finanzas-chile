<div align="center">

# 🇨🇱 skills-finanzas-chile

**Skills de finanzas personales para Chile, listas para tu agente de IA.**
Basadas en fuentes oficiales (CMF, SERNAC, Superir, leychile.cl). Cada cifra trae fuente y fecha. Los cálculos los hace código, no el modelo.

![Skills](https://img.shields.io/badge/skills-24-2ea44f)
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
npx skills add felipegodoycc/skills-finanzas-chile --list     # ver las 24 skills
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
| `plan-refinanciamiento` | Avalancha vs. bola de nieve, prepago, compra de cartera, consecuencias de impago | Método N1-N2; cálculos con tests; consecuencias de impago N3 (Leyes 21.389, 21.442, 18.101/21.461, 17.322, DFL 4, DFL 382, Código Tributario); hipotecario, contribuciones y TAG sin verificar |
| `cobranza-y-renegociacion` | Derechos del deudor, cobranza, Superir | **N3**: Ley 19.496 art. 37, Ley 21.320, Ley 20.720 arts. 260-268, Compendio de la Superir Libro IV (leído completo, salvo los protocolos de audiencias asincrónicas; reemplazó a la NCG 28), Ley 21.680, NCG 540; historial crediticio según Ley 19.628 arts. 17-19 (versión de 2023) y OFC CMF 1.403; falta confirmar la versión vigente tras la Ley 21.719 |
| `presupuesto-personal` | Presupuesto de régimen y de transición | Método N1: metas son propuestas |
| `analisis-gasto-recurrente` | Suscripciones, gasto hormiga | Método N1: umbral operativo |
| `fondo-emergencia-y-metas` | Colchón y metas por tramos | Seguro de cesantía **N3** (Ley 19.728, Res. Ex. 383); "3 a 6 meses" N1 |
| `apv-chile` | APV régimen A y B | **N3**: DL 3.500, DL 824 y circulares SII; faltan costos de retiro por institución |
| `indicadores-oficiales-chile` | UF, UTM, UTA, IPC y dólar; el usuario elige fuente (CMF, Banco Central, SII sin clave, terceros) | Fuente oficial; lector del SII probado con la página real (UF, UTM, UTA); CMF, Banco Central y mindicador sin prueba real |
| `independientes-honorarios` | Boleta de honorarios: retención, cotización obligatoria, Operación Renta, presupuesto con ingreso variable | **N3**: DL 3.500 (arts. 89 a 92 G) y DL 824 (arts. 50, 52, 74) vigentes leídos, más Ley 21.133 y Ley 21.735 (arts. 15 a 23 y transitorio 46); cifras de 2026 contrastadas con SII y Previsión Social |
| `operacion-renta-beneficios` | Beneficios de la Operación Renta: APV, intereses hipotecarios, crédito por educación, gasto presunto | **N3**: texto consolidado del DL 824 (BCN, vigente al 01-11-2026) leído; sin cifras en pesos; leídos también arts. 43, 65, 68, 69 y 97; faltan reglamentos y circulares |
| `ahorro-bajo-riesgo` | Método para comparar depósitos, cuentas de ahorro y fondos mutuos de deuda: tasa real, riesgo, liquidez, costos e impuestos; no recomienda productos | **N3 en lo esencial**: arts. 41 bis, 57 y 107 del DL 824 y plazos del Compendio del Banco Central leídos; garantía estatal según la Ley General de Bancos (arts. 144 a 153, leídos; cooperativas por la Circular 108 de la CMF); art. 107 N° 3 numeral 3.1 y TAC (informe CMF 2023) leídos; sin tasas ni inflación; falta el texto final del Cap. III.E.1 del Banco Central |
| `pensiones` | Reforma de pensiones (Ley 21.735): cotización del empleador y su calendario, Seguro Social, beneficio por años cotizados, CRP, compensación por expectativa de vida y PGU | **N3 en lo esencial**: arts. 1 a 23 y transitorios 4, 34 y 46 leídos (BCN); cifras de la PGU y cotizaciones vigentes según IPS y Superintendencia de Pensiones; falta el art. 67 en adelante (cambios al DL 3.500) |
| `fraude-medios-de-pago` | Robo, extravío o fraude con tarjetas y transferencias: aviso, reclamo, plazos de restitución | **N3**: texto consolidado de la Ley 20.009 (BCN, versión 30-05-2024) leído completo, más el Decreto exento 473 (umbral 35 UF, 2026) y la NCG 538 de la CMF con sus modificaciones |
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

El listado completo, con enlaces, está en **[docs/fuentes.md](docs/fuentes.md)**. Ahí cada fuente está clasificada según cuánto pesa:

- **Normas oficiales:** leyes, decretos y normas de la CMF, la Superir, el SII y la Superintendencia de Pensiones, con el estado de lectura de cada una (completa, por artículos o no leída).
- **Orientación oficial:** fichas y guías de CMF Educa, SERNAC, ChileAtiende, TGR y SII.
- **Estudios:** Lemus y Pulgar, Madeira (Banco Central) y la Fed de Filadelfia. Describen o sustentan un método, pero no son norma.
- **Solo referencia:** prensa, estudios jurídicos, sitios privados y fuentes oficiales extranjeras (CFPB, MoneyHelper) aplicadas por analogía. Nunca sustentan una cifra por sí solas.

Lo que falta está en [`PENDIENTES.md`](PENDIENTES.md): por ejemplo, costos de retiro del APV por institución, la versión vigente de la Ley 19.628 tras la Ley 21.719, el texto final del Cap. III.E.1 del Banco Central y si el retracto de seguros a distancia alcanza al seguro de desgravamen de un crédito.

## 📄 Licencia

Código y datos: MIT (`LICENSE`). Textos: CC BY 4.0 (`LICENSE-CONTENT.md`).
