# skills-finanzas-chile

Skills (formato `SKILL.md`) para que un agente de IA converse sobre **finanzas personales en Chile** con base en fuentes oficiales: CMF, SERNAC, Superir, Diario Oficial y leyes en leychile.cl.

> **Esto no es asesoría financiera, tributaria ni legal.** Es material informativo y de apoyo a la decisión. Las cifras normativas cambian; cada dato indica su fuente y fecha de consulta. Si algo está desactualizado o es incorrecto, abre un issue.

## Por qué existe
Al buscar skills de finanzas para agentes, lo disponible está pensado para EE. UU. o para finanzas institucionales (banca de inversión, equity research). No encontré un set adaptado a Chile (CAE/CTC, TMC, indicadores CMF, derechos del deudor, Superir). Una búsqueda no prueba que no exista: si conoces uno, avísame y lo enlazamos.

## Principios de diseño
1. **Fuente y fecha por cada dato.** Nada de cifras "de memoria".
2. **Se distingue** hecho normativo / dato descriptivo / heurística. La mediana de carga financiera no es una meta; el 50% de la CMF es un umbral de alerta, no un nivel sano.
3. **Los cálculos los hace código**, no el modelo (`scripts/`, sin dependencias, probados).
4. **Marcado explícito de lo no verificado.** Mejor decir "no sé, verifica aquí" que rellenar.
5. **Datos que cambian** (TMC, UF, topes) viven en archivos con fecha de vigencia, no en el texto.

## Contenido

| Skill | Qué cubre | Estado de verificación |
|---|---|---|
| `credito-cae-ctc` | CAE, CTC, comparar créditos, consolidación | Alto (fórmula desde borrador de reglamento, ver nota) |
| `prepago-y-portabilidad` | Prepago (Ley 18.010 art. 10), portabilidad (Ley 21.236) | Medio |
| `endeudamiento-cmf` | Carga financiera, apalancamiento, alta carga | Alto |
| `tasa-maxima-convencional` | TMC y verificación de interés pactado | Alto en método; **tabla vigente no incluida** |
| `cobranza-y-renegociacion` | Derechos SERNAC, cobranza extrajudicial, Superir | Medio (varios puntos marcados) |
| `apv-chile` | APV régimen A y B | **Bajo**: falta fuente oficial |
| `guardrails-finanzas-chile` | Reglas de conducta del agente | n/a |
| `lectura-pdf-segura` | PDF (con clave) → Markdown enmascarado, con avisos de privacidad | Probado con 8 pruebas y datos falsos; ver límites en su SKILL.md |

Compatibilidad con Claude, ChatGPT, NanoClaw y otros: [docs/uso-con-otros-asistentes.md](docs/uso-con-otros-asistentes.md).

Nota: la fórmula de CAE de `scripts/cae.py` proviene de un **borrador** de reglamento del Ministerio de Economía; no se verificó si está vigente. La CAE vinculante es siempre la que informa la institución.

## Uso
Copia las carpetas de `skills/` al directorio de skills de tu agente (por ejemplo `.claude/skills/` en Claude Code o el Claude Agent SDK). El formato es el estándar de Agent Skills; otros agentes que leen `SKILL.md` deberían funcionar, pero solo lo probé con la estructura estándar.

```bash
python3 skills/credito-cae-ctc/scripts/cae.py credito --monto-neto 970000 --cuota 52000 --n 24
python3 skills/endeudamiento-cmf/scripts/indicadores.py --ingreso 1500000 --servicio-deuda 300000 --deuda-total 6000000
```

La **política personal** (tus reglas, metas y cifras) no va en este repo: ver `examples/politica-personal.plantilla.md`.

## Licencia
Código y datos: MIT (`LICENSE`). Textos: CC BY 4.0 (`LICENSE-CONTENT.md`).

## Contribuir
Lee `CONTRIBUTING.md`. Regla central: **toda cifra normativa debe traer URL oficial y fecha de verificación**. Los temas pendientes están en `PENDIENTES.md`.
