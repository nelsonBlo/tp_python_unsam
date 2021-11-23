import os
import pandas as pd
import requests
import xarray as xr

directorio_datos_inta = f'{os.path.dirname(os.getcwd())}/tp_python_unsam/archivos_inta'
directorio_datos_nc = f'{os.path.dirname(os.getcwd())}/tp_python_unsam/archivos_nc'


def leer_archivo_xls(id_estacion):
    """Verifica si el directorio de datos (../archivos) existe. Si no existe, lo crea.
    Luego, verifica si el archivo de datos correspondiente a la estación existe en el directorio de datos.
    Si no existe, lo descarga desde el repositorio del INTA, lo guarda en el directorio de datos y lo entrega
    como dataframe de pandas.
    Si ya existe, lo abre y lo entrega como dataframe de pandas.
    """
    ruta_completa = os.path.join(directorio_datos_inta, f'{id_estacion}.xls')
    if not os.path.exists(directorio_datos_inta):
        os.makedirs(directorio_datos_inta)
    if not os.path.isfile(ruta_completa):
        url = f'http://siga2.inta.gov.ar/document/series/{id_estacion}.xls'
        print('Descargando archivo de datos...', '\n')
        r = requests.get(url, allow_redirects=True)
        open(ruta_completa, 'wb').write(r.content)
        print('Abriendo archivo de datos...', '\n')
    return pd.read_excel(ruta_completa)


def leer_nc(fecha):
    """
    Fecha = datetime 'yyyy-mm-dd'
    Verifica si el directorio de datos (../archivos_nc) existe. Si no existe, lo crea.
    Luego, verifica si el archivo de datos correspondiente a esas fechas existe en el directorio de datos.
    Si no existe, lo descarga desde el repositorio de la NOAA, lo guarda en el directorio de datos.
    Abre el dato de cldamt de fecha para el punto (longitud, latitud)"""

    anio = fecha.year
    mes = f'{fecha.month:02d}'
    nombre_archivo = f"ISCCP-Basic.HGM.v01r00.GLOBAL.{anio}.{mes}.99.9999.GPC.10KM.CS00.EA1.00.nc"

    ruta_completa = os.path.join(directorio_datos_nc, nombre_archivo)

    if not os.path.exists(directorio_datos_nc):
        os.makedirs(directorio_datos_nc)

    if not os.path.isfile(ruta_completa):  # descargo el dato
        url = f"https://www.ncei.noaa.gov/data/international-satellite-cloud-climate-project-isccp-h-series-data/access/isccp-basic/hgm/{nombre_archivo}"
        print('Descargando archivo de datos...', '\n')
        r = requests.get(url, allow_redirects=True)
        open(ruta_completa, 'wb').write(r.content)
    return xr.open_dataset(ruta_completa)[["cldamt"]]

