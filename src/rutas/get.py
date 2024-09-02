from flask import Blueprint, jsonify, request
import psycopg2
from rutas.db_config import DATABASE_CONFIG

users_get_routes = Blueprint('users_get_routes', __name__)

@users_get_routes.route('/api/v1/users', methods=['GET'])
def obtener_usuarios():
    conn = psycopg2.connect(**DATABASE_CONFIG)    
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, gender, created_at FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(users)

@users_get_routes.route('/api/v1/users/<id>', methods=['GET'])
def obtener_usuario_por_id(id):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT user_id, name, gender, x, y, created_at FROM users WHERE user_id = %s", (id,))
    usuario = cur.fetchone()
    cur.execute("SELECT pokemon_id, pokemon_number, level, hp, status, iv_hp, iv_attack, iv_defense, iv_speed, location, xp, captured_at FROM user_pokemon WHERE user_id = %s", (id,))
    pokemons = cur.fetchall()
    cur.close()
    conn.close()
    formatted_pokemons = []
    for pokemon in pokemons:
        formatted_pokemon = {
            "pokemon_id": pokemon[0],
            "pokemon_number": pokemon[1],
            "level": pokemon[2],
            "hp": pokemon [3],
            "status": pokemon[4],
            "ivs": {
                "hp": pokemon[5],
                "attack": pokemon[6],
                "defense": pokemon[7],
                "specialAttack": pokemon[8],
                "specialDefense": pokemon[9],
                "speed": pokemon[10]
            },
            "location": pokemon[11],
            "xp": pokemon[12],
            "captured_at": pokemon[13],
            "evs": {
                "hp": 0,
                "attack": 0,
                "defense": 0,
                "specialAttack": 0,
                "specialDefense": 0,
                "speed": 0
            },            
        }
        formatted_pokemons.append(formatted_pokemon)

    return jsonify({ "user": usuario, "pokemons": formatted_pokemons })

