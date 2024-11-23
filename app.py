from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Order, Fill
import requests
import time
import hmac
import hashlib
import base64

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def sign_request(timestamp, method, path, body=""):
    message = f"{timestamp}{method}{path}{body}"
    secret = base64.b64decode(app.config["COINBASE_API_SECRET"])
    return hmac.new(secret, message.encode(), hashlib.sha256).hexdigest()

@app.route("/")
def index():
    # Fetch orders and fills from the database
    orders = Order.query.all()
    fills = Fill.query.all()
    return render_template("index.html", orders=orders, fills=fills)

@app.route("/update", methods=["POST"])
def update_data():
    timestamp = str(int(time.time()))
    headers = {
        "CB-ACCESS-KEY": app.config["COINBASE_API_KEY"],
        "CB-ACCESS-TIMESTAMP": timestamp,
        "CB-ACCESS-SIGN": sign_request(timestamp, "GET", "/orders/historical/batch"),
    }

    # Fetch orders
    orders_response = requests.get(
        app.config["BASE_URL"] + "orders/historical/batch", headers=headers
    )
    orders_data = orders_response.json()
    # Save orders to the database
    for order in orders_data.get("orders", []):
        new_order = Order(
            product_id=order["product_id"],
            side=order["side"],
            price=order["price"],
            size=order["size"],
            status=order["status"],
            created_at=order["created_at"],
        )
        db.session.add(new_order)

    db.session.commit()
    return "Data updated successfully!"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure the database schema is created
    app.run(debug=True)
