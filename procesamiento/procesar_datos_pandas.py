import pandas as pd


def obtener_promedios_mensual_inta(datos, inicio_periodo, fin_periodo):
    """ calcula la media mensual de los datos en el periodo dado por inicio_periodo y fin_periodo
    """
    datos['Fecha'] = pd.to_datetime(datos['Fecha'])
    subset_datos = datos[(datos['Fecha'] > inicio_periodo) & (datos['Fecha'] < fin_periodo)]
    subset_datos_promedio = subset_datos.groupby(pd.Grouper(key='Fecha', freq='1M')).mean()['Radiacion_Global']
    return subset_datos_promedio
