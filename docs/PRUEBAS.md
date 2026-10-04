# Registro de pruebas

## Edición 0.2.1 — revisión de claridad de licencia

Se partió de la fuente cuyo árbol Git coincide con `12d41530e9beaab9047b9d14964539beb9b69df1`, integrado en la rama principal para 0.2.0. Se revisó la explicación publicada y se contrastó con Apache License 2.0, su FAQ oficial y la documentación de licencias de GitHub. LICENSE y NOTICE permanecen sin cambios. No se cambian los permisos ni se revocan licencias anteriores.

Las 88 pruebas técnicas de partida se ejecutaron satisfactoriamente. Tras la revisión, se ejecutaron **90 pruebas técnicas locales, todas satisfactorias**, incluidas dos comprobaciones nuevas: identidad de las explicaciones de licencia y bloqueo del paquete si divergen. La validación comprueba coherencia, no interpreta jurídicamente el texto. La ejecución de GitHub debe consultarse por commit; no se presupone su resultado.

No se alteró la plantilla Word ni se repitió su auditoría visual; la revisión visual de seis páginas corresponde a 0.2.0. Tampoco se añadieron pruebas de otros asistentes, una auditoría jurídica integral o controles de protección de rama. Los límites y pendientes de la auditoría anterior continúan aplicando. El esquema del estado sigue siendo 2; una actualización documental no genera aprobaciones ni acredita nuevas revisiones de asuntos.

## Edición 0.2.0

Ejecución local real del 4 de octubre de 2026, Python 3.13.5: **88 pruebas técnicas, todas satisfactorias**. Se conservaron los 44 tests originales, corrigiendo el test de duración para leer el guion, y se añadieron 44 pruebas de regresión de entradas, permisos registrados, integridad y distribución.

Además se aplicaron 1534 mutaciones estructurales a un estado sintético sin excepciones no controladas. La cobertura no es exhaustiva. Se generó la plantilla Word en blanco con python-docx 1.2.0, se renderizó a seis páginas y se revisaron visualmente todas ellas; no se observaron recortes ni solapamientos. No se revisó un documento cumplimentado de cliente.

CI se ejecuta para cada cambio publicado. Su estado debe consultarse en la ejecución del commit o PR concreto; un resultado local no se presenta como resultado remoto. No se atribuye una aprobación jurídica a CI. Comandos reproducibles:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build.py --output /ruta/vacia
```

## Antecedente 0.1.0

La suite histórica tenía 44 tests; se volvió a ejecutar localmente antes de modificar la fuente y pasó. Las pruebas adversas de esta auditoría detectaron defectos fuera de esa cobertura. Consultar AUDITORIA_0.2.0.md.

## Evaluación conductual pendiente

`assets/evaluaciones.json` contiene 28 escenarios sintéticos para revisión de respuestas, no 28 resultados de asistentes. Cualquier fallo crítico bloquea aprobación. No se ejecutaron esos escenarios en otras cuentas o productos.
