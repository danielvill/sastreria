from flask import flash, Flask, json, send_file,session, render_template, request,Response ,jsonify, redirect, url_for
from bson import json_util
from controllers.database import Conexion as dbase
from datetime import datetime,timedelta #* Importacion de manejo de tiempo
from flask import jsonify
from reportlab.pdfgen import canvas # *pip install reportlab este es para imprimir reportes
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
from routes.cliente import cliente
from routes.producto import producto
from routes.pedido import pedido
from routes.h_pedido import h_pedido
from routes.medida import medidas
from routes.carrito import carrito


db = dbase()
app = Flask(__name__)
app.secret_key = 'sastreria'
app.config['UPLOAD_FOLDER'] = 'D:/Sastreria/static/img/producto'


# * Vista de Ingreso al sistema 
@app.route('/',methods=['GET','POST'])
def run():
    return render_template('index.html')

# * Vista de About 
@app.route('/about',methods=['GET','POST'])
def about():
    return render_template('about.html')

# * Vista de Shop 
# Esta parte su quieres retroceder 
@app.route('/shop', methods=['GET', 'POST'])
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
    
    return render_template('shop.html', productos=productos, categorias=categorias, total_pages=total_pages, current_page=page, selected_categoria=categoria, selected_subcategoria=subcategoria)


#* Este es para cerrar la sesion 
@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('login'))


#* Vista Ingreso de admin y usuarios
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['user']
        password = request.form['contraseña']
        usuario_fo = db.admin.find_one({'user':usuario,'contraseña':password})
        cliente = db.cliente.find_one({'user':usuario,'contraseña':password})
        if usuario_fo:
            session["username"] = usuario
            return redirect(url_for('cliente.v_cli'))
        elif cliente:
            session["username"] = cliente['user']
            session["id_cliente"] = cliente['id_cliente']  # Guardar id_cliente en la sesión
            print(f"cliente id_cliente: {cliente['id_cliente']}")
            return redirect(url_for('medidas.admedi'))
        else:
            flash("Contraseña incorrecta")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')




# Codigo de ingreso de cliente
app.register_blueprint(cliente)


# Codigo de ingreso de cliente
app.register_blueprint(carrito)

# Codigo de ingreso de producto
app.register_blueprint(producto)

# Codigo de ingreso de pedido
app.register_blueprint(pedido)

# Codigo de ingreso de historial de pedido
app.register_blueprint(h_pedido)

# Codigo de ingreso para el cliente 
app.register_blueprint(medidas)

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    return render_template('404.html', message=message), 404

if __name__ == '__main__':
    app.run(debug=True, port=4000)
