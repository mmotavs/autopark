from flask import Blueprint, jsonify, session
from routes.auth import admin_required
from flask_mysqldb import MySQL

admin = Blueprint('admin', __name__)
mysql = None

def init_admin(app):
    global mysql
    mysql = MySQL(app)

@admin.route('/api/admin/bookings', methods=['GET'])
@admin_required
def get_all_bookings():
    """Получение всех заявок на обслуживание (только для администратора)"""
    try:
        # Заглушка: возвращаем небольшой список фиктивных заявок для фронтенда
        sample = [
            {
                'id': 1,
                'start_date': '2025-11-01T09:00:00',
                'end_date': '2025-11-05T18:00:00',
                'status': 'pending',
                'notes': 'Тестовая заявка',
                'client': {'first_name': 'Иван', 'last_name': 'Иванов', 'phone': '+79990001122'},
                'car': {'make': 'Toyota', 'model': 'Camry', 'plate_number': 'A123BC'}
            }
        ]
        return jsonify(sample)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/admin/maintenance', methods=['GET'])
@admin_required
def get_maintenance_records():
    """Получение всех записей о техобслуживании (только для администратора)"""
    try:
        # Заглушка: возвращаем список автомобилей и их статусов
        sample = [
            {'car': {'make': 'Toyota', 'model': 'Camry', 'plate_number': 'A123BC', 'year': 2019, 'mileage': 50000, 'status': 'available'}},
            {'car': {'make': 'BMW', 'model': 'X5', 'plate_number': 'B321CD', 'year': 2020, 'mileage': 30000, 'status': 'in_service'}}
        ]
        return jsonify(sample)
    except Exception as e:
        return jsonify({'error': str(e)}), 500