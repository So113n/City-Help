import customtkinter as ctk
import os
import webbrowser
import sqlite3
from tkinter import messagebox, ttk
from PIL import Image

from customtkinter import CTkImage

# Настройка пути к папке с логотипами
base_dir = os.path.dirname(os.path.abspath(__file__))  # Путь к папке с файлом main.py
logo_path = os.path.join(base_dir, "Logos", "main_logo.png")  # Путь к логотипу внутри папки Logos

# Проверка на существование файла с логотипом
if not os.path.exists(logo_path):
    raise FileNotFoundError(f"Логотип не найден по пути: {logo_path}")

# Функция для подключения к базе данных
def get_connection():
    return sqlite3.connect("city_reference.db")

# Получение расписания автобусов
def get_bus_schedule():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT route, weekday_schedule, weekend_schedule FROM bus_schedule")
    bus_schedule = cursor.fetchall()
    conn.close()
    return bus_schedule

# Получение расписания ЖД и авиа транспорта
def get_train_air_schedule():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT transport_type, destination, departure_time, arrival_time FROM train_air_schedule")
    train_air_schedule = cursor.fetchall()
    conn.close()
    return train_air_schedule

# Получение информации о приеме администрации
def get_admin_reception():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT department, contact_info, working_hours FROM admin_reception")
    admin_reception = cursor.fetchall()
    conn.close()
    return admin_reception

# Получение расписания приема врачей
def get_hospital_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT doctor_name, specialty, available_days, appointment_hours FROM hospital_appointments")
    hospital_appointments = cursor.fetchall()
    conn.close()
    return hospital_appointments

# Функция для открытия браузера
def open_home_page():
    webbrowser.open("https://nur.yanao.ru/")

def show_personal_account():
    messagebox.showinfo("Личный кабинет", "Функция в разработке")

# Функция для отображения таблицы с данными "Расписание Автобусов"
def show_table(data, columns, title):
    table_window = ctk.CTkToplevel(root)
    table_window.geometry("600x400")
    table_window.title(title)

    table_window.transient(root)
    table_window.grab_set()  # Захватывает все события ввода, чтобы пользователь не мог взаимодействовать с главным окном
    table_window.focus_set()

    tree = ttk.Treeview(table_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    for row in data:
        tree.insert("", "end", values=row)
    tree.pack(expand=True, fill="both")

    # Фрейм для кнопок "Закрыть" и "Карты"
    button_frame = ctk.CTkFrame(table_window)
    button_frame.pack(fill="x", pady=10)

    # Кнопка "Закрыть"
    close_button = ctk.CTkButton(table_window, text="Закрыть", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=table_window.destroy)
    close_button.pack(side="left", pady=0)

    # Кнопка "Карты" справа
    map_button = ctk.CTkButton(button_frame, text="Карты", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=open_map)
    map_button.pack(side="right", padx=20)

def open_map():
    # Здесь можно добавить код для открытия карты
    print("Открытие карты...")

# Функции для кнопок, которые будут показывать данные из базы
def show_bus_schedule():
    columns = ("Маршрут", "Будние дни", "Выходные дни")
    data = get_bus_schedule()
    show_table(data, columns, "Расписание Автобусов")

def show_train_air_schedule():
    columns = ("Тип транспорта", "Назначение", "Время отправления", "Время прибытия")
    data = get_train_air_schedule()
    show_table(data, columns, "Расписание ЖД и Авиа транспорта")

def show_admin_reception():
    columns = ("Отдел", "Контактная информация", "Часы работы")
    data = get_admin_reception()
    show_table(data, columns, "Прием Администрации Нового Уренгоя")

def show_hospital_appointments():
    columns = ("Имя врача", "Специальность", "Доступные дни", "Часы приема")
    data = get_hospital_appointments()
    show_table(data, columns, "Запись на прием к врачу")

# Создаем главное окно
root = ctk.CTk()
root.title("Городская справка - Новый Уренгой")
root.geometry("600x500")
root.configure(fg_color="white")

# Загружаем логотип
logo_image = Image.open(logo_path)  # Путь к логотипу
logo = CTkImage(light_image=logo_image, size=(150, 150))

# Создаем виджет с логотипом
logo_label = ctk.CTkLabel(root, image=logo, text="", fg_color="white")
logo_label.pack(pady=10)

# Header bar с двумя кнопками
header_frame = ctk.CTkFrame(root, fg_color="#1E90FF", corner_radius=20)
header_frame.pack()

home_button = ctk.CTkButton(header_frame, text="На главную", command=open_home_page, fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20)
home_button.pack(side="left", padx=20)

personal_account_button = ctk.CTkButton(header_frame, text="Личный кабинет", command=show_personal_account, fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20)
personal_account_button.pack(side="left", padx=20)

# Фрейм для кнопок
button_frame = ctk.CTkFrame(root, fg_color="white")
button_frame.pack(pady=20)

# Универсальная функция для создания кнопок
def create_button(text, command):
    button = ctk.CTkButton(
        button_frame, text=text, command=command,
        width=150, height=50, corner_radius=20,  # Устанавливаем конкретные размеры для всех кнопок
        fg_color="white", text_color="black", font=("Arial", 13),
        anchor="center"  # Центрируем текст в кнопке
    )
    return button

# Кнопка "Расписание Автобусов"
bus_button = create_button("Расписание Автобусов", show_bus_schedule)
bus_button.grid(row=0, column=0, padx=10, pady=10)

# Кнопка "Расписание ЖД и Авиа транспорта"
train_air_button = create_button("Расписание ЖД и Авиа транспорта", show_train_air_schedule)
train_air_button.grid(row=0, column=1, padx=10, pady=10)

# Кнопка "Прием Администрации Нового Уренгоя"
admin_button = create_button("Прием Администрации Нового Уренгоя", show_admin_reception)
admin_button.grid(row=1, column=0, padx=10, pady=10)

# Кнопка "Запись на прием к врачу"
hospital_button = create_button("Запись на прием к врачу", show_hospital_appointments)
hospital_button.grid(row=1, column=1, padx=10, pady=10)

# Запуск основного цикла программы
root.mainloop()
