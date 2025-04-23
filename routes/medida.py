from datetime import datetime
from flask import Blueprint, make_response, render_template, request, flash, session, redirect, url_for,send_file
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
from reportlab.lib.pagesizes import A4 ,letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
from io import BytesIO

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

# PDF para ver las medidas de blusa 
@medidas.route("/generar_pdf_blusa", methods=['GET'])
def generar_pdf_blusa():
    # Obtener el ID del cliente desde el parámetro GET
    id_cliente = request.args.get('id_cliente')
    
    if not id_cliente:
        flash("ID de cliente no proporcionado", "alert")
        return redirect(url_for('medidas.v_admedi'))
    
    # Obtener los datos de la blusa desde MongoDB
    blusa_data = db["blusa"].find_one({"id_cliente": id_cliente})
    
    if not blusa_data:
        flash("No se encontraron datos de blusa para este cliente", "alert")
        return redirect(url_for('medidas.v_medi', id_cliente=id_cliente))
    
    # Obtener datos del cliente para el encabezado
    cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
    nombre_cliente = cliente_data.get("nombre", "Cliente") if cliente_data else "Cliente"
    
    # Crear el documento PDF en memoria
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Añadir título
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Medidas de Blusa - {nombre_cliente}", styles['Heading1']))
    elements.append(Paragraph(f"ID Cliente: {id_cliente}", styles['Heading2']))
    
    # Preparar los datos para la tabla
    data = [
        ["Campo", "Medida"],
        ["Largo Blusa", blusa_data["largo_blusa"] + " cm"],
        ["Pecho", blusa_data["pecho"] + " cm"],
        ["Cintura", blusa_data["cintura"] + " cm"],
        ["Manga", blusa_data["manga"] + " cm"],
        ["Puño", blusa_data["puño"] + " cm"],
        ["Cuello", blusa_data["cuello"] + " cm"]
    ]
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Añadir fecha de generación
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Regresar al inicio del buffer
    pdf_buffer.seek(0)
    
    # Enviar el archivo directamente como respuesta
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"medidas_blusa_{id_cliente}.pdf",
        mimetype='application/pdf'
    )

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

# Generar pdf de camisa
@medidas.route("/generar_pdf_camisa", methods=['GET'])
def generar_pdf_camisa():
    # Obtener el ID del cliente desde el parámetro GET
    id_cliente = request.args.get('id_cliente')
    
    if not id_cliente:
        flash("ID de cliente no proporcionado", "alert")
        return redirect(url_for('medidas.v_admedi'))
    
    # Obtener los datos de la camisa desde MongoDB
    camisa_data = db["camisa"].find_one({"id_cliente": id_cliente})
    
    if not camisa_data:
        flash("No se encontraron datos de camisa para este cliente", "alert")
        return redirect(url_for('medidas.v_medi', id_cliente=id_cliente))
    
    # Obtener datos del cliente para el encabezado
    cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
    nombre_cliente = cliente_data.get("nombre", "Cliente") if cliente_data else "Cliente"
    
    # Crear el documento PDF en memoria
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Añadir título
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Medidas de camisa - {nombre_cliente}", styles['Heading1']))
    elements.append(Paragraph(f"ID Cliente: {id_cliente}", styles['Heading2']))
    
    # Preparar los datos para la tabla
    data = [
        ["Campo", "Medida"],
        ["Largo camisa", camisa_data["largo_camisa"] + " cm"],
        ["Ancho de espalda", camisa_data["ancho_espalda"] + " cm"],
        ["Caida de hombro", camisa_data["caida_hombro"] + " cm"],
        ["Largo de manga", camisa_data["largo_manga"] + " cm"],
        ["Puño", camisa_data["puño"] + " cm"],
        ["Ancho de brazo", camisa_data["ancho_brazo"] + " cm"],
        ["Contorno de pecho", camisa_data["contorno_pecho"] + " cm"],
        ["Cintura", camisa_data["cintura"] + " cm"],
        ["Pecho", camisa_data["pecho"] + " cm"],
        ["Cuello", camisa_data["cuello"] + " cm"],
    ]
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Añadir fecha de generación
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Regresar al inicio del buffer
    pdf_buffer.seek(0)
    
    # Enviar el archivo directamente como respuesta
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"medidas_camisa_{id_cliente}.pdf",
        mimetype='application/pdf'
    )




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

