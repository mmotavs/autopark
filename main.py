from flask import Flask, request, jsonify, session, send_file, render_template, redirect, url_for
from flask_mysqldb import MySQL
from functools import wraps
import json
import hashlib
import datetime
import MySQLdb

app = Flask(__name__, 
            static_url_path='',
            static_folder='static',
            template_folder='templates')

# Включаем режим отладки
app.debug = True

try:
    # Загрузка конфигурации из файла
    with open('config.json') as config_file:
        config = json.load(config_file)

    # Настройка MySQL
    app.config['MYSQL_HOST'] = config['database']['host']
    app.config['MYSQL_USER'] = config['database']['user']
    app.config['MYSQL_PASSWORD'] = config['database']['password']
    app.config['MYSQL_DB'] = config['database']['database']
    app.config['SECRET_KEY'] = 'your-secret-key'  # Замените на безопасный ключ

    mysql = MySQL(app)
except Exception as e:
    print(f"Ошибка при инициализации приложения: {e}")
    raise

# Декоратор для проверки аутентификации
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Декоратор для проверки прав администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        if session.get('user_role') != 'admin':
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Хеширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    if not request.is_json:
        return jsonify({'error': 'Неверный формат данных. Ожидается JSON.'}), 400
        
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        
        # Проверка обязательных полей
        if not all([email, password, first_name, last_name, phone]):
            return jsonify({'error': 'Все поля обязательны для заполнения'}), 400

        cur = mysql.connection.cursor()
        
        # Проверка существования email
        cur.execute("SELECT client_id FROM clients WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({'error': 'Email уже зарегистрирован'}), 400

        # Хеширование пароля и создание пользователя
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

@app.route('/api/login', methods=['POST'])
def login():
    """Вход в систему"""
    if not request.is_json:
        return jsonify({'error': 'Неверный формат данных. Ожидается JSON.'}), 400

    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Проверка обязательных полей
        if not all([email, password]):
            return jsonify({'error': 'Email и пароль обязательны'}), 400

        cur = mysql.connection.cursor()
        
        # Поиск пользователя
        cur.execute("""
            SELECT client_id, password, status 
            FROM clients 
            WHERE email = %s
        """, (email,))
        
        user = cur.fetchone()
        cur.close()

        if not user or user[1] != hash_password(password):
            return jsonify({'error': 'Неверный email или пароль'}), 401

        # Вход успешен
        session['user_id'] = user[0]
        session['user_role'] = user[2]

        return jsonify({
            'message': 'Вход выполнен успешно',
            'user_role': user[2]
        })
    except Exception as e:
        print(f"Error during login: {e}")
        return handle_db_error(e)

@app.route('/logout')
def logout():
    """Выход из системы"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/trips')
@login_required
def trips():
    """Страница с поездками пользователя"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT t.id, c.brand, c.model, t.start_date, t.end_date, t.total_price, t.status
            FROM trips t
            JOIN cars c ON t.car_id = c.id
            WHERE t.client_id = %s
            ORDER BY t.start_date DESC
        """, (session['user_id'],))
        trips = cur.fetchall()
        cur.close()
        
        return render_template('trips.html', trips=trips)
    except Exception as e:
        print(f"Error fetching trips: {e}")
        return render_template('500.html'), 500

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Административная панель"""
    try:
        cur = mysql.connection.cursor()
        
        # Получаем статистику
        cur.execute("SELECT COUNT(*) FROM clients")
        total_users = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM cars")
        total_cars = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM trips WHERE status = 'active'")
        active_trips = cur.fetchone()[0]
        
        # Последние бронирования
        cur.execute("""
            SELECT t.id, c.first_name, c.last_name, car.brand, car.model, 
                   t.start_date, t.end_date, t.status
            FROM trips t
            JOIN clients c ON t.client_id = c.client_id
            JOIN cars car ON t.car_id = car.id
            ORDER BY t.created_at DESC
            LIMIT 10
        """)
        recent_bookings = cur.fetchall()
        
        cur.close()
        
        return render_template('admin_dashboard.html',
                           total_users=total_users,
                           total_cars=total_cars,
                           active_trips=active_trips,
                           recent_bookings=recent_bookings)
    except Exception as e:
        print(f"Error in admin dashboard: {e}")
        return render_template('500.html'), 500

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    """Получение профиля пользователя"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT first_name, last_name, email, phone, status, created_at 
            FROM clients 
            WHERE client_id = %s
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

@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """Получение списка пользователей (только для администраторов)"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT client_id, first_name, last_name, email, phone, status, created_at 
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

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Выход из системы"""
    session.clear()
    return jsonify({'message': 'Выход выполнен успешно'})

# Маршруты для страниц
@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/cars')
def cars():
    """Страница автомобилей"""
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT id, brand, model, year, price_per_day, status, image_url 
            FROM cars 
            WHERE status = 'available'
            ORDER BY brand, model
        """)
        cars = cur.fetchall()
        cur.close()
        
        # Преобразуем результаты в список словарей для удобства
        cars_list = []
        for car in cars:
            cars_list.append({
                'id': car[0],
                'brand': car[1],
                'model': car[2],
                'year': car[3],
                'price_per_day': car[4],
                'status': car[5],
                'image_url': car[6]
            })
        
        return render_template('cars.html', cars=cars_list)
    except Exception as e:
        print(f"Error fetching cars: {e}")
        return render_template('500.html'), 500

@app.route('/login')
def login_page():
    """Страница входа"""
    if 'user_id' in session:
        if session.get('user_role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    """Страница регистрации"""
    if 'user_id' in session:
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/booking')
@login_required
def booking_page():
    """Страница бронирования"""
    return render_template('booking.html')



# Обработчик ошибок MySQL
def handle_db_error(e):
    print(f"Database error: {e}")
    if isinstance(e, MySQLdb.OperationalError):
        return jsonify({'error': 'Ошибка подключения к базе данных'}), 503
    elif isinstance(e, MySQLdb.IntegrityError):
        return jsonify({'error': 'Нарушение целостности данных'}), 400
    else:
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

# Middleware для проверки авторизации
@app.before_request
def check_auth():
    # Список путей, не требующих авторизации
    public_paths = ['/', '/login', '/register', '/static', '/api/login', '/api/register']
    
    # Пропускаем проверку для статических файлов
    if request.path.startswith('/static/'):
        return
        
    # Проверяем, является ли путь публичным
    if any(request.path.startswith(path) for path in public_paths):
        return
    
    # Проверяем авторизацию для административных путей
    if request.path.startswith('/admin/') or request.path.startswith('/api/admin/'):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        if session.get('user_role') != 'admin':
            return redirect(url_for('index'))
        return
    
    # Проверяем авторизацию для остальных путей
    if 'user_id' not in session:
        return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=True  # Включаем режим отладки
    )
