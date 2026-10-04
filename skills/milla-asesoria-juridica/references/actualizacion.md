# Configuración, retroalimentación y actualización de una skill instalada

## Configuración inicial de la firma

Completar `assets/configuracion.ejemplo.json` en un espacio privado, nunca con datos reales dentro de la biblioteca pública. Identificar responsable profesional, materias cubiertas, jurisdicciones, autorización de proveedores, política de honorarios, canales y persona que aprueba cambios. Los valores pendientes no deben completarse por intuición.

La configuración no amplía habilitación profesional ni concede permisos técnicos. Un estudiante, auxiliar u otro usuario puede preparar documentos y organizar hechos, pero la dirección jurídica y las actuaciones requieren el profesional y las formalidades aplicables.

## Corrección local frente a cambio general

Si el usuario corrige un dato de su caso, actualizar el estado privado con fuente y fecha; no convertirlo en regla para otros clientes. Si corrige el estilo, identificar si es preferencia de ese documento o instrucción institucional. Si corrige una regla jurídica, verificar la fuente y el alcance antes de adoptarla.

Un aviso de reforma, una noticia o un desacuerdo no produce actualización automática. Registrar propuesta: regla anterior, problema, evidencia, consecuencia, texto nuevo, prueba sintética y revisión pendiente. Las reglas anteriores permanecen identificables para revisar su impacto en documentos ya emitidos.

## Procedimiento de actualización

1. Registrar un hallazgo desidentificado, sin hechos que permitan reconstruir el caso.
2. Clasificar el cambio como editorial, técnico, operativo, jurídico o de seguridad.
3. Verificar fuentes y proponer un parche, sin atribuir aprobación a la titular.
4. Ejecutar las pruebas técnicas disponibles y los escenarios conductuales afectados.
5. Obtener aprobación humana según el tipo de cambio; un test verde no valida derecho.
6. Publicar versión y changelog con migración y riesgos; no hacer auto-merge de reglas jurídicas.
7. Sustituir la copia instalada o la guía adjunta al proyecto únicamente cuando se adopte la nueva versión.
8. Revisar asuntos activos afectados; conservar la edición con que se emitieron documentos y corregir por versiones, no por borrado del historial.

Si la IA no tiene permisos de GitHub, debe entregar un archivo o parche propuesto, no afirmar que quedó guardado. Si tiene permisos, la instrucción de mejorar el texto no autoriza publicar información del expediente ni alterar otras ramas o productos.

## Revisión del desempeño

Usar `assets/evaluaciones.json`: entradas sintéticas con conducta esperada y fallo crítico. Conservar para cada prueba modelo/producto, versión, fecha, texto de entrada y salida disociada, evaluación y revisora. No atribuir resultados a modelos no ejecutados. Un fallo crítico bloquea aprobación aunque el estilo sea excelente.

Medir omisiones, preguntas repetidas, afirmaciones sin fuente, errores de montos, datos innecesarios, documentos con marcadores, contradicciones y claridad de siguientes pasos. No equiparar satisfacción del cliente o cobro con corrección jurídica.

## Alcance de la automatización

Esta skill no mantiene tareas de fondo, no reentrena modelos, no vigila reformas ni actualiza copias de otros asistentes. El repositorio incluye CI de pruebas de código y paquetes; no un asesor jurídico autónomo. Una revisión periódica del método puede adoptarse por la firma, pero requiere programarla y definir responsables.

Para continuar en otra IA, exportar versión y resumen de continuidad con datos mínimos autorizados. El repositorio público no recibe ese estado. Las conexiones, calendarios, sistemas de expedientes y envíos deben configurarse y autorizarse por separado.
