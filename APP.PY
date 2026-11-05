#Flask: Permite crear la aplicación web.
#render_template: Muestra archivos HTML.
#request: Recibe los datos enviados desde formularios.
#redirect: Redirecciona a otra página.
#url_for: Genera rutas automáticamente.
#flash: Muestra mensajes al usuario.
#MySQL: Permite conectar Flask con la base de datos MySQL.
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#se crea la instansia de flask que sera el nucleo de la aplicacion web
app = Flask(__name__)

# MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'

#MYSQL_HOST: Servidor donde está la base de datos.
#MYSQL_USER: Usuario de MySQL.
#MYSQL_PASSWORD: Contraseña del usuario.
#MYSQL_DB: Nombre de la base de datos.

mysql = MySQL(app)


#Se utiliza para proteger la información de sesión
# y permitir el uso de mensajes temporales con flash

app.secret_key = 'mysecretkey'

# ruta de la pagina principal
@app.route('/')
def index():

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM contacts")

    data = cur.fetchall()

    cur.close()

    return render_template(
        'index.html',
        contacts=data
    )

# esta ruta recibe los datos completos desde un formulario
# y los inserta en la base de datos
@app.route('/add_contact', methods=['POST'])
def add_contact():

    fullname = request.form['fullname']
    phone = request.form['phone']
    pathologies = request.form['pathologies']

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO contacts(fullname, phone, pathologies)
        VALUES (%s, %s, %s)
    """, (fullname, phone, pathologies))

    mysql.connection.commit()

    cur.close()

    flash('Paciente agregado correctamente')

    return redirect(url_for('index'))

# busca datos para editar
@app.route('/edit/<id>')
def get_contact(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM contacts WHERE id = %s",
        (id,)
    )

    data = cur.fetchall()

    cur.close()

    return render_template(
        'edit-contact.html',
        contact=data[0]
    )

# ACTUALIZAR
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):

    fullname = request.form['fullname']
    phone = request.form['phone']
    pathologies = request.form['pathologies']

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE contacts
        SET fullname=%s,
            phone=%s,
            pathologies=%s
        WHERE id=%s
    """, (fullname, phone, pathologies, id))

    mysql.connection.commit()

    cur.close()

    flash('Paciente actualizado correctamente')

    return redirect(url_for('index'))

# ELIMINAR
@app.route('/delete/<string:id>')
def delete_contact(id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE id = %s",
        (id,)
    )

    mysql.connection.commit()

    cur.close()

    flash('Paciente eliminado correctamente')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)  