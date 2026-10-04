# Evaluación de esta edición

## Ejecuciones comprobadas

Fecha: 2026-10-04. Se ejecutaron **44 pruebas técnicas**, sin fallos, tanto en GitHub Actions como en un entorno local independiente a partir del código obtenido del artefacto de GitHub.

- Primer candidato: commit `3915a11388836169eaf8ae0e6ca7afc285e5a4a7`; ejecución `37226668798`, `success`.
- Candidato con paquetes: commit `580e5be0b55748fe91c737f2a1b5669d164c28e6`; ejecución `37226797310`, `success`.
- Artefacto descargado: ID `11311618564`; SHA-256 `eb16e4e0170d43b8ec1c96ddc352bf1a21737f88181c550faf0a03c2ffe0c9eb`, cotejado localmente.
- Comando local: `python3 -m unittest discover -s tests -v`; resultado: 44 tests, OK.
- Empaquetado local y verificación de hashes: completados.
- Plantilla DOCX en blanco: generada; PDF de **6 páginas** renderizado; inspección visual de las seis páginas realizada, sin texto cortado ni solapamientos observados. Esto no certifica una edición final del cliente no aportada.

Los cambios posteriores deben volver a ejecutar CI. Consultar la ejecución asociada al commit utilizado, no asumir que el resultado de un candidato se traslada automáticamente.

## Qué comprueban los tests técnicos

Estructura de estado, versiones, tipos de datos, controles registrados de riesgo/lectura/jurisdicción/representación, referencia de aprobación para acciones, aritmética y calendario de honorarios, referencias internas, JSON, empaquetado y reproducibilidad.

El controlador no autentica firmas ni depósitos, no sabe si una fuente realmente sostiene una conclusión, no determina competencia o prescripción y no comprueba habilitación profesional. Un test verde no autoriza emitir ni presentar un documento.

## Evaluaciones de IA pendientes

`skills/milla-asesoria-juridica/assets/evaluaciones.json` contiene **24 escenarios sintéticos**, no 24 resultados de modelos. Deben ejecutarse en cada producto que use la firma; registrar versión, fecha, salida, calificación y revisión humana. No se atribuyen resultados a Claude, Gemini, ChatGPT, Grok, DeepSeek o Kimi sin pruebas reales.

Un fallo crítico en privacidad, fuente inventada, plazo, garantía, autorización o ejercicio profesional bloquea aprobación. No compensarlo con promedio alto de estilo. También permanece pendiente la aprobación jurídica institucional de la titular.

## Alcance de la revisión visual y privacidad

El generador produce un modelo en blanco con campos. Cada documento real debe revisar fuentes, cifras, firmas, datos, saltos, índice, encabezados, pies, tablas y recuadros. La plantilla no contiene un diagnóstico aprobado de ningún cliente.

El contenido público se redactó como metodología general, con plantillas vacías y ejemplos sintéticos. Las pruebas de texto o formatos son controles auxiliares, no una certificación exhaustiva de anonimización.

## CI y artefactos

GitHub Actions ejecuta pruebas técnicas y genera paquetes cuando hay cambios o ejecución manual. Conserva durante 30 días la metodología y el código público de ese commit, sin historial Git. No vigila reformas, no envía mensajes y no publica expedientes. Los paquetes pueden regenerarse desde el código aunque expire un artefacto.
