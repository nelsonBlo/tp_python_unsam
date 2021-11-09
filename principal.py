from tp_python_unsam.support import estaciones_inta
from tp_python_unsam.support import archivos
from tp_python_unsam.procesamiento import procesar_datos_pandas

inicio_periodo = '1983-01-01'
fin_periodo = '2017-12-01'


def obtener_datos_estacion_inta(estacion_id):
    if ubicacion is None:
        print('No se encontró la estación.')
        return None
    else:
        datos = archivos.leer_archivo(estacion_id)
        subset = procesar_datos_pandas.obtener_promedios_mensual_inta(datos, inicio_periodo, fin_periodo)
        return subset, ubicacion


estacion_id = input('Ingrese el id de la estación INTA: ')
ubicacion = estaciones_inta.EstacionInta(estacion_id).ubicacion()
# list=obtener_datos_estacion_inta(estacion_id)
# print(obtener_datos_estacion_inta(estacion_id))
print(obtener_datos_estacion_inta(estacion_id))
