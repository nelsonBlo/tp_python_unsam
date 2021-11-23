#data_nc.py

class DataNC():
    """clase para datos satelitales
    """
    def __init__(self, data):
        self.data = data
        self.longitud = None
        self.latitud = None  
        self.nubosidad_punto = None
    
    def longitudes(self):
        self.longitud = self.data.lon.values
        return self.longitud
    
    def latitudes(self):
        self.latitud = self.data.lat.values
        return self.latitud
    
    def leer_nubosidad_punto(self, longitud, latitud):
        self.nubosidad_punto = self.data.loc[dict(lon=longitud, lat=latitud)]["cldamt"].values[0]
        return self.nubosidad_punto