# Mejora continua, versiones y aprobación

## Qué significa «se actualiza»

La herramienta puede registrar problemas y proponer cambios. No se reentrena, no aprende automáticamente de expedientes, no modifica leyes ni mantiene un servicio de vigilancia por instalarla. El repositorio es la fuente de versiones del método; cada copia instalada debe actualizarse expresamente.

## Ciclo de cambio

1. Registrar una observación sin datos de clientes: regla afectada, conducta observada, riesgo, corrección propuesta y ejemplo sintético.
2. Clasificar: estilo; operación; fuente normativa; seguridad; cálculo; compatibilidad técnica.
3. Verificar fuentes. Para cuestiones legales, leer texto vigente, transitorios y criterios aplicables, documentando el caso de uso general sin revelar el expediente.
4. Proponer un parche en rama independiente; enlazar la incidencia y actualizar la prueba que detecta el problema.
5. Ejecutar pruebas técnicas y los escenarios de evaluación afectados. Registrar proveedor, versión, fecha y resultados sólo si realmente se ejecutaron.
6. Revisión humana: la responsable jurídica aprueba contenido legal; el mantenedor revisa técnica y privacidad. No inventar su aprobación ni sustituirla por un test verde.
7. Publicar versión con changelog, riesgos y migración. No activar auto-merge de cambios jurídicos.
8. Evaluar asuntos activos: qué documentos o decisiones dependen de la regla anterior; alertar al equipo y corregir mediante nuevas versiones, sin sobrescribir el historial.

## Niveles de versión propuestos

- PATCH: corrección editorial o técnica que no cambia estrategia ni requisitos.
- MINOR: nueva plantilla, módulo o control compatible, con revisión.
- MAJOR: modificación de alcance, flujo, estructura de estado o reglas sustantivas que exige migración.

Son reglas de mantenimiento propuestas, no normas jurídicas. Mientras el proyecto sea 0.x, un cambio incompatible se identifica incrementando MINOR y documentando migración. La edición 0.2.0 introduce esquema 2 y mantiene el estado de piloto supervisado: no acredita validación de la titular ni pruebas en otros modelos.

## Momentos de revisión

Revisar fuentes en cada nuevo diagnóstico y antes de actuar; también cuando cambie jurisdicción, se reciba una notificación, surja una reforma/criterio o varíe el objetivo. Una revisión periódica mensual del método puede adoptarse como política interna, pero **no está programada** por esta publicación.

La comprobación de que un enlace responde no demuestra que el texto siga vigente ni que una regla sea aplicable. La detección automática de diferencias puede producir una alerta, nunca aprobar por sí misma una nueva regla.

## Métricas útiles

Registrar de manera agregada y disociada: preguntas repetidas, afirmaciones sin fuente, datos críticos omitidos, correcciones de la titular, errores aritméticos, citas descartadas, duración de preparación, claridad percibida y fallos de privacidad. No confundir aceptación de la propuesta, rapidez o satisfacción con corrección jurídica o resultado favorable.

## Configuración pendiente de la firma

La titular debe aprobar: protocolo de conflictos, alcance profesional por materia, tarifas/costos internos, descuentos y créditos, calendario de seguimiento, política de retención, proveedores autorizados, personas revisoras y condiciones internas de distribución. La licencia pública Apache-2.0 fue autorizada para esta edición; no están autorizadas por ello las demás políticas. Hasta entonces esos puntos son pendientes, no decisiones adoptadas por la IA.

## Publicación segura

Esta edición usa GitHub Actions únicamente para pruebas técnicas en cambios y ejecución manual. No consulta expedientes, no tiene secretos, no contacta clientes, no publica reformas y no escribe sobre el repositorio desde CI. El flujo de revisión humana debe conservarse aunque se agreguen agentes colaboradores.
