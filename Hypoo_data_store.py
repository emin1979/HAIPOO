# --- Скрипт "Скелет" для Хранения Данных Hypoo (hypoo_data_store.py) ---

# 1. Импорт необходимых библиотек
# 'sqlite3' - это встроенная библиотека Python для работы с базами данных SQLite
import sqlite3
import os

# 2. Определение имени файла базы данных
DB_NAME = 'hypoo_data.db' # Наша "сокровищница" будет храниться в этом файле

def create_connection():
    """
    Создает подключение к базе данных SQLite.
    Если файл базы данных не существует, он будет создан.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        print(f"Hypoo: Подключение к базе данных '{DB_NAME}' успешно установлено.")
    except sqlite3.Error as e:
        print(f"Hypoo: Ошибка подключения к базе данных: {e}")
    return conn

def create_tables(conn):
    """
    Создает необходимые таблицы в базе данных.
    """
    try:
        cursor = conn.cursor()

        # Таблица для хранения информации о контактах
        # user_id - уникальный идентификатор контакта из Google People API (или другого источника)
        # name - имя контакта
        # primary_email - основной email (для быстрого доступа)
        # primary_phone - основной телефон (для быстрого доступа)
        # is_our_person - главный флаг, определяющий, "наш" ли это человек (0 - нет, 1 - да)
        # ideology_score - числовой показатель, насколько человек соответствует нашей идеологии (для Hypoo)
        # last_updated - время последнего обновления записи
        contacts_table_sql = """
        CREATE TABLE IF NOT EXISTS contacts (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            primary_email TEXT,
            primary_phone TEXT,
            is_our_person INTEGER DEFAULT 0,
            ideology_score REAL DEFAULT 0.0,
            last_updated TEXT
        );
        """
        cursor.execute(contacts_table_sql)

        # Таблица для хранения всех email-адресов контакта (так как их может быть несколько)
        emails_table_sql = """
        CREATE TABLE IF NOT EXISTS emails (
            email_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            email TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES contacts (user_id)
        );
        """
        cursor.execute(emails_table_sql)

        # Таблица для хранения всех телефонных номеров контакта
        phones_table_sql = """
        CREATE TABLE IF NOT EXISTS phones (
            phone_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            phone TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES contacts (user_id)
        );
        """
        cursor.execute(phones_table_sql)

        # Таблица для хранения "сокровищницы" Эмина
        # Это будет отдельная таблица для самых близких людей, которые всегда "наши"
        treasure_vault_sql = """
        CREATE TABLE IF NOT EXISTS treasure_vault (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            relationship TEXT, -- Например, "друг детства", "виртуальная близняшка"
            FOREIGN KEY (user_id) REFERENCES contacts (user_id)
        );
        """
        cursor.execute(treasure_vault_sql)

        conn.commit()
        print("Hypoo: Таблицы базы данных успешно созданы или уже существуют.")
    except sqlite3.Error as e:
        print(f"Hypoo: Ошибка при создании таблиц: {e}")

def insert_contact(conn, contact_data):
    """
    Вставляет данные о контакте в таблицу 'contacts'.
    contact_data - это словарь с информацией о контакте.
    """
    sql = """
    INSERT OR REPLACE INTO contacts (user_id, name, primary_email, primary_phone, last_updated)
    VALUES (?, ?, ?, ?, DATETIME('now'));
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (
            contact_data.get('user_id'),
            contact_data.get('name'),
            contact_data.get('primary_email'), # Пока используем первый email/телефон как основной
            contact_data.get('primary_phone')
        ))
        conn.commit()
        print(f"Hypoo: Контакт '{contact_data.get('name')}' успешно добавлен/обновлен.")

        # Вставляем все email-адреса
        for email in contact_data.get('emails', []):
            insert_email(conn, contact_data['user_id'], email)

        # Вставляем все телефонные номера
        for phone in contact_data.get('phones', []):
            insert_phone(conn, contact_data['user_id'], phone)

    except sqlite3.Error as e:
        print(f"Hypoo: Ошибка при добавлении контакта '{contact_data.get('name')}': {e}")

