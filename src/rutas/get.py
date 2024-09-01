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
    cur.execute("SELECT pokemon_id, pokemon_number, level, iv_hp, iv_attack, iv_defense, iv_speed, location, position, XP, captured_at FROM user_pokemon WHERE user_id = %s", (id,))
    pokemons = cur.fetchall()
    cur.close()
    conn.close()
    formatted_pokemons = []
    for pokemon in pokemons:
        formatted_pokemon = {
            "pokemon_id": pokemon[0],
            "pokemon_number": pokemon[1],
            "level": pokemon[2],
            "ivs": {
                "hp": pokemon[3],
                "attack": pokemon[4],
                "defense": pokemon[5],
                "specialAttack": pokemon[6],
                "specialDefense": pokemon[7],
                "speed": pokemon[8]
            },
            "location": pokemon[9],
            "position": pokemon[10],
            "XP": pokemon[11],
            "captured_at": pokemon[12],
            "evs": {
                "hp": 0,
                "attack": 0,
                "defense": 0,
                "specialAttack": 0,
                "specialDefense": 0,
                "speed": 0
            },
            "stats": {
                "max_hp": 0,
                "current_hp": 0
            },
            "status": "none"
        }
        formatted_pokemons.append(formatted_pokemon)

    return jsonify({ "user": usuario, "pokemons": formatted_pokemons })

