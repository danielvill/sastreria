from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from controllers.database import Conexion as dbase
from modules.medidas import Medida
from pymongo import MongoClient
from bson import ObjectId
from modules.blusa import Blusa
from modules.leva import Leva
from modules.camisa import Camisa
from modules.falda import Falda
from modules.pantalon import Pantalon
from modules.chaleco import Chaleco
from modules.saco import Saco
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
    
    cliente = db["cliente"].find()
    return render_template('admin/medida.html', cliente=cliente)


# Visualizar detalles del cliente por ID y que se pueda revisar
@medidas.route("/admin/medida/<id_cliente>")
def v_medi(id_cliente):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('venta.index'))
    
    # Busca el cliente por id_cliente
    cliente = db['cliente'].find_one({"id_cliente": id_cliente})
    if not cliente:
        
        return redirect(url_for('medidas.v_admedi'))

    # Busca las medidas relacionadas usando id_cliente
    blusa = db["blusa"].find_one({"id_cliente": id_cliente})
    camisa = db["camisa"].find_one({"id_cliente": id_cliente})
    chaleco = db["chaleco"].find_one({"id_cliente": id_cliente})
    leva = db["leva"].find_one({"id_cliente": id_cliente})
    pantalon = db["pantalon"].find_one({"id_cliente": id_cliente})
    falda = db["falda"].find_one({"id_cliente": id_cliente})
    saco = db["saco"].find_one({"id_cliente": id_cliente})
    # Renderiza la plantilla con los datos del cliente y medidas
    return render_template(
        "admin/v_medida.html",
        cliente=cliente,
        blusa=blusa,
        camisa=camisa,
        chaleco=chaleco,
        leva=leva,
        pantalon=pantalon,
        falda=falda,
        saco=saco
    )



# Aqui se necesita para ingresar todas las medidas
# 
# 

@medidas.route("/form/blusa",methods=['GET','POST'])
def blusa():
    if request.method == 'POST':
        blusa = db["blusa"]
        id_cliente = request.form['id_cliente']
        largo_blusa = request.form['largo_blusa']
        pecho = request.form['pecho']
        cintura = request.form['cintura']
        manga = request.form['manga']
        puño = request.form['puño']
        cuello = request.form['cuello']
        
        exist_cliente = blusa.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('form/blusa.html', id_cliente=id_cliente)

        blusa = Blusa(id_cliente, largo_blusa, pecho, cintura, manga, puño, cuello)
        db["blusa"].insert_one(blusa.BlusaDBCollection())
        flash("Medidas de blusa guardada", "success")
        return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")
        return render_template('form/blusa.html', id_cliente=id_cliente)

# Medidas de camisa
@medidas.route("/form/camisa",methods=['GET','POST'])
def camisa():
    if request.method == "POST":
        id_cliente = request.form['id_cliente']
        camisa = db["camisa"]
        largo_camisa = request.form['largo_camisa']
        ancho_espalda = request.form['ancho_espalda']
        caida_hombro = request.form['caida_hombro']
        largo_manga = request.form['largo_manga']
        puño = request.form['puño']
        ancho_brazo = request.form['ancho_brazo']
        contorno_pecho = request.form['contorno_pecho']
        cintura = request.form['cintura']
        pecho = request.form['pecho']
        cuello = request.form['cuello']
        
        exist_cliente = camisa.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo","alert")
            return render_template('form/camisa.html', id_cliente=id_cliente)

        camisa = Camisa(id_cliente, largo_camisa, ancho_espalda, caida_hombro, largo_manga, puño, ancho_brazo, contorno_pecho, cintura, pecho, cuello)
        db["camisa"].insert_one(camisa.CamisaDBCollection())
        flash("Medidas de camisa guardada", "success")
        return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")
        return render_template('form/camisa.html', id_cliente=id_cliente)
 
# Medidas de chaleco
@medidas.route("/form/chaleco",methods=['GET','POST'])
def chaleco():
    if request.method == "POST":
        id_cliente = request.form["id_cliente"]
        chaleco = db["chaleco"]
        largo = request.form["largo"]
        cadera = request.form["cadera"]
        escote = request.form["escote"]
        exist_cliente = chaleco.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('form/chaleco.html', id_cliente=id_cliente)
        
        chaleco = Chaleco(id_cliente, largo, cadera, escote)
        db["chaleco"].insert_one(chaleco.ChalecoDBCollection())
        flash("Medidas de chaleco guardada", "success")
        return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")
        return render_template('form/chaleco.html', id_cliente=id_cliente)

