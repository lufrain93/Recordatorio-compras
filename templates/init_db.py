import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        comprado INTEGER NOT NULL DEFAULT 0
    )
''')

conn.commit()
conn.close()
print("✅ Base de datos creada.")
