# Usar estas skills con Claude, ChatGPT, NanoClaw y otros

El contenido es Markdown plano y los scripts son CLI de Python sin dependencia de ningún asistente. Cómo se conecta cambia según dónde corras el modelo.

| Dónde | Cómo |
|---|---|
| **Claude Code / Agent SDK** | Copia las carpetas de `skills/` a `.claude/skills/` (proyecto) o `~/.claude/skills/`. Carga solo nombre y descripción hasta que son relevantes. |
| **NanoClaw** | Skills en `container/skills/` o en el grupo del agente. **No verifiqué** el mecanismo exacto de selección por grupo; consulta su documentación. Los scripts con secretos (PDF) corren en el host, no en el contenedor. |
| **Claude.ai / ChatGPT / otros chats** | No ejecutan tus scripts locales. Flujo: (1) corre el script en tu equipo, (2) revisa el `.md` enmascarado, (3) súbelo o pégalo, (4) pega el contenido de `guardrails-finanzas-chile/SKILL.md` como instrucciones. No verifiqué si cada chat soporta el formato `SKILL.md`; este flujo no lo necesita. |
| **Modelos locales (Ollama, etc.)** | Mismo flujo. Es la opción donde los datos no salen de tu equipo. |

## Regla común: qué nunca entra al modelo

- La clave de un PDF, contraseñas, tokens, números completos de tarjeta o cuenta.
- Documentos sin revisar después del enmascarado.

## Qué advertir al usuario final

Si construyes un producto sobre esto, muestra el aviso de `lectura-pdf-segura/SKILL.md` antes de la primera carga de un documento, no solo en la documentación.
