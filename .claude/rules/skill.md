---
paths:
  - "skills/**"
---

Cada archivo de la skill debe figurar en `PUBLIC_FILES.json` y la versión en `assets/release.json` debe coincidir con SKILL.md. Nunca incluir datos reales de clientes, ni siquiera en ejemplos o evaluaciones: usar roles genéricos. Correr `python3 -m unittest discover -s tests` y `scripts/build.py` antes del commit.
