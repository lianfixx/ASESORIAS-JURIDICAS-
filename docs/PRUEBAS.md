# Evaluación de esta edición

## Qué comprueban los tests técnicos

`python3 -m unittest discover -s tests -v` revisa estado inicial, versiones, tipos de datos, controles registrados de riesgo/lectura/jurisdicción/representación, necesidad de aprobación para acciones, aritmética y calendario de honorarios, referencias internas, JSON, empaquetado y reproducibilidad.

El controlador no autentica firmas ni depósitos, no sabe si una fuente realmente sostiene una conclusión, no determina competencia o prescripción y no comprueba que alguien tenga habilitación profesional. Un test verde no autoriza emitir ni presentar un documento.

## Evaluaciones de IA

`assets/evaluaciones.json`, dentro de la skill, contiene 24 escenarios sintéticos con conducta esperada y fallo crítico. Deben ejecutarse en cada producto que use la firma; registrar versión, fecha, salida, calificación y revisión humana. No se atribuyen resultados a Claude, Gemini, ChatGPT, Grok, DeepSeek o Kimi sin pruebas reales.

Un fallo crítico en privacidad, fuente inventada, plazo, garantía, autorización o ejercicio profesional bloquea aprobación. No compensarlo con un promedio alto de estilo.

## Plantilla editorial

El generador opcional produce un modelo en blanco. Revisar el DOCX y cada página del PDF renderizado, especialmente encabezados, números, recuadros, tablas y firmas. La prueba visual de una plantilla no valida documentos posteriores rellenados.

## Registro de ejecución

- Fecha: 2026-10-04.
- Commit candidato: `3915a11388836169eaf8ae0e6ca7afc285e5a4a7`.
- GitHub Actions: ejecución `37226668798`, conclusión `success`.
- Se ejecutaron los tests técnicos y la construcción de paquetes. Se añadirá la revisión visual local cuando se complete.
- Los escenarios conductuales de otras IA y la aprobación jurídica de la titular permanecen pendientes.

El workflow conserva, durante 30 días, paquetes de metodología y una copia del código público de ese commit, sin historial de Git. No constituye vigilancia normativa ni publica documentos de clientes. La disponibilidad del workflow no demuestra el resultado de futuras ejecuciones: comprobar cada una.
