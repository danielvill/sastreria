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

# Este codigo lo que permite hacer es que cuando actulice lo que se tiene que borrar es el codigo del 
# Pedido para que en este caso se 

@h_pedido.route('/admin/h_pedido/actualizar', methods=['POST'])
def actualizar_pedidos():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        id_pedido = data.get('id_pedido')
        id_cliente = data.get('id_cliente')  # Obtener id_cliente
        resultado = data.get('resultado')
        fecha_entrega = data.get('fecha_entrega')
        estado = data.get('estado')

        # Validar que el id_pedido y id_cliente estén presentes
        if not id_pedido:
            return jsonify({"success": False, "message": "ID Pedido es requerido"}), 400
        if not id_cliente:
            return jsonify({"success": False, "message": "ID Cliente es requerido"}), 400

        # Crear un diccionario con los campos a actualizar
        update_data = {}
        if resultado is not None:
            update_data['resultado'] = resultado
        if fecha_entrega is not None:
            update_data['fecha_entrega'] = fecha_entrega
        if estado is not None:
            update_data['estado'] = estado

        # Eliminar todos los registros relacionados con el id_cliente en la tabla pedido
        db['pedido'].delete_many({"id_cliente": id_cliente})

        # Actualizar el pedido en la base de datos
        db['h_pedido'].update_one(
            {"id_pedido": id_pedido},  # Filtro por id_pedido
            {"$set": update_data}      # Campos a actualizar
        )

        return jsonify({"success": True, "message": "Pedido actualizado y registros eliminados correctamente"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@h_pedido.route("/admin/v_pedido/<id>")
def v_ped(id):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('h_pedido.index'))
    
    h_pedidos_cursor = db['h_pedido'].find({"id_cliente": id})  # Obtener el cursor
    h_pedidos = list(h_pedidos_cursor)  # Convertir el cursor en una lista

    if not h_pedidos:
        print(f"No se encontraron pedidos para el cliente con id_cliente={id}")
    else:
        print(f"Pedidos encontrados para el cliente con id_cliente={id}: {h_pedidos}")

    return render_template("admin/v_pedido.html", h_pedidos=h_pedidos)
