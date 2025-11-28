from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/users")
def get_users():
    users = [
        {"id": 1, "nome": "Ana"},
        {"id": 2, "nome": "Pedro"},
        {"id": 3, "nome": "Manuela"},
    ]
    return jsonify(users)

app.run(host="0.0.0.0", port=5003)
