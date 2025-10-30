from flask import Blueprint, jsonify, session
from functools import wraps
from routes.auth import login_required, admin_required
from flask_mysqldb import MySQL

users = Blueprint('users', __name__)
mysql = None

def init_users(app):
    global mysql
    mysql = MySQL(app)

@users.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT first_name, last_name, email, phone, status, created_at 
            FROM clients 
            WHERE id = %s
        """, (session['user_id'],))
        
        user = cur.fetchone()
        cur.close()
        
        if user:
            return jsonify({
                'first_name': user[0],
                'last_name': user[1],
                'email': user[2],
                'phone': user[3],
                'status': user[4],
                'created_at': user[5].isoformat() if user[5] else None
            })
            
        return jsonify({'error': 'Пользователь не найден'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, first_name, last_name, email, phone, status, created_at 
            FROM clients
            ORDER BY created_at DESC
        """)
        
        users = cur.fetchall()
        cur.close()
        
        return jsonify([{
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3],
            'phone': user[4],
            'status': user[5],
            'created_at': user[6].isoformat() if user[6] else None
        } for user in users])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500