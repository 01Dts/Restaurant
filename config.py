from datetime import timedelta

class Config:
    JWT_SECRET_KEY = "my-super-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)

    DB_CONFIG = {
        'host': '127.0.0.1',
        'user': 'dts',
        'password': 'dts',
        'database': 'restaurant_db'
    }
