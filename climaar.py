from api import buscar_ciudades, obtener_clima_actual, obtener_pronostico, describir_clima
from favoritas import cargar_favoritas, agregar_favorita, eliminar_favorita


def pedir_numero(maximo):
    texto = input("Elegí un número: ")
    if texto.isdigit() and 1 <= int(texto) <= maximo:
        return int(texto)
    print("Opción no válida.")
    return None


def buscar_ciudad():
    nombre = input("¿Qué ciudad querés buscar? ")
    resultados = buscar_ciudades(nombre)
    if resultados is None:
        return None
    if len(resultados) == 0:
        print("No encontré ninguna ciudad con ese nombre.")
        return None

    for numero, lugar in enumerate(resultados, start=1):
        print(numero, "-", lugar["name"], "|", lugar.get("admin1", "-"), "|", lugar.get("country", "-"))

    numero = pedir_numero(len(resultados))
    if numero is None:
        return None
    return resultados[numero - 1]


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


def quitar_favorita():
    favoritas = cargar_favoritas()
    if len(favoritas) == 0:
        print("Todavía no tenés ciudades favoritas.")
        return

    for numero, lugar in enumerate(favoritas, start=1):
        print(numero, "-", lugar["name"], "|", lugar["admin1"])

    numero = pedir_numero(len(favoritas))
    if numero is None:
        return

    eliminada = eliminar_favorita(numero - 1)
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
        quitar_favorita()
        return None
    elif opcion == "3":
        return None
    else:
        print("La opción no es válida.")
        return None


def ofrecer_guardar(ciudad):
    print()
    respuesta = input("¿Querés guardar esta ciudad en tus favoritas? (s/n) ")
    if respuesta.lower() == "s":
        if agregar_favorita(ciudad):
            print("Guardada en favoritas.")
        else:
            print("Esa ciudad ya está en tus favoritas.")


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


def mostrar_clima(ciudad):
    latitud = ciudad["latitude"]
    longitud = ciudad["longitude"]

    actual = obtener_clima_actual(latitud, longitud)
    if actual is not None:
        mostrar_clima_actual(actual, ciudad)

    diario = obtener_pronostico(latitud, longitud)
    if diario is not None:
        mostrar_pronostico(diario)


def main():
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
            mostrar_clima(ciudad)
            if es_nueva:
                ofrecer_guardar(ciudad)


if __name__ == "__main__":
    main()