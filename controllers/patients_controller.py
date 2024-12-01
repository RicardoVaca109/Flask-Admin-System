from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from sqlalchemy.orm import joinedload
from database import db
#Al importar los modelos de las tablas hacerlos por orden para que funcionen al 100%
from models.patients_model import Patient
from models.enfermedad_model import Enfermedad
from models.patientenfermedad_model import PatienteEnfermedad

patients_controller = Blueprint("patients_controller", __name__)

@patients_controller.route("/manage-patients")
def manage_patients():
    if "username" in session and session ["role_id"] == 4:
        #pacientes = Patient.query.all()
        pacientes = Patient.query.options(joinedload(Patient.enfermedades).joinedload(PatienteEnfermedad.enfermedad))
        return render_template("manage_patients.html", pacientes = pacientes)
    return redirect(url_for("main_controller.index"))