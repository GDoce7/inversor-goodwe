import requests
import hashlib

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

# Función para obtener los datos del inversor, incluido el amperaje si está disponible
def obtener_datos_inversor(token, invertersn):
    url = f"http://openapi.semsportal.com/api/v1/OpenApi/GetInverterDetail"

    headers = {
        "Content-Type": "application/json",
        "token": token
    }

    payload = {
        "inverterSn": invertersn
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data['code'] == 0:
            # Imprimir la respuesta completa para verificar si está el amperaje
            print("Datos del inversor:", data)

            # Buscar los datos de corriente (amperaje) si están disponibles
            if 'data' in data and 'electric_current' in data['data']:
                amperaje = data['data']['electric_current']
                print(f"Amperaje actual del inversor: {amperaje} A")
            else:
                print("No se encontraron datos de amperaje en la respuesta.")
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

    # Si se obtiene el token, buscar los datos del inversor
    if token:
        obtener_datos_inversor(token, invertersn)
