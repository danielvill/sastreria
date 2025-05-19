from datetime import datetime
from flask import Blueprint, make_response, render_template, request, flash, session, redirect, url_for,send_file
from controllers.database import Conexion as dbase
from modules.pedido import Pedido
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import io 
from reportlab.lib.pagesizes import A4 ,letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


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

# Este es para procesar el formulario de lo que son pedidos para este apartado
@pedido.route("/cliente/carrito", methods=['GET', 'POST'])
def adpedido():
    
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_producto_list = request.form.getlist('id_producto')
        producto_list = request.form.getlist('producto')
        cantidad_list = request.form.getlist('cantidad')
        precio_list = request.form.getlist('precio')
        resultado_list = request.form.getlist('resultado')
        
        # Verificar disponibilidad de productos
        productos = db["producto"]
        error_message = None
        
        for i, (id_producto, cantidad) in enumerate(zip(id_producto_list, cantidad_list)):
            # Convertir cantidad a entero
            cantidad_solicitada = int(cantidad)
            
            # Obtener producto de la base de datos
            producto_db = productos.find_one({"id_producto": id_producto})
            
            if producto_db:
                # Convertir la cantidad de string a entero
                cantidad_disponible = int(producto_db.get("cantidad", 0))
                
                # Verificar si hay suficiente cantidad
                if cantidad_solicitada > cantidad_disponible:
                    error_message = f"No hay suficiente stock del producto '{producto_list[i]}'. Cantidad disponible: {cantidad_disponible}. por favor eliminar el producto"
                    break
        
        # Si no hay errores, proceder con la creación del pedido
        if error_message is None:
            id_pedido = str(get_next_sequence('pedidoId')).zfill(1)
            pedido = db["pedido"]
            carrito = db["carrito"]
            
            for id_producto, producto, cantidad, precio, resultado in zip(id_producto_list, producto_list, cantidad_list, precio_list, resultado_list):
                cantidad_int = int(cantidad)
                
                # Crear el pedido
                pedi = Pedido(id_pedido, id_cliente, id_producto, producto, cantidad, precio, resultado)
                pedido.insert_one(pedi.PedidoDBCollection())
                
                # Obtener producto actual
                producto_actual = productos.find_one({"id_producto": id_producto})
                if producto_actual:
                    # Calcular la nueva cantidad
                    cantidad_actual = int(producto_actual.get("cantidad", 0))
                    nueva_cantidad = cantidad_actual - cantidad_int
                    
                    # Actualizar con el nuevo valor numérico
                    productos.update_one(
                        {"id_producto": id_producto},
                        {"$set": {"cantidad": str(nueva_cantidad)}}  # Mantener como string si así está en la BD
                    )
            
            # Eliminar todos los documentos en la colección carrito
            carrito.delete_many({})
            return redirect(url_for('pedido.gracias'))
        else:
            # Devolver a la página con mensaje de error
            return render_template('cliente/carrito.html', error_message=error_message)
    else:
        return render_template('cliente/carrito.html')
    

def generate_pdf(id_pedido, id_cliente, id_producto_list, producto_list, cantidad_list, precio_list, resultado_list):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    # Aquí puedes personalizar el contenido del PDF
    p.drawString(100, 750, f"Pedido ID: {id_pedido}")
    p.drawString(100, 730, f"Cliente ID: {id_cliente}")
    
    y = 700
    for id_producto, producto, cantidad, precio, resultado in zip(id_producto_list, producto_list, cantidad_list, precio_list, resultado_list):
        p.drawString(100, y, f"Producto: {producto} - Cantidad: {cantidad} - Precio: {precio} - Resultado: {resultado}")
        y -= 20
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.getvalue()




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
@pedido.route("/cliente/gracias", methods=['GET', 'POST'])
def gracias():
    # Consulta todos los pedidos (para el método GET)
    pidi = list(db["pedido"].find())

    # Obtener el id_cliente del primer pedido (si existe)
    id_cliente = pidi[0]['id_cliente'] if pidi else None

    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        
        # Consulta la base de datos para obtener los pedidos del cliente
        pedidos = list(db['pedido'].find({"id_cliente": id_cliente}))

        if pedidos:
            # Crear un PDF en memoria
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            style_title = styles['Title']
            style_normal = styles['Normal']

            # Título del PDF
            
            cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
            # Código del cliente
            nombre_cliente = cliente_data.get("apellido", "Cliente") if cliente_data else "Cliente"
            
            # Agrega la imagen
            imagen = Image('static/img/lucero.jpg', width=100, height=200)
            imagen.hAlign = 'CENTER'
            elements.append(imagen)
            elements.append(Spacer(1, 12))
           
            elements.append(Paragraph(f"Nombre del cliente - {nombre_cliente}", styles['Heading2']))
            elements.append(Spacer(1, 12))

            # Crear la tabla con los datos de los pedidos
            data = [['Producto', 'Cantidad', 'Precio', 'Resultado']]
            total = 0

            for pedido in pedidos:
                producto = pedido['producto']
                cantidad = pedido['cantidad']
                precio = pedido['precio']
                resultado = pedido['resultado']
                total += float(resultado)  # Sumar al total
                data.append([producto, cantidad, precio, resultado])

            # Añadir la fila del total
            data.append(['', '', 'Total:', f"{total:.2f}"])

            # Crear la tabla
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)
            # Añadir fecha de generación
            elements.append(Spacer(1, 12))
            
            elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
            doc.build(elements)
            
            # Mover el puntero al inicio del buffer
            buffer.seek(0)

            # Enviar el PDF como respuesta
            return send_file(buffer, as_attachment=True, download_name='comprobante.pdf', mimetype='application/pdf')

    # Renderizar la plantilla para el método GET
    return render_template('cliente/gracias.html', pidi=pidi, id_cliente=id_cliente)