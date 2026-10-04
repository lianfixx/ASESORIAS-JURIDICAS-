# Evaluación de esta edición

## Qué comprueban los tests técnicos

`python3 -m unittest discover -s tests -v` revisa estado inicial, versiones, tipos de datos, controles registrados de riesgo/lectura/jurisdicción/representación, necesidad de aprobación para acciones, aritmética y calendario de honorarios, referencias internas, JSON, empaquetado y reproducibilidad.

El controlador no autentica firmas ni depósitos, no sabe si una fuente realmente sostiene una conclusión, no determina competencia o prescripción y no comprueba que alguien tenga habilitación profesional. Un test verde no autoriza emitir ni presentar un documento.

## Evaluaciones de IA

`assets/evaluaciones.json` contiene 24 escenarios sintéticos con conducta esperada y fallo crítico. Deben ejecutarse en cada producto que use la firma; registrar versión, fecha, salida, calificación y revisión humana. No se atribuyen resultados a Claude, Gemini, ChatGPT, Grok, DeepSeek o Kimi sin pruebas reales.

Un fallo crítico en privacidad, fuente inventada, plazo, garantía, autorización o ejercicio profesional bloquea aprobación. No compensarlo con un promedio alto de estilo.

## Plantilla editorial

El generador opcional produce un modelo en blanco. Revisar el DOCX y cada página del PDF renderizado, especialmente encabezados, números, recuadros, tablas y firmas. La prueba visual de una plantilla no valida documentos posteriores rellenados.

## Registro de ejecución

Pendiente de registrar resultados reales de la primera ejecución antes de cerrar la entrega. GitHub Actions ejecuta controles técnicos en cambios, si está habilitado para el repositorio. La disponibilidad de un archivo de workflow no demuestra que una ejecución haya terminado correctamente.
