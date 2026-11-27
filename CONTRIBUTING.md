# Cómo contribuir

## Reglas de contenido
1. **Fuente primaria primero**: leyes (leychile.cl), Diario Oficial, CMF, SERNAC, Superir, SII, Superintendencia de Pensiones, Banco Central. Foros y blogs solo como referencia y **declarándolo**.
2. **Cada dato normativo** lleva: URL, y fecha de consulta (`YYYY-MM-DD`).
3. **Marca el nivel de verificación**: verificado en fuente oficial / fuente secundaria / no verificado.
4. **No incluyas cifras que cambian** (TMC, UF, UTM, tasas) en el texto. Usa archivos de datos con `vigencia_desde` y `fuente`.
5. **Separa** hechos, estadísticas descriptivas y heurísticas.
6. **Cálculos en código** con pruebas (casos con respuesta conocida), sin dependencias externas.
7. **Nada personal**: ni cuentas, ni montos reales, ni capturas de estados de cuenta, ni nombres.
8. No copies textos largos de las fuentes; resume con tus palabras y enlaza.

## Cambios que se aceptan con prioridad
- Corregir un dato o fuente desactualizada (incluye el diff de la fuente).
- Completar ítems de `PENDIENTES.md`.
- Pruebas para los scripts.

## Antes del pull request
- Ejecuta los scripts con tus casos de prueba y pégalos en la descripción.
- Verifica que ningún archivo contenga datos personales.
- Valida el plugin: `claude plugin validate . --strict` (también corre en CI).
- Si cambias una skill o su description, corre las evals de `evals/` (requiere git 2.31 o superior y consume tu cuota de Claude): `claude plugin eval . --runs 1 --no-publish`. Cada caso de `docs/casos/casos.md` tiene su eval; si agregas un caso, agrega también su carpeta en `evals/`.

## Listado de fuentes
Cada ley, decreto, norma, estudio o referencia que una skill use debe quedar en [`docs/fuentes.md`](docs/fuentes.md) en el mismo commit que lo introduce, con su enlace, su grupo (norma oficial, orientación oficial, estudio o solo referencia) y su estado de lectura (completo, artículos, extracto o no leído). Si una norma es derogada o reemplazada, anótalo ahí y en la skill.
