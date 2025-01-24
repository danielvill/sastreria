from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.pedido import Pedido
from pymongo import MongoClient
db = dbase()
pedido = Blueprint('pedido', __name__)



# Este codigo es para lo que es el ID
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        #  *Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'pedidoiId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')

@pedido.route("/cliente/in_pedido",methods=['GET', 'POST'])
def adpedido():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('pedido.index'))

    if request.method == "POST":
        id_pedido = str(get_next_sequence('pedidoId')).zfill(1)
        pedido = db["pedido"]
        user = request.form["user"]
        telefono = request.form["telefono"]
        
        # Recogemos los productos
        id_producto = request.form.getlist("id_producto")
        producto = request.form.getlist("producto")
        cantidad = request.form.getlist("cantidad")
        precio =request.form.getlist("precio")
        resultado = request.form.getlist("resultado")

        productos=[]
        for i in range(len(id_producto)):
            producto = {
                "id_producto":id_producto[i] if i < len(id_producto) else '',
                "producto": producto[i] if i < len(producto) else '',
                "cantidad": cantidad[i] if i < len(cantidad) else '',
                "precio": precio[i] if i < len(precio) else '',
                "resultado": resultado[i] if i < len(resultado) else ''
            }
            productos.append(producto)

        # Creamos el documento para guardar en la venta
        pedido_documento ={
            "id_pedido": id_pedido,
            "user": user,
            "telefono": telefono,
            "productos": productos
        }   
        # Insertamos el documento en la coleccion de pedido
        pedido.insert_one(pedido_documento)
        
        flash("Pedido registrado con exito")
        return redirect(url_for('pedido.adpedido'))
    else:
        return render_template('cliente/in_pedido.html')


# Visualizar pedido
@pedido.route("/admin/pedido")
def v_pedido():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('pedido.index'))
    pedido = db["pedido"].find()
    return render_template('cliente/pedido.html', pedido=pedido)

