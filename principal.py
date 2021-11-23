import datetime
import pandas as pd

from support import estaciones_inta, data_nc
from support import archivos
from procesamiento import procesar_datos_pandas
from procesamiento import procesar_datos_satelite
from procesamiento import procesar_graficos

inicio_periodo = '1983-07-01'
fin_periodo = '2017-06-01'

estacion_id = input('Ingrese el id de la estación INTA: ')

def obtener_datos_estacion_inta(estacion_id):
    ubicacion = estaciones_inta.EstacionInta(estacion_id).ubicacion()
    if ubicacion is None:
        return None
    else:
        datos = archivos.leer_archivo_xls(estacion_id)
        subset = procesar_datos_pandas.obtener_promedios_mensual_inta(datos, inicio_periodo, fin_periodo)
        return subset, ubicacion

if obtener_datos_estacion_inta(estacion_id):
    #datos INTA radiacion
    ubicacion_inta = estaciones_inta.EstacionInta(estacion_id).ubicacion()
    inta = pd.DataFrame(obtener_datos_estacion_inta(estacion_id)[0])
    print(f' \n La ubicación de la estación es: {ubicacion_inta} y la información de radiación media mensual viene dada por: \n  \n {inta.head()} \n ')

    #datos ISCCP-H nubosidad: grilla
    data = data_nc.DataNC(archivos.leer_nc(datetime.datetime(1984, 1, 1)))
    longitudes_satelite = data.longitudes()
    latitudes_satelite = data.latitudes()
    
    #busca el punto de satelite mas cercano a la estacion INTA: 
    ubicacion_satelite = procesar_datos_satelite.punto_cercano(ubicacion_inta, latitudes_satelite, longitudes_satelite)
    
    #arma serie temporal de nubosidad de ISCCP-H en el punto mas cercano a la estacion INTA
    satelital = procesar_datos_satelite.abre_y_acomoda_nc(inicio_periodo, fin_periodo, ubicacion_satelite[0],
                                                          ubicacion_satelite[1])
    print(f" \n La informacion de nubosidad media mensual satelital viene dada por: \n {satelital.head()}")
    
    print(f" \n Se analiza la relación entre la radiación media mensual de la estacion del INTA y la cobertura nubosa media del punto de ISCCP-H:\n")
    procesar_graficos.mapas(ubicacion_inta, ubicacion_satelite)
    
    print(" \n Esta relación queda determinada por: \n ")    
    procesar_graficos.scatter(inta['Radiacion_Global'], satelital["ISCCP"], estacion_id, ubicacion_satelite)
else:
    print('No se encontró la estación.')
