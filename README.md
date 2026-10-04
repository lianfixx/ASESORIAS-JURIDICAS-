# MILLA ABOGADOS · Asesorías jurídicas asistidas

**Versión 0.2.0 · Piloto supervisado · México configurable · 4 de octubre de 2026**

Una metodología portable para pasar de la información inicial de un cliente a una asesoría, un diagnóstico comprensible y una ruta de actuación documentada. Conserva el estilo institucional de MILLA ABOGADOS y exige revisión de la persona abogada responsable. No es un abogado autónomo, un repertorio de leyes siempre vigente ni una garantía de resultado.

## Comenzar sin programar

Lee [EMPIEZA_AQUI.md](EMPIEZA_AQUI.md). En un chat o proyecto exclusivo del asunto, adjunta la edición universal de la guía, el expediente preliminar y la asesoría de la titular, si ya existe. Escribe:

> Activa MILLA Asesorías en modo GUÍA. Lee los archivos disponibles y distingue lo revisado de lo que sólo se menciona. Antes de avanzar, revisa urgencias, jurisdicción y representación. No repitas preguntas resueltas. Guíame por una etapa cada vez, explica brevemente por qué importa y pide sólo la siguiente información indispensable. No envíes comunicaciones ni asumas honorarios, pagos o autorizaciones.

No incluyas datos identificables en una plataforma hasta comprobar que su uso está autorizado y es adecuado. Este repositorio es público: **no es un expediente de clientes**.

## Qué contiene

- Una [skill](skills/milla-asesoria-juridica/SKILL.md) conforme a la estructura Agent Skills: instrucciones breves, referencias, plantillas y scripts auxiliares.
- Un flujo de recepción, urgencias, resumen, investigación, asesoría de 30–45 minutos, diagnóstico, contratación, negociación, actuación y cierre.
- Módulos familiares y laborales; rutas de investigación para otras materias. Cada asunto requiere fuentes y competencia verificadas.
- Plantillas para los entregables y para el estado del asunto, fuentes, honorarios y aprobación.
- Pruebas técnicas reproducibles y escenarios de evaluación jurídica y comunicativa por una persona revisora.
- Un proceso de retroalimentación, revisión y versiones. Las mejoras no se incorporan automáticamente ni modifican asuntos activos sin revisión.

## Dos maneras de utilizarlo

**Lectura universal:** una guía Markdown/TXT que puede adjuntarse o leerse por partes en asistentes capaces de procesar texto. No requiere soporte nativo de skills. Su eficacia depende del modelo, su contexto y sus herramientas.

**Skill nativa:** la carpeta `skills/milla-asesoria-juridica/` para herramientas compatibles. Consulta [instalación y compatibilidad](docs/INSTALACION.md). La documentación de un formato compatible no equivale a una prueba de funcionamiento en todas las aplicaciones.

## Verificar y generar paquetes

Con Python 3.10 o superior, sin dependencias para las pruebas y el empaquetado:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build.py --output dist
```

Se generan una guía universal, un ZIP de la skill y un manifiesto SHA-256. El generador de plantilla Word es opcional y requiere `python-docx`:

```sh
python3 -m pip install -r requirements-documentos.txt
python3 scripts/plantilla_docx.py --output dist/Plantilla_Diagnostico_MILLA.docx
```

La plantilla tiene campos de captura: **no es un diagnóstico final de ningún cliente**. Antes de entregar documentos reales hay que revisar fuentes, contenido, aprobación, firmas y el PDF renderizado.

## Gobernanza y límites

La biblioteca pública almacena método; los expedientes permanecen separados y privados. Leer [seguridad](SECURITY.md), [recapitulación](docs/RECAPITULACION.md), [mejoras y actualización](docs/MEJORAS_Y_ACTUALIZACION.md) y [evaluación](docs/PRUEBAS.md).

## Licencia para otros profesionales

Las aportaciones originales públicas de esta edición se ofrecen bajo **Apache-2.0**. Se permite usarlas, adaptarlas y redistribuirlas, incluso en servicios remunerados, conservando los avisos y señalando cambios conforme a la licencia. No concede uso de marca para aparentar afiliación ni autorización para ejercer una profesión. Los expedientes privados y los materiales de terceros no se licencian por estar relacionados con esta metodología.

Leer [LICENSE](LICENSE), [NOTICE](NOTICE), [uso y atribución](USO_Y_LICENCIA.md) y [contribuciones](CONTRIBUTING.md). No se exige publicar mejoras privadas ni documentos de clientes. La atribución del método no debe confundirse con la identidad del despacho que presta el servicio.

## Auditoría y migración

La edición 0.2.0 corrige inclusión accidental de archivos, manifestaciones excesivas de privacidad, entradas JSON defectuosas y aprobaciones no vinculadas a una versión concreta. El [informe de auditoría](docs/AUDITORIA_0.2.0.md) identifica evidencia, correcciones y límites. El esquema de estado cambia a 2: [migración supervisada](docs/MIGRACION_0.2.0.md). No se trasladan aprobaciones automáticamente.

Los paquetes se construyen desde [PUBLIC_FILES.json](PUBLIC_FILES.json), no desde una búsqueda indiscriminada. El escaneo es heurístico y no certifica anonimización. Las evaluaciones de respuestas de otros modelos continúan pendientes.

Esta edición no incluye acceso a cuentas, credenciales, envíos de WhatsApp, presentación de demandas ni monitoreo normativo permanente. Los scripts no emiten opiniones jurídicas ni calculan vencimientos procesales. Los documentos finales y las decisiones jurídicas requieren aprobación profesional humana.
