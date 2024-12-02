from database import db
from email_validator import validate_email, EmailNotValidError
class Patient(db.Model):
    __tablename__ = 'Pacientes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer)
    contacto = db.Column(db.String(100), unique=True, nullable=False)
    fecha_registro = db.Column(db.Date)

    # Relación con Tabla PatienteEnfermedad (patientenfermedad_model.py)
    enfermedades = db.relationship('PatienteEnfermedad', back_populates='paciente')
    #  Relación con Tabla Consumo (consumos_model.py)
    consumos = db.relationship("Consumo", back_populates="paciente")

    def set_contact(self, contacto):
        try:
            valid_email = validate_email(contacto).email
            self.contacto = valid_email
        except EmailNotValidError as e:
            raise ValueError(f"Email inválido: {str(e)}")