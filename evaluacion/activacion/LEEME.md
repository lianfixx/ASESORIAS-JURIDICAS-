# Prueba de activación de la descripción

`consultas.json` contiene 21 consultas inventadas: 10 que deberían activar la skill (casos de despacho: pensión, despido, honorarios, acuses, retomar un asunto) y 11 cercanas que **no** deberían (tareas escolares, teoría jurídica, plantillas genéricas, discursos, sitios web, correos personales). No hay datos de clientes.

`prueba_activacion.py` instala la skill en un directorio temporal, cambia sólo su `description` por cada candidata y lanza `claude -p` con la consulta tal cual (sin nombrar la skill), contando si se invoca la herramienta Skill. Es una prueba local, consume cuota del CLI y no corre en CI. Si el CLI devuelve «session limit», las cifras no valen: comprueba una consulta suelta antes de leer resultados.

Uso: `python3 evaluacion/activacion/prueba_activacion.py candidatas.json 2 resultados.json`, donde `candidatas.json` es `{"nombre": "texto de la descripción", ...}`.
