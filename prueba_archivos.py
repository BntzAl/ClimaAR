import json

favoritas = [
    {"name": "Sarandí", "admin1": "Buenos Aires", "latitude": -34.68161, "longitude": -58.34639},
    {"name": "Córdoba", "admin1": "Provincia de Córdoba", "latitude": -31.40648, "longitude": -64.18853}
]

with open("favoritas.json", "w", encoding="utf-8") as archivo:
    json.dump(favoritas, archivo, ensure_ascii=False, indent=2)

print("Guardado.")

with open("favoritas.json", "r", encoding="utf-8") as archivo:
    leidas = json.load(archivo)

print("Leí", len(leidas), "ciudad(es):")
for ciudad in leidas:
    print("-", ciudad["name"], "|", ciudad["admin1"])