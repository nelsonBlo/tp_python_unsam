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
