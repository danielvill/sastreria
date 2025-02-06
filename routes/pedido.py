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
        db.seqs.insert_one({'_id': 'pedidoId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')

@pedido.route("/cliente/carrito", methods=['GET', 'POST'])
def adpedido():
    
    if request.method == 'POST':
        id_pedido = str(get_next_sequence('pedidoId')).zfill(1)
        pedido = db["pedido"]
        carrito = db["carrito"]
        id_cliente = request.form['id_cliente']
        id_producto_list = request.form.getlist('id_producto')
        producto_list = request.form.getlist('producto')
        cantidad_list = request.form.getlist('cantidad')
        precio_list = request.form.getlist('precio')
        resultado_list = request.form.getlist('resultado')

        # Suponiendo que todos los lists son del mismo tamaño
        for id_producto, producto, cantidad, precio, resultado in zip(id_producto_list, producto_list, cantidad_list, precio_list, resultado_list):
            pedi = Pedido(id_pedido, id_cliente, id_producto, producto, cantidad, precio, resultado)
            pedido.insert_one(pedi.PedidoDBCollection())
        
        # Eliminar todos los documentos en la colección carrito
        carrito.delete_many({})

        return redirect(url_for('pedido.gracias'))
    else:
        return render_template('cliente/carrito.html')






# * Vista de Shop 
@pedido.route('/cliente/shop', methods=['GET', 'POST'])
def shop():
    page = int(request.args.get('page', 1))
    categoria = request.args.get('categoria', None)
    subcategoria = request.args.get('subcategoria', None)
    
    productos_per_page = 10
    query = {}
    
    if categoria:
        query['categoria'] = categoria
    if subcategoria:
        query['subcategoria'] = subcategoria
    
    productos = list(db["producto"].find(query).skip((page-1)*productos_per_page).limit(productos_per_page))
    total_productos = db["producto"].count_documents(query)
    total_pages = (total_productos + productos_per_page - 1) // productos_per_page
    
    categorias = {}
    for producto in db["producto"].find():
        cat = producto['categoria']
        subcat = producto['subcategoria']
        if cat not in categorias:
            categorias[cat] = []
        if subcat not in categorias[cat]:
            categorias[cat].append(subcat)
    
    return render_template('/cliente/shop.html', productos=productos, categorias=categorias, total_pages=total_pages, current_page=page, selected_categoria=categoria, selected_subcategoria=subcategoria)


# Es necesario tener un id para lo que es para este producto
# Esta es la parte donde se puede seleccionar para lo que es productos
@pedido.route('/in_pedido/<id_producto>', methods=['GET'])
def in_pedido(id_producto):
    try:
        print(f"Recibido id_producto: {id_producto}")
        producto_id = ObjectId(id_producto)
    except InvalidId:
        print("El ID del producto no es válido")
        return "El ID del producto no es válido", 400

    # Obtener el producto seleccionado
    producto = db["producto"].find_one({"_id": producto_id})
    if not producto:
        print("Producto no encontrado")
        return "Producto no encontrado", 404

    
    # Obtener productos relacionados (misma categoría y subcategoría)
    categoria = producto.get('categoria')
    subcategoria = producto.get('subcategoria')

    query = {
        "categoria": categoria,
        "subcategoria": subcategoria,
        "_id": {"$ne": producto_id}  # Excluir el producto actual
    }
    
    productos_relacionados = list(db["producto"].find(query).limit(4))  # Limitar a 4 productos relacionados, por ejemplo

    
    id_cliente = session.get('id_cliente')
    
    return render_template(
        'cliente/in_pedido.html',
        producto=producto,
        productos_relacionados=productos_relacionados,
        id_cliente=id_cliente,
        str=str  # Pasar la función str al contexto de la plantilla
    )


# Vista de admin pedido
@pedido.route("/admin/pedido",methods=['GET',"POST"])
def v_pedid():
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('pedido.index'))
    
    # Obtener todos los pedidos de la base de datos
    pedidos = db["pedido"].find()

    # Crear un diccionario para agrupar pedidos
    pedidos_agrupados = {}
    for pedido in pedidos:
        id_pedido = pedido['id_pedido']
        id_cliente = pedido['id_cliente']
        if (id_pedido, id_cliente) not in pedidos_agrupados:
            pedidos_agrupados[(id_pedido, id_cliente)] = {
                'id_pedido': id_pedido,
                'id_cliente': id_cliente,
                'productos': []
            }
        pedidos_agrupados[(id_pedido, id_cliente)]['productos'].append(pedido)

    # Convertir el diccionario en una lista para pasarlo al template
    pedidos_agrupados_list = list(pedidos_agrupados.values())
    
    return render_template('admin/pedido.html', pedidos=pedidos_agrupados_list)


# Vista cliente dando gracias
@pedido.route("/cliente/gracias",methods=['GET'])
def gracias():
    return render_template('cliente/gracias.html')

