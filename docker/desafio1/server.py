from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Servidor Flask rodando na porta 8080!"

app.run(host="0.0.0.0", port=8080)
