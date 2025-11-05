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
    # Заглушка регистрации: проверяем входные данные, но не используем БД.
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')

    if not all([email, password, first_name, last_name, phone]):
        return jsonify({'error': 'Все поля обязательны'}), 400

    return jsonify({'message': 'Регистрация (заглушка) успешна'}), 201

@auth.route('/api/login', methods=['POST'])
def login():
    # Заглушка логина: не обращаемся к БД, устанавливаем простую сессию
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email и пароль обязательны'}), 400

    session['user_id'] = 1
    session['user_role'] = 'admin' if 'admin' in (email or '').lower() else 'user'

    return jsonify({'message': 'Вход (заглушка) выполнен успешно', 'user': {'id': session['user_id'], 'role': session['user_role']}})

@auth.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Выход выполнен успешно'})