# Medidas de Falda
@medidas.route("/form/falda",methods=['GET','POST'])
def falda():
    if request.method == "POST":
        falda = db["falda"]
        id_cliente = request.form["id_cliente"]
        largo_cadera = request.form["largo_cadera"]
        cintura = request.form["cintura"]
        cadera = request.form["cadera"]
        vuelo = request.form["vuelo"]
        
        exist_cliente = falda.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('form/falda.html', id_cliente=id_cliente)
        
        falda = Falda(id_cliente, largo_cadera, cintura, cadera, vuelo)
        db["falda"].insert_one(falda.FaldaDBCollection())
        flash("Medidas de falda guardada", "success")
        return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")
        return render_template('form/falda.html', id_cliente=id_cliente)

# Medidas de Leva
@medidas.route("/form/leva",methods=['GET','POST'])
def leva():
    if request.method == "POST":
        leva = db["leva"]
        id_cliente = request.form["id_cliente"]
        espalda = request.form["espalda"]
        largo_saco = request.form["largo_saco"]
        ancho_espalda = request.form["ancho_espalda"]
        media_espalda = request.form["media_espalda"]
        caida_hombro = request.form["caida_hombro"]
        largo_manga = request.form["largo_manga"]
        ancho_puño = request.form["ancho_puño"]
        ancho_brazo = request.form["ancho_brazo"]
        cont_pecho = request.form["cont_pecho"]
        cintura = request.form["cintura"]
        pecho = request.form["pecho"]
        cuello = request.form["cuello"]
        
        exist_cliente = leva.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('form/leva.html', id_cliente=id_cliente)
        

        leva = Leva(id_cliente, espalda, largo_saco, ancho_espalda, media_espalda, caida_hombro, largo_manga, ancho_puño, ancho_brazo, cont_pecho, cintura, pecho, cuello)
        db["leva"].insert_one(leva.LevaDBCollection())
        flash("Medidas de leva guardada", "success")
        return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")
        return render_template('form/leva.html', id_cliente=id_cliente)

# Medidas de Pantalon
@medidas.route("/form/pantalon",methods=['GET','POST'])
def pantalon():
    if request.method == "POST":
        pantalon = db["pantalon"]
        id_cliente = request.form["id_cliente"]
        alto_rodilla = request.form["alto_rodilla"]
        largo_pantalon = request.form["largo_pantalon"]
        cintura = request.form["cintura"]
        cadera = request.form["cadera"]
        muslo = request.form["muslo"]
        rodilla = request.form["rodilla"]
        basta = request.form["basta"]
        tiro = request.form["tiro"]
        
        exist_cliente = pantalon.find_one({"id_cliente":id_cliente})
        
        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('form/pantalon.html', id_cliente=id_cliente)
        
        pantalon = Pantalon(id_cliente, alto_rodilla, largo_pantalon, cintura, cadera, muslo, rodilla, basta, tiro)
        db["pantalon"].insert_one(pantalon.PantalonDBCollection())
        flash("Medidas de pantalon guardada", "success")
        return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")
        return render_template('form/pantalon.html', id_cliente=id_cliente)
# Medidas de Saco
@medidas.route("/form/saco",methods=['GET','POST'])
def saco():
    if request.method == "POST":
        saco = db["saco"]
        id_cliente = request.form["id_cliente"]
        talla_delantero = request.form["talla_delantero"]
        largo_saco = request.form["largo_saco"]
        ancho_espalda = request.form["ancho_espalda"]
        largo_manga = request.form["largo_manga"]
        puño = request.form["puño"]
        ancho_brazo = request.form["ancho_brazo"]
        cont_pecho = request.form["cont_pecho"]
        cont_cintura = request.form["cont_cintura"]
        pecho = request.form["pecho"]
        alto_busto = request.form["alto_busto"]
        distancia_busto = request.form["distancia_busto"]
        talla_espalda = request.form["talla_espalda"]
        media_espalda = request.form["media_espalda"]
        escote = request.form["escote"]

            
        exist_cliente = saco.find_one({"id_cliente":id_cliente})    

        if exist_cliente:
            flash("Datos ya ingresados no puede ingresar de nuevo", "alert")
            return render_template('form/saco.html', id_cliente=id_cliente)
        
        saco = Saco(id_cliente, talla_delantero, largo_saco, ancho_espalda, largo_manga, puño, ancho_brazo, cont_pecho, cont_cintura, pecho, alto_busto, distancia_busto, talla_espalda, media_espalda, escote)
        db["saco"].insert_one(saco.SacoDBCollection())
        flash("Medidas de saco guardada", "success")
        return redirect(url_for('medidas.admedi'))
    else:
        id_cliente = session.get("id_cliente")
        return render_template('form/saco.html', id_cliente=id_cliente)
                    
