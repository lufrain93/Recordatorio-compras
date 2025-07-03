from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'database.db'

# Crear base de datos y tabla si no existen
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                comprado INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Base de datos creada.")

# Conexión a base de datos
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Página principal
@app.route('/')
def index():
    init_db()  # Asegura que la base esté lista
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM productos WHERE comprado = 0').fetchall()
    conn.close()
    return render_template('index.html', items=items)

# Agregar producto
@app.route('/agregar', methods=['POST'])
def agregar():
    producto = request.form['producto']
    conn = get_db_connection()
    conn.execute('INSERT INTO productos (nombre, comprado) VALUES (?, ?)', (producto, 0))
    conn.commit()
    conn.close()
    return redirect('/')

# Marcar como comprado
@app.route('/comprar/<int:id>')
def comprar(id):
    conn = get_db_connection()
    conn.execute('UPDATE productos SET comprado = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

from flask import jsonify

@app.route('/pendientes')
def pendientes():
    conn = get_db_connection()
    total = conn.execute('SELECT COUNT(*) FROM productos WHERE comprado = 0').fetchone()[0]
    conn.close()
    return jsonify({"total": total})

if __name__ == '__main__':
    app.run(debug=True)
