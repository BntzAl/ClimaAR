import requests

from config import URL, URL_BUSQUEDA, CODIGOS_CLIMA


def hacer_peticion(url, parametros):
    try:
        respuesta = requests.get(url, params=parametros, timeout=10)
    except requests.exceptions.Timeout:
        print("La conexión demoró demasiado. Volvé a intentarlo en unos minutos.")
        return None
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar al servidor. Revisá tu conexión a internet.")
        return None

    if respuesta.status_code != 200:
        print("Error en el servicio. Código:", respuesta.status_code)
        return None

    return respuesta.json()


def buscar_ciudades(nombre):
    # Devuelve None si hubo un error, una lista vacía si no encontró nada,
    # o la lista de ciudades encontradas.
    datos = hacer_peticion(URL_BUSQUEDA, {"name": nombre, "count": 5, "language": "es"})
    if datos is None:
        return None
    return datos.get("results", [])


def describir_clima(codigo):
    return CODIGOS_CLIMA.get(codigo, "Desconocido")


def obtener_clima_actual(latitud, longitud):
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,surface_pressure,weather_code",
        "timezone": "auto",
    }
    datos = hacer_peticion(URL, parametros)
    if datos is None:
        return None
    return datos["current"]


def obtener_pronostico(latitud, longitud):
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,apparent_temperature_max,weather_code",
        "timezone": "auto",
    }
    datos = hacer_peticion(URL, parametros)
    if datos is None:
        return None
    return datos["daily"]