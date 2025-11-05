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
    # Простейшая заглушка регистрации — сохранять реальные данные сейчас не требуется.
    # Оставляем проверку формата и обязательных полей, но не выполняем SQL-запросы.
    if not request.is_json:
        return jsonify({'error': 'Неверный формат данных. Ожидается JSON.'}), 400

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone = data.get('phone')

    if not all([email, password, first_name, last_name, phone]):
        return jsonify({'error': 'Все поля обязательны для заполнения'}), 400

    # Возвращаем успешный ответ как заглушку (в будущем здесь будет сохранение в БД)
    return jsonify({'message': 'Регистрация (заглушка) выполнена успешно'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Вход в систему"""
    if not request.is_json:
        return jsonify({'error': 'Неверный формат данных. Ожидается JSON.'}), 400
    # Простая заглушка логина: не обращаемся к БД, но устанавливаем сессию для навигации.
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email и пароль обязательны'}), 400

    # Простая логика: если в email есть слово 'admin' — даём роль admin, иначе user.
    user_id = 1
    role = 'admin' if 'admin' in (email or '').lower() else 'user'
    session['user_id'] = user_id
    session['user_role'] = role

    return jsonify({'message': 'Вход (заглушка) выполнен успешно', 'user_role': role})

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
        # Заглушка: возвращаем пустой список поездок — фронтенд можно отлаживать
        return render_template('trips.html', trips=[])
    except Exception as e:
        print(f"Unexpected error in trips stub: {e}")
        return render_template('500.html'), 500

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Административная панель"""
    try:
        # Заглушка: возвращаем нулевые значения и пустой список бронирований
        return render_template('admin_dashboard.html',
                               total_users=0,
                               total_cars=0,
                               active_trips=0,
                               recent_bookings=[])
    except Exception as e:
        print(f"Unexpected error in admin_dashboard stub: {e}")
        return render_template('500.html'), 500

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    """Получение профиля пользователя"""
    try:
        # Заглушка: вернём профиль, основанный на сессии (если есть)
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """Получение списка пользователей (только для администраторов)"""
    try:
        # Заглушка: возвращаем пустой список — админская логика работы с БД отключена
        return jsonify([])
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
        # Заглушка: статический список автомобилей для работы фронтенда
        cars_list = [
            {'id': 1, 'brand': 'Toyota', 'model': 'Camry', 'year': 2019, 'price_per_day': 4200, 'status': 'available', 'image_url': 'https://i.pinimg.com/736x/b9/c9/a2/b9c9a22952a7febe2b8fff53463e3ac5.jpg'},
            {'id': 2, 'brand': 'BMW', 'model': 'X5', 'year': 2020, 'price_per_day': 8500, 'status': 'available', 'image_url': 'https://i.pinimg.com/736x/6d/35/d5/6d35d5aefc6e8968bfea88264bae49b5.jpg'},
            {'id': 3, 'brand': 'Mazda', 'model': 'CX-5', 'year': 2018, 'price_per_day': 5000, 'status': 'available', 'image_url': 'https://i.pinimg.com/1200x/05/60/27/0560274d90d8f2f606c0fc29478a2c0b.jpg'},
            {'id': 4, 'brand': 'Kia', 'model': 'Rio', 'year': 2017, 'price_per_day': 2500, 'status': 'available', 'image_url': 'https://i.pinimg.com/1200x/85/58/2e/85582e48c7274876b45aa0e084f272c6.jpg'},
            {'id': 5, 'brand': 'Mercedes', 'model': 'E-Class', 'year': 2021, 'price_per_day': 7800, 'status': 'available', 'image_url': 'https://i.pinimg.com/1200x/41/e3/03/41e303628044e0b5b38f2f5248c2410c.jpg'},
            {'id': 6, 'brand': 'Porsche', 'model': '911', 'year': 2022, 'price_per_day': 12500, 'status': 'available', 'image_url': 'https://i.pinimg.com/736x/2a/d7/a9/2ad7a95caf42b7caa074738fc8517452.jpg'}
        ]

        return render_template('cars.html', cars=cars_list)
    except Exception as e:
        print(f"Unexpected error in cars stub: {e}")
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
# @login_required #
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
    public_paths = ['/', '/login', '/register', '/static', '/api/login', '/api/register', '/booking']
    
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
