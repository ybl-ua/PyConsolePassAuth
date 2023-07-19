import bdb
import sqlite3
import os
import stdiomask
import string


# Фунція очищення консолі
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


# Функція створення бази даних користувачів
def create_users_database():
    # Створюємо базу данних користувачів
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    # Таблиця з даними користувачів
    cur.execute("""CREATE TABLE IF NOT EXISTS userdata(
                   login TEXT PRIMARY KEY,
                   password TEXT,
                   adminstatus BOOLEAN,
                   banned BOOLEAN,
                   password_limit BOOLEAN);
    """)
    # Якщо не існує облікового запису admin:admin, то свторюємо його
    try:
        cur.execute("""INSERT INTO userdata(login, password, adminstatus, banned, password_limit) 
                       VALUES(?, ?, ?, ?, ?)""", ('admin', '', True, False, False))
    except sqlite3.IntegrityError:
        pass
    db.commit()  # Зберігаємо зміни


# Функція для реєстрації нового користувача
def add_user_to_database(login, password, adminstatus, banned, password_limit):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    try:
        cur.execute("""INSERT INTO userdata(login, password, adminstatus, banned, password_limit) 
           VALUES(?, ?, ?, ?, ?)""", (login, password, adminstatus, banned, password_limit))
        db.commit()
        print(f'Обліковий запис {login} створено')
        return True
    except sqlite3.IntegrityError:
        clear()
        print('Логін вже використовується. Спробуйте ще раз')
        return False


# Функція перевірки безпечності пароля (він повинен мати літери, цифри та розділові знаки)
def password_is_secure(password):
    letter, digit, punctuation = False, False, False
    for symbol in password:
        if symbol in string.digits:
            digit = True
        elif symbol in string.ascii_letters:
            letter = True
        elif symbol in string.punctuation:
            punctuation = True
    return letter and digit and punctuation


# Функція перевірки аккаунту в бд та виконання входу
def user_is_exist(login, password):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute(f"""SELECT * FROM userdata
                           WHERE login = ?;""", (login,))
    account = cur.fetchone()
    # Перевірка наявності логіна в базі данних та правильності пароля
    if account and password == account[1]:
        clear()
        print('Вхід виконано')
        return account
    else:
        clear()
        print('Логін або пароль вказано невірно')
        return False


# Функція зміни паролю в бд
def update_db(login, password):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute("""UPDATE userdata 
                   SET password = ?
                   WHERE login = ?;""", (password, login))
    db.commit()


# Функція для отримання списку користувачів з бд
def bd_get_usernames():
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute('SELECT login, adminstatus, banned, password_limit FROM userdata')
    return cur.fetchall()


# Функція блокування користувачів
def bd_ban_user(login, ban):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute("""UPDATE userdata 
                   SET banned = ?
                   WHERE login = ?;""", (ban, login))
    db.commit()


# Функція для зміни обмежень паролю
def bd_change_password_setting(login, value):
    db = sqlite3.connect('users.db')
    cur = db.cursor()
    cur.execute("""UPDATE userdata 
                   SET password_limit = ?
                   WHERE login = ?;""", (value, login))
    db.commit()


if __name__ == '__main__':
    create_users_database()
