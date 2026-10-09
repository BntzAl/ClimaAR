import flet as ft

from api import buscar_ciudades, obtener_clima_actual, obtener_pronostico, describir_clima


def main(page: ft.Page):
    page.title = "ClimaAR"
    page.scroll = ft.ScrollMode.AUTO

    campo = ft.TextField(label="Ciudad", expand=True)
    resultados = ft.Column()
    clima = ft.Column()
    pronostico = ft.Column()

    def mostrar_pronostico(diario):
        pronostico.controls.append(ft.Text("Pronóstico de 7 días", size=20, weight=ft.FontWeight.BOLD))
        for i in range(len(diario["time"])):
            pronostico.controls.append(
                ft.Container(
                    padding=12,
                    border_radius=8,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text(diario["time"][i], weight=ft.FontWeight.BOLD),
                            ft.Text(describir_clima(diario["weather_code"][i])),
                            ft.Text("Máx: " + str(diario["temperature_2m_max"][i]) + " °C | Mín: " + str(diario["temperature_2m_min"][i]) + " °C"),
                            ft.Text("Sensación térmica máxima: " + str(diario["apparent_temperature_max"][i]) + " °C"),
                            ft.Text("Probabilidad de lluvia: " + str(diario["precipitation_probability_max"][i]) + " %"),
                        ],
                    ),
                )
            )

    def mostrar_clima(ciudad):
        clima.controls.clear()
        pronostico.controls.clear()

        actual = obtener_clima_actual(ciudad["latitude"], ciudad["longitude"])
        if actual is None:
            clima.controls.append(ft.Text("No se pudo obtener el clima."))
            return

        clima.controls.append(ft.Text(ciudad["name"] + " | " + ciudad.get("admin1", "-"), size=20, weight=ft.FontWeight.BOLD))
        clima.controls.append(ft.Text(str(actual["temperature_2m"]) + " °C", size=50))
        clima.controls.append(ft.Text(describir_clima(actual["weather_code"])))
        clima.controls.append(ft.Text("Sensación térmica: " + str(actual["apparent_temperature"]) + " °C"))
        clima.controls.append(ft.Text("Humedad: " + str(actual["relative_humidity_2m"]) + " %"))
        clima.controls.append(ft.Text("Viento: " + str(actual["wind_speed_10m"]) + " km/h"))
        clima.controls.append(ft.Text("Presión atmosférica: " + str(actual["surface_pressure"]) + " hPa"))

        diario = obtener_pronostico(ciudad["latitude"], ciudad["longitude"])
        if diario is None:
            pronostico.controls.append(ft.Text("No se pudo obtener el pronóstico."))
        else:
            mostrar_pronostico(diario)

    def al_elegir(ciudad):
        def manejar_clic(e):
            resultados.controls.clear()
            mostrar_clima(ciudad)
            page.update()
        return manejar_clic

    def hacer_busqueda():
        resultados.controls.clear()
        clima.controls.clear()
        pronostico.controls.clear()

        lista = buscar_ciudades(campo.value)
        if lista is None:
            resultados.controls.append(ft.Text("No se pudo buscar. Revisá tu conexión."))
            return
        if len(lista) == 0:
            resultados.controls.append(ft.Text("No encontré ninguna ciudad con ese nombre."))
            return

        for ciudad in lista:
            texto = ciudad["name"] + " | " + ciudad.get("admin1", "-") + " | " + ciudad.get("country", "-")
            resultados.controls.append(ft.TextButton(texto, on_click=al_elegir(ciudad)))

    def al_buscar(e):
        hacer_busqueda()
        page.update()

    page.add(
        ft.Text("ClimaAR", size=30, weight=ft.FontWeight.BOLD),
        ft.Row(controls=[campo, ft.Button("Buscar", on_click=al_buscar)]),
        resultados,
        clima,
        pronostico,
    )


ft.run(main)