# Historial público

## 2026-11-04 · corrección: flag de push mal formado

- Agente: Claude Code (sesión en la nube)
- Solicitud: autocorrección de Claude Code al revisar su propio comando (4/11/2026).
- Cambios: la regla que prohíbe forzar el push no atrapaba flags cortos mal formados que contienen `f` o `d` (por ejemplo `-f-never`); el patrón ahora es `-(?!-)\S*[fd]\S*`. Se añadió el caso a las pruebas. Ese push concreto (rama de mes.) fue de avance lineal y no borró historial.
- Archivos: `ia/politica.json`, `ia/REGLAS.md`, `ia/INSTRUCCIONES_PROYECTO.md` y este registro.
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py inicio` → aprobado.
- Pendiente: ninguno.

## 2026-11-04 · frenos de git también para Codex, ChatGPT y Gemini

- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 4/11/2026: que los frenos de git funcionen también con Codex y ChatGPT, no solo con Claude.
- Cambios: `python3 ia/verificar.py inicio`, que `AGENTS.md` pide ejecutar a cualquier IA al empezar, ahora también activa los hooks de git si faltan (antes solo lo hacía el hook de Claude Code). Así Codex, ChatGPT con terminal y Gemini CLI quedan con los mismos frenos de commit y push. `AGENTS.md` e `ia/INSTRUCCIONES_PROYECTO.md` lo indican.
- Archivos: `ia/verificar.py`, `ia/test_guard.py`, `ia/INSTRUCCIONES_PROYECTO.md`, `AGENTS.md` y este registro.
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py inicio` → aprobado.
- Pendiente: ninguno.

## 2026-11-04 · arranque común entre IA (protocolo 1.1.0)