# PDF en chaleco
@medidas.route("/generar_pdf_chaleco", methods=['GET'])
def generar_pdf_chaleco():
    # Obtener el ID del cliente desde el parámetro GET
    id_cliente = request.args.get('id_cliente')
    
    if not id_cliente:
        flash("ID de cliente no proporcionado", "alert")
        return redirect(url_for('medidas.v_admedi'))
    
    # Obtener los datos de la chaleco desde MongoDB
    chaleco_data = db["chaleco"].find_one({"id_cliente": id_cliente})
    
    if not chaleco_data:
        flash("No se encontraron datos de chaleco para este cliente", "alert")
        return redirect(url_for('medidas.v_medi', id_cliente=id_cliente))
    
    # Obtener datos del cliente para el encabezado
    cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
    nombre_cliente = cliente_data.get("nombre", "Cliente") if cliente_data else "Cliente"
    
    # Crear el documento PDF en memoria
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Añadir título
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Medidas de chaleco - {nombre_cliente}", styles['Heading1']))
    elements.append(Paragraph(f"ID Cliente: {id_cliente}", styles['Heading2']))
    
    # Preparar los datos para la tabla
    data = [
        ["Campo", "Medida"],
        ["Largo", chaleco_data["largo"] + " cm"],
        ["Cadera", chaleco_data["cadera"] + " cm"],
        ["Escote", chaleco_data["escote"] + " cm"]
    ]
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Añadir fecha de generación
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Regresar al inicio del buffer
    pdf_buffer.seek(0)
    
    # Enviar el archivo directamente como respuesta
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"medidas_chaleco_{id_cliente}.pdf",
        mimetype='application/pdf'
    )


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
        
# Generar PDF falda

@medidas.route("/generar_pdf_falda", methods=['GET'])
def generar_pdf_falda():
    # Obtener el ID del cliente desde el parámetro GET
    id_cliente = request.args.get('id_cliente')
    
    if not id_cliente:
        flash("ID de cliente no proporcionado", "alert")
        return redirect(url_for('medidas.v_admedi'))
    
    # Obtener los datos de la falda desde MongoDB
    falda_data = db["falda"].find_one({"id_cliente": id_cliente})
    
    if not falda_data:
        flash("No se encontraron datos de falda para este cliente", "alert")
        return redirect(url_for('medidas.v_medi', id_cliente=id_cliente))
    
    # Obtener datos del cliente para el encabezado
    cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
    nombre_cliente = cliente_data.get("nombre", "Cliente") if cliente_data else "Cliente"
    
    # Crear el documento PDF en memoria
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Añadir título
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Medidas de falda - {nombre_cliente}", styles['Heading1']))
    elements.append(Paragraph(f"ID Cliente: {id_cliente}", styles['Heading2']))
    
    # Preparar los datos para la tabla
    data = [
        ["Campo", "Medida"],
        ["Largo de cadera", falda_data["largo_cadera"] + " cm"],
        ["Cintura", falda_data["cintura"] + " cm"],
        ["Cadera", falda_data["cadera"] + " cm"],
        ["Vuelo", falda_data["vuelo"] + " cm"]
    ]
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Añadir fecha de generación
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Regresar al inicio del buffer
    pdf_buffer.seek(0)
    
    # Enviar el archivo directamente como respuesta
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"medidas_falda_{id_cliente}.pdf",
        mimetype='application/pdf'
    )



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

# PDF de leva
@medidas.route("/generar_pdf_leva", methods=['GET'])
def generar_pdf_leva():
    # Obtener el ID del cliente desde el parámetro GET
    id_cliente = request.args.get('id_cliente')
    
    if not id_cliente:
        flash("ID de cliente no proporcionado", "alert")
        return redirect(url_for('medidas.v_admedi'))
    
    # Obtener los datos de la leva desde MongoDB
    leva_data = db["leva"].find_one({"id_cliente": id_cliente})
    
    if not leva_data:
        flash("No se encontraron datos de leva para este cliente", "alert")
        return redirect(url_for('medidas.v_medi', id_cliente=id_cliente))
    
    # Obtener datos del cliente para el encabezado
    cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
    nombre_cliente = cliente_data.get("nombre", "Cliente") if cliente_data else "Cliente"
    
    # Crear el documento PDF en memoria
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Añadir título
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Medidas de leva - {nombre_cliente}", styles['Heading1']))
    elements.append(Paragraph(f"ID Cliente: {id_cliente}", styles['Heading2']))
    
    # Preparar los datos para la tabla
    data = [
        ["Campo", "Medida"],
        ["Espalda", leva_data["espalda"] + " cm"],
        ["Largo de saco", leva_data["largo_saco"] + " cm"],
        ["Ancho de espalda", leva_data["ancho_espalda"] + " cm"],
        ["Media de espalda", leva_data["media_espalda"] + " cm"],
        ["Caida de hombro", leva_data["caida_hombro"] + " cm"],
        ["Largo de manga", leva_data["largo_manga"] + " cm"],
        ["Ancho de puño", leva_data["ancho_puño"] + " cm"],
        ["Ancho de brazo", leva_data["ancho_brazo"] + " cm"],
        ["Cont de pecho", leva_data["cont_pecho"] + " cm"],
        ["Cintura", leva_data["cintura"] + " cm"],
        ["Pecho", leva_data["pecho"] + " cm"],
        ["Cuello", leva_data["cuello"] + " cm"]
    ]
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Añadir fecha de generación
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Regresar al inicio del buffer
    pdf_buffer.seek(0)
    
    # Enviar el archivo directamente como respuesta
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"medidas_leva_{id_cliente}.pdf",
        mimetype='application/pdf'
    )

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

# PDF de pantalon

