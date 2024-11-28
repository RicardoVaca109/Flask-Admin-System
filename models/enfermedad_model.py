from database import db

class Enfermedad(db.Model):
    __tablename__ = 'Enfermedades'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(250))

    # Relación con Tabla PacienteEnfermedad (patientenfermedad_model.py)
    pacientes = db.relationship('PacienteEnfermedad', back_populates='enfermedad')
