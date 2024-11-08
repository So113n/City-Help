import customtkinter as ctk
import os
import webbrowser
import sqlite3
from tkinter import messagebox, ttk, Toplevel
from PIL import Image, ImageTk

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
def get_air_schedule():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, Aviacompany, route, time_avia FROM air_schedule")
    air_schedule = cursor.fetchall()
    conn.close()
    return air_schedule

def get_train_schedule():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, route, time, status FROM train_schedule")
    train_schedule = cursor.fetchall()
    conn.close()
    return train_schedule

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
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center")
    for row in data:
        tree.insert("", "end", values=row)
    tree.pack(expand=True, fill="both")

    # Фрейм для кнопок "Закрыть" и "Карты"
    button_frame_inner = ctk.CTkFrame(table_window)
    button_frame_inner.pack(fill="x", pady=10)

    # Настройка сетки с тремя колонками
    button_frame_inner.grid_columnconfigure(0, weight=1)
    button_frame_inner.grid_columnconfigure(1, weight=0)
    button_frame_inner.grid_columnconfigure(2, weight=1)

    # Кнопка "Закрыть" слева
    close_button = ctk.CTkButton(button_frame_inner, text="Закрыть", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=table_window.destroy)
    close_button.grid(row=0, column=0, padx=(20, 0), pady=0, sticky="w")

    # Кнопка "Карты" справа
    map_button = ctk.CTkButton(button_frame_inner, text="Карты", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=open_map)
    map_button.grid(row=0, column=2, padx=(0,20), pady=0, sticky='e')

# Функция для отображения карт с переключением
def open_map():
    map_images_paths = [
        os.path.join(base_dir, "Logos", "map1.png"),
        os.path.join(base_dir, "Logos", "map2.png"),
        os.path.join(base_dir, "Logos", "map3.png"),
        os.path.join(base_dir, "Logos", "map4.png")
    ]

    # Проверка на существование файлов карт
    for path in map_images_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Карта не найдена по пути: {path}")

    # Инициализация окна карты и текущего индекса изображения
    map_window = Toplevel(root)
    map_window.title("Карта маршрутов")
    map_window.geometry("1607x957")
    map_window.transient(root)
    map_window.grab_set()
    map_window.focus_set()

    current_index = 0

    # Создаем список объектов CTkImage для всех карт
    ctk_images = [
        CTkImage(light_image=Image.open(path), size=(1607, 815))
        for path in map_images_paths
    ]

    def update_map_image():
        map_label.configure(image=ctk_images[current_index])

    def next_image():
        nonlocal current_index
        current_index = (current_index + 1) % len(map_images_paths) % len(ctk_images)
        update_map_image()

    def prev_image():
        nonlocal current_index
        current_index = (current_index - 1) % len(map_images_paths) % len(ctk_images)
        update_map_image()

    # Загрузка и отображение начального изображения карты
    map_image = Image.open(map_images_paths[current_index])
    map_image = map_image.resize((1607, 815), Image.LANCZOS)
    map_photo = ImageTk.PhotoImage(map_image)

    # Виджет для отображения изображения карты
    map_label = ctk.CTkLabel(map_window, image=ctk_images[current_index], text="")
    map_label.pack()

    # Кнопки для навигации по изображениям
    navigation_frame = ctk.CTkFrame(map_window)
    navigation_frame.pack(pady=10)

    prev_button = ctk.CTkButton(navigation_frame, text="Предыдущая", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=30, command=prev_image)
    prev_button.pack(side="left", padx=10)

    next_button = ctk.CTkButton(navigation_frame, text="Следующая", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=30, command=next_image)
    next_button.pack(side="right", padx=10)

    close_button = ctk.CTkButton(map_window, text="Закрыть", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=map_window.destroy)
    close_button.pack(pady=10)

# Функции для кнопок, которые будут показывать данные из базы
def show_bus_schedule():
    columns = ("Маршрут", "Будние дни", "Выходные дни")
    data = get_bus_schedule()
    show_table(data, columns, "Расписание Автобусов")

