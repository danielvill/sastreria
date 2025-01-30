from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.medidas import Medida
from pymongo import MongoClient
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
        busto = request.form['busto']
        cintura = request.form['cintura']
        cadera = request.form['cadera']
        espalda = request.form['espalda']
        mangas = request.form["mangas"]
        comentario = request.form["comentario"]

        exist_cliente = medidas.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('cliente/in_medida.html', id_cliente=id_cliente)
        else:
            medi = Medida(id_medida, id_cliente, busto, cintura, cadera, espalda, mangas, comentario)
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
    busto = request.form["busto"]
    cintura = request.form["cintura"]
    cadera = request.form["cadera"]
    espalda = request.form['espalda']
    mangas = request.form['mangas']
    comentario = request.form["comentario"]
    
    # Verificar que todos los campos estén presentes
    if busto and cintura and cadera and espalda and mangas and comentario:
        medidas.update_one({'id_medida': edamedi },{"$set":{"busto":busto,"cintura":cintura,"cadera":cadera ,"espalda":espalda,"mangas":mangas,"comentario":comentario }})
        flash("Medida editada correctamente", "success")
        return redirect(url_for('medidas.v_admedi'))
    else:
        return render_template('admin/medida.html')

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