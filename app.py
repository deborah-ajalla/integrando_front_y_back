# --> Se diseña un sript para la parte BACKEND que utiliza FLASK de PYTHON.✔ 
# --> Se conecta con base de datos MySQl (Workbench- Xampp). ✔ 
# --> Se conecta con FRONTEND y navega en el menú y las secciones ✔ 
# --> Programa: ◼ Login  ✔ 
#               ◼ Registro de Nuevo Usuario ✔ 
#               ◼ Inicio como Admiistrador ✔
#               ◼ Acceso a panel de Tareas ✔
#               ◼ consultas CRUD ✔
#               ◼ crea, edita, modifica y elimina usuarios ✔
# --> Año:2024 <--

#---------------------------------------------------------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
# 🔸 redirect y url_for =>redireccionan a una pagina.
# 🔸 flash => es de flask, y sirve para enviar msjs
# 🔸 request => para tomar los datos que se ingresan en formualarios
from datetime import datetime    #--> para poder registrar fecha y hora en las taraes

#-----------------------------------
#inicializo la aplicacion
app = Flask(__name__)
#-----------------------------------
# Configuro la conexión
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'usuarios_flask'  #nombre que le puse a la db---
mysql = MySQL(app)
#-----------------------------------
# Configuración de sesión
app.secret_key = 'mysecretkey'
#-----------------------------------

# Ruta principal --> abre el navgador con la página frontend <--
@app.route('/', methods=['GET'])
def home():
    return render_template('index_front.html')
#-----------------------------------
# Rutas del frontend  
# --> DIRECCIONAN A PORTFOLIOS <--
@app.route('/portfolio_juan')
def portfolio_juan():
    return render_template('/portfolios/juan.html')
#-----------------------------------
@app.route('/portfolio_deborah')
def portfolio_deborah():
    return render_template('/portfolios/deborah.html')
#-----------------------------------
@app.route('/portfolio_maximiliano')
def portfolio_maximiliano():
    return render_template('/portfolios/maximiliano.html')
#-----------------------------------
@app.route('/portfolio_david')
def portfolio_david():
    return render_template('/portfolios/david.html')
#-----------------------------------
#--> SECCIÓN SERVICIOS <--
@app.route ('/disenio')
def disenio():
    return render_template ('/servicios/disenio.html')
#-----------------------------------
@app.route('/marketing')
def marketing():
    return render_template('/servicios/marketing.html')
#-----------------------------------
@app.route('/contenido_digital')
def contenido_digital():
    return render_template('/servicios/contenido_digital.html')
#-----------------------------------

# Ruta back  --> direcciona a la pantalla LOGIN del backend <--
@app.route('/back', methods=['GET'])
def back():
     return render_template('index.html')

#-----------------------------------
# Ruta para listado
@app.route('/listado', methods=['GET'])
def list():
    if 'email' in session:
        if session['email'] == 'maxi@gmail.com': 
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT idusuarios, email, password, nombre, apellido FROM usuarios')
                contacts = cursor.fetchall()
                cursor.close()
                
                return render_template('listado.html', contacts=contacts)
            
            except Exception as e:
                return render_template('index.html', message=f"Error al obtener datos: {str(e)}")
        
        else:
             return redirect (url_for('tareas'))
    
    else:
        return render_template('index.html', message="Debes iniciar sesión para acceder a esta página.")
#-----------------------------------
# Ruta para login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email'] #toma dato ingresa en el formulario
    password = request.form['password']

     #--- query ---
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = %s AND password = %s', (email, password)) 
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
        session['email'] = email
        session['nombre'] = user[3]
        session['apellido'] = user[4]

        return redirect(url_for('list'))
    else:
       return render_template('index.html', message="Las credenciales no son correctas")
#-----------------------------------
# Ruta para página de tareas
@app.route('/tareas')
def tareas():
    email = session ['email']  #toma los datos del email que inició sesion
    # --> conecta con bd <--
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tareas WHERE email= %s", [email]) #selescciona los datos de tabla tareas del email que inició sesion
    tareas = cursor.fetchall()

    #--> convierto los datos a diccioonario <--
    lista_insertar = []
    columnas = [column[0] for column in cursor.description] #recorre las columnas con el contenido que tiene
    for record in tareas:
        lista_insertar.append(dict(zip(columnas, record))) #agrega los datos de la lista al diccionario con clave columna y valor = record
    cursor.close() #cierra conexion
    return render_template('tareas.html', tareas= lista_insertar)
