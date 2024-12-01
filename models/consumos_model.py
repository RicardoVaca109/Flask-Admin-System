from database import db

class Consumo(db.Model):
    __tablename__ = 'Consumos'

    idConsumo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_Medicinas = db.Column(db.Integer, db.ForeignKey('Medicinas.id'), nullable=False)
    id_Pacientes = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False)
    cantidad_consumida = db.Column(db.Integer, nullable=False)
    fecha_consumo = db.Column(db.Date)

    # Relación con la tabla Medicinas
    medicina = db.relationship('Medicine', back_populates='consumos')

    # Relación con la tabla Pacientes
    paciente = db.relationship('Patient', back_populates='consumos')