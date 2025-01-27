from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.pedido import Pedido
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
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

@pedido.route("/cliente/carrito",methods=['GET', 'POST'])
def adpedido():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('pedido.index'))
   
    # Agregar codigo ya que cambie lo que es la base de datos 

    return render_template('cliente/carrito.html')


# Visualizar pedido

# * Vista de Shop 
@pedido.route('/cliente/shop', methods=['GET', 'POST'])
def shop():
    page = int(request.args.get('page', 1))
    productos_per_page = 10
    productos = list(db["producto"].find().skip((page-1)*productos_per_page).limit(productos_per_page))
    total_productos = db["producto"].count_documents({})
    total_pages = (total_productos + productos_per_page - 1) // productos_per_page
    
    categorias = {}
    for producto in db["producto"].find():
        categoria = producto['categoria']
        subcategoria = producto['subcategoria']
        if categoria not in categorias:
            categorias[categoria] = []
        if subcategoria not in categorias[categoria]:
            categorias[categoria].append(subcategoria)
    
    return render_template('cliente/shop.html', productos=productos, categorias=categorias, total_pages=total_pages, current_page=page)


# Es necesario tener un id para lo que es para este producto
@pedido.route('/in_pedido/<id_producto>', methods=['GET'])
def in_pedido(id_producto):
    try:
        producto_id = ObjectId(id_producto)
    except InvalidId:
        return "El ID del producto no es válido", 400
    producto = db["producto"].find_one({"_id": producto_id})
    if not producto:
        return "Producto no encontrado", 404
    id_cliente = session.get('id_cliente')
    return render_template('cliente/in_pedido.html', producto=producto,id_cliente=id_cliente)



