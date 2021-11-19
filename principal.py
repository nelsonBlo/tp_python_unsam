import datetime

import numpy as np
import pandas as pd

from support import estaciones_inta, data_nc 
from support import archivos
from procesamiento import procesar_datos_pandas


inicio_periodo = '1983-07-01'
fin_periodo = '2017-06-01'


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
    lon = longitud_satelite[diferencia_longitudes == diferencia_longitudes.min()]
    lat = latitud_satelite[diferencia_latitudes == diferencia_latitudes.min()]
    print(f'\n El punto de satélite más cercano a la estación es: {lon[0]-360, lat[0]}')
    return lon[0], lat[0]

###
#longitud_satelite = archivos.leer_grilla_nc(datetime.datetime(1984, 1, 1))[0]  # ejemplo
#latitud_satelite = archivos.leer_grilla_nc(datetime.datetime(1984, 1, 1))[1]  # ejemplo

data = data_nc.DataNC(archivos.leer_nc(datetime.datetime(1984, 1, 1)))
longitud_satelite = data.longitudes()
latitud_satelite = data.latitudes()

ubicacion_satelite = punto_cercano(ubicacion, latitud_satelite, longitud_satelite)

def abre_y_acomoda_nc(inicio_periodo, fin_periodo, longitud, latitud):
    """
    Abre archivos nc y los acomoda en un array3D?
    """
    fechas = pd.date_range(start=inicio_periodo, end=fin_periodo, freq="M")
    serie = [data_nc.DataNC(archivos.leer_nc(fecha)).leer_nubosidad_punto(longitud, latitud) for fecha in fechas]
    panda_serie = pd.DataFrame(serie, index=fechas, columns=["ISCCP"])
    return panda_serie


# print(punto_cercano(ubicacion, longitud, latitud, ))

print(abre_y_acomoda_nc(inicio_periodo, fin_periodo, ubicacion_satelite[0], ubicacion_satelite[1]))

#%%
### borradores: ####
#%% Uno data frames de salida y los grafico
### DEJARLO LINDO, poner etiqueta con funcion que relaciona estas variables. ARMAR FUNCIONES APARTE ###
import pandas as pd

inta = pd.DataFrame(obtener_datos_estacion_inta(estacion_id)[0])
satelital =  abre_y_acomoda_nc(inicio_periodo, fin_periodo, ubicacion_satelite[0], ubicacion_satelite[1])

inta_satelital = pd.concat([inta['Radiacion_Global'], satelital["ISCCP"]], axis = 1)

def ajuste_lineal_simple(x,y):
    a = np.nansum(((x - x.mean())*(y-y.mean()))) / np.nansum(((x-x.mean())**2))
    b = y.mean() - a*x.mean()
    return a, b

a, b = ajuste_lineal_simple(inta_satelital['Radiacion_Global'], inta_satelital["ISCCP"])
grilla_x = np.linspace(start = min(inta_satelital['Radiacion_Global']), stop = max(inta_satelital['Radiacion_Global']), num = 1000)
grilla_y = grilla_x*a + b

import matplotlib.pyplot as plt
plt.scatter(inta_satelital['Radiacion_Global'], inta_satelital["ISCCP"] )
plt.title('y ajuste lineal')
plt.plot(grilla_x, grilla_y, c = 'green')
plt.xlabel('x')
plt.ylabel('y')

#%% Grafico mapa 
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
from cartopy.io import shapereader
from shapely.geometry.multipolygon import MultiPolygon

df_paises = gpd.read_file(shapereader.natural_earth('10m', 'cultural', 'admin_0_countries')) # cargo paises de natural_earth con geopandas
argentina = MultiPolygon([df_paises.loc[df_paises['ADMIN'] == 'Argentina']['geometry'].values[0][0]])  # los paso a multipolygon para poder graficarlos
   
def grafico_puntos(punto_satelital, punto_inta, shape_paises):
    """
    Grafica puntos de donde se estima la nubosidad satelital y donde se mide por el inta

    """
    #defino puntos a marcar
    geometry_1 = [Point(punto_satelital)] #lista con puntos 1
    geometry_2 = [Point(punto_inta)] #lista con puntos 2
    
    geodata1 = gpd.GeoDataFrame([punto_satelital], geometry=geometry_1)
    geodata2 = gpd.GeoDataFrame([punto_inta], geometry = geometry_2)
    
    #inicio figura
    fig1 = plt.figure(figsize = [10, 6], dpi = 200)    
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(shape_paises, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.4', alpha = 0.8)
    
    #grafico puntos
    geodata1.plot(ax = ax, markersize = 20, c = "seagreen") 
    geodata2.plot(ax = ax, markersize = 20, c = "cornflowerblue") 
    
    #seteo ejes
    ax.set_xticklabels(np.arange(-61, -53)[::1])
    plt.xticks(np.arange(-61, -53)[::1])
    ax.set_xlabel("Lon")
    ax.set_yticklabels(np.arange(-32, -25)[::1])
    plt.yticks(np.arange(-32, -25)[::1])
    ax.set_ylabel("Lat")
    
    #agrego leyenda
    #ax.legend(["ISCCP","SMN", "SMN calibration"], loc = "lower left")
    ax.legend(["ISCCP", "INTA"], loc = "lower left", framealpha = 1)
    
    #agrego etiquetas con numeros de estacion
    #list_smn_etiquetas = [(lon-360, lat) for lon, lat in list(dict_puntos_smn.values())]
    #for i, clave in enumerate(dict_puntos_smn):
     #   ax.annotate(str(clave), list_smn_etiquetas[i], size = 8, weight='bold')
    
    #agrego titulo
    plt.title("Punto satelite e INTA")
    
    plt.show()

grafico_puntos(ubicacion_satelite, (ubicacion[1]+360, ubicacion[0]), argentina)