from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.medidas import Medida
from pymongo import MongoClient
from bson import ObjectId

db = dbase()

medidas = Blueprint('medidas', __name__)
# Este codigo es para lo que es el ID
from pymongo import ReturnDocument
# Este codigo es para lo que es el ID
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        #  *Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'medidaiId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')

# Este codigo es para obtener el id y recuperarlo del cliente
@medidas.route("/cliente/in_medida",methods=['GET','POST'])
def admedi():
    if request.method == 'POST':
        id_medida = str(get_next_sequence('medidaiId')).zfill(1)
        medidas = db["medidas"]
        id_cliente = request.form['id_cliente']
        espalda = request.form['espalda']
        busto = request.form['busto']
        a_brazo = request.form['a_brazo']
        l_brazo = request.form['l_brazo']
        a_puño = request.form["a_puño"]
        t_espalda = request.form["t_espalda"]
        t_delantero = request.form["t_delantero"]
        l_pinza = request.form["l_pinza"]
        cintura = request.form["cintura"]
        l_falda = request.form["l_falda"]
        l_pierna = request.form["l_pierna"]
        a_pierna = request.form["a_pierna"]
        l_tiro = request.form["l_tiro"]
        l_rodilla = request.form["l_rodilla"]

        exist_cliente = medidas.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('cliente/in_medida.html', id_cliente=id_cliente)
        else:
            medi = Medida(id_medida, id_cliente, espalda, busto, a_brazo, l_brazo, a_puño, t_espalda, t_delantero, l_pinza, cintura, l_falda, l_pierna, a_pierna, l_tiro, l_rodilla)
            medidas.insert_one(medi.MedidaDBCollection())
            return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")  # Recuperar id_cliente de la sesión
        return render_template('cliente/in_medida.html', id_cliente=id_cliente)

@medidas.route('/edit_medi/<string:edamedi>', methods=['GET', 'POST'])
def edit_medi(edamedi):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('medidas.index'))
    
    medidas = db['medidas']
    espalda = request.form['espalda']
    busto = request.form['busto']
    a_brazo = request.form['a_brazo']
    l_brazo = request.form['l_brazo']
    a_puño = request.form["a_puño"]
    t_espalda = request.form["t_espalda"]
    t_delantero = request.form["t_delantero"]
    l_pinza = request.form["l_pinza"]
    cintura = request.form["cintura"]
    l_falda = request.form["l_falda"]
    l_pierna = request.form["l_pierna"]
    a_pierna = request.form["a_pierna"]
    l_tiro = request.form["l_tiro"]
    l_rodilla = request.form["l_rodilla"]

    if espalda and busto and a_brazo and l_brazo and a_puño and t_espalda and t_delantero and l_pinza and cintura and l_falda and l_pierna and a_pierna and l_tiro and l_rodilla :
        
        medidas.update_one({"_id": edamedi}, {"$set": {"espalda": espalda, "busto": busto, "a_brazo": a_brazo, "l_brazo": l_brazo, "a_puño": a_puño, "t_espalda": t_espalda, "t_delantero": t_delantero, "l_pinza": l_pinza, "cintura": cintura, "l_falda": l_falda, "l_pierna": l_pierna, "a_pierna": a_pierna, "l_tiro": l_tiro, "l_rodilla": l_rodilla }})
        flash("Medida editada correctamente", "success")
        return redirect(url_for('medidas.v_medi'))
    else:
        return render_template('admin/v_medida.html')

# Visualizar medidas
@medidas.route("/cliente/medida")
def v_medida():
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('medidas.index'))
    
    # Obtener id_cliente de la sesión este es para mostrar al cliente que ingreso la medida
    id_cliente = session.get("id_cliente")
    
    # Filtrar las medidas por id_cliente
    medidas = db["medidas"].find({"id_cliente": id_cliente})
    
    return render_template('cliente/medida.html', medidas=medidas)

# Vista de medida para editar lo que es clientes
@medidas.route("/admin/medida")
def v_admedi():
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('medidas.index'))
    
    medidas = db["medidas"].find()
    return render_template('admin/medida.html', medidas=medidas)


# Visualizar detalles del cliente por ID y que se pueda revisar 
@medidas.route("/admin/medida/<id>")
def v_medi(id):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('venta.index'))
    medida = db['medidas'].find_one({"_id": ObjectId(id)})
    return render_template("admin/v_medida.html", medida=medida)
