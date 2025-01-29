# Importar los modelos
from models.medicine_model import Medicine
from database import db

class ModelFactory:
    @staticmethod
    def create_medicine(nombre, sistema, categoria, cantidad, stock_minimo, fecha_expiracion, descripcion):
        """Crea y guarda una medicina en la base de datos."""
        medicine = Medicine(
            nombre=nombre,
            sistema=sistema,
            categoria=categoria,
            cantidad=cantidad,
            stock_minimo=stock_minimo,
            fecha_expiracion=fecha_expiracion,
            descripcion=descripcion
        )
        db.session.add(medicine)
        db.session.commit()
        return medicine