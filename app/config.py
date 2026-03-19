import os
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")  # localhost da máquina
DB_PORT = os.getenv("MYSQL_PORT", "3307")       # porta mapeada no compose
DB_NAME = os.getenv("MYSQL_DATABASE", "fafnir_db")

class Config:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")

    CATEGORIES_PER_PAGE = 10
    LOCATIONS_PER_PAGE = 1