# tp_python_unsam

Objetivo del trabajo:

Determinar si las estimaciones del porcentaje de cobertura nubosa media mensual satelital
de la base de datos ISCCP-H* son representativas de la nubosidad en superficie en el
Noreste Argentino.

Integrantes del grupo:

Nadia Testani, nadiatestani@gmail.com
Agustina Quiros, agustinaqr@gmail.com
Nelson Bocanegra Lopez, nelsonblopez@gmail.com


Metodología:

Se validarán las estimaciones del porcentaje de cobertura nubosa media mensual satelital
de la base de datos ISCCP-H* con datos de radiación en superficie tomados en estaciones
meteorológicas convencionales de la red INTA** en el Noreste Argentino. Se analizará la
correlación entre series temporales de estas dos variables en puntos de medición/
estimación cercanos, esperando que la misma exista y, en particular, que sea negativa.

* https://www.ncei.noaa.gov/products/international-satellite-cloud-climatology
** http://siga2.inta.gov.ar/#


Instalación:
1. Se recomienda utilizar un Entorno Virtual de Python.
2. Instalar las librerías requeridas con: 'pip install -r requirements.txt'


Ejecución:
1. Ejecutar el archivo 'procesar_datos.py'