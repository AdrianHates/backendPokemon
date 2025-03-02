from flask import Blueprint, jsonify, request
import psycopg2
from rutas.db_config import DATABASE_CONFIG
from psycopg2.extras import RealDictCursor


users_get_routes = Blueprint('users_get_routes', __name__)

@users_get_routes.route('/api/v1/users', methods=['GET'])
def obtener_usuarios():
    conn = psycopg2.connect(**DATABASE_CONFIG)    
    cur = conn.cursor(cursor_factory=RealDictCursor) 
    cur.execute("SELECT user_id, name, gender, created_at FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(users)

@users_get_routes.route('/api/v1/users/<id>', methods=['GET'])
def obtener_usuario_por_id(id):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor) 
    cur.execute("SELECT user_id, name, gender, x, y, created_at FROM users WHERE user_id = %s", (id,))
    usuario = cur.fetchone()
    cur.close()

    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT pokemon_id, pokemon_number, level, hp, status, iv_hp, iv_attack, iv_defense, iv_specialAttack, iv_specialDefense, iv_speed, location, xp, captured_at FROM user_pokemon WHERE user_id = %s", (id,))
    pokemons = cur.fetchall()
    
    cur.close()
    conn.close()
    formatted_pokemons = [
        {
            "pokemon_id": pokemon["pokemon_id"],
            "pokemon_number": pokemon["pokemon_number"],
            "level": pokemon["level"],
            "hp": pokemon["hp"],
            "status": pokemon["status"],
            "ivs": {
                "hp": pokemon["iv_hp"],
                "attack": pokemon["iv_attack"],
                "defense": pokemon["iv_defense"],
                "specialAttack": pokemon["iv_specialattack"],
                "specialDefense": pokemon["iv_specialdefense"],
                "speed": pokemon["iv_speed"]
            },
            "location": pokemon["location"],
            "xp": pokemon["xp"],
            "captured_at": pokemon["captured_at"],
            "evs": {
                "hp": 0,
                "attack": 0,
                "defense": 0,
                "specialAttack": 0,
                "specialDefense": 0,
                "speed": 0
            },            
        }
        for pokemon in pokemons
    ]

    return jsonify({ "user": usuario, "pokemons": formatted_pokemons })

