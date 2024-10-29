import sqlite3

# Подключение к базе данных (если файл базы данных не существует, он будет создан автоматически)
conn = sqlite3.connect("city_reference.db")
cursor = conn.cursor()

# Создание таблицы для расписания автобусов
cursor.execute('''
CREATE TABLE IF NOT EXISTS bus_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route TEXT NOT NULL,
    weekday_schedule TEXT,
    weekend_schedule TEXT
)
''')

# Создание таблицы для расписания ЖД и авиа транспорта
cursor.execute('''
CREATE TABLE IF NOT EXISTS train_air_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transport_type TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TEXT,
    arrival_time TEXT
)
''')

# Создание таблицы для приема администрации
cursor.execute('''
CREATE TABLE IF NOT EXISTS admin_reception (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    contact_info TEXT,
    working_hours TEXT
)
''')

# Создание таблицы для расписания приема врачей
cursor.execute('''
CREATE TABLE IF NOT EXISTS hospital_appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    available_days TEXT,
    appointment_hours TEXT
)
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных и таблицы успешно созданы.")