#-----------------------------------
#ruta para BORRAR Nueva Tarea ❤❤
@app.route('/delete_tarea', methods=['POST'])
def delete_tarea():
    #--> conecta con bd <--
    cursor = mysql.connection.cursor()
    id = request.form['id']  # tomo el id de la tarea que esta hidden
    sql = "DELETE FROM tareas WHERE idtareas = %s"
    data = (id, ) #se pone coma porque se esperan 2 parametros.
    cursor.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('tareas'))
#-----------------------------------
#ruta para agregar una nueva tarea  ❤❤ 
@app.route('/nueva_tarea', methods=['POST'])
def nueva_tarea():
    titulo = request.form ['titulo']  #creo una variable en donde guardo lo que se ingresa en el campo titulo.
    descripcion = request.form ['descripcion']

    email = session ['email'] # toma el email de la sesion iniciada
    fecha = datetime.now()    # creo variable para guardar la fecha en que se crea la tarea

    date_tarea = fecha.strftime ("%Y-%m-%d %H:%M:%S") # establezco formato que quiero para ver la fecha 
                                                      # y para el horario las letras son mayusculas
    
    if titulo and descripcion and email:
        #---> conecto con bd ❤❤ <---
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO tareas (email, titulo, descripcion, date_tarea) VALUES (%s, %s, %s, %s)" #instrucción
        data = (email, titulo, descripcion, date_tarea) #guardo los datos
        cursor.execute (sql, data) #ejecuta la instrucción con los parametros de insert y los datos recopilados
        mysql.connection.commit() #para que se guarden los cambios (muestre en la pantalla)
    
    return redirect(url_for ('tareas')) #ejecutado el guardado de los datos, redirige a la misma ventana tareas
#-----------------------------------
# Ruta para salir de pantalla tareas
@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('back'))
#-----------------------------------
# Ruta para registrarse
@app.route('/registro')
def registro():
    return render_template('registro.html')
#-----------------------------------
# Ruta para agregar usuario
@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       nombre = request.form['nombre']
       apellido = request.form['apellido']

        #--- query ---
       cursor = mysql.connection.cursor() #conecta
       cursor.execute('INSERT INTO usuarios (email, password, nombre, apellido) VALUES (%s, %s, %s, %s)', (email, password, nombre, apellido)) #escribe consulta
       mysql.connection.commit() #ejecuta consulta
       #--- envio msj cuando se insertó un dato ---
       
       flash('Ya estás registrado/a, ahora puedes iniciar sesión !!!')
       return render_template ('index.html')
#-----------------------------------
# Ruta para actualizar usuario
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']

        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE usuarios
        SET email = %s,
            password = %s,
            nombre = %s,
            apellido = %s
        WHERE idusuarios = %s
        """, (email, password, nombre, apellido, id))
        mysql.connection.commit()
        flash('Usuario actualizado con éxito!')
        return redirect(url_for('list'))
#-----------------------------------    
# Ruta para eliminar usuario
@app.route('/usuario/borrar/<int:id>')
def usuarios_borrar(id):
    conexion = mysql.connect
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE idusuarios = %s", (id,))
    conexion.commit()
    print(f"Usuario con id {id} eliminado")
    return redirect(url_for('list'))
#-----------------------------------
# Ruta para editar usuario
@app.route('/usuarios/edit/<int:id>')
def usuarios_editar(id):
    print(f"Intentando editar usuario con id {id}")
    conexion = mysql.connection
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE idusuarios =%s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    print(f"Datos del usuario: {usuario}")
    return render_template('edit.html', usuario=usuario)
#-----------------------------------
#para inicializar la app.
#para que se vean los cambios automaticamente activo debug
if __name__ == '__main__':
    app.run(port=3000, debug=True)