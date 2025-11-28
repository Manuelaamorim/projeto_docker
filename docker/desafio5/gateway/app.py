from flask import Flask, jsonify
import requests

app = Flask(__name__)

USERS_URL = "http://users_service:5003/users"
ORDERS_URL = "http://orders_service:5002/orders"

@app.get("/users")
def gateway_users():
    data = requests.get(USERS_URL).json()
    return jsonify({"users": data})

@app.get("/orders")
def gateway_orders():
    data = requests.get(ORDERS_URL).json()
    return jsonify({"orders": data})

app.run(host="0.0.0.0", port=5004)
