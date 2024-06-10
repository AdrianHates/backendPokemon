# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from rutas.post import users_routes
from rutas.get import users_get_routes
from flask_cors import CORS
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

app = Flask(__name__)
CORS(app)
# Establecer la conexión a la base de datos

conn = psycopg2.connect(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    sslmode="require"
)

# Crear una tabla de usuarios si no existe
cur = conn.cursor()
cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        gender VARCHAR(5) NOT NULL,
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
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);""")
cur.execute("SELECT * FROM user_pokemon")
print(cur.fetchall())
conn.commit()
conn.close()

app.register_blueprint(users_routes)
app.register_blueprint(users_get_routes)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
