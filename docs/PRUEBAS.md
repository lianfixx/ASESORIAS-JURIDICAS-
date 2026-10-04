# Registro de pruebas

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
