from flask_sqlalchemy import SQLAlchemy

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.db = SQLAlchemy()  # Crear la instancia única de SQLAlchemy
        return cls._instance

    @staticmethod
    def get_db():
        return DatabaseConnection()._instance.db


# Crear una función para obtener la instancia de la base de datos
db = DatabaseConnection.get_db()
