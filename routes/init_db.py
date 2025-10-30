import mysql.connector
import json
import hashlib
from datetime import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Загрузка конфигурации
with open('config.json') as config_file:
    config = json.load(config_file)

# Подключение к базе данных
db = mysql.connector.connect(
    host=config['database']['host'],
    user=config['database']['user'],
    password=config['database']['password'],
    database='autopark'
)

cursor = db.cursor()

# Данные администратора
admin_data = {
    'email': 'admin@autopark.ru',
    'password': hash_password('admin123'),
    'first_name': 'Администратор',
    'last_name': 'Системы',
    'phone': '+7(999)999-99-99',
    'status': 'admin'
}

# SQL запрос для вставки данных
insert_query = """
INSERT INTO clients (first_name, last_name, email, phone, password, status, created_at)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

try:
    # Проверяем, существует ли уже администратор
    cursor.execute("SELECT client_id FROM clients WHERE email = %s", (admin_data['email'],))
    if not cursor.fetchone():
        # Вставляем данные администратора
        admin_values = (
            admin_data['first_name'],
            admin_data['last_name'],
            admin_data['email'],
            admin_data['phone'],
            admin_data['password'],
            admin_data['status'],
            datetime.now()
        )
        cursor.execute(insert_query, admin_values)

    # Подтверждение изменений
    db.commit()
    print("Данные успешно добавлены в базу данных")

except mysql.connector.Error as error:
    print(f"Ошибка при добавлении данных: {error}")

finally:
    # Закрытие соединения
    if db.is_connected():
        cursor.close()
        db.close()
        print("Соединение с базой данных закрыто")