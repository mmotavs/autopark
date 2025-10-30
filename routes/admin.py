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
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                b.booking_id,
                b.start_date,
                b.end_date,
                b.status,
                b.notes,
                c.first_name as client_first_name,
                c.last_name as client_last_name,
                c.phone as client_phone,
                cars.make,
                cars.model,
                cars.plate_number
            FROM bookings b
            JOIN clients c ON b.client_id = c.client_id
            JOIN cars ON b.car_id = cars.car_id
            ORDER BY b.created_at DESC
        """)
        
        bookings = cur.fetchall()
        cur.close()
        
        return jsonify([{
            'id': booking[0],
            'start_date': booking[1].isoformat() if booking[1] else None,
            'end_date': booking[2].isoformat() if booking[2] else None,
            'status': booking[3],
            'notes': booking[4],
            'client': {
                'first_name': booking[5],
                'last_name': booking[6],
                'phone': booking[7]
            },
            'car': {
                'make': booking[8],
                'model': booking[9],
                'plate_number': booking[10]
            }
        } for booking in bookings])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/api/admin/maintenance', methods=['GET'])
@admin_required
def get_maintenance_records():
    """Получение всех записей о техобслуживании (только для администратора)"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT 
                cars.make,
                cars.model,
                cars.plate_number,
                cars.year,
                cars.mileage,
                cars.status
            FROM cars
            ORDER BY cars.created_at DESC
        """)
        
        maintenance = cur.fetchall()
        cur.close()
        
        return jsonify([{
            'car': {
                'make': record[0],
                'model': record[1],
                'plate_number': record[2],
                'year': record[3],
                'mileage': record[4],
                'status': record[5]
            }
        } for record in maintenance])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500