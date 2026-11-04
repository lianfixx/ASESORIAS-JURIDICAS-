# Integración de la skill 0.4.0

Fecha: 4 de noviembre de 2026.

Esta edición conserva el contenido, el régimen propietario y el estado de piloto
supervisado de 0.3.2. Añade guía para trabajar en Claude Code sin cambiar el
método jurídico ni atribuir aprobación jurídica o vigencia normativa.

## Cambios

- Nueva referencia `references/claude-code.md`, incluida en el inventario y en
  el paquete. Describe frenos activos, modo plan, reparto en paralelo, `/goal`,
  navegador, seguimiento comercial y mejora continua.
- SKILL.md añade la sección «Terminado y trabajo en Claude Code». No agrega
  campos al frontmatter ni cambia la descripción de 200 caracteres.
- Los frenos activos (hooks) sólo operan en Claude Code dentro de este
  repositorio; no existen en claude.ai, en la guía universal ni en otras IA.

## Comprobaciones

Ejecutar desde la raíz:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build.py --output /tmp/milla-build
```

La batería contiene 23 pruebas técnicas. El empaquetado debe producir un ZIP de
23 archivos, archivo `.skill`, guía universal y huellas para la versión 0.4.0.

Estas pruebas no certifican corrección jurídica, vigencia de fuentes, anonimato,
aprobación profesional, activación en un asistente ni instalación permanente en
una aplicación de IA.
