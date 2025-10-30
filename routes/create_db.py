import mysql.connector
import json

# Загрузка конфигурации
with open('config.json') as config_file:
    config = json.load(config_file)

# Подключение к MySQL серверу (без указания базы данных)
db = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password']
)

cursor = db.cursor()

# Использование существующей базы данных
cursor.execute("USE autopark")

# Создание таблицы clients
cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL,
    password VARCHAR(100) NOT NULL,
    status ENUM('user', 'admin') DEFAULT 'user',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Создание таблицы cars
cursor.execute("""
CREATE TABLE IF NOT EXISTS cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    plate_number VARCHAR(20) NOT NULL UNIQUE,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year SMALLINT NOT NULL,
    mileage INT NOT NULL,
    status ENUM('available', 'in_service', 'maintenance') DEFAULT 'available',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Создание таблицы bookings
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    car_id INT,
    employee_id INT,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    status ENUM('pending', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (car_id) REFERENCES cars(car_id)
)
""")

print("База данных и таблицы успешно созданы")

# Закрытие соединения
cursor.close()
db.close()