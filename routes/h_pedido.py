from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.h_pedido import H_pedido
from pymongo import MongoClient
from bson import json_util
from flask import jsonify
from bson.objectid import ObjectId
db = dbase()
h_pedido = Blueprint('h_pedido', __name__)


# * Visualizar Historial pedido
@h_pedido.route("/admin/h_pedido")
def v_hpedi():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('admin.index'))  # Redirige al usuario al inicio si no está en la sesión

    # Agrupa los pedidos por id_cliente y selecciona el primer pedido de cada grupo
    pipeline = [
        {"$group": {
            "_id": "$id_cliente",
            "pedido": {"$first": "$$ROOT"}
        }},
        {"$replaceRoot": {"newRoot": "$pedido"}}
    ]
    h_pedido = db['h_pedido'].aggregate(pipeline)

    return render_template("admin/h_pedido.html", h_pedido=h_pedido)

@h_pedido.route('/admin/h_pedido/actualizar', methods=['POST'])
def actualizar_pedidos():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        id_pedido = data.get('id_pedido')
        resultado = data.get('resultado')
        fecha_entrega = data.get('fecha_entrega')
        estado = data.get('estado')

        # Validar que el id_pedido esté presente
        if not id_pedido:
            return jsonify({"success": False, "message": "ID Pedido es requerido"}), 400

        # Crear un diccionario con los campos a actualizar
        update_data = {}
        if resultado is not None:
            update_data['resultado'] = resultado
        if fecha_entrega is not None:
            update_data['fecha_entrega'] = fecha_entrega
        if estado is not None:
            update_data['estado'] = estado

        # Actualizar el pedido en la base de datos
        db['h_pedido'].update_one(
            {"id_pedido": id_pedido},  # Filtro por id_pedido
            {"$set": update_data}      # Campos a actualizar
        )

        return jsonify({"success": True, "message": "Pedido actualizado correctamente"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500