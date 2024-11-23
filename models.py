from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(100))
    side = db.Column(db.String(10))  # BUY or SELL
    price = db.Column(db.Float)
    size = db.Column(db.Float)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)

class Fill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100))
    product_id = db.Column(db.String(100))
    price = db.Column(db.Float)
    size = db.Column(db.Float)
    fee = db.Column(db.Float)
    trade_time = db.Column(db.DateTime)
