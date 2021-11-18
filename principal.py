import pandas as pd

from tp_python_unsam.support import estaciones_inta
from tp_python_unsam.support import archivos 
from tp_python_unsam.procesamiento import procesar_datos_pandas

inicio_periodo = '1983-07-01'
fin_periodo = '2017-06-01'


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

###
#obtener lon y lat cercanas a punto inta
###

longitud = 300.5 #ejemplo
latitud = -27.5 #ejemplo

def abre_y_acomoda_nc(inicio_periodo, fin_periodo, longitud, latitud):
    """
    Abre archivos nc y los acomoda en un array3D?
    """
    fechas = pd.date_range(start=inicio_periodo, end= fin_periodo, freq="M")
    serie = [archivos.leer_archivo_nc(fecha, longitud, latitud)["cldamt"].values[0] for fecha in fechas]
    panda_serie = pd.DataFrame(serie, index = fechas, columns = ["ISCCP"])
    return panda_serie

print(abre_y_acomoda_nc(inicio_periodo, fin_periodo, longitud, latitud))