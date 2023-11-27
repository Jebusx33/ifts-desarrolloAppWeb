from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#conectar a la Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:root@localhost/sitio_ifts_desarrollo'
mysql = SQLAlchemy(app)


# Definir el modelo
class Libros(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    nombre = mysql.Column(mysql.String(255))
    imagen = mysql.Column(mysql.String(255))
    url = mysql.Column(mysql.String(255))

# Use the Flask app context to create tables
with app.app_context():
    mysql.create_all()


@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/libros')
def libros():
    return render_template('sitio/libros.html')

@app.route('/descripcion')
def descripcion():
    return render_template('sitio/descripcion.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')

@app.route('/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():
     #Traes todos los libros por mysql
    libros = Libros.query.all()

    # Print libros data for debugging
    for libro in libros:
        print(f"ID: {libro.id}, Nombre: {libro.nombre}, Imagen: {libro.imagen}, URL: {libro.url}")

    # Convert libros to a list of dictionaries
    libros_data = [
        {'id': libro.id, 'nombre': libro.nombre, 'imagen': libro.imagen, 'url': libro.url}
        for libro in libros
    ]

    # Return libros_data as JSON (for demonstration purposes)
    return render_template('admin/libros.html', libros=libros_data)

@app.route('/admin/productos')
def admin_productos():
    return render_template('admin/productos.html')

@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    _nombre = request.form['txtNombre']
    _url = request.form['txtUrl']
    _archivo = request.files['txtImagen']

    try:
        nuevo_libro = Libros(nombre=_nombre, imagen=_archivo.filename, url=_url)
        mysql.session.add(nuevo_libro)
        mysql.session.commit()
    except Exception as e:
        print("Error al insertar en la base de datos:", str(e))
    finally:
        # Cierra la conexión
        mysql.session.close()

    print(_nombre)
    print(_url)
    print(_archivo.filename)
    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    if request.method == 'POST':
        libro_id = request.form.get('libro_id')  # Obtén el ID del libro desde el formulario
        if libro_id:
            try:
                libro_a_borrar = Libros.query.get(libro_id)  # Consulta el libro por su ID
                if libro_a_borrar:
                    mysql.session.delete(libro_a_borrar)  # Elimina el libro de la sesión
                    mysql.session.commit()  # Confirma los cambios
            except Exception as e:
                print("Error al borrar el libro de la base de datos:", str(e))
            finally:
                mysql.session.close()  # Cierra la conexión a la base de datos

    return redirect('/admin/libros')

@app.route('/admin/libros/editar', methods=['POST'])
#funcion para edita un libro
def admin_libros_editar():
    if request.method == 'POST':
        libro_id = request.form.get('libro_id')  # Obtén el ID del libro desde el formulario
        nuevo_nombre = request.form.get('nuevo_nombre')  # Obtén el nuevo nombre del libro desde el formulario
        nuevo_url = request.form.get('nuevo_url')  # Obtén la nueva URL del libro desde el formulario
        nueva_imagen = request.form.get('nueva_imagen')  # Obtén la nueva URL del libro desde el formulario
        if libro_id:
            try:
                libro_a_editar = Libros.query.get(libro_id)  # Consulta el libro por su ID
                if libro_a_editar:
                    libro_a_editar.nombre = nuevo_nombre  # Actualiza el nombre del libro
                    libro_a_editar.url = nuevo_url  # Actualiza la URL del libro
                    libro_a_editar.imagen= nueva_imagen
                    mysql.session.commit()  # Confirma los cambios
            except Exception as e:
                print("Error al editar el libro en la base de datos:", str(e))
            finally:
                mysql.session.close()  # Cierra la conexión a la base de datos

    return redirect('/admin/libros')

if __name__ =='__main__':
    app.run(debug=True)