from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/usuarios")
def listar_usuarios():
    usuarios = [
        {"id": 1, "nome": "Ana", "idade": 22},
        {"id": 2, "nome": "Pedro", "idade": 25},
        {"id": 3, "nome": "Marina", "idade": 21},
    ]
    return jsonify(usuarios)

@app.route("/")
def home():
    return "Service A: lista de usuários."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