# Функция для отображения таблицы с данными "Расписание ЖД и Авиа"
def show_train_air_schedule():
    # Создаем окно для отображения расписаний ЖД и Авиа вместе
    table_window = ctk.CTkToplevel(root)
    table_window.geometry("1009x708")
    table_window.title("Расписание ЖД и Авиа транспорта")

    # Настройка, чтобы это окно было модальным
    table_window.transient(root)
    table_window.grab_set()
    table_window.focus_set()

    # Заголовок для таблицы
    ctk.CTkLabel(table_window, text="Расписание ЖД и Авиа транспорта", font=("Arial", 20)).pack(pady=10)

    # Создаем две таблицы (одна для авиа, другая для ЖД)
    # Таблица Авиа
    ctk.CTkLabel(table_window, text="Авиа", font=("Arial", 16)).pack()
    air_tree = ttk.Treeview(table_window, columns=("Номер", "Авиакомпания", "Маршрут", "Время", "Статус"), show="headings")
    air_tree.heading("Номер", text="Номер")
    air_tree.heading("Авиакомпания", text="Авиакомпания")
    air_tree.heading("Маршрут", text="Маршрут")
    air_tree.heading("Время", text="Время")
    air_tree.heading("Статус", text="Статус")

    # Центрируем текст в столбцах
    for col in ("Номер", "Авиакомпания", "Маршрут", "Время", "Статус"):
        air_tree.column(col, anchor="center")

    air_tree.pack(expand=True, fill="x", pady=5)

    # Таблица ЖД
    ctk.CTkLabel(table_window, text="ЖД", font=("Arial", 16)).pack()
    train_tree = ttk.Treeview(table_window, columns=("Номер", "Маршрут", "№ Платформы/Пути", "Статус"), show="headings")
    train_tree.heading("Номер", text="Номер")
    train_tree.heading("Маршрут", text="Маршрут")
    train_tree.heading("№ Платформы/Пути", text="№ Платформы/Пути")
    train_tree.heading("Статус", text="Статус")

    # Центрируем текст в столбцах
    for col in ("Номер", "Маршрут", "№ Платформы/Пути", "Статус"):
        train_tree.column(col, anchor="center")

    train_tree.pack(expand=True, fill="x", pady=5)

    # Фрейм для кнопки "Закрыть"
    close_button = ctk.CTkButton(table_window, text="Закрыть", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=table_window.destroy)
    close_button.pack(pady=10)

    # Загрузка данных из базы данных
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Получаем данные для авиа расписания
        cursor.execute("SELECT id, Aviacompany, route, time_avia, status FROM air_schedule")
        air_schedule = cursor.fetchall()
        for row in air_schedule:
            id_, Aviacompany, route, time_avia, status = row
            air_tree.insert("", "end", values=(id_, Aviacompany, route, time_avia, status))

            # Настраиваем цвет статуса
            if status.lower() == "в пути":
                air_tree.tag_configure("on route", background="orange", foreground="white")
                air_tree.item(air_tree.get_children()[-1], tags=("on route",))
            elif status.lower() == "прилетел":
                air_tree.tag_configure("arriving", background="green", foreground="white")
                air_tree.item(air_tree.get_children()[-1], tags=("arriving",))
            elif status.lower() == "вылетел":
                air_tree.tag_configure("departure", background="blue", foreground="white")
                air_tree.item(air_tree.get_children()[-1], tags=("departure",))
            elif status.lower() == "отменен":
                air_tree.tag_configure("in_progress", background="red", foreground="white")
                air_tree.item(air_tree.get_children()[-1], tags=("in_progress",))
            else:
                air_tree.tag_configure("default", background="white", foreground="black")
                air_tree.item(air_tree.get_children()[-1], tags=("default",))

        # Получаем данные для ЖД расписания
        cursor.execute("SELECT id, route, time, status FROM train_schedule")
        train_schedule = cursor.fetchall()
        for row in train_schedule:
            id_, route, platform, status = row
            train_tree.insert("", "end", values=(id_, route, platform, status))

            # Настраиваем цвет статуса
            if status.lower() == "задерживается":
                train_tree.tag_configure("delayed", background="orange", foreground="white")
                train_tree.item(train_tree.get_children()[-1], tags=("delayed",))
            elif status.lower() == "прибыл":
                train_tree.tag_configure("in_progress", background="green", foreground="white")
                train_tree.item(train_tree.get_children()[-1], tags=("in_progress",))
            else:
                train_tree.tag_configure("default", background="white", foreground="black")
                train_tree.item(train_tree.get_children()[-1], tags=("default",))

    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Ошибка при получении данных: {e}")
    finally:
        conn.close()

