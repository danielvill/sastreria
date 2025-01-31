from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.h_pedido import H_pedido
from pymongo import MongoClient
db = dbase()
h_pedido = Blueprint('h_pedido', __name__)


@h_pedido.route("/admin/pedido", methods=['GET', 'POST'])
def h_pedi():
    
    if request.method == 'POST':
        h_pedido = db["h_pedido"]
        pedido = db["pedido"]
        id_pedido = request.form["id_pedido"]
        id_cliente = request.form['id_cliente']
        id_producto_list = request.form.getlist('id_producto')
        producto_list = request.form.getlist('producto')
        cantidad_list = request.form.getlist('cantidad')
        precio_list = request.form.getlist('precio')
        resultado_list = request.form.getlist('resultado')
        fecha_entrega = request.form["fecha_entrega"]
        estado =  request.form["estado"]
        # Suponiendo que todos los lists son del mismo tamaño
        for id_pedido, id_cliente, id_producto,producto, cantidad, precio, resultado , fecha_entrega,estado in zip(id_producto_list, producto_list, cantidad_list, precio_list, resultado_list):
            h_ped = H_pedido(id_pedido, id_cliente, id_producto, producto, cantidad, precio, resultado,fecha_entrega,estado)
            h_pedido.insert_one(h_ped.HpedidoDBCollection())
        
        # Eliminar todos los documentos en la colección carrito
        
        return redirect(url_for('h_pedido.gracias'))
    else:
        return render_template('admin/pedido.html')


