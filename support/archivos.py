import os
import pandas as pd
import requests

directorio_datos = f'{os.path.dirname(os.getcwd())}/archivos'


def leer_archivo(id_estacion):
    """Verifica si el directorio de datos (../archivos) existe. Si no existe, lo crea.
    Luego, verifica si el archivo de datos correspondiente a la estación existe en el directorio de datos.
    Si no existe, lo descarga desde el repositorio del INTA, lo guarda en el directorio de datos y lo entrega
    como dataframe de pandas.
    Si ya existe, lo abre y lo entrega como dataframe de pandas.
    """
    ruta_completa = f'{directorio_datos}/{id_estacion}.xls'
    if not os.path.exists(directorio_datos):
        os.makedirs(directorio_datos)
    if not os.path.isfile(ruta_completa):
        url = f'http://siga2.inta.gov.ar/document/series/{id_estacion}.xls'
        print('Descargando archivo de datos...','\n')
        r = requests.get(url, allow_redirects=True)
        open(ruta_completa, 'wb').write(r.content)
        print('Abriendo archivo de datos...','\n')
    return pd.read_excel(ruta_completa)


# leer archivos nc
import xarray as xr

directorio_datos_nc = f'{os.path.dirname(os.getcwd())}/python_unsam/tp_python_unsam/archivos_nc'

def leer_archivo_nc(fecha, longitud, latitud):
    """
    Fecha = str 'yyyy-mm-dd'
    Verifica si el directorio de datos (../archivos_nc) existe. Si no existe, lo crea.
    Luego, verifica si el archivo de datos correspondiente a esas fechas existe en el directorio de datos.
    Si no existe, lo descarga desde el repositorio de la NOAA, lo guarda en el directorio de datos.
    Abre el dato del nc de fecha para el punto (longitud, latitud)"""
    
    #fecha_dt = datetime.datetime.strptime(fecha, "%Y-%m-%d")
    anio = fecha.year
    mes = fecha.month
    
    if len(str(mes))== 1: #si es un mes de un digito, agrego 0 antes del mes
        nombre_archivo = f"ISCCP-Basic.HGM.v01r00.GLOBAL.{anio}.0{mes}.99.9999.GPC.10KM.CS00.EA1.00.nc"
    else: #sino no
        nombre_archivo = f"ISCCP-Basic.HGM.v01r00.GLOBAL.{anio}.{mes}.99.9999.GPC.10KM.CS00.EA1.00.nc"
    
    ruta_completa = os.path.join(directorio_datos_nc, nombre_archivo)
    
    if not os.path.exists(directorio_datos_nc):
        os.makedirs(directorio_datos_nc)
    
    if not os.path.isfile(ruta_completa): #descargo el dato 
        url = f"https://www.ncei.noaa.gov/data/international-satellite-cloud-climate-project-isccp-h-series-data/access/isccp-basic/hgm/{nombre_archivo}"
        print('Descargando archivo de datos...','\n')
        r = requests.get(url, allow_redirects=True)
        open(ruta_completa, 'wb').write(r.content)        
    
    data = xr.open_dataset(ruta_completa)[["cldamt"]].loc[dict(lon = longitud,lat = latitud)] #abro el archivo, selecciono solo la variable "cldamt" y selecciono el punto de lon y lat a usar 
    return(data)
