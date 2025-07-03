from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM productos WHERE comprado = 0').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/agregar', methods=['POST'])
def agregar():
    producto = request.form['producto']
    conn = get_db_connection()
    conn.execute('INSERT INTO productos (nombre, comprado) VALUES (?, ?)', (producto, 0))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/comprar/<int:id>')
def comprar(id):
    conn = get_db_connection()
    conn.execute('UPDATE productos SET comprado = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
