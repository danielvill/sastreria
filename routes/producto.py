from flask import Blueprint, render_template, request, flash, session, redirect, url_for ,current_app
from controllers.database import Conexion as dbase
from modules.producto import Producto
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import os

db = dbase()
producto = Blueprint('producto', __name__)

# Este es para lo que es las imagenes
@producto.route('/alguna_ruta')
def alguna_funcion():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
# codigo de verificacion de productos con las imagenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Este codigo es para las  imagenes
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Este codigo es para lo que es el ID
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'productoId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')


@producto.route('/admin/in_producto', methods=['GET', 'POST'])
def adpro():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('user.index'))
    
    if request.method == 'POST':
        id_producto = str(get_next_sequence('productoId')).zfill(3)
        producto = db["producto"]
        nombre = request.form['nombre']
        precio = request.form['precio']
        categoria = request.form['categoria']
        subcategoria = request.form['subcategoria']
        descripcion = request.form['descripcion']
        
        if 'imagen' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['imagen']
        if file.filename == '':
                flash('Selecciona una imagen')
                return redirect(request.url)
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_filename = filename
            
        produc = Producto(id_producto, nombre, precio, categoria,subcategoria,descripcion, imagen_filename)
        producto.insert_one(produc.ProductoDBCollection())
        flash("Producto agregado correctamente","success")
        return redirect(url_for('producto.adpro'))
    else:
        return render_template('admin/in_producto.html')

# Editar Producto
@producto.route('/edit_pro/<string:edipro>', methods=['GET', 'POST'])
def edit_pro(edipro):
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('producto.index'))
    producto = db['producto']
    producto_existente = producto.find_one({"id_producto": edipro})

    if request.method == 'POST':
        id_producto = request.form["id_producto"]
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        categoria = request.form["categoria"]
        subcategoria = request.form["subcategoria"]
        descripcion = request.form["descripcion"]

        if "imagen" in request.files and request.files['imagen'].filename != '':
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_filename = os.path.join('img', filename)
        else:
            imagen_filename = producto_existente['imagen']

        campos = [id_producto, nombre, precio, categoria,subcategoria, descripcion]

        try:
            if all(campos):
                producto.update_one({"id_producto": edipro}, {"$set": {
                    "id_producto": id_producto,
                    "nombre": nombre,
                    "precio": precio,
                    "categoria": categoria,
                    "subcategoria": subcategoria,
                    "descripcion": descripcion,
                    "imagen": imagen_filename
                }})
                flash("Producto " + nombre + " actualizado correctamente","success")
                return redirect(url_for('producto.v_product'))
            else:
                flash("Todos los campos son obligatorios","alert")
                return redirect(url_for('producto.edit_pro', edipro=edipro))
        except Exception as e:
            print(e)
            flash("Ha ocurrido un error","alert")
            return redirect(url_for('producto.edit_pro', edipro=edipro))

    return render_template('admin/edit_pro.html', producto=producto_existente)


# Eliminar Producto
@producto.route('/delete_pr/<string:eliadpro>')
def delete_pr(eliadpro):
    producto = db["producto"]
    documento = producto.find_one({"id_producto": eliadpro})
    if documento:
        nombre = documento["nombre"]
        producto.delete_one({"id_producto": eliadpro})
        flash("Producto " + nombre + " eliminado correctamente","success")
    else:
        flash("Producto no encontrado","alert")
    return redirect(url_for('producto.v_product'))

# Visualizar producto
@producto.route("/admin/producto")
def v_product():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('producto.index'))
    producto = db["producto"].find()
    return render_template('admin/producto.html', producto=producto)

