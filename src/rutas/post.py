from flask import Blueprint, jsonify, request
import random
from rutas.db_config import DATABASE_CONFIG
import psycopg2

usuarios_routes = Blueprint('usuarios_routes', __name__)

# Aquí debes establecer tu conexión con la base de datos

@usuarios_routes.route('/api/v1/usuarios', methods=['POST'])
def crear_usuario():
    # Asegúrate de tener una conexión válida
    conn = psycopg2.connect(
    **DATABASE_CONFIG
)
    cur = conn.cursor()

    data = request.get_json()
    nombre = data['name']
    genero = data['gender'][0]
    #inicio
    x = 0
    y = 10
    
    cur.execute("INSERT INTO usuarios (nombre, genero, x, y) VALUES (%s, %s, %s, %s) RETURNING user_id", (nombre, genero, x, y))
    new_user_id = cur.fetchone()[0] 
    numero_aleatorio = random.randint(0, 31)

    cur.execute("INSERT INTO user_pokemon(user_id, pokemon_id, hp, IVs, location, XP ) VALUES (%s, %s, %s, %s, %s, %s)", (new_user_id, 25, 100, numero_aleatorio, "equipo", 0))
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({'message': 'Usuario creado exitosamente'})