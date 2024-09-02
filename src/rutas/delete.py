from flask import Blueprint, jsonify, request
from rutas.db_config import DATABASE_CONFIG
import psycopg2

users_delete_routes = Blueprint('users_delete_routes', __name__)

@users_routes.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def eliminar_usuario(user_id):
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    
    cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({'message': f'User with ID {user_id} deleted successfully'}), 200