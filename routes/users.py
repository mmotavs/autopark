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
    # Заглушка профиля: возвращаем фиктивные данные на основе сессии
    if 'user_id' not in session:
        return jsonify({'error': 'Не авторизован'}), 401

    return jsonify({
        'first_name': 'Тест',
        'last_name': 'Пользователь',
        'email': 'user@example.com',
        'phone': '+7(000)000-00-00',
        'status': session.get('user_role', 'user'),
        'created_at': None
    })

@users.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    # Заглушка: возвращаем пустой список пользователей
    return jsonify([])