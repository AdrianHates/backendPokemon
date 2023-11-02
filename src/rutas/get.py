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
    cur.close()
    conn.close()

    return jsonify(usuario)