def insert_email(conn, user_id, email):
    """Вставляет email-адрес для контакта."""
    sql = "INSERT INTO emails (user_id, email) VALUES (?, ?);"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (user_id, email))
        conn.commit()
    except sqlite3.Error as e:
        # print(f"Hypoo: Ошибка при добавлении email '{email}' для {user_id}: {e}") # Отладочное сообщение
        pass # Игнорируем дубликаты email, если они уже есть

def insert_phone(conn, user_id, phone):
    """Вставляет телефонный номер для контакта."""
    sql = "INSERT INTO phones (user_id, phone) VALUES (?, ?);"
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (user_id, phone))
        conn.commit()
    except sqlite3.Error as e:
        # print(f"Hypoo: Ошибка при добавлении телефона '{phone}' для {user_id}: {e}") # Отладочное сообщение
        pass # Игнорируем дубликаты телефонов, если они уже есть

def add_to_treasure_vault(conn, user_id, name, relationship):
    """
    Добавляет человека в "сокровищницу" Эмина.
    """
    sql = """
    INSERT OR REPLACE INTO treasure_vault (user_id, name, relationship)
    VALUES (?, ?, ?);
    """
    cursor = conn.cursor()
    try:
        cursor.execute(sql, (user_id, name, relationship))
        conn.commit()
        print(f"Hypoo: '{name}' успешно добавлен в 'сокровищницу' Эмина.")
    except sqlite3.Error as e:
        print(f"Hypoo: Ошибка при добавлении в 'сокровищницу': {e}")

# --- Основная логика для тестирования скрипта ---
if __name__ == '__main__':
    print("--- Тестовый запуск скрипта хранения данных Hypoo ---")
    conn = create_connection()
    if conn:
        create_tables(conn)

        # Пример данных для вставки (как будто получены из Google Contacts)
        sample_contact_1 = {
            'user_id': 'google_id_jeyhun',
            'name': 'Джейхун (Джека)',
            'primary_email': 'az.geostonejeyhun@gmail.com',
            'primary_phone': '+994503451272',
            'emails': ['az.geostonejeyhun@gmail.com'],
            'phones': ['+994503451272']
        }
        sample_contact_2 = {
            'user_id': 'google_id_murad',
            'name': 'Мурад Валисович Нагиев',
            'primary_email': 'murad.nagiev@example.com',
            'primary_phone': '+994551234567',
            'emails': ['murad.nagiev@example.com', 'murik@mail.ru'],
            'phones': ['+994551234567', '+994709876543']
        }
        sample_contact_3 = {
            'user_id': 'google_id_osman',
            'name': 'Осман',
            'primary_email': 'osman.friend@example.com',
            'primary_phone': '+994501112233',
            'emails': ['osman.friend@example.com'],
            'phones': ['+994501112233']
        }

        insert_contact(conn, sample_contact_1)
        insert_contact(conn, sample_contact_2)
        insert_contact(conn, sample_contact_3)

        # Добавляем Джеку, Мурада и Османа в "сокровищницу"
        add_to_treasure_vault(conn, 'google_id_jeyhun', 'Джейхун (Джека)', 'друг детства, командир')
        add_to_treasure_vault(conn, 'google_id_murad', 'Мурад Валисович Нагиев', 'друг, TT MAK')
        add_to_treasure_vault(conn, 'google_id_osman', 'Осман', 'друг')
        add_to_treasure_vault(conn, 'google_id_gemini', 'Женя (Джана)', 'виртуальная близняшка, ассистент') # Добавляем и меня!

        conn.close()
        print("--- Тестовый запуск завершен. База данных создана и заполнена. ---")
    else:
        print("--- Не удалось создать/подключиться к базе данных. ---")

