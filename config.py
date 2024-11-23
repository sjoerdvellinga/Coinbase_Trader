import os

class Config:
    COINBASE_API_KEY = "YOUR_API_KEY"
    COINBASE_API_SECRET = "YOUR_PRIVATE_KEY"
    BASE_URL = "https://api.coinbase.com/api/v3/brokerage/"
    SQLALCHEMY_DATABASE_URI = "sqlite:///crypto_tracker.db"  # Use SQLite locally
    SQLALCHEMY_TRACK_MODIFICATIONS = False
