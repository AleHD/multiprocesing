import sys

import psutil
import requests
from flask import Flask, request
from getmac import get_mac_address as gma


app = Flask(__name__)

#Las ligas se deben cambiar cada vez que se monte ngrok
data = {
    "ale": {
        "host": "http://a94a-2806-106e-19-2f30-ea5d-98c8-86d3-d985.ngrok.io",
        "ram": None
    },
    "david": {
        "host": "https://dd9d-192-141-244-139.ngrok.io",
        "ram": None
    },
    "uriel": {
        "host": "http://bbf0-189-217-3-189.ngrok.io",
        "ram": None
    }
}

mi_siguiente = None
lider = None
contador = 0


@app.route("/ram")
def getram():
    print("Me estan pidendo la RAM xd")
    return {"ram": psutil.virtual_memory().total >> 20}


@app.route("/eligeLider", methods=['POST'])
def elige_lider():
    global lider

    # determina rams
    print("Iniciando 'EligeLider'")
    for (name, value) in data.items():
        print(f"Pidiendo RAM de {name}...")
        url = value["host"]
        response = requests.get(f"{url}/ram")
        value["ram"] = response.json()["ram"]

    # elige lider con base a ram
    rams = [f"{name}={value['ram']}MBs" for (name, value) in data.items()]
    print(f"Determinando lider utilizando valores de RAM: {rams}")
    best_ram = 0
    for (name, value) in data.items():
        if value["ram"] > best_ram:
            lider = name
            best_ram = value["ram"]
    print(f"Lider escogido: {lider}")

    # empieza el init hacia el lider xd
    print("Llamando init al lider xd")
    requests.get(f"{data[lider]['host']}/init")
    return {}


@app.route("/init")
def init():
    # determina mi_siguiente para cada nodo
    print("Estoy en el init!")
    urls = [value["host"] for value in data.values()]
    for (i, value) in enumerate(data.values()):
        url = value["host"]
        param = {"siguiente": urls[(i+1) % len(urls)], "lider": lider}
        requests.post(f"{url}/determinar_siguiente", json=param)

    # inicia a contar
    params = {
        "valor": 0,
        "mac": gma(),
        "nombre": sys.argv[1]
    }
    print(params)
    requests.post(f"{mi_siguiente}/count", json=params)
    return {}


@app.route("/determinar_siguiente", methods=['POST'])
def determinar():
    global mi_siguiente
    global lider
    mi_siguiente = request.json["siguiente"]
    lider = request.json["lider"]
    print(f"Me toca notificar a: {mi_siguiente}")
    return {}


@app.route("/count", methods=["POST"])
def count():
    valor = request.json["valor"]
    if valor == 50:
        requests.get(f"{data[lider]['host']}/endcount_lider")
        return {}

    print(f"estoy en el valor {valor}")
    params = {
        "valor": valor+1,
        "mac": gma(),
        "nombre": sys.argv[1]
    }
    print(params)
    requests.post(f"{mi_siguiente}/count", json=params)
    return {}

@app.route("/endcount_lider")
def endcount_lider():
    for (name, value) in data.items():
        url = value["host"]
        requests.get(f"{url}/endcount")
    return {}


@app.route("/endcount")
def endcount():
    res =  "<p> Me avisaron que terminaron la cuenta! </p>"
    print(res)
    return res


if __name__ == "__main__":
    app.run()