@medidas.route("/generar_pdf_pantalon", methods=['GET'])
def generar_pdf_pantalon():
    # Obtener el ID del cliente desde el parámetro GET
    id_cliente = request.args.get('id_cliente')
    
    if not id_cliente:
        flash("ID de cliente no proporcionado", "alert")
        return redirect(url_for('medidas.v_admedi'))
    
    # Obtener los datos de la pantalon desde MongoDB
    pantalon_data = db["pantalon"].find_one({"id_cliente": id_cliente})
    
    if not pantalon_data:
        flash("No se encontraron datos de pantalon para este cliente", "alert")
        return redirect(url_for('medidas.v_medi', id_cliente=id_cliente))
    
    # Obtener datos del cliente para el encabezado
    cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
    nombre_cliente = cliente_data.get("nombre", "Cliente") if cliente_data else "Cliente"
    
    # Crear el documento PDF en memoria
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Añadir título
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Medidas de pantalon - {nombre_cliente}", styles['Heading1']))
    elements.append(Paragraph(f"ID Cliente: {id_cliente}", styles['Heading2']))
    
    # Preparar los datos para la tabla
    data = [
        ["Campo", "Medida"],
        ["Alto de rodilla", pantalon_data["alto_rodilla"] + " cm"],
        ["Largo de pantalon", pantalon_data["largo_pantalon"] + " cm"],
        ["Cintura", pantalon_data["cintura"] + " cm"],
        ["Cadera", pantalon_data["cadera"] + " cm"],
        ["Muslo", pantalon_data["muslo"] + " cm"],
        ["Rodilla", pantalon_data["rodilla"] + " cm"],
        ["Basta", pantalon_data["basta"] + " cm"],
        ["Tiro", pantalon_data["tiro"] + " cm"]
    ]
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Añadir fecha de generación
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Regresar al inicio del buffer
    pdf_buffer.seek(0)
    
    # Enviar el archivo directamente como respuesta
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"medidas_pantalon_{id_cliente}.pdf",
        mimetype='application/pdf'
    )


# Medidas de Saco

@medidas.route("/form/saco",methods=['GET','POST'])
def saco():
    if request.method == "POST":
        saco = db["saco"]
        id_cliente = request.form["id_cliente"]
        talla_dealntero = request.form["talla_dealntero"]
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
                    

# PDF DE SACO
@medidas.route("/generar_pdf_saco", methods=['GET'])
def generar_pdf_saco():
    # Obtener el ID del cliente desde el parámetro GET
    id_cliente = request.args.get('id_cliente')
    
    if not id_cliente:
        flash("ID de cliente no proporcionado", "alert")
        return redirect(url_for('medidas.v_admedi'))
    
    # Obtener los datos de la saco desde MongoDB
    saco_data = db["saco"].find_one({"id_cliente": id_cliente})
    
    if not saco_data:
        flash("No se encontraron datos de saco para este cliente", "alert")
        return redirect(url_for('medidas.v_medi', id_cliente=id_cliente))
    
    # Obtener datos del cliente para el encabezado
    cliente_data = db["cliente"].find_one({"id_cliente": id_cliente})
    nombre_cliente = cliente_data.get("nombre", "Cliente") if cliente_data else "Cliente"
    
    # Crear el documento PDF en memoria
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    elements = []
    
    # Añadir título
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Medidas de saco - {nombre_cliente}", styles['Heading1']))
    elements.append(Paragraph(f"ID Cliente: {id_cliente}", styles['Heading2']))
    
    # Preparar los datos para la tabla
    data = [
        ["Campo", "Medida"],
        ["Talla delantero", saco_data["talla_dealntero"] + " cm"],
        ["Largo de saco", saco_data["largo_saco"] + " cm"],
        ["Ancho de espalda", saco_data["ancho_espalda"] + " cm"],
        ["Largo de manga", saco_data["largo_manga"] + " cm"],
        ["Puño", saco_data["puño"] + " cm"],
        ["Ancho de brazo", saco_data["ancho_brazo"] + " cm"],
        ["Cont de pecho", saco_data["cont_pecho"] + " cm"],
        ["Cont de cintura", saco_data["cont_cintura"] + " cm"],
        ["Pecho", saco_data["pecho"] + " cm"],
        ["Alto de busto", saco_data["alto_busto"] + " cm"],
        ["Distancia de busto", saco_data["distancia_busto"] + " cm"],
        ["Talla de espalda", saco_data["talla_espalda"] + " cm"],
        ["Media de espalda", saco_data["media_espalda"] + " cm"],
        ["Escote", saco_data["escote"] + " cm"],
        
        #distancia_busto
        
    ]
    
    # Crear la tabla
    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (1, 0), 12),
        ('BACKGROUND', (0, 1), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ]))
    
    elements.append(table)
    
    # Añadir fecha de generación
    elements.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal']))
    
    # Construir el PDF
    doc.build(elements)
    
    # Regresar al inicio del buffer
    pdf_buffer.seek(0)
    
    # Enviar el archivo directamente como respuesta
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"medidas_saco_{id_cliente}.pdf",
        mimetype='application/pdf'
    )