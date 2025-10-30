from flask import Blueprint, request, jsonify, session
from flask_mysqldb import MySQL
from functools import wraps
import hashlib

auth = Blueprint('auth', __name__)
mysql = None

def init_auth(app):
    global mysql
    mysql = MySQL(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Необходима авторизация'}), 401
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Необходима авторизация'}), 401
        if session.get('user_role') != 'admin':
            return jsonify({'error': 'Требуются права администратора'}), 403
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        
        if not all([email, password, first_name, last_name, phone]):
            return jsonify({'error': 'Все поля обязательны'}), 400

        cur = mysql.connection.cursor()
        
        cur.execute("SELECT id FROM clients WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({'error': 'Email уже зарегистрирован'}), 400

        hashed_password = hash_password(password)
        cur.execute("""
            INSERT INTO clients (email, password, first_name, last_name, phone, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'user', NOW())
        """, (email, hashed_password, first_name, last_name, phone))
        
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'message': 'Регистрация успешна'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email и пароль обязательны'}), 400

        cur = mysql.connection.cursor()
        
        hashed_password = hash_password(password)
        cur.execute("""
            SELECT client_id, status, first_name, last_name 
            FROM clients 
            WHERE email = %s AND password = %s
        """, (email, hashed_password))
        
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_role'] = user[1]
            return jsonify({
                'message': 'Вход выполнен успешно',
                'user': {
                    'id': user[0],
                    'role': user[1],
                    'name': f"{user[2]} {user[3]}"
                }
            })
        
        return jsonify({'error': 'Неверный email или пароль'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Выход выполнен успешно'})