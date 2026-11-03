# Integración de la skill 0.3.2

Fecha: 3 de noviembre de 2026.

Esta edición conserva el contenido, el régimen propietario y el estado de piloto
supervisado de 0.3.1. El cambio corrige dos incompatibilidades técnicas sin
atribuir aprobación jurídica ni vigencia normativa.

## Cambios

- `compatibility` se trasladó a `metadata` para ajustarse al frontmatter vigente
  de las skills de Codex.
- `hash_document` deja de rechazar una ruta únicamente porque un ancestro del
  sistema, como `/var` en macOS, sea un enlace simbólico. El archivo solicitado
  debe existir, ser regular, medir entre 1 byte y 25 MiB y no ser él mismo un
  enlace simbólico.
- Se añadió una prueba de regresión que exige rechazar el enlace simbólico final.

## Comprobaciones

Ejecutar desde la raíz:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build.py --output /tmp/milla-build
```

La batería contiene 23 pruebas técnicas. El empaquetado debe producir ZIP,
archivo `.skill`, guía universal y huellas para la versión 0.3.2.

Estas pruebas no certifican corrección jurídica, vigencia de fuentes, anonimato,
aprobación profesional ni instalación permanente en una aplicación de IA.
