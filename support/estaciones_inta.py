import requests

main_url='http://siga2.inta.gov.ar/js/main.js'
uri = "http://siga2.inta.gov.ar/valor.php?param_type=estacion&param_value="


class EstacionInta():
    def __init__(self, estacion_id):
        self.estacion_id = estacion_id
        self.data = None
        self.obtener()

    def obtener(self):
        response = requests.get(self.__obtener_uri())
        self.data = response.json()

    def ubicacion(self):
        """Devuelve una tupla con la ubicación de la estación: (latitud, longitud)"""
        for estacion in self.data:
            if self.estacion_id == estacion['idInterno']:
                return estacion['latitud'], estacion['longitud']
        return None

    def latitud(self):
        for estacion in self.data:
            if self.estacion_id == estacion['idInterno']:
                return estacion['latitud']
        return None

    def longitud(self):
        for estacion in self.data:
            if self.estacion_id == estacion['idInterno']:
                return estacion['longitud']
        return None

    def nombre(self):
        for estacion in self.data:
            if self.estacion_id == estacion['idInterno']:
                return estacion['nombre']
        return None

    def __obtener_uri(self):
        response = requests.get(main_url)
        response_text = response.text
        value = response_text[response.text.rfind('$http.get(') + 11:response.text.find('.php')]
        return uri.replace('valor', value)
