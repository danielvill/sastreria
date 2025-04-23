from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from pymongo import MongoClient
db = dbase()
chart = Blueprint('chart', __name__)


# Chart de la parte principal del dasbohard
@chart.route("/admin/dasbohard")
def dasbor():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('cliente.index'))  # Redirige al usuario al inicio si no está en la sesión

    # Contar registros en cada colección para saber el total de cada uno de las tablas 
    total_clientes = db['cliente'].count_documents({})
    total_productos = db['producto'].count_documents({})
    total_h_pedidos = db['h_pedido'].count_documents({})
    total_pedidos = db['pedido'].count_documents({})
    productos = db["producto"].find()
    h_pedido = db["h_pedido"].find()
    # Pasar los totales al template
    return render_template(
        "admin/dasbohard.html",
        total_clientes=total_clientes,
        total_productos=total_productos,
        total_h_pedidos=total_h_pedidos,
        total_pedidos=total_pedidos,
        producto = productos,
        h_pedido = h_pedido
    )
