from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from models.users_model import User
from database import db

dashboard_controller = Blueprint("dashboard_controller", __name__)

# Ruta Dashboard
@dashboard_controller.route("/dashboard")
def dashboard():
    if "username" in session:
        if session.get("role_id") == 1: #Suponiendo que el rol es de administrador
            return render_template("dashboard_admin.html", username = session['username'])
        elif session.get("role_id") == 2: #Suponiendo que el rol es de usuario
            return render_template("dashboard_user.html", username = session['username'])
        elif session.get("role_id") == 3: #Suponiendo que el rol es de inventario
            return render_template("dashboard_invent.html", username = session['username'])
        elif session.get("role_id") == 4: #Suponiendo que el rol es de enfermeria
            return render_template("dashboard_nurse.html", username = session['username'])
    return redirect(url_for('main_controller.index'))

@dashboard_controller.route("/manage-users") # Manejo de Usuarios
def manage_users():
    if "username" in session and session ["role_id"] == 1:
        users = User.query.all()
        return render_template("manage_users.html", users = users)
    return redirect(url_for("main_controller.index"))

@dashboard_controller.route("/manage-users/create", methods = ['GET','POST'])
def create_user():
    if "username" in session and session ["role_id"] != 1:
        flash("No tienes permiso para realizar la siguiente accion")
        return redirect(url_for("dashboard_controller.dashboard"))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        role_id = request.form.get("role_id")
        
        #Creacion del nuevo usuario
        new_user = User(username = username, email = email, role_id = role_id)
        new_user.set_password(password) # establecer la contraseña encriptada
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Usuario nuevo creado")
            return(redirect(url_for("dashboard_controller.manage-users")))
        except Exception as e:
            db.session.rollback()
            flash("Error al crear nuevo usuario: {e}", "danger")
    users = User.query.all()
    return(render_template("manage_users.html", users = users))

@dashboard_controller.route("/manage-users/edit/<int:user_id>", methods=['GET', 'POST'])
def edit_user(user_id):
    # Verificar si el usuario tiene el role_id de administrador
    if "username" not in session or session["role_id"] != 1:
        flash("No tienes permisos para realizar esta acción.", "danger")
        return redirect(url_for("dashboard_controller.dashboard"))
    
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        user.role_id = request.form.get("role_id")
        password = request.form.get("password")
        if password:
            user.set_password(password)
        try:
            db.session.commit()
            flash("Usuario actualizado exitosamente.", "success")
            return redirect(url_for("dashboard_controller.manage_users"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el usuario: {e}", "danger")
            return redirect(url_for("dashboard_controller.manage_users"))
    return render_template("manage_users.html", users=User.query.all())

@dashboard_controller.route("/manage-users/delete/<int:user_id>", methods=['POST'])
def delete_user(user_id):
    if "username" not in session or session["role_id"] != 1:
        flash("No tienes permisos para realizar esta acción.", "danger")
        return redirect(url_for("dashboard_controller.dashboard"))
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash("Usuario eliminado exitosamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar usuario: {e}", "danger")

    return redirect(url_for("dashboard_controller.manage_users"))