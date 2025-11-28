from flask import Flask, jsonify
import requests

app = Flask(__name__)

SERVICE_A_URL = "http://service_a:5001/usuarios"


@app.route("/")
def home():
    return "Service B: consumindo Service A."

@app.route("/info")
def info():
    usuarios = requests.get(SERVICE_A_URL).json()

    resposta = []
    for u in usuarios:
        resposta.append(
            f"Usuario {u['nome']} ({u['idade']} anos) - ativo desde 2023"
        )

    return jsonify(resposta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)
