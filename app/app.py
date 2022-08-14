from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

# Para reconocer caracteres especiales:
app.config['JSON_AS_ASCII'] = False

# Conexión a MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123abc'
app.config['MYSQL_DB'] = 'dentista'

conexion = MySQL(app)


@app.before_request
def before_request():
    print('Antes de la petición')


@app.after_request
def after_request(response):
    print('Después de la petición')
    return response


@app.route('/')
def index():
    # return "<h1>Hello World!<h1/>"
    cursos = ['PHP', 'Python', 'Java', 'Kotlin', 'Dart', 'Javascript']
    data = {
        'titulo': 'Index desde data',
        'bienvenida': 'Hola mundo!',
        'cursos': cursos,
        'numero_cursos': len(cursos)
    }
    return render_template('index.html', data=data)


@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {
        'titulo': 'Contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "Ok"


@app.route('/pacientes')
def listar_pacientes():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = 'SELECT * FROM pacientes ORDER BY nombre ASC'
        cursor.execute(sql)
        pacientes = cursor.fetchall()
        # print(pacientes)
        data['pacientes'] = pacientes
        data['mensaje'] = 'Exito!'
    except Exception as ex:
        data['mensaje'] = 'Error...'

    # return render_template('pacientes.html', data=data)
    return jsonify(data)


@app.route('/pacientes/listar')
def lista_pacientes(data):
    data = listar_pacientes()
    return render_template('pacientes.html', data=data)


def pagina_no_encontrada(error):
    # Este renderiza la vista del error:
    # return render_template('404.html'), 404
    # Este redirecciona a la función index
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
