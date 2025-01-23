from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.cliente import Cliente
from pymongo import MongoClient
db = dbase()
cliente = Blueprint('cliente', __name__)



# Este codigo es para lo que es el ID
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        #  *Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'cliId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')

@cliente.route("/cliente/in_cliente",methods=['GET','POST'])
def adcli():
    
    
    if request.method == 'POST':
        id_cliente = str(get_next_sequence('cliId')).zfill(1)
        cliente = db["cliente"]
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        exist_telefono = cliente.find_one({"telefono":telefono})

        if exist_telefono:
            flash("El número de teléfono ya está registrado")
            return render_template('cliente/in_cliente.html')
        else:
            client = Cliente(id_cliente,nombre,apellido,telefono,correo,contraseña)
            cliente.insert_one(client.ClienteDBCollection())
            flash("Cliente registrado")
            return redirect(url_for('cliente.adcli'))
    else:
        return render_template('cliente/in_cliente.html')

@cliente.route('/edit_cli/<string:edacli>', methods=['GET', 'POST'])#
def edit_cli(edacli):
    cliente = db['cliente']
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    if nombre and apellido  and telefono and correo and contraseña :
        cliente.update_one({'id_cliente' : edacli}, {'$set' : {'nombre' : nombre, 'apellido' : apellido, "telefono" : telefono , "correo" : correo , "contraseña" : contraseña}})
        flash("Editado correctamente ")
        return redirect(url_for('cliente.v_user'))
    else:
        return render_template('admin/cliente.html')


# * Eliminar cliente
@cliente.route('/delete_cli/<string:eliacli>')
def delete_cli(eliacli):
    cliente = db["cliente"]
    documento =  cliente.find_one({"id_cliente":eliacli})
    nombre = documento["nombre"]
    apellido = documento["apellido"]
    cliente.delete_one({"id_cliente":eliacli})
    flash("Cliente  "+ nombre +" "+ apellido + " eliminado correctamente") 
    return redirect(url_for('cliente.v_cli'))

# * Visualizar cliente
@cliente.route("/admin/cliente")
def v_cli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('cliente.index'))  # * Redirige al usuario al inicio si no está en la sesión
    cliente = db['cliente'].find()
    return render_template("admin/cliente.html", cliente=cliente)
