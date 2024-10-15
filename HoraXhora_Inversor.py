import requests
import hashlib
import datetime

# Función para obtener el token
def obtener_token(account, password):
    url = "http://openapi.semsportal.com/api/OpenApi/GetToken"
    password_md5 = hashlib.md5(password.encode()).hexdigest()
    payload = {"account": account, "pwd": password_md5}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data['data']['token']
        else:
            print("Error al obtener el token:", data['msg'])
            return None
    except requests.exceptions.HTTPError as err:
        print("Error de red:", err)
        return None

# Función para obtener la generación de energía por hora
def obtener_generacion_por_hora(token, invertersn, date):
    url = f"http://openapi.semsportal.com/api/OpenApi/GetInverterPower"
    headers = {"Content-Type": "application/json", "token": token}
    payload = {"invertersn": invertersn, "date": date}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data['code'] == 0:
            energia_total_por_hora = {}  # Diccionario para almacenar la energía por hora
            energia_total_dia = 0.0  # Variable para sumar la energía total del día

            for point in data['data']:
                time = point['date']  # Hora
                generation_watts = point['pac']  # Potencia generada en ese momento (Watts)
                hour = time.split(' ')[1][:2]  # Extraer solo la hora (HH) del formato

                # Convertir la potencia a kilovatios
                generation_kw = generation_watts / 1000.0

                # Calcular la energía generada en ese intervalo de 5 minutos (5/60 horas)
                energia_intervalo = generation_kw * (5 / 60)

                # Sumar la energía generada en este intervalo a la hora correspondiente
                if hour not in energia_total_por_hora:
                    energia_total_por_hora[hour] = 0.0
                energia_total_por_hora[hour] += energia_intervalo

            # Imprimir la energía por hora y sumar la energía total del día
            for hour, energia in energia_total_por_hora.items():
                print(f"Energía generada en la hora {hour}: {energia:.4f} kWh")
                energia_total_dia += energia

            # Imprimir la suma total de energía generada en todo el día
            print(f"\nEnergía total generada el {date}: {energia_total_dia:.4f} kWh")

        else:
            print("Error al obtener los detalles del inversor:", data['msg'])
    except requests.exceptions.HTTPError as err:
        print("Error de red:", err)


# Ejecución del script
if __name__ == "__main__":
    account = "goodwe@perfecthome.mx"
    password = "gw123456"
    invertersn = "52000SSX207W0018"
    date = "2024-10-10"  # Aquí puedes cambiar la fecha

    # Obtener el token
    token = obtener_token(account, password)

    # Si se obtiene el token, buscar la generación por hora
    if token:
        obtener_generacion_por_hora(token, invertersn, date)