- Agente: Claude Code (sesión en la nube)
- Solicitud: Emi, 4/11/2026: «haz lo que tengas que hacer para que entiendas» las reglas al trabajar.
- Cambios: `python3 ia/verificar.py inicio` resume al empezar rama, último commit y su IA, reglas, registro vigente y hooks de git; en Claude Code corre solo con un hook `SessionStart` y activa los hooks de git si faltan. `ia/PROTOCOLO.md` pasa a 1.1.0; `AGENTS.md`, `GEMINI.md` e `ia/INSTRUCCIONES_PROYECTO.md` indican el comando a las demás IA.
- Archivos: `.claude/settings.json`, `ia/verificar.py`, `ia/test_guard.py`, `ia/PROTOCOLO.md`, `ia/INSTRUCCIONES_PROYECTO.md`, `AGENTS.md`, `GEMINI.md` y este registro.
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py inicio` → aprobado.
- Pendiente: ninguno.

## 2026-11-04 · 0.4.1 · registro obligatorio y trabajo entre IA

- Agente: Claude Code (sesión en la nube; modelo según la sesión)
- Solicitud: Emi, 4/11/2026: auditar y documentar las mejoras, hacerlas funcionar igual con ChatGPT, Gemini u otra IA, y documentar siempre todo cambio, use la IA que use, bajo las mismas reglas.
- Cambios: capa común `ia/` (protocolo común 1.0.0 basado en el de Mes, `REGLAS.md` generadas de `politica.json`, frenos para Claude Code, hooks de git para cualquier IA, workflow `registro-ia.yml`, `INSTRUCCIONES_PROYECTO.md` para ChatGPT y Gemini, plantillas de petición y entrega); `GEMINI.md`; sección «Trabajo entre IA» en `AGENTS.md`; `.claude/settings.json` apunta a `ia/guard.py` (se retira `.claude/hooks/`); auditoría en `ia/AUDITORIA_2026-11-04.md`. Skill 0.4.1: sección «Registro y continuidad entre IA» y nota de portabilidad en `references/claude-code.md`; el método no cambia.
- Archivos: ver `ia/AUDITORIA_2026-11-04.md`, sección «Archivos cambiados».
- Verificación: `python3 ia/test_guard.py` → aprobado; `python3 ia/verificar.py reglas --check` → aprobado; `python3 -m unittest discover -s tests` → aprobado (23); `scripts/build.py` → aprobado.
- Revisión independiente: 17 hallazgos sobre el código común; corregidos los reproducidos, con pruebas de regresión (detalle en `ia/AUDITORIA_2026-11-04.md`).
- Pendiente: activar los hooks de git en cada copia (`sh ia/instalar.sh`); opcionalmente exigir el check `registro-ia` con protección de rama en GitHub.

## 0.4.0 — 4 de noviembre de 2026

- Se añadió `references/claude-code.md`: frenos activos del repositorio, modo plan y entrevista (sólo para MEJORAR o documentos completos desde cero, dentro del límite de preguntas vigente), reparto en paralelo para AUDITAR e INTERNO con datos minimizados, `/goal`, navegador para consultar fuentes oficiales, seguimiento comercial con CRM sólo con autorización específica y uso de `/insights` conforme a `references/actualizacion.md`.
- SKILL.md suma la sección «Terminado y trabajo en Claude Code» con el criterio de terminado por modo y los pasos que merecen máxima profundidad; la nueva referencia se agregó al listado y al inventario de `PUBLIC_FILES.json` (23 archivos).
- No se configuran `/loop` ni tareas programadas: la skill sigue sin tareas recurrentes.
- El método no cambió: reglas jurídicas, de verificación, privacidad, envío, estilo, licencia y controles se conservan. La edición sigue en piloto supervisado y la batería continúa en 23 pruebas.
- Se actualizaron los metadatos, ejemplos, NOTICE, empaquetado, guía de instalación y nombre del artefacto de CI a 0.4.0.

## 0.3.2 — 3 de noviembre de 2026

- Se ajustó el frontmatter al formato actual de Codex sin cambiar el alcance jurídico ni la licencia.
- El cálculo de huellas acepta rutas temporales normales de macOS bajo `/var`, pero sigue rechazando archivos que sean enlaces simbólicos.
- La batería aumenta a 23 pruebas e incluye una regresión explícita contra enlaces simbólicos.
- Se actualizaron los metadatos, ejemplos, empaquetado y guía de instalación a 0.3.2.

## 0.3.1 — 7 de octubre de 2026

- Se incorpora la skill completa y las mejoras operativas propuestas en 0.2.2, sobre la rama propietaria 0.3.0, a petición del titular.
- Se conservan sin cambios el texto de `LICENSE` y las condiciones de `USO_Y_LICENCIA.md`; se corrigen los metadatos y explicaciones del paquete que lo presentaban como una edición Apache.
- Se conservan las referencias jurídicas, las reglas de privacidad y revisión humana, los 35 escenarios conductuales y los expedientes sintéticos del paquete aportado.
- Se incorpora un empaquetador reproducible y una batería específica de 22 pruebas técnicas de integración, con CI y artefactos. No se afirma haber repetido las 93 pruebas del entorno de Claude ni su evaluación en modelos.
- Se documentan origen, huellas y limitaciones de los registros de evaluación. Se señala la diferencia entre los 202 caracteres del registro de activación y los 200 de la descripción empaquetada.
- La publicación de la skill en este repositorio público sustituye el estado de portal exclusivamente informativo. La licencia propietaria no impide técnicamente leer o descargar los archivos.
- La edición permanece en piloto supervisado, con revisión jurídica pendiente y sin instalación automática en cuentas de IA.

## 0.3.0 — 7 de octubre de 2026

- Se descontinúa la distribución abierta de versiones nuevas.
- Se adopta un modelo de Licencia Profesional escrita, pagada y limitada al uso interno del licenciatario.
- Se prohíben reventa, redistribución, sublicencia, marca blanca, hospedaje como servicio y comercialización de adaptaciones sin autorización específica.
- La rama pública deja de distribuir la herramienta completa y funciona como página informativa.
- Se reconoce expresamente que las versiones 0.2.0 y 0.2.1 conservan su licencia histórica Apache-2.0.

## 0.2.1 y anteriores

Versiones históricas. Consultar AVISO_VERSIONES_HISTORICAS.md.
