import requests
import hashlib

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

# Función para obtener los detalles del inversor
def obtener_detalles_inversor(token, invertersn):
    url = f"http://openapi.semsportal.com/api/OpenApi/GetInverterBySN?invertersn={invertersn}"

    headers = {
        "Content-Type": "application/json",
        "token": token
    }

    try:
        # Realizar la solicitud GET para obtener los detalles del inversor
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parsear la respuesta
        data = response.json()

        if data['code'] == 0:
            # Imprimir detalles del inversor
            print("Eday:", data['data']['daily_generation'], "kWh")
            print("Etotal:", data['data']['total_generation'], "kWh")
            print("Status:", data['data']['status'])
        else:
            print("Error al obtener los detalles del inversor:", data['msg'])
    except requests.exceptions.HTTPError as err:
        print("Error de red:", err)

# Ejecución del script
if __name__ == "__main__":
    account = "goodwe@perfecthome.mx"
    password = "gw123456"
    invertersn = "52000SSX207W0018"  # Cambia el número de serie si lo necesitas

    # Obtener el token
    token = obtener_token(account, password)

    # Si se obtiene el token, buscar detalles del inversor
    if token:
        obtener_detalles_inversor(token, invertersn)
