import requests
import hashlib
import datetime as dt

BASE_URL = "http://openapi.semsportal.com/api/OpenApi"

# ---------- Auxiliares ----------
def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def ayer_formato_api() -> str:
    """Devuelve la fecha de ayer en formato YYYY-MM-DD (hora de México)."""
    tz_mex = dt.timezone(dt.timedelta(hours=-6))          # CST sin DST 2025
    return (dt.datetime.now(tz_mex) - dt.timedelta(days=1)).date().isoformat()


# ---------- 1. Obtener token ----------
def obtener_token(account: str, password: str) -> str | None:
    url = f"{BASE_URL}/GetToken"
    payload = {"account": account, "pwd": md5(password)}

    try:
        data = requests.post(url, json=payload, timeout=15).json()
        if data["code"] == 0:
            return data["data"]["token"]          # :contentReference[oaicite:1]{index=1}
        print("Error al obtener token:", data["msg"])
    except requests.exceptions.RequestException as err:
        print("Error de red:", err)
    return None


# ---------- 2. Detalles instantáneos del inversor ----------
def obtener_detalles_inversor(token: str, invertersn: str) -> None:
    url = f"{BASE_URL}/GetInverterBySN?invertersn={invertersn}"
    headers = {"Content-Type": "application/json", "token": token}

    try:
        data = requests.get(url, headers=headers, timeout=15).json()
        if data["code"] == 0:
            d = data["data"]
            print(f"- Detalles actuales del inversor {invertersn}")
            print("    Eday:  ", d["daily_generation"],  "kWh")
            print("    Etotal:", d["total_generation"],  "kWh")
            print("    Status:", d["status"])
        else:
            print("Error detalles inversor:", data["msg"])
    except requests.exceptions.RequestException as err:
        print("Error de red:", err)


# ---------- 3. Generación de AYER ----------
def obtener_generacion_ayer(token: str, invertersn: str) -> None:
    url = f"{BASE_URL}/GetInverterGeneration"
    headers = {"Content-Type": "application/json", "token": token}
    fecha_ayer = ayer_formato_api()

    payload = {
        "invertersn": invertersn,
        "date": fecha_ayer,  # ejemplo: 2025-06-19
        "type": 0            # 0 = diario :contentReference[oaicite:2]{index=2}
    }

    try:
        data = requests.post(url, json=payload, headers=headers, timeout=15).json()
        if data["code"] != 0:
            print("Error generación ayer:", data["msg"])
            return

        # ----- Dos posibles estructuras según firmware/API -----
        kwh = None
        # v0: data["pv"]  → lista de PointModel {x,y}
        if "pv" in data["data"]:
            for punto in data["data"]["pv"]:
                if punto["x"].startswith(fecha_ayer):
                    kwh = punto["y"]
                    break
        # v1: data["records"] → lista de InverterGenerationItem
        elif "records" in data["data"]:
            for rec in data["data"]["records"]:
                if rec["time"].startswith(fecha_ayer):
                    kwh = rec["pv"]
                    break

        if kwh is not None:
            print(f"- Generación AYER ({fecha_ayer}): {kwh} kWh")
        else:
            print(f"No se encontró dato de generación para {fecha_ayer}")

    except requests.exceptions.RequestException as err:
        print("Error de red:", err)


# ------------------ Ejecución principal ------------------
if __name__ == "__main__":
    account    = "goodwe@perfecthome.mx"
    password   = "gw123456"
    invertersn = "52000SSX207W0018"     # cámbialo por el tuyo

    token = obtener_token(account, password)
    if not token:
        exit(1)

    obtener_detalles_inversor(token, invertersn)
    obtener_generacion_ayer(token, invertersn)
