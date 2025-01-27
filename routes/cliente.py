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
        user = request.form['user']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contraseña = request.form['contraseña']

        exist_telefono = cliente.find_one({"telefono":telefono})
        exist_contraseña = cliente.find_one({"contraseña":contraseña})


        if exist_telefono:
            flash("El número de teléfono ya está registrado" ,"alert")
            return render_template('cliente/in_cliente.html')
        elif exist_contraseña:
            flash("La contraseña ya está registrada" ,"alert")
            return render_template('cliente/in_cliente.html')
        else:
            client = Cliente(id_cliente,user,apellido,telefono,correo,contraseña)
            cliente.insert_one(client.ClienteDBCollection())
            return redirect(url_for('cliente.envio'))
    else:
        return render_template('cliente/in_cliente.html')


@cliente.route("/cliente/envio",methods=['GET','POST'])
def envio():
     # * Redirige al usuario al inicio si no está en la sesión
    return render_template("cliente/envio.html")




@cliente.route('/edit_cli/<string:edacli>', methods=['GET', 'POST'])#
def edit_cli(edacli):
    cliente = db['cliente']
    user = request.form["user"]
    apellido = request.form["apellido"]
    telefono = request.form["telefono"]
    correo = request.form['correo']
    contraseña = request.form['contraseña']
    
    if user and apellido  and telefono and correo and contraseña :
        cliente.update_one({'id_cliente' : edacli}, {'$set' : {'user' : user, 'apellido' : apellido, "telefono" : telefono , "correo" : correo , "contraseña" : contraseña}})
        flash("Editado correctamente ")
        return redirect(url_for('cliente.v_cli'))
    else:
        return render_template('admin/cliente.html')


# * Eliminar cliente
@cliente.route('/delete_cli/<string:eliacli>')
def delete_cli(eliacli):
    cliente = db["cliente"]
    documento =  cliente.find_one({"id_cliente":eliacli})
    user = documento["user"]
    apellido = documento["apellido"]
    cliente.delete_one({"id_cliente":eliacli})
    flash("Cliente  "+ user +" "+ apellido + " eliminado correctamente") 
    return redirect(url_for('cliente.v_cli'))

# * Visualizar cliente
@cliente.route("/admin/cliente")
def v_cli():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('cliente.index')) # * Redirige al usuario al inicio si no está en la sesión
    cliente = db['cliente'].find()
    return render_template("admin/cliente.html", cliente=cliente)
