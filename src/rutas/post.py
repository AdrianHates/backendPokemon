from flask import Blueprint, jsonify, request
from rutas.db_config import DATABASE_CONFIG
import psycopg2

users_post_routes = Blueprint('users_post_routes', __name__)

# Aquí debes establecer tu conexión con la base de datos

@users_post_routes.route('/api/v1/users', methods=['POST'])
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
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'user create successfully'})

@users_post_routes.route('/api/v1/pokemons', methods=['POST'])
def capturar_pokemon():
    data = request.get_json()
    user_id = data['user_id']
    pokemon_number = data['pokemon_number']
    level = data['level']
    hp = data['stats']['current_hp']
    status = 0
    iv_hp = data['ivs']['hp']
    iv_attack = data['ivs']['attack']
    iv_defense = data['ivs']['defense']
    iv_specialAttack = data['ivs']['specialAttack']
    iv_specialDefense = data['ivs']['specialDefense']
    iv_speed = data['ivs']['speed']
    location = data['location']
    xp = data['xp']

    conn = psycopg2.connect(
    **DATABASE_CONFIG)
    cur = conn.cursor()    
    cur.execute("INSERT INTO user_pokemon(user_id, pokemon_number, level, hp, status, iv_hp, iv_attack, iv_defense, iv_specialAttack, iv_specialDefense, iv_speed, location, xp ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_id, pokemon_number, level, hp, status, iv_hp, iv_attack, iv_specialAttack, iv_defense, iv_specialDefense, iv_speed, location, xp))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'pokemon obtained successfully'})