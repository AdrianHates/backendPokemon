# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from rutas.post import usuarios_routes
from rutas.get import usuarios_get_routes
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app) 
# Establecer la conexión a la base de datos
conn = psycopg2.connect(
    database="POKEMON",
    user="fl0user",
    password="Jgt0yFH5fPVh",
    host="ep-wispy-meadow-64258402.us-east-2.aws.neon.fl0.io",
    port="5432",
    sslmode="require"
)

# Crear una tabla de usuarios si no existe
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        user_id SERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL,
        genero VARCHAR(1),
        x INT NOT NULL,
        y INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
''')

cur.execute("""CREATE TABLE IF NOT EXISTS user_pokemon (
    user_pokemon_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    pokemon_id INTEGER NOT NULL,
    hp INT CHECK (hp BETWEEN 0 AND 255),
    IVs INT CHECK (IVs BETWEEN 0 AND 31),
    location VARCHAR(10) NOT NULL,
    position INT NOT NULL,
    XP INT,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
);""")
cur.execute("SELECT * FROM user_pokemon")
print(cur.fetchall())
conn.commit()
conn.close()

app.register_blueprint(usuarios_routes)
app.register_blueprint(usuarios_get_routes)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
