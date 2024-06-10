from flask import Blueprint, jsonify, request
import psycopg2
from rutas.db_config import DATABASE_CONFIG

users_get_routes = Blueprint('users_get_routes', __name__)

@users_get_routes.route('/api/v1/users', methods=['GET'])
def obtener_usuarios():
    conn = psycopg2.connect(**DATABASE_CONFIG)    
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, gender, created_at FROM users")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(usuarios)

@users_get_routes.route('/api/v1/users/<id>', methods=['GET'])
def obtener_usuario_por_id(id):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, gender, x, y, created_at FROM users WHERE user_id = %s", (id,))
    usuario = cur.fetchone()
    cur.execute("SELECT user_pokemon_id, pokemon_id, hp, IVs, location, position, XP, captured_at FROM user_pokemon WHERE user_id = %s", (id,))
    pokemons = cur.fetchall()
    cur.close()
    conn.close()
    formatted_pokemons = []
    for pokemon in pokemons:
        formatted_pokemon = {
            "user_pokemon_id": pokemon[0],
            "pokemon_id": pokemon[1],
            "hp": pokemon[2],
            "IVs": pokemon[3],
            "location": pokemon[4],
            "position": pokemon[5],
            "XP": pokemon[6],
            "captured_at": pokemon[7]
        }
        formatted_pokemons.append(formatted_pokemon)

    return jsonify({ "user": usuario, "pokemons": formatted_pokemons })

