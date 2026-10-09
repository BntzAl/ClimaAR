import requests

nombre = input("¿Qué ciudad querés buscar? ")

respuesta = requests.get(
    "https://geocoding-api.open-meteo.com/v1/search",
    params={"name": nombre, "count": 5, "language": "es"},
)

datos = respuesta.json()

if "results" in datos:
    resultados = datos["results"]

    for numero, lugar in enumerate(resultados, start=1):
        print(numero, "-", lugar["name"], "|", lugar.get("admin1", "-"), "|", lugar.get("country", "-"))

    eleccion = input("Elegí un número: ")

    if eleccion.isdigit() and 1 <= int(eleccion) <= len(resultados):
        elegido = resultados[int(eleccion) - 1]
        print("Elegiste:", elegido["name"], "| Latitud:", elegido["latitude"], "| Longitud:", elegido["longitude"])
    else:
        print("Opción no válida.")
else:
    print("No encontré ninguna ciudad con ese nombre.")