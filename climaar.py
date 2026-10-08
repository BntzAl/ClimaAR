import json
import os
import requests

URL = "https://api.open-meteo.com/v1/forecast"
URL_BUSQUEDA = "https://geocoding-api.open-meteo.com/v1/search"
ARCHIVO_FAVORITAS = "favoritas.json"


def describir_temperatura(temp):
    if temp < 10:
        return "Hace frío"
    elif temp < 20:
        return "Está fresco"
    else:
        return "Hace calor"


def recomendar_ropa(temp):
    if temp < 10:
        return "Abrigate bien"
    elif temp < 20:
        return "Llevá una campera ligera"
    else:
        return "Podés usar ropa ligera"


def pedir_numero(maximo):
    texto = input("Elegí un número: ")
    if texto.isdigit() and 1 <= int(texto) <= maximo:
        return int(texto)
    print("Opción no válida.")
    return None


def buscar_ciudad():
    nombre = input("¿Qué ciudad querés buscar? ")
    respuesta = requests.get(
        URL_BUSQUEDA,
        params={"name": nombre, "count": 5, "language": "es"},
    )
    if respuesta.status_code != 200:
        print("Error al buscar la ciudad. Código:", respuesta.status_code)
        return None

    datos = respuesta.json()
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
    respuesta = requests.get(URL, params=parametros)
    if respuesta.status_code == 200:
        return respuesta.json()
    print("Error al pedir los datos. Código:", respuesta.status_code)
    return None


def obtener_clima_actual(latitud, longitud):
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,surface_pressure",
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
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,apparent_temperature_max",
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
    print("Medición:", actual["time"])
    print("Temperatura:", actual["temperature_2m"], "°C")
    print("Sensación térmica:", actual["apparent_temperature"], "°C")
    print("Humedad:", actual["relative_humidity_2m"], "%")
    print("Viento:", actual["wind_speed_10m"], "km/h")
    print("Presión atmosférica:", actual["surface_pressure"], "hPa")
    print()
    print(describir_temperatura(actual["temperature_2m"]))
    print("Recomendación de ropa:", recomendar_ropa(actual["apparent_temperature"]))


def mostrar_pronostico(diario):
    print()
    print("--- Pronóstico de 7 días ---")
    for i in range(len(diario["time"])):
        print(
            diario["time"][i],
            "| Máx:", diario["temperature_2m_max"][i], "°C",
            "| Mín:", diario["temperature_2m_min"][i], "°C",
            "| Lluvia:", diario["precipitation_probability_max"][i], "%",
            "| Sens:", diario["apparent_temperature_max"][i], "°C",
            "|", describir_temperatura(diario["temperature_2m_max"][i]),
            "|", recomendar_ropa(diario["apparent_temperature_max"][i]),
        )


print("1 - Buscar una ciudad")
print("2 - Ver mis favoritas")
opcion = input("¿Qué querés hacer? ")

ciudad = None
es_nueva = False

if opcion == "1":
    ciudad = buscar_ciudad()
    es_nueva = True
elif opcion == "2":
    ciudad = elegir_favorita()
else:
    print("Opción no válida.")

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
        respuesta = input("¿Querés guardarla en favoritas? (s/n) ")
        if respuesta.lower() == "s":
            agregar_favorita(ciudad)