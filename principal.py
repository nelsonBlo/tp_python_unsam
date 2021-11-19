import datetime

import numpy as np
import pandas as pd

from support import estaciones_inta
from support import archivos
from procesamiento import procesar_datos_pandas

inicio_periodo = '1983-07-01'
fin_periodo = '1983-10-01'


def obtener_datos_estacion_inta(estacion_id):
    if ubicacion is None:
        print('No se encontró la estación.')
        return None
    else:
        datos = archivos.leer_archivo_xls(estacion_id)
        subset = procesar_datos_pandas.obtener_promedios_mensual_inta(datos, inicio_periodo, fin_periodo)
        return subset, ubicacion


estacion_id = input('Ingrese el id de la estación INTA: ')
ubicacion = estaciones_inta.EstacionInta(estacion_id).ubicacion()
# list=obtener_datos_estacion_inta(estacion_id)
# print(obtener_datos_estacion_inta(estacion_id))
print(obtener_datos_estacion_inta(estacion_id))


###
# obtener lon y lat cercanas a punto inta
def punto_cercano(ubicacion, latitud_satelite, longitud_satelite):
    longitud_satelite = np.array(longitud_satelite)
    latitud_satelite = np.array(latitud_satelite)

    diferencia_longitudes = abs(longitud_satelite - (ubicacion[1] + 360))
    diferencia_latitudes = abs(latitud_satelite - ubicacion[0])
    long = longitud_satelite[diferencia_longitudes == diferencia_longitudes.min()]
    lat = latitud_satelite[diferencia_latitudes == diferencia_latitudes.min()]
    print(f'el punto más cercano a la estación es: {long-360, lat}')
    return long, lat

###
longitud_satelite = archivos.leer_grilla_nc(datetime.datetime(1984, 1, 1))[0]  # ejemplo
latitud_satelite = archivos.leer_grilla_nc(datetime.datetime(1984, 1, 1))[1]  # ejemplo

ubicacion_satelite = punto_cercano(ubicacion, latitud_satelite, longitud_satelite)


def abre_y_acomoda_nc(inicio_periodo, fin_periodo, longitud, latitud):
    """
    Abre archivos nc y los acomoda en un array3D?
    """
    fechas = pd.date_range(start=inicio_periodo, end=fin_periodo, freq="M")
    serie = [archivos.leer_nubosidad_nc(fecha, longitud, latitud)[0] for fecha in fechas]
    panda_serie = pd.DataFrame(serie, index=fechas, columns=["ISCCP"])
    return panda_serie


# print(punto_cercano(ubicacion, longitud, latitud, ))

print(abre_y_acomoda_nc(inicio_periodo, fin_periodo, ubicacion_satelite[0], ubicacion_satelite[1]))
