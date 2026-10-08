# Integración de la skill 0.3.1

Fecha de preparación: 7 de octubre de 2026. Base de publicación: `23cfcc2f175c95e9b295e78f68ace95eb25ac134` (edición propietaria 0.3.0).

## Qué se incorporó

Se tomó la skill completa del ZIP 0.2.2 aportado por el titular: metodología, referencias, recursos, controles y 35 escenarios. Se recuperaron del bundle los expedientes inventados y el material de la prueba de activación. Se conservó la descripción empaquetada de 200 caracteres, sin atribuirle una nueva prueba de activación.

Se integró una edición 0.3.1 en vez de sustituir la rama principal por la 0.2.2 anterior al cambio de licencia. El texto de `LICENSE` y `USO_Y_LICENCIA.md` de 0.3.0 permanece íntegro. La copia instalada incluye esas condiciones; los metadatos identifican `LicenseRef-MILLA-Professional-1.0`. Se conservan el origen, avisos históricos y el componente de control que mantiene su aviso Apache.

La autorización del titular para subir la skill a este repositorio se documenta como decisión de publicación, no como aprobación jurídica de las reglas o de respuestas a clientes. El repositorio sigue siendo público; la licencia no restringe técnicamente su lectura o descarga.

## Qué se comprobó en esta integración

Se ejecutó `python3 -m unittest discover -s tests -v`: **22 pruebas superadas**. Cubren versión, metadatos, descripción, identidad de la licencia, avisos históricos, enlaces relativos, JSON, escenarios, configuración en blanco, estado sintético, bloqueo de actuaciones sin aprobaciones, identificadores, ubicación de estados privados, versiones incompatibles, importes, sumas, claves duplicadas, inventario del paquete, reproducibilidad, destino del build y huellas de documentos.

El empaquetador generó un ZIP de **22 archivos** con una sola carpeta raíz, una copia `.skill`, una guía universal y las huellas SHA-256. Dos construcciones independientes produjeron resultados idénticos. Los casos sintéticos y las pruebas quedan fuera del paquete instalable.

GitHub Actions quedó configurado para repetir esta batería y crear los artefactos. El resultado efectivo de una ejecución remota debe consultarse en el run correspondiente; este texto no sustituye esa evidencia.

## Qué no se está afirmando

Las 93 pruebas que declaró Claude pertenecen a su entorno y a su edición; no se presentan como 93 pruebas reejecutadas aquí. Esta integración aporta su batería identificada de 22 pruebas y no certifica equivalencia total de cobertura con la anterior.

No se reejecutaron aquí las evaluaciones de respuestas ni de activación en modelos. No se instaló esta edición en una cuenta de ChatGPT o Claude. No se verificaron íntegramente los fundamentos jurídicos ni se obtuvo aprobación de la titular.

## Trazabilidad y límites de la evaluación aportada

[`evaluacion/PROCEDENCIA_0.2.2.json`](evaluacion/PROCEDENCIA_0.2.2.json) identifica las huellas del ZIP, bundle y registros originales. Los registros completos de respuestas permanecen en los adjuntos de origen; no se publican como una nueva evaluación 0.3.1 ni se importan los tres commits antiguos sobre `main`.

[`evaluacion/RESUMEN_0.2.2.json`](evaluacion/RESUMEN_0.2.2.json) separa resultados reportados de limitaciones. El informe de Claude presenta 30/30 activaciones pertinentes y 0/33 improcedentes, pero su JSON registra una candidata de **202 caracteres**, mientras el ZIP y el informe describen **200**. Por ello no se acredita que la cadena empaquetada sea exactamente la evaluada. Además, se reutilizó el conjunto de consultas para ajustar la descripción y no se demostró lectura consistente de referencias.

La revisión jurídica, las pruebas independientes de activación con la descripción exacta y una evaluación en la aplicación de destino siguen pendientes. Un test técnico correcto no permite cerrar esos pendientes.
