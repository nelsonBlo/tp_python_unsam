import numpy as np
import pandas as pd
import datetime
from support import data_nc, archivos
from tqdm import tqdm


def punto_cercano(ubicacion, latitud_satelite, longitud_satelite):
    """ calcula la ubicacion del punto de satelite mas cercano a ubicacion """
    longitud_satelite = np.array(longitud_satelite)
    latitud_satelite = np.array(latitud_satelite)

    diferencia_longitudes = abs(longitud_satelite - (ubicacion[0] + 360))
    diferencia_latitudes = abs(latitud_satelite - ubicacion[1])
    lon = longitud_satelite[diferencia_longitudes == diferencia_longitudes.min()]
    lat = latitud_satelite[diferencia_latitudes == diferencia_latitudes.min()]
    print(f'\n El punto de satélite más cercano a la estación es: {lon[0] - 360, lat[0]}')
    return lon[0], lat[0]


def abre_y_acomoda_nc(inicio_periodo, fin_periodo, longitud, latitud):
    """
    Abre archivos nc y los acomoda en una panda serie de los valores de nubosidad dentro del rango de fechas
    """
    print(f" \n Los datos de nubosidad del punto ({longitud-360}, {latitud}) se estan procesando, esto puede demorar...")
    fechas = pd.date_range(start=inicio_periodo, end=fin_periodo, freq="M")
    serie = [data_nc.DataNC(archivos.leer_nc(fecha)).leer_nubosidad_punto(longitud, latitud) for fecha in tqdm(fechas)]
    panda_serie = pd.DataFrame(serie, index=fechas, columns=["ISCCP"])
    return panda_serie
