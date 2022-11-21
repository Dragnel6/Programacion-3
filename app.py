from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL


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

@app.route('/libro')
def libro():
    return render_template('sitio/libro.html')  

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


    sql="INSERT INTO `modelos` (`id`, `nombre`, `imagen`, `archivos`) VALUES (NULL,%s,%s,%s);"
    datos=(_nombre,_imagen.filename,_archivo.filename)

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
    cursor.execute("SELECT * FROM `modelos` WHERE id=%s",(_id))
    modelo=cursor.fetchall()
    conexion.commit()
    print(modelo)

    conexion=mysql.connect()
    cursor= conexion.cursor()
    cursor.execute("DELETE FROM modelos WHERE id=%s",(_id))
    conexion.commit()

    return redirect('/admin/libro2')          

if __name__=='__main__':
    app.run(debug=True)
        