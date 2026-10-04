# Instalación y compatibilidad

Consulta técnica: 2026-10-04. Ver fuentes T01–T06 en `skills/milla-asesoria-juridica/assets/fuentes.json`. Verifica la documentación del producto instalado antes de modificar su configuración.

## 1. Lectura universal: la alternativa más sencilla

Genera `MILLA_GUIA_UNIVERSAL.md` o `.txt` con `python3 scripts/build.py --output dist`. Adjunta ese archivo a un chat o proyecto del asunto. Contiene las instrucciones, referencias, plantillas y fuentes; no necesita que la IA abra archivos relativos del repositorio.

Para ChatGPT, Claude en conversación, Gemini en conversación, Grok, DeepSeek o Kimi: esta es una estrategia de lectura, no una instalación nativa certificada. Deben poder procesar el archivo o texto en su contexto. Si existe límite de tamaño, adjunta primero SKILL.md y después sólo las referencias necesarias, indicando qué partes se cargaron. No basta compartir un enlace a una carpeta y asumir que el asistente leyó todos los archivos.

Un proyecto por asunto y un proyecto maestro sin clientes es la organización recomendada. Cuando exista memoria limitada al proyecto, revisa su configuración. Esto ayuda a separar contexto, pero no sustituye autorización, seguridad o control de acceso. Las copias de la guía cargadas en proyectos no se actualizan automáticamente con GitHub. Reemplázalas al adoptar otra versión.

## 2. Claude Code

La documentación consultada admite skills en `.claude/skills/` del proyecto y `~/.claude/skills/` del usuario. Copia la carpeta completa `milla-asesoria-juridica`, no sólo SKILL.md. Si ya existe, compara y respalda antes de sustituirla.

Desde el clon del repositorio, para una instalación nueva en un proyecto:

```sh
mkdir -p .claude/skills
# Ejecutar sólo si el destino no existe; no sobrescribir una versión instalada sin revisión.
cp -R skills/milla-asesoria-juridica .claude/skills/
```

Invocación documentada: `/milla-asesoria-juridica`. Comprueba que la descripción y versión sean las esperadas. No se han ejecutado aquí pruebas dentro de Claude Code ni se garantiza la interfaz de todas sus versiones.

## 3. Codex

La documentación consultada indica `.agents/skills/` para el ámbito del proyecto y `~/.agents/skills/` para el usuario. Copia la carpeta completa en el ámbito deseado, revisa conflictos de nombres y pide explícitamente usar `milla-asesoria-juridica`. No se necesita activar herramientas adicionales para leer el protocolo.

No confundir Codex con las conversaciones ordinarias de ChatGPT: para estas últimas utiliza la guía universal o las funciones de skills que estén disponibles y documentadas en esa cuenta.

## 4. Gemini CLI

La documentación consultada admite `.gemini/skills/` y `.agents/skills/` en el espacio de trabajo, además de ubicaciones de usuario. La copia manual de la carpeta completa permite evitar un instalador remoto. Verifica el resultado con las funciones de listado/recarga de skills documentadas por la versión instalada. No desactives la confirmación de confianza sólo para acelerar la instalación.

Gemini CLI no es la misma interfaz que la aplicación web o móvil Gemini. En estas últimas, el mecanismo universal es la lectura del documento.

## 5. Otros agentes y productos

| Entorno | Mecanismo de esta edición | Estado de verificación |
|---|---|---|
| Agent Skills | SKILL.md, referencias, assets, scripts | Estructura contrastada con especificación |
| Claude Code | Carpeta de skill | Compatibilidad documental; ejecución no probada |
| Codex | Carpeta de skill | Compatibilidad documental; ejecución no probada |
| Gemini CLI | Carpeta de skill | Compatibilidad documental; ejecución no probada |
| ChatGPT Projects | Guía + instrucciones + expediente privado separado | Flujo documental; instalación no realizada en la cuenta |
| Claude/Gemini/Grok/DeepSeek/Kimi en chat | Adjuntar/pegar guía o partes pertinentes | Portabilidad de texto; comportamiento por probar |
| Agente sin navegador | Resumen y borradores con pendientes | No emitir vigencia jurídica como verificada |
| Agente sin escritura o GitHub | Sugerencias y parche para revisión | No afirmar cambios guardados/publicados |

## Desinstalación y actualización

Retira únicamente la copia instalada de la skill, no expedientes ni documentos. Para actualizar, compara CHANGELOG y fuentes, ejecuta pruebas, aprueba la versión y sustituye la copia. Un asunto abierto conserva registro de la versión con la que se emitieron sus documentos; migrarlo exige revisar el impacto.

## Dependencias y permisos

La guía no necesita Python. Los scripts auxiliares y tests requieren Python 3.10+. La plantilla Word requiere `python-docx`. No se incluyen API keys, llamadas a modelos, envío de WhatsApp, servidores MCP, ni permisos para leer todas las carpetas del equipo. Las conexiones externas deben autorizarse por separado.
