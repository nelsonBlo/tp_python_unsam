from tp_python_unsam.support import estaciones_inta
from tp_python_unsam.support import archivos

estacion_id = input('Ingrese el id de la estación INTA: ')

ubicacion = estaciones_inta.EstacionInta(estacion_id).ubicacion()

print('Las coordenadas de la estación son (Latitud, longitud): ', ubicacion, '\n')

datos = archivos.leer_archivo(estacion_id)
print('Los datos de la estación son :\n', datos)
