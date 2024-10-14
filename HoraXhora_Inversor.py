import requests
import hashlib
import datetime

# Función para obtener el token
def obtener_token(account, password):
    url = "http://openapi.semsportal.com/api/OpenApi/GetToken"

    # Convertir la contraseña a MD5
    password_md5 = hashlib.md5(password.encode()).hexdigest()

    # Datos que se envían en la solicitud
    payload = {
        "account": account,
        "pwd": password_md5
    }

    try:
        # Realizar la solicitud POST para obtener el token
        response = requests.post(url, json=payload)
        response.raise_for_status()

        # Parsear la respuesta
        data = response.json()

        if data['code'] == 0:
            return data['data']['token']
        else:
            print("Error al obtener el token:", data['msg'])
            return None
    except requests.exceptions.HTTPError as err:
        print("Error de red:", err)
        return None

# Función para obtener la generación de energía hora por hora del inversor
def obtener_generacion_por_hora(token, invertersn, date):
    url = f"http://openapi.semsportal.com/api/OpenApi/GetInverterPower"

    headers = {
        "Content-Type": "application/json",
        "token": token
    }

    payload = {
        "invertersn": invertersn,
        "date": date
    }

    try:
        # Realizar la solicitud POST para obtener los datos de generación por hora
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # Parsear la respuesta
        data = response.json()

        if data['code'] == 0:
            # Iterar a través de los datos por hora
            for point in data['data']['pv']:
                time = point['x']  # Hora
                generation = point['y']  # Potencia generada en ese momento
                print(f"Hora: {time}, Generación: {generation} W")
        else:
            print("Error al obtener los detalles del inversor:", data['msg'])
    except requests.exceptions.HTTPError as err:
        print("Error de red:", err)

# Ejecución del script
if __name__ == "__main__":
    account = "goodwe@perfecthome.mx"
    password = "gw123456"
    invertersn = "52000SSX207W0018"  # Cambia el número de serie si lo necesitas
    date = str(datetime.date.today())  # Puedes poner cualquier fecha en formato YYYY-MM-DD

    # Obtener el token
    token = obtener_token(account, password)

    # Si se obtiene el token, buscar la generación por hora
    if token:
        obtener_generacion_por_hora(token, invertersn, date)
