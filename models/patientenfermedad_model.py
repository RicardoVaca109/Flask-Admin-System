from database import db

class PacienteEnfermedad(db.Model):
    __tablename__ = 'Paciente_Enfermedad'

    id_paciente = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), primary_key=True, nullable=False)
    id_enfermedad = db.Column(db.Integer, db.ForeignKey('Enfermedades.id'), primary_key=True, nullable=False)
    
    # # Relación con Paciente y Enfermedad
    paciente = db.relationship('Patient', back_populates='enfermedades')
    enfermedad = db.relationship('Enfermedad', back_populates='pacientes')