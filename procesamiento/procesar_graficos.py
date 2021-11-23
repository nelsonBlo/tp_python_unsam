import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import cartopy.crs as ccrs
from cartopy.io import shapereader
from shapely.geometry.multipolygon import MultiPolygon

def mapas(ubicacion_inta, ubicacion_satelite):
    """
    Grafica puntos de donde se estima la nubosidad satelital y donde se mide por el inta
    """
    #cargo shape de argentina
    df_paises = gpd.read_file(shapereader.natural_earth('10m', 'cultural', 'admin_0_countries')) # cargo paises de natural_earth con geopandas
    argentina = MultiPolygon([df_paises.loc[df_paises['ADMIN'] == 'Argentina']['geometry'].values[0][0]])  # los paso a multipolygon para poder graficarlos
    
    #defino puntos a marcar
    geometry_1 = [Point(ubicacion_satelite)] #lista con puntos 1
    geometry_2 = [Point((ubicacion_inta[0]+360, ubicacion_inta[1]))] #lista con puntos 2
    
    geodata1 = gpd.GeoDataFrame([ubicacion_satelite], geometry=geometry_1)
    geodata2 = gpd.GeoDataFrame([(ubicacion_inta[0]+360, ubicacion_inta[1])], geometry = geometry_2)
    
    #inicio figura
    fig1 = plt.figure(figsize = [10, 6], dpi = 200)    
    ax = fig1.add_subplot(111, projection = ccrs.PlateCarree(central_longitude = 0)) #seteo proyeccion
    
    #agrego geometrias de fondo: provincias y paises
    ax.add_geometries(argentina, crs = ccrs.PlateCarree(), facecolor = 'none',
                      edgecolor = '0.4', alpha = 0.8)
    
    #grafico puntos
    geodata1.plot(ax = ax, markersize = 20, c = "seagreen") 
    geodata2.plot(ax = ax, markersize = 20, c = "cornflowerblue") 
    
    #seteo ejes
    plt.xticks(np.arange(-61, -53)[::1])
    ax.set_xlabel("Lon")
    plt.yticks(np.arange(-32, -25)[::1])
    ax.set_ylabel("Lat")
    
    #agrego leyenda
    ax.legend(["ISCCP", "INTA"], loc = "lower left", framealpha = 1)
    
    #agrego titulo
    plt.title("Puntos de la estacion del INTA y de grilla de ISCCP a comparar") 
    plt.show()

def ajuste_lineal_simple(x, y):
    """ calcula los coeficientes de la regresion lineal por cuadrados minimos de las variables x, y
    """
    a = np.nansum(((x - x.mean()) * (y - y.mean()))) / np.nansum(((x - x.mean()) ** 2))
    b = y.mean() - a * x.mean()
    return a, b


def scatter(inta_satelital_r, inta_satelital_n, estacion, ubicacion):
    """ Realiza scatter plots de inta_satelital_r e inta_satelital_n y calcula su recta de regresion por
    cuadrados minimos
    """
    a = ajuste_lineal_simple(inta_satelital_r, inta_satelital_n)[0]
    b = ajuste_lineal_simple(inta_satelital_r, inta_satelital_n)[1]
    grilla_x = np.linspace(start=min(inta_satelital_r), stop=max(inta_satelital_r), num=1000)
    grilla_y = grilla_x * a + b
    plt.figure(figsize = [8, 5], dpi = 200)  
    plt.scatter(inta_satelital_r, inta_satelital_n, alpha=0.5)
    plt.title(f'Regresión lineal \n Nubosidad (ISCCP - H {ubicacion[0] - 360, ubicacion[1]}) ~ Radiación {(estacion)}')
    plt.plot(grilla_x, grilla_y, c='red')
    plt.xlabel('Radiación Global ' + r'($W/m^²$)')
    plt.ylabel('Nubosidad (%)')
    plt.annotate(f"Nubosidad ~ {round(a, 2)} * Radiacion + {round(b, 2)}", xy=(grilla_x[100], grilla_y[100]), fontsize=10, weight='bold')
    plt.show()

