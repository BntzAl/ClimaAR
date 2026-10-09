import requests


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


url = "https://api.open-meteo.com/v1/forecast"
parametros = {
    "latitude": -34.68,
    "longitude": -58.34,
    "current": "temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,surface_pressure",
    "timezone": "auto",
}

respuesta = requests.get(url, params=parametros)

if respuesta.status_code == 200:
    datos = respuesta.json()
    actual = datos["current"]

    print("========================")
    print("        CLIMAAR")
    print("========================")
    print("Medición:", actual["time"])
    print("Temperatura:", actual["temperature_2m"], "°C")
    print("Sensación térmica:", actual["apparent_temperature"], "°C")
    print("Humedad:", actual["relative_humidity_2m"], "%")
    print("Viento:", actual["wind_speed_10m"], "km/h")
    print("Presión atmosférica:", actual["surface_pressure"], "hPa")
    print()
    print(describir_temperatura(actual["temperature_2m"]))
    print("Recomendación de ropa:", recomendar_ropa(actual["temperature_2m"]))
else:
    print("Error al pedir los datos. Código:", respuesta.status_code)


parametros_dias = {
    "latitude": -34.68,
    "longitude": -58.34,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
    "timezone": "auto",
}

respuesta_dias = requests.get(url, params=parametros_dias)

if respuesta_dias.status_code == 200:
    diario = respuesta_dias.json()["daily"]

    print()
    print("--- Pronóstico de 7 días ---")
    for i in range(len(diario["time"])):
        print(
            diario["time"][i],
            "| Máx:", diario["temperature_2m_max"][i], "°C",
            "| Mín:", diario["temperature_2m_min"][i], "°C",
            "| Lluvia:", diario["precipitation_probability_max"][i], "%",
            "|",describir_temperatura(diario["temperature_2m_max"][i]),
            "|",recomendar_ropa(diario["temperature_2m_max"][i])
        )
else:
    print("Error al pedir el pronóstico. Código:", respuesta_dias.status_code)