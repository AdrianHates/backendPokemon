# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from rutas.post import users_post_routes
from rutas.get import users_get_routes
from flask_cors import CORS
import os
from dotenv import load_dotenv
import psycopg2
from rutas.db_config import DATABASE_CONFIG

load_dotenv()

app = Flask(__name__)
CORS(app)
# Establecer la conexión a la base de datos

conn = psycopg2.connect(
    **DATABASE_CONFIG
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
    pokemon_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    pokemon_number INTEGER NOT NULL,
    level INTEGER NOT NULL,
    hp INT CHECK (hp BETWEEN 0 AND 255),
    status INTEGER CHECK (status IN (0, 1, 2, 3, 4, 5)),    
    IV_hp INT CHECK (IV_hp BETWEEN 0 AND 31),
    IV_attack INT CHECK (IV_attack BETWEEN 0 AND 31),
    IV_defense INT CHECK (IV_defense BETWEEN 0 AND 31),
    IV_specialAttack INT CHECK (IV_specialAttack BETWEEN 0 AND 31),
    IV_specialDefense INT CHECK (IV_specialDefense BETWEEN 0 AND 31),
    IV_speed INT CHECK (IV_speed BETWEEN 0 AND 31),
    location JSONB NOT NULL,
    xp INT NOT NULL,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);""")
cur.execute("SELECT * FROM user_pokemon")
print(cur.fetchall())
conn.commit()
conn.close()

app.register_blueprint(users_post_routes)
app.register_blueprint(users_get_routes)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)
