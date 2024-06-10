from flask import Blueprint, jsonify, request
import random
from rutas.db_config import DATABASE_CONFIG
import psycopg2

users_routes = Blueprint('users_routes', __name__)

# Aquí debes establecer tu conexión con la base de datos

@users_routes.route('/api/v1/users', methods=['POST'])
def crear_usuario():
    # Asegúrate de tener una conexión válida
    conn = psycopg2.connect(
    **DATABASE_CONFIG
)
    cur = conn.cursor()

    data = request.get_json()
    name = data['name']
    gender = data['gender']
    #inicio
    x = 0
    y = 10
    
    cur.execute("INSERT INTO users (name, gender, x, y) VALUES (%s, %s, %s, %s) RETURNING user_id", (name, gender, x, y))
    new_user_id = cur.fetchone()[0] 
    numero_aleatorio = random.randint(0, 31)

    cur.execute("INSERT INTO user_pokemon(user_id, pokemon_id, hp, IVs, location, position, XP ) VALUES (%s, %s, %s, %s, %s, %s, %s)", (new_user_id, 25, 100, numero_aleatorio, "equipo", 1, 0))
    conn.commit()

    cur.close()
    conn.close()
    return jsonify({'message': 'user create successfully'})