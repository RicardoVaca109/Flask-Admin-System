from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from sqlalchemy import func, extract
from sqlalchemy.orm import joinedload
from database import db


from models.medicine_model import Medicine
from models.consumos_model import Consumo
from models.patients_model import Patient
from models.enfermedad_model import Enfermedad
from models.patientenfermedad_model import PatienteEnfermedad

inventory_controller = Blueprint("inventory_controller", __name__)

@inventory_controller.route("/manage-consumos", methods=['GET', 'POST'])
def manage_consumos():
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            flash("Por favor, selecciona ambas fechas", "warning")
            return redirect(url_for('inventory_controller.manage_consumos'))

        # Filtrar consumos por rango de fechas
        consumos_query = db.session.query(
            func.year(Consumo.fecha_consumo).label('anio'),
            func.month(Consumo.fecha_consumo).label('mes'),
            Medicine.nombre.label('medicina'),
            func.sum(Consumo.cantidad_consumida).label('total_consumido')
        ).join(Medicine, Consumo.id_Medicinas == Medicine.id)\
         .filter(Consumo.fecha_consumo.between(fecha_inicio, fecha_fin))\
         .group_by(func.year(Consumo.fecha_consumo), func.month(Consumo.fecha_consumo), Medicine.nombre)\
         .order_by('anio', 'mes')

        consumos = consumos_query.all()

        # Preparar los datos finales para el template
        resultado_consumos = []
        total_consumido_global = sum(c.total_consumido for c in consumos)

        for consumo in consumos:
            porcentaje_consumo = (consumo.total_consumido / total_consumido_global) * 100 if total_consumido_global > 0 else 0

            resultado_consumos.append({
                'anio': consumo.anio,
                'mes': consumo.mes,
                'medicina': consumo.medicina,
                'total_consumido': consumo.total_consumido,
                'porcentaje_consumo': porcentaje_consumo
            })

        return render_template('manage_inventory.html', consumos=resultado_consumos, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    return render_template('manage_inventory.html', consumos=[], fecha_inicio=None, fecha_fin=None)


@inventory_controller.route("/reporte-medicina-mas-consumida", methods=['GET', 'POST'])
def reporte_medicina_mas_consumida():
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            flash("Por favor, selecciona ambas fechas", "warning")
            return redirect(url_for('inventory_controller.reporte_medicina_mas_consumida'))

        # Consulta para obtener la medicina más consumida por mes y cantidad de pacientes
        consulta = db.session.query(
            func.year(Consumo.fecha_consumo).label('anio'),
            func.month(Consumo.fecha_consumo).label('mes'),
            Medicine.nombre.label('medicina'),
            func.sum(Consumo.cantidad_consumida).label('total_consumido'),
            func.count(Consumo.id_Pacientes).label('total_pacientes')  # Aquí se corrige el atributo
        ).join(Medicine, Consumo.id_Medicinas == Medicine.id)\
         .filter(Consumo.fecha_consumo.between(fecha_inicio, fecha_fin))\
         .group_by(func.year(Consumo.fecha_consumo), func.month(Consumo.fecha_consumo), Medicine.nombre)\
         .subquery()

        # Filtrar solo las medicinas más consumidas por mes
        medicinas_mas_consumidas = db.session.query(
            consulta.c.anio,
            consulta.c.mes,
            consulta.c.medicina,
            consulta.c.total_consumido,
            consulta.c.total_pacientes
        ).filter(consulta.c.total_consumido == db.session.query(
            func.max(consulta.c.total_consumido)
        ).filter(
            consulta.c.anio == func.year(Consumo.fecha_consumo),
            consulta.c.mes == func.month(Consumo.fecha_consumo)
        ).correlate(consulta))

        resultados = medicinas_mas_consumidas.all()

        return render_template(
            'reporte_medicina_mas_consumida.html',
            resultados=resultados,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
# reportes entre rango de fechas y sumatoria total de medicinas consumidas por paciente  que este ordenada (en este rango de fechas que pacientes consumieorn mas medicina)
    return render_template('reporte_medicina_mas_consumida.html', resultados=[], fecha_inicio=None, fecha_fin=None)

@inventory_controller.route("/prediccion-consumos", methods=['GET', 'POST'])
def predict_consumos():
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            flash("Por favor, selecciona ambas fechas", "warning")
            return redirect(url_for('inventory_controller.predict_consumos'))

        # Obtener el total de consumos por mes en el rango de fechas
        consumos_query = db.session.query(
            func.year(Consumo.fecha_consumo).label('anio'),
            func.month(Consumo.fecha_consumo).label('mes'),
            Medicine.nombre.label('medicina'),
            Medicine.sistema.label('sistema'),
            Medicine.categoria.label('categoria'),
            func.sum(Consumo.cantidad_consumida).label('total_consumido')
        ).join(Medicine, Consumo.id_Medicinas == Medicine.id)\
         .filter(Consumo.fecha_consumo.between(fecha_inicio, fecha_fin))\
         .group_by(func.year(Consumo.fecha_consumo), func.month(Consumo.fecha_consumo), Medicine.id)\
         .order_by('anio', 'mes')

        consumos = consumos_query.all()

        # Calcular la media de consumo por medicina para predicción
        predicciones = {}
        for consumo in consumos:
            if consumo.medicina not in predicciones:
                predicciones[consumo.medicina] = {
                    'total': 0,
                    'meses': 0,
                    'sistema': consumo.sistema,
                    'categoria': consumo.categoria
                }

            predicciones[consumo.medicina]['total'] += consumo.total_consumido
            predicciones[consumo.medicina]['meses'] += 1

        predicciones_finales = [
            {
                'medicina': medicina,
                'sistema': datos['sistema'],
                'categoria': datos['categoria'],
                'consumo_promedio': round(datos['total'] / datos['meses'], 2)
            }
            for medicina, datos in predicciones.items()
        ]

        return render_template(
            'prediccion_consumos.html',
            predicciones=predicciones_finales,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    return render_template('prediccion_consumos.html', predicciones=[], fecha_inicio=None, fecha_fin=None)

@inventory_controller.route("/reporte-consumo-pacientes", methods=['GET', 'POST'])
def reporte_consumo_pacientes():
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            flash("Por favor, selecciona ambas fechas", "warning")
            return redirect(url_for('inventory_controller.reporte_consumo_pacientes'))

        # Consulta para obtener el consumo total por paciente
        consulta = db.session.query(
            Patient.nombre.label('nombre_paciente'),
            Patient.apellido.label('apellido_paciente'),
            func.sum(Consumo.cantidad_consumida).label('total_medicinas_consumidas')
        ).join(Consumo, Patient.id == Consumo.id_Pacientes)\
         .filter(Consumo.fecha_consumo.between(fecha_inicio, fecha_fin))\
         .group_by(Patient.id)\
         .order_by(func.sum(Consumo.cantidad_consumida).desc())

        resultados = consulta.all()

        return render_template(
            'reporte_consumo_pacientes.html',
            resultados=resultados,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

    return render_template('reporte_consumo_pacientes.html', resultados=[], fecha_inicio=None, fecha_fin=None)

