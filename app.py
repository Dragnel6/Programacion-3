import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
import datetime
from flask import send_from_directory

app=Flask(__name__)
app.secret_key="develoteca"
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

@app.route('/imgs/<imagen>')
def imgs(imagen):
    print(imagen)
    return send_from_directory(os.path.join('imgs'),imagen)

@app.route('/default/<file>')
def default(file):
    print(file)
    return send_from_directory(os.path.join('defaults'),file)

@app.route('/modelos/<modelo>')
def modelos(modelo):
    print(modelo)
    return send_from_directory(os.path.join('templates/sitio/archivos!'),modelo)

@app.route("/css/<archivocss>")
def css_link(archivocss):
    return send_from_directory(os.path.join('static/css/bootstrap.css'),archivocss)

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

@app.route('/calcular')
def calcular():
    return render_template('sitio/calcular.html')

@app.route('/calcular-<id>')
def calcular_id(id):

    sql = "SELECT * FROM `modelos` WHERE id = %s LIMIT 1"
    id = (id)

    conexion= mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,id)
    response=cursor.fetchall()
    conexion.commit()
    print(response)

    return render_template('sitio/calcular.html', model=response[0]);

@app.route('/admin/')
def admin_index2():
    if not 'login' in session:
        return redirect('/admin/login')
    return render_template('admin/index2.html') 

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')  

@app.route('/admin/login', methods=['POST']) 
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
    print(_usuario)
    print(_password)

    if _usuario=="admin" and _password=="123":
        session["login"]=True
        session["usuario"]="Administrador"
        return redirect("/admin")

    return render_template('admin/login.html', mensaje='El usuario o contraseña es incorreta')   

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')

@app.route('/admin/libro2')
def admin_libro2():
     
    if not 'login' in session:
        return redirect('/admin/login')

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("SELECT * FROM `modelos`")
    modelos=cursor.fetchall()
    conexion.commit()
    print(modelos)

    return render_template('admin/libro2.html', libro2=modelos) 

@app.route('/admin/libro2/guardar', methods=['POST'])
def admin_libro2_guardar():

    if not 'login' in session:
        return redirect('/admin/login')

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

@app.route('/calcular/nuevo', methods=['POST'])
def guardar_calculo():
    # Deshabilitado temporalmente
    # _archivo=request.files['txtArchivo']
    # _relleno=request.form['relleno']
    # _calidad=request.form['calidad']

    # tiempo = datetime.datetime.now()
    # horaActual = tiempo.strftime('%Y%H%M%S')

    # if _archivo.filename!="":
    #     nuevoArchivo = horaActual+"_"+_archivo.filename
    #     _archivo.save("temp/calculos/"+nuevoArchivo)

    # sql="INSERT INTO `calculos` (`archivo`, `relleno`, `calida`) VALUES (NULL,%s,%s,%s);"
    # datos=(nuevoArchivo, _relleno, _calidad)

    # conexion= mysql.connect()
    # cursor=conexion.cursor()
    # cursor.execute(sql,datos)
    # conexion.commit()

    # print(_archivo) 
    # print(_relleno)
    # print(_calidad)

    print(request.files['txtArchivo']) 
    print(request.form['relleno'])
    print(request.form['calidad'])   

    return redirect('/calcular')

@app.route('/admin/libro2/borrar', methods=['POST'])
def admin_libro2_borrar():

    if not 'login' in session:
        return redirect('/admin/login')

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
        