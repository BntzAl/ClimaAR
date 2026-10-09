# ClimaAR

Aplicación meteorológica desarrollada en Python, pensada como proyecto de aprendizaje y portfolio.

## Qué hace hoy

- Busca ciudades por nombre.
- Permite elegir entre los resultados encontrados.
- Muestra el clima actual y su estado (despejado, nublado, lluvia, etc.).
- Muestra el pronóstico de 7 días.
- Muestra temperatura y sensación térmica.
- Muestra humedad, viento y presión atmosférica.
- Permite guardar, consultar y eliminar ciudades favoritas (versión de consola).
- Muestra mensajes claros cuando falla la conexión.
- Tiene una interfaz gráfica con ventana, hecha con Flet.

## Dos formas de usarla

- **Consola:** `python climaar.py` (menú completo, con favoritas).
- **Ventana:** `python interfaz.py` (versión gráfica en desarrollo: búsqueda, clima actual y pronóstico de 7 días).

## Estructura del proyecto

- `climaar.py`: menú y pantallas de la versión de consola.
- `interfaz.py`: interfaz gráfica con Flet.
- `api.py`: pedidos a la API de Open-Meteo.
- `favoritas.py`: lectura y escritura de ciudades favoritas.
- `config.py`: constantes y códigos del clima.
- `requirements.txt`: librerías necesarias con su versión.

## Cómo ejecutarlo

1. Instalar Python.
2. Crear y activar un entorno virtual.
3. Instalar las dependencias con `pip install -r requirements.txt`.
4. Ejecutar `python climaar.py` o `python interfaz.py`.

## Tecnologías

- Python
- API de [Open-Meteo](https://open-meteo.com/) (sin clave)
- Librería `requests`
- [Flet](https://flet.dev/) para la interfaz gráfica

## Próximos pasos

- Llevar las ciudades favoritas a la ventana.
- Agregar íconos meteorológicos.
- Agregar más información meteorológica.
- Crear versiones para Windows, macOS y Android.