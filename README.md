# MILLA Asesorías · asesoría jurídica guiada

**Edición 0.3.1 · licencia propietaria · piloto supervisado · México**

La skill está en [`skills/milla-asesoria-juridica/SKILL.md`](skills/milla-asesoria-juridica/SKILL.md). Esta edición incorpora las mejoras operativas del paquete 0.2.2 aportado por el titular y conserva las condiciones de licencia adoptadas en 0.3.0. No constituye aprobación jurídica de las respuestas ni instalación automática en una cuenta de IA.

## Acceso y uso

Esta edición **no es software abierto ni una descarga de libre uso**. El uso de la edición propietaria requiere una **Licencia Profesional escrita, vigente y pagada**, conforme a [`LICENSE`](LICENSE) y [`USO_Y_LICENCIA.md`](USO_Y_LICENCIA.md).

La licencia ordinaria permite al profesional o firma autorizada utilizarla internamente en su propio trabajo y cobrar honorarios por los servicios jurídicos que preste a sus clientes. No permite vender, revender, sublicenciar, publicar, redistribuir, compartir, alojar, ofrecer como servicio ni comercializar una adaptación de la herramienta sin autorización específica.

## Contenido disponible

La biblioteca incluye la skill completa con sus referencias, plantillas y controles auxiliares; 35 escenarios conductuales; expedientes enteramente sintéticos para evaluación; un empaquetador reproducible y 22 pruebas técnicas de integración. Las pruebas técnicas no certifican corrección jurídica, vigencia de leyes ni activación automática en un asistente.

Consulta [`docs/INTEGRACION_0.3.1.md`](docs/INTEGRACION_0.3.1.md) para conocer lo integrado, las comprobaciones y los pendientes. Los registros originales de Claude no se presentan como nuevas pruebas de esta edición: se documentan su procedencia, huellas y limitaciones en [`docs/evaluacion/`](docs/evaluacion/PROCEDENCIA_0.2.2.json).

## Empaquetar y utilizar

Con Python 3.10 o posterior, desde la carpeta del repositorio:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build.py --output /tmp/milla-build
```

Se generan un ZIP, su copia con extensión `.skill`, una guía universal de texto y las huellas SHA-256. La extensión que admite la aplicación debe comprobarse en su interfaz; el archivo `.skill` no es un instalador ejecutable.

Para trabajar en una conversación, proporciona la guía universal completa o los archivos de la skill y pide aplicar el modo GUÍA. La aplicación debe confirmar lectura de las referencias necesarias. Adjuntar un archivo no equivale a instalarlo permanentemente ni sincroniza otros chats. Lee [`docs/INSTALACION.md`](docs/INSTALACION.md).

GitHub Actions ejecuta las pruebas y genera un artefacto de empaquetado en cada revisión que las supere. El artefacto tiene retención de siete días; los archivos fuente y el script permiten reconstruirlo.

## Estado del repositorio y privacidad

Por instrucción del titular, este repositorio vuelve a alojar la herramienta. **Mientras el repositorio sea público, sus archivos serán visibles y podrán descargarse: la licencia no es un control técnico de acceso.** La publicación no transforma la edición propietaria en una oferta de uso libre. Para restringir el acceso técnico debe cambiarse la visibilidad o utilizarse un repositorio privado.

No se alojan aquí expedientes ni estados de asuntos reales. Los documentos de clientes, firmas, comunicaciones, identificaciones, datos personales y credenciales deben mantenerse fuera de esta biblioteca. Consulta [`SECURITY.md`](SECURITY.md).

## Propiedad, versiones históricas y solicitudes

La licencia es de uso, no de propiedad. No autoriza utilizar la marca para aparentar afiliación, representación o aval. La herramienta es auxiliar y no sustituye investigación vigente, criterio profesional, habilitación legal, secreto profesional ni revisión humana.

Los permisos válidamente concedidos en versiones históricas y los componentes con aviso propio se conservan. La copia de Apache en la carpeta `LICENSES` de la skill documenta ese origen y no licencia de nuevo el conjunto propietario. Consulta [`AVISO_VERSIONES_HISTORICAS.md`](AVISO_VERSIONES_HISTORICAS.md).

Solicitudes: [`SOLICITAR_LICENCIA.md`](SOLICITAR_LICENCIA.md), **socios@millabogados.com**. El pago aislado no sustituye el instrumento escrito que identifica licenciatario, modalidad, usuarios, versión, plazo, precio y alcance.
