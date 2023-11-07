from flask import Blueprint, jsonify, request
import psycopg2
from rutas.db_config import DATABASE_CONFIG

usuarios_get_routes = Blueprint('usuarios_get_routes', __name__)

@usuarios_get_routes.route('/api/v1/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = psycopg2.connect(**DATABASE_CONFIG)    
    cur = conn.cursor()
    cur.execute("SELECT user_id, nombre, genero, created_at FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify(usuarios)

@usuarios_get_routes.route('/api/v1/usuarios/<id>', methods=['GET'])
def obtener_usuario_por_id(id):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT user_id, nombre, genero, x, y, created_at FROM usuarios WHERE user_id = %s", (id,))
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

    return jsonify({ "usuario": usuario, "pokemons": formatted_pokemons })

