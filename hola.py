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


ciudad = "Sarandí"
temperatura = 18

print("========================")
print("        CLIMAAR")
print("========================")
print("Ubicación:", ciudad)
print("Temperatura:", temperatura, "°C")
print(describir_temperatura(temperatura))
print("Recomendación de ropa:", recomendar_ropa(temperatura))
print("--- Pruebas ---")
print(describir_temperatura(5))
print(describir_temperatura(15))
print(describir_temperatura(30))
print("Recomendación de ropa:")
print(recomendar_ropa(5))
print(recomendar_ropa(15))
print(recomendar_ropa(30))

pronostico = [18, 22, 9, 15, 27, 3, 40, 21, 20, 30, 5]

print("--- Pronóstico ---")
for temp in pronostico:
    print(temp, "°C:", describir_temperatura(temp), "-", recomendar_ropa(temp))

clima_hoy = {
    "ciudad": "Sarandí",
    "temperatura": 18,
    "sensacion": 17,
    "humedad": 72,
    "viento": 14,
    "prob_lluvia": 30,
    "presion": 1015,
}

print("--- Clima de hoy ---")
print("Ciudad:", clima_hoy["ciudad"])
print("Temperatura:", clima_hoy["temperatura"], "°C")
print("Sensación térmica:", clima_hoy["sensacion"], "°C")
print("Humedad:", clima_hoy["humedad"], "%")
print("Viento:", clima_hoy["viento"], "km/h")
print("Probabilidad de lluvia:", clima_hoy["prob_lluvia"], "%")
print("Presión atmosférica:", clima_hoy["presion"], "hPa")
print(describir_temperatura(clima_hoy["temperatura"]))
