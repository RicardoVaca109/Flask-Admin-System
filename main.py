# main.py
#Importar Librerias
import os
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

# Importar la base de datos desde database.py
from database import db

#Importar controladores
from controllers.auth_controller import auth_controller
from controllers.dashboard_controller import dashboard_controller
from controllers.main_controller import main_controller
from controllers.patients_controller import patients_controller
from controllers.inventory_controller import inventory_controller
from models.users_model import User


# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = "DysonSlMilo2003"

# Configurar SQLAlchemy para base de datos Railway
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# #Configurar SQLAlchemy para base de datos local
# app.config["SQLALCHEMY_DATABASE_URI"] = (
#     f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
#     f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
# )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la base de datos con la aplicación
db.init_app(app)

# Probar la conexión sin crear tablas
with app.app_context():
    try:
        db.session.execute(text("SELECT 1"))
        print("Connection successful")
    except OperationalError as e:
        print("Connection failed:", e)

# Registrar blueprints
app.register_blueprint(main_controller)
app.register_blueprint(auth_controller)
app.register_blueprint(dashboard_controller)
app.register_blueprint(patients_controller)
app.register_blueprint(inventory_controller)

if __name__ == "__main__":
    app.run(debug=True)
