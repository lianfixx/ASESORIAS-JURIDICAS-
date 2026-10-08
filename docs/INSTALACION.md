# Preparar y usar la skill 0.3.1

La distribución conserva las condiciones de `LICENSE`. Estos pasos no acreditan una licencia de uso ni sustituyen revisión jurídica.

## Obtener el paquete

Desde una copia del repositorio con Python 3.10 o posterior:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build.py --output /tmp/milla-build
```

La salida contiene `milla-asesoria-juridica-0.3.1.zip`, una copia idéntica con extensión `.skill`, `MILLA_GUIA_UNIVERSAL_0.3.1.txt` y `SHA256SUMS.txt`. El ZIP contiene una sola carpeta raíz con `SKILL.md`, sus referencias, recursos, script de control y avisos de licencia. No incluye los expedientes sintéticos ni los registros de un asunto.

## Uso como archivos de referencia

Adjunta la guía universal o proporciona la carpeta completa en un entorno autorizado. Pide leer `SKILL.md`, comprobar la versión y aplicar el modo GUÍA. El asistente debe cargar las referencias que exige cada tarea antes de concluir. Cuando la aplicación no puede abrir rutas relativas, la guía universal reúne los textos con sus nombres de origen.

No asumas que el asistente leyó el ZIP porque lo recibió: debe confirmar acceso al contenido. Compartir una URL del repositorio tampoco garantiza que la aplicación pueda consultarlo.

## Instalación propia de cada producto

El mecanismo de instalación y la extensión admitida dependen del producto, versión, cuenta y espacio de trabajo. Comprueba su documentación oficial y su interfaz actual. No se afirma que la extensión `.skill` sea aceptada por todas las aplicaciones; su contenido es un ZIP y no un ejecutable.

Esta integración no realizó una instalación dentro de una cuenta de ChatGPT o Claude. La instalación del ZIP 0.2.2 mencionada en el informe aportado corresponde al entorno anterior de Claude, no a una prueba de la edición 0.3.1.

## Sustituir una copia anterior

Conserva la versión utilizada en documentos ya emitidos. Reemplaza la copia instalada sólo cuando se adopte la nueva versión y confirma cuál está leyendo el asistente. Actualizar GitHub no actualiza otras cuentas, conversaciones ni proyectos.

Los estados anteriores requieren revisión de compatibilidad. No cambies una versión en el JSON para eludir un control ni migres aprobaciones sin revisar el documento, acción, versión y huella correspondientes.
