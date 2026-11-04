# Auditoría y mejoras · 4 de noviembre de 2026

Repositorio `lianfixx/ASESORIAS-JURIDICAS-`. Agente: Claude Code (sesión en la nube); solicitante: Emi. Base auditada:
`043fd59` (main antes de los cambios del 4/11). Este documento registra con precisión qué cambió, por qué
y cómo se verificó; se complementa con `CHANGELOG.md` (o el registro propio del proyecto).

## Resumen

Skill `milla-asesoria-juridica`: 0.3.2 → **0.4.1** (dos publicaciones el 4/11: mejoras del video y registro entre IA). El método no cambió.

Se añadió la **capa común entre IA** (`ia/`), idéntica en los 14 repositorios de lianfixx:
`ia/PROTOCOLO.md` 1.0.0 (generaliza el protocolo de Mes), `ia/REGLAS.md` (generadas de
`ia/politica.json`), los frenos (`ia/guard.py`), los hooks de git (`ia/githooks/`, que se activan con
`sh ia/instalar.sh`), el workflow `.github/workflows/registro-ia.yml`, `GEMINI.md`, las
instrucciones para Proyectos de ChatGPT o Gems de Gemini (`ia/INSTRUCCIONES_PROYECTO.md`) y las
plantillas de petición y entrega entre IA.

## Reglas de este repositorio

7 reglas que bloquean, 4 que piden confirmación de Emi y 3 controles previos a commit
o push. La lista legible está en `ia/REGLAS.md`; los casos de prueba, en `ia/politica.json` → `tests`.
Registro válido para la regla «todo cambio se documenta»: `^CHANGELOG\.md$`.

## Del video a este repositorio

| Del video (Fran Salazar, «Lo que Claude Code puede hacer…», 3/11/2026) | Aplicación |
|---|---|
| CLAUDE.md y sus tres preguntas | `CLAUDE.md` breve que importa `AGENTS.md`; el detalle vive en la skill y sus referencias. |
| `.claude/rules/` por tipo de archivo | Reglas con `paths:` donde hay archivos con invariantes propias. |
| Hooks: lo que debe cumplirse sí o sí | `ia/guard.py` + `ia/politica.json`, aplicados por Claude Code, por hooks de git y por GitHub Actions. |
| Modo plan y entrevista | Solo en arranques nuevos o ambiguos, según cada skill (ver su `references/claude-code.md`). |
| ultrathink | Cada skill marca los pasos que piden máxima profundidad. |
| Agentes en paralelo, `/goal`, `/loop`, `claude -p` | Criterio de terminado verificable en SKILL.md; reparto, `/goal` y `/loop` en `references/claude-code.md`; INDEP y DOF traen `scripts/headless.sh`, sin activar. |
| Navegador (Chrome / Playwright) | Indicado por skill, nunca para eludir accesos ni enviar sin autorización. |
| `/rewind`, `/btw`, `!`, `/context`, `/compact`, `/voice`, `/remote-control` | Hábitos de sesión: solo como atajos breves en la referencia, no en el cuerpo de la skill. |

## Archivos cambiados desde la base

- `.agents/skills/milla-asesoria-juridica/SKILL.md` — añadido
- `.claude/rules/skill.md` — añadido
- `.claude/settings.json` — añadido
- `.claude/skills/milla-asesoria-juridica/SKILL.md` — añadido
- `.github/CODEOWNERS` — añadido
- `.github/workflows/registro-ia.yml` — añadido
- `.github/workflows/validar.yml` — modificado
- `AGENTS.md` — modificado
- `CHANGELOG.md` — modificado
- `CLAUDE.md` — añadido
- `GEMINI.md` — añadido
- `PUBLIC_FILES.json` — modificado
- `README.md` — modificado
- `SECURITY.md` — modificado
- `docs/INSTALACION.md` — modificado
- `docs/INTEGRACION_0.4.0.md` — añadido
- `ia/.gitignore` — añadido
- `ia/INSTRUCCIONES_PROYECTO.md` — añadido
- `ia/PROTOCOLO.md` — añadido
- `ia/REGLAS.md` — añadido
- `ia/check_skill.py` — añadido
- `ia/githooks/pre-commit` — añadido
- `ia/githooks/pre-push` — añadido
- `ia/guard.py` — añadido
- `ia/instalar.sh` — añadido
- `ia/plantillas/ENTREGA.md` — añadido
- `ia/plantillas/PETICION.md` — añadido
- `ia/politica.json` — añadido
- `ia/test_guard.py` — añadido
- `ia/verificar.py` — añadido
- `skills/milla-asesoria-juridica/NOTICE` — modificado
- `skills/milla-asesoria-juridica/SKILL.md` — modificado
- `skills/milla-asesoria-juridica/assets/configuracion.ejemplo.json` — modificado
- `skills/milla-asesoria-juridica/assets/estado.ejemplo.json` — modificado
- `skills/milla-asesoria-juridica/assets/evaluaciones.json` — modificado
- `skills/milla-asesoria-juridica/assets/release.json` — modificado
- `skills/milla-asesoria-juridica/references/claude-code.md` — añadido
- `tests/test_integracion.py` — modificado

## Verificación

| Comando | Resultado | Detalle |
|---|---|---|
| `python3 ia/test_guard.py` | aprobado | Ran 32 tests in 7.641s · OK |
| `python3 ia/verificar.py reglas --check` | aprobado |  |
| `python3 ia/check_skill.py skills/milla-asesoria-juridica` | aprobado | SKILL.md compatible: skills/milla-asesoria-juridica |
| `python3 -m unittest discover -s tests` | aprobado | OK |
| `python3 scripts/build.py --output <temporal>` | aprobado | /tmp/tmp.bXM8qBGzh2/SHA256SUMS.txt |

## Límites y pendientes

- Los frenos de Claude Code solo actúan en Claude Code dentro de este repositorio. Los hooks de git
  requieren `sh ia/instalar.sh` en cada copia. GitHub Actions marca un push sin registro, pero no lo
  revierte ni lo impide: para impedirlo hace falta protección de rama con el check obligatorio, que
  se configura en GitHub y no se activó aquí.
- En chat (claude.ai, ChatGPT o Gemini) no hay freno automático: la IA debe cumplir `ia/REGLAS.md` y
  entregar un «Registro pendiente».
- No se verificó la subida real de skills a claude.ai ni a ChatGPT, ni el descubrimiento de
  `.agents/skills/` por cada versión de Codex o de `GEMINI.md` por Gemini CLI.
- Los nombres de conectores (Gmail, Drive) cambian según la instalación; comprobarlos con `/mcp`
  antes de programar ejecuciones.
