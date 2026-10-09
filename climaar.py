import json
import os
import requests

URL = "https://api.open-meteo.com/v1/forecast"
URL_BUSQUEDA = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVO_FAVORITAS = "favoritas.json"
CODIGOS_CLIMA = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna leve",
    53: "Llovizna moderada",
    55: "Llovizna intensa",
    56: "Llovizna helada",
    57: "Llovizna helada",
    61: "Lluvia leve",
    63: "Lluvia moderada",
    65: "Lluvia fuerte",
    66: "Lluvia helada",
    67: "Lluvia helada",
    71: "Nevada leve",
    73: "Nevada moderada",
    75: "Nevada fuerte",
    77: "Granos de nieve",
    80: "Chubascos leves",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    85: "Chubascos de nieve leves",
    86: "Chubascos de nieve fuertes",
    95: "Tormenta",
    96: "Tormenta con granizo",
    99: "Tormenta con granizo fuerte",
}


def pedir_numero(maximo):
    texto = input("Elegí un número: ")
    if texto.isdigit() and 1 <= int(texto) <= maximo:
        return int(texto)
    print("Opción no válida.")
    return None

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


def buscar_ciudad():
    nombre = input("¿Qué ciudad querés buscar? ")
    datos = hacer_peticion(URL_BUSQUEDA, {"name": nombre, "count": 5, "language": "es"})
    if datos is None:
        return None

    if "results" not in datos:
        print("No encontré ninguna ciudad con ese nombre.")
        return None

    resultados = datos["results"]
    for numero, lugar in enumerate(resultados, start=1):
        print(numero, "-", lugar["name"], "|", lugar.get("admin1", "-"), "|", lugar.get("country", "-"))

    numero = pedir_numero(len(resultados))
    if numero is None:
        return None
    return resultados[numero - 1]


def cargar_favoritas():
    if not os.path.exists(ARCHIVO_FAVORITAS):
        return []
    with open(ARCHIVO_FAVORITAS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_favoritas(favoritas):
    with open(ARCHIVO_FAVORITAS, "w", encoding="utf-8") as archivo:
        json.dump(favoritas, archivo, ensure_ascii=False, indent=2)


def elegir_favorita():
    favoritas = cargar_favoritas()
    if len(favoritas) == 0:
        print("Todavía no tenés ciudades favoritas.")
        return None

    for numero, lugar in enumerate(favoritas, start=1):
        print(numero, "-", lugar["name"], "|", lugar["admin1"])

    numero = pedir_numero(len(favoritas))
    if numero is None:
        return None
    return favoritas[numero - 1]

def eliminar_favorita():
    favoritas = cargar_favoritas()
    if len(favoritas) == 0:
        print("Todavía no tenés ciudades favoritas.")
        return

    for numero, lugar in enumerate(favoritas, start=1):
        print(numero, "-", lugar["name"], "|", lugar["admin1"])

    numero = pedir_numero(len(favoritas))
    if numero is None:
        return

    eliminada = favoritas.pop(numero - 1)

    guardar_favoritas(favoritas)

    print("Se eliminó", eliminada["name"])

def menu_favoritas():
    print()
    print("--- Mis Favoritas ---")
    print("1 - Consultar una ciudad")
    print("2 - Eliminar una ciudad")
    print("3 - Volver")

    opcion = input("¿Qué querés hacer? ")

    if opcion == "1":
        return elegir_favorita()
    elif opcion == "2":
        eliminar_favorita()
        return None
    elif opcion == "3":
        return None
    else:
        print("La opción no es válida.")
        return None

def agregar_favorita(ciudad):
    favoritas = cargar_favoritas()
    for lugar in favoritas:
        if lugar["latitude"] == ciudad["latitude"] and lugar["longitude"] == ciudad["longitude"]:
            print("Esa ciudad ya está en tus favoritas.")
            return

    favoritas.append({
        "name": ciudad["name"],
        "admin1": ciudad.get("admin1", "-"),
        "latitude": ciudad["latitude"],
        "longitude": ciudad["longitude"],
    })
    guardar_favoritas(favoritas)
    print("Guardada en favoritas.")


def pedir_datos(parametros):
    return hacer_peticion(URL, parametros)

def describir_clima(codigo):
    return CODIGOS_CLIMA.get(codigo, "Desconocido")

def obtener_clima_actual(latitud, longitud):
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,surface_pressure,weather_code",
        "timezone": "auto",
    }
    datos = pedir_datos(parametros)
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
    datos = pedir_datos(parametros)
    if datos is None:
        return None
    return datos["daily"]


def mostrar_clima_actual(actual, ciudad):
    print()
    print("========================")
    print("        CLIMAAR")
    print("========================")
    print("Ubicación:", ciudad["name"], "|", ciudad.get("admin1", "-"))
    print("Estado:", describir_clima(actual["weather_code"]))
    print("Medición:", actual["time"].replace("T", " "))
    print()
    print("--- Condiciones actuales ---")
    print("Temperatura:", actual["temperature_2m"], "°C")
    print("Sensación térmica:", actual["apparent_temperature"], "°C")
    print("Humedad:", actual["relative_humidity_2m"], "%")
    print("Viento:", actual["wind_speed_10m"], "km/h")
    print("Presión atmosférica:", actual["surface_pressure"], "hPa")
    print()


def mostrar_pronostico(diario):
    print()
    print("--- Pronóstico de 7 días ---")

    for i in range(len(diario["time"])):
        print()
        print(diario["time"][i])
        print("Máxima:", diario["temperature_2m_max"][i], "°C")
        print("Mínima:", diario["temperature_2m_min"][i], "°C")
        print("Sensación térmica máxima:", diario["apparent_temperature_max"][i], "°C")
        print("Probabilidad de lluvia:", diario["precipitation_probability_max"][i], "%")
        print("Estado:", describir_clima(diario["weather_code"][i]))
        print("----------------------")

while True:
    print()
    print("--- ClimaAR ---")
    print("1 - Buscar una ciudad")
    print("2 - Ver mis favoritas")
    print("3 - Salir")

    opcion = input("¿Qué querés hacer? ")

    ciudad = None
    es_nueva = False

    if opcion == "1":
        ciudad = buscar_ciudad()
        es_nueva = True

    elif opcion == "2":
        ciudad = menu_favoritas()

    elif opcion == "3":
        print("¡Hasta luego!")
        break

    else:
        print("La opción no es válida.")

    if ciudad is not None:
        latitud = ciudad["latitude"]
        longitud = ciudad["longitude"]

        actual = obtener_clima_actual(latitud, longitud)
        if actual is not None:
            mostrar_clima_actual(actual, ciudad)

        diario = obtener_pronostico(latitud, longitud)
        if diario is not None:
            mostrar_pronostico(diario)

        if es_nueva:
            print()
            respuesta = input("¿Querés guardar esta ciudad en tus favoritas? (s/n) ")
            if respuesta.lower() == "s":
                agregar_favorita(ciudad)