# Auditoría de licencia, metodología y controles · 0.2.0

Fecha de corte: 2026-10-04. Estado: piloto supervisado. Revisión técnica asistida por IA, no auditoría independiente ni aprobación profesional institucional.

## Alcance y procedencia

Se verificó el repositorio público `lianfixx/ASESORIAS-JURIDICAS-` mediante la conexión autorizada. Base: commit `87780e8b4bc11421afe1e3d80fcc44046ee12b50`; árbol `cd1fe968e0559d701a1a14ee7a84cf6a757490c9`. La copia fuente del paquete previo produjo exactamente ese árbol Git antes de modificarla. Se revisaron código, metodología, plantillas, fuentes registradas y controles de distribución de esa revisión.

No se auditó exhaustivamente todo el historial Git, forks, cachés, cuentas de terceros, asistentes externos ni expedientes privados. Los documentos históricos de clientes no se incorporaron a esta publicación.

## Hallazgos y correcciones

| Hallazgo | Relevancia | Corrección de esta edición |
|---|---|---|
| Biblioteca pública sin licencia expresa | Impedía asumir permiso de reutilización | Apache-2.0 íntegra, NOTICE, alcance, contribuciones y exclusiones de marca/datos |
| Archivo añadido a la skill entraba automáticamente en el ZIP | Riesgo alto de publicación accidental | Inventario explícito, rechazo de archivos no aprobados en la skill y de archivos versionados fuera del inventario |
| Código fuente se empaquetaba con una ruta diferente | El ZIP fuente podía eludir controles | Ambos ZIP usan el mismo inventario y manifiesto de hashes |
| Escaneo limitado a la skill | Documentación de raíz sin el mismo control | Escaneo de todos los archivos del inventario; valores detectados no se muestran en logs |
| Manifiesto declaraba ausencia de datos de clientes | Afirmación no demostrable por patrones | Se registra alcance heurístico, falsos positivos/negativos y revisión humana; no se certifica anonimización |
| Tipos JSON malformados producían errores o aceptación indebida | Bypass o interrupción del control | Tipos estrictos, rechazo de booleanos como versión, duplicados y constantes no estándar |
| Aprobación sólo identificaba una acción | Podía reutilizarse después de cambiar el documento | ID, versión, SHA-256, fuentes del documento y comprobación del archivo actual |
| Estado privado podía crearse fuera de la skill pero dentro del repo | Riesgo de mezcla entre método y casos | Creación rechazada en la biblioteca completa o la skill instalada |
| Prueba de duración no leía el guion | Un test verde no detectaba cambios en la agenda | La prueba analiza intervalos reales de la tabla, continuidad y duración |
| Versión y paquetes podían divergir | Distribución inconsistente | Registro de release, licencia en cada formato, reproducibilidad y migración explícita |
| Terceros podían confundir marca con autorización | Riesgo de atribución profesional falsa | Separación de origen del método, identidad del usuario, habilitación y responsabilidad |

## Pruebas reproducibles

La línea base superó sus 44 pruebas técnicas, pero las nuevas pruebas adversas reprodujeron errores de tipos, JSON y distribución no contemplados por esa suite. La edición corregida superó 88 pruebas técnicas locales; se comprobó su plantilla en blanco en seis páginas. La ejecución y resultados se documentan en [PRUEBAS.md](PRUEBAS.md). No confundir cantidad de pruebas con cobertura absoluta.

## Revisión jurídica y metodológica

Se conservan: resumen preliminar antes del diagnóstico; urgencias antes de completar formularios o cobrar; hechos atribuidos a sus fuentes; competencia y reglas locales verificadas; separación de negociación privada y mecanismo institucional; documento proporcional al consenso; honorarios sólo autorizados; supervisión profesional y cierre no automático.

Se contrastaron fuentes primarias sobre licencia Apache, privacidad, conciliación laboral y régimen transitorio procesal. Esto confirma controles metodológicos acotados, no revalida cada afirmación de conversaciones históricas ni todas las normas de México. No se añadieron jurisprudencias no verificadas ni se sustituyó una investigación por materia y sede. Las fichas operativas de cada centro siguen requiriendo comprobación real.

## Pendientes y límites

1. **Protección de rama:** la rama principal se encontró sin protección. Se añade CODEOWNERS y se usa revisión mediante PR, pero eso no impide técnicamente cambios directos. Requiere configurar reglas y revisores desde la administración de GitHub.
2. **Pruebas de otras IA:** los escenarios son definiciones para evaluar respuestas, no resultados atribuidos a modelos. No se ejecutó la skill en Claude, Gemini, Grok, DeepSeek, Kimi u otras cuentas.
3. **Validación profesional:** sigue pendiente la aprobación institucional de la persona abogada responsable y la validación de cada diagnóstico, actuación y política interna.
4. **Privacidad:** la revisión y el escaneo reducen riesgo; no demuestran ausencia universal de datos o secretos ni cubren copias históricas/externas.
5. **Cadena de suministro:** acciones fijadas por SHA y permisos mínimos; no se realizó una auditoría interna completa de dependencias ni una prueba de penetración.
6. **Autoría y derechos:** la autorización cubre los derechos que puedan otorgar los aportantes; no certifica registro, exclusividad, origen humano íntegro ni licencias de materiales ajenos.
7. **Controles opcionales:** leer instrucciones no impide que un modelo las ignore. Los scripts deben ejecutarse; no se presenta un bloqueo automático universal de las aplicaciones de IA.
8. **Integridad no es autenticidad:** hashes y referencias de aprobación detectan incoherencias registradas. No verifican firma, mandato, depósitos, habilitación ni validez sustantiva.

## Fuentes externas contrastadas

- Apache License 2.0, secciones 2 y 4–9: https://www.apache.org/licenses/LICENSE-2.0
- Apache FAQ de licencias: https://www.apache.org/foundation/license-faq.html
- GitHub, licencias de repositorios: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- Cámara de Diputados, LFPDPPP, consentimiento, excepciones y seguridad: https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf
- Cámara de Diputados, LFT, conciliación prejudicial y excepciones: https://www.diputados.gob.mx/LeyesBiblio/pdf/LFT.pdf
- Cámara de Diputados, CNPCF, implementación y transitorios: https://www.diputados.gob.mx/LeyesBiblio/pdf/CNPCF.pdf

La fecha de consulta no convierte estas fuentes en un catálogo siempre vigente. No existe actualización de fondo ni vigilancia normativa programada por instalar esta skill.
