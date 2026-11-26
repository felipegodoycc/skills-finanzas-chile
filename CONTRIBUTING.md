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

## Fuentes en el README
Cada ley, decreto, norma o estudio que una skill use debe quedar listado en la sección «Fuentes consultadas» del `README.md` (texto completo, o leído solo en los artículos que usa) en el mismo commit que lo introduce. Si una norma es derogada o reemplazada, anótalo ahí y en la skill.
