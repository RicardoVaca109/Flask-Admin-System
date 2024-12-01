from database import db

class Medicine(db.Model):
    __tablename__ = 'Medicinas'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    nombre = db.Column(db.String(100), nullable = False)
    sistema = db.Column(db.String(60), nullable = False)
    categoria = db.Column(db.String(60), nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    stock_minimo = db.Column(db.Integer, nullable = False)
    fecha_expiracion = db.Column(db.Date)
    descripcion = db.Column(db.String(250))
    
    # Relacion con la tabla Consumos
    consumos = db.relationship('Consumo', back_populates='medicina')
