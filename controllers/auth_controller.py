from flask import Blueprint, render_template, url_for, redirect, session, request
from models.users_model import User
from models.role_model import Role
from database import db

auth_controller = Blueprint("auth_controller", __name__)

# Ruta Login
@auth_controller.route("/login", methods=["POST"])
def login():
    # Recolectar la data del form de html
    usuario = request.form['username']
    password = request.form['password']
    email = request.form['email']
    user = User.query.filter_by(username = usuario, email = email).first() # Verificar usuario y email
    
    # Verificar contraseña y existencia del usuario
    if user and user.check_password(password):
        session['username'] = usuario
        session['role_id'] = user.role_id
        session['role_name'] = user.role.role_name
        return redirect(url_for('dashboard_controller.dashboard'))
    else:
        return render_template("index.html", error="Usuario, email o contraseña incorrectos")


# Ruta Registro
@auth_controller.route("/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    # Verificar si ya existe un usuario con el mismo username o email
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return render_template("index.html", error="Usuario ya existe")
    
    # Asignar rol según si es el primer usuario o no
    role_admin = Role.query.filter_by(role_name="administrador").first()
    role_user = Role.query.filter_by(role_name="usuario").first()
    
    # Si no existen usuarios, asignar el rol de administrador al primer usuario
    role_id = role_admin.id if User.query.count() == 0 else role_user.id
    
     # Crear nuevo usuario y asignarle el rol adecuado
    new_user = User(username=username, role_id=role_id)
    new_user.set_password(password)
    new_user.set_email(email)
    db.session.add(new_user)
    db.session.commit()
    
    # Iniciar sesión automáticamente para el nuevo usuario registrado
    session['username'] = username
    session['role_id'] = new_user.role_id
    return redirect(url_for('dashboard_controller.dashboard'))

   

@auth_controller.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('role_id', None)
    session.pop('role_name', None)
    return redirect(url_for('main_controller.index'))     
