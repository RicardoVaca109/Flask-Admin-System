from database import db

class Role(db.Model):
    __tablename__ = 'roles'
    
    # Mapeo de la tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    
    # Relación con User
    users = db.relationship('User', backref='role', lazy=True)