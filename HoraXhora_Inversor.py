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

# Función para obtener los datos de potencia instantánea (pac) en intervalos
def obtener_potencia_horaria(token, invertersn, date):
    url = f"http://openapi.semsportal.com/api/v1/OpenApi/GetInverterData"
    headers = {"Content-Type": "application/json", "token": token}
    payload = {"invertersn": invertersn, "date": date}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        if data['code'] == 0:
            return data['data']  # Retornamos todos los datos de potencia
        else:
            print("Error al obtener los detalles del inversor:", data['msg'])
            return None
    except requests.exceptions.HTTPError as err:
        print("Error de red:", err)

# Función para calcular la energía generada por hora usando los datos de potencia (pac)
def calcular_energia_por_potencia(token, invertersn, date):
    # Obtener datos de potencia para el día
    datos_potencia = obtener_potencia_horaria(token, invertersn, date)
    
    if datos_potencia:
        # Extraemos los valores de potencia (pac) en vatios
        potencia_por_hora = [dato['pac'] for dato in datos_potencia['records']]

        # Calcular la energía generada por hora
        energia_horaria = []
        for potencia in potencia_por_hora:
            # Energía generada (kWh) = Potencia (W) / 1000 * 1 hora
            energia_generada = (potencia / 1000) * 1  # 1 hora
            energia_horaria.append(energia_generada)
        
        # Mostrar la energía generada por hora
        for hora, energia in enumerate(energia_horaria, 1):
            print(f"Energía generada en la hora {hora}: {energia:.5f} kWh")

# Ejecución del script
if __name__ == "__main__":
    account = "goodwe@perfecthome.mx"
    password = "gw123456"
    invertersn = "52000SSX207W0018"
    date = "2024-10-13"

    # Obtener el token
    token = obtener_token(account, password)

    if token:
        # Calcular la energía generada por hora usando la potencia
        calcular_energia_por_potencia(token, invertersn, date)
