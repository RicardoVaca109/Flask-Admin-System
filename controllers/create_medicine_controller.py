from flask import Blueprint, request, jsonify
from factory.model_factory import ModelFactory

create_medicine_controller = Blueprint("create_medicine_controller", __name__)  # 👈 Sin `url_prefix` aquí

@create_medicine_controller.route("/medicines", methods=["POST"])
def create_medicine():
    data = request.json
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    new_medicine = ModelFactory.create_medicine(
        nombre=data["nombre"],
        sistema=data["sistema"],
        categoria=data["categoria"],
        cantidad=data["cantidad"],
        stock_minimo=data["stock_minimo"],
        fecha_expiracion=data["fecha_expiracion"],
        descripcion=data["descripcion"]
    )
    return jsonify({"id": new_medicine.id, "nombre": new_medicine.nombre}), 201
