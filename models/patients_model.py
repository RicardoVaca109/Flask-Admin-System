from database import db

class Patient(db.Model):
    __tablename__ = 'Pacientes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)
    contacto = db.Column(db.String(100))
    fecha_registro = db.Column(db.Date)

    # Relación con Tabla PacienteEnfermedad (patientenfermedad_model.py)
    enfermedades = db.relationship('PacienteEnfermedad', back_populates='paciente')
