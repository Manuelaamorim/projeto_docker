from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/orders")
def get_orders():
    pedidos = [
        {"order_id": 101, "user_id": 1, "item": "Teclado"},
        {"order_id": 102, "user_id": 2, "item": "Mouse"},
        {"order_id": 103, "user_id": 3, "item": "Monitor"},
    ]
    return jsonify(pedidos)

app.run(host="0.0.0.0", port=5002)
