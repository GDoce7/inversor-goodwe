import requests
import hashlib
import datetime

# Credenciales de la cuenta y URL base para México
account = "goodwe@perfecthome.mx"
password = "gw123456"
base_url = "http://openapi.semsportal.com/api/OpenApi"  # URL específico para México

# Función para obtener el token de autorización
def get_token():
    url = f"{base_url}/GetToken"
    hashed_password = hashlib.md5(password.encode()).hexdigest()  # Convertir la contraseña a MD5
    payload = {
        "account": account,
        "pwd": hashed_password
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["data"]["token"]

# Función para obtener los datos diarios de generación de una planta
def get_daily_generation_data(plant_id, start_date, end_date, token):
    url = f"{base_url}/GetPlantPower"
    headers = {"Authorization": f"Bearer {token}"}
    daily_data = []

    current_date = start_date
    while current_date <= end_date:
        payload = {
            "plant_id": plant_id,
            "date": current_date.strftime("%Y-%m-%d")
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", {})
        
        # Almacenar la fecha y los datos de potencia
        if "pv_power" in data:
            daily_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "power_data": data["pv_power"]
            })
        
        current_date += datetime.timedelta(days=1)
    
    return daily_data

# Script principal
def main():
    # Ejemplo de ID de la planta
    plant_id = "COPYRENT PENINSULAR S. DE R.L. DE C.V."  # Reemplaza con el ID real de la planta si es distinto
    start_date = datetime.datetime(2024, 9, 1)
    end_date = datetime.datetime(2024, 10, 30)
    
    # Autenticarse y obtener el token
    token = get_token()
    
    # Obtener los datos de generación diaria
    daily_data = get_daily_generation_data(plant_id, start_date, end_date, token)
    
    # Mostrar los datos
    for day_data in daily_data:
        print(f"Fecha: {day_data['date']}")
        for entry in day_data["power_data"]:
            print(f"Hora: {entry['x']}, Potencia: {entry['y']} W")

if __name__ == "__main__":
    main()
