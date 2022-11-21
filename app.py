import os
from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
import datetime
from flask import send_from_directory

app=Flask(__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates\sitio\img'),imagen)

@app.route('/libro')
def libro():

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `modelos`")
    modelos=cursor.fetchall()
    conexion.commit()

    return render_template('sitio/libro.html', libro=modelos)  

@app.route('/materiales')
def materiales():
    return render_template('sitio/materiales.html')      
 

@app.route('/contacto')
def contacto():
    return render_template('sitio/contacto.html')    

@app.route('/admin/')
def admin_index2():
    return render_template('admin/index2.html') 

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')  

@app.route('/admin/libro2')
def admin_libro2():

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `modelos`")
    modelos=cursor.fetchall()
    conexion.commit()
    print(modelos)

    return render_template('admin/libro2.html', libro2=modelos) 

@app.route('/admin/libro2/guardar', methods=['POST'])
def admin_libro2_guardar():
    _nombre=request.form['txtNombre']
    _imagen=request.files['txtImagen']
    _archivo=request.files['txtArchivo']

    tiempo = datetime.datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')

    if _imagen.filename!="":
        nuevoNombre = horaActual+"_"+_imagen.filename
        _imagen.save("templates/sitio/img/"+nuevoNombre)
    
    if _archivo.filename!="":
        nuevoArchivo = horaActual+"_"+_archivo.filename
        _archivo.save("templates/sitio/archivos!/"+nuevoArchivo)

    sql="INSERT INTO `modelos` (`id`, `nombre`, `imagen`, `archivos`) VALUES (NULL,%s,%s,%s);"
    datos=(_nombre,nuevoNombre,nuevoArchivo)

    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_nombre) 
    print(_imagen) 
    print(_archivo)      

    return redirect('/admin/libro2') 

@app.route('/admin/libro2/borrar', methods=['POST'])
def admin_libro2_borrar():

    _id=request.form['txtID']
    print(_id)

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT imagen FROM `modelos` WHERE id=%s",(_id))
    modelo=cursor.fetchall()
    conexion.commit()
    print(modelo)

    if os.path.exists("templates/sitio/img/"+str(modelo[0][0])):
        os.unlink("templates/sitio/img/"+str(modelo[0][0]))

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT archivos FROM `modelos` WHERE id=%s",(_id))
    modelo=cursor.fetchall()
    conexion.commit()
    print(modelo)

    if os.path.exists("templates/sitio/archivos!/"+str(modelo[0][0])):
        os.unlink("templates/sitio/archivos!/"+str(modelo[0][0]))    

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("DELETE FROM modelos WHERE id=%s",(_id))
    conexion.commit()

    return redirect('/admin/libro2')          

if __name__=='__main__':
    app.run(debug=True)
        