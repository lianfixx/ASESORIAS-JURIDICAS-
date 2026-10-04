# Migración a 0.2.0 · esquema de estado 2

La biblioteca y los expedientes no son lo mismo. Actualizar la skill no autoriza modificar documentos emitidos, borrar evidencia ni trasladar aprobaciones. Conservar la edición anterior del estado en almacenamiento privado, registrar quién migra y revisar los asuntos afectados. Nunca subir esos registros al repositorio público.

## Qué cambia

`assets/release.json` define versión, esquema y licencia. En un estado revisado se registran `schema_version: 2`, `skill_version: "0.2.0"` y la lista `documents`. No basta cambiar esos dos números: cada autorización debe relacionarse con una acción, un documento, su versión y la huella SHA-256 del archivo efectivamente revisado.

Las fuentes llevan ID único. Cada documento identifica las fuentes utilizadas con `source_ids`. Una fuente verificada de otro apartado no desbloquea el documento que utiliza fuentes pendientes. El control no evalúa la suficiencia jurídica del texto ni comprueba por internet su vigencia.

Ejemplo exclusivamente sintético de estructura; las huellas y datos deben provenir de una revisión real, no copiarse:

```json
{
  "documents": [{
    "id": "DOC-001",
    "version": "v1",
    "sha256": "[HUELLA CALCULADA DEL ARCHIVO]",
    "status": "revisado",
    "source_ids": ["SRC-001"]
  }],
  "approvals": [{
    "action": "emitir_diagnostico",
    "document_id": "DOC-001",
    "document_version": "v1",
    "document_sha256": "[MISMA HUELLA REVISADA]",
    "approved_by": "[PERSONA QUE REALMENTE APROBO]",
    "date": "[FECHA REAL]",
    "evidence_ref": "[REFERENCIA PRIVADA DE LA AUTORIZACION]"
  }]
}
```

Los corchetes son explicativos: ese fragmento no es un estado válido listo para ejecutar. Se conserva la evidencia de aprobación fuera del repositorio. El controlador no convierte una anotación en firma auténtica.

## Comprobación

```sh
python3 skills/milla-asesoria-juridica/scripts/control.py check /ruta/privada/estado.json
python3 skills/milla-asesoria-juridica/scripts/control.py check /ruta/privada/estado.json --gate emitir_diagnostico --document-id DOC-001 --document /ruta/privada/diagnostico.pdf
```

Si cambia el archivo, cotejar diferencias, obtener la revisión correspondiente y actualizar versión, huella y evidencia. No actualizar todas las huellas sólo para conseguir un resultado verde. Las aprobaciones históricas sin vinculación suficiente quedan pendientes de nueva revisión; no se regeneran retrospectivamente.

El script impide crear estados en la biblioteca pública. En una skill instalada también deben quedar fuera de su carpeta. El control de un riesgo urgente interrumpe la ruta ordinaria; nunca debe retrasar la ayuda o actuación profesional urgente que corresponda.

## Distribución

Conservar `LICENSE` y `NOTICE` al redistribuir la biblioteca. Las nuevas copias se generan en una carpeta vacía y con el inventario público. La guía completa sirve para lectura; los controles de archivo requieren ejecutar los scripts en un entorno adecuado. Actualizar manualmente las copias instaladas y la guía adjunta a cada proyecto cuando se adopte esta edición.