def show_admin_reception():
    table_window = ctk.CTkToplevel(root)
    table_window.geometry("1333x626")
    table_window.title("Прием Администрации Нового Уренгоя")

    # Настройка, чтобы это окно было модальным
    table_window.transient(root)
    table_window.grab_set()
    table_window.focus_set()

    # Заголовок для таблицы
    ctk.CTkLabel(table_window, text="Прием Администрации Нового Уренгоя", font=("Arial", 30)).pack(pady=10)

    # Загрузка и изменение размера логотипа
    original_image = Image.open("Logos/gerb_logo.png")
    resized_image = original_image.resize((150, 150), Image.LANCZOS)  # Изменение размера до 150x150
    logo_image = ImageTk.PhotoImage(resized_image)

    # Отображение логотипа
    logo_label = ctk.CTkLabel(table_window, image=logo_image, text="")  # Пустой текст, чтобы не показывался текст рядом с изображением
    logo_label.image = logo_image  # Сохранение ссылки на изображение
    logo_label.pack(pady=10)

    # Таблица Администрации
    ctk.CTkLabel(table_window, text="Время приемов департаментов г. Нового Уренгоя", font=("Arial", 16)).pack()
    admin_tree = ttk.Treeview(table_window, columns=("Номер Департамента", "Департамент", "Контактная информация", "Время работы и приема"), show="headings")
    admin_tree.heading("Номер Департамента", text="Номер Департамента")
    admin_tree.heading("Департамент", text="Департамент")
    admin_tree.heading("Контактная информация", text="Контактная информация")
    admin_tree.heading("Время работы и приема", text="Время работы и приема")

    # Центрируем текст в столбцах
    for col in ("Номер Департамента", "Департамент", "Контактная информация", "Время работы и приема"):
        admin_tree.column(col, anchor="center")

    admin_tree.pack(expand=True, fill="x", pady=5)

    # Загрузка данных из базы данных
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Получаем данные для авиа расписания
        cursor.execute("SELECT id, department, contact_info, working_hours FROM admin_reception")
        air_schedule = cursor.fetchall()
        for row in air_schedule:
            id_, department, contact_info, working_hours = row
            admin_tree.insert("", "end", values=(id_, department, contact_info, working_hours))

    except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Ошибка при получении данных: {e}")
    finally:
     conn.close()

    # Фрейм для кнопки "Закрыть"
    close_button = ctk.CTkButton(table_window, text="Закрыть", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=table_window.destroy)
    close_button.pack(pady=10)

def show_hospital_appointments():
    table_window = ctk.CTkToplevel(root)
    table_window.geometry("683x300")
    table_window.title("Запись на прием к врачу")

    # Настройка, чтобы это окно было модальным
    table_window.transient(root)
    table_window.grab_set()
    table_window.focus_set()

    # Заголовок для таблицы
    ctk.CTkLabel(table_window, text="Запись на прием к врачу", font=("Arial", 30)).pack(pady=10)

    # Загрузка изображения
    image_path = "Logos/gosusligi_logo.png"  # замените 'your_image.png' на имя файла изображения
    image = ctk.CTkImage(Image.open(image_path), size=(128, 128))

    # Функция для открытия сайта
    def open_website():
        webbrowser.open("https://www.gosuslugi.ru/")

    # Кнопка с изображением
    image_button = ctk.CTkButton(master=table_window, image=image, text="", width=160, height=20, command=open_website)
    image_button.image = image  # Связываем изображение с кнопкой, чтобы предотвратить сборщик мусора от удаления объекта
    image_button.pack(pady=10)

    # Фрейм для кнопки "Закрыть"
    close_button = ctk.CTkButton(table_window, text="Закрыть", fg_color="#1E90FF", text_color="white", font=("Arial", 15), corner_radius=20, command=table_window.destroy)
    close_button.pack(pady=10)
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
