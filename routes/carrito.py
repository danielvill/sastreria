from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.carrito import Carrito
from pymongo import MongoClient
db = dbase()
carrito = Blueprint('carrito', __name__)

@carrito.route("/cliente/in_pedido", methods=['GET', 'POST'])
def adcarrito():
    if request.method == 'POST':
        carrito = db["carrito"]
        id_cliente = request.form['id_cliente']
        id_producto = request.form['id_producto']
        producto = request.form['producto']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        carrit = Carrito(id_cliente, id_producto, producto, cantidad, precio)
        carrito.insert_one(carrit.CarritoDBCollection())
        return redirect(url_for('carrito.v_carri'))
    else:
        return render_template('cliente/in_pedido.html')


# * Visualizar carrito
@carrito.route("/cliente/carrito")
def v_carri():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('carrito.index')) # * Redirige al usuario al inicio si no está en la sesión
    carrito = db['carrito'].find()
    return render_template("cliente/carrito.html", carrito=carrito)


# Eliminar Pedido
@carrito.route('/delete_carr/<string:eliacarr>')
def delete_carr(eliacarr):
    carrito = db["carrito"]
    
    carrito.delete_one({"id_producto":eliacarr}) 
    return redirect(url_for('carrito.v_carri'))