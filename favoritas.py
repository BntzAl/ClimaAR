import json
import os

from config import ARCHIVO_FAVORITAS


def cargar_favoritas():
    if not os.path.exists(ARCHIVO_FAVORITAS):
        return []
    with open(ARCHIVO_FAVORITAS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_favoritas(favoritas):
    with open(ARCHIVO_FAVORITAS, "w", encoding="utf-8") as archivo:
        json.dump(favoritas, archivo, ensure_ascii=False, indent=2)


def agregar_favorita(ciudad):
    # Devuelve True si la guardó, o False si ya estaba en la lista.
    favoritas = cargar_favoritas()
    for lugar in favoritas:
        if lugar["latitude"] == ciudad["latitude"] and lugar["longitude"] == ciudad["longitude"]:
            return False

    favoritas.append({
        "name": ciudad["name"],
        "admin1": ciudad.get("admin1", "-"),
        "latitude": ciudad["latitude"],
        "longitude": ciudad["longitude"],
    })
    guardar_favoritas(favoritas)
    return True


def eliminar_favorita(indice):
    # Saca la ciudad que está en esa posición de la lista y la devuelve.
    favoritas = cargar_favoritas()
    eliminada = favoritas.pop(indice)
    guardar_favoritas(favoritas)
    return eliminada